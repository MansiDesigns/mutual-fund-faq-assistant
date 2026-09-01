---
name: Emerald Trust
colors:
  surface: '#f7faf9'
  surface-dim: '#d7dbda'
  surface-bright: '#f7faf9'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f1f4f3'
  surface-container: '#ebeeed'
  surface-container-high: '#e6e9e8'
  surface-container-highest: '#e0e3e2'
  on-surface: '#181c1c'
  on-surface-variant: '#3c4a43'
  inverse-surface: '#2d3131'
  inverse-on-surface: '#eef1f0'
  outline: '#6b7b72'
  outline-variant: '#bacac1'
  surface-tint: '#006c4f'
  primary: '#006c4f'
  on-primary: '#ffffff'
  primary-container: '#00d09c'
  on-primary-container: '#00533c'
  inverse-primary: '#2fe0aa'
  secondary: '#565f6a'
  on-secondary: '#ffffff'
  secondary-container: '#dae3f0'
  on-secondary-container: '#5c6570'
  tertiary: '#595f69'
  on-tertiary: '#ffffff'
  tertiary-container: '#b2b8c4'
  on-tertiary-container: '#434953'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#59fdc5'
  primary-fixed-dim: '#2fe0aa'
  on-primary-fixed: '#002116'
  on-primary-fixed-variant: '#00513b'
  secondary-fixed: '#dae3f0'
  secondary-fixed-dim: '#bec7d3'
  on-secondary-fixed: '#131c25'
  on-secondary-fixed-variant: '#3f4852'
  tertiary-fixed: '#dde3ef'
  tertiary-fixed-dim: '#c1c7d3'
  on-tertiary-fixed: '#161c25'
  on-tertiary-fixed-variant: '#414751'
  background: '#f7faf9'
  on-background: '#181c1c'
  surface-variant: '#e0e3e2'
typography:
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  code:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  container-max: 800px
  gutter: 1rem
  margin-mobile: 1rem
  margin-desktop: 2rem
  stack-sm: 0.5rem
  stack-md: 1rem
  stack-lg: 1.5rem
---

## Brand & Style

The design system is engineered for a mutual fund FAQ assistant, prioritizing clarity, financial security, and approachable expertise. Drawing inspiration from modern fintech interfaces, it employs a **Corporate / Modern** style characterized by high-density information management balanced by generous whitespace.

The visual narrative focuses on "The Green Path to Growth," utilizing emerald accents against a clinical, stable background to foster user confidence. Surfaces are flat or subtly layered, avoiding heavy skeuomorphism in favor of a crisp, systematic digital-first aesthetic. The interface should feel transparent, fast, and authoritative.

## Colors

This design system utilizes a high-contrast palette to ensure financial data and chat interactions are highly legible.

- **Primary (#00D09C):** Emerald Green. Used for primary actions, success states, and key brand highlights. It symbolizes growth and vitality.
- **Secondary (#1C252E):** Dark Slate. Used for primary text, deep backgrounds in dark mode, and heavy lifting in the visual hierarchy.
- **Tertiary (#7C828D):** Cool Grey. Used for secondary text, labels, and icons that should not distract from the main content.
- **Neutral (#F4F7F6):** Off-white/Mint-tinted white. Used for the main application background to reduce eye strain compared to pure white.
- **Surface:** Pure White (#FFFFFF) is reserved for cards, chat bubbles, and input areas to create a distinct layer above the neutral background.

## Typography

The design system relies exclusively on **Inter** to convey a systematic, utilitarian, and modern professional vibe. 

- **Weight Usage:** Bold (700) is reserved for page titles. Semi-bold (600) is used for component headers and buttons. Regular (400) is used for all conversational text.
- **Hierarchy:** Maintain a strict vertical rhythm. Chat responses use `body-lg` for maximum readability, while disclaimers and secondary data use `body-sm`.
- **Contrast:** Ensure all text on `neutral` or `surface` backgrounds meets WCAG AA standards using the `secondary` color.

## Layout & Spacing

The design system uses a **Fixed Grid** approach for the chat interface to maintain focus and a **Fluid Grid** for secondary dashboard elements.

- **Assistant Container:** The main chat interface is centered with a maximum width of 800px to prevent long line lengths in chat bubbles, which harms readability.
- **The 8px Rule:** All spacing increments are multiples of 8px. 
- **Mobile Adaptation:** On mobile devices, side margins shrink to 16px. Chat bubbles take up 90% of the screen width.
- **Safe Areas:** Ensure a bottom-padding of 32px for the input area to allow for mobile home indicators and floating action buttons.

## Elevation & Depth

This design system uses **Low-contrast outlines** combined with **Tonal layers** to establish hierarchy without the visual clutter of heavy shadows.

- **Level 0 (Background):** `neutral_color_hex`. The base of the application.
- **Level 1 (Cards/Bubbles):** White surface with a 1px border of `#E5E7EB`. No shadow.
- **Level 2 (Interactive/Floating):** White surface with a very soft, diffused shadow: `0px 4px 12px rgba(0, 0, 0, 0.05)`. Used for the fixed input bar at the bottom.
- **Active State:** When a user clicks a button or interacts with an input, the border color shifts to the `primary` emerald green.

## Shapes

The shape language is **Rounded**, reflecting a modern and friendly financial tool that doesn't feel overly rigid or "bank-like."

- **Chat Bubbles:** Use `rounded-lg` (1rem). The tail of the bubble is omitted for a cleaner, "pill-card" hybrid look.
- **Action Buttons:** Use `rounded-xl` (1.5rem) to create a distinct, touch-friendly appearance.
- **Inputs:** Use `rounded-lg` (0.5rem) to maintain a structured, professional feel for data entry.

## Components

### Chat Bubbles
- **Bot Bubble:** White background, 1px grey border, dark slate text. Iconography (small emerald logo) placed to the left.
- **User Bubble:** Light emerald tint (`#E6FAF5`) or subtle neutral grey. Right-aligned. No border.

### Quick-Action Buttons
- Compact chips used for suggested questions. 
- Style: Transparent background, `primary` green border, `primary` green text. 
- Hover: Light green background tint.

### Input Field
- Fixed to the bottom of the viewport.
- Contains a search icon, the text area, and a prominent emerald 'Send' button.
- Style: Subtle shadow (Elevation Level 2) to indicate it sits above the scrolling content.

### Disclaimer Banners
- Used for financial warnings or "Not investment advice" notices.
- Style: Background `#FFF9E6` (soft amber) or `#F4F7F6`. 
- Typography: `body-sm` with a secondary grey color to appear less prominent than the main assistant response.

### Progress Indicators
- For "Thinking" states or data loading.
- Style: Three pulsing dots using the `primary` emerald color.