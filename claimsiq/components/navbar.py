import reflex as rx
from claimsiq.theme import COLORS, FONT_SIZES, SPACING, SHADOWS

def nav_link(label: str, href: str, icon: str, is_active: bool = False) -> rx.Component:
    """Navigation link with icon and hover effect"""
    return rx.link(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(label, size="2", weight="medium"),
            spacing="2",
            align="center",
        ),
        href=href,
        padding="2",
        border_radius="0.5rem",
        color=COLORS["primary"] if is_active else COLORS["gray_700"],
        background=COLORS["gray_100"] if is_active else "transparent",
        _hover={
            "background": COLORS["gray_100"],
            "color": COLORS["primary"],
        },
    )

def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            # Logo section
            rx.hstack(
                rx.icon("activity", size=28, color=COLORS["primary"]),
                rx.heading("ClaimsIQ", size="6", color=COLORS["primary"]),
                spacing="2",
                align="center",
            ),

            # Navigation links
            rx.hstack(
                nav_link("Dashboard", "/", "home", is_active=True),
                nav_link("Claims", "/claims", "file-text"),
                nav_link("Analytics", "/analytics", "bar-chart-2"),
                nav_link("Providers", "/providers", "users"),
                spacing="1",
                display=["none", "none", "flex"],  # Hide on mobile
            ),

            rx.spacer(),

            # Right side actions
            rx.hstack(
                # Search bar
                rx.input(
                    placeholder="Search claims...",
                    size="2",
                    width="250px",
                    display=["none", "none", "block"],  # Hide on mobile
                ),
                # Dark mode toggle
                rx.icon_button(
                    rx.cond(
                        rx.State.dark_mode,
                        rx.icon("sun", size=20),
                        rx.icon("moon", size=20),
                    ),
                    on_click=rx.State.toggle_dark_mode,
                    variant="ghost",
                    size="3",
                    color=COLORS["gray_600"],
                ),
                # Notifications
                rx.icon_button(
                    rx.icon("bell", size=20),
                    variant="ghost",
                    size="3",
                    color=COLORS["gray_600"],
                ),
                # User menu
                rx.menu.root(
                    rx.menu.trigger(
                        rx.avatar(
                            fallback="U",
                            size="2",
                            color=COLORS["primary"],
                        )
                    ),
                    rx.menu.content(
                        rx.menu.item("Profile", shortcut="⌘P"),
                        rx.menu.item("Settings", shortcut="⌘S"),
                        rx.menu.separator(),
                        rx.menu.item("Logout", color="red"),
                    ),
                ),
                spacing="3",
                align="center",
            ),

            spacing="6",
            align="center",
            width="100%",
        ),
        padding="4",
        background=COLORS["white"],
        box_shadow=SHADOWS["sm"],
        border_bottom=f"1px solid {COLORS['gray_200']}",
        width="100%",
        position="sticky",
        top="0",
        z_index="50",
    )
