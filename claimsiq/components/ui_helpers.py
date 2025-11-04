import reflex as rx
from claimsiq.theme import COLORS, SHADOWS, SPACING

def empty_state(
    icon: str,
    title: str,
    description: str,
    action_text: str = "",
    on_action=None
) -> rx.Component:
    """Empty state component with icon, title, description, and optional action"""
    return rx.center(
        rx.vstack(
            rx.icon(
                icon,
                size=64,
                color=COLORS["gray_300"],
                stroke_width=1,
            ),
            rx.heading(
                title,
                size="5",
                color=COLORS["gray_700"],
                text_align="center",
            ),
            rx.text(
                description,
                size="3",
                color=COLORS["gray_500"],
                text_align="center",
                max_width="400px",
            ),
            rx.cond(
                action_text != "",
                rx.button(
                    action_text,
                    on_click=on_action,
                    size="3",
                ),
                rx.fragment(),
            ),
            spacing="4",
            align="center",
        ),
        padding="12",
        min_height="400px",
        width="100%",
    )


def skeleton_card() -> rx.Component:
    """Loading skeleton for metric cards"""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.skeleton(
                    height="24px",
                    width="24px",
                    border_radius="0.5rem",
                ),
                rx.spacer(),
                rx.skeleton(
                    height="20px",
                    width="60px",
                    border_radius="0.5rem",
                ),
                width="100%",
            ),
            rx.skeleton(
                height="16px",
                width="60%",
                border_radius="0.25rem",
            ),
            rx.skeleton(
                height="40px",
                width="100%",
                border_radius="0.25rem",
            ),
            spacing="3",
            width="100%",
        ),
        padding="5",
        border_radius="0.75rem",
        background=COLORS["white"],
        box_shadow=SHADOWS["md"],
        width="100%",
    )


def skeleton_table() -> rx.Component:
    """Loading skeleton for tables"""
    return rx.box(
        rx.vstack(
            # Header skeleton
            rx.hstack(
                rx.skeleton(height="32px", width="150px"),
                rx.spacer(),
                rx.skeleton(height="32px", width="200px"),
                width="100%",
            ),
            # Table rows skeleton
            rx.vstack(
                *[
                    rx.skeleton(
                        height="48px",
                        width="100%",
                        border_radius="0.25rem",
                    )
                    for _ in range(5)
                ],
                spacing="2",
                width="100%",
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


def loading_spinner(text: str = "Loading...") -> rx.Component:
    """Centered loading spinner with text"""
    return rx.center(
        rx.vstack(
            rx.spinner(size="3", color=COLORS["primary"]),
            rx.text(
                text,
                size="3",
                color=COLORS["gray_500"],
                weight="medium",
            ),
            spacing="3",
            align="center",
        ),
        padding="12",
        min_height="400px",
        width="100%",
    )


def sortable_header(
    label: str,
    column: str,
    current_column: str,
    current_direction: str,
    on_click,
    class_name: str | None = None,
) -> rx.Component:
    """Sortable table header with indicator"""
    is_active = column == current_column

    return rx.table.column_header_cell(
        rx.hstack(
            rx.text(label, weight="medium"),
            rx.cond(
                is_active,
                rx.cond(
                    current_direction == "desc",
                    rx.icon(
                        "chevron-down",
                        size=14,
                        color=COLORS["primary"],
                    ),
                    rx.icon(
                        "chevron-up",
                        size=14,
                        color=COLORS["primary"],
                    ),
                ),
                rx.icon(
                    "chevron-down",
                    size=14,
                    color=COLORS["gray_300"],
                ),
            ),
            spacing="1",
            align="center",
        ),
        on_click=on_click,
        cursor="pointer",
        _hover={"background": COLORS["gray_50"]},
        class_name=class_name,
    )
