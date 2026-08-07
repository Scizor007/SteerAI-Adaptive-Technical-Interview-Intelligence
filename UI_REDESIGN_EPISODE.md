# UI Redesign Episode — SteerAI

## Summary
The frontend was completely redesigned from a basic functional scaffold into a premium, SaaS-like assessment platform named **SteerAI**. The visual language shifted away from generic AI dashboards and chatbot clichés, drawing heavy inspiration from top-tier products like Linear, Stripe, Raycast, and Vercel.

## Design System

### Visual Language
- **Aesthetic:** Minimal, professional, lots of whitespace, strong hierarchy.
- **Micro-interactions:** Elegant hover states, smooth Framer Motion transitions, and purpose-driven animations (e.g. skeleton loaders, active state pulses).
- **Layout:** Maximum width of 1400px with a responsive grid.

### Color Tokens (Strict 8-Color Palette)
- **Primary Background:** `#09090B` (Deep rich black)
- **Secondary Background:** `#111114` (Subtle elevation)
- **Surface:** `#1A1A1F` (Cards and distinct blocks)
- **Primary Text:** `#F4F4F5` (High contrast, readable)
- **Secondary Text:** `#8B8B95` (Muted metadata)
- **Border:** `#2A2A30` (Subtle structural lines)
- **Accent:** `#5E6AD2` (Premium Indigo/Blurple)
- **Signal (Success):** `#22C55E` (Emerald green for live/success states)
*(Semantic aliases derived from these: Warning `#EAB308`, Error `#EF4444`)*

### Typography
- **Display:** `Plus Jakarta Sans` — Chosen for its geometric, modern, and highly legible appearance that immediately signals a premium tech product.
- **Body:** `Inter` — The gold standard for clean, neutral, and readable UI text.
- **Monospace:** `IBM Plex Mono` — A beautiful, technical, and slightly more editorial monospace font than generic system defaults, fitting the "assessment platform" vibe perfectly.

### Spacing & Motion
- **Spacing:** Generous padding around cards (up to 3rem), logical scale from `0.25rem` up to `4rem`.
- **Motion:** Powered by Framer Motion. Uses a specific spring config (`stiffness: 380`, `damping: 32`) for snappy, non-floaty interactions.

## Components Created
A full suite of non-duplicated UI primitives was built in `src/components/ui`:
- `Button` (Primary, Secondary, Ghost variants)
- `Input` & `Textarea` (With accessible focus states)
- `Card` & `MetricCard` (With subtle borders and optional hover elevation)
- `Progress` & `Stepper` (For interview tracking)
- `Badge` (Semantic status labeling)
- `Modal` (Animated dialogs)
- `Timeline` (For curriculum or interview flow)
- `Sidebar` & `Navbar` (Layout scaffolding)
- `Tabs` (View switching)
- `Tooltip` (Contextual helpers)
- `Avatar` (Candidate photos)
- `LoadingState`, `EmptyState`, `ErrorState`, `Skeleton` (Feedback states)

## Design Decisions
1. **Interview Workspace (Not a Chatbot):** The core interview screen was explicitly designed *not* to look like a chat interface. It features a left sidebar for candidate progress, a central stage for the current question/answer, and a right sidebar for live evaluation notes and confidence scores. This enforces the feeling of an objective assessment tool.
2. **Iconography:** Used `lucide-react` sparingly to ensure a clean, uncluttered interface.
3. **Typography as Brand:** By leveraging Plus Jakarta Sans for display and IBM Plex Mono for technical data, the typography itself carries the brand's identity without needing excessive logos or neon gradients.
