"""Media placement module for inserting media references into markdown articles.

Provides utilities to parse markdown content, identify heading/paragraph positions,
and insert image or video references at calculated insertion points within the body.
"""

import os
from typing import List, Tuple


def parse_markdown(content: str) -> Tuple[str, str]:
    """Separate frontmatter from body.

    Frontmatter is delimited by `---` lines at the very top of the file.
    Returns a tuple of (frontmatter, body). If no frontmatter is found,
    returns ("", content).
    """
    if not content.startswith("---"):
        return "", content

    end_idx = content.find("\n---", 3)
    if end_idx == -1:
        return "", content

    frontmatter = content[: end_idx + 4]
    body = content[end_idx + 4 :].lstrip("\n")
    return frontmatter, body


def find_heading_positions(body: str) -> List[int]:
    """Find all H1 and H2 heading line indices.

    Headings are lines that start with `# ` or `## `.
    Returns a list of line numbers (0-based) where headings start.
    """
    headings = []
    for i, line in enumerate(body.splitlines()):
        stripped = line.lstrip()
        if stripped.startswith("# ") or stripped.startswith("## "):
            headings.append(i)
    return headings


def _find_paragraph_positions(body: str) -> List[int]:
    """Find the start line of each paragraph.

    A paragraph starts at a non-empty line that follows an empty line
    or is the very first line of the body.
    """
    lines = body.splitlines()
    paragraphs = []
    prev_empty = True
    for i, line in enumerate(lines):
        if line.strip():
            if prev_empty:
                paragraphs.append(i)
            prev_empty = False
        else:
            prev_empty = True
    return paragraphs


def calculate_insertion_points(body: str, media_count: int) -> List[int]:
    """Calculate line indices where media references should be inserted.

    Rules:
      * media_count == 1  -> [0] (insert at body start)
      * media_count  > 1  -> first media at 0, remaining evenly spaced
    """
    if media_count <= 0:
        return []

    lines = body.splitlines()
    total_lines = len(lines)

    if media_count == 1:
        return [0]

    insertion_points = [0]
    remaining = media_count - 1

    headings = find_heading_positions(body)

    if headings:
        for i in range(remaining):
            if i < len(headings):
                insertion_points.append(headings[i])
            else:
                insertion_points.append(total_lines)
    else:
        paragraphs = _find_paragraph_positions(body)
        if not paragraphs:
            insertion_points.extend([total_lines] * remaining)
            return insertion_points

        sections = max(remaining + 1, 3)
        group_size = max(1, len(paragraphs) // sections)

        for i in range(1, remaining + 1):
            para_idx = i * group_size
            if para_idx < len(paragraphs):
                insertion_points.append(paragraphs[para_idx])
            else:
                insertion_points.append(total_lines)

    return insertion_points


def format_media_reference(media_path: str, is_video: bool = False, thumb_path: str = None) -> str:
    """Return a markdown media reference string.

    Images: `![alt_text](media_path)`
    Videos: `[![alt_text](thumb_path)](media_path)`

    alt_text is derived from the filename without extension.
    """
    basename = os.path.basename(media_path)
    name, _ = os.path.splitext(basename)

    if is_video:
        alt_text = f"Video {name}"
        thumb = thumb_path or media_path
        return f"[![{alt_text}]({thumb})]({media_path})"
    else:
        alt_text = name
        return f"![{alt_text}]({media_path})"


def insert_media(content: str, media_list: List[Tuple[str, bool, str]]) -> str:
    """Insert formatted media references into a markdown document.

    Args:
        content: Full markdown content (including optional frontmatter).
        media_list: List of tuples (media_path, is_video, thumb_path).

    Returns:
        Updated markdown content with media references inserted.
    """
    frontmatter, body = parse_markdown(content)
    lines = body.splitlines()
    insertion_points = calculate_insertion_points(body, len(media_list))

    media_refs = [
        format_media_reference(path, is_vid, thumb)
        for path, is_vid, thumb in media_list
    ]

    for i in range(len(media_refs) - 1, -1, -1):
        line_no = insertion_points[i]
        ref = media_refs[i]
        if line_no <= len(lines):
            lines.insert(line_no, ref)
        else:
            lines.append(ref)

    new_body = "\n".join(lines)
    if frontmatter:
        return frontmatter + "\n" + new_body
    return new_body
