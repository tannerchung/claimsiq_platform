"""
Enhanced Dark Mode Claim Detail Modal

Improvements:
- Proper heading hierarchy (h1, h2, h3)
- Color-coded badges for status and risk
- Clear visual sectioning with borders and cards
- Muted styling for empty/unavailable fields
- Labeled notes textarea
- Grouped quick stats with borders
- High contrast for dark mode
- Keyboard accessibility
- Responsive design
"""
import reflex as rx
from claimsiq.theme import DARK_COLORS, DARK_SHADOWS
from claimsiq.state import ClaimsState


def dark_detail_field(label: str, value: rx.Component | str, is_empty: bool = False) -> rx.Component:
    """
    Single field in claim details with proper labeling

    Args:
        label: Field label
        value: Field value (component or string)
        is_empty: Whether the field is empty/unavailable (applies muted styling)
    """
    return rx.box(
        rx.vstack(
            rx.text(
                label,
                size="1",
                weight="bold",
                style={
                    "color": DARK_COLORS["text_tertiary"],
                    "text-transform": "uppercase",
                    "letter-spacing": "0.05em",
                },
            ),
            rx.cond(
                is_empty,
                # Empty state styling
                rx.text(
                    value if isinstance(value, str) else "—",
                    size="3",
                    style={
                        "color": DARK_COLORS["text_disabled"],
                        "font-style": "italic",
                    },
                ),
                # Normal value
                value if isinstance(value, rx.Component) else rx.text(
                    value,
                    size="3",
                    weight="medium",
                    style={"color": DARK_COLORS["text_primary"]},
                ),
            ),
            spacing="1",
            align="start",
            width="100%",
        ),
        style={
            "padding": "12px",
            "background": DARK_COLORS["bg_elevated"],
            "border-radius": "8px",
            "border": f"1px solid {DARK_COLORS['border']}",
        },
        width="100%",
    )


def dark_info_card(heading: str, children: list) -> rx.Component:
    """Card for grouping related information"""
    return rx.box(
        rx.vstack(
            # Section heading (h3 level)
            rx.heading(
                heading,
                size="4",
                as_="h3",
                style={
                    "color": DARK_COLORS["text_primary"],
                    "margin-bottom": "16px",
                },
            ),
            *children,
            spacing="3",
            align="start",
            width="100%",
        ),
        style={
            "padding": "20px",
            "background": DARK_COLORS["bg_card"],
            "border-radius": "12px",
            "border": f"1px solid {DARK_COLORS['border']}",
            "box-shadow": DARK_SHADOWS["md"],
        },
        width="100%",
    )


def claim_detail_modal_dark() -> rx.Component:
    """
    Enhanced dark mode claim details modal with:
    - Proper semantic heading hierarchy (h1, h2, h3)
    - Color-coded status and risk badges
    - Clear visual sectioning with cards and borders
    - Muted styling for empty fields
    - Labeled textarea for notes
    - High contrast for accessibility
    - Keyboard navigation support
    - Responsive layout
    """
    claim = ClaimsState.selected_claim

    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                # Modal Header (h1 level)
                rx.hstack(
                    rx.heading(
                        rx.text("Claim #", claim.get("id", "N/A"), as_="span"),
                        size="7",
                        as_="h1",
                        style={"color": DARK_COLORS["text_primary"]},
                    ),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.button(
                            rx.icon("x", size=20),
                            variant="ghost",
                            size="2",
                            style={
                                "color": DARK_COLORS["text_secondary"],
                                "_hover": {"background": DARK_COLORS["bg_elevated"]},
                            },
                            aria_label="Close dialog",
                        ),
                    ),
                    width="100%",
                    align="center",
                    style={"margin-bottom": "24px"},
                ),

                # Two-column layout
                rx.grid(
                    # Left Column: Claim Details
                    dark_info_card(
                        "Claim Information",
                        [
                            # Claim Amount - emphasized
                            rx.box(
                                rx.vstack(
                                    rx.text(
                                        "Claim Amount",
                                        size="1",
                                        weight="bold",
                                        style={
                                            "color": DARK_COLORS["text_tertiary"],
                                            "text-transform": "uppercase",
                                            "letter-spacing": "0.05em",
                                        },
                                    ),
                                    rx.text(
                                        claim.get("claim_amount_formatted", "$0.00"),
                                        size="7",
                                        weight="bold",
                                        style={"color": DARK_COLORS["primary"]},
                                    ),
                                    spacing="1",
                                    align="start",
                                ),
                                style={
                                    "padding": "16px",
                                    "background": f"linear-gradient(135deg, {DARK_COLORS['primary_bg']}, {DARK_COLORS['bg_elevated']})",
                                    "border-radius": "8px",
                                    "border": f"1px solid {DARK_COLORS['primary']}",
                                },
                                width="100%",
                            ),

                            # Status - color-coded badge
                            rx.box(
                                rx.vstack(
                                    rx.text(
                                        "Status",
                                        size="1",
                                        weight="bold",
                                        style={
                                            "color": DARK_COLORS["text_tertiary"],
                                            "text-transform": "uppercase",
                                            "letter-spacing": "0.05em",
                                        },
                                    ),
                                    rx.match(
                                        claim.get("status", "unknown"),
                                        ("approved", rx.badge(
                                            rx.hstack(
                                                rx.icon("circle-check", size=16),
                                                rx.text("Approved", weight="bold"),
                                                spacing="2",
                                            ),
                                            color_scheme="green",
                                            variant="solid",
                                            size="2",
                                        )),
                                        ("pending", rx.badge(
                                            rx.hstack(
                                                rx.icon("clock", size=16),
                                                rx.text("Pending Review", weight="bold"),
                                                spacing="2",
                                            ),
                                            color_scheme="blue",
                                            variant="solid",
                                            size="2",
                                        )),
                                        ("denied", rx.badge(
                                            rx.hstack(
                                                rx.icon("circle-x", size=16),
                                                rx.text("Denied", weight="bold"),
                                                spacing="2",
                                            ),
                                            color_scheme="red",
                                            variant="solid",
                                            size="2",
                                        )),
                                        ("flagged", rx.badge(
                                            rx.hstack(
                                                rx.icon("flag", size=16),
                                                rx.text("Flagged", weight="bold"),
                                                spacing="2",
                                            ),
                                            color_scheme="orange",
                                            variant="solid",
                                            size="2",
                                        )),
                                        rx.badge(
                                            rx.text("Unknown", weight="bold"),
                                            color_scheme="gray",
                                            variant="soft",
                                            size="2",
                                        ),
                                    ),
                                    spacing="2",
                                    align="start",
                                ),
                                style={
                                    "padding": "12px",
                                    "background": DARK_COLORS["bg_elevated"],
                                    "border-radius": "8px",
                                    "border": f"1px solid {DARK_COLORS['border']}",
                                },
                                width="100%",
                            ),

                            # Risk Score - color-coded with emphasis
                            rx.box(
                                rx.vstack(
                                    rx.text(
                                        "Risk Assessment",
                                        size="1",
                                        weight="bold",
                                        style={
                                            "color": DARK_COLORS["text_tertiary"],
                                            "text-transform": "uppercase",
                                            "letter-spacing": "0.05em",
                                        },
                                    ),
                                    rx.hstack(
                                        rx.text(
                                            claim.get("risk_score", 0),
                                            size="6",
                                            weight="bold",
                                            style={"color": DARK_COLORS["text_primary"]},
                                        ),
                                        rx.match(
                                            claim.get("ui_risk_level", "low"),
                                            ("high", rx.badge(
                                                rx.hstack(
                                                    rx.icon("triangle-alert", size=14),
                                                    rx.text("HIGH RISK", weight="bold"),
                                                    spacing="1",
                                                ),
                                                color_scheme="red",
                                                variant="solid",
                                                size="2",
                                            )),
                                            ("medium", rx.badge(
                                                rx.hstack(
                                                    rx.icon("circle-alert", size=14),
                                                    rx.text("MEDIUM", weight="bold"),
                                                    spacing="1",
                                                ),
                                                color_scheme="orange",
                                                variant="solid",
                                                size="2",
                                            )),
                                            ("low", rx.badge(
                                                rx.hstack(
                                                    rx.icon("shield-check", size=14),
                                                    rx.text("LOW RISK", weight="bold"),
                                                    spacing="1",
                                                ),
                                                color_scheme="green",
                                                variant="soft",
                                                size="2",
                                            )),
                                            rx.badge("LOW RISK", color_scheme="green", variant="soft", size="2"),
                                        ),
                                        spacing="3",
                                        align="center",
                                    ),
                                    # Risk reason if present
                                    rx.cond(
                                        claim.get("ui_has_reason", False),
                                        rx.box(
                                            rx.hstack(
                                                rx.icon("info", size=16, color=DARK_COLORS["danger"]),
                                                rx.text(
                                                    claim.get("ui_risk_reason", ""),
                                                    size="2",
                                                    style={"color": DARK_COLORS["danger"]},
                                                ),
                                                spacing="2",
                                                align="start",
                                            ),
                                            style={
                                                "margin-top": "8px",
                                                "padding": "8px 12px",
                                                "background": DARK_COLORS["danger_bg"],
                                                "border-radius": "6px",
                                                "border": f"1px solid {DARK_COLORS['danger']}",
                                            },
                                        ),
                                        rx.fragment(),
                                    ),
                                    spacing="2",
                                    align="start",
                                    width="100%",
                                ),
                                style={
                                    "padding": "16px",
                                    "background": DARK_COLORS["bg_elevated"],
                                    "border-radius": "8px",
                                    "border": f"1px solid {DARK_COLORS['border']}",
                                },
                                width="100%",
                            ),

                            rx.box(height="8px"),  # Spacer

                            # Other claim details
                            dark_detail_field(
                                "Claim Date",
                                claim.get("claim_date", "Not available"),
                                is_empty=claim.get("claim_date", "") == "",
                            ),
                            dark_detail_field(
                                "Provider ID",
                                claim.get("provider_id", "Unknown provider"),
                                is_empty=False,
                            ),
                            dark_detail_field(
                                "Patient Info",
                                rx.hstack(
                                    rx.text(f"Age {claim.get('patient_age', 'N/A')}", size="2"),
                                    rx.text("•", size="2", style={"color": DARK_COLORS["text_tertiary"]}),
                                    rx.cond(
                                        claim.get('patient_gender') == 'M',
                                        rx.text("Male", size="2"),
                                        rx.text("Female", size="2"),
                                    ),
                                    rx.text("•", size="2", style={"color": DARK_COLORS["text_tertiary"]}),
                                    rx.text(claim.get("patient_state", "N/A"), size="2"),
                                    spacing="2",
                                ),
                                is_empty=False,
                            ),
                            dark_detail_field(
                                "Procedure",
                                rx.vstack(
                                    rx.text(claim.get("procedure_codes", "Not specified"), weight="bold", size="2"),
                                    rx.text(claim.get("procedure_description", ""), size="2", style={"color": DARK_COLORS["text_secondary"]}),
                                    spacing="1",
                                    align="start",
                                ),
                                is_empty=False,
                            ),
                            dark_detail_field(
                                "Diagnosis",
                                rx.vstack(
                                    rx.text(claim.get("diagnosis_code", "Not specified"), weight="bold", size="2"),
                                    rx.text(claim.get("diagnosis_description", ""), size="2", style={"color": DARK_COLORS["text_secondary"]}),
                                    spacing="1",
                                    align="start",
                                ),
                                is_empty=False,
                            ),
                        ],
                    ),

                    # Right Column: Quick Stats & Notes
                    rx.vstack(
                        dark_info_card(
                            "Quick Statistics",
                            [
                                # Days pending with visual indicator
                                rx.box(
                                    rx.hstack(
                                        rx.box(
                                            rx.icon("calendar", size=28, color=DARK_COLORS["primary"]),
                                            style={
                                                "padding": "12px",
                                                "background": DARK_COLORS["primary_bg"],
                                                "border-radius": "8px",
                                            },
                                        ),
                                        rx.vstack(
                                            rx.text(
                                                rx.cond(
                                                    claim.get('status') == 'pending',
                                                    "Days Pending",
                                                    "Days to Process",
                                                ),
                                                size="1",
                                                weight="bold",
                                                style={"color": DARK_COLORS["text_tertiary"]},
                                            ),
                                            rx.text(
                                                rx.cond(
                                                    claim.get('days_to_process'),
                                                    rx.text(claim.get('days_to_process', 0), " days", as_="span"),
                                                    "Pending review",
                                                ),
                                                size="4",
                                                weight="bold",
                                                style={"color": DARK_COLORS["text_primary"]},
                                            ),
                                            spacing="0",
                                            align="start",
                                        ),
                                        spacing="3",
                                        align="center",
                                    ),
                                    style={
                                        "padding": "16px",
                                        "background": DARK_COLORS["bg_elevated"],
                                        "border-radius": "8px",
                                        "border": f"1px solid {DARK_COLORS['border']}",
                                    },
                                    width="100%",
                                ),

                                # Provider history
                                rx.box(
                                    rx.vstack(
                                        rx.hstack(
                                            rx.icon("building", size=16, color=DARK_COLORS["text_secondary"]),
                                            rx.text(
                                                "Provider History",
                                                size="1",
                                                weight="bold",
                                                style={"color": DARK_COLORS["text_tertiary"]},
                                            ),
                                            spacing="2",
                                        ),
                                        rx.text(
                                            "First time filing",
                                            size="2",
                                            style={
                                                "color": DARK_COLORS["text_disabled"],
                                                "font-style": "italic",
                                            },
                                        ),
                                        spacing="2",
                                        align="start",
                                    ),
                                    style={
                                        "padding": "12px",
                                        "background": DARK_COLORS["bg_elevated"],
                                        "border-radius": "8px",
                                        "border": f"1px solid {DARK_COLORS['border']}",
                                    },
                                    width="100%",
                                ),

                                # Similar claims
                                rx.box(
                                    rx.vstack(
                                        rx.hstack(
                                            rx.icon("file-stack", size=16, color=DARK_COLORS["text_secondary"]),
                                            rx.text(
                                                "Similar Claims",
                                                size="1",
                                                weight="bold",
                                                style={"color": DARK_COLORS["text_tertiary"]},
                                            ),
                                            spacing="2",
                                        ),
                                        rx.text(
                                            "None from this provider",
                                            size="2",
                                            style={
                                                "color": DARK_COLORS["text_disabled"],
                                                "font-style": "italic",
                                            },
                                        ),
                                        spacing="2",
                                        align="start",
                                    ),
                                    style={
                                        "padding": "12px",
                                        "background": DARK_COLORS["bg_elevated"],
                                        "border-radius": "8px",
                                        "border": f"1px solid {DARK_COLORS['border']}",
                                    },
                                    width="100%",
                                ),
                            ],
                        ),

                        # Processor Notes Card
                        dark_info_card(
                            "Processor Notes",
                            [
                                rx.box(
                                    rx.vstack(
                                        rx.text(
                                            "Add your review notes below:",
                                            size="2",
                                            style={"color": DARK_COLORS["text_secondary"]},
                                        ),
                                        rx.text_area(
                                            placeholder="Enter detailed notes about this claim review...",
                                            size="2",
                                            style={
                                                "min-height": "120px",
                                                "background": DARK_COLORS["bg_primary"],
                                                "border-color": DARK_COLORS["border"],
                                                "color": DARK_COLORS["text_primary"],
                                                "_focus": {
                                                    "border-color": DARK_COLORS["primary"],
                                                    "box-shadow": f"0 0 0 1px {DARK_COLORS['primary']}",
                                                },
                                            },
                                            aria_label="Processor notes for this claim",
                                        ),
                                        spacing="2",
                                        width="100%",
                                    ),
                                    width="100%",
                                ),
                            ],
                        ),

                        spacing="4",
                        width="100%",
                    ),

                    columns="2",
                    spacing="5",
                    width="100%",
                    style={"margin-bottom": "24px"},
                ),

                # Action Buttons - Clear visual hierarchy
                rx.box(
                    rx.vstack(
                        rx.text(
                            "Review Actions",
                            size="2",
                            weight="bold",
                            style={
                                "color": DARK_COLORS["text_secondary"],
                                "margin-bottom": "8px",
                            },
                        ),
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
                                style={
                                    "flex": "1",
                                    "padding": "16px 24px",
                                    "_hover": {"transform": "translateY(-2px)"},
                                },
                                aria_label="Approve this claim",
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
                                style={
                                    "flex": "1",
                                    "padding": "16px 24px",
                                    "_hover": {"transform": "translateY(-2px)"},
                                },
                                aria_label="Deny this claim",
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
                                style={
                                    "flex": "1",
                                    "padding": "16px 24px",
                                    "border-width": "2px",
                                    "_hover": {"transform": "translateY(-2px)"},
                                },
                                aria_label="Flag this claim for further review",
                            ),

                            spacing="4",
                            width="100%",
                        ),
                        spacing="0",
                        width="100%",
                    ),
                    style={
                        "padding": "20px",
                        "background": DARK_COLORS["bg_elevated"],
                        "border-radius": "12px",
                        "border": f"1px solid {DARK_COLORS['border']}",
                    },
                    width="100%",
                ),

                spacing="0",
                width="100%",
            ),
            max_width="1000px",
            style={
                "padding": "32px",
                "background": DARK_COLORS["bg_secondary"],
                "border-radius": "16px",
                "box-shadow": DARK_SHADOWS["xl"],
            },
        ),
        open=ClaimsState.show_claim_modal,
        on_open_change=ClaimsState.set_show_claim_modal,
    )
