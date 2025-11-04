import reflex as rx
from claimsiq.theme import COLORS, SHADOWS
from claimsiq.state import ClaimsState


def risk_chip(label: str, key: str, color: str, is_active) -> rx.Component:
    """Multi-select chip for risk filters."""
    return rx.cond(
        is_active,
        rx.button(
            rx.hstack(
                rx.icon("check", size=16),
                rx.text(label),
                spacing="1",
            ),
            size="2",
            variant="solid",
            color_scheme=color,
            on_click=lambda value=key: ClaimsState.toggle_risk(value),
        ),
        rx.button(
            label,
            size="2",
            variant="outline",
            color_scheme=color,
            on_click=lambda value=key: ClaimsState.toggle_risk(value),
        ),
    )


def filters_panel() -> rx.Component:
    """Advanced filters panel for claims."""
    return rx.vstack(
        # Header
        rx.vstack(
            rx.heading("Filters", size="4", color=COLORS["gray_900"]),
            rx.text(
                "Refine the claim list below. Filters apply instantly across charts and metrics.",
                size="2",
                color=COLORS["gray_500"],
            ),
            spacing="2",
            align="start",
            width="100%",
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
                        on_change=ClaimsState.update_date_start,
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
                        on_change=ClaimsState.update_date_end,
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
                risk_chip("Low (< 0.4)", "low", "green", ClaimsState.risk_low_active),
                risk_chip("Medium (0.4-0.7)", "medium", "orange", ClaimsState.risk_medium_active),
                risk_chip("High (≥ 0.7)", "high", "red", ClaimsState.risk_high_active),
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
                    rx.icon("refresh_cw", size=16),
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
            rx.box(
                filters_panel(),
                padding="4",
                background=COLORS["white"],
                border_radius="0.75rem",
                box_shadow=SHADOWS["lg"],
                width="320px",
            ),
            side="bottom",
            align="end",
        ),
    )
