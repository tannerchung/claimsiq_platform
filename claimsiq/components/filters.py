import reflex as rx
from claimsiq.theme import COLORS, SHADOWS
from claimsiq.state import ClaimsState


def filters_panel() -> rx.Component:
    """Advanced filters panel for claims"""
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.heading("Filters", size="4", color=COLORS["gray_900"]),
                rx.spacer(),
                rx.button(
                    rx.icon("x", size=16),
                    on_click=ClaimsState.clear_filters,
                    variant="ghost",
                    size="1",
                    color=COLORS["gray_500"],
                ),
                width="100%",
                align="center",
            ),

            rx.separator(),

            # Date Range Filter
            rx.vstack(
                rx.text(
                    "Date Range",
                    size="2",
                    weight="bold",
                    color=COLORS["gray_700"],
                ),
                rx.vstack(
                    rx.hstack(
                        rx.text("From:", size="1", color=COLORS["gray_600"]),
                        rx.input(
                            type="date",
                            value=ClaimsState.date_start,
                            on_change=lambda val: ClaimsState.set_date_range(val, ClaimsState.date_end),
                            size="2",
                            width="100%",
                        ),
                        spacing="2",
                        width="100%",
                        align="center",
                    ),
                    rx.hstack(
                        rx.text("To:", size="1", color=COLORS["gray_600"]),
                        rx.input(
                            type="date",
                            value=ClaimsState.date_end,
                            on_change=lambda val: ClaimsState.set_date_range(ClaimsState.date_start, val),
                            size="2",
                            width="100%",
                        ),
                        spacing="2",
                        width="100%",
                        align="center",
                    ),
                    spacing="2",
                    width="100%",
                ),
                spacing="2",
                width="100%",
            ),

            rx.separator(),

            # Amount Range Filter
            rx.vstack(
                rx.text(
                    "Amount Range",
                    size="2",
                    weight="bold",
                    color=COLORS["gray_700"],
                ),
                rx.vstack(
                    rx.hstack(
                        rx.text(
                            f"${ClaimsState.amount_min:,.0f} - ${ClaimsState.amount_max:,.0f}",
                            size="2",
                            color=COLORS["gray_600"],
                            weight="medium",
                        ),
                        width="100%",
                    ),
                    rx.slider(
                        default_value=[0, 100000],
                        min=0,
                        max=100000,
                        step=1000,
                        # on_change would need custom handling
                        width="100%",
                    ),
                    spacing="2",
                    width="100%",
                ),
                spacing="2",
                width="100%",
            ),

            rx.separator(),

            # Risk Level Filter
            rx.vstack(
                rx.text(
                    "Risk Level",
                    size="2",
                    weight="bold",
                    color=COLORS["gray_700"],
                ),
                rx.vstack(
                    rx.checkbox(
                        "Low Risk (< 0.4)",
                        size="2",
                        color_scheme="green",
                    ),
                    rx.checkbox(
                        "Medium Risk (0.4 - 0.7)",
                        size="2",
                        color_scheme="orange",
                    ),
                    rx.checkbox(
                        "High Risk (≥ 0.7)",
                        size="2",
                        color_scheme="red",
                    ),
                    spacing="2",
                    align="start",
                    width="100%",
                ),
                spacing="2",
                width="100%",
            ),

            rx.separator(),

            # Action Buttons
            rx.vstack(
                rx.button(
                    rx.hstack(
                        rx.icon("filter", size=16),
                        rx.text("Apply Filters"),
                        spacing="2",
                    ),
                    width="100%",
                    size="2",
                ),
                rx.button(
                    rx.hstack(
                        rx.icon("refresh-cw", size=16),
                        rx.text("Reset All"),
                        spacing="2",
                    ),
                    on_click=ClaimsState.clear_filters,
                    variant="outline",
                    width="100%",
                    size="2",
                ),
                spacing="2",
                width="100%",
            ),

            spacing="4",
            width="100%",
        ),
        padding="4",
        background=COLORS["white"],
        border_radius="0.75rem",
        box_shadow=SHADOWS["lg"],
        width="320px",
        max_height="600px",
        overflow_y="auto",
    )


def filters_button() -> rx.Component:
    """Button to toggle filters panel"""
    return rx.popover.root(
        rx.popover.trigger(
            rx.button(
                rx.hstack(
                    rx.icon("filter", size=18),
                    rx.text("Filters"),
                    spacing="2",
                    align="center",
                ),
                variant="outline",
                size="2",
            ),
        ),
        rx.popover.content(
            filters_panel(),
            side="bottom",
            align="end",
        ),
    )
