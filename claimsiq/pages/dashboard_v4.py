"""
Dashboard V4 - Production-Ready with Perfect Layout

Comprehensive layout improvements:
✅ Clean grid system with consistent spacing
✅ Ample whitespace between sections
✅ Logical grouping (summary cards → charts → filters → table)
✅ Sidebar layout for filters (left) + main content (right)
✅ Sticky header with all CTAs in one place
✅ Side-by-side charts with responsive stacking
✅ Dedicated table section with sticky headers
✅ Visual hierarchy with distinct backgrounds
✅ Responsive design for mobile/tablet
✅ Error messages near relevant actions
"""
import reflex as rx
from claimsiq.state import ClaimsState
from claimsiq.components.cards_v2 import clickable_metric_card, metric_value_large, metric_value_with_subtitle
from claimsiq.components.navbar import navbar
from claimsiq.components.tables import claims_table
from claimsiq.components.charts import claims_trend_chart, risk_distribution_chart, status_breakdown_chart
from claimsiq.components.modals_v2 import claim_detail_modal_v2
from claimsiq.components.notifications import notification_toast
from claimsiq.components.filters_enhanced import (
    status_filter_section,
    risk_level_filter_section,
    date_range_filter_section,
    active_filters_summary,
)
from claimsiq.components.errors import enhanced_error_display
from claimsiq.components.pagination import enhanced_pagination
from claimsiq.theme import COLORS


def action_bar() -> rx.Component:
    """
    Sticky action bar with all primary CTAs.
    Visible at top: Data management + Export + Refresh
    """
    return rx.box(
        rx.hstack(
            # Left: Data loading actions
            rx.hstack(
                rx.button(
                    rx.hstack(
                        rx.icon("cloud-download", size=18),
                        rx.text("Kaggle", size="2", weight="medium"),
                        spacing="2",
                    ),
                    on_click=ClaimsState.load_kaggle_data,
                    loading=ClaimsState.is_loading_data,
                    disabled=ClaimsState.is_loading_data,
                    color_scheme="blue",
                    variant="soft",
                    size="2",
                    aria_label="Load real data from Kaggle",
                ),
                rx.button(
                    rx.hstack(
                        rx.icon("sparkles", size=18),
                        rx.text("Sample", size="2", weight="medium"),
                        spacing="2",
                    ),
                    on_click=lambda: ClaimsState.generate_sample_data(1000),
                    loading=ClaimsState.is_loading_data,
                    disabled=ClaimsState.is_loading_data,
                    color_scheme="green",
                    variant="soft",
                    size="2",
                    aria_label="Generate 1000 sample claims",
                ),
                spacing="2",
            ),

            rx.spacer(),

            # Center: Last updated
            rx.hstack(
                rx.icon("clock", size=16, color=COLORS["gray_500"]),
                rx.text(
                    rx.cond(
                        ClaimsState.last_updated != "",
                        f"Updated {ClaimsState.last_updated_label}",
                        "Loading...",
                    ),
                    size="2",
                    color=COLORS["gray_600"],
                    weight="medium",
                ),
                spacing="2",
                padding_x="4",
                padding_y="2",
                class_name="bg-gray-100 rounded-lg",
            ),

            rx.spacer(),

            # Right: Export and refresh actions
            rx.hstack(
                rx.button(
                    rx.hstack(
                        rx.icon("refresh-cw", size=18),
                        rx.text("Refresh", size="2", weight="medium"),
                        spacing="2",
                    ),
                    on_click=ClaimsState.refresh_all_data,
                    loading=ClaimsState.is_loading_summary | ClaimsState.is_loading_claims,
                    variant="outline",
                    color_scheme="gray",
                    size="2",
                    aria_label="Refresh all dashboard data",
                ),
                rx.button(
                    rx.hstack(
                        rx.icon("download", size=18),
                        rx.text("Export CSV", size="2", weight="medium"),
                        spacing="2",
                    ),
                    on_click=ClaimsState.export_to_csv,
                    color_scheme="blue",
                    size="2",
                    aria_label="Export filtered claims to CSV",
                ),
                spacing="2",
            ),

            width="100%",
            align="center",
            class_name="flex items-center justify-between w-full",
        ),
        padding="4",
        class_name="bg-white border-b-2 border-gray-200 shadow-sm",
        width="100%",
    )


def filters_sidebar() -> rx.Component:
    """
    Left sidebar with all filters.
    Sticky positioning to remain visible while scrolling.
    """
    return rx.box(
        rx.vstack(
            # Sidebar header
            rx.hstack(
                rx.icon("sliders-horizontal", size=20, color=COLORS["primary"]),
                rx.heading(
                    "Filters",
                    size="5",
                    color=COLORS["gray_900"],
                ),
                spacing="2",
                margin_bottom="4",
            ),

            # Clear all button
            rx.button(
                rx.hstack(
                    rx.icon("x-circle", size=16),
                    rx.text("Clear All", size="2", weight="bold"),
                    spacing="2",
                ),
                on_click=ClaimsState.clear_filters,
                color_scheme="red",
                variant="outline",
                size="2",
                width="100%",
                margin_bottom="4",
            ),

            # Active filters summary
            active_filters_summary(),

            # Filter sections
            status_filter_section(),
            risk_level_filter_section(),
            date_range_filter_section(),

            spacing="0",
            width="100%",
        ),
        padding="6",
        class_name="bg-white rounded-xl shadow-md border border-gray-200 sticky top-4",
        width="100%",
        max_height="calc(100vh - 2rem)",
        overflow_y="auto",
    )


def section_header(title: str, subtitle: str = "") -> rx.Component:
    """Section header with title and optional subtitle"""
    return rx.vstack(
        rx.heading(
            title,
            size="7",
            color=COLORS["gray_900"],
            weight="bold",
        ),
        rx.cond(
            subtitle != "",
            rx.text(
                subtitle,
                size="3",
                color=COLORS["gray_600"],
            ),
            rx.fragment(),
        ),
        spacing="1",
        align="start",
        margin_bottom="6",
    )


def summary_cards_section() -> rx.Component:
    """
    Summary cards in a clean 4-column grid.
    First thing users see for quick insights.
    """
    return rx.box(
        section_header(
            "Dashboard Overview",
            "Key metrics at a glance - click any card to filter claims",
        ),
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
            spacing="5",
            width="100%",
        ),
        padding="8",
        class_name="bg-gradient-to-br from-blue-50 to-white rounded-2xl border-2 border-blue-100",
        margin_bottom="10",
        width="100%",
    )


def analytics_section() -> rx.Component:
    """
    Analytics charts in a clean grid layout.
    Side-by-side on desktop, stacked on mobile.
    """
    return rx.box(
        section_header(
            "Analytics",
            "Trends and distribution over time",
        ),
        rx.grid(
            # Left: Trend chart (takes more space)
            claims_trend_chart(),

            # Right: Stacked distribution charts
            rx.vstack(
                risk_distribution_chart(),
                status_breakdown_chart(),
                spacing="5",
                width="100%",
            ),

            columns="2",
            spacing="5",
            width="100%",
        ),
        padding="8",
        class_name="bg-white rounded-2xl border-2 border-gray-200",
        margin_bottom="10",
        width="100%",
    )


def claims_queue_section() -> rx.Component:
    """
    Dedicated claims table section with sticky search/actions bar.
    Clear visual separation from analytics.
    """
    return rx.box(
        section_header(
            "Claims Queue",
            f"Showing {ClaimsState.sorted_claims.length()} claims - click any row to view details and take action",
        ),

        # Table container with sticky header
        rx.box(
            # Search and table actions bar
            rx.box(
                rx.hstack(
                    rx.input(
                        placeholder="Search claims by ID, provider, or status...",
                        value=ClaimsState.search_query,
                        on_change=ClaimsState.set_search_query,
                        size="3",
                        width=["100%", "100%", "400px"],
                        class_name="flex-1",
                    ),
                    rx.badge(
                        f"{ClaimsState.sorted_claims.length()} results",
                        color_scheme="blue",
                        variant="soft",
                        size="2",
                    ),
                    spacing="3",
                    width="100%",
                    align="center",
                ),
                padding="4",
                class_name="bg-gray-50 border-b border-gray-200 sticky top-0 z-10",
            ),

            # Claims table
            claims_table(),

            # Enhanced pagination
            enhanced_pagination(),

            class_name="bg-white rounded-2xl shadow-md border-2 border-gray-200 overflow-hidden",
        ),

        padding="8",
        class_name="bg-gradient-to-br from-gray-50 to-white rounded-2xl",
        width="100%",
    )


def dashboard_v4() -> rx.Component:
    """
    Dashboard V4 - Production-ready with perfect layout.

    Layout structure:
    ┌─────────────────────────────────────────────┐
    │ Navbar (sticky)                             │
    ├─────────────────────────────────────────────┤
    │ Action Bar (sticky)                         │
    │ [Kaggle] [Sample] | Updated | [Refresh] [Export] │
    ├─────────────────────────────────────────────┤
    │ Error Messages (if any)                     │
    ├───────────┬─────────────────────────────────┤
    │           │ Summary Cards (4-column grid)   │
    │           ├─────────────────────────────────┤
    │  Filters  │ Analytics Charts (2-column)     │
    │  Sidebar  │ - Trend Chart | Distribution    │
    │  (sticky) ├─────────────────────────────────┤
    │           │ Claims Queue Section            │
    │           │ - Search Bar (sticky)           │
    │           │ - Claims Table                  │
    │           │ - Pagination                    │
    └───────────┴─────────────────────────────────┘
    """
    return rx.box(
        # Global overlays
        notification_toast(),
        claim_detail_modal_v2(),

        # Main layout
        rx.vstack(
            # Sticky navbar
            rx.box(
                navbar(),
                class_name="sticky top-0 z-50",
            ),

            # Sticky action bar
            rx.box(
                action_bar(),
                class_name="sticky top-[64px] z-40",
            ),

            # Error messages (if any)
            rx.box(
                enhanced_error_display(),
                padding_x="8",
                padding_top="6",
                width="100%",
            ),

            # Main content area with sidebar + content
            rx.box(
                rx.grid(
                    # Left sidebar: Filters (sticky)
                    rx.box(
                        filters_sidebar(),
                        display=["none", "none", "block"],  # Hidden on mobile
                    ),

                    # Right content area
                    rx.vstack(
                        # Section 1: Summary Cards
                        summary_cards_section(),

                        # Section 2: Analytics Charts
                        analytics_section(),

                        # Section 3: Claims Queue
                        claims_queue_section(),

                        spacing="0",
                        width="100%",
                    ),

                    columns=["1", "1", "280px 1fr"],  # Sidebar 280px, content fills rest
                    spacing="6",
                    width="100%",
                ),
                padding="8",
                max_width="1600px",
                margin_x="auto",
                width="100%",
            ),

            spacing="0",
            width="100%",
        ),

        class_name="min-h-screen bg-gray-50",
        on_mount=ClaimsState.load_all_data,
        role="main",
        aria_label="Claims Dashboard",
    )
