import reflex as rx
from claimsiq.theme import COLORS, FONT_SIZES, SPACING, SHADOWS, TRANSITIONS

def metric_card(
    label: str,
    value: rx.Component,
    icon: str,
    color: str = COLORS["primary"],
    trend: str = "",
    trend_direction: str = "up",
    description: str = "",
    cta_label: str | None = None,
    on_click=None,
) -> rx.Component:
    """Enhanced metric card with icon, value, optional trend indicator, and contextual CTA."""
    box_kwargs = {}
    if on_click:
        box_kwargs["on_click"] = on_click
        box_kwargs["cursor"] = "pointer"
        box_kwargs["role"] = "button"
        box_kwargs["tab_index"] = 0
        box_kwargs["aria_label"] = label
    else:
        box_kwargs["cursor"] = "default"

    base_classes = (
        "rounded-xl bg-white shadow-md hover:shadow-lg transition-all duration-200 "
        "hover:-translate-y-0.5 focus-visible:outline-none focus-visible:ring-2 "
        "focus-visible:ring-offset-2 focus-visible:ring-blue-500"
    )
    if on_click:
        base_classes = f"{base_classes} cursor-pointer"
    else:
        base_classes = f"{base_classes} cursor-default"

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
                                "trending_up" if trend_direction == "up" else "trending_down",
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
                class_name="flex items-center justify-between w-full",
            ),
            # Label
            rx.text(
                label,
                size="2",
                weight="medium",
                class_name="text-gray-500 font-medium",
                margin_top="2",
            ),
            # Value
            value,
            # Supporting copy
            rx.cond(
                description != "",
                rx.text(
                    description,
                    size="1",
                    color=COLORS["gray_500"],
                    margin_top="1",
                ),
                rx.fragment(),
            ),
            # CTA row
            rx.cond(
                cta_label is not None,
                rx.hstack(
                    rx.text(
                        cta_label,
                        size="2",
                        color=color,
                        weight="medium",
                    ),
                    rx.icon("arrow_up_right", size=16, color=color),
                    spacing="1",
                    align="center",
                    class_name="group-hover:translate-x-0.5 transition-transform duration-200",
                ),
                rx.fragment(),
            ),
            spacing="0",
            align="start",
            width="100%",
        ),
        padding="6",
        class_name=f"{base_classes} w-full",
        **box_kwargs,
    )
