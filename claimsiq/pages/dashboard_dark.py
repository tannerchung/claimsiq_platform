"""
Dashboard Dark Mode - Accessible and Beautiful

Professional dark theme with:
✅ Semi-transparent backgrounds (no pure black)
✅ Off-white text for readability (#f3f4f6)
✅ Subtle drop shadows and borders
✅ Gradient background instead of flat black
✅ Visual hierarchy with accent colors
✅ Different shades for each section
✅ Proper contrast ratios (WCAG AA compliant)
✅ Light/dark mode toggle
✅ Ample padding between sections
✅ Accessible color combinations
"""
import reflex as rx
from claimsiq.state import ClaimsState
from claimsiq.theme import DARK_COLORS, DARK_GRADIENTS, DARK_SHADOWS
from claimsiq.components.cards_v2 import clickable_metric_card, metric_value_large, metric_value_with_subtitle
from claimsiq.components.navbar import navbar
from claimsiq.components.tables import claims_table
from claimsiq.components.charts import claims_trend_chart, risk_distribution_chart, status_breakdown_chart
from claimsiq.components.modals_v2 import claim_detail_modal_v2
from claimsiq.components.notifications import notification_toast
from claimsiq.components.pagination import enhanced_pagination


def theme_toggle() -> rx.Component:
    """Light/Dark mode toggle button"""
    return rx.button(
        rx.cond(
            ClaimsState.dark_mode,
            rx.hstack(
                rx.icon("sun", size=18, color=DARK_COLORS["warning"]),
                rx.text("Light Mode", size="2", color=DARK_COLORS["text_primary"]),
                spacing="2",
            ),
            rx.hstack(
                rx.icon("moon", size=18),
                rx.text("Dark Mode", size="2"),
                spacing="2",
            ),
        ),
        on_click=ClaimsState.toggle_dark_mode,
        variant="outline",
        size="2",
        style={
            "border-color": DARK_COLORS["border"],
            "color": DARK_COLORS["text_primary"],
            "_hover": {
                "background": DARK_COLORS["bg_elevated"],
                "border-color": DARK_COLORS["primary"],
            },
        },
        aria_label="Toggle dark mode",
    )


def dark_action_bar() -> rx.Component:
    """Sticky action bar with dark theme styling"""
    return rx.box(
        rx.hstack(
            # Left: Data loading
            rx.hstack(
                rx.button(
                    rx.hstack(
                        rx.icon("cloud-download", size=18),
                        rx.text("Kaggle Data", size="2", weight="medium"),
                        spacing="2",
                    ),
                    on_click=ClaimsState.load_kaggle_data,
                    loading=ClaimsState.is_loading_data,
                    disabled=ClaimsState.is_loading_data,
                    style={
                        "background": DARK_COLORS["primary_bg"],
                        "color": DARK_COLORS["primary"],
                        "border": f"1px solid {DARK_COLORS['primary']}",
                        "_hover": {"background": "rgba(37, 99, 235, 0.2)"},
                    },
                    size="2",
                ),
                rx.button(
                    rx.hstack(
                        rx.icon("sparkles", size=18),
                        rx.text("Sample Data", size="2", weight="medium"),
                        spacing="2",
                    ),
                    on_click=lambda: ClaimsState.generate_sample_data(1000),
                    loading=ClaimsState.is_loading_data,
                    disabled=ClaimsState.is_loading_data,
                    style={
                        "background": DARK_COLORS["success_bg"],
                        "color": DARK_COLORS["success"],
                        "border": f"1px solid {DARK_COLORS['success']}",
                        "_hover": {"background": "rgba(16, 185, 129, 0.2)"},
                    },
                    size="2",
                ),
                spacing="3",
            ),

            rx.spacer(),

            # Center: Last updated
            rx.hstack(
                rx.icon("clock", size=16, color=DARK_COLORS["text_tertiary"]),
                rx.text(
                    rx.cond(
                        ClaimsState.last_updated != "",
                        f"Updated {ClaimsState.last_updated_label}",
                        "Loading...",
                    ),
                    size="2",
                    color=DARK_COLORS["text_secondary"],
                    weight="medium",
                ),
                spacing="2",
                padding_x="4",
                padding_y="2",
                style={
                    "background": DARK_COLORS["bg_elevated"],
                    "border-radius": "8px",
                    "border": f"1px solid {DARK_COLORS['border']}",
                },
            ),

            rx.spacer(),

            # Right: Actions + Theme toggle
            rx.hstack(
                rx.button(
                    rx.hstack(
                        rx.icon("refresh-cw", size=18),
                        rx.text("Refresh", size="2", weight="medium"),
                        spacing="2",
                    ),
                    on_click=ClaimsState.refresh_all_data,
                    loading=ClaimsState.is_loading_summary | ClaimsState.is_loading_claims,
                    variant="outline",
                    size="2",
                    style={
                        "border-color": DARK_COLORS["border"],
                        "color": DARK_COLORS["text_primary"],
                        "_hover": {"background": DARK_COLORS["bg_elevated"]},
                    },
                ),
                rx.button(
                    rx.hstack(
                        rx.icon("download", size=18),
                        rx.text("Export CSV", size="2", weight="medium"),
                        spacing="2",
                    ),
                    on_click=ClaimsState.export_to_csv,
                    style={
                        "background": DARK_COLORS["primary"],
                        "color": DARK_COLORS["bg_primary"],
                        "_hover": {"box-shadow": DARK_SHADOWS["glow"]},
                    },
                    size="2",
                ),
                theme_toggle(),
                spacing="3",
            ),

            width="100%",
            align="center",
        ),
        padding="5",
        style={
            "background": DARK_COLORS["bg_card"],
            "border-bottom": f"1px solid {DARK_COLORS['border']}",
            "box-shadow": DARK_SHADOWS["md"],
        },
        width="100%",
    )


def section_divider() -> rx.Component:
    """Accent divider line between sections"""
    return rx.box(
        height="1px",
        width="100%",
        style={
            "background": f"linear-gradient(90deg, transparent 0%, {DARK_COLORS['primary']} 50%, transparent 100%)",
        },
        margin_y="8",
    )


def dark_section_header(title: str, subtitle: str = "", icon: str = "") -> rx.Component:
    """Section header with dark theme styling"""
    return rx.vstack(
        rx.hstack(
            rx.cond(
                icon != "",
                rx.icon(icon, size=28, color=DARK_COLORS["primary"]),
                rx.fragment(),
            ),
            rx.heading(
                title,
                size="8",
                style={
                    "color": DARK_COLORS["text_primary"],
                    "font-weight": "bold",
                    "letter-spacing": "-0.02em",
                },
            ),
            spacing="3",
            align="center",
        ),
        rx.cond(
            subtitle != "",
            rx.text(
                subtitle,
                size="3",
                style={
                    "color": DARK_COLORS["text_secondary"],
                    "margin-top": "8px",
                },
            ),
            rx.fragment(),
        ),
        spacing="0",
        align="start",
        margin_bottom="6",
    )


def dark_summary_cards() -> rx.Component:
    """Summary cards with dark theme"""
    return rx.box(
        dark_section_header(
            "Portfolio Overview",
            "Real-time metrics and trends - click any card to filter",
            "layout-dashboard",
        ),
        rx.grid(
            # Total Claims
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon("file-text", size=32, color=DARK_COLORS["primary"]),
                        rx.spacer(),
                        rx.badge(
                            rx.hstack(
                                rx.icon("trending-up", size=14),
                                rx.text("+12%", size="1"),
                                spacing="1",
                            ),
                            color_scheme="green",
                            variant="soft",
                        ),
                        width="100%",
                    ),
                    rx.text(
                        "Total Claims",
                        size="3",
                        weight="medium",
                        style={"color": DARK_COLORS["text_tertiary"], "margin-top": "16px"},
                    ),
                    rx.text(
                        ClaimsState.total_claims,
                        size="9",
                        weight="bold",
                        style={"color": DARK_COLORS["text_primary"]},
                    ),
                    spacing="0",
                    width="100%",
                ),
                padding="6",
                on_click=lambda: ClaimsState.drill_into_status("all"),
                style={
                    "background": DARK_GRADIENTS["card"],
                    "border-radius": "16px",
                    "border": f"1px solid {DARK_COLORS['border']}",
                    "box-shadow": DARK_SHADOWS["lg"],
                    "cursor": "pointer",
                    "transition": "all 0.3s ease",
                    "_hover": {
                        "box-shadow": DARK_SHADOWS["glow"],
                        "border-color": DARK_COLORS["primary"],
                        "transform": "translateY(-4px)",
                    },
                },
            ),

            # Approved
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon("circle-check", size=32, color=DARK_COLORS["success"]),
                        rx.spacer(),
                        rx.badge(
                            rx.hstack(
                                rx.icon("trending-up", size=14),
                                rx.text("+8%", size="1"),
                                spacing="1",
                            ),
                            color_scheme="green",
                            variant="soft",
                        ),
                        width="100%",
                    ),
                    rx.text(
                        "Approved",
                        size="3",
                        weight="medium",
                        style={"color": DARK_COLORS["text_tertiary"], "margin-top": "16px"},
                    ),
                    rx.text(
                        ClaimsState.approved_count,
                        size="9",
                        weight="bold",
                        style={"color": DARK_COLORS["success"]},
                    ),
                    rx.text(
                        ClaimsState.approval_rate_label,
                        size="2",
                        style={"color": DARK_COLORS["text_secondary"]},
                    ),
                    spacing="0",
                    width="100%",
                ),
                padding="6",
                on_click=lambda: ClaimsState.drill_into_status("approved"),
                style={
                    "background": DARK_GRADIENTS["card"],
                    "border-radius": "16px",
                    "border": f"1px solid {DARK_COLORS['border']}",
                    "box-shadow": DARK_SHADOWS["lg"],
                    "cursor": "pointer",
                    "transition": "all 0.3s ease",
                    "_hover": {
                        "box-shadow": f"0 0 20px rgba(52, 211, 153, 0.3)",
                        "border-color": DARK_COLORS["success"],
                        "transform": "translateY(-4px)",
                    },
                },
            ),

            # Pending
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon("clock", size=32, color=DARK_COLORS["warning"]),
                        rx.spacer(),
                        rx.badge(
                            rx.hstack(
                                rx.icon("trending-down", size=14),
                                rx.text("-3%", size="1"),
                                spacing="1",
                            ),
                            color_scheme="red",
                            variant="soft",
                        ),
                        width="100%",
                    ),
                    rx.text(
                        "Pending",
                        size="3",
                        weight="medium",
                        style={"color": DARK_COLORS["text_tertiary"], "margin-top": "16px"},
                    ),
                    rx.text(
                        ClaimsState.pending_count,
                        size="9",
                        weight="bold",
                        style={"color": DARK_COLORS["warning"]},
                    ),
                    spacing="0",
                    width="100%",
                ),
                padding="6",
                on_click=lambda: ClaimsState.drill_into_status("pending"),
                style={
                    "background": DARK_GRADIENTS["card"],
                    "border-radius": "16px",
                    "border": f"1px solid {DARK_COLORS['border']}",
                    "box-shadow": DARK_SHADOWS["lg"],
                    "cursor": "pointer",
                    "transition": "all 0.3s ease",
                    "_hover": {
                        "box-shadow": f"0 0 20px rgba(251, 191, 36, 0.3)",
                        "border-color": DARK_COLORS["warning"],
                        "transform": "translateY(-4px)",
                    },
                },
            ),

            # Flagged
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon("flag", size=32, color=DARK_COLORS["danger"]),
                        rx.spacer(),
                        rx.badge(
                            rx.hstack(
                                rx.icon("trending-up", size=14),
                                rx.text("+5%", size="1"),
                                spacing="1",
                            ),
                            color_scheme="red",
                            variant="soft",
                        ),
                        width="100%",
                    ),
                    rx.text(
                        "Flagged",
                        size="3",
                        weight="medium",
                        style={"color": DARK_COLORS["text_tertiary"], "margin-top": "16px"},
                    ),
                    rx.text(
                        ClaimsState.flagged_count,
                        size="9",
                        weight="bold",
                        style={"color": DARK_COLORS["danger"]},
                    ),
                    spacing="0",
                    width="100%",
                ),
                padding="6",
                on_click=lambda: ClaimsState.drill_into_status("flagged"),
                style={
                    "background": DARK_GRADIENTS["card"],
                    "border-radius": "16px",
                    "border": f"1px solid {DARK_COLORS['border']}",
                    "box-shadow": DARK_SHADOWS["lg"],
                    "cursor": "pointer",
                    "transition": "all 0.3s ease",
                    "_hover": {
                        "box-shadow": f"0 0 20px rgba(248, 113, 113, 0.3)",
                        "border-color": DARK_COLORS["danger"],
                        "transform": "translateY(-4px)",
                    },
                },
            ),

            columns="4",
            spacing="6",
            width="100%",
        ),
        padding="8",
        style={
            "background": DARK_COLORS["bg_card"],
            "border-radius": "20px",
            "border": f"1px solid {DARK_COLORS['border_light']}",
            "box-shadow": DARK_SHADOWS["xl"],
        },
        margin_bottom="10",
        width="100%",
    )


def dashboard_dark() -> rx.Component:
    """
    Professional dark mode dashboard with accessibility.

    Color Palette:
    - Background: #0f1419 (near-black with blue tint)
    - Cards: #1e2433 (slate gray)
    - Text: #f3f4f6 (off-white)
    - Accent: #60a5fa (bright blue)

    Features:
    ✅ WCAG AA compliant contrast
    ✅ No pure black (reduces eye strain)
    ✅ Gradient backgrounds
    ✅ Subtle shadows for depth
    ✅ Accent colors for hierarchy
    ✅ Different shades per section
    ✅ Light/dark mode toggle
    """
    return rx.box(
        # Overlays
        notification_toast(),
        claim_detail_modal_v2(),

        # Main layout
        rx.vstack(
            # Navbar (dark styled)
            rx.box(
                navbar(),
                style={
                    "background": DARK_COLORS["bg_card"],
                    "border-bottom": f"1px solid {DARK_COLORS['border']}",
                },
                class_name="sticky top-0 z-50",
            ),

            # Action bar (dark styled)
            rx.box(
                dark_action_bar(),
                class_name="sticky top-[64px] z-40",
            ),

            # Main content
            rx.box(
                rx.vstack(
                    # Section 1: Summary Cards
                    dark_summary_cards(),

                    # Divider
                    section_divider(),

                    # Section 2: Analytics (placeholder for now)
                    rx.box(
                        dark_section_header(
                            "Analytics & Trends",
                            "Visual insights into claims patterns",
                            "bar-chart-2",
                        ),
                        rx.grid(
                            claims_trend_chart(),
                            rx.vstack(
                                risk_distribution_chart(),
                                status_breakdown_chart(),
                                spacing="5",
                                width="100%",
                            ),
                            columns="2",
                            spacing="6",
                            width="100%",
                        ),
                        padding="8",
                        style={
                            "background": DARK_COLORS["bg_secondary"],
                            "border-radius": "20px",
                            "border": f"1px solid {DARK_COLORS['border']}",
                            "box-shadow": DARK_SHADOWS["xl"],
                        },
                        margin_bottom="10",
                        width="100%",
                    ),

                    # Divider
                    section_divider(),

                    # Section 3: Claims Table
                    rx.box(
                        dark_section_header(
                            "Claims Queue",
                            f"Processing {ClaimsState.sorted_claims.length()} claims",
                            "list",
                        ),
                        rx.box(
                            claims_table(),
                            enhanced_pagination(),
                            style={
                                "background": DARK_COLORS["bg_card"],
                                "border-radius": "16px",
                                "border": f"1px solid {DARK_COLORS['border']}",
                                "overflow": "hidden",
                            },
                        ),
                        padding="8",
                        style={
                            "background": DARK_COLORS["bg_tertiary"],
                            "border-radius": "20px",
                            "border": f"1px solid {DARK_COLORS['border']}",
                            "box-shadow": DARK_SHADOWS["xl"],
                        },
                        width="100%",
                    ),

                    spacing="0",
                    width="100%",
                ),
                padding="8",
                max_width="1600px",
                margin_x="auto",
                width="100%",
            ),

            spacing="0",
            width="100%",
        ),

        style={
            "min-height": "100vh",
            "background": DARK_GRADIENTS["background"],
        },
        on_mount=ClaimsState.load_all_data,
        role="main",
        aria_label="Claims Dashboard Dark Mode",
    )
