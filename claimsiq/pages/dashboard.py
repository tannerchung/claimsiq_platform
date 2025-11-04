import reflex as rx
from claimsiq.state import ClaimsState
from claimsiq.components.cards import metric_card
from claimsiq.components.navbar import navbar
from claimsiq.components.tables import claims_table
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
                    rx.heading("Dashboard", size="8"),
                    rx.grid(
                        metric_card(
                            "Total Claims",
                            rx.text(ClaimsState.total_claims),
                            COLORS["primary"]
                        ),
                        metric_card(
                            "Approved",
                            rx.text(ClaimsState.approved_count),
                            COLORS["success"]
                        ),
                        metric_card(
                            "Pending",
                            rx.text(ClaimsState.pending_count),
                            COLORS["warning"]
                        ),
                        metric_card(
                            "Flagged",
                            rx.text(ClaimsState.flagged_count),
                            COLORS["danger"]
                        ),
                        columns="4",
                        spacing="4",
                        width="100%",
                    ),
                    claims_table(),
                    spacing="6",
                    width="100%",
                ),
                padding="6",
                max_width="1400px",
                margin="0 auto",
            ),
            spacing="0",
            width="100%",
        ),
        background=COLORS["light_gray"],
        min_height="100vh",
        on_mount=ClaimsState.load_all_data,
    )
