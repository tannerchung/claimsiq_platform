import reflex as rx
from claimsiq.theme import COLORS, SHADOWS
from claimsiq.state import ClaimsState
from claimsiq.components.tables import status_badge, risk_badge


def detail_row(label: str, value: rx.Component) -> rx.Component:
    """Row for claim detail display"""
    return rx.hstack(
        rx.text(
            label,
            size="2",
            weight="medium",
            class_name="text-gray-600 w-36",
        ),
        value,
        spacing="4",
        width="100%",
        align="center",
        class_name="flex items-center gap-4 w-full",
    )


def claim_detail_modal() -> rx.Component:
    """Modal for displaying claim details"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                # Header
                rx.hstack(
                    rx.heading(
                        f"Claim #{ClaimsState.selected_claim_id}",
                        size="6",
                        class_name="text-gray-900",
                    ),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.icon_button(
                            rx.icon("x", size=20),
                            variant="ghost",
                            class_name="text-gray-500",
                        ),
                    ),
                    width="100%",
                    align="center",
                    class_name="flex items-center justify-between w-full",
                ),

                rx.separator(),

                # Claim Details Grid
                rx.grid(
                    # Left column
                    rx.vstack(
                        detail_row(
                            "Claim ID",
                            rx.text(
                                ClaimsState.selected_claim["id"],
                                weight="bold",
                                color=COLORS["gray_900"],
                            ),
                        ),
                        detail_row(
                            "Date",
                            rx.text(
                                ClaimsState.selected_claim["claim_date"],
                                color=COLORS["gray_700"],
                            ),
                        ),
                        detail_row(
                            "Amount",
                            rx.text(
                                f"${ClaimsState.selected_claim['claim_amount']:,.2f}",
                                weight="bold",
                                color=COLORS["success"],
                                size="4",
                            ),
                        ),
                        spacing="3",
                        align="start",
                        width="100%",
                    ),

                    # Right column
                    rx.vstack(
                        detail_row(
                            "Status",
                            status_badge(ClaimsState.selected_claim["status"]),
                        ),
                        detail_row(
                            "Risk Score",
                            risk_badge(
                                ClaimsState.selected_claim["risk_score"],
                                ClaimsState.selected_claim["ui_risk_reason"],
                                ClaimsState.selected_claim["ui_has_reason"],
                            ),
                        ),
                        detail_row(
                            "Patient",
                            rx.text(
                                ClaimsState.selected_claim.get("patient_name", "N/A"),
                                color=COLORS["gray_700"],
                            ),
                        ),
                        spacing="3",
                        align="start",
                        width="100%",
                    ),

                    columns="2",
                    spacing="6",
                    width="100%",
                ),

                rx.separator(),

                # Additional Information Section
                rx.vstack(
                    rx.heading("Additional Information", size="4", color=COLORS["gray_900"]),
                    rx.box(
                        rx.vstack(
                            detail_row(
                                "Provider",
                                rx.text(
                                    ClaimsState.selected_claim.get("provider_name", "N/A"),
                                    color=COLORS["gray_700"],
                                ),
                            ),
                            detail_row(
                                "Diagnosis Code",
                                rx.badge(
                                    ClaimsState.selected_claim.get("diagnosis_code", "N/A"),
                                    variant="outline",
                                ),
                            ),
                            detail_row(
                                "Service Type",
                                rx.text(
                                    ClaimsState.selected_claim.get("service_type", "N/A"),
                                    color=COLORS["gray_700"],
                                ),
                            ),
                            spacing="3",
                            width="100%",
                        ),
                        padding="4",
                        background=COLORS["gray_50"],
                        border_radius="0.5rem",
                        width="100%",
                    ),
                    spacing="3",
                    width="100%",
                ),

                rx.separator(),

                # Action Buttons
                rx.hstack(
                    rx.button(
                        rx.hstack(
                            rx.icon("circle_check", size=18),
                            rx.text("Approve"),
                            spacing="2",
                        ),
                        color_scheme="green",
                        size="3",
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon("circle_x", size=18),
                            rx.text("Deny"),
                            spacing="2",
                        ),
                        color_scheme="red",
                        variant="outline",
                        size="3",
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon("flag", size=18),
                            rx.text("Flag for Review"),
                            spacing="2",
                        ),
                        color_scheme="orange",
                        variant="outline",
                        size="3",
                    ),
                    spacing="3",
                    width="100%",
                ),

                spacing="5",
                width="100%",
            ),
            max_width="800px",
            padding="6",
        ),
        open=ClaimsState.show_claim_modal,
        on_open_change=ClaimsState.set_show_claim_modal,
    )
