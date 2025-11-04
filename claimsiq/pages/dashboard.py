import reflex as rx
from claimsiq.state import ClaimsState
from claimsiq.components.cards import metric_card
from claimsiq.components.navbar import navbar
from claimsiq.components.tables import claims_table
from claimsiq.components.charts import claims_trend_chart, risk_distribution_chart, status_breakdown_chart
from claimsiq.theme import COLORS, SPACING

def dashboard() -> rx.Component:
    return rx.box(
        rx.vstack(
            navbar(),
            rx.box(
                rx.vstack(
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
                    rx.heading("Dashboard", size="8", color=COLORS["gray_900"]),
                    rx.grid(
                        metric_card(
                            label="Total Claims",
                            value=rx.text(
                                ClaimsState.total_claims,
                                size="8",
                                weight="bold",
                                color=COLORS["primary"]
                            ),
                            icon="file-text",
                            color=COLORS["primary"],
                            trend="+12%",
                            trend_direction="up"
                        ),
                        metric_card(
                            label="Approved",
                            value=rx.text(
                                ClaimsState.approved_count,
                                size="8",
                                weight="bold",
                                color=COLORS["success"]
                            ),
                            icon="check-circle",
                            color=COLORS["success"],
                            trend="+8%",
                            trend_direction="up"
                        ),
                        metric_card(
                            label="Pending",
                            value=rx.text(
                                ClaimsState.pending_count,
                                size="8",
                                weight="bold",
                                color=COLORS["warning"]
                            ),
                            icon="clock",
                            color=COLORS["warning"],
                            trend="-3%",
                            trend_direction="down"
                        ),
                        metric_card(
                            label="Flagged",
                            value=rx.text(
                                ClaimsState.flagged_count,
                                size="8",
                                weight="bold",
                                color=COLORS["danger"]
                            ),
                            icon="alert-triangle",
                            color=COLORS["danger"],
                            trend="+5%",
                            trend_direction="up"
                        ),
                        columns="4",
                        spacing="4",
                        width="100%",
                    ),

                    # Analytics Charts Section
                    rx.heading(
                        "Analytics",
                        size="6",
                        color=COLORS["gray_900"],
                        margin_top="4",
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

                    # Claims Table Section
                    claims_table(),

                    spacing="6",
                    width="100%",
                ),
                padding="8",
                max_width="1400px",
                margin="0 auto",
            ),
            spacing="0",
            width="100%",
        ),
        background=COLORS["bg_secondary"],
        min_height="100vh",
        on_mount=ClaimsState.load_all_data,
    )
