# News For General Awareness

Weekly collection of current affairs and news insights from major newspapers, built with [Hugo](https://gohugo.io/) and the [PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme.

## Setup

```bash
# Clone with submodules
git clone --recurse-submodules <repo-url>

# Or initialize submodules after cloning
git submodule update --init --recursive
```

## Development

```bash
# Start dev server (includes drafts)
hugo server -D

# Start server in production mode (excludes drafts)
hugo server -e production

# Build for production
hugo
```

The site will be available at `http://localhost:1313/`. Hugo watches for changes and auto-reloads.

## Project Structure

```
.
├── archetypes/          # Templates for new content
├── content/
│   └── posts/           # Weekly news collections go here
├── layouts/             # Custom template overrides
├── static/              # Static assets (images, files)
├── themes/hugo-PaperMod # Theme (git submodule)
└── hugo.toml            # Site configuration
```

## Adding News Posts

### Create a new weekly post

Week titles and filenames are generated using a Python script:

```bash
# Generate week info for a specific date
python3 scripts/week_title.py 2026-02-14
# Output: Title: February 2026, Week 2
#         Filename: 2026-02-week-2.md

# Create new post
hugo new posts/2026-02-week-2.md
```

### Manually create a post

Create a markdown file in `content/posts/`:

```markdown
+++
title = 'January 2024, Week 3'
date = 2024-01-15T10:00:00+05:30
draft = false
tags = ['politics', 'economy', 'international']
summary = 'Key news highlights from major newspapers'
+++

## Politics

### Article Title
**Source:** The Hindu / Indian Express / etc.
**Date:** January 12, 2024

Key points:
- Main point 1
- Main point 2
- Main point 3

## Economy

[Similar format...]
```

### Frontmatter options

| Field       | Description                                      |
|-------------|--------------------------------------------------|
| `title`     | Post title (e.g., "Week of January 15, 2024")   |
| `date`      | Publication date                                 |
| `draft`     | Set to `true` to hide from production builds     |
| `tags`      | List of tags for categorization                  |
| `summary`   | Short description shown in post listings         |
| `ShowToc`   | Set to `false` to hide table of contents         |

## Workflow with Claude Code

This project is optimized for use with Claude Code, which automatically processes news articles and adds them to weekly posts.

### Simple Workflow

1. **Provide Article to Claude:**
   ```
   Process this article:
   [attach screenshot/image of news article]
   ```

2. **Claude automatically:**
   - Extracts and summarizes the article (main facts + perspective/context)
   - Determines the current week using `scripts/week_title.py`
   - Finds existing weekly post or creates new one (format: `2026-02-week-2.md`)
   - Adds article to the TOP of the post
   - Updates relevant tags
   - Saves changes

3. **Review and Publish:**
   - Preview with `hugo server -D`
   - When ready, set `draft = false` in the post frontmatter
   - Push to GitHub to deploy

### Example Interaction

```
You: "Process this article"
     [Image: Screenshot of article about renewable energy]

Claude: [Processes and adds to current week's post: content/posts/2026-02-week-2.md]
```

### Manual Workflow (Alternative)

If you prefer to compile manually:
1. Save article screenshots during the week
2. Provide batch to Claude: "Process these 5 articles"
3. Claude adds all to appropriate weekly post
4. Review and publish

## Useful Commands

```bash
# Create new weekly post
hugo new posts/week-2024-01-15.md

# Start server with drafts visible
hugo server -D

# Build site (output to public/)
hugo

# Build with minification
hugo --minify
```

## Deployment

The site automatically deploys to GitHub Pages when you push to `main`.

### Setup (one-time)

1. Go to your GitHub repo **Settings** → **Pages**
2. Under **Build and deployment**, set Source to **GitHub Actions**

### Manual deployment

Push to `main` branch or manually trigger the workflow from the **Actions** tab.

## Resources

- [Hugo Documentation](https://gohugo.io/documentation/)
- [PaperMod Wiki](https://github.com/adityatelange/hugo-PaperMod/wiki)
