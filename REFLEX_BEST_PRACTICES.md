# Reflex Framework Best Practices

**CRITICAL: Read this before writing any Reflex code!**

This document outlines Reflex-specific patterns that differ from standard Python and cause compilation errors if not followed.

---

## 1. Reflex Vars - The #1 Source of Errors

### ❌ WRONG - Cannot Use Python Operators
```python
# This will FAIL with TypeError
def risk_badge(risk_score):
    return rx.cond(
        risk_score >= 0.7,  # ❌ TypeError: '>=' not supported
        rx.badge("High"),
        rx.badge("Low"),
    )
```

### ✅ CORRECT - Convert Var to Float First
```python
def risk_badge(risk_score):
    # Convert Reflex Var to float before comparisons
    score = risk_score.to(float) if hasattr(risk_score, 'to') else risk_score

    return rx.cond(
        score >= 0.7,  # ✅ Works with converted float
        rx.badge("High"),
        rx.badge("Low"),
    )
```

### ❌ WRONG - Cannot Use Python if/else
```python
# This will FAIL with VarTypeError
direction = "asc" if sort_direction == "asc" else "desc"  # ❌ Cannot convert Var to bool
```

### ✅ CORRECT - Use rx.cond() Instead
```python
# Use Reflex's conditional rendering
rx.cond(
    sort_direction == "asc",
    rx.icon("chevron-up"),
    rx.icon("chevron-down"),
)
```

### ❌ WRONG - Using .get() on Reflex Var Dict
```python
# This returns CustomVarOperation which breaks comparisons
risk_score = claim.get("risk_score", 0)  # ❌ CustomVarOperation type
if risk_score >= 0.7:  # ❌ TypeError
    ...
```

### ✅ CORRECT - Use Direct Bracket Access
```python
# Use bracket notation for dictionary access
risk_score = claim["risk_score"]  # ✅ Returns proper Var type
if risk_score >= 0.7:  # ✅ Works (after .to(float) conversion)
    ...
```

### Pattern Summary
```python
# ALWAYS follow this pattern for Reflex Vars:
def component_with_comparison(reflex_var):
    # 1. Convert to Python type if needed for comparisons
    value = reflex_var.to(float) if hasattr(reflex_var, 'to') else reflex_var

    # 2. Use rx.cond() instead of if/else
    # 3. Use rx.match() for pattern matching
    # 4. NEVER use Python's if, and, or, not with Reflex Vars
    return rx.cond(
        value >= threshold,
        component_a(),
        component_b(),
    )
```

---

## 2. Icon Names - Must Use Lucide Icon Format

### ❌ WRONG - Invalid Icon Names
```python
rx.icon("x-circle")       # ❌ Invalid - kebab-case not supported
rx.icon("help-circle")    # ❌ Invalid
rx.icon("alert-triangle") # ❌ Invalid
```

### ✅ CORRECT - Use Simple Names or Underscore Format
```python
rx.icon("x")              # ✅ Simple name
rx.icon("circle_help")    # ✅ Underscore format
rx.icon("triangle_alert") # ✅ Underscore format
```

### How to Find Valid Icon Names
1. Check Reflex docs: https://reflex.dev/docs/library/data-display/icon/#icons-list
2. Common patterns:
   - Simple: `x`, `check`, `search`, `eye`, `edit`, `trash`
   - Compound: `circle_help`, `triangle_alert`, `chevron_up`, `chevron_down`
3. When in doubt, use simple single-word icons

---

## 3. Event Handlers - Lambda Closures

### ❌ WRONG - Lambda Without Default Argument
```python
# This will capture the LAST value only
rx.foreach(
    items,
    lambda item: rx.button(
        "Click",
        on_click=lambda: process(item["id"])  # ❌ Late binding issue
    )
)
```

### ✅ CORRECT - Lambda With Default Argument
```python
# Capture value immediately with default argument
rx.foreach(
    items,
    lambda item: rx.button(
        "Click",
        on_click=lambda item_id=item["id"]: process(str(item_id))  # ✅ Early binding
    )
)
```

---

## 4. State Methods - Always Verify They Exist

### ❌ WRONG - Assuming Method Names
```python
# Assuming a method exists without checking
on_click=ClaimsState.select_claim(claim_id)  # ❌ Method might not exist
```

### ✅ CORRECT - Grep First, Then Use
```bash
# Always search for the actual method name first
grep "def.*claim" claimsiq/state.py
```

```python
# Use the actual method name from the codebase
on_click=ClaimsState.open_claim_modal(str(claim_id))  # ✅ Verified method
```

---

## 5. Component Props - Type Safety

### ❌ WRONG - Passing Wrong Types
```python
rx.input(
    value=123,  # ❌ Should be string
    on_change=ClaimsState.set_value  # ❌ Wrong handler signature
)
```

### ✅ CORRECT - Match Expected Types
```python
rx.input(
    value=str(value),  # ✅ Convert to string
    on_change=ClaimsState.set_value  # ✅ Correct signature
)
```

---

## 6. Styling - Use Reflex's Style Props

### ❌ WRONG - CSS Class Names Not in Config
```python
class_name="bg-blue-500"  # ❌ Tailwind class might not be configured
```

### ✅ CORRECT - Use Reflex Style Dict
```python
style={
    "background": COLORS["primary"],  # ✅ Use theme colors
    "padding": "16px",
    "border-radius": "8px",
}
```

---

## 7. Spacing and Layout Constraints

### ❌ WRONG - Invalid Spacing Values
```python
rx.vstack(
    component1(),
    component2(),
    spacing="10",  # ❌ Invalid! Only '0'-'9' allowed
)

rx.box(
    content,
    padding="15",  # ❌ Invalid! Only '0'-'9' allowed
)
```

### ✅ CORRECT - Valid Spacing Values
```python
rx.vstack(
    component1(),
    component2(),
    spacing="9",  # ✅ Maximum allowed value
)

rx.box(
    content,
    padding="9",  # ✅ Maximum allowed value
)
```

### Valid Values
- **spacing**: Only accepts `'0'`, `'1'`, `'2'`, `'3'`, `'4'`, `'5'`, `'6'`, `'7'`, `'8'`, `'9'`
- **padding**: Only accepts `'0'`, `'1'`, `'2'`, `'3'`, `'4'`, `'5'`, `'6'`, `'7'`, `'8'`, `'9'`
- **margin**: Only accepts `'0'`, `'1'`, `'2'`, `'3'`, `'4'`, `'5'`, `'6'`, `'7'`, `'8'`, `'9'`

**Note**: If you need larger spacing, use CSS style dict with pixel/rem values:
```python
rx.box(
    content,
    style={"padding": "48px", "margin": "64px"}  # ✅ Works with any value
)
```

---

## 8. Common Error Messages and Fixes

### Error: "Cannot convert Var to bool"
**Fix**: Use `rx.cond()` instead of `if/else`

### Error: "'>=' not supported between Var and float"
**Fix**: Convert Var using `.to(float)` before comparison

### Error: "Invalid icon tag: x-circle"
**Fix**: Use `x` or `circle_x` instead

### Error: "AttributeError: 'ClaimsState' has no attribute 'method_name'"
**Fix**: Grep the state file to find the actual method name

### Error: "Invalid var passed for prop VStack.spacing, expected type... got value 10"
**Fix**: Spacing/padding props only accept '0'-'9'. Use '9' max or CSS style dict for larger values

---

## Quick Checklist Before Writing Reflex Code

- [ ] Using `rx.cond()` instead of `if/else` for conditional rendering?
- [ ] Converting Reflex Vars with `.to(type)` before comparisons?
- [ ] Using valid icon names (check docs or use simple names)?
- [ ] Using lambda default arguments for event handlers in loops?
- [ ] Verified state method names exist in the codebase?
- [ ] Using direct bracket access `claim["key"]` instead of `.get()`?

---

## Reference: Working Examples

### Risk Badge (Proper Var Handling)
```python
def risk_badge_dark(risk_score) -> rx.Component:
    # Step 1: Convert Var to float
    score = risk_score.to(float) if hasattr(risk_score, 'to') else risk_score

    # Step 2: Use rx.cond() for conditional rendering
    return rx.cond(
        score >= 0.7,
        rx.badge("HIGH RISK", color_scheme="red"),
        rx.cond(
            score >= 0.4,
            rx.badge("Medium", color_scheme="orange"),
            rx.badge("Low", color_scheme="green"),
        ),
    )
```

### Table with Event Handlers
```python
rx.foreach(
    ClaimsState.paginated_claims,
    lambda claim: rx.table.row(
        rx.table.cell(claim["id"]),
        # Use default argument to capture value
        on_click=lambda claim_id=claim["id"]: ClaimsState.open_claim_modal(str(claim_id)),
    ),
)
```

### Sortable Header with Icons
```python
def sortable_header(label, column, current_sort, direction):
    is_active = current_sort == column

    return rx.table.column_header_cell(
        rx.hstack(
            rx.text(label),
            # Use rx.cond(), not if/else
            rx.cond(
                is_active,
                rx.cond(
                    direction == "asc",
                    rx.icon("chevron_up"),  # Valid icon name
                    rx.icon("chevron_down"),  # Valid icon name
                ),
                rx.icon("chevrons_up_down"),
            ),
        ),
    )
```

---

## Summary: Most Common Mistakes

1. **Using Python `if/else` with Reflex Vars** → Use `rx.cond()`
2. **Not converting Vars before comparisons** → Use `.to(float)`
3. **Invalid icon names with hyphens** → Use underscores or simple names
4. **Using `.get()` on Reflex Var dicts** → Use bracket notation `["key"]`
5. **Lambda late binding in loops** → Use default arguments
6. **Assuming method names** → Always grep first

---

**Remember: When in doubt, check existing working code in the codebase as reference!**
