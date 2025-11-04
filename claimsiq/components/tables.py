import reflex as rx
from claimsiq.theme import COLORS, FONT_SIZES, SPACING, SHADOWS
from claimsiq.state import ClaimsState
from claimsiq.components.ui_helpers import empty_state, sortable_header

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
            # Header with search and filters
            rx.hstack(
                rx.heading("Claims", size="5", color=COLORS["gray_900"]),
                rx.spacer(),
                rx.hstack(
                    # Search input
                    rx.input(
                        placeholder="Search claims...",
                        value=ClaimsState.search_query,
                        on_change=ClaimsState.set_search_query,
                        size="2",
                        width="250px",
                    ),
                    # Status filter
                    rx.select(
                        ["all", "pending", "approved", "denied", "flagged"],
                        value=ClaimsState.selected_status,
                        on_change=lambda val: [
                            ClaimsState.set_status_filter(val),
                            ClaimsState.load_claims()
                        ],
                        size="2",
                    ),
                    spacing="3",
                ),
                spacing="4",
                width="100%",
                align="center",
            ),
            # Table content
            rx.cond(
                ClaimsState.is_loading,
                rx.center(
                    rx.spinner(size="3", color=COLORS["primary"]),
                    padding="12",
                    min_height="400px",
                ),
                rx.cond(
                    ClaimsState.paginated_claims.length() > 0,
                    rx.vstack(
                        # Table
                        rx.table.root(
                            rx.table.header(
                                rx.table.row(
                                    sortable_header(
                                        "Claim ID",
                                        "id",
                                        ClaimsState.sort_column,
                                        ClaimsState.sort_direction,
                                        lambda: ClaimsState.sort_by("id"),
                                    ),
                                    sortable_header(
                                        "Date",
                                        "claim_date",
                                        ClaimsState.sort_column,
                                        ClaimsState.sort_direction,
                                        lambda: ClaimsState.sort_by("claim_date"),
                                    ),
                                    sortable_header(
                                        "Amount",
                                        "claim_amount",
                                        ClaimsState.sort_column,
                                        ClaimsState.sort_direction,
                                        lambda: ClaimsState.sort_by("claim_amount"),
                                    ),
                                    rx.table.column_header_cell("Status"),
                                    sortable_header(
                                        "Risk Score",
                                        "risk_score",
                                        ClaimsState.sort_column,
                                        ClaimsState.sort_direction,
                                        lambda: ClaimsState.sort_by("risk_score"),
                                    ),
                                )
                            ),
                            rx.table.body(
                                rx.foreach(
                                    ClaimsState.paginated_claims,
                                    lambda claim: rx.table.row(
                                        rx.table.cell(
                                            rx.text(claim["id"], weight="medium")
                                        ),
                                        rx.table.cell(
                                            rx.text(
                                                claim["claim_date"],
                                                color=COLORS["gray_600"],
                                            )
                                        ),
                                        rx.table.cell(
                                            rx.text(
                                                f"${claim['claim_amount']:,.2f}",
                                                weight="medium",
                                                color=COLORS["gray_900"],
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
                        # Pagination
                        rx.hstack(
                            rx.text(
                                f"Showing {ClaimsState.page_start} to {ClaimsState.page_end} of {ClaimsState.sorted_claims.length()}",
                                size="2",
                                color=COLORS["gray_500"],
                                weight="medium",
                            ),
                            rx.spacer(),
                            rx.hstack(
                                rx.icon_button(
                                    rx.icon("chevron-left", size=18),
                                    on_click=ClaimsState.previous_page,
                                    disabled=ClaimsState.current_page == 1,
                                    variant="soft",
                                    size="2",
                                ),
                                rx.text(
                                    f"Page {ClaimsState.current_page} of {ClaimsState.total_pages}",
                                    size="2",
                                    weight="medium",
                                    color=COLORS["gray_700"],
                                ),
                                rx.icon_button(
                                    rx.icon("chevron-right", size=18),
                                    on_click=ClaimsState.next_page,
                                    disabled=ClaimsState.is_last_page,
                                    variant="soft",
                                    size="2",
                                ),
                                spacing="2",
                                align="center",
                            ),
                            width="100%",
                            align="center",
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    empty_state(
                        icon="inbox",
                        title="No Claims Found",
                        description="No claims match your search criteria. Try adjusting your filters or search query.",
                    ),
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
