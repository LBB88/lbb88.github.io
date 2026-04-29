# Media Import Skill Decisions

## Import Directory Location
Assumed `import/` is at the repository root (sibling to `src/`), not inside `src/`. This is based on the task specification referencing `/import/pages/` and `/import/posts/` without the `src/` prefix, unlike `/src/assets/images/` which explicitly includes `src/`.

## Mixed Media Logging
For folders containing both images and videos, the log entry uses the images directory as the `dest_path` since images are the primary content type. If only videos exist, the videos directory is used.

## Entry Type in Logs
Added an `entry_type` parameter to `write_log_entry()` and `process_folder()` to distinguish PAGE vs POST imports in the log output, even though the original task specification only showed a generic `TYPE` placeholder.

## No Full Atomicity for Mixed Media
Each `move_media_files()` call handles its own rollback. If a folder has both images and videos, and the video move fails, the already-moved images are not rolled back. This was chosen for simplicity; full folder-level atomicity would require a more complex two-phase commit pattern.

## CLI Design
Used `argparse` with a single `--dry-run` flag, matching the style of `fix-frontmatter.py` in the same skill directory.

## Insertion Point Calculation
When headings exist, remaining media are placed at heading boundaries in order. This keeps media near section starts rather than mid-paragraph.

## Paragraph Detection
A paragraph start is defined as a non-empty line that follows an empty line (or the first line). This avoids counting continuation lines as separate paragraphs.

## Reverse Insertion
Media references are inserted from last to first so that line indices remain valid during insertion.
