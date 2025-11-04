"""
Dashboard V3 - Production-Ready with UX Improvements

Comprehensive UX enhancements based on feedback:
✅ Enhanced error messages with retry buttons and troubleshooting
✅ Improved filters panel with collapsible sections and tooltips
✅ Better pagination with page indicators
✅ Sticky header with global actions
✅ Improved loading states and confirmations
✅ Accessibility improvements (aria-labels, tooltips)
✅ Consistent styling and spacing
✅ Alternating table row colors
✅ Better visual hierarchy
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
from claimsiq.components.filters_enhanced import enhanced_filters_panel
from claimsiq.components.errors import enhanced_error_display
from claimsiq.components.pagination import enhanced_pagination
from claimsiq.theme import COLORS


def export_button() -> rx.Component:
    """CSV export button with icon and loading state"""
    return rx.tooltip(
        rx.button(
            rx.hstack(
                rx.icon("download", size=18),
                rx.text("Export CSV", size="2", weight="medium"),
                spacing="2",
            ),
            on_click=ClaimsState.export_to_csv,
            color_scheme="blue",
            variant="outline",
            size="2",
            aria_label="Export filtered claims to CSV file",
        ),
        content="Download current view as CSV file",
    )


def refresh_button() -> rx.Component:
    """Refresh data button with loading state"""
    return rx.tooltip(
        rx.button(
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
            aria_label="Refresh all dashboard data",
        ),
        content="Reload data from server",
    )


def sticky_header() -> rx.Component:
    """Sticky header with global actions and key stats"""
    return rx.box(
        rx.vstack(
            # Navbar
            navbar(),

            # Dashboard header with actions
            rx.box(
                rx.hstack(
                    # Title and last updated
                    rx.vstack(
                        rx.heading(
                            "Claims Dashboard",
                            size="8",
                            class_name="text-gray-900",
                        ),
                        rx.hstack(
                            rx.icon("clock", size=14, color=COLORS["gray_500"]),
                            rx.text(
                                rx.cond(
                                    ClaimsState.last_updated != "",
                                    f"Updated: {ClaimsState.last_updated_label}",
                                    "Loading...",
                                ),
                                size="2",
                                color=COLORS["gray_600"],
                            ),
                            spacing="1",
                        ),
                        spacing="1",
                        align="start",
                    ),
                    rx.spacer(),

                    # Global actions
                    rx.hstack(
                        compact_data_buttons(),
                        refresh_button(),
                        export_button(),
                        spacing="2",
                    ),

                    width="100%",
                    align="center",
                    class_name="flex items-center justify-between w-full",
                ),
                class_name="px-4 py-4 md:px-6 md:py-4 lg:px-8 lg:py-4 max-w-7xl mx-auto w-full",
            ),

            spacing="0",
            width="100%",
        ),
        class_name="sticky top-0 z-40 bg-white border-b-2 border-gray-200 shadow-sm",
        width="100%",
    )


def help_text_callout() -> rx.Component:
    """First-time user help text"""
    return rx.box(
        rx.hstack(
            rx.icon("info", size=20, color=COLORS["primary"]),
            rx.vstack(
                rx.text(
                    "Welcome to Claims Dashboard",
                    size="3",
                    weight="bold",
                    color=COLORS["primary"],
                ),
                rx.text(
                    "Click metric cards to filter claims • Use Advanced Filters for detailed searches • Click any claim row to view details and take actions",
                    size="2",
                    color=COLORS["gray_700"],
                ),
                spacing="1",
                align="start",
            ),
            spacing="3",
            align="start",
        ),
        padding="4",
        class_name="bg-blue-50 border-l-4 border-blue-500 rounded-lg",
        margin_bottom="6",
        width="100%",
        role="status",
        aria_label="Dashboard help information",
    )


def loading_overlay() -> rx.Component:
    """Full-screen loading overlay for initial data load"""
    return rx.cond(
        ClaimsState.is_loading_summary & ClaimsState.is_loading_claims,
        rx.box(
            rx.vstack(
                rx.spinner(size="3", color=COLORS["primary"]),
                rx.text(
                    "Loading dashboard data...",
                    size="3",
                    color=COLORS["gray_700"],
                    weight="medium",
                ),
                spacing="3",
                align="center",
            ),
            class_name="fixed inset-0 bg-white bg-opacity-90 flex items-center justify-center z-50",
        ),
        rx.fragment(),
    )


def dashboard_v3() -> rx.Component:
    """
    Dashboard V3 - Production-ready with comprehensive UX improvements.

    Features:
    - Sticky header with global actions
    - Enhanced error messages with retry buttons
    - Improved filters with collapsible sections
    - Better pagination with clear indicators
    - Loading states and confirmations
    - Accessibility improvements
    - Help text for first-time users
    - Consistent visual design
    """
    return rx.box(
        # Toast notifications overlay
        notification_toast(),

        # Claim details modal
        claim_detail_modal_v2(),

        # Loading overlay
        loading_overlay(),

        rx.vstack(
            # Sticky header
            sticky_header(),

            # Main Content Container
            rx.box(
                rx.vstack(
                    # Enhanced error display
                    enhanced_error_display(),

                    # Help text for new users (can be dismissible)
                    rx.cond(
                        ClaimsState.total_claims == 0,
                        help_text_callout(),
                        rx.fragment(),
                    ),

                    # Metric Cards
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

                    # Analytics Charts
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

                    # Claims Queue Section
                    rx.box(
                        rx.heading(
                            "Claims Queue",
                            size="6",
                            class_name="text-gray-900",
                            margin_bottom="4",
                        ),

                        # Enhanced Filters Panel
                        enhanced_filters_panel(),

                        rx.box(height="4"),  # Spacer

                        # Claims Table with enhanced pagination
                        rx.box(
                            claims_table(),
                            enhanced_pagination(),
                            class_name="bg-white rounded-xl shadow-md overflow-hidden",
                        ),

                        width="100%",
                    ),

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
        role="main",
        aria_label="Claims Dashboard",
    )
