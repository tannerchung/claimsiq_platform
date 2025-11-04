"""
Enhanced Metric Cards for Dashboard V2

Clickable cards that filter the table when clicked, following the user workflow spec.
"""
import reflex as rx
from claimsiq.theme import COLORS
from claimsiq.state import ClaimsState


def clickable_metric_card(
    label: str,
    value: rx.Component,
    icon: str,
    color: str = COLORS["primary"],
    trend: str = "",
    trend_direction: str = "up",
    status_filter: str = "all",
) -> rx.Component:
    """
    Enhanced metric card that filters the table when clicked.

    Args:
        label: Card label (e.g., "Total Claims")
        value: Value component to display
        icon: Icon name
        color: Icon and accent color
        trend: Trend text (e.g., "+12%")
        trend_direction: "up" or "down"
        status_filter: Status to filter by when clicked ("all", "approved", "pending", "flagged")
    """

    # Determine if this card is currently active (selected filter)
    is_active = ClaimsState.selected_status == status_filter

    return rx.box(
        rx.vstack(
            # Top row: Icon and trend badge
            rx.hstack(
                rx.icon(
                    icon,
                    size=28,
                    color=color,
                ),
                rx.spacer(),
                rx.cond(
                    trend != "",
                    rx.badge(
                        rx.hstack(
                            rx.icon(
                                "trending-up" if trend_direction == "up" else "trending-down",
                                size=14,
                            ),
                            rx.text(trend, size="1", weight="bold"),
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
                size="3",
                weight="medium",
                class_name="text-gray-600",
                margin_top="3",
            ),
            # Value
            value,
            # Active indicator
            rx.cond(
                is_active,
                rx.badge(
                    rx.hstack(
                        rx.icon("filter", size=12),
                        rx.text("Filtered", size="1"),
                        spacing="1",
                    ),
                    color_scheme="blue",
                    variant="solid",
                    class_name="mt-2",
                ),
                rx.fragment(),
            ),
            spacing="0",
            align="start",
            width="100%",
        ),
        padding="6",
        on_click=lambda: ClaimsState.drill_into_status(status_filter),
        class_name=rx.cond(
            is_active,
            "rounded-xl bg-gradient-to-br from-blue-50 to-white shadow-lg border-2 border-blue-400 hover:shadow-xl transition-all duration-200 hover:-translate-y-1 cursor-pointer w-full",
            "rounded-xl bg-white shadow-md hover:shadow-lg transition-all duration-200 hover:-translate-y-1 cursor-pointer w-full border-2 border-transparent hover:border-gray-200",
        ),
        role="button",
        aria_label=f"Filter by {label}",
        tabindex="0",
    )


def metric_value_large(value: str | int, color: str = COLORS["gray_900"]) -> rx.Component:
    """Large value text for metric cards"""
    return rx.text(
        value,
        size="9",
        weight="bold",
        color=color,
        class_name="tabular-nums",
    )


def metric_value_with_subtitle(
    value: str | int,
    subtitle: str,
    value_color: str = COLORS["gray_900"],
    subtitle_color: str = COLORS["gray_500"],
) -> rx.Component:
    """Value with subtitle for more complex metrics"""
    return rx.vstack(
        rx.text(
            value,
            size="9",
            weight="bold",
            color=value_color,
            class_name="tabular-nums",
        ),
        rx.text(
            subtitle,
            size="2",
            color=subtitle_color,
        ),
        spacing="0",
        align="start",
    )
