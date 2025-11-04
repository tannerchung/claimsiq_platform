import reflex as rx

from claimsiq.components.cards import metric_card
from claimsiq.components.charts import (
    claims_trend_chart,
    risk_distribution_chart,
    status_breakdown_chart,
)
from claimsiq.components.data_management import data_management_panel
from claimsiq.components.filters import filters_panel
from claimsiq.components.modals import claim_detail_modal
from claimsiq.components.navbar import navbar
from claimsiq.components.notifications import notification_toast
from claimsiq.components.tables import claims_table
from claimsiq.components.ui_helpers import skeleton_card
from claimsiq.state import ClaimsState
from claimsiq.theme import COLORS


def _time_range_select() -> rx.Component:
    """Shared time range selector driving the entire dashboard."""
    time_range_map = {
        "Last 7 days": "7d",
        "Last 30 days": "30d",
        "Last 90 days": "90d",
        "Last 12 months": "365d",
    }

    return rx.vstack(
        rx.text("Time range", size="2", color=COLORS["gray_500"], weight="medium"),
        rx.select(
            list(time_range_map.keys()),
            value=rx.match(
                ClaimsState.time_range,
                ("7d", "Last 7 days"),
                ("30d", "Last 30 days"),
                ("90d", "Last 90 days"),
                ("365d", "Last 12 months"),
                "Last 90 days",
            ),
            on_change=lambda label: ClaimsState.set_time_range(time_range_map.get(label, "90d")),
            size="2",
            width="180px",
        ),
        spacing="2",
        align="start",
    )


def _global_controls() -> rx.Component:
    """Top-level controls and status indicators."""
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.heading("Dashboard", size="8", class_name="text-gray-900"),
                rx.text(
                    "Monitor claims performance, spotlight risks, and drill into flagged items in a single view.",
                    size="3",
                    color=COLORS["gray_600"],
                    max_width="720px",
                ),
                spacing="2",
                align="start",
            ),
            rx.spacer(),
            rx.vstack(
                _time_range_select(),
                rx.hstack(
                    rx.text("Last updated", size="1", color=COLORS["gray_500"]),
                    rx.badge(
                        ClaimsState.last_updated_label,
                        color_scheme="gray",
                        variant="soft",
                    ),
                    spacing="2",
                    align="center",
                ),
                spacing="4",
                align="end",
            ),
            width="100%",
            align="start",
        ),
        rx.hstack(
            rx.button(
                rx.hstack(
                    rx.icon("refresh_cw", size=18),
                    rx.text("Refresh data"),
                    rx.cond(
                        ClaimsState.is_loading_summary | ClaimsState.is_loading_claims,
                        rx.spinner(size="2"),
                        rx.fragment(),
                    ),
                    spacing="2",
                    align="center",
                ),
                on_click=ClaimsState.refresh_all_data,
                variant="outline",
                size="2",
            ),
            rx.spacer(),
            rx.badge(
                "Filters apply to all sections",
                variant="soft",
                color_scheme="blue",
            ),
            width="100%",
            align="center",
        ),
        spacing="6",
        width="100%",
    )


def _metrics_grid() -> rx.Component:
    """Contextual metric cards with drill-in CTAs."""
    return rx.cond(
        ClaimsState.is_loading_summary,
        rx.grid(
            skeleton_card(),
            skeleton_card(),
            skeleton_card(),
            skeleton_card(),
            columns="4",
            spacing="4",
            width="100%",
        ),
        rx.grid(
            metric_card(
                label="Total Claims",
                value=rx.vstack(
                    rx.text(
                        ClaimsState.total_claims,
                        size="8",
                        weight="bold",
                        color=COLORS["primary"],
                    ),
                    rx.text(
                        "Across selected time range",
                        size="2",
                        color=COLORS["gray_500"],
                    ),
                    spacing="1",
                    align="start",
                ),
                icon="file_text",
                color=COLORS["primary"],
                trend="+12%",
                trend_direction="up",
                cta_label="View all claims",
                on_click=lambda: ClaimsState.drill_into_status("all"),
            ),
            metric_card(
                label="Approved",
                value=rx.vstack(
                    rx.text(
                        ClaimsState.approved_count,
                        size="8",
                        weight="bold",
                        color=COLORS["success"],
                    ),
                    rx.text(
                        ClaimsState.approval_rate_label,
                        size="2",
                        color=COLORS["gray_500"],
                    ),
                    spacing="1",
                    align="start",
                ),
                icon="circle_check",
                color=COLORS["success"],
                trend="+8%",
                trend_direction="up",
                cta_label="Show approved",
                on_click=lambda: ClaimsState.drill_into_status("approved"),
            ),
            metric_card(
                label="Pending",
                value=rx.vstack(
                    rx.text(
                        ClaimsState.pending_count,
                        size="8",
                        weight="bold",
                        color=COLORS["warning"],
                    ),
                    rx.text(
                        "Investigate aging cases",
                        size="2",
                        color=COLORS["gray_500"],
                    ),
                    spacing="1",
                    align="start",
                ),
                icon="clock",
                color=COLORS["warning"],
                trend="-3%",
                trend_direction="down",
                cta_label="Review pending",
                on_click=lambda: ClaimsState.drill_into_status("pending"),
            ),
            metric_card(
                label="Flagged",
                value=rx.vstack(
                    rx.text(
                        ClaimsState.flagged_count,
                        size="8",
                        weight="bold",
                        color=COLORS["danger"],
                    ),
                    rx.text(
                        "Requires manual review",
                        size="2",
                        color=COLORS["gray_500"],
                    ),
                    spacing="1",
                    align="start",
                ),
                icon="triangle_alert",
                color=COLORS["danger"],
                trend="+5%",
                trend_direction="up",
                cta_label="Open flagged list",
                on_click=lambda: ClaimsState.drill_into_status("flagged"),
            ),
            columns="4",
            spacing="4",
            width="100%",
        ),
    )

def _analytics_section() -> rx.Component:
    """Analytics charts with contextual heading."""
    return rx.vstack(
        rx.hstack(
            rx.heading(
                "Analytics",
                size="6",
                class_name="text-gray-900",
            ),
            rx.badge(
                "Real-time snapshot",
                variant="soft",
                color_scheme="blue",
            ),
            spacing="3",
            align="center",
        ),
        rx.grid(
            claims_trend_chart(),
            rx.grid(
                risk_distribution_chart(),
                status_breakdown_chart(),
                columns="1",
                spacing="4",
                width="100%",
            ),
            columns="2",
            spacing="4",
            width="100%",
        ),
        spacing="4",
        width="100%",
    )


def _sidebar() -> rx.Component:
    """Left sidebar housing filters and data utilities."""
    return rx.vstack(
        rx.box(
            filters_panel(),
            class_name="bg-white rounded-2xl shadow-sm border border-gray-200 p-5 space-y-4",
            width="100%",
        ),
        rx.box(
            data_management_panel(),
            class_name="bg-white rounded-2xl shadow-sm border border-gray-200 p-5 space-y-4",
            width="100%",
        ),
        spacing="6",
        width="100%",
    )


def _main_column() -> rx.Component:
    """Primary dashboard column with metrics, charts, and table."""
    return rx.vstack(
        rx.cond(
            ClaimsState.error_message != "",
            rx.callout(
                ClaimsState.error_message,
                icon="triangle_alert",
                color_scheme="red",
                role="alert",
            ),
            rx.fragment(),
        ),
        rx.box(
            _global_controls(),
            class_name="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 space-y-6",
            width="100%",
        ),
        rx.box(
            _metrics_grid(),
            class_name="bg-white rounded-2xl shadow-sm border border-gray-200 p-6",
            width="100%",
        ),
        rx.box(
            _analytics_section(),
            class_name="bg-white rounded-2xl shadow-sm border border-gray-200 p-6",
            width="100%",
        ),
        claims_table(),
        spacing="6",
        width="100%",
    )


def dashboard() -> rx.Component:
    return rx.box(
        notification_toast(),
        claim_detail_modal(),
        rx.vstack(
            navbar(),
            rx.box(
                rx.box(
                    _sidebar(),
                    _main_column(),
                    class_name="grid gap-6 w-full lg:grid-cols-[280px_1fr]",
                ),
                class_name="px-4 py-8 md:px-6 lg:px-8 max-w-7xl mx-auto w-full",
            ),
            spacing="0",
            width="100%",
            class_name="w-full",
        ),
        class_name="min-h-screen bg-gray-50",
        on_mount=ClaimsState.load_all_data,
    )
