import reflex as rx
from claimsiq.theme import COLORS, FONT_SIZES, SPACING

def metric_card(label: str, value: str, color: str = COLORS["primary"]) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(label, size="2", color=COLORS["gray"]),
            rx.text(value, size="7", weight="bold", color=color),
            spacing="2",
            align="start",
        ),
        padding="4",
        border_radius="0.5rem",
        background=COLORS["white"],
        box_shadow="0 1px 3px 0 rgba(0, 0, 0, 0.1)",
        width="100%",
    )
