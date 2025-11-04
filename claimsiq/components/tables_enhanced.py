"""
Enhanced Claims Table with Alternating Row Colors and Better UX
"""
import reflex as rx
from claimsiq.theme import COLORS
from claimsiq.state import ClaimsState


def status_badge(status: str) -> rx.Component:
    """Status badge with color coding"""
    return rx.match(
        status,
        ("approved", rx.badge("Approved", color_scheme="green", variant="soft", size="2")),
        ("pending", rx.badge("Pending", color_scheme="blue", variant="soft", size="2")),
        ("denied", rx.badge("Denied", color_scheme="red", variant="soft", size="2")),
        ("flagged", rx.badge("Flagged", color_scheme="orange", variant="soft", size="2")),
        rx.badge(status, color_scheme="gray", variant="soft", size="2"),
    )


def risk_badge(risk_score: float) -> rx.Component:
    """Risk score badge with color coding"""
    return rx.match(
        risk_score >= 0.7,
        (True, rx.badge("High", color_scheme="red", variant="soft", size="2")),
        (False, rx.match(
            risk_score >= 0.4,
            (True, rx.badge("Medium", color_scheme="orange", variant="soft", size="2")),
            (False, rx.badge("Low", color_scheme="green", variant="soft", size="2")),
        )),
    )


def sortable_header(
    label: str,
    column: str,
    current_sort: str,
    direction: str,
    on_click,
) -> rx.Component:
    """Sortable table header with visual indicator"""
    is_active = current_sort == column

    return rx.table.column_header_cell(
        rx.hstack(
            rx.text(label, size="2", weight="bold"),
            rx.cond(
                is_active,
                rx.icon(
                    "chevron-up" if direction == "asc" else "chevron-down",
                    size=16,
                ),
                rx.icon("chevrons-up-down", size=14, color=COLORS["gray_400"]),
            ),
            spacing="1",
            align="center",
        ),
        on_click=on_click,
        style={
            "cursor": "pointer",
            "_hover": {"background": COLORS["gray_100"]},
        },
    )


def enhanced_claims_table() -> rx.Component:
    """
    Enhanced claims table with:
    - Alternating row colors
    - Better hover states
    - Sortable columns
    - Inline actions
    """
    return rx.box(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell(
                        "Claim ID",
                        position="sticky",
                        left="0",
                        background=COLORS["white"],
                        z_index="10",
                    ),
                    sortable_header(
                        "Provider",
                        "provider_id",
                        ClaimsState.sort_column,
                        ClaimsState.sort_direction,
                        ClaimsState.sort_by("provider_id"),
                    ),
                    sortable_header(
                        "Date",
                        "claim_date",
                        ClaimsState.sort_column,
                        ClaimsState.sort_direction,
                        ClaimsState.sort_by("claim_date"),
                    ),
                    sortable_header(
                        "Amount",
                        "claim_amount",
                        ClaimsState.sort_column,
                        ClaimsState.sort_direction,
                        ClaimsState.sort_by("claim_amount"),
                    ),
                    sortable_header(
                        "Status",
                        "status",
                        ClaimsState.sort_column,
                        ClaimsState.sort_direction,
                        ClaimsState.sort_by("status"),
                    ),
                    sortable_header(
                        "Risk",
                        "risk_score",
                        ClaimsState.sort_column,
                        ClaimsState.sort_direction,
                        ClaimsState.sort_by("risk_score"),
                    ),
                    rx.table.column_header_cell("Actions"),
                    background=COLORS["gray_50"],
                ),
            ),
            rx.table.body(
                rx.foreach(
                    ClaimsState.paginated_claims,
                    lambda claim: rx.table.row(
                        rx.table.cell(
                            rx.text(
                                claim["id"],
                                weight="medium",
                                size="2",
                            ),
                            position="sticky",
                            left="0",
                            background="inherit",
                            z_index="5",
                        ),
                        rx.table.cell(
                            rx.text(
                                claim.get("provider_id", "—"),
                                size="2",
                                color=COLORS["gray_700"],
                            )
                        ),
                        rx.table.cell(
                            rx.text(
                                claim["claim_date"],
                                size="2",
                                color=COLORS["gray_700"],
                            )
                        ),
                        rx.table.cell(
                            rx.text(
                                claim.get("claim_amount_formatted", "$0.00"),
                                weight="medium",
                                size="2",
                                color=COLORS["gray_900"],
                            )
                        ),
                        rx.table.cell(
                            status_badge(claim["status"])
                        ),
                        rx.table.cell(
                            risk_badge(claim.get("risk_score", 0))
                        ),
                        rx.table.cell(
                            rx.hstack(
                                rx.icon_button(
                                    rx.icon("eye", size=16),
                                    on_click=ClaimsState.open_claim_modal(claim["id"]),
                                    size="1",
                                    variant="ghost",
                                    color_scheme="blue",
                                ),
                                spacing="1",
                            )
                        ),
                        on_click=ClaimsState.open_claim_modal(claim["id"]),
                        style={
                            "cursor": "pointer",
                            "_hover": {"background": "#eff6ff"},  # blue-50
                            "transition": "background-color 0.2s",
                        },
                    ),
                ),
                class_name="[&>tr:nth-child(even)]:bg-gray-50 [&>tr:nth-child(odd)]:bg-white",
            ),
            variant="surface",
            size="3",
            width="100%",
        ),
        width="100%",
        overflow_x="auto",
        class_name="rounded-2xl border border-slate-200/70 dark:border-slate-700/60 shadow-md bg-white/90 dark:bg-slate-800/95 backdrop-blur",
    )
