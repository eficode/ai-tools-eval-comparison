#!/bin/bash
# Fast Start - Complete setup in one command!

################################################################################
# RF docs MCP Server - Fast Start
# 
# This script sets up everything you need:
# 1. Generates MCP configuration for your IDE
# 2. Starts services via docker compose:
#    - RF docs MCP server
################################################################################

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
MCP_DIR="${PROJECT_ROOT}/RF-docs-MCP-server"

echo "╔════════════════════════════════════════════════════════════════════════╗"
echo "║   RF docs MCP Server - Fast Start                                     ║"
echo "╚════════════════════════════════════════════════════════════════════════╝"
echo ""

# Detect if running interactively
if [ -t 0 ]; then
    echo "Select your AI assistant:"
    echo ""
    echo "  1) GitHub Copilot"
    echo "  2) Claude Code"
    echo "  3) GitLab Duo"
    echo "  4) Amazon Q"
    echo ""
    read -p "Enter your choice (1-4): " choice
    
    case "$choice" in
        1) tool="copilot" ;;
        2) tool="claude-code" ;;
        3) tool="gitlab" ;;
        4) tool="amazonq" ;;
        *)
            echo "Invalid choice."
            exit 1
            ;;
    esac
else
    echo "Usage: ./fast-start.sh"
    echo ""
    echo "Run interactively to select your IDE."
    exit 0
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Step 1: Generate MCP Configuration
echo "📋 Step 1: Generating MCP configuration for $tool..."
cd "$MCP_DIR"
if bash create-mcp-config.sh "$tool"; then
    echo "✅ MCP configuration generated"
else
    echo "❌ Failed to generate MCP configuration"
    exit 1
fi

echo ""

# Step 2: Start services
echo "📚 Step 2: Starting services..."
cd "$PROJECT_ROOT"
if docker compose up -d; then
    echo "✅ Services started"
else
    echo "❌ Failed to start services"
    exit 1
fi

echo ""
echo "📚 Step 3: Generating RF library documentation..."
echo "   This creates documentation for Browser, Requests, and Robocop libraries"
sleep 3  # Give container time to fully start

if docker exec rf-docs-mcp /app/generate_library_docs.sh; then
    echo "✅ Library documentation generated successfully"
else
    echo "⚠️  Library documentation generation had issues (non-critical)"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ Everything is running!"
echo ""
echo "📍 Services:"
echo "   • MCP Server: rf-docs-mcp container"
echo ""
echo "📚 Library Documentation:"
echo "   Generated in container at: /app/docs/"
echo "   • Browser.html, Browser.json, Browser.xml"
echo "   • RequestsLibrary.html, RequestsLibrary.json, RequestsLibrary.xml"
echo "   • Robocop_help.txt, Robocop_rules.txt"
echo ""
echo "   View docs: docker exec rf-docs-mcp ls -lh /app/docs"
echo "   Regenerate: docker exec rf-docs-mcp /app/generate_library_docs.sh"
echo ""
echo "🛑 To stop services and remove containers, networks, and volumes:"
echo "   docker-compose down                              # Stop container"
echo ""
