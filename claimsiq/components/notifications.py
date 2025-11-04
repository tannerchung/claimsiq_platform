import reflex as rx
from claimsiq.theme import COLORS, SHADOWS
from claimsiq.state import ClaimsState


def notification_toast() -> rx.Component:
    """Toast notification component"""

    # Map notification types to colors
    color_map = {
        "success": COLORS["success"],
        "error": COLORS["danger"],
        "warning": COLORS["warning"],
        "info": COLORS["primary"],
    }

    icon_map = {
        "success": "circle_check",
        "error": "circle_x",
        "warning": "triangle_alert",
        "info": "info",
    }

    return rx.cond(
        ClaimsState.show_notification,
        rx.box(
            rx.hstack(
                rx.icon(
                    icon_map.get(ClaimsState.notification_type, "info"),
                    size=20,
                    color=color_map.get(ClaimsState.notification_type, COLORS["primary"]),
                ),
                rx.text(
                    ClaimsState.notification_message,
                    size="2",
                    weight="medium",
                    color=COLORS["gray_900"],
                ),
                rx.spacer(),
                rx.icon_button(
                    rx.icon("x", size=16),
                    on_click=ClaimsState.hide_notification,
                    variant="ghost",
                    size="1",
                    color=COLORS["gray_500"],
                ),
                spacing="3",
                align="center",
                width="100%",
            ),
            position="fixed",
            top="20px",
            right="20px",
            padding="4",
            background=COLORS["white"],
            border_radius="0.75rem",
            box_shadow=SHADOWS["xl"],
            border=f"1px solid {color_map.get(ClaimsState.notification_type, COLORS['primary'])}",
            min_width="320px",
            max_width="500px",
            z_index="1000",
            animation="slideIn 0.3s ease-out",
        ),
        rx.fragment(),
    )
