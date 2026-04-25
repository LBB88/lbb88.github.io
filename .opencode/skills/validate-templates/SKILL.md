# Validate Jekyll Templates

Validates that markdown files (posts and pages) contain the required sections for proper Jekyll rendering and category linking.

## Checks Performed

### For All Markdown Files
- [ ] Frontmatter block exists (between `---` markers)
- [ ] `layout` field is present
- [ ] `title` field is present
- [ ] `categories` field is present

### For Posts (`_posts/` directory)
- [ ] `date` field is present
- [ ] Liquid code block for related posts exists (`where_exp` with `post.categories contains`)
- [ ] Limit is set to 2 recent posts
- [ ] Dynamic topic page link exists (`where_exp` with `p.categories contains`)
- [ ] Content exists before the Liquid code block

### For Pages (root `src/` directory)
- [ ] `permalink` field is present
- [ ] Liquid code block for post listing exists (`where: "categories", page.categories`)
- [ ] Content exists before the Liquid code block

## Usage

Run this validation after creating or modifying posts/pages:

```bash
# Validate all posts
validate-templates src/_posts/

# Validate all pages
validate-templates src/ --pages

# Validate specific file
validate-templates src/_posts/2026-04-25-my-post.md
```

## Exit Codes

- `0` - All validations passed
- `1` - One or more validations failed

## Example Output

```
✓ src/_posts/2026-04-25-my-post.md
  ✓ Frontmatter present
  ✓ Required fields: layout, title, date, categories
  ✓ Related posts block found
  ✓ Limit set to 2
  ✓ Dynamic topic link found
  ✓ Content before Liquid block

✗ src/topic1.md
  ✗ Missing permalink in frontmatter
```
