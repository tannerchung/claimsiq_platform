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
    base_class = (
        "w-full cursor-pointer rounded-2xl border border-slate-200/70 dark:border-slate-700/60 "
        "bg-white/90 dark:bg-slate-800/95 backdrop-blur shadow-sm hover:shadow-lg transition-all duration-200 "
        "hover:-translate-y-1"
    )
    active_class = (
        base_class
        + " ring-2 ring-blue-200/80 dark:ring-blue-500/40 border-blue-400/80 dark:border-blue-500/60 shadow-lg"
    )

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
                        class_name="bg-emerald-500/15 dark:bg-emerald-500/20 text-emerald-500 dark:text-emerald-300"
                        if trend_direction == "up"
                        else "bg-rose-500/15 dark:bg-rose-500/20 text-rose-500 dark:text-rose-300",
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
                class_name="text-sm font-medium tracking-wide text-slate-500 dark:text-slate-300 uppercase",
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
                    class_name="mt-3 bg-blue-500/15 dark:bg-blue-500/20 text-blue-500 dark:text-blue-300",
                ),
                rx.fragment(),
            ),
            spacing="3",
            align="start",
            width="100%",
        ),
        padding="6",
        on_click=ClaimsState.drill_into_status(status_filter),
        class_name=rx.cond(is_active, active_class, base_class),
        role="button",
        aria_label=f"Filter by {label}",
        tabindex="0",
    )


def metric_value_large(value: str | int, color: str | None = None) -> rx.Component:
    """Large value text for metric cards"""
    return rx.text(
        value,
        size="9",
        weight="bold",
        class_name="tabular-nums text-5xl font-bold text-slate-900 dark:text-slate-100",
        style={"color": color} if color else None,
    )


def metric_trend(text: str) -> rx.Component:
    """Trend indicator for metric cards (e.g., +12%, -3%)"""
    return rx.text(
        text,
        size="2",
        weight="medium",
        color=COLORS["gray_600"],
        class_name="text-sm text-slate-500 dark:text-slate-300",
    )


def metric_value_with_subtitle(
    value: str | int,
    subtitle: str,
    value_color: str | None = None,
    subtitle_color: str | None = None,
) -> rx.Component:
    """Value with subtitle for more complex metrics"""
    return rx.vstack(
        rx.text(
            value,
            size="9",
            weight="bold",
            class_name="tabular-nums text-5xl font-bold text-slate-900 dark:text-slate-100",
            style={"color": value_color} if value_color else None,
        ),
        rx.text(
            subtitle,
            size="2",
            class_name="text-sm text-slate-500 dark:text-slate-300",
            style={"color": subtitle_color} if subtitle_color else None,
        ),
        spacing="0",
        align="start",
    )
