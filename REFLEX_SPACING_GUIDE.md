# Reflex Spacing System Guide

## Understanding Reflex Spacing Constraints

### The Problem
Reflex's `spacing`, `padding`, and `margin` props only accept values '0' through '9', which map to Radix UI's spacing scale:

| Value | Pixels | Use Case |
|-------|--------|----------|
| '0' | 0px | No spacing |
| '1' | 4px | Minimal spacing |
| '2' | 8px | Tight spacing |
| '3' | 12px | Small spacing |
| '4' | 16px | Default spacing |
| '5' | 24px | Medium spacing |
| '6' | 32px | Large spacing |
| '7' | 40px | Extra large spacing |
| '8' | 48px | XXL spacing |
| **'9'** | **64px** | **Maximum** |

### The Limitation
**Maximum spacing is only 64px** - insufficient for proper visual hierarchy between major sections!

---

## The Solution: CSS Style Dicts

For spacing larger than 64px, use CSS `style` dictionaries with explicit pixel values:

### ❌ WRONG - Trying to use values > '9'
```python
rx.vstack(
    component1(),
    component2(),
    spacing="10",  # ❌ TypeError! Only '0'-'9' allowed
)

rx.box(
    content,
    padding="15",  # ❌ TypeError! Only '0'-'9' allowed
)
```

### ✅ CORRECT - Using CSS Style Dict
```python
# For large spacing between sections
rx.vstack(
    component1(),
    component2(),
    spacing="0",  # Disable Reflex spacing
    # Use explicit margins instead:
    style={"gap": "96px"}  # ✅ Any pixel value!
)

# For generous padding inside sections
rx.box(
    content,
    style={
        "padding": "48px",  # ✅ Works perfectly!
        "margin-top": "64px",
        "margin-bottom": "32px",
    }
)
```

---

## Real-World Example: Section Spacing

### Before (Cramped)
```python
rx.vstack(
    summary_cards(),
    analytics_section(),
    claims_table(),
    spacing="9",  # Only 64px - not enough!
)
```

### After (Proper Spacing)
```python
rx.vstack(
    # Section 1
    summary_cards(),

    # Section 2
    rx.box(
        analytics_section(),
        style={
            "margin-top": "48px",  # 48px gap from previous
            "padding": "48px",      # 48px internal padding
        }
    ),

    # Section 3
    rx.box(
        claims_table(),
        style={
            "margin-top": "48px",  # 48px gap from previous
            "padding": "48px",      # 48px internal padding
        }
    ),

    spacing="0",  # Don't use Reflex spacing
)
```

---

## Best Practices for Dark Mode Dashboard

### Page-Level Padding
```python
rx.box(
    content,
    style={
        "padding": "48px 64px",  # Vertical: 48px, Horizontal: 64px
    },
    max_width="1600px",
    margin_x="auto",
)
```

### Section Containers
```python
rx.box(
    section_header(),
    section_content(),
    style={
        "padding": "48px",           # Internal padding
        "margin-top": "48px",        # Gap from previous section
        "border-radius": "20px",
        "background": DARK_COLORS["bg_card"],
    }
)
```

### Section Headers
```python
def section_header(title, subtitle):
    return rx.vstack(
        rx.heading(title),
        rx.text(subtitle),
        style={
            "margin-bottom": "32px",  # Space below header
        }
    )
```

### Navbar & Sticky Elements
```python
# Navbar
rx.box(
    navbar_content(),
    class_name="sticky top-0 z-50",
)

# Action bar (below navbar)
rx.box(
    action_bar_content(),
    class_name="sticky top-[64px] z-40",
    style={
        "margin-bottom": "32px",  # Space before main content
    }
)
```

---

## Spacing Recommendations by Context

### Tight Spacing (Components within a group)
```python
rx.vstack(
    label(),
    input(),
    spacing="2",  # 8px - tight spacing within form field
)
```

### Medium Spacing (Related sections)
```python
rx.vstack(
    header(),
    content(),
    spacing="5",  # 24px - medium spacing
)
```

### Large Spacing (Major sections)
```python
rx.box(
    section_content(),
    style={"margin-top": "48px"}  # Explicit large gap
)
```

### Extra Large Spacing (Page-level divisions)
```python
rx.box(
    major_section(),
    style={"margin-top": "96px"}  # Extra large gap
)
```

---

## Common Spacing Values

### Standard Scale
- **4px** - Minimal (icon-to-text)
- **8px** - Tight (form labels)
- **12px** - Small (button groups)
- **16px** - Default (card content)
- **24px** - Medium (section spacing)
- **32px** - Large (headers)
- **48px** - XL (section padding)
- **64px** - XXL (page padding)
- **96px** - 3XL (major dividers)

---

## Quick Decision Tree

**Need spacing/padding/margin?**

→ Is it **< 64px**?
  - YES: Use Reflex props (`spacing="6"`)
  - NO: Use CSS style dict (`style={"padding": "96px"}`)

→ Is it a **major section break**?
  - Use 48-96px with style dict

→ Is it **internal component spacing**?
  - Use Reflex props ('2'-'5')

→ Is it a **section header**?
  - Use 32px margin-bottom

---

## Summary

| Context | Method | Example |
|---------|--------|---------|
| Small spacing (< 64px) | Reflex props | `spacing="5"` |
| Large spacing (≥ 64px) | CSS style dict | `style={"gap": "96px"}` |
| Section padding | CSS style dict | `style={"padding": "48px"}` |
| Section margins | CSS style dict | `style={"margin-top": "48px"}` |
| Page padding | CSS style dict | `style={"padding": "48px 64px"}` |

---

## Updated in `REFLEX_BEST_PRACTICES.md`

This spacing system documentation has been added to the best practices guide for reference.

**Remember**: When in doubt, use explicit pixel values in CSS style dicts for precise control! 🎯
