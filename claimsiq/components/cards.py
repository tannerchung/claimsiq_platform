import reflex as rx
from claimsiq.theme import COLORS, FONT_SIZES, SPACING, SHADOWS, TRANSITIONS

def metric_card(
    label: str,
    value: rx.Component,
    icon: str,
    color: str = COLORS["primary"],
    trend: str = "",
    trend_direction: str = "up"
) -> rx.Component:
    """Enhanced metric card with icon, value, and optional trend indicator"""
    return rx.box(
        rx.vstack(
            # Top row: Icon and trend badge
            rx.hstack(
                rx.icon(
                    icon,
                    size=24,
                    color=color,
                ),
                rx.spacer(),
                rx.cond(
                    trend != "",
                    rx.badge(
                        rx.hstack(
                            rx.icon(
                                "trending-up" if trend_direction == "up" else "trending-down",
                                size=12,
                            ),
                            rx.text(trend, size="1"),
                            spacing="1",
                            align="center",
                        ),
                        color_scheme="green" if trend_direction == "up" else "red",
                        variant="soft",
                    ),
                    rx.fragment(),
                ),
                width="100%",
                align="center",
            ),
            # Label
            rx.text(
                label,
                size="2",
                color=COLORS["gray_500"],
                weight="medium",
            ),
            # Value
            value,
            spacing="3",
            align="start",
            width="100%",
        ),
        padding="5",
        border_radius="0.75rem",
        background=COLORS["white"],
        box_shadow=SHADOWS["md"],
        width="100%",
        transition=TRANSITIONS["normal"],
        _hover={
            "box_shadow": SHADOWS["lg"],
            "transform": "translateY(-2px)",
        },
        cursor="pointer",
    )
