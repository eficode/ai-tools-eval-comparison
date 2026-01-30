# Robot Framework Test Generation – Comparison and Evaluation Matrix (Markdown)

Tools compared: [Tool 1], [Tool 2], [Tool 3], [Tool 4]
Schedule: Results in [DATE]

📌 Scoring Scale
0–5 score, where: 0 = Not acceptable, 5 = Excellent

## How to Use

- Evaluate each tool’s UI and API suites against the same app state and dataset.
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
- Syntax: Modern RF 7.x syntax preferred (VAR, RETURN, IF/WHILE/TRY, Test Tags) over deprecated patterns (Set Variable, [Return], Run Keyword If, Force Tags).

## Dataset and Scenarios

- Seed at least 3 books, varied categories/authors/pages; include favorite toggles.
- Use identical test data across tools when possible to compare assertions and locators.

## Tagging Conventions

- UI: ui, smoke, crud, search, filter, favorites, validation, sort
- API: api, crud, error-handling, validation, consistency, concurrency
- Critical paths tagged “critical”; smoke for minimum viability.

## Do’s and Don’ts (Adherence)

- Do separate keywords/resources (page objects, API helpers).
- Do use waits over sleeps; justify any Sleep with async reasons.
- Don’t embed Gherkin inside keyword bodies; keep GWT only in Test Cases.
- Don’t hardcode environment-specific paths; use variables/resources.

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


🧩 Evaluation Matrix (Markdown Table)

1. Test Quality & Structure (15%)

| Criteria                                                | [Tool 1] | [Tool 2] | [Tool 3] | [Tool 4] |
| ------------------------------------------------------- | -------- | -------- | -------- | -------- |
| Test naming clarity and consistency                     |          |          |          |          |
| Given/When/Then structure used correctly                |          |          |          |          |
| Readability and clarity                                 |          |          |          |          |
| Proper use of variables (${SCALAR}, @{LIST}, &{DICT})   |          |          |          |          |
| Keyword documentation quality                           |          |          |          |          |
| Settings section ordering (Documentation → Tags → ...)  |          |          |          |          |
| Category Subtotal (avg)                                 |          |          |          |          |

2. Maintainability & Modularity (15%)

| Criteria                               | [Tool 1] | [Tool 2] | [Tool 3] | [Tool 4] |
| -------------------------------------- | -------- | -------- | -------- | -------- |
| Reusable keywords generated            |          |          |          |          |
| Duplication avoidance                  |          |          |          |          |
| Logical separation into resource files |          |          |          |          |
| Separation of concerns (UI vs logic)   |          |          |          |          |
| Ease of extending or modifying tests   |          |          |          |          |
| Meaningful comments (explaining "why") |          |          |          |          |
| Category Subtotal (avg)                |          |          |          |          |

3. Coverage (10%)

| Criteria                         | [Tool 1] | [Tool 2] | [Tool 3] | [Tool 4] |
| -------------------------------- | -------- | -------- | -------- | -------- |
| CRUD operations tested           |          |          |          |          |
| Search & filtering tested        |          |          |          |          |
| Favorite toggle tested           |          |          |          |          |
| Negative cases & edge cases      |          |          |          |          |
| API test coverage                |          |          |          |          |
| UI + backend round-trip coverage |          |          |          |          |
| Category Subtotal (avg)          |          |          |          |          |

4. Correctness (15%)

| Criteria                                                    | [Tool 1] | [Tool 2] | [Tool 3] | [Tool 4] |
| ----------------------------------------------------------- | -------- | -------- | -------- | -------- |
| Robot Framework syntax correctness                          |          |          |          |          |
| Valid library usage (Browser/RequestsLibrary)               |          |          |          |          |
| Browser context management (New Browser → Context → Page)   |          |          |          |          |
| Selector stability (data-testid > role > text > CSS)        |          |          |          |          |
| RequestsLibrary session management (Create/Use Session)     |          |          |          |          |
| Assertions validate correct outcomes                        |          |          |          |          |
| Proper assertion types (Should Be Equal vs Should Contain)  |          |          |          |          |
| Domain logic accuracy (books, categories, favorites)        |          |          |          |          |
| Category Subtotal (avg)                                     |          |          |          |          |

5. Execution Quality (10%)

| Criteria                            | [Tool 1] | [Tool 2] | [Tool 3] | [Tool 4] |
| ----------------------------------- | -------- | -------- | -------- | -------- |
| Test reliability (non-flaky)        |          |          |          |          |
| Correct wait usage vs sleep         |          |          |          |          |
| Runtime efficiency                  |          |          |          |          |
| Test setup & teardown correctness   |          |          |          |          |
| Cleanups avoid leaving state behind |          |          |          |          |
| Category Subtotal (avg)             |          |          |          |          |

6. Adherence to Project Guidelines (10%)

| Criteria                                               | [Tool 1] | [Tool 2] | [Tool 3] | [Tool 4] |
| ------------------------------------------------------ | -------- | -------- | -------- | -------- |
| Settings section ordering (Documentation → Tags → ...) |          |          |          |          |
| Variable naming conventions (${}, @{}, &{})            |          |          |          |          |
| Uses page object pattern where appropriate             |          |          |          |          |
| Proper tagging (ui/api/smoke/crud)                     |          |          |          |          |
| Uses test templates when beneficial                    |          |          |          |          |
| No Gherkin inside keywords (GWT in test cases only)    |          |          |          |          |
| Category Subtotal (avg)                                |          |          |          |          |

7. Architectural Alignment (5%)

| Criteria                                  | [Tool 1] | [Tool 2] | [Tool 3] | [Tool 4] |
| ----------------------------------------- | -------- | -------- | -------- | -------- |
| Reflects real system architecture         |          |          |          |          |
| Correct usage of REST endpoints           |          |          |          |          |
| Covers UI → API → DB flows where relevant |          |          |          |          |
| Category Subtotal (avg)                   |          |          |          |          |

8. Prompt Responsiveness & Control (3%)

| Criteria                          | [Tool 1] | [Tool 2] | [Tool 3] | [Tool 4] |
| --------------------------------- | -------- | -------- | -------- | -------- |
| Follows instructions accurately   |          |          |          |          |
| Consistency across generations    |          |          |          |          |
| Avoids hallucinating requirements |          |          |          |          |
| Category Subtotal (avg)           |          |          |          |          |

9. Usability & CI Integration (2%)

| Criteria                                              | [Tool 1] | [Tool 2] | [Tool 3] | [Tool 4] |
| ----------------------------------------------------- | -------- | -------- | -------- | -------- |
| Containerized CI readiness (artifacts, exit codes, envs) |          |          |          |          |
| Easy to use with existing workflow                    |          |          |          |          |
| Minimal manual fixes required                         |          |          |          |          |
| Category Subtotal (avg)                               |          |          |          |          |

10. Static Code Quality - Robocop Analysis (10%)

| Criteria                                                | [Tool 1] | [Tool 2] | [Tool 3] | [Tool 4] |
| ------------------------------------------------------- | -------- | -------- | -------- | -------- |
| Total violation count (fewer is better)                 |          |          |          |          |
| Naming violations (NAME02, NAME18)                      |          |          |          |          |
| Deprecation warnings (DEPR*, 0301)                      |          |          |          |          |
| Variable scope issues (VAR06 - no test variables)       |          |          |          |          |
| Formatting issues (SPC01 whitespace, SPC05 spacing)     |          |          |          |          |
| Import ordering issues (IMP01, IMP02)                   |          |          |          |          |
| Tag configuration issues (TAG07 - unnecessary tags)     |          |          |          |          |
| Unused variables (VAR02)                                |          |          |          |          |
| Modern syntax compliance (VAR01, RETURN01)              |          |          |          |          |
| Category Subtotal (avg)                                 |          |          |          |          |

11. Test Suite Volume & Missing Cases (5%)

| Criteria                                         | [Tool 1] | [Tool 2] | [Tool 3] | [Tool 4] |
| ------------------------------------------------ | -------- | -------- | -------- | -------- |
| UI test case count                               |          |          |          |          |
| API test case count                              |          |          |          |          |
| Total test case count                            |          |          |          |          |
| Relative volume score (0–5)                      |          |          |          |          |
| Missing: search+filter combination               |          |          |          |          |
| Missing: sort scenarios (title/author/pages)     |          |          |          |          |
| Missing: edit UI flow                            |          |          |          |          |
| Missing: validation breadth (multi-field/types)  |          |          |          |          |
| Missing: favorite toggle variants (unmark/filter)|          |          |          |          |
| Missing: concurrency / data consistency (API)    |          |          |          |          |
| Missing: combined CRUD chains (multi-step API)   |          |          |          |          |
| Missing: negative 404 coverage breadth           |          |          |          |          |
| Category Subtotal (avg)                          |          |          |          |          |

🏁 Final Weighted Score Summary

| Tool           | Weighted Score | Rank | Notes                                                                                       |
| -------------- | -------------- | ---- | ------------------------------------------------------------------------------------------- |
| [Tool 1]       |                |      |                                                                                             |
| [Tool 2]       |                |      |                                                                                             |
| [Tool 3]       |                |      |                                                                                             |
| [Tool 4]       |                |      |                                                                                             |

**Weighted Score Calculation:**
Total Score (100%) = Sum of (Category Weight × Category Average Score)

**Category Weights:**
1. Test Quality & Structure: 20%
2. Maintainability & Modularity: 20%
3. Coverage: 10%
4. Correctness: 15%
5. Execution Quality: 10%
6. Adherence to Project Guidelines: 10%
7. Architectural Alignment: 5%
8. Prompt Responsiveness & Control: 3%
9. Usability & CI Integration: 2%
10. Static Code Quality (Robocop): 10%
11. Test Suite Volume & Missing Cases: 5%

**Total: 110% (Normalized to 100%)**

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

**Tool-Specific Context:**
- GitLab Duo: .gitlab/duo/project-context.md, workflow-context.md, mr-review-instructions.md, code-standards.md
- GitHub Copilot: .github/copilot/review-guide.md, standards.md, workflow.md, architecture.md, context.md
- Amazon Q: .amazonq/rules/project-context.yaml, workflow-context.yaml, mr-review-instructions.yaml, code-standards.yaml

