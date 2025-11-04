"""
Advanced Filters Panel for Dashboard V2

Filters for date range, amount range, risk levels, and status.
Optimized for Fraud Investigator workflow.
"""
import reflex as rx
from claimsiq.theme import COLORS
from claimsiq.state import ClaimsState


def risk_filter_chip(risk_level: str, label: str, color: str) -> rx.Component:
    """Clickable chip for risk level filtering"""
    # Determine which Var to use based on risk level
    if risk_level == "low":
        is_active = ClaimsState.risk_low_active
    elif risk_level == "medium":
        is_active = ClaimsState.risk_medium_active
    elif risk_level == "high":
        is_active = ClaimsState.risk_high_active
    else:
        is_active = False

    return rx.button(
        rx.hstack(
            rx.cond(
                is_active,
                rx.icon("check", size=16),
                rx.fragment(),
            ),
            rx.text(label, weight="medium"),
            spacing="2",
        ),
        on_click=ClaimsState.toggle_risk(risk_level),
        color_scheme=color,
        variant=rx.cond(is_active, "solid", "outline"),
        size="2",
    )


def advanced_filters_panel() -> rx.Component:
    """
    Advanced filters panel with:
    - Status filter (All, Approved, Pending, Denied, Flagged)
    - Risk level filters (Low, Medium, High)
    - Date range picker
    - Amount range slider
    - Clear all filters button
    """

    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.icon("filter", size=20, color=COLORS["primary"]),
                rx.heading(
                    "Filters",
                    size="4",
                    class_name="text-xl font-semibold text-slate-800 dark:text-slate-100",
                ),
                rx.spacer(),
                rx.button(
                    rx.hstack(
                        rx.icon("x", size=16),
                        rx.text("Clear All", size="2"),
                        spacing="1",
                    ),
                    on_click=ClaimsState.clear_filters,
                    variant="ghost",
                    color_scheme="gray",
                    size="2",
                ),
                width="100%",
                align="center",
                class_name="flex items-center justify-between w-full",
                margin_bottom="4",
            ),

            # Status Filter
            rx.box(
                rx.text(
                    "Status",
                    size="2",
                    weight="bold",
                    class_name="text-sm uppercase tracking-wide text-slate-500 dark:text-slate-300",
                    margin_bottom="2",
                ),
                rx.hstack(
                    rx.button(
                        rx.hstack(
                            rx.cond(
                                ClaimsState.selected_status == "all",
                                rx.icon("check", size=16),
                                rx.fragment(),
                            ),
                            rx.text("All", weight="medium"),
                            rx.badge(ClaimsState.total_claims, color_scheme="gray", variant="soft"),
                            spacing="2",
                        ),
                        on_click=ClaimsState.set_status_filter("all"),
                        color_scheme="gray",
                        variant=rx.cond(ClaimsState.selected_status == "all", "solid", "outline"),
                        size="2",
                    ),
                    rx.button(
                        rx.hstack(
                            rx.cond(
                                ClaimsState.selected_status == "approved",
                                rx.icon("check", size=16),
                                rx.fragment(),
                            ),
                            rx.text("Approved", weight="medium"),
                            rx.badge(ClaimsState.approved_count, color_scheme="green", variant="soft"),
                            spacing="2",
                        ),
                        on_click=ClaimsState.set_status_filter("approved"),
                        color_scheme="green",
                        variant=rx.cond(ClaimsState.selected_status == "approved", "solid", "outline"),
                        size="2",
                    ),
                    rx.button(
                        rx.hstack(
                            rx.cond(
                                ClaimsState.selected_status == "pending",
                                rx.icon("check", size=16),
                                rx.fragment(),
                            ),
                            rx.text("Pending", weight="medium"),
                            rx.badge(ClaimsState.pending_count, color_scheme="blue", variant="soft"),
                            spacing="2",
                        ),
                        on_click=ClaimsState.set_status_filter("pending"),
                        color_scheme="blue",
                        variant=rx.cond(ClaimsState.selected_status == "pending", "solid", "outline"),
                        size="2",
                    ),
                    rx.button(
                        rx.hstack(
                            rx.cond(
                                ClaimsState.selected_status == "flagged",
                                rx.icon("check", size=16),
                                rx.fragment(),
                            ),
                            rx.text("Flagged", weight="medium"),
                            rx.badge(ClaimsState.flagged_count, color_scheme="orange", variant="soft"),
                            spacing="2",
                        ),
                        on_click=ClaimsState.set_status_filter("flagged"),
                        color_scheme="orange",
                        variant=rx.cond(ClaimsState.selected_status == "flagged", "solid", "outline"),
                        size="2",
                    ),
                    spacing="2",
                    wrap="wrap",
                    class_name="flex flex-wrap gap-2",
                ),
                margin_bottom="4",
            ),

            # Risk Level Filters
            rx.box(
                rx.text(
                    "Risk Levels",
                    size="2",
                    weight="bold",
                    class_name="text-sm uppercase tracking-wide text-slate-500 dark:text-slate-300",
                    margin_bottom="2",
                ),
                rx.hstack(
                    risk_filter_chip("low", "Low Risk", "green"),
                    risk_filter_chip("medium", "Medium Risk", "orange"),
                    risk_filter_chip("high", "High Risk", "red"),
                    spacing="2",
                ),
                margin_bottom="4",
            ),

            # Date Range
            rx.box(
                rx.text(
                    "Date Range",
                    size="2",
                    weight="bold",
                    class_name="text-sm uppercase tracking-wide text-slate-500 dark:text-slate-300",
                    margin_bottom="2",
                ),
                rx.hstack(
                    rx.vstack(
                        rx.text(
                            "Start Date",
                            size="1",
                            class_name="text-xs font-medium text-slate-500 dark:text-slate-300",
                        ),
                        rx.input(
                            type="date",
                            value=ClaimsState.date_start,
                            on_change=ClaimsState.update_date_start,
                            size="2",
                            class_name="w-full",
                        ),
                        spacing="1",
                        align="start",
                        class_name="flex-1",
                    ),
                    rx.vstack(
                        rx.text(
                            "End Date",
                            size="1",
                            class_name="text-xs font-medium text-slate-500 dark:text-slate-300",
                        ),
                        rx.input(
                            type="date",
                            value=ClaimsState.date_end,
                            on_change=ClaimsState.update_date_end,
                            size="2",
                            class_name="w-full",
                        ),
                        spacing="1",
                        align="start",
                        class_name="flex-1",
                    ),
                    spacing="3",
                    width="100%",
                ),
                margin_bottom="4",
            ),

            # Active Filters Summary
            rx.cond(
                (ClaimsState.selected_status != "all") |
                (ClaimsState.risk_filters.length() > 0) |
                (ClaimsState.date_start != "") |
                (ClaimsState.date_end != ""),
                rx.box(
                    rx.text(
                        "Active Filters",
                        size="2",
                        weight="bold",
                        class_name="text-sm uppercase tracking-wide text-blue-500 dark:text-blue-300",
                        margin_bottom="2",
                    ),
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
                            ),
                            rx.fragment(),
                        ),
                        spacing="2",
                        wrap="wrap",
                    ),
                    padding="3",
                    class_name="bg-blue-50 rounded-lg border border-blue-200",
                ),
                rx.fragment(),
            ),

            spacing="0",
            width="100%",
        ),
        padding="6",
        class_name="bg-white/90 dark:bg-slate-800/95 border border-slate-200/70 dark:border-slate-700/60 rounded-2xl shadow-md backdrop-blur w-full",
    )
