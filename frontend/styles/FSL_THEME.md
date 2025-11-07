# 🎨 Full-Spectrum Labs Theme Tokens  
*Runeterra Lore – Phase 3.4 Release*

---

## Color System

| Token            | Description                    | Value        |
|------------------|--------------------------------|--------------|
| `$fsl-bg`        | Background (main surface)      | `#0a0a0f`    |
| `$fsl-panel`     | Secondary panels / cards       | `#141421`    |
| `$fsl-accent`    | Primary accent (Hextech blue)  | `#1e90ff`    |
| `$fsl-accent-glow`| Soft glow for hover, outlines | `rgba(30, 144, 255, 0.6)` |
| `$fsl-text-primary`| Default readable text        | `#e6e6fa`    |
| `$fsl-text-secondary`| Muted text / descriptions   | `#b8b8d0`    |
| `$fsl-border`    | Subtle border tint             | `#2b2b3d`    |
| `$fsl-error`     | Error / warning accents        | `#ff4c4c`    |

---

## Typography

| Token           | Purpose                        | Value                                         |
|-----------------|--------------------------------|-----------------------------------------------|
| `$fsl-font-sans`| Main UI / headings             | `"Inter", "Segoe UI", sans-serif`             |
| `$fsl-font-mono`| Code / numbers                 | `"Fira Code", monospace`                      |
| `$fsl-font-size-base` | Body text                  | `16px`                                        |
| `$fsl-font-size-sm` | Secondary text              | `14px`                                        |
| `$fsl-font-size-lg` | Headers                     | `20px`                                        |

---

## Spacing Scale

| Token         | Value    |
|---------------|----------|
| `$space-xs`   | `4px`    |
| `$space-sm`   | `8px`    |
| `$space-md`   | `16px`   |
| `$space-lg`   | `24px`   |
| `$space-xl`   | `40px`   |

---

## Mixins (From _mixins.scss_)

- `@include card;` → applies panel background, rounded corners, and shadow  
- `@include flex-center;` → centers content both ways  
- `@include hover-glow($color: $fsl-accent-glow);` → adds the signature FSL shimmer  

---

## Usage Notes
- Keep all new color values derived from `$fsl-accent` for consistency.  
- Always import via `index.scss` — never import partials directly.  
- Use `hover-glow` mixin for interactive elements only (links, cards, buttons).  
- Token updates cascade globally through Sass; rebuild Next.js after edits.

---

**Revision:** Phase 3.4 | Author: Full-Spectrum Labs Core Theme Maintainer
