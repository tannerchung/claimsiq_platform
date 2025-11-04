"""
Enhanced Claim Detail Modal for Dashboard V2

Two-column layout with clear action buttons (Approve/Deny/Flag).
Optimized for Claims Processor workflow.
"""
import reflex as rx
from claimsiq.theme import COLORS
from claimsiq.state import ClaimsState


def detail_row(label: str, value: rx.Component) -> rx.Component:
    """Single row in claim details."""
    return rx.hstack(
        rx.text(
            f"{label}:",
            size="2",
            weight="bold",
            color=COLORS["gray_700"],
            min_width="120px",
        ),
        value,
        spacing="3",
        margin_bottom="2",
        align="center",
    )


def claim_detail_modal_v2() -> rx.Component:
    """
    Enhanced claim details modal with:
    - Two-column layout
    - Clear action buttons (Approve/Deny/Flag)
    - Quick stats and provider history
    - Keyboard shortcuts (A=approve, D=deny, Esc=close)
    """
    return rx.dialog.root(
        rx.dialog.content(
            rx.cond(
                ClaimsState.has_modal_claim,
                rx.vstack(
                    # Header
                    rx.hstack(
                        rx.heading(
                            rx.text(
                                "Claim #",
                                ClaimsState.modal_claim["id"],
                                as_="span",
                            ),
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
                                detail_row(
                                    "Claim Amount",
                                    rx.text(
                                        ClaimsState.modal_claim["claim_amount_formatted"],
                                        size="3",
                                        weight="bold",
                                        color=COLORS["primary"],
                                    ),
                                ),
                                detail_row(
                                    "Approved Amount",
                                    rx.text(
                                        ClaimsState.modal_claim["approved_amount_formatted"],
                                        size="2",
                                        color=COLORS["gray_900"],
                                    ),
                                ),
                                detail_row(
                                    "Claim Date",
                                    rx.text(
                                        ClaimsState.modal_claim["claim_date"],
                                        size="2",
                                        color=COLORS["gray_900"],
                                    ),
                                ),
                               detail_row(
                                   "Status",
                                   rx.match(
                                       ClaimsState.modal_claim["status"],
                                       (
                                           "approved",
                                           rx.badge("Approved", color_scheme="green", variant="soft"),
                                       ),
                                        (
                                            "pending",
                                            rx.badge("Pending", color_scheme="blue", variant="soft"),
                                        ),
                                        (
                                            "denied",
                                            rx.badge("Denied", color_scheme="red", variant="soft"),
                                        ),
                                        (
                                            "flagged",
                                            rx.badge("Flagged", color_scheme="orange", variant="soft"),
                                       ),
                                       rx.badge("Unknown", color_scheme="gray", variant="soft"),
                                   ),
                               ),
                                rx.cond(
                                    ClaimsState.modal_claim.get("denial_reason"),
                                    detail_row(
                                        "Reason",
                                        rx.text(
                                            ClaimsState.modal_claim["denial_reason"],
                                            size="2",
                                            color=COLORS["danger"],
                                        ),
                                    ),
                                    rx.fragment(),
                                ),
                                detail_row(
                                    "Provider",
                                    rx.text(
                                        ClaimsState.modal_claim["provider_name"],
                                        size="2",
                                        color=COLORS["gray_900"],
                                    ),
                                ),
                                detail_row(
                                    "Patient ID",
                                    rx.text(
                                        ClaimsState.modal_claim["patient_id"],
                                        size="2",
                                        color=COLORS["gray_900"],
                                    ),
                                ),
                                detail_row(
                                    "Procedure Code",
                                    rx.text(
                                        ClaimsState.modal_claim["procedure_code"],
                                        size="2",
                                        color=COLORS["gray_900"],
                                    ),
                                ),

                                rx.divider(margin_y="3"),

                                detail_row(
                                    "Risk Score",
                                    rx.hstack(
                                        rx.text(
                                            ClaimsState.modal_claim["risk_score"],
                                            size="3",
                                            weight="bold",
                                        ),
                                        rx.match(
                                            ClaimsState.modal_claim["ui_risk_level"],
                                            (
                                                "high",
                                                rx.badge(
                                                    "HIGH RISK",
                                                    color_scheme="red",
                                                    variant="solid",
                                                ),
                                            ),
                                            (
                                                "medium",
                                                rx.badge(
                                                    "MEDIUM",
                                                    color_scheme="orange",
                                                    variant="soft",
                                                ),
                                            ),
                                            (
                                                "low",
                                                rx.badge(
                                                    "LOW",
                                                    color_scheme="green",
                                                    variant="soft",
                                                ),
                                            ),
                                            rx.badge("LOW", color_scheme="green", variant="soft"),
                                        ),
                                        spacing="2",
                                        align="center",
                                    ),
                                ),
                                rx.cond(
                                    ClaimsState.modal_claim["ui_has_reason"],
                                    rx.box(
                                        rx.text(
                                            "Risk Reason:",
                                            size="2",
                                            weight="bold",
                                            color=COLORS["gray_700"],
                                            margin_bottom="1",
                                        ),
                                        rx.text(
                                            ClaimsState.modal_claim["ui_risk_reason"],
                                            size="2",
                                            color=COLORS["danger"],
                                            class_name="bg-red-50 p-2 rounded border border-red-200",
                                        ),
                                        margin_top="2",
                                        width="100%",
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
                                detail_row(
                                    "Provider History",
                                    rx.text(
                                        ClaimsState.modal_quick_stats["provider_summary"],
                                        size="2",
                                        color=COLORS["gray_600"],
                                    ),
                                ),
                                detail_row(
                                    "Similar Claims",
                                    rx.text(
                                        ClaimsState.modal_quick_stats["similar_summary"],
                                        size="2",
                                        color=COLORS["gray_600"],
                                    ),
                                ),
                                detail_row(
                                    "Processing Time",
                                    rx.text(
                                        ClaimsState.modal_quick_stats["days_pending_label"],
                                        size="2",
                                        color=COLORS["gray_900"],
                                        weight="medium",
                                    ),
                                ),

                                rx.divider(margin_y="3"),

                                rx.box(
                                    rx.text(
                                        "Processor Notes",
                                        size="2",
                                        weight="bold",
                                        color=COLORS["gray_700"],
                                        margin_bottom="2",
                                    ),
                                    rx.vstack(
                                        rx.text_area(
                                            placeholder="Add notes about this claim...",
                                            size="2",
                                            min_height="100px",
                                            class_name="w-full",
                                            value=ClaimsState.modal_notes,
                                            on_change=ClaimsState.set_modal_notes,
                                        ),
                                        rx.hstack(
                                            rx.button(
                                                rx.cond(
                                                    ClaimsState.is_saving_notes,
                                                    rx.hstack(
                                                        rx.spinner(size="3"),
                                                        rx.text("Saving", size="2"),
                                                        spacing="2",
                                                        align="center",
                                                    ),
                                                    rx.hstack(
                                                        rx.icon("edit", size=16),
                                                        rx.text("Save Notes", size="2"),
                                                        spacing="2",
                                                        align="center",
                                                    ),
                                                ),
                                                on_click=ClaimsState.save_modal_notes,
                                                disabled=ClaimsState.is_saving_notes,
                                                size="2",
                                                color_scheme="blue",
                                            ),
                                            spacing="2",
                                            width="100%",
                                            class_name="flex justify-end w-full",
                                        ),
                                        spacing="3",
                                        width="100%",
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

                        columns="1",
                        class_name="grid gap-4 w-full md:grid-cols-2",
                        spacing="4",
                        width="100%",
                        margin_bottom="4",
                    ),

                    # Action Buttons Row
                    rx.hstack(
                        rx.button(
                            rx.hstack(
                                rx.cond(
                                    ClaimsState.is_processing_claim,
                                    rx.spinner(size="3"),
                                    rx.icon("circle-check", size=20),
                                ),
                                rx.text("Approve", size="3", weight="bold"),
                                spacing="2",
                            ),
                            on_click=lambda: ClaimsState.approve_claim(ClaimsState.selected_claim_id),
                            color_scheme="green",
                            size="3",
                            class_name="flex-1",
                            disabled=ClaimsState.is_processing_claim,
                        ),
                        rx.button(
                            rx.hstack(
                                rx.cond(
                                    ClaimsState.is_processing_claim,
                                    rx.spinner(size="3"),
                                    rx.icon("circle-x", size=20),
                                ),
                                rx.text("Deny", size="3", weight="bold"),
                                spacing="2",
                            ),
                            on_click=lambda: ClaimsState.deny_claim(ClaimsState.selected_claim_id),
                            color_scheme="red",
                            size="3",
                            class_name="flex-1",
                            disabled=ClaimsState.is_processing_claim,
                        ),
                        rx.button(
                            rx.hstack(
                                rx.cond(
                                    ClaimsState.is_processing_claim,
                                    rx.spinner(size="3"),
                                    rx.icon("flag", size=20),
                                ),
                                rx.text("Flag for Review", size="3", weight="bold"),
                                spacing="2",
                            ),
                            on_click=lambda: ClaimsState.flag_claim(ClaimsState.selected_claim_id),
                            color_scheme="orange",
                            variant="outline",
                            size="3",
                            class_name="flex-1",
                            disabled=ClaimsState.is_processing_claim,
                        ),
                        spacing="3",
                        width="100%",
                        class_name="flex gap-3 w-full flex-col md:flex-row",
                    ),

                    spacing="4",
                    width="100%",
                ),
                rx.center(
                    rx.text(
                        "Select a claim from the table to view its details.",
                        size="2",
                        color=COLORS["gray_600"],
                    ),
                    padding="6",
                    width="100%",
                ),
            ),
            max_width="900px",
            padding="6",
            class_name="bg-white rounded-xl shadow-2xl",
        ),
        open=ClaimsState.show_claim_modal,
        on_open_change=ClaimsState.set_show_claim_modal,
    )
