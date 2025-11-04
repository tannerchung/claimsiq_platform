"""
Dark Mode Form Controls with Enhanced Typography

Features:
- ✅ Larger text in inputs (16px minimum)
- ✅ Generous padding (12px horizontal, 10px vertical)
- ✅ High contrast labels
- ✅ Bold labels for clarity
- ✅ Better line heights
- ✅ Accessible color combinations
"""
import reflex as rx
from claimsiq.theme import DARK_COLORS


def dark_input(
    placeholder: str = "",
    value: str = "",
    on_change=None,
    type: str = "text",
    size: str = "3",
) -> rx.Component:
    """
    Enhanced input field for dark mode with:
    - 16px font size
    - Generous padding
    - High contrast
    """
    return rx.input(
        placeholder=placeholder,
        value=value,
        on_change=on_change,
        type=type,
        size=size,
        style={
            "font-size": "16px",
            "font-weight": "400",
            "padding": "10px 16px",  # Generous padding
            "line-height": "1.6",
            "color": DARK_COLORS["text_primary"],
            "background": DARK_COLORS["bg_card"],
            "border": f"1px solid {DARK_COLORS['border']}",
            "border-radius": "8px",
            "_placeholder": {
                "color": DARK_COLORS["text_tertiary"],
            },
            "_focus": {
                "border-color": DARK_COLORS["primary"],
                "box-shadow": f"0 0 0 2px {DARK_COLORS['primary_bg']}",
            },
        },
    )


def dark_select(
    options: list,
    value: str = "",
    on_change=None,
    size: str = "3",
) -> rx.Component:
    """
    Enhanced select dropdown for dark mode
    """
    return rx.select(
        options,
        value=value,
        on_change=on_change,
        size=size,
        style={
            "font-size": "16px",
            "font-weight": "400",
            "padding": "10px 16px",
            "line-height": "1.6",
            "color": DARK_COLORS["text_primary"],
            "background": DARK_COLORS["bg_card"],
            "border": f"1px solid {DARK_COLORS["border"]}",
            "border-radius": "8px",
        },
    )


def dark_label(
    text: str,
    for_id: str = "",
) -> rx.Component:
    """
    Enhanced label with bold weight and high contrast
    """
    return rx.text(
        text,
        as_="label",
        for_=for_id,
        style={
            "font-size": "15px",
            "font-weight": "600",  # Bold labels
            "color": DARK_COLORS["text_primary"],
            "margin-bottom": "8px",
            "display": "block",
            "letter-spacing": "0.3px",
        },
    )


def dark_button(
    text: str,
    on_click=None,
    variant: str = "solid",
    color_scheme: str = "blue",
    size: str = "3",
    icon: str = "",
) -> rx.Component:
    """
    Enhanced button with proper padding and typography
    """
    content = rx.cond(
        icon != "",
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(text, weight="medium"),
            spacing="2",
        ),
        rx.text(text, weight="medium"),
    )

    return rx.button(
        content,
        on_click=on_click,
        variant=variant,
        color_scheme=color_scheme,
        size=size,
        style={
            "font-size": "16px",
            "font-weight": "600",
            "padding": "10px 20px",  # Generous padding
            "line-height": "1.5",
            "min-height": "44px",  # Touch-friendly
            "border-radius": "8px",
        },
    )


def dark_search_input(
    placeholder: str = "Search claims...",
    on_change=None,
) -> rx.Component:
    """
    Search input with icon and enhanced padding
    """
    return rx.box(
        rx.hstack(
            rx.icon(
                "search",
                size=20,
                color=DARK_COLORS["text_tertiary"],
                style={
                    "position": "absolute",
                    "left": "16px",
                    "top": "50%",
                    "transform": "translateY(-50%)",
                },
            ),
            rx.input(
                placeholder=placeholder,
                on_change=on_change,
                style={
                    "font-size": "16px",
                    "font-weight": "400",
                    "padding": "10px 16px 10px 48px",  # Left padding for icon
                    "line-height": "1.6",
                    "width": "100%",
                    "color": DARK_COLORS["text_primary"],
                    "background": DARK_COLORS["bg_card"],
                    "border": f"1px solid {DARK_COLORS['border']}",
                    "border-radius": "8px",
                    "_placeholder": {
                        "color": DARK_COLORS["text_tertiary"],
                    },
                    "_focus": {
                        "border-color": DARK_COLORS["primary"],
                        "box-shadow": f"0 0 0 2px {DARK_COLORS['primary_bg']}",
                    },
                },
            ),
            position="relative",
            width="100%",
        ),
        width="100%",
    )


def dark_checkbox(
    label: str,
    checked: bool = False,
    on_change=None,
) -> rx.Component:
    """
    Enhanced checkbox with bold label
    """
    return rx.hstack(
        rx.checkbox(
            checked=checked,
            on_change=on_change,
            size="3",
            style={
                "accent-color": DARK_COLORS["primary"],
            },
        ),
        rx.text(
            label,
            style={
                "font-size": "16px",
                "font-weight": "500",
                "color": DARK_COLORS["text_primary"],
                "cursor": "pointer",
            },
            on_click=on_change,
        ),
        spacing="3",
        align="center",
    )
