"""
Dark Mode Filters Bar - Compact horizontal filters below action bar

Features:
- Horizontal layout for space efficiency
- Sticky positioning with navbar and action bar
- Dark theme styling
- Quick filter chips for common operations
"""
import reflex as rx
from claimsiq.theme import DARK_COLORS, DARK_SHADOWS
from claimsiq.state import ClaimsState


def dark_filters_bar() -> rx.Component:
    """Compact horizontal filters bar for dark mode"""
    return rx.box(
        rx.box(
            rx.hstack(
                # Left: Quick Status Filters
                rx.hstack(
                    rx.text(
                        "Status:",
                        size="2",
                        weight="bold",
                        style={"color": DARK_COLORS["text_secondary"]},
                    ),
                    rx.button(
                        rx.hstack(
                            rx.cond(
                                ClaimsState.selected_status == "all",
                                rx.icon("check", size=14),
                                rx.fragment(),
                            ),
                            rx.text("All", size="2"),
                            rx.badge(
                                ClaimsState.total_claims,
                                variant="soft",
                                color_scheme="gray",
                                size="1",
                            ),
                            spacing="2",
                        ),
                        on_click=ClaimsState.set_status_filter("all"),
                        variant=rx.cond(
                            ClaimsState.selected_status == "all",
                            "solid",
                            "outline"
                        ),
                        color_scheme="gray",
                        size="2",
                    ),
                    rx.button(
                        rx.hstack(
                            rx.cond(
                                ClaimsState.selected_status == "approved",
                                rx.icon("check", size=14),
                                rx.fragment(),
                            ),
                            rx.text("Approved", size="2"),
                            rx.badge(
                                ClaimsState.approved_count,
                                variant="soft",
                                color_scheme="green",
                                size="1",
                            ),
                            spacing="2",
                        ),
                        on_click=ClaimsState.set_status_filter("approved"),
                        variant=rx.cond(
                            ClaimsState.selected_status == "approved",
                            "solid",
                            "outline"
                        ),
                        color_scheme="green",
                        size="2",
                    ),
                    rx.button(
                        rx.hstack(
                            rx.cond(
                                ClaimsState.selected_status == "pending",
                                rx.icon("check", size=14),
                                rx.fragment(),
                            ),
                            rx.text("Pending", size="2"),
                            rx.badge(
                                ClaimsState.pending_count,
                                variant="soft",
                                color_scheme="blue",
                                size="1",
                            ),
                            spacing="2",
                        ),
                        on_click=ClaimsState.set_status_filter("pending"),
                        variant=rx.cond(
                            ClaimsState.selected_status == "pending",
                            "solid",
                            "outline"
                        ),
                        color_scheme="blue",
                        size="2",
                    ),
                    rx.button(
                        rx.hstack(
                            rx.cond(
                                ClaimsState.selected_status == "flagged",
                                rx.icon("check", size=14),
                                rx.fragment(),
                            ),
                            rx.text("Flagged", size="2"),
                            rx.badge(
                                ClaimsState.flagged_count,
                                variant="soft",
                                color_scheme="red",
                                size="1",
                            ),
                            spacing="2",
                        ),
                        on_click=ClaimsState.set_status_filter("flagged"),
                        variant=rx.cond(
                            ClaimsState.selected_status == "flagged",
                            "solid",
                            "outline"
                        ),
                        color_scheme="red",
                        size="2",
                    ),
                    spacing="2",
                    align="center",
                ),

                rx.box(
                    height="24px",
                    width="1px",
                    style={"background": DARK_COLORS["border"]},
                ),

                # Middle: Risk Filters
                rx.hstack(
                    rx.text(
                        "Risk:",
                        size="2",
                        weight="bold",
                        style={"color": DARK_COLORS["text_secondary"]},
                    ),
                    rx.button(
                        rx.hstack(
                            rx.cond(
                                ClaimsState.risk_low_active,
                                rx.icon("check", size=14),
                                rx.fragment(),
                            ),
                            rx.text("Low", size="2"),
                            spacing="2",
                        ),
                        on_click=ClaimsState.toggle_risk("low"),
                        variant=rx.cond(ClaimsState.risk_low_active, "solid", "outline"),
                        color_scheme="green",
                        size="2",
                    ),
                    rx.button(
                        rx.hstack(
                            rx.cond(
                                ClaimsState.risk_medium_active,
                                rx.icon("check", size=14),
                                rx.fragment(),
                            ),
                            rx.text("Medium", size="2"),
                            spacing="2",
                        ),
                        on_click=ClaimsState.toggle_risk("medium"),
                        variant=rx.cond(ClaimsState.risk_medium_active, "solid", "outline"),
                        color_scheme="orange",
                        size="2",
                    ),
                    rx.button(
                        rx.hstack(
                            rx.cond(
                                ClaimsState.risk_high_active,
                                rx.icon("check", size=14),
                                rx.fragment(),
                            ),
                            rx.text("High", size="2"),
                            spacing="2",
                        ),
                        on_click=ClaimsState.toggle_risk("high"),
                        variant=rx.cond(ClaimsState.risk_high_active, "solid", "outline"),
                        color_scheme="red",
                        size="2",
                    ),
                    spacing="2",
                    align="center",
                ),

                rx.box(
                    height="24px",
                    width="1px",
                    style={"background": DARK_COLORS["border"]},
                ),

                # Right: Date Range
                rx.hstack(
                    rx.text(
                        "Date:",
                        size="2",
                        weight="bold",
                        style={"color": DARK_COLORS["text_secondary"]},
                    ),
                    rx.input(
                        type="date",
                        value=ClaimsState.date_start,
                        on_change=ClaimsState.update_date_start,
                        size="2",
                        style={
                            "width": "150px",
                            "background": DARK_COLORS["bg_elevated"],
                            "border-color": DARK_COLORS["border"],
                            "color": DARK_COLORS["text_primary"],
                        },
                    ),
                    rx.text("to", size="2", style={"color": DARK_COLORS["text_tertiary"]}),
                    rx.input(
                        type="date",
                        value=ClaimsState.date_end,
                        on_change=ClaimsState.update_date_end,
                        size="2",
                        style={
                            "width": "150px",
                            "background": DARK_COLORS["bg_elevated"],
                            "border-color": DARK_COLORS["border"],
                            "color": DARK_COLORS["text_primary"],
                        },
                    ),
                    spacing="2",
                    align="center",
                ),

                rx.spacer(),

                # Far Right: Clear Filters
                rx.button(
                    rx.hstack(
                        rx.icon("x", size=16),
                        rx.text("Clear All", size="2"),
                        spacing="2",
                    ),
                    on_click=ClaimsState.clear_filters,
                    variant="outline",
                    color_scheme="red",
                    size="2",
                ),

                width="100%",
                align="center",
                spacing="4",
            ),
            style={"padding": "12px 64px"},  # Match navbar/action bar padding
            max_width="1600px",
            margin_x="auto",
            width="100%",
        ),
        style={
            "background": DARK_COLORS["bg_card"],
            "border-bottom": f"1px solid {DARK_COLORS['border']}",
            "box-shadow": DARK_SHADOWS["sm"],
        },
        width="100%",
    )
