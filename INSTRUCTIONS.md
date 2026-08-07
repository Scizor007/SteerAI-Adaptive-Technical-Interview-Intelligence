# INSTRUCTIONS.md — Permanent AI & Development Rules

> These rules apply to ALL contributors (human and AI) at ALL times.
> Never remove or override without explicit team agreement.

---

## Code Integrity

1. **Never remove working features** without explicit instruction.
2. **Never refactor unrelated code** when implementing a feature.
3. **Preserve API compatibility** unless explicitly requested to break it.
4. **Keep commits focused** — one logical change per commit.

## Architecture

5. **Keep architecture modular** — each module has a single responsibility.
6. **Keep components reusable** — no page-specific logic in shared components.
7. **Never duplicate business logic** — extract to shared modules/utilities.
8. **Prefer composition over inheritance** — compose small modules, don't build monoliths.
9. **Keep functions focused and small** — a function should do one thing well.
10. **Separate concerns strictly**:
    - UI components must NOT contain API calls
    - Business logic must NOT contain rendering
    - API layer must NOT contain UI state

## Security

11. **Never expose API keys** in source code, commits, or documentation.
12. **Never hardcode secrets** — use environment variables via config.
13. **Never commit `.env` files** — only `.env.example` with placeholder values.

## Naming & Code Style

14. **Use descriptive naming** — variables, functions, files should be self-documenting.
15. **Use strict TypeScript** — no `any` types unless absolutely necessary.
16. **Never hardcode values** that belong in configuration, constants, or mock data.
17. **Keep code self-documenting** — prefer clear names over excessive comments.

## Design & UI

18. **Never default to the generic AI-app look** — stay within the design token system defined in CONTEXT.md.
19. **Design tokens are the source of truth** — all colors, typography, and spacing must reference tokens.
20. **Only change design tokens with explicit approval** — they are project-wide decisions.

## Documentation

21. **Update documentation after every meaningful change** — CONTEXT.md, TASKS.md, HANDOFF.md at minimum.
22. **PROMPTS.md is append-only** — never delete prompt history.
23. **DECISIONS.md is append-only** — never delete or modify past decisions.
24. **Never recreate documentation files from scratch** if they already exist.

## Dependencies

25. **Avoid unnecessary third-party dependencies** — justify every new package.
26. **Pin dependency versions** — no floating versions in production.

## Multi-AI Collaboration

27. **Keep the codebase navigable** — another AI should understand the project from the repo alone.
28. **Document architectural decisions** — the "why" matters as much as the "what."
29. **Maintain consistent file organization** — follow the established folder structure.

## Hackathon Rules

30. **Favor simple, maintainable solutions** — avoid overengineering.
31. **Implement MVP first, then polish** — never delay P1 for P5.
32. **Never generate the whole project in one pass** — work incrementally.
33. **Preserve previous work** unless explicitly instructed to remove it.
