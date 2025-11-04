"""
Enhanced Claim Detail Modal for Dashboard V2

Two-column layout with clear action buttons (Approve/Deny/Flag).
Optimized for Claims Processor workflow.
"""
import reflex as rx
from claimsiq.theme import COLORS
from claimsiq.state import ClaimsState


def detail_row(label: str, value: rx.Component | str) -> rx.Component:
    """Single row in claim details"""
    return rx.hstack(
        rx.text(
            f"{label}:",
            size="2",
            weight="bold",
            color=COLORS["gray_700"],
            min_width="120px",
        ),
        value if isinstance(value, rx.Component) else rx.text(
            value,
            size="2",
            color=COLORS["gray_900"],
        ),
        spacing="3",
        margin_bottom="2",
    )


def claim_detail_modal_v2() -> rx.Component:
    """
    Enhanced claim details modal with:
    - Two-column layout
    - Clear action buttons (Approve/Deny/Flag)
    - Quick stats and provider history
    - Keyboard shortcuts (A=approve, D=deny, Esc=close)
    """
    claim = ClaimsState.selected_claim

    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                # Header
                rx.hstack(
                    rx.heading(
                        rx.text("Claim #", claim.get("id", ""), as_="span"),
                        size="6",
                        color=COLORS["gray_900"],
                    ),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.button(
                            rx.icon("x", size=20),
                            variant="ghost",
                            color_scheme="gray",
                            size="2",
                        ),
                    ),
                    width="100%",
                    align="center",
                    class_name="flex items-center justify-between w-full",
                    margin_bottom="4",
                ),

                # Two-column layout
                rx.grid(
                    # Left Column: Claim Details
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "Claim Details",
                                size="4",
                                color=COLORS["gray_900"],
                                margin_bottom="3",
                            ),

                            detail_row("Claim Amount", rx.text(
                                claim.get("claim_amount_formatted", "$0.00"),
                                size="3",
                                weight="bold",
                                color=COLORS["primary"],
                            )),
                            detail_row("Claim Date", claim.get("claim_date", "—")),
                            detail_row("Status", rx.match(
                                claim.get("status", "unknown"),
                                ("approved", rx.badge("Approved", color_scheme="green", variant="soft")),
                                ("pending", rx.badge("Pending", color_scheme="blue", variant="soft")),
                                ("denied", rx.badge("Denied", color_scheme="red", variant="soft")),
                                ("flagged", rx.badge("Flagged", color_scheme="orange", variant="soft")),
                                rx.badge("Unknown", color_scheme="gray", variant="soft"),
                            )),
                            detail_row("Provider", rx.cond(
                                claim.get("provider_name"),
                                claim.get("provider_name"),
                                rx.cond(
                                    claim.get("provider_id"),
                                    claim.get("provider_id"),
                                    "Unknown"
                                )
                            )),
                            detail_row("Patient ID", claim.get("patient_id", "—")),
                            detail_row("Procedure Code", claim.get("procedure_code", "—")),

                            rx.divider(margin_y="3"),

                            detail_row("Risk Score", rx.hstack(
                                rx.text(
                                    claim.get("risk_score", 0),
                                    size="3",
                                    weight="bold",
                                ),
                                rx.match(
                                    claim.get("ui_risk_level", "low"),
                                    ("high", rx.badge("HIGH RISK", color_scheme="red", variant="solid")),
                                    ("medium", rx.badge("MEDIUM", color_scheme="orange", variant="soft")),
                                    ("low", rx.badge("LOW", color_scheme="green", variant="soft")),
                                    rx.badge("LOW", color_scheme="green", variant="soft"),
                                ),
                                spacing="2",
                            )),

                            rx.cond(
                                claim.get("ui_has_reason", False),
                                rx.box(
                                    rx.text(
                                        "Risk Reason:",
                                        size="2",
                                        weight="bold",
                                        color=COLORS["gray_700"],
                                        margin_bottom="1",
                                    ),
                                    rx.text(
                                        claim.get("ui_risk_reason", ""),
                                        size="2",
                                        color=COLORS["danger"],
                                        class_name="bg-red-50 p-2 rounded border border-red-200",
                                    ),
                                    margin_top="2",
                                ),
                                rx.fragment(),
                            ),

                            spacing="0",
                            align="start",
                            width="100%",
                        ),
                        padding="4",
                        class_name="bg-gray-50 rounded-lg",
                    ),

                    # Right Column: Quick Stats
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "Quick Stats",
                                size="4",
                                color=COLORS["gray_900"],
                                margin_bottom="3",
                            ),

                            detail_row("Provider History", rx.text(
                                "First time filing",  # This would come from backend
                                size="2",
                                color=COLORS["gray_600"],
                                style={"font-style": "italic"},
                            )),

                            detail_row("Similar Claims", rx.text(
                                "None from this provider",  # This would come from backend
                                size="2",
                                color=COLORS["gray_600"],
                                style={"font-style": "italic"},
                            )),

                            detail_row("Days Pending", rx.hstack(
                                rx.text(
                                    claim.get('days_pending', 0),
                                    size="2",
                                    weight="medium",
                                ),
                                rx.text(
                                    "days",
                                    size="2",
                                    weight="medium",
                                ),
                                spacing="1",
                            )),

                            rx.divider(margin_y="3"),

                            rx.box(
                                rx.text(
                                    "Processor Notes",
                                    size="2",
                                    weight="bold",
                                    color=COLORS["gray_700"],
                                    margin_bottom="2",
                                ),
                                rx.text_area(
                                    placeholder="Add notes about this claim...",
                                    size="2",
                                    min_height="100px",
                                    class_name="w-full",
                                ),
                                width="100%",
                            ),

                            spacing="0",
                            align="start",
                            width="100%",
                        ),
                        padding="4",
                        class_name="bg-blue-50 rounded-lg",
                    ),

                    columns="2",
                    spacing="4",
                    width="100%",
                    margin_bottom="4",
                ),

                # Action Buttons Row
                rx.hstack(
                    rx.button(
                        rx.hstack(
                            rx.icon("circle-check", size=20),
                            rx.text("Approve", size="3", weight="bold"),
                            spacing="2",
                        ),
                        on_click=lambda: ClaimsState.approve_claim(ClaimsState.selected_claim_id),
                        color_scheme="green",
                        size="3",
                        class_name="flex-1",
                    ),

                    rx.button(
                        rx.hstack(
                            rx.icon("circle-x", size=20),
                            rx.text("Deny", size="3", weight="bold"),
                            spacing="2",
                        ),
                        on_click=lambda: ClaimsState.deny_claim(ClaimsState.selected_claim_id),
                        color_scheme="red",
                        size="3",
                        class_name="flex-1",
                    ),

                    rx.button(
                        rx.hstack(
                            rx.icon("flag", size=20),
                            rx.text("Flag for Review", size="3", weight="bold"),
                            spacing="2",
                        ),
                        on_click=lambda: ClaimsState.flag_claim(ClaimsState.selected_claim_id),
                        color_scheme="orange",
                        variant="outline",
                        size="3",
                        class_name="flex-1",
                    ),

                    spacing="3",
                    width="100%",
                    class_name="flex gap-3 w-full",
                ),

                spacing="0",
                width="100%",
            ),
            max_width="900px",
            padding="6",
            class_name="bg-white rounded-xl shadow-2xl",
        ),
        open=ClaimsState.show_claim_modal,
        on_open_change=ClaimsState.set_show_claim_modal,
    )
