import reflex as rx
from claimsiq.theme import COLORS, FONT_SIZES, SPACING, SHADOWS
from claimsiq.state import ClaimsState

def get_risk_color(risk_score: float) -> str:
    if risk_score >= 0.7:
        return COLORS["danger"]
    elif risk_score >= 0.4:
        return COLORS["warning"]
    return COLORS["success"]

def risk_badge(risk_score: float) -> rx.Component:
    """Visual risk indicator with color, icon, and label"""
    return rx.cond(
        risk_score >= 0.7,
        rx.badge(
            rx.hstack(
                rx.icon("alert-triangle", size=14),
                rx.text(f"{risk_score:.2f}", size="2", weight="medium"),
                spacing="1",
                align="center",
            ),
            color_scheme="red",
            variant="solid",
        ),
        rx.cond(
            risk_score >= 0.4,
            rx.badge(
                rx.hstack(
                    rx.icon("alert-circle", size=14),
                    rx.text(f"{risk_score:.2f}", size="2", weight="medium"),
                    spacing="1",
                    align="center",
                ),
                color_scheme="orange",
                variant="soft",
            ),
            rx.badge(
                rx.hstack(
                    rx.icon("check-circle", size=14),
                    rx.text(f"{risk_score:.2f}", size="2", weight="medium"),
                    spacing="1",
                    align="center",
                ),
                color_scheme="green",
                variant="soft",
            ),
        ),
    )

def status_badge(status: str) -> rx.Component:
    """Color-coded status badges"""
    # Color mapping for different statuses
    return rx.match(
        status,
        ("approved", rx.badge(status.capitalize(), color_scheme="green", variant="soft")),
        ("pending", rx.badge(status.capitalize(), color_scheme="blue", variant="soft")),
        ("denied", rx.badge(status.capitalize(), color_scheme="red", variant="soft")),
        ("flagged", rx.badge(status.capitalize(), color_scheme="orange", variant="soft")),
        rx.badge(status.capitalize(), color_scheme="gray", variant="soft"),
    )

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
                                    rx.table.cell(
                                        rx.text(claim["id"], weight="medium")
                                    ),
                                    rx.table.cell(claim["claim_date"]),
                                    rx.table.cell(
                                        rx.text(
                                            f"${claim['claim_amount']:,.2f}",
                                            weight="medium",
                                        )
                                    ),
                                    rx.table.cell(
                                        status_badge(claim["status"])
                                    ),
                                    rx.table.cell(
                                        risk_badge(claim["risk_score"])
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
        padding="5",
        background=COLORS["white"],
        border_radius="0.75rem",
        box_shadow=SHADOWS["md"],
        width="100%",
    )
