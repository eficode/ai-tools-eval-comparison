#!/usr/bin/env python3
"""
MCP server for Robot Framework 7.4.1 Documentation
Fetches and provides searchable access to Robot Framework 7.4.1 documentation.

Tools:
  - fetch_rf_documentation() - Downloads RF 7.4.1 docs (HTML) for all standard libraries
  - search_rf_documentation(query, max_results) - Search the documentation
  - get_library_keywords(library_name, filter_pattern) - List keywords from a specific library
  - get_all_keywords(filter_pattern) - List all keywords from all standard libraries
  - get_builtin_keywords(filter_pattern) - List BuiltIn keywords (backward compat)
  - get_keyword_documentation(keyword_name, library_name) - Get detailed docs for a specific keyword
  - check_keyword_availability(keyword_name) - Check if keyword exists in any standard library
  - get_documentation_url(topic) - Get direct URLs to RF documentation
"""
import os
import re
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from html.parser import HTMLParser

from mcp.server.fastmcp import FastMCP

APP_NAME = "rf-docs-mcp"
RF_VERSION = "7.4.1"
RF_DOCS_URL = f"https://robotframework.org/robotframework/{RF_VERSION}/RobotFrameworkUserGuide.html"
RF_BASE_LIB_URL = f"https://robotframework.org/robotframework/{RF_VERSION}/libraries"

# Standard libraries to fetch
STANDARD_LIBRARIES = [
    "BuiltIn",
    "Collections", 
    "DateTime",
    "OperatingSystem",
    "Process",
    "Screenshot",
    "String",
    "Telnet",
    "XML"
]

# Storage paths
CACHE_DIR = Path(os.getenv("RF_DOCS_CACHE", "/tmp/rf_docs_cache"))
DOCS_FILE = CACHE_DIR / f"RobotFrameworkUserGuide_{RF_VERSION}.html"
INDEX_FILE = CACHE_DIR / f"docs_index_{RF_VERSION}.json"
KEYWORDS_INDEX = CACHE_DIR / f"all_keywords_{RF_VERSION}.json"

# Installed library docs location
LIBRARY_DOCS_DIR = Path("/app/docs")

mcp = FastMCP(APP_NAME)


class DocumentationParser(HTMLParser):
    """Parse Robot Framework documentation HTML to extract structured content."""
    
    def __init__(self):
        super().__init__()
        self.sections = []
        self.current_section = None
        self.current_content = []
        self.in_section = False
        self.section_level = 0
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        # Detect section headers (h1, h2, h3, h4)
        if tag in ['h1', 'h2', 'h3', 'h4']:
            # Save previous section
            if self.current_section:
                self.current_section['content'] = ' '.join(self.current_content).strip()
                self.sections.append(self.current_section)
            
            # Start new section
            self.section_level = int(tag[1])
            section_id = attrs_dict.get('id', '')
            self.current_section = {
                'id': section_id,
                'level': self.section_level,
                'title': '',
                'content': ''
            }
            self.current_content = []
            self.in_section = True
            
    def handle_endtag(self, tag):
        if tag in ['h1', 'h2', 'h3', 'h4']:
            self.in_section = False
            
    def handle_data(self, data):
        if self.in_section and self.current_section:
            # This is the section title
            self.current_section['title'] = data.strip()
        elif self.current_section:
            # This is section content
            text = data.strip()
            if text:
                self.current_content.append(text)
    
    def get_sections(self):
        # Save last section
        if self.current_section:
            self.current_section['content'] = ' '.join(self.current_content).strip()
            self.sections.append(self.current_section)
        return self.sections


def _download_file(url: str, target_path: Path, user_agent: str = None) -> Dict:
    """Download a file from URL with proper error handling."""
    try:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create request with user agent to avoid 403
        headers = {'User-Agent': user_agent or 'Mozilla/5.0 (compatible; RF-MCP-Docs/1.0)'}
        req = Request(url, headers=headers)
        
        with urlopen(req, timeout=30) as response:
            content = response.read()
            target_path.write_bytes(content)
            
        return {
            "success": True,
            "path": str(target_path),
            "size_bytes": len(content),
            "url": url
        }
    except HTTPError as e:
        return {
            "success": False,
            "error": f"HTTP Error {e.code}: {e.reason}",
            "url": url
        }
    except URLError as e:
        return {
            "success": False,
            "error": f"URL Error: {e.reason}",
            "url": url
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "url": url
        }


def _parse_documentation() -> Dict:
    """Parse downloaded documentation and create searchable index."""
    if not DOCS_FILE.exists():
        return {"error": "Documentation not downloaded. Call fetch_rf_documentation first."}
    
    try:
        html_content = DOCS_FILE.read_text(encoding='utf-8')
        parser = DocumentationParser()
        parser.feed(html_content)
        sections = parser.get_sections()
        
        # Create searchable index
        index = {
            "version": RF_VERSION,
            "parsed_at": datetime.now().isoformat(),
            "total_sections": len(sections),
            "sections": sections
        }
        
        # Save index
        INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
        INDEX_FILE.write_text(json.dumps(index, indent=2))
        
        return {
            "success": True,
            "sections_parsed": len(sections),
            "index_path": str(INDEX_FILE)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Parsing error: {str(e)}"
        }


def _parse_library_keywords(library_name: str) -> Dict:
    """Parse library documentation to extract keywords from embedded JSON."""
    library_file = CACHE_DIR / f"{library_name}_{RF_VERSION}.html"
    
    if not library_file.exists():
        return {"error": f"{library_name} documentation not downloaded."}
    
    try:
        html_content = library_file.read_text(encoding='utf-8')
        
        # The keywords are embedded in JavaScript as: libdoc = {...};
        # Find the start of libdoc object
        start_match = re.search(r'libdoc\s*=\s*\{', html_content)
        
        if not start_match:
            return {
                "success": False,
                "error": "Could not find libdoc in HTML"
            }
        
        # Extract JSON by counting braces
        start_pos = start_match.end() - 1  # Include the opening brace
        depth = 0
        in_string = False
        escape = False
        
        for i in range(start_pos, len(html_content)):
            char = html_content[i]
            
            if escape:
                escape = False
                continue
                
            if char == '\\':
                escape = True
                continue
                
            if char == '"' and not escape:
                in_string = not in_string
                continue
                
            if not in_string:
                if char == '{':
                    depth += 1
                elif char == '}':
                    depth -= 1
                    if depth == 0:
                        end_pos = i + 1
                        libdoc_json = html_content[start_pos:end_pos]
                        break
        else:
            return {
                "success": False,
                "error": "Could not find end of libdoc JSON"
            }
        
        # Parse the JSON
        libdoc_data = json.loads(libdoc_json)
        
        keywords = {}
        for kw_data in libdoc_data.get("keywords", []):
            name = kw_data.get("name", "")
            if not name:
                continue
                
            # Build arguments string from args array
            args_parts = []
            for arg in kw_data.get("args", []):
                arg_repr = arg.get("repr", "")
                if arg_repr:
                    args_parts.append(arg_repr)
            args_str = ", ".join(args_parts)
            
            # Extract short documentation (strip HTML)
            doc = kw_data.get("shortdoc", "")
            doc = re.sub(r'<[^>]+>', '', doc)  # Remove HTML tags
            doc = re.sub(r'``([^`]+)``', r'\1', doc)  # Convert rst code to plain
            
            keywords[name] = {
                "name": name,
                "id": name.replace(" ", "%20"),
                "args": args_str,
                "doc": doc,
                "library": library_name,
                "source": kw_data.get("source", ""),
                "lineno": kw_data.get("lineno", "")
            }
        
        return {
            "success": True,
            "library": library_name,
            "keywords": keywords,
            "total_keywords": len(keywords)
        }
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"JSON parsing error: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Parsing error: {str(e)}"
        }


@mcp.tool()
def fetch_rf_documentation(force_refresh: bool = False) -> Dict:
    """
    Download Robot Framework 7.4.1 documentation for all standard libraries.
    
    Parameters:
      - force_refresh: If True, re-download even if cached (default: False)
    
    Returns:
      - success: Boolean indicating if download succeeded
      - version: RF version (always 7.4.1)
      - files_downloaded: List of downloaded files
      - cache_location: Where files are stored
      - libraries: Dictionary of library parsing results
    """
    results = {
        "version": RF_VERSION,
        "cache_location": str(CACHE_DIR),
        "files_downloaded": [],
        "libraries": {}
    }
    
    # Download User Guide
    if force_refresh or not DOCS_FILE.exists():
        result = _download_file(RF_DOCS_URL, DOCS_FILE)
        results["user_guide"] = result
        if result["success"]:
            results["files_downloaded"].append("RobotFrameworkUserGuide.html")
    else:
        results["user_guide"] = {
            "success": True,
            "cached": True,
            "path": str(DOCS_FILE)
        }
    
    # Parse and index User Guide documentation
    if DOCS_FILE.exists():
        parse_result = _parse_documentation()
        results["indexing"] = parse_result
    
    # Download and parse all standard libraries
    all_keywords = {}
    total_keywords = 0
    
    for library_name in STANDARD_LIBRARIES:
        library_file = CACHE_DIR / f"{library_name}_{RF_VERSION}.html"
        library_url = f"{RF_BASE_LIB_URL}/{library_name}.html"
        
        # Download library docs
        if force_refresh or not library_file.exists():
            result = _download_file(library_url, library_file)
            if result["success"]:
                results["files_downloaded"].append(f"{library_name}.html")
        
        # Parse keywords
        if library_file.exists():
            keywords_result = _parse_library_keywords(library_name)
            results["libraries"][library_name] = {
                "success": keywords_result.get("success", False),
                "total_keywords": keywords_result.get("total_keywords", 0)
            }
            
            if keywords_result.get("success"):
                all_keywords[library_name] = keywords_result.get("keywords", {})
                total_keywords += keywords_result.get("total_keywords", 0)
    
    # Save combined keywords index
    if all_keywords:
        keywords_index = {
            "version": RF_VERSION,
            "parsed_at": datetime.now().isoformat(),
            "total_libraries": len(all_keywords),
            "total_keywords": total_keywords,
            "libraries": all_keywords
        }
        KEYWORDS_INDEX.write_text(json.dumps(keywords_index, indent=2))
        results["keywords_index"] = {
            "success": True,
            "path": str(KEYWORDS_INDEX),
            "total_libraries": len(all_keywords),
            "total_keywords": total_keywords
        }
    
    results["success"] = results.get("user_guide", {}).get("success", False)
    
    return results


@mcp.tool()
def search_rf_documentation(query: str, max_results: int = 10) -> Dict:
    """
    Search Robot Framework 7.4.1 documentation.
    
    Parameters:
      - query: Search term or phrase
      - max_results: Maximum number of results to return (default: 10)
    
    Returns:
      - results: List of matching sections with relevance scores
      - total_matches: Total number of matches found
    """
    if not INDEX_FILE.exists():
        return {
            "error": "Documentation index not found. Call fetch_rf_documentation first.",
            "hint": "Run fetch_rf_documentation() to download and index docs"
        }
    
    try:
        index_data = json.loads(INDEX_FILE.read_text())
        sections = index_data.get("sections", [])
        
        query_lower = query.lower()
        results = []
        
        for section in sections:
            title = section.get("title", "").lower()
            content = section.get("content", "").lower()
            
            # Simple relevance scoring
            title_matches = title.count(query_lower)
            content_matches = content.count(query_lower)
            
            if title_matches > 0 or content_matches > 0:
                relevance = (title_matches * 10) + content_matches
                
                results.append({
                    "title": section.get("title", ""),
                    "id": section.get("id", ""),
                    "level": section.get("level", 0),
                    "relevance": relevance,
                    "content_preview": section.get("content", "")[:300] + "...",
                    "url": f"{RF_DOCS_URL}#{section.get('id', '')}"
                })
        
        # Sort by relevance
        results.sort(key=lambda x: x["relevance"], reverse=True)
        
        return {
            "version": RF_VERSION,
            "query": query,
            "total_matches": len(results),
            "results": results[:max_results]
        }
    except Exception as e:
        return {"error": f"Search failed: {str(e)}"}


@mcp.tool()
def get_library_keywords(library_name: str = "BuiltIn", filter_pattern: Optional[str] = None) -> Dict:
    """
    Get list of keywords from a specific Robot Framework 7.4.1 library.
    
    Parameters:
      - library_name: Library name (BuiltIn, Collections, String, etc.) (default: BuiltIn)
      - filter_pattern: Optional regex pattern to filter keyword names
    
    Returns:
      - version: RF version (7.4.1)
      - library: Library name
      - total_keywords: Total number of keywords
      - keywords: List of keyword names and brief descriptions
    """
    if library_name not in STANDARD_LIBRARIES:
        return {
            "error": f"Unknown library: {library_name}",
            "available_libraries": STANDARD_LIBRARIES
        }
    
    # Ensure we have the data
    library_file = CACHE_DIR / f"{library_name}_{RF_VERSION}.html"
    if not library_file.exists():
        fetch_result = fetch_rf_documentation()
        if not fetch_result.get("success"):
            return {"error": f"Failed to fetch {library_name} documentation"}
    
    keywords_result = _parse_library_keywords(library_name)
    
    if not keywords_result.get("success"):
        return keywords_result
    
    keywords = keywords_result["keywords"]
    
    # Apply filter if provided
    if filter_pattern:
        try:
            pattern = re.compile(filter_pattern, re.IGNORECASE)
            keywords = {k: v for k, v in keywords.items() if pattern.search(k)}
        except re.error as e:
            return {"error": f"Invalid regex pattern: {str(e)}"}
    
    # Format for output
    keyword_list = [
        {
            "name": k,
            "library": library_name,
            "args": v["args"],
            "description": v["doc"][:200]
        }
        for k, v in sorted(keywords.items())
    ]
    
    return {
        "version": RF_VERSION,
        "library": library_name,
        "total_keywords": len(keyword_list),
        "keywords": keyword_list
    }


@mcp.tool()
def get_all_keywords(filter_pattern: Optional[str] = None) -> Dict:
    """
    Get list of all keywords from all Robot Framework 7.4.1 standard libraries.
    
    Parameters:
      - filter_pattern: Optional regex pattern to filter keyword names
    
    Returns:
      - version: RF version (7.4.1)
      - total_keywords: Total number of keywords across all libraries
      - libraries: Dictionary of libraries with their keywords
    """
    if not KEYWORDS_INDEX.exists():
        fetch_result = fetch_rf_documentation()
        if not fetch_result.get("success"):
            return {"error": "Failed to fetch documentation"}
    
    try:
        index_data = json.loads(KEYWORDS_INDEX.read_text())
        all_libraries = index_data.get("libraries", {})
        
        # Apply filter if provided
        if filter_pattern:
            try:
                pattern = re.compile(filter_pattern, re.IGNORECASE)
                filtered_libraries = {}
                for lib_name, keywords in all_libraries.items():
                    filtered_kw = {k: v for k, v in keywords.items() if pattern.search(k)}
                    if filtered_kw:
                        filtered_libraries[lib_name] = filtered_kw
                all_libraries = filtered_libraries
            except re.error as e:
                return {"error": f"Invalid regex pattern: {str(e)}"}
        
        # Format for output
        result_libraries = {}
        total_keywords = 0
        
        for lib_name, keywords in all_libraries.items():
            keyword_list = [
                {
                    "name": k,
                    "library": lib_name,
                    "args": v["args"],
                    "description": v["doc"][:200]
                }
                for k, v in sorted(keywords.items())
            ]
            result_libraries[lib_name] = keyword_list
            total_keywords += len(keyword_list)
        
        return {
            "version": RF_VERSION,
            "total_keywords": total_keywords,
            "total_libraries": len(result_libraries),
            "libraries": result_libraries
        }
    except Exception as e:
        return {"error": f"Failed to read keywords index: {str(e)}"}


@mcp.tool()
def get_builtin_keywords(filter_pattern: Optional[str] = None) -> Dict:
    """
    Get list of all BuiltIn keywords in Robot Framework 7.4.1.
    (Shortcut for get_library_keywords with library_name="BuiltIn")
    
    Parameters:
      - filter_pattern: Optional regex pattern to filter keyword names
    
    Returns:
      - version: RF version (7.4.1)
      - total_keywords: Total number of keywords
      - keywords: List of keyword names and brief descriptions
    """
    return get_library_keywords("BuiltIn", filter_pattern)


@mcp.tool()
def get_keyword_documentation(keyword_name: str, library_name: Optional[str] = None) -> Dict:
    """
    Get detailed documentation for a specific keyword.
    
    Parameters:
      - keyword_name: Name of the keyword (case-insensitive)
      - library_name: Optional library name (if None, searches all libraries)
    
    Returns:
      - keyword: Keyword name
      - library: Library containing the keyword
      - available: Whether keyword exists in RF 7.4.1
      - documentation: Full keyword documentation
      - arguments: Keyword arguments
    """
    if not KEYWORDS_INDEX.exists():
        fetch_result = fetch_rf_documentation()
        if not fetch_result.get("success"):
            return {"error": "Failed to fetch documentation"}
    
    try:
        index_data = json.loads(KEYWORDS_INDEX.read_text())
        all_libraries = index_data.get("libraries", {})
        
        # Filter libraries if specified
        if library_name:
            if library_name not in all_libraries:
                return {
                    "error": f"Library '{library_name}' not found",
                    "available_libraries": list(all_libraries.keys())
                }
            libraries_to_search = {library_name: all_libraries[library_name]}
        else:
            libraries_to_search = all_libraries
        
        # Case-insensitive search
        keyword_name_lower = keyword_name.lower().replace("_", " ").replace("-", " ")
        
        for lib_name, keywords in libraries_to_search.items():
            for k, v in keywords.items():
                if k.lower().replace("_", " ").replace("-", " ") == keyword_name_lower:
                    lib_url = f"{RF_BASE_LIB_URL}/{lib_name}.html"
                    return {
                        "version": RF_VERSION,
                        "keyword": k,
                        "library": lib_name,
                        "available": True,
                        "arguments": v["args"],
                        "documentation": v["doc"],
                        "url": f"{lib_url}#{v['id']}"
                    }
        
        return {
            "version": RF_VERSION,
            "keyword": keyword_name,
            "available": False,
            "message": f"Keyword '{keyword_name}' not found in any standard library for RF {RF_VERSION}",
            "hint": "Use get_all_keywords() to see all available keywords"
        }
    except Exception as e:
        return {"error": f"Failed to search keyword: {str(e)}"}


@mcp.tool()
def check_keyword_availability(keyword_name: str) -> Dict:
    """
    Quick check if a keyword exists in Robot Framework 7.4.1 (searches all standard libraries).
    
    Parameters:
      - keyword_name: Name of the keyword to check
    
    Returns:
      - available: Boolean indicating if keyword exists
      - version: RF version checked (7.4.1)
      - library: Library containing the keyword (if found)
      - keyword: The keyword name as found in docs (if available)
    """
    result = get_keyword_documentation(keyword_name)
    
    return {
        "version": RF_VERSION,
        "keyword_searched": keyword_name,
        "available": result.get("available", False),
        "library": result.get("library") if result.get("available") else None,
        "keyword_actual_name": result.get("keyword") if result.get("available") else None,
        "message": result.get("message", f"Keyword '{result.get('keyword')}' is available in {result.get('library')} library")
    }


@mcp.tool()
def get_documentation_url(topic: Optional[str] = None) -> Dict:
    """
    Get direct URLs to Robot Framework 7.4.1 documentation.
    
    Parameters:
      - topic: Optional topic (user_guide, builtin, releases)
    
    Returns:
      - version: RF version
      - urls: Dictionary of documentation URLs
    """
    urls = {
        "user_guide": RF_DOCS_URL,
        "builtin_library": f"{RF_BASE_LIB_URL}/BuiltIn.html",
        "release_notes": f"https://github.com/robotframework/robotframework/blob/master/doc/releasenotes/rf-{RF_VERSION}.rst",
        "all_libraries": f"https://robotframework.org/robotframework/{RF_VERSION}/libraries/",
        "standard_libraries": {
            "BuiltIn": f"{RF_BASE_LIB_URL}/BuiltIn.html",
            "Collections": f"{RF_BASE_LIB_URL}/Collections.html",
            "DateTime": f"{RF_BASE_LIB_URL}/DateTime.html",
            "OperatingSystem": f"{RF_BASE_LIB_URL}/OperatingSystem.html",
            "Process": f"{RF_BASE_LIB_URL}/Process.html",
            "Screenshot": f"{RF_BASE_LIB_URL}/Screenshot.html",
            "String": f"{RF_BASE_LIB_URL}/String.html",
            "Telnet": f"{RF_BASE_LIB_URL}/Telnet.html",
            "XML": f"{RF_BASE_LIB_URL}/XML.html"
        }
    }
    
    return {
        "version": RF_VERSION,
        "urls": urls if not topic else {topic: urls.get(topic, "Topic not found")}
    }




if __name__ == "__main__":
    mcp.run()
