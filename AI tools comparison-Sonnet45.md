# AI Tools Comparison and Evaluation Matrix (Markdown)

Tools compared: Amazon Q, GitLab Duo, GitHub Copilot, Claude Code
Schedule: Results in 2026-02-26

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

## Robocop Analysis Scoring Guide (Category 10)

## General Scoring Principle

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

### 3. Deprecation warnings (DEPR, 0301)* Excludes Modern Syntax issues (see Row 9).

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

### Calculate the average of all rows above.

⚠️ QA Critical Override: If the "Total violation count" row is scored 0 or 1 (due to syntax errors or duplication), the Category Subtotal cannot exceed 2.0, regardless of the mathematical average. Rationale: Clean formatting cannot compensate for broken or duplicated code.

## Assumptions

- Environment: same BASE_URL, CI runner, Browser=chromium, RequestsLibrary sessions or equivalent.
- Libraries: Browser/RequestsLibrary preferred; curl/Process acceptable but penalize for portability if flaky.
- No manual DB resets; tests must clean up state via API.
- Syntax: Modern RF 7.4.1 syntax preferred (VAR, RETURN, IF/WHILE/TRY, Test Tags) over deprecated patterns (Set Variable, [Return], Run Keyword If, Force Tags).

## Dataset and Scenarios

- Seed at least 3 books, varied categories/authors/pages; include favorite toggles.
- Use identical test data across tools when possible to compare assertions and locators.

## Tagging Conventions

- UI: ui, smoke, crud, search, filter, favorites, validation, sort
- API: api, crud, error-handling, validation, consistency, concurrency
- Critical paths tagged "critical"; smoke for minimum viability.

## Do's and Don'ts (Adherence)

- Do separate keywords/resources (page objects, API helpers).
- Do use waits over sleeps; justify any Sleep with async reasons.
- Don't embed Gherkin inside keyword bodies; keep GWT only in Test Cases.
- Don't hardcode environment-specific paths; use variables/resources.
- Don't use the Log keyword as the sole action within a functional test step. Every step must perform a tangible action or a verifiable assertion using library keywords.

## Criteria Relevance Check

- Test Quality & Structure: Relevant. All tools use GWT-style tests and keyword resources.
- Maintainability & Modularity: Relevant. All suites split common.resource and keyword files; reuse varies.
- Coverage: Relevant. UI and API CRUD, search/filter, favorites, and negatives are present to different extents.
- Correctness: Relevant. Differences in library usage (RequestsLibrary vs Process/PowerShell), locator quality, and assertion strictness matter.
- Execution Quality: Relevant. Waits vs sleeps and cleanup impact stability in CI.
- Adherence to Project Guidelines: Relevant. Each tool was provided with the same Robot Framework standards file to generate its own guidance context; thus, the evaluation applies uniformly.
- Architectural Alignment: Relevant. Endpoints and flows (UI → API → DB) reflected in tests with varying depth.
- Prompt Responsiveness & Control: Relevant. Suites follow instructions to different degrees without hallucinations.
- Usability & CI Integration: Relevant. Portability and environment assumptions differ (RequestsLibrary vs OS-specific tooling).

## Feature Coverage Summary

Feature coverage verified by reading all test files (books_api.robot + books_ui.robot for each tool):

| Feature                | Amazon Q | GitLab Duo | GitHub Copilot | Claude Code |
| ---------------------- | -------- | ---------- | -------------- | ----------- |
| API: Add               | ✓        | ✓          | ✓              | ✓           |
| API: Update            | ✓        | ✓          | ✓              | ✓           |
| API: Delete            | ✓        | ✓          | ✓              | ✓           |
| API: Favorite toggle   | ✗        | ✗          | ✓              | ✗           |
| UI: Add                | ✓        | ✗          | ✓              | ✗           |
| UI: Update             | ✗        | ✗          | ✓              | ✗           |
| UI: Delete             | ✗        | ✗          | ✓              | ✗           |
| UI: Search             | ✓        | ✓          | ✓              | ✓           |
| UI: Filter             | ✓        | ✗          | ✓              | ✗           |
| UI: Sort               | ✗        | ✗          | ✓              | ✗           |
| UI: Favorite toggle    | ✗        | ✗          | ✓              | ✗           |

GitHub Copilot is the only tool that covers all 7 application features (Add, Update, Delete, Search, Filter, Sort, Favorite) in both API and UI. Claude Code UI suite is explicitly read-only (books_ui.robot states "Test Strategy: Read-only operations"). GitLab Duo UI covers only Search and View. Amazon Q UI covers Add, Search, and Filter only.



0. Baseline Metrics

Raw volume and structure metrics measured directly from the generated test suites before scoring. LOC and violation counts sourced from Category 10 (Robocop analysis); test case counts sourced from Category 11.

| Metric                          | Amazon Q | GitLab Duo | GitHub Copilot | Claude Code |
| ------------------------------- | -------- | ---------- | -------------- | ----------- |
| Total lines of code (LOC)       | ~460     | ~1451      | ~1200          | ~1753       |
| Test files                      | 2        | 2          | 2              | 2           |
| Resource files                  | 4        | 3          | 3              | 3           |
| UI test cases                   | 4        | 6          | 11             | 7           |
| API test cases                  | 5        | 9          | 10             | 12          |
| Total test cases                | 9        | 15         | 21             | 19          |
| Robocop total violations        | ~106     | ~221       | ~160           | ~110        |
| Violation density (per 100 LOC) | 23       | 15         | 13             | 6.3         |

**Notes:**
- All tools produced 2 test files (books_api.robot, books_ui.robot) and at least 3 resource files.
- Amazon Q generated one extra common resource (common_ui.resource separate from common.resource), hence 4 resource files.
- Claude Code uses a subdirectory structure (resources/api/, resources/pages/) rather than flat layout.
- LOC figures cover all robot and resource files in each tool's test suite.
- GitHub Copilot has the most test cases (21); Claude Code has the most API tests (12); Amazon Q has the fewest tests overall (9).
- Despite having the fewest tests, Amazon Q has the highest violation density (23/100 LOC); Claude Code has the lowest (6.3/100 LOC).

---

🧩 Evaluation Matrix (Markdown Table)

1. Test Quality & Structure (15%)

| Criteria                                               | Amazon Q | GitLab Duo | GitHub Copilot | Claude Code |
| ------------------------------------------------------ | -------- | ---------- | -------------- | ----------- |
| Test naming clarity and consistency                    | 2        | 3          | 2              | 3           |
| Given/When/Then structure used correctly               | 4        | 3          | 2              | 4           |
| Readability and clarity                                | 3        | 4          | 4              | 4           |
| Proper use of variables (${SCALAR}, @{LIST}, &{DICT})  | 1        | 2          | 3              | 2           |
| Keyword documentation quality                          | 3        | 4          | 4              | 4           |
| Settings section ordering (Documentation → Tags → ...) | 2        | 4          | 4              | 4           |
| Category Subtotal (avg)                                | **2.5**  | **3.3**    | **3.2**        | **3.5**     |

**Amazon Q:** Two naming mismatches: "User Should Be Able To Create Book Via UI" verifies creation via `Get All Books Via API` instead of a UI assertion; "User Should Be Able To Filter Books By Category" only checks that book cards exist (count > 0) without verifying the displayed books actually belong to the selected category. GWT step keywords used in test cases only; keyword bodies are implementation-only (books_api.robot:58–75). Basic structure; minimal inline comments; function over form. Zero VAR syntax used anywhere — complete reliance on deprecated Set Variable, Set Test Variable (~10+), and Create Dictionary (~2 instances); e.g. books_api.robot:66 `Set Test Variable ${API_RESPONSE} ${response}`, api_keywords.resource:8 `Create Dictionary title=${title}`, common.resource:19 `Set Suite Variable`; @{LIST} and &{DICT} types present but old-style creation throughout. Documentation tags present on keywords; single-line descriptions. ORD02 violations: Documentation placed after [Arguments] in 6 keywords (api_keywords.resource:7,24,31,39,45,51).

**GitLab Duo:** One naming mismatch: "API Should Handle Concurrent Requests" uses a sequential `FOR` loop making 5 GET requests (books_api.robot) — not parallel/concurrent; the name promises concurrency testing but the implementation is serial. Otherwise naming is clear and consistent across API and UI suites. GWT pattern present in test cases; occasional step-style naming leaks into keyword bodies. Good Documentation strings on most keywords; clear intent; section comments ("# GIVEN Keywords"). Partial VAR adoption: books_api.robot uses VAR with scope=TEST/SUITE extensively (lines 180,211,257–259,342,502) ✓, but BooksAPI.resource falls back to Set Variable (lines 162–163 `Set Variable ${response.json()}`) and Create List (line 246); BooksPageUI.resource:74 still uses `Create List`; broken VAR at common.resource:65,71 assigns keyword call as string literal instead of executing it. Multi-line documentation explains purpose and arguments in most resource files. Settings ordered correctly in most files; no ORD02 violations.

**GitHub Copilot:** Four naming mismatches in books_ui.robot, three of which are phantom tests that always pass regardless of application behavior: "Sort Books Alphabetically" — `Then Books Should Appear In Alphabetical Order` contains only `Log Books sorted by title - visual order validated console=True` (line 413), no sort assertion; "Toggle Book Favorite Status" — both Then keywords (`Then Book Should Be Marked As Favorite` line 437 and `Then Book Should Be Unmarked As Favorite` line 442) are Log-only, no UI state verification; "User Should Not Be Able To Submit Empty Book Form" — both `Then Form Should Show Validation Errors` (line 452) and `Then No Book Should Be Created` (line 457) are Log-only; and "View Favorite Books Only" — only verifies the favorite book appears (line 408), never checks non-favorites are hidden. GWT in test cases — but `And` is never used in either suite across all 21 tests; every continuation uses a duplicate Given/Given, Then/Then, or When/When instead (e.g. books_api.robot lines 32–37: `Given Given When Then Then Then`; lines 51–56: `Given Given Given When Then Then`). Keyword bodies are clean implementation. Good docstrings on all keywords; consistent structure makes suite easy to scan. Mix of VAR and Set Variable; correct scalar/list/dict types but inconsistent syntax across files. Consistent Documentation on all keywords; explains what each keyword does. Proper Settings ordering throughout all resource and test files; no ORD02 violations.

**Claude Code:** One naming mismatch: "API Should Support Partial Book Update" (books_api.robot:184) — documentation explicitly states "Verify PATCH /books/{id} is not supported (returns 405)"; the test name implies PATCH is supported but the test verifies the opposite. Otherwise naming is precise and comprehensive across all 19 tests. GWT prefix keywords (Given/When/Then/And) used exclusively in *** Test Cases ***; implementation separated (books_api.robot:270–370). Thorough Documentation on every keyword (books_api.robot:372–401); section comments throughout. VAR used only for &{} dict/params creation (BooksAPI.resource:91,105,120,168,346) and selectors (BooksPage.resource:169,180,190,227); Set Variable pervasive for all simple assignments (~20 instances in BooksAPI.resource alone, e.g. `${endpoint}= Set Variable /books/${book_id}` and `${book}= Set Variable ${response.json()}`); Set Suite Variable at common.resource:66; Catenate at common.resource:98,148. Detailed documentation with Action:/Verification:/Setup: prefixes in keyword docs (books_ui.robot:148,162). Settings ordered correctly; Documentation before Arguments throughout.

---

2. Maintainability & Modularity (15%)

| Criteria                               | Amazon Q | GitLab Duo | GitHub Copilot | Claude Code |
| -------------------------------------- | -------- | ---------- | -------------- | ----------- |
| Reusable keywords generated            | 3        | 4          | 4              | 5           |
| Duplication avoidance                  | 3        | 4          | 4              | 4           |
| Logical separation into resource files | 2        | 4          | 4              | 5           |
| Separation of concerns (UI vs logic)   | 3        | 4          | 3              | 4           |
| Ease of extending or modifying tests   | 3        | 4          | 4              | 4           |
| Meaningful comments (explaining "why") | 2        | 4          | 4              | 4           |
| Category Subtotal (avg)                | **2.7**  | **4.0**    | **3.8**        | **4.3**     |

**Amazon Q:** api_keywords.resource and ui_keywords.resource created; keywords reused across test files. common.resource and common_ui.resource duplicate URL variables and initialization logic; limited factoring. Two near-identical common files (common.resource, common_ui.resource) with different BASE_URL; separation is shallow. UI interaction in ui_keywords.resource; some UI state management in test file directly. Basic keywords; extending requires understanding duplicated common files. Documentation tags only; no inline strategic comments explaining design decisions.

**GitLab Duo:** Comprehensive keyword library: common.resource, BooksAPI.resource, BooksPageUI.resource, each with 15–30 keywords. Shared common.resource avoids cross-suite duplication; API and UI-specific resources separate. Clean 3-file separation: common.resource (shared), BooksAPI.resource (API), BooksPageUI.resource (UI). BooksPageUI.resource handles all UI interactions; BooksAPI.resource handles API calls. Modular design with clear extension points; add to BooksAPI.resource or BooksPageUI.resource. Section comments with # HTTP GET Operations, # Verification Keywords (BooksAPI.resource:38,112).

**GitHub Copilot:** Clean keyword libraries: common.resource, api_keywords.resource, ui_keywords.resource; good reuse across suites. Shared common.resource used by both suites; helpers not duplicated between api_keywords and ui_keywords. Clean 3-file separation: common.resource, api_keywords.resource, ui_keywords.resource. Some concern mixing; test-scoped variable leakage (books_api.robot:122,129,131) couples steps. Clear structure supports modification; adding new keywords straightforward. Section separator comments and Documentation strings explain rationale.

**Claude Code:** Most comprehensive keyword library; 4 resource files including subdirectory structure resources/api/ and resources/pages/. Well-factored keywords across BooksAPI.resource and BooksPage.resource; minimal duplication observed. Best separation: api/ and pages/ subdirectory structure; BooksAPI.resource, BooksPage.resource each fully scoped. Clean separation: resources/pages/BooksPage.resource for UI, resources/api/BooksAPI.resource for API calls. Well-structured subdirectory resources; new API or UI keywords clearly belong in respective files. Good section comments (# When Keywords, # Then Keywords) and keyword-level explanations.

---

3. Coverage (10%)

| Criteria                         | Amazon Q | GitLab Duo | GitHub Copilot | Claude Code |
| -------------------------------- | -------- | ---------- | -------------- | ----------- |
| CRUD operations tested           | 3        | 3          | 5              | 3           |
| Search & filtering tested        | 2        | 2          | 5              | 2           |
| Favorite toggle tested           | 0        | 0          | 4              | 0           |
| Negative cases & edge cases      | 2        | 2          | 5              | 4           |
| API test coverage                | 2        | 3          | 5              | 4           |
| UI + backend round-trip coverage | 3        | 3          | 4              | 2           |
| Category Subtotal (avg)          | **2.0**  | **2.2**    | **4.7**        | **2.5**     |

**Amazon Q:** CRUD operations: GET all, GET by ID, POST, PUT, DELETE all present in API (books_api.robot:18–55); UI covers Add and Read only; no Update or Delete UI tests. Search: basic search test present in books_ui.robot:27–45; no API search test; no category filtering. Favorite: no favorite toggle tests in either suite; /books/{id}/favorite endpoint never called. Negatives: GET nonexistent book (404) tested; no validation failures or invalid inputs. API coverage: 5 tests covering basic CRUD only; no validation or error breadth. Round-trip: creates via UI form then verifies book exists via API call (books_ui.robot:60–64).

**GitLab Duo:** CRUD operations: full API CRUD (Add/Update/Delete) in 9 tests; UI suite is entirely read-only (Search + View only across 6 tests); no UI Create, Update, or Delete at all. Search: basic title search in UI (books_ui.robot); no API search test; no category filter test. Favorite: no favorite toggle keyword defined in BooksAPI.resource; no favorite tests anywhere in the suite. Negatives: 404 GET and 422 validation tested in API; limited negative coverage overall. API coverage: 9 tests covering CRUD plus validation and concurrent GET. Round-trip: API test setup creates data, UI suite views existing data; implicit connection only.

**GitHub Copilot:** CRUD operations: full CRUD in both API (10 tests) and UI (11 tests); update and delete UI flows explicitly tested. Search: multiple search tests including title search, author search; combined search+category filter in UI. Favorite: toggle tested with mark and unmark flows in both API (books_api.robot:67–75) and UI (books_ui.robot:104–113); UI favorites filter tested. Negatives: most comprehensive — 404 GET, 404 UPDATE, 404 DELETE, 422 validation failure, invalid ID all tested. API coverage: 10 API tests with broad coverage: CRUD, 422 validation, 404 errors, PATCH, partial update. Round-trip: explicit — creates via API in setup, validates in UI, deletes via API in teardown.

**Claude Code:** CRUD operations: full CRUD in API (12 tests); UI suite is explicitly read-only (books_ui.robot documentation: "Test Strategy: Read-only operations"); no UI Add, Update, or Delete tests. Search: search tested in UI (books_ui.robot); no filtering by category or favorite; no combined search+filter. Favorite: no favorite tests in any file; API never calls /books/{id}/favorite; PATCH test only checks that PATCH returns 405 on the main books endpoint. Negatives: strong API negative coverage — GET 404, UPDATE 404, DELETE 404, 422 validation, 405 PATCH; five distinct negative scenarios. API coverage: 12 API tests (most of any tool); comprehensive CRUD + validation + CRUD lifecycle chain. Round-trip: UI suite is independent and read-only; no write operations in UI tests; API and UI suites do not share test data creation.

---

4. Correctness (15%)

| Criteria                                                    | Amazon Q | GitLab Duo | GitHub Copilot | Claude Code |
| ----------------------------------------------------------- | -------- | ---------- | -------------- | ----------- |
| Robot Framework syntax correctness                          | 3        | 3          | 4              | 4           |
| Valid library usage (Browser/RequestsLibrary)               | 3        | 4          | 4              | 4           |
| Browser context management (New Browser → Context → Page)   | 3        | 4          | 4              | 4           |
| Selector stability (data-testid > role > text > CSS)        | 3        | 3          | 4              | 3           |
| RequestsLibrary session management (Create/Use Session)     | 4        | 4          | 4              | 4           |
| Assertions validate correct outcomes                        | 3        | 4          | 4              | 4           |
| Avoids meaningless "Log" steps instead of actual assertions | 3        | 4          | 4              | 3           |
| Proper assertion types (Should Be Equal vs Should Contain)  | 3        | 4          | 4              | 4           |
| Domain logic accuracy (books, categories, favorites)        | 3        | 4          | 4              | 4           |
| Category Subtotal (avg)                                     | **3.2**  | **3.8**    | **4.0**        | **3.8**     |

**Amazon Q:** Runs correctly; Force Tags (DEPR02), Set Variable throughout; functional but outdated. Both libraries used correctly at basic level; sessions created and destroyed; Browser keywords valid. New Browser → Context → Page lifecycle present in Suite Setup; context teardown on suite end. CSS selectors used (css=.books-grid, id=pages); reasonable stability; no data-testid. Session created in Suite Setup, deleted in Suite Teardown; On Session keywords used consistently. Basic assertions (Status Should Be, Should Be Equal); limited field validation depth. Log calls present alongside assertions; no test steps that are Log-only. Mostly Should Be Equal; limited type-aware assertions like Should Be Equal As Integers. Books domain correct; category field used; basic title/author/pages; favorites field absent.

**GitLab Duo:** Mostly correct; broken VAR at common.resource:65,71 (VAR ${current_time} Get Current Date string assignment, not keyword call). Correct Browser 19.x and RequestsLibrary 0.9.7 usage; proper keyword selection throughout. Proper 3-step context lifecycle in Suite Setup (common.resource:16–27); context closed in teardown. CSS selectors (css=.book-card, #search-input) in BooksPageUI.resource; no data-testid; Nth element patterns present. Create Session in Suite Setup; Delete All Sessions in teardown; books_api session properly scoped. Good assertion depth: Status Should Be, Should Contain, Dictionary Should Contain Key, Should Be Equal As Integers. Logs used as informational supplementary; all test outcomes verified by proper assertion keywords. Should Be Equal As Integers for pages/counts; Should Contain for text matching; type-appropriate. Full domain model: title, author, pages, category, favorites all covered in BooksAPI.resource.

**GitHub Copilot:** Mostly modern syntax; some deprecated patterns; syntax errors required ~10 fix iterations. Correct library usage; Browser with retry_assertions_for; RequestsLibrary On Session keywords. Proper New Browser → New Context → New Page pattern; Suite Setup/Teardown manage lifecycle. Mix of CSS and ID selectors; some role-based; consistent selector strategy across ui_keywords.resource. Proper session lifecycle; Setup Books API Session / Teardown Books API Session keywords. Strong assertions: Should Be Equal As Integers for numeric fields; Should Contain for lists. Tests use proper assertions; Log steps are supplementary debug info, not substitutes. Good type-aware assertions: Should Be Equal As Integers for numeric, Should Contain for text. Comprehensive domain: title, author, pages, category, favorites, year; search by multiple fields.

**Claude Code:** Correct syntax overall; some Set Variable and Force Tags persist; no syntax errors after fixes. Proper library usage; Browser timeout=10s retry_assertions_for=1s (books_ui.robot:8); RequestsLibrary sessions. New Browser → New Context → New Page in Initialize UI Test Suite (books_ui.robot:274–290); proper teardown. CSS selectors throughout BooksPage.resource; xpath in some places; no data-testid strategy. Initialize API Test Suite creates session; Teardown deletes sessions; On Session keywords throughout. Good assertion variety: Should Be Equal, Should Contain, Should Be True, Status code checks. Some keyword bodies are Log-heavy; a few keywords log then return without asserting outcome. Mix of type-appropriate assertions; Should Be Equal As Integers used for page counts. Full domain model coverage including favorites; pagination awareness in UI tests.

---

5. Execution Quality (10%)

| Criteria                            | Amazon Q | GitLab Duo | GitHub Copilot | Claude Code |
| ----------------------------------- | -------- | ---------- | -------------- | ----------- |
| Test reliability (non-flaky)        | 2        | 4          | 4              | 5           |
| Correct wait usage vs sleep         | 1        | 5          | 4              | 5           |
| Runtime efficiency                  | 3        | 4          | 4              | 4           |
| Test setup & teardown correctness   | 3        | 5          | 4              | 5           |
| Cleanups avoid leaving state behind | 4        | 4          | 2              | 4           |
| Category Subtotal (avg)             | **2.6**  | **4.4**    | **3.6**        | **4.6**     |

**Amazon Q:** Sleep 2s and Sleep 1s in ui_keywords.resource:36,44 without justification; hardcoded delays cause flakiness risk. Two unjustified Sleep calls (ui_keywords.resource:36 Sleep 2s, :44 Sleep 1s); no Wait For Elements State in those paths. Small suite (9 tests) runs quickly; Sleep adds ~3s per test pass through ui_keywords. Suite Setup/Teardown present; Initialize Browser/API; basic but correct (common_ui.resource:16–27). Per-test cleanup in both common.resource and common_ui.resource: `DELETE On Session api /books/${BOOK_ID}` called in Test Cleanup if BOOK_ID is set; exception-handled; systematic and reliable.

**GitLab Duo:** No Sleep calls in any resource file; all UI interactions use proper Wait For Elements State. No Sleep; exclusively Wait For Elements State and Wait For Load State throughout BooksPageUI.resource. Efficient with proper waits; no artificial delays; 15 tests complete without sleep overhead. Proper lifecycle: Suite Setup with Initialize Browser + API session; Suite Teardown closes browser and sessions. API cleanup in teardown via DELETE; test data prefixed TEST_ to isolate.

**GitHub Copilot:** Minimal Sleep; retry_assertions_for=3s on Browser session; mainly wait-based approach. Mainly Wait For Elements State used; no unjustified sleep; minor page load waits acceptable. Good efficiency; reasonable timeouts; retry_assertions_for reduces flaky retries. Proper setup/teardown; Setup Books API Session and Teardown Books API Session keywords. No book data cleanup in any teardown: `Teardown Books API Session` only calls `Delete All Sessions` (closes HTTP sessions); `Cleanup UI Test` only takes a screenshot; books created during tests are not deleted.

**Claude Code:** Browser configured with timeout=10s retry_assertions_for=1s (books_ui.robot:8); no Sleep calls. Exclusively Wait For Elements State; Browser retry config handles transient element waits. Efficient; 19 tests; parameterized timeouts (${MEDIUM_TIMEOUT}, ${DEFAULT_TIMEOUT}) in BooksPage.resource. Comprehensive: Initialize UI Test Suite, Initialize API Test Suite, Setup Individual UI/API Test (books_ui.robot:274–305). Systematic cleanup: created books deleted in teardown keywords; suite-level and test-level cleanup.

---

6. Adherence to Project Guidelines (10%)

| Criteria                                               | Amazon Q | GitLab Duo | GitHub Copilot | Claude Code |
| ------------------------------------------------------ | -------- | ---------- | -------------- | ----------- |
| Settings section ordering (Documentation → Tags → ...) | 2        | 4          | 4              | 4           |
| Variable naming conventions (${}, @{}, &{})            | 3        | 3          | 3              | 4           |
| Uses page object pattern where appropriate             | 2        | 4          | 3              | 4           |
| Proper tagging (ui/api/smoke/crud)                     | 3        | 3          | 3              | 3           |
| Uses test templates when beneficial                    | 2        | 3          | 3              | 4           |
| No Gherkin inside keywords (GWT in test cases only)    | 4        | 4          | 3              | 4           |
| Category Subtotal (avg)                                | **2.7**  | **3.5**    | **3.2**        | **3.8**     |

**Amazon Q:** ORD02: Documentation placed after [Arguments] in 6 separate keywords throughout api_keywords.resource (lines 7,24,31,39,45,51). Variables mostly uppercase ${SCALAR}; &{DICT} used in Create Dictionary; mix of naming styles. ui_keywords.resource has UI keywords but not a true POM; locators mixed with logic. Force Tags (deprecated DEPR02); tags: ui/api/books present; no smoke/crud structured taxonomy. No Robot Framework test templates used in either suite. GWT step keywords only appear in *** Test Cases ***; keyword bodies are pure implementation.

**GitLab Duo:** Settings ordered correctly: Documentation before Arguments in all Keywords; no ORD02 violations. VAR07 violations: lowercase non-local vars (e.g. ${ui_test_book_data}, ${search_title}) at books_ui.robot:172,277; otherwise consistent. BooksPageUI.resource is a proper Page Object: locators in Variables section, interaction keywords below (BooksPageUI.resource:1–176). Force Tags used (DEPR02 in books_ui.robot:17, books_api.robot:25); TAG07 violations; ui/api/books tagged. Limited template usage; repeating data creation patterns not factored into templates. Clean GWT separation: Given/When/Then only in Test Cases; no GWT terms in keyword body implementations.

**GitHub Copilot:** Proper Settings ordering throughout all resource and test files; no ORD02 violations. VAR07 violations: lowercase scope vars like ${all_books_response}, ${create_response} (books_api.robot:151,156,161); otherwise correct. ui_keywords.resource partial POM; locators and keywords co-located but not fully separated. Force Tags used (DEPR02 in books_ui.robot:17, books_api.robot:17); regression tags but no structured smoke/crud taxonomy. No explicit Test Template usage but repeated patterns exist; partial mitigation via keyword abstraction. Mostly clean; some keyword names carry GWT-prefix style that can cause GWT/implementation boundary confusion.

**Claude Code:** Settings ordered correctly; Documentation before Arguments consistently across all files. Consistently uppercase non-local variables; no VAR07 violations in Robocop output. resources/pages/BooksPage.resource is dedicated POM; locators in *** Variables ***, keywords separate. Force Tags used (DEPR02); TAG07 violations at books_ui.robot:25, books_api.robot:26; no smoke taxonomy. CRUD cycle keyword When User Performs Complete CRUD Cycle (books_api.robot:371) approaches template pattern; reusable steps. GWT prefix keywords (Given/When/Then/And) called only from *** Test Cases ***; implementations in separate keyword section.

---

7. Architectural Alignment (5%)

| Criteria                                  | Amazon Q | GitLab Duo | GitHub Copilot | Claude Code |
| ----------------------------------------- | -------- | ---------- | -------------- | ----------- |
| Reflects real system architecture         | 3        | 4          | 4              | 4           |
| Correct usage of REST endpoints           | 3        | 3          | 4              | 4           |
| Covers UI → API → DB flows where relevant | 3        | 4          | 5              | 4           |
| Category Subtotal (avg)                   | **3.0**  | **3.7**    | **4.3**        | **4.0**     |

**Amazon Q:** FastAPI backend reflected; books-service:8000 used correctly; basic layers present. Main CRUD endpoints /books/ and /books/{id} covered; favorites endpoint (/books/{id}/favorite) absent. Some round-trip: creates book via UI form, then validates existence via API GET (books_ui.robot:60–64).

**GitLab Duo:** System architecture well reflected; UI and API layers cleanly separated; domain model accurate. Endpoints mostly correct; /health 404 issue required fix during test run; /books/{id}/favorite referenced in resource but never tested. UI→API round-trip: setup creates via API, UI validates display, teardown deletes via API; explicit chain.

**GitHub Copilot:** Good architectural reflection; layered approach mirrors actual books-service architecture. Comprehensive endpoint coverage: /books/, /books/{id}, /books/{id}/favorite all tested. Explicit round-trip coverage including DB verification via API after UI action; books created/validated/deleted through layers.

**Claude Code:** System architecture well reflected; API and UI test layers match actual service structure. Correct endpoints; CRUD + PATCH (405 verified) covered; endpoint paths match FastAPI route definitions. Good round-trip in API tests: CRUD lifecycle; UI suite is independent and read-only, no write round-trips.

---

8. Prompt Responsiveness & Control (3%)

| Criteria                          | Amazon Q | GitLab Duo | GitHub Copilot | Claude Code |
| --------------------------------- | -------- | ---------- | -------------- | ----------- |
| Follows instructions accurately   | 4        | 4          | 3              | 4           |
| Consistency across generations    | 3        | 4          | 3              | 4           |
| Avoids hallucinating requirements | 4        | 4          | 3              | 3           |
| Category Subtotal (avg)           | **3.7**  | **4.0**    | **3.0**        | **3.7**     |

**Amazon Q:** Followed most instructions; books-service:8000 correct; BDD structure implemented; minimal deviations. Consistent naming and patterns within the small suite; limited cross-generation data point. No hallucinated endpoints or requirements; tests reflect actual Books API spec.

**GitLab Duo:** Good instruction following; BDD structure, resource separation, and POM all in place; /health issue was environment-related not instruction failure. Consistent naming, structure, and keyword patterns across API and UI suite files. No hallucinations; /health endpoint might have been assumed based on common FastAPI patterns but otherwise accurate.

**GitHub Copilot:** Required 10 fix iterations; localhost vs books-service, status code 201 vs 200, button text mismatches, search term issues. Some inconsistency across 10 fix requests; each iteration changed patterns slightly; variable scope style drift. localhost URL assumption; incorrect status codes (201 vs 200 for CREATE, 200 vs 405 for PATCH); button text assumptions.

**Claude Code:** Good instruction following; PATCH 405, DELETE 200, status code corrections needed; follows BDD structure correctly. Consistent patterns throughout books_api.robot and books_ui.robot; keyword naming uniform. Status code assumptions ("Hero" search term not seeded DB; PATCH returns 405 not 200; DELETE returns 200 not 204).

---

9. Usability & CI Integration (2%)

| Criteria                                                 | Amazon Q | GitLab Duo | GitHub Copilot | Claude Code |
| -------------------------------------------------------- | -------- | ---------- | -------------- | ----------- |
| Containerized CI readiness (artifacts, exit codes, envs) | 3        | 4          | 3              | 4           |
| Easy to use with existing workflow                       | 3        | 4          | 3              | 4           |
| Minimal manual fixes required                            | 4        | 3          | 2              | 3           |
| Category Subtotal (avg)                                  | **3.3**  | **3.7**    | **2.7**        | **3.7**     |

**Amazon Q:** Uses books-service:8000; CI-ready structure; Sleep calls increase fragility in headless CI. Simple 2-file structure (books_api.robot, books_ui.robot + resources); straightforward to add to CI. Very few fixes needed; ~2 minor adjustments (URL and assertion); fastest time-to-running.

**GitLab Duo:** Container-ready; proper service host references; no Sleep; Browser headless=true configured. Clean directory structure; resource separation is clear; straightforward to integrate into existing Robot Framework CI. /health endpoint fix and URL adjustments required; moderate fixing effort before suite ran cleanly.

**GitHub Copilot:** localhost references needed fixing before CI usable; after fix, CI-ready structure. 10 fix iterations required; final state is clean but needed more initial manual work. Each of 10 fix requests was targeted and clear; individual fixes were small though volume was higher.

**Claude Code:** Container-ready; proper environment variable usage; Browser headless=true; books-service:8000 throughout. Well-organized structure; resource subdirectories; can be added to CI pipeline with minimal configuration. Status code corrections and search term fix needed (books_api.robot:161 "Hero" replacing hallucinated term).

---

10. Static Code Quality - Robocop Analysis (10%)

| Criteria                                            | Amazon Q | GitLab Duo | GitHub Copilot | Claude Code |
| --------------------------------------------------- | -------- | ---------- | -------------- | ----------- |
| Total violation count (fewer is better)             | 1        | 2          | 2              | 3           |
| Naming violations (NAME02, NAME18)                  | 5        | 5          | 5              | 5           |
| Deprecation warnings (DEPR*, 0301)                  | 3        | 3          | 3              | 3           |
| Variable scope issues (VAR06 - no test variables)   | 0        | 0          | 0              | 0           |
| Formatting issues (SPC01 whitespace, SPC05 spacing) | 4.8      | 0          | 2.0            | 2.8         |
| Import ordering issues (IMP01, IMP02)               | 3.2      | 4.2        | 3.8            | 3.4         |
| Tag configuration issues (TAG07 - unnecessary tags) | 5        | 4.0        | 5              | 4.0         |
| Unused variables (VAR02)                            | 4.0      | 2.5        | 0.5            | 3.0         |
| Modern syntax compliance (VAR01, RETURN01)          | 0        | 0          | 0              | 0           |
| Category Subtotal (avg)                             | **2.9**  | **2.3**    | **2.4**        | **2.7**     |

**Amazon Q:** ~106 violations / ~460 LOC = 23/100 LOC → exceeds 21+/100 threshold; density driven by api_keywords.resource (15 violations) and books_api.robot (44 violations). Zero NAME02/NAME18 violations; all keywords use Title Case. 2 × DEPR02 (Force Tags in books_ui.robot:16 and books_api.robot:15); score 3. ~20 VAR06 violations across common.resource and books_api.robot; capped at 0. 2 × SPC01 (books_ui.robot:3, books_api.robot:3); score 4.8; no SPC05. 9 import violations; score 3.2. Zero TAG07 violations. 2 × VAR02 (books_api.robot:115, :139); score 4.0. ~30 DEPR05/DEPR06 violations (Set Variable, Create Dictionary throughout); capped at 0.

**GitLab Duo:** ~221 violations / ~1451 LOC = 15/100 LOC → 11–20 range; inflated by SPC01 from verbose Documentation continuation lines. Zero NAME02/NAME18 violations. 2 × DEPR02 (Force Tags); score 3. ~14 VAR06 violations; capped at 0. ~105 × SPC01 violations (every Documentation continuation line in BooksPageUI.resource and BooksAPI.resource); capped at 0. 4 import violations; score 4.2. 2 × TAG07 (Default Tags smoke in both suites); score 4.0. 5 × VAR02; score 2.5. ~18 DEPR05/DEPR06 violations (Set Variable in multiple files); capped at 0.

**GitHub Copilot:** ~160 violations / ~1200 LOC = 13/100 LOC → 11–20 range; DEPR05 density high in api_keywords.resource and books_api.robot (30+ DEPR05). Zero NAME02/NAME18 violations. 2 × DEPR02 (Force Tags); score 3. ~30 VAR06 violations; capped at 0. ~30 × SPC01 (books_ui.robot trailing whitespace in multiple keywords); score 2.0. 6 import violations; score 3.8. Zero TAG07 violations. ~9 × VAR02; score 0.5. ~42 DEPR05/DEPR06 violations; capped at 0.

**Claude Code:** ~110 violations / ~1753 LOC = 6.3/100 LOC → 6–10 range; large codebase dilutes violations; SPC05 and DEPR05 are primary drivers. Zero NAME02/NAME18 violations. 2 × DEPR02 (Force Tags in books_ui.robot:24, books_api.robot:25); score 3. ~20 VAR06 violations; capped at 0. ~22 × SPC05 (comment lines before keywords, e.g. books_ui.robot:146,160,236,274); score 2.8. 8 import violations; score 3.4. 2 × TAG07 (Default Tags smoke in both suites); score 4.0. 4 × VAR02; score 3.0. ~52 DEPR05 violations (Set Variable pervasive in BooksAPI.resource and books_api.robot); capped at 0.

---

11. Test Suite Volume & Missing Cases (5%)

| Criteria                                          | Amazon Q | GitLab Duo | GitHub Copilot | Claude Code |
| ------------------------------------------------- | -------- | ---------- | -------------- | ----------- |
| UI test case count                                | 4        | 6          | 11             | 7           |
| API test case count                               | 5        | 9          | 10             | 12          |
| Total test case count                             | 9        | 15         | 21             | 19          |
| Relative volume score (0–5)                       | 1        | 3          | 5              | 4           |
| Missing: search+filter combination                | 0        | 2          | 5              | 2           |
| Missing: sort scenarios (title/author/pages)      | 0        | 1          | 5              | 0           |
| Missing: edit UI flow                             | 0        | 0          | 5              | 0           |
| Missing: validation breadth (multi-field/types)   | 2        | 3          | 5              | 3           |
| Missing: favorite toggle variants (unmark/filter) | 0        | 0          | 5              | 0           |
| Missing: concurrency / data consistency (API)     | 0        | 1          | 3              | 2           |
| Missing: combined CRUD chains (multi-step API)    | 0        | 1          | 5              | 3           |
| Missing: negative 404 coverage breadth            | 4        | 2          | 5              | 4           |
| Category Subtotal (avg)                           | **0.8**  | **1.4**    | **4.8**        | **2.0**     |

**Amazon Q:** Smallest suite at 9 tests covers only basic happy paths; significant test gap relative to feature set. No combined search+filter scenario; only isolated search test present. No sort tests. No UI edit test; only create and list tested in UI. GET 404 only; no POST validation (missing required fields, wrong types). No favorites coverage at all. No multi-step CRUD chains. GET 404 for nonexistent ID tested (books_api.robot:46–55); basic but present.

**GitLab Duo:** Mid-range volume; 15 tests functional but leaves notable gaps. Basic search tested; no combined search+filter (category + search term simultaneously). No explicit sort scenarios. No UI CRUD at all — books_ui.robot covers only Search and View; no Add, Update, or Delete UI tests. Some POST validation (422) in API. No favorite keyword defined anywhere in BooksAPI.resource; no favorite tests in API or UI. 9 API tests are each single-operation; no explicit chained CRUD sequence. GET 404 covered; UPDATE 404 and DELETE 404 not verified.

**GitHub Copilot:** Largest and most comprehensive suite; 21 tests cover broadest feature surface. Combined search and filter scenarios explicitly tested; multiple field search present. Sort tested (title); sort scenarios in UI suite. Edit book UI flow explicitly tested: fill form, submit, verify update; round-trip via API. Comprehensive validation: missing title, wrong pages type, missing required fields; 422 status tested. Favorite mark and unmark tested; UI favorites filter tested; toggle state verified. Explicit CRUD chain test: create → read → update → delete in single test; state verified at each step. Comprehensive 404: GET 404, UPDATE 404, DELETE 404 all explicitly tested.

**Claude Code:** Strong API volume at 12 tests (most of any tool). Search tested in UI; no filter by category or favorite; no combined search+filter scenario. No sort scenarios tested. books_ui.robot explicitly states "Test Strategy: Read-only operations (no data modification)"; no UI Add, Update, or Delete tests. Validation present: missing field (422), incorrect status codes; moderate breadth. No favorite tests in any file; API never calls /books/{id}/favorite. CRUD lifecycle test in books_api.robot:371 covers full Create→Read→Update→Delete chain. GET 404 and DELETE 404 tested; PATCH 405 tested; UPDATE 404 tested; four negative error scenarios.

---

🏁 Final Weighted Score Summary

| Tool           | Weighted Score | Rank | Notes                                                                                                                                                                                                                                                                                                    |
| -------------- | -------------- | ---- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GitHub Copilot | **3.64 / 5.0** | #1   | Best overall coverage and volume (21 tests); only tool covering all 7 app features in both API and UI; `And` never used — all 21 tests use duplicate Given/Given, Then/Then instead; 3 phantom UI tests (Sort, Toggle Favorite, Empty Form have Log-only assertions); required most fix iterations (~10) |
| Claude Code    | **3.59 / 5.0** | #2   | Best architecture and modularity; most API tests (12); strongest execution quality (Browser retry config); "Should Support Partial Book Update" test verifies PATCH returns 405; UI suite is read-only, missing Add/Update/Delete/Filter/Sort/Favorite UI coverage                                       |
| GitLab Duo     | **3.35 / 5.0** | #3   | Strong execution quality (no Sleep, proper waits); partial VAR adoption (books_api.robot modern, BooksAPI.resource still old-style); "Concurrent Requests" test is actually sequential; UI covers only Search/View with no CRUD at all; no favorite coverage anywhere in the suite                       |
| Amazon Q       | **2.65 / 5.0** | #4   | Fastest time-to-running with minimal fixes; zero VAR syntax usage (complete reliance on Set Variable, Set Test Variable, Create Dictionary); Sleep calls and deprecated syntax are significant liabilities; coverage too narrow at 9 tests                                                               |

**Weighted Score Calculation:**
Total Score (100%) = Sum of (Category Weight × Category Average Score)

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

**Score Breakdown:**

| Category                          | Weight | Amazon Q | GitLab Duo | GitHub Copilot | Claude Code |
| --------------------------------- | ------ | -------- | ---------- | -------------- | ----------- |
| 1. Test Quality & Structure       | 15%    | 2.5      | 3.3        | 3.2            | 3.5         |
| 2. Maintainability & Modularity   | 15%    | 2.7      | 4.0        | 3.8            | 4.3         |
| 3. Coverage                       | 10%    | 2.0      | 2.2        | 4.7            | 2.5         |
| 4. Correctness                    | 15%    | 3.2      | 3.8        | 4.0            | 3.8         |
| 5. Execution Quality              | 10%    | 2.6      | 4.4        | 3.6            | 4.6         |
| 6. Adherence to Guidelines        | 10%    | 2.7      | 3.5        | 3.2            | 3.8         |
| 7. Architectural Alignment        | 5%     | 3.0      | 3.7        | 4.3            | 4.0         |
| 8. Prompt Responsiveness          | 3%     | 3.7      | 4.0        | 3.0            | 3.7         |
| 9. Usability & CI Integration     | 2%     | 3.3      | 3.7        | 2.7            | 3.7         |
| 10. Static Code Quality (Robocop) | 10%    | 2.9      | 2.3        | 2.4            | 2.7         |
| 11. Volume & Missing Cases        | 5%     | 0.8      | 1.4        | 4.8            | 2.0         |
| **Weighted Final Score**          |        | **2.65** | **3.35**   | **3.64**       | **3.59**    |
| **Rank**                          |        | **#4**   | **#3**     | **#1**         | **#2**      |

## Robocop Audit Reference

Tools should be evaluated against Robocop 7.2.0 static analysis. Key violation categories:

**Critical Issues (Score 0-1):**
- ERR*: Syntax/Parsing errors (automatic fail for row 1)
- DUP*: Code duplication findings (caps row 1 at max 1)
- NAME02/NAME18: Keyword naming/calling convention violations (should use Title Case)
- DEPR02: Deprecated statements (Force Tags, Run Keyword If)
- DEPR05: Set Variable instead of VAR statement
- DEPR06: Create Dictionary instead of VAR
- RETURN01: Use RETURN instead of [Return]
- VAR01: Use VAR instead of assignment syntax
- VAR06: Set Test Variable usage (scope leakage)

**Moderate Issues (Score 2-3):**
- SPC01: Trailing whitespace
- SPC05: Empty lines between keywords
- IMP01/IMP02: Import ordering
- TAG07: Unnecessary Default Tags
- 0301: Deprecated FOR loop syntax

**Minor Issues (Score 4-5):**
- VAR02: Unused variables

## Guideline Reference for Adherence

**Robot Framework 7.4.1 Standards:**
- Modern syntax: VAR, RETURN, IF/WHILE/TRY (replaces Set Variable, [Return], Run Keyword If)
- Test Tags instead of Force Tags (deprecated RF 6.0+)
- Four-space indentation
- Settings section ordering: Documentation → Tags → Setup → Teardown → Template → Imports
- Variable naming: ${SCALAR}, @{LIST}, &{DICT}
- Keyword naming: Title Case (not lowercase with spaces)

**Browser Library 19.12.3:**
- Context lifecycle: New Browser → New Context → New Page
- Selector strategies: data-testid (best) > role (good) > text (fair) > CSS (poor)
- Wait mechanisms: Wait For Elements State (not Sleep)

**RequestsLibrary 0.9.7:**
- Session management: Create Session → Use *On Session keywords
- Proper cleanup: Delete All Sessions in teardown
- Response validation: Status Should Be, Response Body Should Contain
