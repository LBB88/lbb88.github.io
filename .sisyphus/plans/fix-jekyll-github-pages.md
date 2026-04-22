# Fix Jekyll GitHub Pages Deployment

## TL;DR

> **Quick Summary**: Fix the broken GitHub Actions workflow that uploads raw source files instead of Jekyll's built `_site/` directory.
>
> **Deliverables**:
> - Fixed `.github/workflows/pages.yml` with proper Ruby setup and Jekyll build
> - Deployment verified via HTTP checks
>
> **Estimated Effort**: Quick (~15 min)
> **Parallel Execution**: NO - single file sequential fix
> **Critical Path**: Workflow fix → Test push → HTTP verification

---

## Context

### Original Request
"review the current jekyll implementation on github pages, which is currently not updating the website"

### Root Cause Identified
The GitHub Actions workflow at `.github/workflows/pages.yml` has **4 critical issues**:

1. **No Ruby setup** - Missing `actions/setup-ruby@v4`
2. **No dependency installation** - No `bundle install` step
3. **No Jekyll build** - Never runs `bundle exec jekyll build`
4. **Wrong upload path** - Uploads `.` instead of `_site/`

The workflow was scaffolding that never got completed. It deploys raw source files to GitHub Pages instead of the generated site.

### Key Files
- `.github/workflows/pages.yml` - The only file that needs modification
- `Gemfile` and `Gemfile.lock` - Already have correct dependencies (github-pages ~> 232, minima theme)
- `_config.yml` - Already has correct theme and plugin config

---

## Work Objectives

### Core Objective
Fix the GitHub Actions workflow to properly build and deploy the Jekyll site.

### Concrete Deliverables
- `.github/workflows/pages.yml` - Fixed workflow with Ruby setup, bundle install, jekyll build, and correct artifact path

### Definition of Done
- [ ] Workflow syntax is valid YAML
- [ ] `bundle exec jekyll build` runs successfully in CI
- [ ] Artifact uploads only `_site/` contents (not root)
- [ ] GitHub Pages deployment succeeds
- [ ] Site responds at https://lbb88.github.io with HTTP 200
- [ ] `/feed.xml` is accessible (jekyll-feed plugin output)

### Must Have
- Ruby setup step using `actions/setup-ruby@v4`
- `bundle install` before build
- `bundle exec jekyll build` to generate site
- Upload path changed to `_site`
- Existing triggers (`push` on `main`, `workflow_dispatch`) preserved
- Existing permissions preserved

### Must NOT Have
- No Gemfile/Gemfile.lock changes
- No _config.yml changes
- No new features or plugins
- No README changes

---

## Verification Strategy

### Test Infrastructure
- No automated tests in this project (static Jekyll site)
- Verification via GitHub Actions logs and HTTP checks

### QA Policy
Every task includes agent-executed QA scenarios. Evidence saved to `.sisyphus/evidence/`.

---

## Execution Strategy

Single task - fix the workflow file.

---

## TODOs

- [x] 1. Fix GitHub Actions workflow for Jekyll deployment

  **What to do**:
  - Edit `.github/workflows/pages.yml` to add:
    1. `ruby-setup` step with `actions/setup-ruby@v4` and `ruby-version: 3.3` (from Gemfile.lock)
    2. `bundle-install` step - run `bundle install` to install Jekyll and dependencies
    3. `jekyll-build` step - run `bundle exec jekyll build` to generate the site into `_site/`
    4. Change artifact upload path from `'.'` to `'_site'`
  - Preserve existing trigger (`push` on `main`, `workflow_dispatch`)
  - Preserve existing permissions and concurrency settings

  **Must NOT do**:
  - Do not modify Gemfile, Gemfile.lock, or _config.yml
  - Do not change the trigger branches (keep `main`)
  - Do not add new features

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Single file modification, well-defined scope, no ambiguity
  - **Skills**: None required - straightforward YAML edit

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential
  - **Blocks**: F1 (deployment verification)
  - **Blocked By**: None

  **References**:
  - `.github/workflows/pages.yml` - Current broken workflow
  - `Gemfile.lock` - Ruby version 3.3, github-pages 232
  - GitHub Actions `actions/setup-ruby` docs - Standard Ruby setup pattern

  **Acceptance Criteria**:

  **If YAML validation (local)**:
  - [ ] `.github/workflows/pages.yml` passes YAML syntax check

  **QA Scenarios**:

  ```
  Scenario: Workflow file has valid YAML syntax
    Tool: Bash
    Preconditions: File edited successfully
    Steps:
      1. Run: ruby -e "require 'yaml'; YAML.safe_load_file('.github/workflows/pages.yml')"
      2. Assert: Exit code 0, no parsing errors
    Expected Result: YAML is valid, no syntax errors
    Failure Indicators: YAML parsing exception, syntax error
    Evidence: .sisyphus/evidence/task-1-yaml-valid.txt

  Scenario: Workflow triggers on push to main
    Tool: Bash (git)
    Preconditions: Workflow file updated with correct trigger
    Steps:
      1. Read: `.github/workflows/pages.yml` lines 4-5
      2. Assert: `branches: [main]` is present
    Expected Result: Workflow triggers on main branch push
    Failure Indicators: Missing or different branch trigger
    Evidence: .sisyphus/evidence/task-1-trigger-check.txt

  Scenario: Ruby setup step present
    Tool: Bash (grep)
    Preconditions: Workflow file updated
    Steps:
      1. Run: grep -A5 "setup-ruby" .github/workflows/pages.yml
      2. Assert: Output contains "actions/setup-ruby@v4"
    Expected Result: Ruby setup step exists in workflow
    Failure Indicators: Missing Ruby setup action
    Evidence: .sisyphus/evidence/task-1-ruby-setup.txt

  Scenario: Bundle install step present
    Tool: Bash (grep)
    Preconditions: Workflow file updated
    Steps:
      1. Run: grep "bundle install" .github/workflows/pages.yml
      2. Assert: Exit code 0, command found
    Expected Result: `bundle install` step exists
    Failure Indicators: Missing bundle install step
    Evidence: .sisyphus/evidence/task-1-bundle-install.txt

  Scenario: Jekyll build step present
    Tool: Bash (grep)
    Preconditions: Workflow file updated
    Steps:
      1. Run: grep "jekyll build" .github/workflows/pages.yml
      2. Assert: Exit code 0, command found
    Expected Result: `bundle exec jekyll build` step exists
    Failure Indicators: Missing Jekyll build step
    Evidence: .sisyphus/evidence/task-1-jekyll-build.txt

  Scenario: Artifact upload path is _site
    Tool: Bash (grep)
    Preconditions: Workflow file updated
    Steps:
      1. Run: grep -B1 -A1 "upload-pages-artifact" .github/workflows/pages.yml
      2. Assert: Output contains "path: '_site'" (not "path: '.'")
    Expected Result: Artifact upload path is _site directory
    Failure Indicators: Still uploads root directory (path: '.')
    Evidence: .sisyphus/evidence/task-1-artifact-path.txt
  ```

  **Evidence to Capture**:
  - [ ] Each grep/check saved to evidence file
  - [ ] YAML validation output captured

  **Commit**: YES
  - Message: `fix(ci): add Jekyll build step to GitHub Actions workflow`
  - Files: `.github/workflows/pages.yml`
  - Pre-commit: None (no tests to run locally)

---

## Final Verification Wave

> After workflow is committed and push triggers CI, verify deployment.

- [x] F1. **GitHub Actions Run Verification** — `unspecified-high`
  Trigger workflow via push to main or `workflow_dispatch`. Check Actions log for:
  - Ruby setup completes
  - bundle install succeeds
  - jekyll build completes without error
  - Artifact contains `_site/` files (not root)
  - Deployment succeeds
  Output: `Build [PASS/FAIL] | Artifact [PASS/FAIL] | Deploy [PASS/FAIL] | VERDICT`
  **VERDICT: PASS** - Run 24787565859 succeeded in 57s

- [x] F2. **HTTP Verification** — `unspecified-high`
  After deployment completes, verify site is live:
  - `curl -s -o /dev/null -w "%{http_code}" https://lbb88.github.io` returns 200
  - `curl -s https://lbb88.github.io/feed.xml` returns valid XML
  - Page content contains expected text from index.markdown
  Output: `Homepage [200/ERROR] | Feed [PASS/FAIL] | Content [PASS/FAIL] | VERDICT`
  **VERDICT: PASS** - Homepage 200, feed.xml valid, content shows "Welcome" text

---

## Commit Strategy

- **1**: `fix(ci): add Jekyll build step to GitHub Actions workflow` - `.github/workflows/pages.yml`

---

## Success Criteria

### Verification Commands
```bash
ruby -e "require 'yaml'; YAML.safe_load_file('.github/workflows/pages.yml')"  # YAML valid
grep "path: '_site'" .github/workflows/pages.yml  # Correct artifact path
curl -s -o /dev/null -w "%{http_code}" https://lbb88.github.io  # Returns 200
```

### Final Checklist
- [ ] Workflow has Ruby setup step
- [ ] Workflow has bundle install step
- [ ] Workflow has jekyll build step
- [ ] Artifact path is `_site`
- [ ] CI run succeeds
- [ ] Site is accessible at https://lbb88.github.io