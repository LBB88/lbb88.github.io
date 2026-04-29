# Plan: Media Import Functionality for validate-new-pages Skill

## TL;DR

> **Quick Summary**: Enhance validate-new-pages skill to import media from `/import/pages/` and `/import/_posts/` folders into Jekyll assets, rename and move markdown files to `/src/` or `/src/_posts/`, embed media references in markdown, and log all processed files.
>
> **Deliverables**:
> - `import-media.py` - Media discovery, move, sanitization, deduplication
> - `media-placement.py` - Algorithm for inserting media at top + spacing throughout
> - Modified `validate-new-pages.py` - Add `--import` flag, integrate before validation
> - `processed.log` - Text log tracking processed imports
> - Updated `SKILL.md` - New functionality documented at top
>
> **Estimated Effort**: Medium
> **Parallel Execution**: NO - sequential Python scripts
> **Critical Path**: Requirements → Modules → Integration → Testing → Documentation

---

## Context

### Original Request
Add media import functionality to validate-new-pages skill:
1. `/import/pages/YYYYMMDD_*` folders → media to assets, rename md to `topic-slug.md`, move to `/src/`
2. `/import/_posts/YYYYMMDD_*` folders → media to assets, rename md to `YYYY-MM-DD_slug.md`, move to `/src/_posts/`
3. Embed media references in markdown body (first at top, remaining spaced throughout)
4. Maintain text log of processed files

### Confirmed Requirements
- **Pages destination**: `/src/` root (no subfolder)
- **Slug selection**: First media filename (alphabetically sorted)
- **Image format**: Standard `![alt](path)` (no space before bracket)
- **Video format**: `[![thumb](/path)](video/path)`
- **Spacing**: First media at body start, remaining evenly distributed by heading sections

### Metis Review Findings
- Need idempotency (running twice = same result)
- Need deduplication strategy (file-1.jpg, file-2.jpg if exists)
- Need rollback on failure (no partial state)
- Max file size: 50MB recommended guardrail

---

## Work Objectives

### Core Objective
Automate media import from `/import/` folders into Jekyll structure with proper markdown embedding.

### Concrete Deliverables

**1. import-media.py** (new file)
- Folder discovery: glob `YYYYMMDD_*` pattern in `/import/pages/` and `/import/_posts/`
- Media detection by extension: images (`.jpg,.jpeg,.png,.gif,.webp`), videos (`.mp4,.webm,.mov`)
- File move with sanitization: spaces→hyphens, special chars removed
- Deduplication: append `-1`, `-2` if target exists
- Slug generation: first media filename (without extension) used for md rename
- Log entries to `processed.log`

**2. media-placement.py** (new file)
- Parse markdown: separate frontmatter from body
- Find insertion points:
  - First media: after frontmatter, before first H1/H2 heading
  - Spacing: divide body into equal sections by heading count (default: 3 sections if no headings)
- Insert media references at calculated positions

**3. Modified validate-new-pages.py**
- Add `--import` flag
- When `--import` set: call import functions before existing validation
- Move renamed content.md to destination based on type (pages→`/src/`, posts→`/src/_posts/`)
- Existing flags (`--pages`, `--posts`, `--apply`) work unchanged

**4. processed.log** (new file)
- Location: `.opencode/skills/validate-new-pages/processed.log`
- Format: `[YYYY-MM-DD HH:MM:SS] TYPE: folder → dest.md | media: file1, file2`

**5. Updated SKILL.md**
- New section at TOP of skill
- Document `--import` flag and behavior
- Include usage examples

### Definition of Done
- [x] Media files moved from import folders to `/src/assets/images/` or `/src/assets/videos/`
- [x] Markdown files renamed and moved to correct destination
- [x] Markdown body contains media references (first at top, remaining spaced)
- [x] Log file has entry for each processed folder
- [x] Import folders cleaned up (media removed, md moved)
- [x] Idempotent: running twice produces same result

### Must Have
- Process both `/import/pages/` and `/import/_posts/` folders
- Rename pages: `topic-slug.md` (slug from first media filename)
- Rename posts: `YYYY-MM-DD_slug.md` (date from folder, slug from media)
- Jekyll-compatible markdown: images `![alt](path)`, videos `[![thumb](path)](path)`
- First media at body start, remaining evenly spaced
- Text log tracking all processed imports

### Must NOT Have (Guardrails)
- No thumbnail generation (use existing files only)
- No image resizing/compression
- No external URL downloading
- No modification of existing `/src/` content (only import-processed)
- No processing of files outside defined import paths

---

## Verification Strategy

### QA Policy - Agent-Executed Scenarios

**Scenario 1: Pages import (single image)**
```
Tool: Bash
Steps:
  1. Create /import/pages/20260428_test/ with content.md + photo.jpg
  2. Run: python3 .opencode/skills/validate-new-pages/validate-new-pages.py --import
  3. Verify: /src/assets/images/photo.jpg exists
  4. Verify: /src/photo.md exists (renamed from content.md, slug from “photo”)
  5. Verify: /src/photo.md body starts with ![photo](/assets/images/photo.jpg)
  6. Verify: /import/pages/20260428_test/ folder media removed
  7. Verify: processed.log has entry for 20260428_test
Expected Result: All assertions pass
Evidence: .sisyphus/evidence/1-pages-single-image.md
```

**Scenario 2: Posts import (multiple media with video)**
Note: Slug comes from first media filename alphabetically (&quot;thumb&quot; from thumb.jpeg), not folder suffix
```
Tool: Bash
Steps:
  1. Create /import/_posts/20260428_test/ with content.md + thumb.jpeg + video.mp4
  2. Run import
  3. Verify: /src/assets/images/thumb.jpeg exists
  4. Verify: /src/assets/videos/video.mp4 exists
  5. Verify: /src/_posts/2026-04-28-thumb.md exists (renamed from content.md, slug from first media &quot;thumb&quot;)
  6. Verify: first media reference at body start (either image or video format)
  7. Verify: second media reference spaced in body
  8. Verify: video format is [![thumb](/assets/images/thumb.jpeg)](/assets/videos/video.mp4)
Expected Result: All assertions pass
Evidence: .sisyphus/evidence/2-posts-multiple-media.md
```

**Scenario 3: Deduplication handling**
```
Tool: Bash
Preconditions: /src/assets/images/photo.jpg already exists
Steps:
  1. Create folder with photo.jpg
  2. Run import
  3. Verify: imported file renamed to photo-1.jpg
  4. Verify: markdown references photo-1.jpg
  5. Verify: original photo.jpg preserved
Expected Result: No overwrite, renamed file used
Evidence: .sisyphus/evidence/3-deduplication.md
```

**Scenario 4: Idempotency check**
```
Tool: Bash
Steps:
  1. Run import on fresh folder
  2. Run import again on same folder (already cleaned, so no-op expected)
  3. Verify: no duplicate log entries
  4. Verify: same final state
Expected Result: Second run is no-op
Evidence: .sisyphus/evidence/4-idempotency.md
```

**Scenario 5: Error rollback**
```
Tool: Bash
Steps:
  1. Create folder with invalid/corrupted media file
  2. Run import
  3. Verify: no partial state (if move partially fails, rollback)
  4. Verify: error logged
Expected Result: Clean failure, no corruption
Evidence: .sisyphus/evidence/5-rollback.md
```

---

## Execution Strategy

### Sequential Steps (NO parallelization)

```
Step 1: Create import-media.py
  ├── Folder discovery (glob YYYYMMDD_* pattern)
  ├── Media type detection by extension
  ├── File move with sanitization
  ├── Deduplication (append -1, -2 if exists)
  ├── Slug generation from first media filename
  └── Log entry generation

Step 2: Create media-placement.py
  ├── Frontmatter/body parsing
  ├── Find first heading position
  ├── Calculate spacing intervals (by heading count)
  └── Insert media references at positions

Step 3: Modify validate-new-pages.py
  ├── Add --import argument
  ├── When --import: call import functions before validation
  ├── Rename content.md based on type (page→slug.md, post→YYYY-MM-DD_slug.md)
  └── Move to correct destination (/src/ or /src/_posts/)

Step 4: Create processed.log placeholder
  └── Empty file with header comment

Step 5: Update SKILL.md
  └── New section at top documenting --import functionality

Step 6: Manual QA testing (5 scenarios)

Step 7: Final oracle review
```

### Dependency Matrix

- **Step 1**: None (foundation)
- **Step 2**: Step 1 (uses import-media functions)
- **Step 3**: Steps 1+2 (integrates modules)
- **Step 4**: None (standalone file)
- **Step 5**: Steps 1-4 (documents everything)
- **Step 6**: Steps 1-5 (needs working implementation)
- **Step 7**: All steps (final review)

---

## TODOs

- [x] 1. Create import-media.py module

  **What to do**:
  - Folder discovery: glob for `YYYYMMDD_*` in `/import/pages/` and `/import/_posts/`
  - Media detection: images (`.jpg,.jpeg,.png,.gif,.webp`), videos (`.mp4,.webm,.mov`)
  - File move: copy to `/src/assets/images/` or `/src/assets/videos/`, sanitize filename
  - Sanitization: spaces→hyphens, remove special chars, lowercase extension
  - Deduplication: if target exists, try `-1`, `-2`, etc.
  - Slug generation: first media file (sorted alphabetically), strip extension
  - Log entry format: `[TIMESTAMP] TYPE: folder → dest.md | media: files`

  **Must NOT do**:
  - No thumbnail generation
  - No external downloads
  - No modification outside import/ and assets/

  **Recommended Agent Profile**:
  - **Category**: `quick` (straightforward file operations)
  - **Skills**: `[]`
  - **Reason**: Well-defined patterns from validate-new-pages.py

  **References**:
  - `validate-new-pages.py:1-20` - Path resolution patterns
  - `validate-templates.py:45-60` - Frontmatter parsing for date extraction
  - Observed import folder: `20260428_112958/content.md` structure

  **Acceptance Criteria**:
  - [ ] `python3 import-media.py --help` shows usage
  - [ ] Discovers folders in both /import/pages/ and /import/_posts/
  - [ ] Correctly moves image to images/, video to videos/
  - [ ] Sanitizes filenames (photo.jpg, not “photo?.jpg”)

- [x] 2. Create media-placement.py algorithm module

  **What to do**:
  - Parse markdown content (frontmatter vs body)
  - Find first H1/H2 heading position
  - Calculate spacing: divide body into N+1 sections (N = number of headings, min 3 sections)
  - Insert first media after frontmatter, before first heading
  - Insert remaining media at equal intervals
  - Return modified content

  **Must NOT do**:
  - No semantic analysis
  - No AI-generated alt text (use filename as alt)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **References**:
  - `validate-templates.py:45-60` - Frontmatter regex parsing
  - Example content.md structure (205 lines with headings)

  **Acceptance Criteria**:
  - [ ] `insert_media(content, media_list)` function exists
  - [ ] First image appears after frontmatter, before first heading
  - [ ] Remaining media evenly spaced
  - [ ] Video format: `[![alt](thumb_path)](video_path)`

- [x] 3. Modify validate-new-pages.py with --import flag

  **What to do**:
  - Add `--import` argument to parser
  - When `--import`:
    - Call import_media() for both pages and posts folders
    - Get slug from first media filename
    - Rename content.md:
      - Pages: `{slug}.md` → `/src/{slug}.md`
      - Posts: `content.md` → `/src/_posts/YYYY-MM-DD_{slug}.md`
    - Clean up import folder (media removed, md moved)
    - Log to processed.log
  - Existing behavior unchanged when `--import` not specified

  **Must NOT do**:
  - Don't break existing --pages, --posts, --apply flags
  - Don't import unless --import explicitly specified

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **References**:
  - `validate-new-pages.py:55-77` - Argument parser structure

  **Acceptance Criteria**:
  - [ ] `python3 validate-new-pages.py --import` processes folders
  - [ ] `python3 validate-new-pages.py` unchanged behavior
  - [ ] Both /import/pages/ and /import/_posts/ processed
  - [ ] Log entry created per folder

- [x] 4. Create processed.log placeholder

  **What to do**:
  - Create at `.opencode/skills/validate-new-pages/processed.log`
  - Add header: `# Processed Import Log\n# Format: [TIMESTAMP] TYPE: folder → dest.md | media: files`

  **Recommended Agent Profile**:
  - **Category**: `quick`

  **Acceptance Criteria**:
  - [ ] File exists with header comment

- [x] 5. Update SKILL.md

  **What to do**:
  - Add new section at TOP (before existing content)
  - Document:
    - `--import` flag purpose and usage
    - What happens: media moves, md renamed and moved, references embedded
    - Log file location
    - Spacing behavior

  **Must NOT do**:
  - Don't remove existing documentation
  - Don't change existing behavior descriptions

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: `[]`

  **References**:
  - Current SKILL.md structure and formatting

  **Acceptance Criteria**:
  - [ ] New section at top of skill
  - [ ] --import flag documented with examples

- [x] 6. Manual QA testing (5 scenarios)

  **What to do**:
  - Run all scenarios from Verification Strategy
  - Capture evidence to `.sisyphus/evidence/`
  - Fix any issues

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: `[]`

  **Acceptance Criteria**:
  - [ ] Scenario 1 (pages single image): PASS
  - [ ] Scenario 2 (posts multiple media): PASS
  - [ ] Scenario 3 (deduplication): PASS
  - [ ] Scenario 4 (idempotency): PASS
  - [ ] Scenario 5 (rollback): PASS

- [x] 7. Final oracle review

  **What to do**:
  - Verify all Must Have items implemented
  - Verify no Must NOT Have items present
  - Check evidence files exist

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: `[]` (oracle for verification)

  **Acceptance Criteria**:
  - [ ] All Must Have: PRESENT
  - [ ] All Must NOT Have: ABSENT
  - [ ] Evidence files: ALL PRESENT
  - [ ] VERDICT: APPROVE or REJECT

---

## Final Verification Wave

- [x] F1. Plan Compliance Audit — `oracle`
  - Verify all Must Have implemented
  - Verify all Must NOT Have absent
  - Check media formats correct (images: `![alt](path)`, videos: `[![thumb](path)](path)`)
  - Verify log file created and updated

- [x] F2. Code Quality Review — `unspecified-high`
  - No debug prints left in
  - Proper error handling with rollback
  - No partial state on failure

- [x] F3. Real Manual QA — `unspecified-high`
  - Execute all 5 scenarios
  - Capture evidence

- [x] F4. Scope Fidelity Check — `deep`
  - Only import folders processed
  - Only media files moved
  - No existing src/ files modified
  - No creep beyond scope

---

## Commit Strategy

- **YES**: Group related changes
- **Message**: `feat(validate-new-pages): add media import from /import/ folders`
- **Files**: `validate-new-pages.py`, `import-media.py`, `media-placement.py`, `processed.log`, `SKILL.md`
- **Pre-commit**: Run all 5 QA scenarios

---

## Success Criteria

```bash
# Test import functionality
python3 .opencode/skills/validate-new-pages/validate-new-pages.py --import

# Check log
cat .opencode/skills/validate-new-pages/processed.log

# Verify assets
ls -la src/assets/images/
ls -la src/assets/videos/

# Verify renamed md files
ls src/*.md  # pages
ls src/_posts/*.md  # posts

# Verify media references in markdown
grep -E '!\/' src/*.md src/_posts/*.md

# Existing validation still works
python3 .opencode/skills/validate-new-pages/validate-new-pages.py --pages
python3 .opencode/skills/validate-new-pages/validate-new-pages.py --posts
```