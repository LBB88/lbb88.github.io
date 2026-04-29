"""Media placement module for inserting media references into markdown articles.

Provides utilities to parse markdown content, identify heading/paragraph positions,
and insert image or video references at calculated insertion points within the body.
"""

import os
import re
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
    lines = body.splitlines()
    paragraphs = []
    prev_empty = True
    for i, line in enumerate(body.splitlines()):
        if line.strip():
            if prev_empty:
                paragraphs.append(i)
            prev_empty = False
        else:
            prev_empty = True
    return paragraphs


def _is_list_item(line: str) -> bool:
    stripped = line.strip()
    return bool(re.match(r'^[-*+]\s', stripped)) or bool(re.match(r'^\d+\.\s', stripped))


def _is_emoji_prefixed(line: str) -> bool:
    stripped = line.strip()
    if not stripped or len(stripped) < 2:
        return False
    first_char = stripped[0]
    return ord(first_char) > 127


def find_safe_insertion_points(body: str) -> List[int]:
    lines = body.splitlines()
    total = len(lines)

    if total == 0:
        return []

    safe = []

    for i, line in enumerate(lines):
        stripped = line.strip()

        if not stripped:
            safe.append(i)
            continue

        if stripped.startswith('# '):
            safe.append(i)
            continue

        if i == total - 1:
            safe.append(i)
            continue

        is_list = _is_list_item(stripped)
        is_emoji = _is_emoji_prefixed(line)

        if is_list or is_emoji:
            j = i
            while j < total:
                j_line = lines[j].strip()
                j_is_list = _is_list_item(j_line)
                j_is_emoji = _is_emoji_prefixed(lines[j])
                if not j_is_list and not j_is_emoji:
                    break
                j += 1

            last_list_line = j - 1 if j < total else total - 1
            safe.append(last_list_line)
            continue

        next_line = lines[i + 1]
        next_stripped = next_line.strip()

        if not next_stripped or next_stripped.startswith('# ') or i + 1 == total - 1:
            safe.append(i)
            continue

    if 0 not in safe:
        safe.insert(0, 0)

    return sorted(set(safe))


def calculate_insertion_points(body: str, media_count: int) -> List[int]:
    if media_count <= 0:
        return []

    lines = body.splitlines()
    total_lines = len(lines)

    if media_count == 1:
        return [0]

    if total_lines == 0:
        return [0] * media_count

    safe_points = find_safe_insertion_points(body)

    if len(safe_points) < media_count:
        safe_points = list(range(total_lines))

    result = []
    last_pos = -1

    for i in range(media_count):
        target = int((i / media_count) * total_lines)

        best_pos = safe_points[-1] if safe_points else total_lines - 1

        for sp in safe_points:
            if sp > last_pos and sp > target:
                best_pos = sp
                break
            elif sp > last_pos:
                best_pos = sp

        result.append(best_pos)
        last_pos = best_pos

    return result


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
