# {Presentation Title}

## Metadata

- **Audience:** {who is this for}
- **Duration:** {estimated total time}
- **Date:** {presentation date}

## Slide Structure

### 1. Title ({title})
- Subtitle / context line

### 2. Agenda
- Topic 1
- Topic 2
- Topic 3
- Topic 4

### 3–N. Content Slides

Each content slide should have:
- **One main concept** — if you need more than 6 bullets, split into two slides
- **Visual aid** — mermaid diagram, code block, or table where possible
- **Progressive reveal** — use v-clicks so audience follows your pace

### N+1. Questions / Discussion
- Open floor

## Slide Types Reference

### Code slide
```markdown
# Slide Title

<div class="text-xs">

\`\`\`language
// real code from the workspace
\`\`\`

</div>

<v-clicks>

### Key takeaway

- Point about the code

</v-clicks>
```

### Diagram slide
```markdown
# Slide Title

<div class="text-xs flex justify-center">

\`\`\`mermaid {scale: 0.65}
graph LR
    A[Thing] --> B[Other Thing]
\`\`\`

</div>
```

### Comparison slide
```markdown
# Slide Title

| Aspect | Option A | Option B |
|---|---|---|
| row 1 | val | val |
| row 2 | val | val |
```

### Progressive bullets slide
```markdown
# Slide Title

<v-clicks>

- **Bold lead** — explanation
- **Bold lead** — explanation
- **Bold lead** — explanation

</v-clicks>
```

## Speaker Notes Pattern

For each slide, write notes in this format in SCRIPT.md:

```markdown
## {N} — {Slide Title} (~{X}min)

> What you'd actually say out loud.
>
> **Emphasize** key phrases.
>
> Include context that doesn't belong on the slide — background, anticipated questions, decisions made.
```
