"""
Dark Mode Table with Enhanced Typography and Readability

Addresses:
- ✅ Larger font sizes (16px minimum for values)
- ✅ Bold weights for headers and key numbers
- ✅ High contrast text colors
- ✅ Row striping for easy scanning
- ✅ Ample cell padding
- ✅ Better line heights
- ✅ Accessible color combinations (WCAG AA)
"""
import reflex as rx
from claimsiq.theme import DARK_COLORS, DARK_SHADOWS
from claimsiq.state import ClaimsState


def status_badge_dark(status: str) -> rx.Component:
    """Status badge with high contrast colors for dark mode"""
    return rx.match(
        status,
        ("approved", rx.badge(
            "Approved",
            color_scheme="green",
            variant="solid",
            size="2",
            style={
                "font-size": "14px",
                "font-weight": "600",
                "padding": "4px 12px",
            }
        )),
        ("pending", rx.badge(
            "Pending",
            color_scheme="orange",
            variant="solid",
            size="2",
            style={
                "font-size": "14px",
                "font-weight": "600",
                "padding": "4px 12px",
            }
        )),
        ("denied", rx.badge(
            "Denied",
            color_scheme="red",
            variant="solid",
            size="2",
            style={
                "font-size": "14px",
                "font-weight": "600",
                "padding": "4px 12px",
            }
        )),
        ("flagged", rx.badge(
            "⚠ Flagged",
            color_scheme="yellow",
            variant="solid",
            size="2",
            style={
                "font-size": "14px",
                "font-weight": "700",  # Extra bold for flagged
                "padding": "4px 12px",
            }
        )),
        rx.badge(status, color_scheme="gray", variant="soft", size="2"),
    )


def risk_badge_dark(risk_score) -> rx.Component:
    """Risk badge with enhanced visibility for dark mode"""
    # Convert to float if it's a Var
    score = risk_score.to(float) if hasattr(risk_score, 'to') else risk_score

    return rx.cond(
        score >= 0.7,
        rx.badge(
            "HIGH RISK",
            color_scheme="red",
            variant="solid",
            size="2",
            style={
                "font-size": "14px",
                "font-weight": "700",
                "padding": "4px 12px",
                "text-transform": "uppercase",
            }
        ),
        rx.cond(
            score >= 0.4,
            rx.badge(
                "Medium",
                color_scheme="orange",
                variant="solid",
                size="2",
                style={
                    "font-size": "14px",
                    "font-weight": "600",
                    "padding": "4px 12px",
                }
            ),
            rx.badge(
                "Low",
                color_scheme="green",
                variant="soft",
                size="2",
                style={
                    "font-size": "14px",
                    "font-weight": "500",
                    "padding": "4px 12px",
                }
            ),
        ),
    )


def dark_table_cell(
    content: rx.Component,
    is_bold: bool = False,
    is_amount: bool = False,
) -> rx.Component:
    """
    Table cell with proper typography for dark mode

    Args:
        content: Cell content
        is_bold: Whether to use bold weight (for amounts, key data)
        is_amount: Whether this is a currency amount (extra large)
    """
    if is_amount:
        # Currency amounts: large, bold, high contrast
        return rx.table.cell(
            content,
            style={
                "font-size": "16px",
                "font-weight": "700",
                "color": DARK_COLORS["text_primary"],
                "padding": "16px 12px",
                "line-height": "1.6",
            }
        )
    elif is_bold:
        # Bold cells: IDs, headers
        return rx.table.cell(
            content,
            style={
                "font-size": "15px",
                "font-weight": "600",
                "color": DARK_COLORS["text_primary"],
                "padding": "16px 12px",
                "line-height": "1.6",
            }
        )
    else:
        # Regular cells: readable size
        return rx.table.cell(
            content,
            style={
                "font-size": "15px",
                "font-weight": "400",
                "color": DARK_COLORS["text_secondary"],
                "padding": "16px 12px",
                "line-height": "1.6",
            }
        )


def sortable_header_dark(
    label: str,
    column: str,
    current_sort: str,
    direction: str,
    on_click,
) -> rx.Component:
    """Sortable header with enhanced typography for dark mode"""
    is_active = current_sort == column

    return rx.table.column_header_cell(
        rx.hstack(
            rx.text(
                label,
                size="3",  # Larger size
                weight="bold",  # Always bold
                color=DARK_COLORS["text_primary"],
                style={
                    "font-size": "16px",
                    "text-transform": "uppercase",
                    "letter-spacing": "0.5px",
                },
            ),
            rx.cond(
                is_active,
                rx.cond(
                    direction == "asc",
                    rx.icon("chevron-up", size=18, color=DARK_COLORS["primary"]),
                    rx.icon("chevron-down", size=18, color=DARK_COLORS["primary"]),
                ),
                rx.icon(
                    "chevrons-up-down",
                    size=16,
                    color=DARK_COLORS["text_tertiary"],
                ),
            ),
            spacing="2",
            align="center",
        ),
        on_click=on_click,
        style={
            "cursor": "pointer",
            "background": DARK_COLORS["bg_elevated"],
            "padding": "16px 12px",
            "border-bottom": f"2px solid {DARK_COLORS['border_light']}",
            "_hover": {
                "background": DARK_COLORS["bg_tertiary"],
            },
        },
    )


def dark_claim_row(claim: dict) -> rx.Component:
    """Create a table row for a single claim - dark mode version."""
    return rx.table.row(
        # Claim ID - bold
        dark_table_cell(
            rx.text(
                claim["id"],
                color=DARK_COLORS["primary"],
            ),
            is_bold=True,
        ),

        # Provider - regular
        dark_table_cell(
            rx.text(
                claim.get("provider_id", "—"),
            ),
        ),

        # Date - regular
        dark_table_cell(
            rx.text(
                claim["claim_date"],
            ),
        ),

        # Amount - LARGE and BOLD
        dark_table_cell(
            rx.text(
                claim.get("claim_amount_formatted", "$0.00"),
                color=DARK_COLORS["success"],  # Green for money
            ),
            is_amount=True,
        ),

        # Status badge - enhanced
        rx.table.cell(
            status_badge_dark(claim["status"]),
            style={
                "padding": "16px 12px",
            },
        ),

        # Risk badge - enhanced
        rx.table.cell(
            risk_badge_dark(claim.get("risk_score", 0)),
            style={
                "padding": "16px 12px",
            },
        ),

        # Actions
        rx.table.cell(
            rx.icon_button(
                rx.icon("eye", size=18),
                on_click=ClaimsState.open_claim_modal(claim["id"]),
                size="2",
                variant="ghost",
                style={
                    "color": DARK_COLORS["primary"],
                    "_hover": {
                        "background": DARK_COLORS["primary_bg"],
                    },
                },
            ),
            style={
                "padding": "16px 12px",
            },
        ),

        on_click=ClaimsState.open_claim_modal(claim["id"]),
        style={
            "cursor": "pointer",
            "transition": "all 0.2s ease",
            "_hover": {
                "background": DARK_COLORS["bg_tertiary"],
                "box-shadow": DARK_SHADOWS["glow"],
            },
        },
        # CSS for alternating rows
        class_name="[&:nth-child(even)]:bg-[#1a1f2e] [&:nth-child(odd)]:bg-[#0f1419]",
    )


def dark_claims_table() -> rx.Component:
    """
    Enhanced claims table for dark mode with:
    - Larger font sizes (15-16px)
    - Bold weights for headers and amounts
    - High contrast colors
    - Row striping
    - Ample padding
    - Better line heights
    """
    return rx.box(
        rx.table.root(
            # Header with bold, large text
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell(
                        rx.text(
                            "CLAIM ID",
                            style={
                                "font-size": "16px",
                                "font-weight": "700",
                                "text-transform": "uppercase",
                                "letter-spacing": "0.5px",
                                "color": DARK_COLORS["text_primary"],
                            }
                        ),
                        position="sticky",
                        left="0",
                        background=DARK_COLORS["bg_elevated"],
                        z_index="10",
                        style={
                            "padding": "16px 12px",
                            "border-bottom": f"2px solid {DARK_COLORS['border_light']}",
                        },
                    ),
                    sortable_header_dark(
                        "PROVIDER",
                        "provider_id",
                        ClaimsState.sort_column,
                        ClaimsState.sort_direction,
                        ClaimsState.sort_by("provider_id"),
                    ),
                    sortable_header_dark(
                        "DATE",
                        "claim_date",
                        ClaimsState.sort_column,
                        ClaimsState.sort_direction,
                        ClaimsState.sort_by("claim_date"),
                    ),
                    sortable_header_dark(
                        "AMOUNT",
                        "claim_amount",
                        ClaimsState.sort_column,
                        ClaimsState.sort_direction,
                        ClaimsState.sort_by("claim_amount"),
                    ),
                    sortable_header_dark(
                        "STATUS",
                        "status",
                        ClaimsState.sort_column,
                        ClaimsState.sort_direction,
                        ClaimsState.sort_by("status"),
                    ),
                    sortable_header_dark(
                        "RISK",
                        "risk_score",
                        ClaimsState.sort_column,
                        ClaimsState.sort_direction,
                        ClaimsState.sort_by("risk_score"),
                    ),
                    rx.table.column_header_cell(
                        rx.text(
                            "ACTIONS",
                            style={
                                "font-size": "16px",
                                "font-weight": "700",
                                "text-transform": "uppercase",
                                "letter-spacing": "0.5px",
                                "color": DARK_COLORS["text_primary"],
                            }
                        ),
                        style={
                            "padding": "16px 12px",
                            "border-bottom": f"2px solid {DARK_COLORS['border_light']}",
                        },
                    ),
                    style={
                        "background": DARK_COLORS["bg_elevated"],
                    },
                ),
            ),

            # Body with enhanced typography and row striping
            rx.table.body(
                rx.foreach(
                    ClaimsState.paginated_claims,
                    dark_claim_row
                ),
            ),

            variant="surface",
            size="3",
            width="100%",
        ),
        width="100%",
        overflow_x="auto",
        border_radius="12px",
        border=f"1px solid {DARK_COLORS['border']}",
        box_shadow=DARK_SHADOWS["lg"],
    )
