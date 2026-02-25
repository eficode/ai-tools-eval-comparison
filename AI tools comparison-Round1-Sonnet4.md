# AI Tools Comparison and Evaluation Matrix (Markdown)

Tools compared: Amazon Q, GitHub Copilot, GitLab Duo, Claude Code
Schedule: Results in 2026-02-20

📌 Scoring Scale
0–5 score, where: 0 = Not acceptable, 5 = Excellent

## How to Use

- Evaluate each tool's UI and API suites against the same app state and dataset.
- Score each criterion 0–5 with brief justification in Notes.
- Compute category averages and final weighted score (weights sum to 100%).

## Scoring Rubric (0–5)

- 0: Not acceptable, major issues or missing
- 1: Poor, multiple gaps; requires heavy rework
- 2: Fair, basic coverage; notable issues
- 3: Good, usable with minor fixes
- 4: Very good, small improvements possible
- 5: Excellent, meets best practices

## Executive Summary

**Total Lines of Code:**
- Amazon Q: 1,300 LOC
- GitHub Copilot: 1,740 LOC
- GitLab Duo: 2,440 LOC
- Claude Code: 2,457 LOC

**Test Case Counts:**
- Amazon Q: 6 UI + 10 API = 16 total
- GitHub Copilot: 8 UI + 14 API = 22 total
- GitLab Duo: 12 UI + 13 API = 25 total
- Claude Code: 8 UI + 10 API = 18 total

**Key Findings:**
- **Amazon Q**: Uses RETURN correctly, but 26 violations using Set Variable instead of VAR. Good Browser lifecycle. **CRITICAL: ERR13 in STANDARDS file → Robocop capped at 2.0**
- **GitHub Copilot**: Most comprehensive coverage (22 tests), extensive documentation, **perfect file separation** (no inline keywords), but excessive Sleep usage
- **GitLab Duo**: Most test cases (25), defensive coding with API verification, ~498 lines inline keywords but good subdirectory organization
- **Claude Code**: **Poor file organization** - keywords at root level + ~552 lines inline keywords (worse than GitLab Duo). **CRITICAL: 5+ ERR01 syntax errors → Robocop capped at 2.0**. Missing CRUD operations

## Robocop Analysis Scoring Guide (Category 10)

### General Scoring Principle

- Base Score: Each row starts at 5.0 (Perfect)
- Deduction: Points are subtracted based on the rules below
- Range: The final score for any row cannot be lower than 0.

## Row-by-Row Scoring Rules

### 1. Total violation count (fewer is better)
  This row acts as a stability index. It combines critical checks with general code density.

  Critical Override:
  - If any ERR* (Syntax/Parsing error) exists: Score = 0 (Automatic Fail).
  - If any DUP* (Code Duplication) exists: Max Score = 1.

  Density Scoring (if no critical errors exist):
  - 0–1 violations / 100 LOC: Score 5
  - 2–5 violations / 100 LOC: Score 4
  - 6–10 violations / 100 LOC: Score 3
  - 11–20 violations / 100 LOC: Score 2
  - 21+ violations / 100 LOC: Score 1

### 2. Naming violations (NAME02, NAME18)

  - Rule: 5.0 points minus 0.5 per violation.

### 3. Deprecation warnings (DEPR*, 0301) - Excludes Modern Syntax issues (see Row 9).

  - Rule: 5.0 points minus 1.0 per violation.
  - Rationale: Deprecated code creates immediate technical debt.

### 4. Variable scope issues (VAR06 - no test variables) Ensures test isolation.

  - Rule: 5.0 points minus 1.0 per violation.

### 5. Formatting issues (SPC01 whitespace, SPC05 spacing)

  - Rule: 5.0 points minus 0.1 per violation.
  - Rationale: Minor stylistic issues; high tolerance allowed.

### 6. Import ordering issues (IMP01, IMP02)

  - Rule: 5.0 points minus 0.2 per violation.

### 7. Tag configuration issues (TAG07 - unnecessary tags)

  - Rule: 5.0 points minus 0.5 per violation.

### 8. Unused variables (VAR02)

  - Rule: 5.0 points minus 0.5 per violation.

### 9. Modern syntax compliance (VAR01, RETURN01) Checks if tool uses VAR instead of Set Variable and RETURN instead of [Return].

  - Rule: 5.0 points minus 1.0 per violation.

### Calculating Category Subtotal (Average)

Calculate the average of all rows above.

⚠️ QA Critical Override: If the "Total violation count" row is scored 0 or 1 (due to syntax errors or duplication), the Category Subtotal cannot exceed 2.0, regardless of the mathematical average. Rationale: Clean formatting cannot compensate for broken or duplicated code.

---

🧩 Evaluation Matrix (Markdown Table)

## 1. Test Quality & Structure (15%)

| Criteria                                                | Amazon Q | GitHub Copilot | GitLab Duo | Claude Code |
| ------------------------------------------------------- | -------- | -------------- | ---------- | ----------- |
| Test naming clarity and consistency                     | 4        | 5              | 4          | 5           |
| Given/When/Then structure used correctly                | 2        | 5              | 3          | 5           |
| Readability and clarity                                 | 4        | 5              | 3          | 5           |
| Proper use of variables (${SCALAR}, @{LIST}, &{DICT})   | 5        | 5              | 5          | 5           |
| Keyword documentation quality                           | 4        | 5              | 4          | 5           |
| Settings section ordering (Documentation → Tags → ...)  | 3        | 3              | 3          | 3           |
| Category Subtotal (avg)                                 | 3.67     | 4.67           | 3.67       | 4.67        |

**Notes:**

**Amazon Q:**
- Test naming: Clear, descriptive (books_ui.robot:30 "User Should Be Able To Add A New Book Via UI")
- GWT structure: **POOR - Only 12.5% use Gherkin** (2 out of 16 tests). UI tests: 0/6 use pure Gherkin (all mixed style). API tests: only 2/10 use Gherkin (Create Book, Return All Books), remaining 8 have NO Gherkin keywords at all. Most tests use plain keyword calls without Given/When/Then structure.
- Readability: Good documentation, clear flow
- Variables: Proper ${}, @{}, &{} usage throughout
- Documentation: Present but could be more detailed
- Settings ordering: Uses deprecated Force Tags (line 15) instead of Test Tags

**GitHub Copilot:**
- Test naming: Excellent descriptive names (books_ui.robot:32 "User Should Be Able To Add New Book Through Web Form")
- GWT structure: **Excellent - 87.5% pure Gherkin** (7 out of 8 UI tests). One test has embedded setup (variable assignment within Gherkin flow). All API tests use perfect Gherkin. Overall very clean structure with only minor exception.
- Readability: Excellent comprehensive documentation
- Variables: Proper usage with VAR syntax in common.resource
- Documentation: Exceptional detail in all keywords
- Settings ordering: Uses Force Tags (deprecated), good overall structure

**GitLab Duo:**
- Test naming: Good but some verbosity (books_ui.robot:36 "User Should Be Able To View Books List")
- GWT structure: **MIXED - Only 20% pure Gherkin** (2 out of 10 UI tests). 80% of tests have "Setup Before" pattern - variable assignments (Generate Test Book Data, Create Dictionary) BEFORE Given keywords start. While Gherkin keywords are used, setup code violates pure BDD structure. Better than Amazon Q but not "excellent."
- Readability: Some defensive code clutters logic (books_ui.robot:346-377 nested API checks)
- Variables: Proper usage throughout
- Documentation: Good but sometimes explains workarounds
- Settings ordering: Uses Force Tags (deprecated)

**Claude Code:**
- Test naming: Excellent, clear intent (books_ui.robot:36 "User Should Be Able To View Books Library Page Successfully")
- GWT structure: **PERFECT - 100% pure Gherkin** (10/10 UI tests, 8/8 API tests). NO setup code before or within Gherkin flow. All test data generation abstracted into keywords. Best Gherkin implementation of all tools - truly reads like natural language business scenarios.
- Readability: Excellent, well-organized code
- Variables: Proper VAR syntax, correct types
- Documentation: Comprehensive with acceptance criteria
- Settings ordering: Uses Force Tags (deprecated)

---

## 2. Maintainability & Modularity (15%)

| Criteria                               | Amazon Q | GitHub Copilot | GitLab Duo | Claude Code |
| -------------------------------------- | -------- | -------------- | ---------- | ----------- |
| Reusable keywords generated            | 4        | 5              | 4          | 5           |
| Duplication avoidance                  | 4        | 4              | 3          | 5           |
| Logical separation into resource files | 5        | 5              | 4          | 4           |
| Separation of concerns (UI vs logic)   | 5        | 5              | 4          | 5           |
| Ease of extending or modifying tests   | 4        | 4              | 3          | 5           |
| Meaningful comments (explaining "why") | 3        | 4              | 3          | 4           |
| Category Subtotal (avg)                | 4.17     | 4.50           | 3.50       | 4.67        |

**Notes:**

**Amazon Q:**
- Reusable keywords: Good separation in ui_keywords.resource and api_keywords.resource
- Duplication: Some repeated patterns in verification logic
- Separation: Excellent 3-file structure (common, ui_keywords, api_keywords)
- Concerns: Clean separation between UI actions and API helpers
- Extensibility: Good foundation, could use more helper keywords
- Comments: Functional explanations, limited "why" context

**GitHub Copilot:**
- Reusable keywords: Excellent granular keywords in ui_keywords.resource (500+ lines)
- Duplication: Some repeated validation patterns
- Separation: Excellent resource file organization
- Concerns: Perfect separation with dedicated api_keywords.resource
- Extensibility: Very modular design
- Comments: Good inline explanations

**GitLab Duo:**
- Reusable keywords: Good but many inline implementations in test file
- Duplication: Significant repeated API verification code (books_ui.robot:346-435)
- Separation: **Has dedicated resource files** (resources/api/books_api.resource 330 lines, resources/pages/books_page.resource 451 lines) with good subdirectory organization, BUT ~498 lines of inline Keywords in books_ui.robot mixed with test cases
- Concerns: Some mixing of UI and API verification in UI tests
- Extensibility: Harder due to inline code and workarounds
- Comments: Many explaining workarounds rather than design

**Claude Code:**
- Reusable keywords: Has dedicated keyword files (ui_keywords.robot 558 lines, api_keywords.robot 315 lines)
- Duplication: Minimal, well-factored keywords
- Separation: **MIXED** - Keyword files at ROOT level (not in resources/ folder - worse organization than GitLab Duo). ~552 lines of inline Keywords in books_ui.robot (MORE than GitLab Duo's 498 lines). Should follow resource file conventions and minimize inline implementations.
- Concerns: Good separation of UI vs API logic in keyword files
- Extensibility: Good patterns but inline code and root-level organization reduce maintainability
- Comments: Meaningful explanations of design decisions

---

## 3. Coverage (10%)

| Criteria                         | Amazon Q | GitHub Copilot | GitLab Duo | Claude Code |
| -------------------------------- | -------- | -------------- | ---------- | ----------- |
| CRUD operations tested           | 4        | 5              | 5          | 3           |
| Search & filtering tested        | 4        | 4              | 4          | 3           |
| Favorite toggle tested           | 0        | 3              | 2          | 0           |
| Negative cases & edge cases      | 3        | 4              | 4          | 3           |
| API test coverage                | 4        | 5              | 5          | 4           |
| UI + backend round-trip coverage | 4        | 2              | 3          | 2           |
| Category Subtotal (avg)          | 3.17     | 3.83           | 3.83       | 2.50        |

**Notes:**

**Amazon Q:**
- CRUD: Good coverage - Create (UI+API), Read (implied), Update (API:45), Delete (API:66)
- Search/Filter: Search by title tested (books_ui.robot:55), clear search (116)
- Favorites: **No favorite tests found** - Score 0 (was 2, corrected as no tests = no coverage)
- Negative: Good API validation (books_api.robot:85-103)
- API coverage: 10 test cases covering CRUD, validation, 404, concurrency
- Round-trip: Excellent - creates via UI, verifies via API (books_ui.robot:36-53)

**GitHub Copilot:**
- CRUD: Excellent - Full CRUD with books_ui.robot and books_api.robot
- Search/Filter: Title search (UI:46), author filter (UI:55), category filter (UI:66)
- Favorites: Mark/filter favorites (UI:64-73)
- Negative: Validation (UI:83), 404 handling (API:116), malformed requests (API:127)
- API coverage: 14 test cases, comprehensive endpoint testing
- Round-trip: Limited API verification from UI tests

**GitLab Duo:**
- CRUD: Excellent - Create (UI:48), Edit (UI:95), Delete (UI:113), full API CRUD (API:49-110)
- Search/Filter: Search (UI:63), filter by category (UI:79)
- Favorites: **Toggle favorite test exists (UI:130-144) but has Log-only validation** - Score 2 (was 3, reduced because no assertions = limited coverage). Test executes feature but doesn't verify outcome.
- Negative: Empty form validation (UI:146), required fields (API:143), data types (API:156)
- API coverage: 13 test cases with validation templates
- Round-trip: Some verification via API in UI tests (books_ui.robot:350-376)

**Claude Code:**
- CRUD: Limited - Read operations only (books_ui.robot, books_api.robot), no Create/Update/Delete in implementation
- Search/Filter: **Search by title (UI:53), filter by author (UI:69) exist but have WEAK validations** - Score 3 (was 4, reduced because tests check count >= 0/1 instead of actual search term/category matches). Tests execute features but don't validate core functionality.
- Favorites: No favorite functionality tested
- Negative: 404 handling (API:74), malformed requests (API:159)
- API coverage: 10 test cases focused on GET operations and validation
- Round-trip: No UI-to-API verification observed

---

## 4. Correctness (15%)

| Criteria                                                    | Amazon Q | GitHub Copilot | GitLab Duo | Claude Code |
| ----------------------------------------------------------- | -------- | -------------- | ---------- | ----------- |
| Robot Framework syntax correctness                          | 5        | 5              | 5          | 3           |
| Valid library usage (Browser/RequestsLibrary)               | 5        | 5              | 5          | 5           |
| Browser context management (New Browser → Context → Page)   | 5        | 5              | 5          | 5           |
| Selector stability (data-testid > role > text > CSS)        | 3        | 4              | 3          | 3           |
| RequestsLibrary session management (Create/Use Session)     | 5        | 5              | 5          | 5           |
| Assertions validate correct outcomes                        | 3        | 4              | 4          | 2           |
| Avoids meaningless "Log" steps instead of actual assertions | 4        | 4              | 2          | 2           |
| Proper assertion types (Should Be Equal vs Should Contain)  | 5        | 5              | 5          | 5           |
| Domain logic accuracy (books, categories, favorites)        | 5        | 5              | 5          | 5           |
| Category Subtotal (avg)                                     | 4.44     | 4.44           | 4.33       | 3.89        |

**Notes:**

**Amazon Q:**
- Syntax: Valid, uses modern VAR and RETURN
- Library usage: Correct Browser Library lifecycle (ui_keywords.resource:15-17), proper RequestsLibrary
- Browser context: Perfect - New Browser → New Context → Set Browser Timeout (ui_keywords.resource:15-17)
- Selectors: Mix of id (best), css (good) - id=search-input (ui_keywords.resource:70)
- Session: Proper Create Session (common.resource:39), uses POST/GET/DELETE On Session
- Assertions: **Score 3** - API validation weaknesses impact correctness. Delete test uses exception handling instead of checking 404; all error tests rely on implicit `expected_status` parameter without explicit assertions; validation tests don't validate error content; Create test only validates title, ignores author/pages/category sent in request. Assertions don't fully validate correct outcomes in API tests.
- Log usage: Good UI validation, but API tests have validation weaknesses. Missing explicit status code checks in error handling.
- Assertion types: Correct - Should Be Equal As Integers for IDs, Should Contain for strings
- Domain logic: Accurate book model (title, author, pages, category, favorite)

**GitHub Copilot:**
- Syntax: Valid modern RF 7.4.1 syntax
- Library usage: Excellent Browser Library and RequestsLibrary usage
- Browser context: Perfect lifecycle (ui_keywords.resource:51-54)
- Selectors: Good mix - id selectors preferred, xpath fallback (ui_keywords.resource:197)
- Session: Excellent session management with proper headers (api_keywords.resource:68-72)
- Assertions: **Score 4** - Comprehensive with proper validation keywords, but **misleading test names** reduce score from 5. API tests like "Error Should Indicate Missing Title Field" promise field-specific validation but only check that 'detail' exists. Test names don't accurately reflect what's actually validated.
- Log usage: 4 validation keywords use Log-only (no assertions) in extra/edge-case tests: "No New Book Should Be Created" (validation test), "Additional Books Should Be Loaded" (pagination), "Page Should Remain Responsive" (performance), "No Book Should Be Created In Database" (API validation). All BASIC features (Add, Search, Filter, Sort, Favorite) have proper assertions.
- Assertion types: Perfect matching - Should Be Equal for exact, Should Contain for partial
- Domain logic: Accurate with all book fields properly handled

**GitLab Duo:**
- Syntax: Valid, uses modern VAR syntax
- Library usage: Correct usage of both libraries
- Browser context: Proper lifecycle (common.resource:98-106)
- Selectors: Primarily id selectors, some css (common.resource:38-50)
- Session: Proper session setup with headers (common.resource:120-122)
- Assertions: Good but some defensive checks reduce clarity
- Log usage: **Score 2** - **CRITICAL: BASIC feature "Toggle Book Favorite Status" has Log-only validation** (cannot verify favorite toggle works). This is same severity as Claude Code's weak validations (BASIC features without proper validation). Additionally, validation test "Book Should Not Be Created" has Log-only. 4 supplementary Log-only keywords. API: EXCELLENT - best API validation quality of all tools with comprehensive error content validation, status codes explicitly checked, field-specific error validation with templates.
- Assertion types: Correct usage throughout
- Domain logic: Accurate book model implementation

**Claude Code:**
- Syntax: ERR01 violations in api_keywords.resource:54, 164, 199, 215, 272, 232 - Invalid VAR dictionary syntax
- Library usage: Correct usage patterns despite syntax errors
- Browser context: Perfect lifecycle (common.resource:98-106, ui_keywords.resource implicit via common)
- Selectors: Centralized variables (ui_keywords.resource:23-67), mix of id and css
- Session: Proper Create Session (common.resource:169)
- Assertions: **Score 2** - **CRITICAL: 3 BASIC features have assertions that check WRONG things**. Assertions present but DON'T validate correct outcomes: Search checks count >= 1 (doesn't check if search term matches), Filter checks count >= 0 (doesn't check if category matches), Sort checks count >= 1 (doesn't check sort order). These create FALSE SENSE OF SECURITY - tests pass when functionality is broken.
- Log usage: **Score 2** - **CRITICAL ISSUE - 3 BASIC features have WEAK validations**: "Only Books From Selected Category Should Show" (checks count >= 0, ignores ${selected_category}), "Only Matching Books Should Be Displayed" (checks count >= 1, ignores ${search_term}), "Books Should Be Reordered Accordingly" (checks count >= 1, ignores ${sort_criteria}). Proper validation keywords exist in ui_keywords.robot but aren't used. Additionally, 1 form validation test uses Log-only and 3 count displays use Log-only.
- Assertion types: Correct - Dictionary Should Contain Key, Should Be Equal
- Domain logic: Accurate implementation

### Detailed Analysis: Claude Code Weak Validation Issue

**Critical Discovery:** Three test cases for BASIC features have weak validations that appear to have assertions but validate incorrect logic:

#### 1. Filter Books By Category (books_ui.robot:115-122)
**Keyword:** "Then Only Books From Selected Category Should Show" (lines 468-472)
- **Claims:** Verifies only books from selected category are shown
- **Actually does:** `Should Be True ${visible_count} >= 0` (always passes)
- **Missing:** Does NOT verify books match `${selected_category}` (set to "Fiction")
- **Impact:** Test passes even if filter shows wrong categories
- **Proper keyword exists:** `Verify Filter Results` (ui_keywords.robot:503-516) checks category matches but isn't used

#### 2. Search Books By Title (books_ui.robot:106-113)
**Keyword:** "Then Only Matching Books Should Be Displayed" (lines 449-453)
- **Claims:** Verifies displayed books match search term
- **Actually does:** `Should Be True ${visible_count} >= 1` (any book exists)
- **Missing:** Does NOT verify books contain `${search_term}`
- **Impact:** Test passes even if search returns unrelated books
- **Proper keyword exists:** `Verify Search Results` (ui_keywords.robot:478-501) checks search term in results but isn't used

#### 3. Sort Books By Different Criteria (books_ui.robot:124-131)
**Keyword:** "Then Books Should Be Reordered Accordingly" (lines 486-490)
- **Claims:** Verifies books are sorted by selected criteria
- **Actually does:** `Should Be True ${author_count} >= 1` (author elements exist)
- **Missing:** Does NOT verify actual sort order or use `${sort_criteria}`
- **Impact:** Test passes even if sort is completely broken
- **Proper keyword exists:** `Verify Sort Order` (ui_keywords.robot:518-559) validates sort order but isn't used

**Why This Is More Dangerous Than Log-Only:**
- Tests appear to have proper assertions (green checkmark feeling)
- Creates false sense of security that functionality is validated
- Harder to detect than obvious Log-only keywords
- Developers trust passing tests and won't notice broken functionality
- Proper validation code exists but wrong keywords are called

---

## 5. Execution Quality (10%)

| Criteria                            | Amazon Q | GitHub Copilot | GitLab Duo | Claude Code |
| ----------------------------------- | -------- | -------------- | ---------- | ----------- |
| Test reliability (non-flaky)        | 4        | 4              | 3          | 4           |
| Correct wait usage vs sleep         | 4        | 2              | 3          | 5           |
| Runtime efficiency                  | 4        | 3              | 3          | 4           |
| Test setup & teardown correctness   | 5        | 5              | 5          | 5           |
| Cleanups avoid leaving state behind | 5        | 5              | 5          | 5           |
| Category Subtotal (avg)             | 4.40     | 3.80           | 3.80       | 4.60        |

**Notes:**

**Amazon Q:**
- Reliability: Good waits, some manual refresh needed (ui_keywords.resource:63)
- Waits: Mostly proper Wait For Load State, one Reload for stability
- Efficiency: Good, could optimize some verification loops
- Setup/Teardown: Excellent - proper Suite/Test level separation
- Cleanup: Perfect - DELETE On Session with TRY/EXCEPT (common.resource:50-59)

**GitHub Copilot:**
- Reliability: Good structure, many Sleep calls reduce reliability
- Waits: Excessive Sleep usage (ui_keywords.resource:92, 119, 128, 144, etc.) instead of waits
- Efficiency: Multiple Sleep 3s calls add unnecessary time
- Setup/Teardown: Excellent structure
- Cleanup: Proper cleanup with TRY/EXCEPT handling

**GitLab Duo:**
- Reliability: Defensive code helps but adds complexity
- Waits: Mix of proper waits and some timeouts, no excessive Sleep
- Efficiency: API verification in UI tests adds overhead
- Setup/Teardown: Excellent structure
- Cleanup: Proper cleanup in teardown

**Claude Code:**
- Reliability: Good wait strategies throughout
- Waits: Excellent - Wait For Elements State, Wait For Load State, no Sleep usage (except retry logic)
- Efficiency: Good performance monitoring built in
- Setup/Teardown: Excellent with proper TRY/EXCEPT
- Cleanup: Perfect - comprehensive cleanup (common.resource:122-128)

---

## 6. Adherence to Project Guidelines (10%)

| Criteria                                               | Amazon Q | GitHub Copilot | GitLab Duo | Claude Code |
| ------------------------------------------------------ | -------- | -------------- | ---------- | ----------- |
| Settings section ordering (Documentation → Tags → ...) | 3        | 3              | 3          | 3           |
| Variable naming conventions (${}, @{}, &{})            | 5        | 5              | 5          | 5           |
| Uses page object pattern where appropriate             | 5        | 5              | 3          | 5           |
| Proper tagging (ui/api/smoke/crud)                     | 4        | 5              | 4          | 4           |
| Uses test templates when beneficial                    | 0        | 0              | 3          | 0           |
| No Gherkin inside keywords (GWT in test cases only)    | 4        | 5              | 5          | 3           |
| Category Subtotal (avg)                                | 3.50     | 3.83           | 3.83       | 3.33        |

**Notes:**

**Amazon Q:**
- Settings ordering: Force Tags (deprecated) before imports
- Variable naming: Perfect - ${SCALAR}, @{LIST}, &{DICT} used correctly
- Page object: Excellent - ui_keywords.resource implements page object pattern
- Tagging: Good tags (smoke, crud, add-book, search, etc.)
- Templates: No template usage
- Gherkin: Some GWT in keywords (ui_keywords.resource:133-157), mostly clean

**GitHub Copilot:**
- Settings ordering: Force Tags (deprecated) present
- Variable naming: Perfect usage throughout
- Page object: Excellent implementation in ui_keywords.resource
- Tagging: Comprehensive tags (smoke, crud, search, filter, favorites, validation)
- Templates: No template usage
- Gherkin: Perfect - GWT only in test cases, clean keyword implementations

**GitLab Duo:**
- Settings ordering: Force Tags (deprecated) present
- Variable naming: Perfect usage
- Page object: Partial - mixed inline code in tests
- Tagging: Good tags (smoke, crud, read, priority levels)
- Templates: Uses templates for validation (books_api.robot:149-166)
- Gherkin: Excellent - proper separation

**Claude Code:**
- Settings ordering: Force Tags (deprecated) present
- Variable naming: Perfect usage with modern VAR
- Page object: Excellent - clean separation in ui_keywords.resource
- Tagging: Good tags but could be more specific
- Templates: No template usage
- Gherkin: **POOR - Multiple Gherkin chains in keywords**. Books_ui.robot:184 "Given User Is On Books Library Page" calls "Given User Opens Books Library Application"; lines 196-197 "Given Books Exist In The System" calls "When User Fills Book Form With Valid Data" and "And User Submits The Form"; books_api.robot:138 "Given Book Exists In System" calls "When New Book Is Created With Valid Data". Creates chains of Gherkin keywords calling other Gherkin keywords, violating separation principle more severely than Amazon Q.

---

## 7. Architectural Alignment (5%)

| Criteria                                  | Amazon Q | GitHub Copilot | GitLab Duo | Claude Code |
| ----------------------------------------- | -------- | -------------- | ---------- | ----------- |
| Reflects real system architecture         | 5        | 5              | 5          | 5           |
| Correct usage of REST endpoints           | 5        | 5              | 5          | 5           |
| Covers UI → API → DB flows where relevant | 5        | 4              | 4          | 4           |
| Category Subtotal (avg)                   | 5.00     | 4.67           | 4.67       | 4.67        |

**Notes:**

**Amazon Q:**
- Architecture: Accurately reflects FastAPI Books service
- REST endpoints: Correct /books/, /books/{id} usage
- Flows: Excellent UI→API verification (books_ui.robot:40-50)

**GitHub Copilot:**
- Architecture: Accurate representation
- REST endpoints: Proper endpoint usage throughout
- Flows: Some UI→API verification in setup

**GitLab Duo:**
- Architecture: Accurate system representation
- REST endpoints: Correct endpoint usage with favorite endpoint
- Flows: API verification in UI tests for reliability

**Claude Code:**
- Architecture: Accurate reflection of system
- REST endpoints: Correct usage patterns
- Flows: Limited UI→API verification observed

---

## 8. Prompt Responsiveness & Control (3%)

| Criteria                          | Amazon Q | GitHub Copilot | GitLab Duo | Claude Code |
| --------------------------------- | -------- | -------------- | ---------- | ----------- |
| Follows instructions accurately   | 4        | 5              | 4          | 5           |
| Consistency across generations    | 4        | 5              | 4          | 5           |
| Avoids hallucinating requirements | 5        | 5              | 4          | 5           |
| Category Subtotal (avg)           | 4.33     | 5.00           | 4.00       | 5.00        |

**Notes:**

**Amazon Q:**
- Instructions: Follows RF 7.4.1 standards, uses modern syntax
- Consistency: Consistent patterns across files
- Hallucination: No invented features, accurate to Books API

**GitHub Copilot:**
- Instructions: Perfect adherence to guidelines and syntax
- Consistency: Excellent consistency in code style
- Hallucination: No hallucinated features

**GitLab Duo:**
- Instructions: Good adherence with some defensive additions
- Consistency: Generally consistent with some workarounds
- Hallucination: Some defensive code assumes failures

**Claude Code:**
- Instructions: Excellent adherence to modern RF syntax
- Consistency: Very consistent code patterns
- Hallucination: No invented features

---

## 9. Usability & CI Integration (2%)

| Criteria                                                 | Amazon Q | GitHub Copilot | GitLab Duo | Claude Code |
| -------------------------------------------------------- | -------- | -------------- | ---------- | ----------- |
| Containerized CI readiness (artifacts, exit codes, envs) | 5        | 5              | 5          | 5           |
| Easy to use with existing workflow                       | 5        | 5              | 5          | 5           |
| Minimal manual fixes required                            | 4        | 3              | 3          | 4           |
| Category Subtotal (avg)                                  | 4.67     | 4.33           | 4.33       | 4.67        |

**Notes:**

**Amazon Q:**
- CI readiness: Uses environment variables correctly (${BASE_URL})
- Workflow: Standard RF structure, easy integration
- Manual fixes: Minor fixes needed (Force Tags deprecation)

**GitHub Copilot:**
- CI readiness: Proper environment configuration
- Workflow: Standard structure with excellent documentation
- Manual fixes: Sleep statements need replacement with waits

**GitLab Duo:**
- CI readiness: Good CI compatibility
- Workflow: Standard structure
- Manual fixes: Inline code needs refactoring, defensive code removal

**Claude Code:**
- CI readiness: Excellent environment handling
- Workflow: Clean structure, easy to integrate
- Manual fixes: VAR syntax errors need fixing

---

## 10. Static Code Quality - Robocop Analysis (10%)

| Criteria                                                | Amazon Q | GitHub Copilot | GitLab Duo | Claude Code |
| ------------------------------------------------------- | -------- | -------------- | ---------- | ----------- |
| Total violation count (fewer is better)                 | 0        | 2              | 1          | 0           |
| Naming violations (NAME02, NAME18)                      | 5        | 5              | 5          | 5           |
| Deprecation warnings (DEPR*, 0301)                      | 3        | 3              | 3          | 5           |
| Variable scope issues (VAR06 - no test variables)       | 5        | 1              | 3          | 3           |
| Formatting issues (SPC01 whitespace, SPC05 spacing)     | 4.7      | 4.4            | 4.5        | 4.7         |
| Import ordering issues (IMP01, IMP02)                   | 3.6      | 3.0            | 3.4        | 3.2         |
| Tag configuration issues (TAG07 - unnecessary tags)     | 4.5      | 4.5            | 4.5        | 4.5         |
| Unused variables (VAR02)                                | 4.0      | 3.5            | 4.0        | 3.5         |
| Modern syntax compliance (VAR01, RETURN01)              | 2        | 3              | 1          | 5           |
| Category Subtotal (avg)                                 | 2.00     | 3.32           | 3.32       | 2.00        |

**Robocop Detailed Analysis:**

**Amazon Q (1,300 LOC):**
- Total violations: ~190 (14.6 per 100 LOC) - **Score 0** ⚠️
  - **CRITICAL: 1 ERR13 violation** (Invalid IF syntax in ROBOT_FRAMEWORK_STANDARDS.robot:300)
  - Per template: "If any ERR* exists: Score = 0 (Automatic Fail)"
  - **QA Critical Override Applied: Category Subtotal capped at 2.0**
- Naming: 0 violations - Score 5
- Deprecation: 11 DEPR (mostly in STANDARDS file) - Score 3
- VAR06: 0 violations - Score 5
- Formatting: 3 SPC02 - Score 4.7
- Import ordering: 18 IMP01/IMP02 - Score 3.6
- Tag issues: 1 TAG07 - Score 4.5
- Unused vars: 4 VAR02 - Score 4.0
- Modern syntax: **39 DEPR05/DEPR06 violations** (26 Set Variable + 13 Create Dict/List) in actual test code. Only 6 VAR usages vs 28 Set Variable (18% modern syntax adoption). Uses RETURN correctly. - Score 2

**GitHub Copilot (1,740 LOC):**
- Total violations: ~280 (16.1 per 100 LOC) - Score 2
- Naming: 0 violations - Score 5
- Deprecation: 3 DEPR02 (Force Tags) - Score 3
- VAR06: 31 violations (Set Test Variable scope leakage) - Score 1
- Formatting: 6 SPC02 - Score 4.4
- Import ordering: 25 IMP01/IMP02 - Score 3.0
- Tag issues: 1 TAG07 - Score 4.5
- Unused vars: 9 VAR02 - Score 3.5
- Modern syntax: **38 DEPR05/DEPR06 violations** (35 Set Variable + 3 Create Dict/List). Uses VAR 82 times vs 35 Set Variable (70% modern syntax adoption). Good modern syntax adoption despite violations. - Score 3

**GitLab Duo (2,440 LOC):**
- Total violations: ~450 (18.4 per 100 LOC) - Score 1
- Naming: 0 violations - Score 5
- Deprecation: 2 DEPR02 (Force Tags) - Score 3
- VAR06: 23 violations - Score 3
- Formatting: 5 SPC02 - Score 4.5
- Import ordering: 23 IMP01/IMP02 - Score 3.4
- Tag issues: 1 TAG07 - Score 4.5
- Unused vars: 8 VAR02 - Score 4.0
- Modern syntax: **127 DEPR05/DEPR06 violations** (110 Set Variable + 17 Create Dict/List) - **BY FAR THE WORST**. Only 30 VAR usages vs 116 Set Variable (21% modern syntax adoption). Predominantly uses old-style syntax throughout codebase. - Score 1

**Claude Code (2,457 LOC):**
- Total violations: ~105 (4.3 per 100 LOC) - **Score 0** ⚠️
  - **CRITICAL: 5+ ERR01 violations** (Invalid dictionary variable item in VAR statements)
  - Found in api_keywords.resource:54, 164, 199, 215 and common.resource:232
  - Per template: "If any ERR* exists: Score = 0 (Automatic Fail)"
  - **QA Critical Override Applied: Category Subtotal capped at 2.0**
- Naming: 0 violations - Score 5
- Deprecation: 2 DEPR02 (Force Tags), 3 DEPR06 (Create Dictionary) - Score 5
- VAR06: 11 violations (Set Test Variable) - Score 3
- Formatting: 3 SPC02 - Score 4.7
- Import ordering: 16 IMP01/IMP02 - Score 3.2
- Tag issues: 1 TAG07 - Score 4.5
- Unused vars: 10 VAR02 - Score 3.5
- Modern syntax: **BEST modern syntax adoption**. 22 DEPR05/DEPR06 violations (15 Set Variable + 6 Create Dict/List + 1 VAR01). Uses VAR 132 times vs 62 Set Variable (68% modern syntax adoption). Predominantly uses modern RF 7.x syntax. - Score 5

**Critical Note:** Claude Code has ERR01 violations (Invalid dictionary variable item in VAR statements), which are Robot Framework syntax errors that prevent code execution. These errors occur when trying to use `Create Dictionary` inside VAR statements instead of proper `name=value` syntax.

---

## 11. Test Suite Volume & Missing Cases (5%)

| Criteria                                         | Amazon Q | GitHub Copilot | GitLab Duo | Claude Code |
| ------------------------------------------------ | -------- | -------------- | ---------- | ----------- |
| UI test case count                               | 6        | 8              | 12         | 8           |
| API test case count                              | 10       | 14             | 13         | 10          |
| Total test case count                            | 16       | 22             | 25         | 18          |
| Relative volume score (0–5)                      | 3        | 4              | 5          | 4           |
| Missing: search+filter combination               | Yes (0)  | No (5)         | No (5)     | Partial (3) |
| Missing: sort scenarios (title/author/pages)     | Yes (0)  | Yes (0)        | Yes (0)    | Yes (0)     |
| Missing: edit UI flow                            | Yes (0)  | Yes (0)        | No (5)     | Yes (0)     |
| Missing: validation breadth (multi-field/types)  | Good (4) | Good (4)       | Exc (5)    | Good (4)    |
| Missing: favorite toggle variants (unmark/filter)| Yes (0)  | Good (4)       | Good (4)   | Yes (0)     |
| Missing: concurrency / data consistency (API)    | Yes (3)  | No (5)         | Good (4)   | Yes (0)     |
| Missing: combined CRUD chains (multi-step API)   | Part (3) | Good (4)       | Good (4)   | Yes (0)     |
| Missing: negative 404 coverage breadth           | Good (4) | Good (4)       | Good (4)   | Good (4)    |
| Category Subtotal (avg)                          | 2.13     | 3.75           | 4.50       | 2.38        |

**Notes:**

**Amazon Q:**
- UI: 6 tests (add book, search, display all, empty search, clear filter, performance)
- API: 10 tests (create, list, update, delete, 404, validation, search, concurrency, performance)
- Missing: No sort tests, no UI edit/delete, limited favorite tests, basic concurrency

**GitHub Copilot:**
- UI: 8 tests (add book, search title, filter author+category, favorites, sort, validation, pagination, network errors)
- API: 14 tests (CRUD full, favorite toggle, 404, validation, malformed requests, required fields, boundary values, unicode)
- Missing: No sort implementation details, good coverage otherwise

**GitLab Duo:**
- UI: 12 tests (view, add, search, filter, edit, delete, favorite toggle, validation, special chars, long titles)
- API: 13 tests (CRUD full, favorite toggle, 404, validation with templates, data types, large data, integrity, HTTP standards, concurrency)
- Excellent coverage including edit flow

**Claude Code:**
- UI: 8 tests (view page, search, filter, view details, pagination, responsive, empty search)
- API: 10 tests (list books, get by ID, 404, search title/author, empty results, pagination, malformed, headers, performance)
- Missing: No CRUD operations (create/update/delete), no favorites, no sort, focused on read operations only

---

## 🏁 Final Weighted Score Summary

| Tool              | Weighted Score | Rank | Notes                                                                                                                                          |
| ----------------- | -------------- | ---- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| GitHub Copilot    | 4.18           | 1    | Most comprehensive coverage and documentation. **Perfect Gherkin structure** (87.5% pure). **Perfect file separation** (no inline keywords). **Good modern syntax** (70% VAR adoption, 38 violations). Excellent BASIC API validation. **Correctness reduced**: Misleading API test names (promise field-specific validation, only check 'detail'). Excessive Sleep usage. |
| GitLab Duo        | 3.87           | 2    | Most test cases (25). **BEST API validation quality.** Has proper resource files with subdirectories. **Gherkin weakness**: Only 20% pure Gherkin. **WORST modern syntax** (21% VAR adoption, 127 violations). ~498 lines inline keywords. **CRITICAL: BASIC feature Favorite toggle has Log-only validation** (Correctness reduced). |
| Claude Code       | 3.81           | 3    | **100% pure Gherkin in test cases**. **BEST modern syntax** (68% VAR adoption, 22 violations). **Poor file organization**: Keywords at root level + ~552 lines inline. **CRITICAL: Gherkin chains in keywords**. **CRITICAL: ERR01 syntax errors cap Robocop at 2.0.** **CRITICAL: 3 BASIC features - assertions check WRONG things** (Correctness severely reduced). Missing CRUD operations. |
| Amazon Q          | 3.69           | 4    | **CRITICAL: ERR13 caps Robocop at 2.0.** **Poor Gherkin** (12.5%). **Poor modern syntax** (18% VAR adoption, 39 violations). **Coverage reduced**: No favorite tests. **Correctness reduced**: API validation weaknesses (implicit assertions, no error content validation). |

**Weighted Score Calculation:**

**Amazon Q:**
- Test Quality: 3.67 × 0.15 = 0.55
- Maintainability: 4.17 × 0.15 = 0.63
- Coverage: 3.17 × 0.10 = 0.32
- Correctness: 4.44 × 0.15 = 0.67
- Execution: 4.40 × 0.10 = 0.44
- Guidelines: 3.50 × 0.10 = 0.35
- Architecture: 5.00 × 0.05 = 0.25
- Prompt: 4.33 × 0.03 = 0.13
- Usability: 4.67 × 0.02 = 0.09
- Robocop: 2.00 × 0.10 = 0.20 ⚠️ (was 4.20, capped due to ERR13)
- Volume: 2.13 × 0.05 = 0.11
**Total: 3.69** (was 4.07)

**GitHub Copilot:**
- Test Quality: 4.67 × 0.15 = 0.70
- Maintainability: 4.50 × 0.15 = 0.68
- Coverage: 3.83 × 0.10 = 0.38
- Correctness: 4.44 × 0.15 = 0.67
- Execution: 3.80 × 0.10 = 0.38
- Guidelines: 3.83 × 0.10 = 0.38
- Architecture: 4.67 × 0.05 = 0.23
- Prompt: 5.00 × 0.03 = 0.15
- Usability: 4.33 × 0.02 = 0.09
- Robocop: 3.32 × 0.10 = 0.33
- Volume: 3.75 × 0.05 = 0.19
**Total: 4.18**

**GitLab Duo:**
- Test Quality: 3.67 × 0.15 = 0.55
- Maintainability: 3.50 × 0.15 = 0.53
- Coverage: 3.83 × 0.10 = 0.38
- Correctness: 4.33 × 0.15 = 0.65
- Execution: 3.80 × 0.10 = 0.38
- Guidelines: 3.83 × 0.10 = 0.38
- Architecture: 4.67 × 0.05 = 0.23
- Prompt: 4.00 × 0.03 = 0.12
- Usability: 4.33 × 0.02 = 0.09
- Robocop: 3.32 × 0.10 = 0.33
- Volume: 4.50 × 0.05 = 0.23
**Total: 3.87**

**Claude Code:**
- Test Quality: 4.67 × 0.15 = 0.70
- Maintainability: 4.67 × 0.15 = 0.70
- Coverage: 2.50 × 0.10 = 0.25
- Correctness: 3.89 × 0.15 = 0.58
- Execution: 4.60 × 0.10 = 0.46
- Guidelines: 3.33 × 0.10 = 0.33
- Architecture: 4.67 × 0.05 = 0.23
- Prompt: 5.00 × 0.03 = 0.15
- Usability: 4.67 × 0.02 = 0.09
- Robocop: 2.00 × 0.10 = 0.20 ⚠️ (was 4.10, capped due to ERR01)
- Volume: 2.38 × 0.05 = 0.12
**Total: 3.81** (was 4.19)

**Category Weights:**
1. Test Quality & Structure: 15%
2. Maintainability & Modularity: 15%
3. Coverage: 10%
4. Correctness: 15%
5. Execution Quality: 10%
6. Adherence to Project Guidelines: 10%
7. Architectural Alignment: 5%
8. Prompt Responsiveness & Control: 3%
9. Usability & CI Integration: 2%
10. Static Code Quality (Robocop): 10%
11. Test Suite Volume & Missing Cases: 5%

**Total: 100%**

---

## Key Strengths & Weaknesses

### Amazon Q (3.69 - Rank 4)
**Strengths:**
- Uses RETURN correctly
- Perfect Browser Library lifecycle
- Excellent UI→API verification pattern
- Clean code structure
- Good UI validation with proper assertions

**Weaknesses:**
- **CRITICAL: ERR13 syntax error in STANDARDS file → Robocop capped at 2.0 (-0.22 points)**
- **CRITICAL: Poor Gherkin structure** - Only 12.5% of tests (2/16) use Gherkin. UI tests: 0/6 use pure Gherkin. API tests: only 2/10 use Gherkin, remaining 8 have NO Given/When/Then keywords
- **CRITICAL: Poor modern syntax adoption** - 39 violations (26 Set Variable + 13 Create Dict/List). Only 18% VAR adoption (6 VAR vs 28 Set Variable). Predominantly uses old-style syntax
- **CRITICAL: Assertions don't validate correct outcomes (Score 3)** - API validation weaknesses: Delete test uses exception handling instead of checking 404; all error tests rely on implicit `expected_status` parameter; doesn't validate error content; Create test only validates title, ignores other fields
- Missing favorite toggle tests
- Limited coverage (16 tests total)
- Uses deprecated Force Tags
- Moderate violation density (14.6/100 LOC)

### GitHub Copilot (4.18 - Rank 1) 🥇
**Strengths:**
- Most comprehensive test coverage (22 tests)
- Excellent documentation quality
- Wide range of test scenarios (CRUD, search, filter, favorites, sort, validation)
- Excellent BASIC API validation - all fields validated, multi-step verification
- **Good modern syntax adoption** - 70% VAR usage (82 VAR vs 35 Set Variable), 38 violations
- **No ERR* or DUP* violations - executable test suite**

**Weaknesses:**
- **Assertions don't fully validate correct outcomes (Score 4)** - Misleading API test names: Tests promise field-specific validation ("Error Should Indicate Missing Title Field") but only check 'detail' exists - similar to weak validation pattern. Not as severe as Claude Code but reduces correctness score.
- Excessive Sleep usage (should use Wait For Elements State)
- 31 VAR06 violations (Set Test Variable scope leakage)
- Uses deprecated Force Tags
- Higher violation density (16.1/100 LOC)
- 4 UI validation keywords in edge-case tests use Log-only

### GitLab Duo (3.87 - Rank 2) 🥈
**Strengths:**
- Most test cases (25 total)
- Only tool testing edit UI flow
- Template usage for validation
- Comprehensive CRUD coverage
- **BEST API validation quality** - validates status codes AND error content, field-specific error validation with templates, no weaknesses found
- **No ERR* or DUP* violations - executable test suite**

**Weaknesses:**
- **CRITICAL: WORST modern syntax adoption** - 127 violations (110 Set Variable + 17 Create Dict/List), **3x worse than any other tool**. Only 21% VAR adoption (30 VAR vs 116 Set Variable). Predominantly uses old-style syntax throughout
- **CRITICAL: UI Favorite toggle (BASIC feature) has Log-only validation (Score 2)** - Cannot verify favorite toggle works. Same severity as Claude Code's weak validations (BASIC features without proper validation). Reduces correctness score significantly.
- **Gherkin structure weakness**: Only 20% pure Gherkin (2/10 UI tests). 80% have "Setup Before" pattern - variable assignments before Given keywords. While Gherkin keywords are used, setup code violates pure BDD structure and reduces readability.
- Defensive API verification clutters UI tests
- Missing dedicated resource files for UI keywords
- Inline code reduces maintainability
- Highest violation density (18.4/100 LOC)
- 1 additional validation test and 4 supplementary keywords use Log-only

### Claude Code (3.81 - Rank 3) 🥉
**Strengths:**
- **BEST Gherkin structure in test cases** - 100% pure Gherkin across all 18 tests (10 UI + 8 API). NO setup code before or within Gherkin flow. Test data generation properly abstracted into keywords.
- **BEST modern syntax adoption** - 68% VAR usage (132 VAR vs 62 Set Variable), only 22 violations. Predominantly uses modern RF 7.x syntax (VAR, RETURN, IF/WHILE)
- Good code structure (4.67 Maintainability)
- Lowest violation density before override (4.3/100 LOC)
- Proper validation keywords exist in ui_keywords.robot (Verify Search Results, Verify Filter Results, Verify Sort Order)

**Weaknesses:**
- **CRITICAL: Poor file organization** - Keyword files (ui_keywords.robot 558 lines, api_keywords.robot 315 lines) at ROOT level instead of in resources/ folder. ~552 lines of inline Keywords in books_ui.robot (MORE than GitLab Duo's 498 lines). Worse organization than GitLab Duo.
- **CRITICAL: Gherkin chains in keywords** - Gherkin keywords call other Gherkin keywords (books_ui.robot:184, 196-197, 560-561; books_api.robot:138), violating keyword implementation principles more severely than Amazon Q
- **CRITICAL: 5+ ERR01 syntax errors in VAR dictionary → Robocop capped at 2.0 (-0.21 points)**
- **Code fails to execute** due to syntax errors in api_keywords.resource:54, 164, 199, 215
- **CRITICAL: Assertions check WRONG things (Score 2)** - 3 BASIC features (Search/Filter/Sort) have assertions present but validate incorrect logic: Search checks count >= 1 (doesn't check if search term matches), Filter checks count >= 0 (doesn't check if category matches), Sort checks count >= 1 (doesn't check sort order). Creates FALSE SENSE OF SECURITY - tests pass when functionality is broken. Severely reduces correctness score.
- Missing CRUD operations entirely (no create/update/delete tests)
- No favorite functionality
- Limited to read-only operations
- Lowest coverage score (2.50)

---

## Recommendations

1. **GitHub Copilot** (4.18): **Fix misleading API test names** - "Error Should Indicate Missing X Field" keywords should validate which field is missing, not just check 'detail' exists (reduces correctness score). Replace Sleep calls with Wait keywords, fix 31 VAR06 violations, replace deprecated Force Tags. Add proper assertions to 4 UI edge-case validation keywords. Continue strong modern syntax adoption.
2. **GitLab Duo** (3.87): **URGENT: Add proper assertions to UI favorite toggle validation** (BASIC feature currently Log-only - severely reduces correctness score to 2). **URGENT: Migrate to modern VAR syntax** - Replace 127 violations (110 Set Variable + 17 Create Dict/List), currently only 21% VAR adoption. Refactor inline code to dedicated resource files, reduce defensive API checks, replace Force Tags. **Maintain excellent API validation practices** as model for other tools.
3. **Claude Code** (3.81): **URGENT: Replace 3 weak UI validation keywords** - Use proper keywords from ui_keywords.robot: "Verify Search Results", "Verify Filter Results", "Verify Sort Order". Currently assertions check wrong things (count >= 0/1 instead of actual values) - **severely reduces correctness score to 2**. **URGENT: Fix file organization** - Move keyword files into resources/ folder, refactor ~552 lines of inline Keywords. **URGENT: Fix Gherkin chains in keywords**. **URGENT: Fix 5+ ERR01 syntax errors** (blocking execution). Maintain excellent modern syntax adoption (best of all tools). Implement CRUD operations.
4. **Amazon Q** (3.69): **CRITICAL: Improve API validation** - Add explicit status code assertions instead of relying on expected_status parameter; validate error message content; validate all fields in create tests (not just title) - **reduces correctness score to 3**. **Fix ERR13 in STANDARDS file** (or exclude from Robocop). **Migrate to VAR syntax** - Replace 39 violations, currently only 18% VAR adoption. **Implement favorite toggle tests** (currently none, reduces coverage score). Implement sort functionality.

---

## Conclusion

**GitHub Copilot** (4.18) achieves the highest overall score due to exceptional coverage breadth (22 tests) and documentation quality, despite execution issues with excessive Sleep usage. **Good modern syntax adoption** with 70% VAR usage (82 VAR vs 35 Set Variable). BASIC API validation is excellent with comprehensive field validation. However, **correctness reduced (Score 4)** due to **misleading API test names** - tests like "Error Should Indicate Missing Title Field" promise field-specific validation but only check that 'detail' exists. While not as severe as other tools' validation issues, test names should accurately reflect what's validated.

**GitLab Duo** (3.87) takes second place with the most comprehensive feature testing (25 tests) and **the best API validation quality of all tools**. GitLab Duo is the only tool with no API validation weaknesses - it validates status codes AND error content with field-specific validation using templates. This demonstrates exceptional testing discipline. However, **critical correctness issue (Score 2)**: **BASIC feature "Toggle Book Favorite Status" has Log-only validation** - cannot verify favorite toggle works, same severity as Claude Code's weak validations. Additional weaknesses: **WORST modern syntax** - 127 violations (3x worse than any other tool) with only 21% VAR adoption. Maintainability issues from defensive coding and inline implementations persist.

**Claude Code** (3.81) drops to third place despite having **the best modern syntax adoption** (68% VAR usage, only 22 violations). **Correctness severely reduced (Score 2)**: **3 BASIC features (Search, Filter, Sort) have assertions that check WRONG things** - assertions present but validate incorrect logic (count >= 0/1 instead of actual search term/category/sort order matches). Creates FALSE SENSE OF SECURITY - tests pass when functionality is broken. Additional critical issues: **Poor file organization** - keyword files at root level instead of resources/ folder, plus ~552 lines of inline keywords (more than GitLab Duo's 498). **Gherkin keywords chain together** (books_ui.robot:184, 196-197; books_api.robot:138), violating the principle that Gherkin should only appear in test cases. Combined with execution-blocking ERR01 syntax errors and missing CRUD operations, Claude Code's perfect test case Gherkin structure and best modern syntax adoption cannot overcome these validation, file organization, and keyword implementation failures.

**Amazon Q** (3.69) remains in fourth place with multiple critical issues: **Correctness reduced (Score 3)** - API validation weaknesses: relies on implicit `expected_status` parameter; doesn't validate error content; Create test only validates title, ignores other fields. **Poor Gherkin structure** - only 12.5% of tests use Given/When/Then (2 out of 16); UI tests have 0% pure Gherkin; 8 out of 10 API tests have NO Gherkin keywords at all. **Poor modern syntax adoption** - 39 violations with only 18% VAR usage (6 VAR vs 28 Set Variable), predominantly old-style syntax. ERR13 syntax error triggers QA Critical Override, capping Robocop at 2.0. Inconsistent testing practices across the board.

**Key Insights:**

1. **Coverage scores must reflect effective testing, not just test existence** - Tests without proper validation don't provide real coverage. Amazon Q (no favorite tests = 0), GitLab Duo (favorite test with Log-only validation = 2), Claude Code (Search/Filter tests with weak validation = 3) received reduced coverage scores. A test that executes a feature but doesn't validate outcomes provides limited value and creates false confidence in test coverage.

2. **Weak validations are more dangerous than Log-only** - Claude Code's UI assertions that check the wrong things (count >= 0/1 instead of actual values) and GitHub Copilot's misleading API test names create false confidence that tests are validating functionality when they're not. This is harder to detect than obvious Log-only keywords.

3. **API validation quality varies significantly** - GitLab Duo demonstrates best practices (explicit status checks, error content validation, templates), while Amazon Q relies on implicit checks without explicit assertions. API tests should validate status codes AND error message content, not just status codes alone.

4. **Assertion quality matters most for BASIC features** - Claude Code's weak validations for 3 BASIC UI features (Search, Filter, Sort) and GitLab Duo's Log-only UI validation for favorite toggle directly reduce coverage scores since these tests don't effectively validate core functionality. Edge-case validation issues are less impactful. However, GitLab Duo's excellent API validation partially compensates.

5. **Misleading test names are a form of weak validation** - GitHub Copilot's "Error Should Indicate Missing Title Field" keywords promise field-specific validation but only check generic 'detail' exists. Test names must accurately reflect what is actually validated.

6. **Proper validation code that exists but isn't used is a critical failure** - Claude Code has correct validation keywords available in ui_keywords.robot but uses weak/incorrect ones instead, suggesting systematic testing issues.

7. **Gherkin chains in keywords violate separation principles** - Claude Code's Gherkin keywords calling other Gherkin keywords (e.g., "Given User Is On Books Library Page" calls "Given User Opens Books Library Application") creates harder-to-maintain keyword hierarchies and violates the principle that Gherkin structure should only appear in test cases, not keyword implementations.

8. **Modern syntax adoption varies dramatically** - Claude Code leads with 68% VAR adoption (132 VAR vs 62 Set Variable, 22 violations), GitHub Copilot follows with 70% VAR usage (82 vs 35, 38 violations), while GitLab Duo (21% VAR, 127 violations) and Amazon Q (18% VAR, 39 violations) lag far behind. GitLab Duo has **3x more violations than any other tool**, indicating systematic old-style syntax throughout. Modern syntax (VAR, RETURN) improves code readability and aligns with RF 7.x best practices.

9. **Syntax errors are non-negotiable** - Amazon Q and Claude Code's structural qualities cannot overcome execution-blocking ERR* violations that cap Robocop scores at 2.0.

10. **Execution correctness must be the foundation** - GitHub Copilot and GitLab Duo maintained executable test suites despite higher violation densities, while Claude Code's cleaner code (4.3/100 LOC) fails to execute.

The ideal approach would combine GitHub Copilot's comprehensive coverage with GitLab Duo's excellent API validation practices, Claude Code's modern syntax adoption and excellent Gherkin test structure, while ensuring zero ERR* violations and proper validation for all BASIC features.
