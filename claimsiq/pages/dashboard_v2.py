"""
Dashboard V2 - Optimized for User Workflows

Enhanced dashboard designed specifically for:
1. Claims Manager - Portfolio snapshot and trend analysis
2. Claims Processor - Efficient work queue processing
3. Fraud Investigator - Pattern detection and investigation

Key improvements:
- Clickable metric cards that filter the table
- Enhanced claim detail modal with action buttons
- Advanced filters panel for investigators
- CSV export functionality
- Real-time toast notifications
- Better visual indicators for sorting/filtering state
"""
import reflex as rx
from claimsiq.state import ClaimsState
from claimsiq.components.cards_v2 import clickable_metric_card, metric_value_large, metric_value_with_subtitle
from claimsiq.components.navbar import navbar
from claimsiq.components.tables import claims_table
from claimsiq.components.charts import claims_trend_chart, risk_distribution_chart, status_breakdown_chart
from claimsiq.components.modals_v2 import claim_detail_modal_v2
from claimsiq.components.notifications import notification_toast
from claimsiq.components.data_management import compact_data_buttons
from claimsiq.components.filters_v2 import advanced_filters_panel
from claimsiq.theme import COLORS


def export_button() -> rx.Component:
    """CSV export button with download functionality"""
    return rx.button(
        rx.hstack(
            rx.icon("download", size=18),
            rx.text("Export CSV", size="2", weight="medium"),
            spacing="2",
        ),
        on_click=ClaimsState.export_to_csv,
        color_scheme="blue",
        variant="outline",
        size="2",
    )


def refresh_button() -> rx.Component:
    """Refresh all data button"""
    return rx.button(
        rx.hstack(
            rx.icon("refresh-cw", size=18),
            rx.text("Refresh", size="2"),
            spacing="2",
        ),
        on_click=ClaimsState.refresh_all_data,
        loading=ClaimsState.is_loading_summary | ClaimsState.is_loading_claims,
        color_scheme="gray",
        variant="outline",
        size="2",
    )


def dashboard_v2() -> rx.Component:
    """
    Dashboard V2 - Fully optimized for all three user personas.

    Layout:
    1. Navbar with data controls and export
    2. 4 Clickable Metric Cards (Total, Approved, Pending, Flagged)
    3. Analytics Charts Row
    4. Advanced Filters Panel (collapsible)
    5. Claims Table (with sorting, search, pagination)
    6. Claim Detail Modal (with action buttons)
    7. Toast Notifications
    """
    return rx.box(
        # Toast notifications overlay
        notification_toast(),

        # Claim details modal
        claim_detail_modal_v2(),

        rx.vstack(
            # Navbar
            navbar(),

            # Main Content Container
            rx.box(
                rx.vstack(
                    # Error message (if any)
                    rx.cond(
                        ClaimsState.error_message != "",
                        rx.callout(
                            ClaimsState.error_message,
                            icon="triangle_alert",
                            color_scheme="red",
                            role="alert",
                            class_name="mb-6",
                        ),
                        rx.fragment(),
                    ),

                    # Header with actions
                    rx.hstack(
                        rx.vstack(
                            rx.heading(
                                "Dashboard V2",
                                size="8",
                                class_name="text-gray-900",
                            ),
                            rx.text(
                                rx.cond(
                                    ClaimsState.last_updated != "",
                                    f"Last updated: {ClaimsState.last_updated_label}",
                                    "Loading data...",
                                ),
                                size="2",
                                color=COLORS["gray_600"],
                            ),
                            spacing="1",
                            align="start",
                        ),
                        rx.spacer(),
                        rx.hstack(
                            compact_data_buttons(),
                            refresh_button(),
                            export_button(),
                            spacing="2",
                        ),
                        width="100%",
                        align="center",
                        class_name="flex items-center justify-between w-full",
                        margin_bottom="6",
                    ),

                    # STEP 2: VIEW PORTFOLIO SNAPSHOT - 4 Clickable Metric Cards
                    rx.box(
                        rx.grid(
                            clickable_metric_card(
                                label="Total Claims",
                                value=metric_value_large(
                                    ClaimsState.total_claims,
                                    color=COLORS["primary"]
                                ),
                                icon="file-text",
                                color=COLORS["primary"],
                                trend="+12%",
                                trend_direction="up",
                                status_filter="all",
                            ),
                            clickable_metric_card(
                                label="Approved",
                                value=metric_value_with_subtitle(
                                    ClaimsState.approved_count,
                                    ClaimsState.approval_rate_label,
                                    value_color=COLORS["success"],
                                ),
                                icon="circle-check",
                                color=COLORS["success"],
                                trend="+8%",
                                trend_direction="up",
                                status_filter="approved",
                            ),
                            clickable_metric_card(
                                label="Pending",
                                value=metric_value_large(
                                    ClaimsState.pending_count,
                                    color=COLORS["warning"]
                                ),
                                icon="clock",
                                color=COLORS["warning"],
                                trend="-3%",
                                trend_direction="down",
                                status_filter="pending",
                            ),
                            clickable_metric_card(
                                label="Flagged",
                                value=metric_value_large(
                                    ClaimsState.flagged_count,
                                    color=COLORS["danger"]
                                ),
                                icon="flag",
                                color=COLORS["danger"],
                                trend="+5%",
                                trend_direction="up",
                                status_filter="flagged",
                            ),
                            columns="4",
                            spacing="4",
                            width="100%",
                        ),
                        margin_bottom="8",
                        width="100%",
                    ),

                    # STEP 3: ANALYZE TRENDS - Charts Section
                    rx.box(
                        rx.heading(
                            "Analytics",
                            size="6",
                            class_name="text-gray-900",
                            margin_bottom="4",
                        ),
                        rx.grid(
                            claims_trend_chart(),
                            rx.vstack(
                                risk_distribution_chart(),
                                status_breakdown_chart(),
                                spacing="4",
                                width="100%",
                            ),
                            columns="2",
                            spacing="4",
                            width="100%",
                        ),
                        margin_bottom="8",
                        width="100%",
                    ),

                    # STEP 4 & 5: DEEP DIVE - Advanced Filters & Claims Table
                    rx.heading(
                        "Claims Queue",
                        size="6",
                        class_name="text-gray-900",
                        margin_top="2",
                        margin_bottom="4",
                    ),

                    # Advanced Filters Panel
                    advanced_filters_panel(),

                    rx.box(height="4"),  # Spacer

                    # Claims Table
                    claims_table(),

                    spacing="0",
                    width="100%",
                ),
                class_name="px-4 py-6 md:px-6 md:py-8 lg:px-8 lg:py-10 max-w-7xl mx-auto w-full",
            ),

            spacing="0",
            width="100%",
            class_name="w-full",
        ),

        class_name="min-h-screen bg-gray-50",
        on_mount=ClaimsState.load_all_data,
    )
