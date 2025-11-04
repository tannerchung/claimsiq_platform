import reflex as rx
from claimsiq.theme import COLORS, FONT_SIZES, SPACING

def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.heading("ClaimsIQ", size="6", color=COLORS["primary"]),
            rx.spacer(),
            rx.text("MVP Dashboard", size="2", color=COLORS["gray"]),
            spacing="4",
            align="center",
            width="100%",
        ),
        padding="4",
        background=COLORS["white"],
        box_shadow="0 1px 3px 0 rgba(0, 0, 0, 0.1)",
        width="100%",
    )
