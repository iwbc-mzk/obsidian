---
created: 2026-02-28 Sat 10:45
updated: 2026-02-28 Sat 11:58
---
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is an Obsidian knowledge vault that doubles as a published documentation site. The vault content is transformed into a MkDocs site (Material theme) deployed to GitHub Pages at `obsidian.bibliophage.jp`.

## MkDocs Build Commands

```bash
# Install dependencies
poetry install

# Prepare docs (copy & transform Obsidian content → MkDocs format)
python .mkdocs/scripts/prepare_docs.py

# Serve locally (prepare + serve)
python .mkdocs/scripts/prepare_docs.py --local && mkdocs serve --open

# Build static site
mkdocs build -v

# Deploy to GitHub Pages (CI does this automatically on push to main)
mkdocs gh-deploy
```

## Architecture

### Publishing Pipeline

1. **Source**: Obsidian markdown files in `02_Daily/`, `03_MOC/`, `04_Article/`, `06_ReadingNotes/`
2. **Transform**: `.mkdocs/scripts/prepare_docs.py` converts Obsidian syntax to standard Markdown:
   - Converts `![[image]]` wiki-link embeds → standard `![](path)` format
   - Strips Obsidian image size specs (e.g., `|400`)
   - Copies assets from `01_Assets/` to MkDocs docs directory
3. **Build**: MkDocs with roamlinks plugin processes wikilinks for cross-referencing
4. **Deploy**: GitHub Actions (`deploy.yml`) runs the pipeline on push to `main` and deploys to `gh-pages` branch

### Vault Folder Structure

| Folder | Purpose |
|--------|---------|
| `00_Index/` | Landing page and navigation hub |
| `01_Assets/` | All images and attachments (configured as attachment folder) |
| `02_Daily/` | Daily notes and weekly summaries |
| `03_MOC/` | Maps of Content (topic hubs) |
| `04_Article/` | Main knowledge base articles (default new file location) |
| `05_Templates/` | Note templates |
| `06_ReadingNotes/` | Structured book reading notes |
| `Clippings/` | Web clippings (not published) |
| `.mkdocs/` | MkDocs build configuration, scripts, and generated docs |

### Key Configuration Files

- `mkdocs.yml` — Site config: Material theme, MathJax/KaTeX, Mermaid, Google Analytics
- `.mkdocs/conf.yml` — Controls which folders are included in the published site
- `.mkdocs/scripts/prepare_docs.py` — Content transformation script
- `pyproject.toml` — Python dependencies (poetry): mkdocs-material, mkdocs-roamlinks-plugin, mkdocs-callouts, pyyaml
- `.gitignore` — Excludes `.mkdocs/site/`, `.mkdocs/docs/` (generated), `.venv/`, workspace state

### Git Workflow

Commits are vault backups with the format `vault backup: YYYY-MM-DD HH:MM:SS`. The `obsidian-git` plugin handles automated commits from within Obsidian.

## Content Notes

- Articles are bilingual (Japanese and English)
- Content focuses on: competitive programming algorithms, Python, security, software design patterns, reading notes
- Math rendering uses both MathJax and KaTeX (both are configured)
- Mermaid diagrams are supported in published articles

### 改行コード
編集時は必ずCRLF形式の改行を利用する
