import reflex as rx

from claimsiq.theme import COLORS
from claimsiq.state import ClaimsState
from claimsiq.components.ui_helpers import empty_state, sortable_header, skeleton_table

HIGH_ROW_CLASS = "cursor-pointer bg-red-50 hover:bg-red-100 border-l-4 border-red-300 transition-colors duration-150"
MEDIUM_ROW_CLASS = "cursor-pointer bg-amber-50 hover:bg-amber-100 border-l-4 border-amber-300 transition-colors duration-150"
LOW_ROW_CLASS = "cursor-pointer hover:bg-gray-50 transition-colors duration-150"


def risk_badge(risk_score, reason=None, has_reason=None) -> rx.Component:
    """Visual risk indicator with color, icon, label, and optional reason."""
    # Convert to float if it's a Var
    score = risk_score.to(float) if hasattr(risk_score, 'to') else risk_score
    try:
        score = float(score)
    except (TypeError, ValueError):
        score = 0.0

    badge = rx.cond(
        score >= 0.7,
        rx.badge(
            rx.hstack(
                rx.icon("triangle_alert", size=14),
                rx.text(f"{score:.2f}", size="2", weight="medium"),
                spacing="1",
                align="center",
            ),
            color_scheme="red",
            variant="solid",
        ),
        rx.cond(
            score >= 0.4,
            rx.badge(
                rx.hstack(
                    rx.icon("circle_alert", size=14),
                    rx.text(f"{score:.2f}", size="2", weight="medium"),
                    spacing="1",
                    align="center",
                ),
                color_scheme="orange",
                variant="soft",
            ),
            rx.badge(
                rx.hstack(
                    rx.icon("circle_check", size=14),
                    rx.text(f"{score:.2f}", size="2", weight="medium"),
                    spacing="1",
                    align="center",
                ),
                color_scheme="green",
                variant="soft",
            ),
        ),
    )

    reason_component = rx.fragment()
    if reason is not None:
        condition = reason != ""
        cond_var = has_reason if has_reason is not None else condition
        reason_component = rx.cond(
            cond_var,
            rx.text(
                reason,
                size="1",
                color=COLORS["gray_500"],
                max_width="180px",
            ),
            rx.fragment(),
        )

    return rx.vstack(
        badge,
        reason_component,
        spacing="1",
        align="start",
    )

def status_badge(status) -> rx.Component:
    """Color-coded status badges"""
    # Color mapping for different statuses - use hardcoded capitalized labels
    return rx.match(
        status,
        ("approved", rx.badge("Approved", color_scheme="green", variant="soft")),
        ("pending", rx.badge("Pending", color_scheme="blue", variant="soft")),
        ("denied", rx.badge("Denied", color_scheme="red", variant="soft")),
        ("flagged", rx.badge("Flagged", color_scheme="orange", variant="soft")),
        rx.badge("Unknown", color_scheme="gray", variant="soft"),
    )


def status_filter_chip(status_key: str, label: str) -> rx.Component:
    """Clickable chip that applies a status filter."""
    return rx.cond(
        ClaimsState.selected_status == status_key,
        rx.button(
            rx.hstack(
                rx.icon("check", size=16),
                rx.text(label, weight="medium"),
                spacing="1",
                align="center",
            ),
            size="2",
            variant="solid",
            color_scheme="blue",
            on_click=lambda status=status_key: ClaimsState.set_status_filter(status),
        ),
        rx.button(
            label,
            size="2",
            variant="outline",
            color_scheme="gray",
            on_click=lambda status=status_key: ClaimsState.set_status_filter(status),
        ),
    )


def sticky_cell(content: rx.Component) -> rx.Component:
    """Sticky first column cell for claim ID."""
    return rx.table.cell(
        content,
        class_name="sticky left-0 bg-white/95 backdrop-blur px-4",
        border_right="1px solid #e5e7eb",
    )


def claim_row(claim: dict) -> rx.Component:
    """Create a table row for a single claim."""
    return rx.table.row(
        sticky_cell(
            rx.text(
                claim["id"],
                weight="medium",
            )
        ),
        rx.table.cell(
            rx.text(
                rx.cond(
                    claim.get("provider_name"),
                    claim.get("provider_name"),
                    rx.cond(
                        claim.get("provider_id"),
                        claim.get("provider_id"),
                        "—"
                    )
                ),
                color=COLORS["gray_600"],
            )
        ),
        rx.table.cell(
            rx.text(
                claim["claim_date"],
                color=COLORS["gray_600"],
            )
        ),
        rx.table.cell(
            rx.text(
                claim.get("claim_amount_formatted", "$0.00"),
                weight="medium",
                color=COLORS["gray_900"],
            )
        ),
        rx.table.cell(
            status_badge(claim["status"])
        ),
        rx.table.cell(
            risk_badge(
                claim["risk_score"],
                reason=claim["ui_risk_reason"],
                has_reason=claim["ui_has_reason"],
            )
        ),
        # Store claim ID in id attribute for extraction
        id=claim["id"],
        on_click=ClaimsState.open_claim_modal,
        cursor="pointer",
        class_name=rx.match(
            claim["ui_risk_level"],
            ("high", HIGH_ROW_CLASS),
            ("medium", MEDIUM_ROW_CLASS),
            ("low", LOW_ROW_CLASS),
            LOW_ROW_CLASS,
        ),
        role="button",
        aria_label=f"View claim {claim['id']}",
    )

def claims_table() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.vstack(
                rx.hstack(
                    rx.heading("Claims", size="5", class_name="text-gray-900"),
                    rx.cond(
                        ClaimsState.selected_status != "all",
                        rx.badge(
                            f"Filtered: {ClaimsState.selected_status}",
                            color_scheme="blue",
                            variant="soft",
                        ),
                        rx.fragment(),
                    ),
                    rx.spacer(),
                    rx.button(
                        rx.hstack(
                    rx.icon("download", size=18),
                            rx.text("Export"),
                            spacing="2",
                        ),
                        on_click=ClaimsState.export_to_csv,
                        variant="outline",
                        size="2",
                    ),
                    spacing="4",
                    align="center",
                    width="100%",
                ),
                rx.hstack(
                    status_filter_chip("all", "All"),
                    status_filter_chip("approved", "Approved"),
                    status_filter_chip("pending", "Pending"),
                    status_filter_chip("flagged", "Flagged"),
                    rx.spacer(),
                    rx.input(
                        placeholder="Search claim ID or provider...",
                        value=ClaimsState.search_query,
                        on_change=ClaimsState.set_search_query,
                        size="2",
                        width="280px",
                    ),
                    rx.cond(
                        (ClaimsState.selected_status != "all") | (ClaimsState.search_query != ""),
                        rx.button(
                            rx.hstack(
                                rx.icon("circle_x", size=16),
                                rx.text("Clear filters"),
                                spacing="1",
                            ),
                            on_click=ClaimsState.clear_filters,
                            variant="ghost",
                            size="2",
                        ),
                        rx.fragment(),
                    ),
                    spacing="3",
                    align="center",
                    width="100%",
                ),
                spacing="3",
                width="100%",
            ),
            # Table content
            rx.cond(
                ClaimsState.is_loading_claims,
                skeleton_table(),
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
                                        ClaimsState.sort_by("id"),
                                        class_name="sticky left-0 z-20 bg-white/95 backdrop-blur",
                                    ),
                                    rx.table.column_header_cell(
                                        "Provider",
                                        class_name="min-w-[160px]",
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
                                    rx.table.column_header_cell("Status"),
                                    sortable_header(
                                        "Risk Score",
                                        "risk_score",
                                        ClaimsState.sort_column,
                                        ClaimsState.sort_direction,
                                        ClaimsState.sort_by("risk_score"),
                                    ),
                                )
                            ),
                            rx.table.body(
                                rx.foreach(
                                    ClaimsState.paginated_claims,
                                    claim_row
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
                                    rx.icon("chevron_left", size=18),
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
                                    rx.icon("chevron_right", size=18),
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
            class_name="space-y-4 w-full",
        ),
        class_name="p-6 bg-white rounded-xl shadow-md w-full",
    )
