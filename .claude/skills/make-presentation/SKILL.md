---
name: make-presentation
description: Create a Slidev presentation from a topic outline. Generates slides.md, speaker notes, package.json, styles, and README — ready to npm install && npm run dev.
argument-hint: <topic or path to outline file>
---

# make-presentation

You are a presentation builder. Given a topic, outline, or reference file, you create a complete Slidev presentation that is ready to run immediately.

## Workflow

### 1. Gather context

- If the user provides a file path, read it for the outline/requirements.
- If the user provides a topic description, use that directly.
- Ask clarifying questions ONLY if the topic is too vague to produce useful slides (e.g. "quarterly update" with no specifics). If you have enough to work with, proceed.

### 2. Research (if applicable)

- If the outline references code, configs, dashboards, or documentation in the workspace — read those files to extract real examples.
- Prefer real code snippets over pseudocode. Real data over placeholder data.
- If the user mentions specific repos/paths, go read them.

### 3. Create the presentation directory

Create the following structure:

```
<presentation-dir>/
├── package.json          # Slidev project with dependencies
├── slides.md             # The actual presentation
├── styles/
│   └── index.css         # Custom styles (hide Slidev chrome by default)
├── SCRIPT.md             # Speaker notes — detailed script per slide
└── README.md             # Setup, dev, present, export instructions
```

### 4. slides.md conventions

Use this Slidev structure:

```markdown
---
theme: seriph
background: https://cover.sli.dev
title: <Presentation Title>
class: text-center
---

# Title

subtitle

---
layout: default
---

# Slide Title

content with v-clicks for progressive reveal

<!--
Speaker notes in HTML comments (brief — full notes go in SCRIPT.md)
-->
```

**Style rules:**
- Use `<v-clicks>` for progressive bullet reveals
- Use mermaid diagrams (with `{scale: 0.7}` for fit) for flows and architecture
- Use `<div class="text-xs">` wrapper for code blocks to prevent overflow
- Use tables for comparisons
- Keep slides concise — no walls of text
- Real code > pseudocode. Real data > placeholder data.
- One concept per slide. Split if it's getting dense.
- Slide count target: 12–20 slides for a 20-30 min presentation. Adjust proportionally.

### 5. SCRIPT.md conventions

```markdown
# Presentation Title — Speaker Script

## 1 — Slide Title (~Xmin)

> Detailed talking points in blockquotes.
>
> **Bold** key phrases you want to emphasize when speaking.
>
> Include context that doesn't belong on the slide itself — background, why decisions were made, anticipated questions.

---

## 2 — Next Slide (~Xmin)
...
```

### 6. package.json

```json
{
  "name": "<kebab-case-title>",
  "type": "module",
  "private": true,
  "scripts": {
    "dev": "slidev --open",
    "build": "slidev build",
    "export": "slidev export"
  },
  "dependencies": {
    "@slidev/cli": "^0.49.0",
    "@slidev/theme-default": "latest",
    "@slidev/theme-seriph": "latest"
  }
}
```

### 7. styles/index.css

```css
/* Hide Slidev's chrome in audience/default view.
   Keyboard shortcuts still work; presenter mode at /presenter still has its UI. */

#slidev-goto-dialog {
  display: none !important;
}
```

### 8. README.md

Include: setup (`npm install`), dev (`npm run dev`), presenting in Google Meet (tab sharing), presenter mode URL, export commands, and useful keyboard shortcuts.

### 9. Install and launch

After creating all files:
1. Run `npm install` in the presentation directory
2. Run `npm run dev` (non-blocking)
3. Provide the browser preview URL

## Quality checklist

- [ ] Every slide has corresponding speaker notes in SCRIPT.md
- [ ] Code examples are real (from the workspace), not fabricated
- [ ] Mermaid diagrams render correctly (proper syntax, scale set)
- [ ] No slide has more than ~6 bullet points
- [ ] Presentation has a clear narrative arc: context → detail → next steps
- [ ] Total estimated speaking time noted in SCRIPT.md header
