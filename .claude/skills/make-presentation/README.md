# /make-presentation

Create a complete [Slidev](https://sli.dev) presentation from a topic outline or description. Produces a ready-to-run project with slides, speaker script, and all scaffolding.

## What it does

1. Reads your outline (file or inline description)
2. Researches referenced code/configs/docs in your workspace
3. Generates a full Slidev project:
   - `slides.md` — the presentation with mermaid diagrams, code blocks, v-clicks
   - `SCRIPT.md` — detailed speaker notes per slide
   - `package.json`, `styles/index.css`, `README.md` — project scaffolding
4. Runs `npm install` and starts the dev server

## Example invocations

```
/make-presentation "quarterly infra update — cover k8s migration status, WAF rollout, and observability roadmap"

/make-presentation ~/notes/meeting-outline.txt

/make-presentation "onboarding talk for new engineers — how our platform works, 15 minutes"
```

## Example outline file

```
- Platform overview (5 min)
    - Architecture diagram: EKS, ALB, WAF, RDS
    - Key services and their owners
- Deployment pipeline (5 min)
    - GitHub Actions → Helm → ArgoCD
    - Code example from .github/workflows/deploy.yml
- Observability (5 min)
    - Grafana dashboards, what to look at
    - How to add metrics to your service
- Questions
```

## Output

A directory you can immediately `cd` into and run:

```bash
npm run dev     # http://localhost:3030
```

Present directly in a browser tab, share via Google Meet tab sharing. Presenter notes at `/presenter`.

## Design principles

- **Real code over pseudocode** — if your outline references files in the workspace, the skill reads them and includes actual snippets
- **One concept per slide** — dense slides get split automatically
- **Progressive reveals** — bullet points use `<v-clicks>` so you control pacing
- **Speaker notes are a full script** — not just reminders, but what you'd actually say
- **Immediately runnable** — no manual setup needed after generation

## Customization

After generation, edit `slides.md` directly — Slidev hot-reloads. Common tweaks:

- Change theme: edit the `theme:` frontmatter (try `apple-basic`, `bricks`, `dracula`)
- Add images: drop them in a `public/` folder, reference as `/image.png`
- Adjust timing: reorder slides, split or merge as needed
- Add transitions: `transition: slide-left` in slide frontmatter

## Dependencies

- Node.js (for Slidev)
- npm
