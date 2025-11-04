"""
Enhanced Filters Panel with Better UX

Improvements:
- Collapsible sections for each filter group
- Visual grouping and better spacing
- Tooltips for clarity
- Prominent "Clear All" button
- Accessible aria-labels
"""
import reflex as rx
from claimsiq.theme import COLORS
from claimsiq.state import ClaimsState


def filter_section(
    title: str,
    icon: str,
    content: rx.Component,
    tooltip: str = "",
    is_open: bool = True,
) -> rx.Component:
    """
    Collapsible filter section with header and content.

    Args:
        title: Section title
        icon: Icon name
        content: Filter controls content
        tooltip: Helpful tooltip text
        is_open: Whether section starts expanded
    """
    return rx.box(
        rx.vstack(
            # Section header with icon
            rx.hstack(
                rx.icon(icon, size=18, color=COLORS["primary"]),
                rx.text(
                    title,
                    size="3",
                    weight="bold",
                    color=COLORS["gray_900"],
                ),
                rx.cond(
                    tooltip != "",
                    rx.tooltip(
                        rx.icon("circle_help", size=14, color=COLORS["gray_500"]),
                        content=tooltip,
                    ),
                    rx.fragment(),
                ),
                spacing="2",
                align="center",
                margin_bottom="3",
            ),

            # Section content
            content,

            spacing="0",
            width="100%",
        ),
        padding="4",
        class_name="bg-gray-50 rounded-lg border border-gray-200",
        margin_bottom="3",
        width="100%",
    )


def status_filter_section() -> rx.Component:
    """Status filter with badges showing counts"""
    return filter_section(
        title="Status",
        icon="filter",
        tooltip="Filter claims by their current processing status",
        content=rx.vstack(
            rx.text(
                "Select a status to filter claims:",
                size="2",
                color=COLORS["gray_600"],
                margin_bottom="2",
            ),
            rx.box(
                rx.grid(
                    rx.button(
                        rx.hstack(
                            rx.cond(
                                ClaimsState.selected_status == "all",
                                rx.icon("check", size=16),
                                rx.fragment(),
                            ),
                            rx.text("All", weight="medium", size="2"),
                            rx.badge(
                                ClaimsState.total_claims,
                                color_scheme="gray",
                                variant="soft",
                                size="1",
                            ),
                            spacing="2",
                        ),
                        on_click=ClaimsState.set_status_filter("all"),
                        color_scheme="gray",
                        variant=rx.cond(ClaimsState.selected_status == "all", "solid", "outline"),
                        size="2",
                        width="100%",
                    ),
                    rx.button(
                        rx.hstack(
                            rx.cond(
                                ClaimsState.selected_status == "approved",
                                rx.icon("check", size=16),
                                rx.fragment(),
                            ),
                            rx.text("Approved", weight="medium", size="2"),
                            rx.badge(
                                ClaimsState.approved_count,
                                color_scheme="green",
                                variant="soft",
                                size="1",
                            ),
                            spacing="2",
                        ),
                        on_click=ClaimsState.set_status_filter("approved"),
                        color_scheme="green",
                        variant=rx.cond(ClaimsState.selected_status == "approved", "solid", "outline"),
                        size="2",
                        width="100%",
                    ),
                    rx.button(
                        rx.hstack(
                            rx.cond(
                                ClaimsState.selected_status == "pending",
                                rx.icon("check", size=16),
                                rx.fragment(),
                            ),
                            rx.text("Pending", weight="medium", size="2"),
                            rx.badge(
                                ClaimsState.pending_count,
                                color_scheme="blue",
                                variant="soft",
                                size="1",
                            ),
                            spacing="2",
                        ),
                        on_click=ClaimsState.set_status_filter("pending"),
                        color_scheme="blue",
                        variant=rx.cond(ClaimsState.selected_status == "pending", "solid", "outline"),
                        size="2",
                        width="100%",
                    ),
                    rx.button(
                        rx.hstack(
                            rx.cond(
                                ClaimsState.selected_status == "flagged",
                                rx.icon("check", size=16),
                                rx.fragment(),
                            ),
                            rx.text("Flagged", weight="medium", size="2"),
                            rx.badge(
                                ClaimsState.flagged_count,
                                color_scheme="orange",
                                variant="soft",
                                size="1",
                            ),
                            spacing="2",
                        ),
                        on_click=ClaimsState.set_status_filter("flagged"),
                        color_scheme="orange",
                        variant=rx.cond(ClaimsState.selected_status == "flagged", "solid", "outline"),
                        size="2",
                        width="100%",
                    ),
                    columns="2",
                    spacing="2",
                    width="100%",
                ),
            ),
            spacing="0",
            width="100%",
        ),
    )


def risk_level_filter_section() -> rx.Component:
    """Risk level filter with multi-select chips"""
    def risk_chip(level: str, label: str, color: str, is_active):
        return rx.button(
            rx.hstack(
                rx.cond(
                    is_active,
                    rx.icon("check", size=16),
                    rx.fragment(),
                ),
                rx.text(label, weight="medium", size="2"),
                spacing="2",
            ),
            on_click=ClaimsState.toggle_risk(level),
            color_scheme=color,
            variant=rx.cond(is_active, "solid", "outline"),
            size="2",
            width="100%",
            aria_label=f"Filter by {label}",
        )

    return filter_section(
        title="Risk Levels",
        icon="shield-alert",
        tooltip="Filter by risk score: Low (0-0.4), Medium (0.4-0.7), High (0.7+). You can select multiple levels.",
        content=rx.vstack(
            rx.text(
                "Select one or more risk levels:",
                size="2",
                color=COLORS["gray_600"],
                margin_bottom="2",
            ),
            rx.grid(
                risk_chip("low", "Low Risk", "green", ClaimsState.risk_low_active),
                risk_chip("medium", "Medium Risk", "orange", ClaimsState.risk_medium_active),
                risk_chip("high", "High Risk", "red", ClaimsState.risk_high_active),
                columns="3",
                spacing="2",
                width="100%",
            ),
            spacing="0",
            width="100%",
        ),
    )


def date_range_filter_section() -> rx.Component:
    """Date range filter with calendar pickers"""
    return filter_section(
        title="Date Range",
        icon="calendar",
        tooltip="Filter claims by their submission date range",
        content=rx.vstack(
            rx.text(
                "Select date range for claims:",
                size="2",
                color=COLORS["gray_600"],
                margin_bottom="2",
            ),
            rx.grid(
                rx.vstack(
                    rx.text("Start Date", size="1", color=COLORS["gray_700"], weight="medium"),
                    rx.input(
                        type="date",
                        value=ClaimsState.date_start,
                        on_change=ClaimsState.update_date_start,
                        size="2",
                        width="100%",
                        aria_label="Start date for filter",
                    ),
                    spacing="1",
                    align="start",
                    width="100%",
                ),
                rx.vstack(
                    rx.text("End Date", size="1", color=COLORS["gray_700"], weight="medium"),
                    rx.input(
                        type="date",
                        value=ClaimsState.date_end,
                        on_change=ClaimsState.update_date_end,
                        size="2",
                        width="100%",
                        aria_label="End date for filter",
                    ),
                    spacing="1",
                    align="start",
                    width="100%",
                ),
                columns="2",
                spacing="3",
                width="100%",
            ),
            spacing="0",
            width="100%",
        ),
    )


def active_filters_summary() -> rx.Component:
    """Summary of currently active filters with quick remove buttons"""
    return rx.cond(
        (ClaimsState.selected_status != "all") |
        (ClaimsState.risk_filters.length() > 0) |
        (ClaimsState.date_start != "") |
        (ClaimsState.date_end != ""),
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.icon("filter-x", size=16, color=COLORS["primary"]),
                    rx.text(
                        "Active Filters",
                        size="2",
                        weight="bold",
                        color=COLORS["primary"],
                    ),
                    spacing="2",
                    margin_bottom="2",
                ),
                rx.box(
                    rx.hstack(
                        rx.cond(
                            ClaimsState.selected_status != "all",
                            rx.badge(
                                rx.hstack(
                                    rx.text(f"Status: {ClaimsState.selected_status}", size="1"),
                                    rx.icon("x", size=12),
                                    spacing="1",
                                ),
                                color_scheme="blue",
                                variant="solid",
                                on_click=ClaimsState.set_status_filter("all"),
                                cursor="pointer",
                                role="button",
                                aria_label="Remove status filter",
                            ),
                            rx.fragment(),
                        ),
                        rx.cond(
                            ClaimsState.risk_filters.length() > 0,
                            rx.badge(
                                rx.hstack(
                                    rx.text(f"{ClaimsState.risk_filters.length()} risk filters", size="1"),
                                    rx.icon("x", size=12),
                                    spacing="1",
                                ),
                                color_scheme="orange",
                                variant="solid",
                                on_click=ClaimsState.set_risk_filters([]),
                                cursor="pointer",
                                role="button",
                                aria_label="Remove risk filters",
                            ),
                            rx.fragment(),
                        ),
                        rx.cond(
                            (ClaimsState.date_start != "") | (ClaimsState.date_end != ""),
                            rx.badge(
                                rx.hstack(
                                    rx.text("Date range", size="1"),
                                    rx.icon("x", size=12),
                                    spacing="1",
                                ),
                                color_scheme="purple",
                                variant="solid",
                                on_click=lambda: [ClaimsState.set_date_range("", "")],
                                cursor="pointer",
                                role="button",
                                aria_label="Remove date filter",
                            ),
                            rx.fragment(),
                        ),
                        spacing="2",
                        wrap="wrap",
                    ),
                ),
                spacing="0",
                width="100%",
            ),
            padding="3",
            class_name="bg-blue-50 rounded-lg border border-blue-200",
            margin_bottom="3",
            width="100%",
        ),
        rx.fragment(),
    )


def enhanced_filters_panel() -> rx.Component:
    """
    Enhanced filters panel with:
    - Collapsible sections
    - Visual grouping
    - Tooltips
    - Prominent Clear All button
    - Active filters summary
    """
    return rx.box(
        rx.vstack(
            # Header with Clear All button
            rx.hstack(
                rx.hstack(
                    rx.icon("sliders-horizontal", size=20, color=COLORS["primary"]),
                    rx.heading("Filters", size="4", class_name="text-gray-900"),
                    spacing="2",
                    align="center",
                ),
                rx.spacer(),
                rx.button(
                    rx.hstack(
                        rx.icon("x", size=18),
                        rx.text("Clear All Filters", size="2", weight="bold"),
                        spacing="2",
                    ),
                    on_click=ClaimsState.clear_filters,
                    variant="solid",
                    color_scheme="red",
                    size="2",
                    aria_label="Clear all active filters",
                ),
                width="100%",
                align="center",
                class_name="flex items-center justify-between w-full",
                margin_bottom="4",
            ),

            # Active filters summary (if any)
            active_filters_summary(),

            # Filter sections
            status_filter_section(),
            risk_level_filter_section(),
            date_range_filter_section(),

            spacing="0",
            width="100%",
        ),
        padding="5",
        class_name="bg-white rounded-xl shadow-md border-2 border-gray-200",
        width="100%",
    )
