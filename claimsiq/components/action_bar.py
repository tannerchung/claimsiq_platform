"""
Enhanced Action Bar with Theme Toggle and Prominent Actions
"""
import reflex as rx
from claimsiq.theme import COLORS
from claimsiq.state import ClaimsState


def action_bar() -> rx.Component:
    """
    Sticky action bar with:
    - Theme toggle
    - Export actions
    - Refresh button
    - Better visual hierarchy
    """
    return rx.box(
        rx.hstack(
            # Left: Title and last updated
            rx.hstack(
                rx.icon("activity", size=24, color=COLORS["primary"]),
                rx.vstack(
                    rx.heading("ClaimsIQ Dashboard", size="6", weight="bold"),
                    rx.text(
                        rx.cond(
                            ClaimsState.last_updated,
                            f"Last updated: {ClaimsState.last_updated_label}",
                            "Loading...",
                        ),
                        size="1",
                        color=COLORS["gray_600"],
                    ),
                    spacing="0",
                    align="start",
                ),
                spacing="3",
            ),

            rx.spacer(),

            # Right: Actions
            rx.hstack(
                # Refresh button
                rx.button(
                    rx.icon("refresh-cw", size=16),
                    "Refresh Data",
                    on_click=ClaimsState.load_all_data,
                    variant="outline",
                    size="2",
                    color_scheme="gray",
                ),

                # Export CSV button - prominent
                rx.button(
                    rx.icon("download", size=16),
                    "Export CSV",
                    on_click=ClaimsState.export_to_csv,
                    variant="solid",
                    size="2",
                    color_scheme="blue",
                ),

                # Divider
                rx.divider(orientation="vertical", size="4"),

                # Theme toggle
                rx.tooltip(
                    rx.icon_button(
                        rx.icon("moon", size=18),
                        on_click=ClaimsState.toggle_dark_mode,
                        variant="ghost",
                        size="2",
                        color_scheme="gray",
                        aria_label="Toggle dark mode",
                    ),
                    content="Toggle dark/light mode",
                ),

                # Notifications
                rx.tooltip(
                    rx.icon_button(
                        rx.icon("bell", size=18),
                        variant="ghost",
                        size="2",
                        color_scheme="gray",
                        aria_label="Notifications",
                    ),
                    content="Notifications",
                ),

                spacing="3",
                align="center",
            ),

            width="100%",
            align="center",
            justify="between",
        ),
        padding="4",
        background="white",
        border_bottom=f"1px solid {COLORS['gray_200']}",
        position="sticky",
        top="0",
        z_index="50",
        box_shadow=COLORS.get("shadow", "0 1px 3px 0 rgba(0, 0, 0, 0.1)"),
    )


def quick_actions_panel() -> rx.Component:
    """
    Quick actions panel for common operations
    """
    return rx.box(
        rx.vstack(
            rx.text(
                "Quick Actions",
                size="3",
                weight="bold",
                color=COLORS["gray_900"],
            ),

            rx.divider(),

            rx.vstack(
                rx.button(
                    rx.hstack(
                        rx.icon("file-plus", size=16),
                        rx.text("Generate Sample Data", size="2"),
                        spacing="2",
                    ),
                    on_click=lambda: ClaimsState.generate_sample_data(1000),
                    variant="outline",
                    width="100%",
                    justify="start",
                ),

                rx.button(
                    rx.hstack(
                        rx.icon("database", size=16),
                        rx.text("Load Kaggle Dataset", size="2"),
                        spacing="2",
                    ),
                    on_click=ClaimsState.load_kaggle_data,
                    variant="outline",
                    width="100%",
                    justify="start",
                ),

                rx.button(
                    rx.hstack(
                        rx.icon("bar-chart-3", size=16),
                        rx.text("View Analytics", size="2"),
                        spacing="2",
                    ),
                    variant="outline",
                    width="100%",
                    justify="start",
                ),

                spacing="2",
                width="100%",
            ),

            spacing="3",
            align="start",
            width="100%",
        ),
        padding="4",
        background=COLORS["gray_50"],
        border_radius="8px",
        border=f"1px solid {COLORS['gray_200']}",
    )
