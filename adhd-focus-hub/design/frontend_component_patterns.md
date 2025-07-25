# Frontend Component Patterns for Organization and Learning Features

This document outlines recommended React component patterns for the new organization and learning sections of the ADHD Focus Hub. These guidelines ensure consistent structure, accessibility, and performance across the application.

## 1. Page Layout
- **Page components** (`pages/Organization.tsx` and `pages/Learning.tsx`) should assemble smaller, reusable components.
- Use a common `page` wrapper class for spacing and responsive layout.
- Keep each page focused on orchestrating child components and handling local state.

## 2. Reusable Building Blocks
- **FormSection** – wrapper for labeled inputs or textareas.
- **TipCard** – displays quick tips with icon, title, and description.
- **ResponsePanel** – shows AI responses and suggestions.
- Extract these pieces from existing pages so they can be reused in future features.

## 3. Service Integration
- Centralize API calls in the `services/` directory.
- For organization and learning endpoints:
  - `OrganizationService.getOrganizationPlan(payload)` → `POST /api/v1/organize`
  - `LearningService.getLearningPlan(payload)` → `POST /api/v1/learn`
- Keep response types in `services/types.ts` and align them with the backend Pydantic models. Coordinate with the BackendArchitect to finalize field names and error shapes.

## 4. Accessibility Guidelines
- Use semantic HTML elements (`<label>`, `<section>`, `<button>`).
- Ensure form controls have associated labels and `aria` attributes where needed.
- Provide clear focus states and maintain color contrast ratios that meet WCAG AA.
- Support keyboard navigation for all interactive components.

## 5. Performance Considerations
- Avoid unnecessary re-renders by splitting complex pages into smaller memoized components.
- Lazy-load heavy components when entering the page (`React.lazy`).
- Limit state updates and prefer local state within forms instead of global context where possible.

## 6. Future Enhancements
- Extract a generic `AIInteraction` component for any feature that sends a request and displays a structured response.
- Plan for caching of recent responses when Redis integration is complete so conversation history can be reused.

---
These patterns will help keep the frontend codebase maintainable as we add more ADHD-focused tools. Work closely with the BackendArchitect to verify API paths and data contracts before final implementation.
