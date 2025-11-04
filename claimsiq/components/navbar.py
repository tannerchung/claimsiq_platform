import reflex as rx
from claimsiq.theme import COLORS, FONT_SIZES, SPACING

def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.heading("ClaimsIQ", size="lg", color=COLORS["primary"]),
            rx.spacer(),
            rx.text("MVP Dashboard", font_size=FONT_SIZES["sm"], color=COLORS["gray"]),
            spacing=SPACING["md"],
            align="center",
            width="100%",
        ),
        padding=SPACING["lg"],
        background=COLORS["white"],
        box_shadow="0 1px 3px 0 rgba(0, 0, 0, 0.1)",
        width="100%",
    )
