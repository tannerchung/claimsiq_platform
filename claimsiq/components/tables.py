import reflex as rx
from claimsiq.theme import COLORS, FONT_SIZES, SPACING
from claimsiq.state import ClaimsState

def get_risk_color(risk_score: float) -> str:
    if risk_score >= 0.7:
        return COLORS["danger"]
    elif risk_score >= 0.4:
        return COLORS["warning"]
    return COLORS["success"]

def claims_table() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading("Claims", size="5"),
                rx.spacer(),
                rx.select(
                    ["all", "pending", "approved", "denied", "flagged"],
                    value=ClaimsState.selected_status,
                    on_change=lambda val: [
                        ClaimsState.set_status_filter(val),
                        ClaimsState.load_claims()
                    ],
                ),
                spacing="4",
                width="100%",
            ),
            rx.cond(
                ClaimsState.is_loading,
                rx.spinner(size="3"),
                rx.cond(
                    ClaimsState.claims_data.length() > 0,
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("Claim ID"),
                                rx.table.column_header_cell("Date"),
                                rx.table.column_header_cell("Amount"),
                                rx.table.column_header_cell("Status"),
                                rx.table.column_header_cell("Risk Score"),
                            )
                        ),
                        rx.table.body(
                            rx.foreach(
                                ClaimsState.claims_data,
                                lambda claim: rx.table.row(
                                    rx.table.cell(claim["id"]),
                                    rx.table.cell(claim["claim_date"]),
                                    rx.table.cell(f"${claim['claim_amount']:,.2f}"),
                                    rx.table.cell(
                                        rx.badge(claim["status"], variant="soft")
                                    ),
                                    rx.table.cell(
                                        rx.text(
                                            claim["risk_score"],
                                            weight="bold"
                                        )
                                    ),
                                )
                            )
                        ),
                        width="100%",
                    ),
                    rx.text("No claims data available", color=COLORS["gray"]),
                )
            ),
            spacing="4",
            width="100%",
        ),
        padding="4",
        background=COLORS["white"],
        border_radius="0.5rem",
        box_shadow="0 1px 3px 0 rgba(0, 0, 0, 0.1)",
        width="100%",
    )
