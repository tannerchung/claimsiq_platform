import reflex as rx
from claimsiq.theme import COLORS, FONT_SIZES, SPACING, SHADOWS, DARK_COLORS
from claimsiq.state import ClaimsState

def nav_link(label: str, href: str, icon: str, is_active: bool = False, dark_mode: bool = False) -> rx.Component:
    """Navigation link with icon and hover effect"""
    if dark_mode:
        return rx.link(
            rx.hstack(
                rx.icon(icon, size=18),
                rx.text(label, size="2", weight="medium"),
                spacing="2",
                align="center",
            ),
            href=href,
            style={
                "padding": "8px 16px",
                "border-radius": "8px",
                "color": DARK_COLORS["primary"] if is_active else DARK_COLORS["text_secondary"],
                "background": DARK_COLORS["bg_elevated"] if is_active else "transparent",
                "_hover": {
                    "background": DARK_COLORS["bg_elevated"],
                    "color": DARK_COLORS["primary"],
                },
            },
        )
    else:
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

def navbar(dark_mode: bool = False) -> rx.Component:
    """Navbar with optional dark mode styling"""
    if dark_mode:
        return rx.box(
            rx.hstack(
                # Logo section
                rx.hstack(
                    rx.icon("activity", size=28, color=DARK_COLORS["primary"]),
                    rx.heading("ClaimsIQ", size="6", style={"color": DARK_COLORS["text_primary"]}),
                    spacing="2",
                    align="center",
                ),

                # Navigation links
                rx.hstack(
                    nav_link("Dashboard", "/dark", "home", is_active=True, dark_mode=True),
                    spacing="1",
                    display=["none", "none", "flex"],
                ),

                rx.spacer(),

                # Right side actions
                rx.hstack(
                    # Search bar
                    rx.input(
                        placeholder="Search claims...",
                        size="2",
                        width="250px",
                        display=["none", "none", "block"],
                        style={
                            "background": DARK_COLORS["bg_elevated"],
                            "border-color": DARK_COLORS["border"],
                            "color": DARK_COLORS["text_primary"],
                        },
                    ),
                    # Dark mode toggle
                    rx.icon_button(
                        rx.cond(
                            ClaimsState.dark_mode,
                            rx.icon("sun", size=20),
                            rx.icon("moon", size=20),
                        ),
                        on_click=ClaimsState.toggle_dark_mode,
                        variant="ghost",
                        size="3",
                        style={"color": DARK_COLORS["text_secondary"]},
                    ),
                    # Notifications
                    rx.icon_button(
                        rx.icon("bell", size=20),
                        variant="ghost",
                        size="3",
                        style={"color": DARK_COLORS["text_secondary"]},
                    ),
                    # User menu
                    rx.menu.root(
                        rx.menu.trigger(
                            rx.avatar(
                                fallback="U",
                                size="2",
                                color=DARK_COLORS["primary"],
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
            style={
                "padding": "16px 64px",  # Match main content padding
                "background": DARK_COLORS["bg_card"],
                "border-bottom": f"1px solid {DARK_COLORS['border']}",
            },
            max_width="1600px",  # Match main content max-width
            margin_x="auto",
            width="100%",
        )
    else:
        return rx.box(
            rx.hstack(
                # Logo section
                rx.hstack(
                    rx.icon("activity", size=28, color=COLORS["primary"]),
                    rx.heading("ClaimsIQ", size="6", class_name="text-primary"),
                    spacing="2",
                    align="center",
                    class_name="flex items-center gap-2",
                ),

                # Navigation links (Claims, Analytics, Providers pages coming soon)
                rx.hstack(
                    nav_link("Dashboard", "/", "home", is_active=True),
                    # nav_link("Claims", "/claims", "file-text"),
                    # nav_link("Analytics", "/analytics", "bar-chart-2"),
                    # nav_link("Providers", "/providers", "users"),
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
                            ClaimsState.dark_mode,
                            rx.icon("sun", size=20),
                            rx.icon("moon", size=20),
                        ),
                        on_click=ClaimsState.toggle_dark_mode,
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
                class_name="flex items-center justify-between gap-6 w-full",
            ),
            class_name="px-4 py-4 bg-white shadow-sm border-b border-gray-200 w-full sticky top-0 z-50",
        )
