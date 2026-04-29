# Media Import Skill Learnings

## Path Resolution Pattern
Following the existing `validate-new-pages.py` pattern:
```python
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
```
This resolves to the git repository root, allowing consistent access to `src/`, `import/`, and other top-level directories.

## Media Organization
- Images go to `src/assets/images/`
- Videos go to `src/assets/videos/`
- Mixed-media folders are handled by moving each file type to its respective directory

## Filename Sanitization Pipeline
The sanitization follows a strict sequence:
1. Replace spaces with hyphens
2. Remove special characters (keep only alphanumeric, hyphens, dots)
3. Collapse multiple consecutive hyphens
4. Strip leading/trailing hyphens
5. Fallback to 'media' if empty
6. Lowercase extension only

## Deduplication Strategy
Use a counter suffix `-1`, `-2`, etc. inserted before the file extension. Implemented with an infinite loop that breaks when a non-existing filename is found.

## Rollback Pattern
When using `shutil.move()` in batches, track successful moves as `(new_path, original_path)` tuples. On any exception, iterate the tracked moves in reverse and attempt to move each file back to its original location. Suppress errors during rollback to avoid masking the original exception.

## Log Format
Standard format: `[YYYY-MM-DD HH:MM:SS] TYPE: folder_name → dest_path | media: file1, file2`
Where TYPE is PAGE or POST depending on the source import directory.

## Slug Generation
Sort media files alphabetically by filename (case-insensitive), take the first one, sanitize its name, strip the extension, and lowercase the result.

## Media Placement Module

- **File**: `.opencode/skills/validate-new-pages/media-placement.py`
- **Purpose**: Parses markdown content and inserts media references at calculated positions within the article body.

### Key Implementation Details

1. **Frontmatter Parsing**: Uses simple string search for `---` delimiters. Frontmatter must start at the very first character.
2. **Heading Detection**: Only H1 (`# `) and H2 (`## `) are considered for insertion boundaries. Lines are stripped of leading whitespace before checking.
3. **Insertion Strategy**:
   - 1 media item -> insert at body start (position 0)
   - 2+ media items -> first at position 0, remaining placed at heading boundaries or paragraph boundaries
   - If media count exceeds available sections, extras are appended at the end (after the last line)
4. **Paragraph Fallback**: When no headings exist, paragraphs are identified by non-empty lines following empty lines. The body is divided into sections (minimum 3) and media placed at paragraph boundaries.
5. **Media Formatting**:
   - Images: `![filename](/path/to/file.jpg)`
   - Videos: `[![Video filename](/path/to/thumb.jpeg)](/path/to/video.mp4)`

### Edge Cases Handled

- Empty body: media references appended after frontmatter
- No headings: falls back to paragraph-based spacing
- No paragraphs: all remaining media appended at end
- Media count > available sections: extras appended at end

### Testing Notes

- Verified with example content.md structure from task context
- All functions tested: parse_markdown, find_heading_positions, calculate_insertion_points, format_media_reference, insert_media
- Module uses only standard library (os, typing)
- File has a hyphen in the name (`media-placement.py`), so dynamic import via `importlib.util` is needed for testing
