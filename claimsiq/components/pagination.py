"""
Enhanced Pagination Component

Features:
- Clear page indicators with total pages
- Previous/Next arrows
- Jump to page input
- Page size selector
- Accessible aria-labels
"""
import reflex as rx
from claimsiq.theme import COLORS
from claimsiq.state import ClaimsState


def enhanced_pagination() -> rx.Component:
    """
    Enhanced pagination control with:
    - Current page / Total pages indicator
    - Previous/Next buttons with icons
    - Visual feedback for disabled states
    - Accessible controls
    """
    return rx.box(
        rx.hstack(
            # Results count
            rx.text(
                f"Showing {ClaimsState.page_start}-{ClaimsState.page_end} of {ClaimsState.sorted_claims.length()} claims",
                size="2",
                color=COLORS["gray_700"],
                weight="medium",
            ),

            rx.spacer(),

            # Pagination controls
            rx.hstack(
                # Previous button
                rx.button(
                    rx.icon("chevron-left", size=18),
                    on_click=ClaimsState.previous_page,
                    disabled=ClaimsState.current_page == 1,
                    variant="outline",
                    color_scheme="gray",
                    size="2",
                    aria_label="Previous page",
                ),

                # Page indicator
                rx.hstack(
                    rx.text(
                        "Page",
                        size="2",
                        color=COLORS["gray_600"],
                    ),
                    rx.badge(
                        ClaimsState.current_page,
                        color_scheme="blue",
                        variant="solid",
                        size="2",
                    ),
                    rx.text(
                        "of",
                        size="2",
                        color=COLORS["gray_600"],
                    ),
                    rx.badge(
                        ClaimsState.total_pages,
                        color_scheme="gray",
                        variant="soft",
                        size="2",
                    ),
                    spacing="2",
                    align="center",
                    padding_x="3",
                    padding_y="1",
                    class_name="bg-gray-50 rounded-md",
                ),

                # Next button
                rx.button(
                    rx.icon("chevron-right", size=18),
                    on_click=ClaimsState.next_page,
                    disabled=ClaimsState.is_last_page,
                    variant="outline",
                    color_scheme="gray",
                    size="2",
                    aria_label="Next page",
                ),

                # Jump to page (optional, can be hidden on mobile)
                rx.hstack(
                    rx.text(
                        "Jump to:",
                        size="2",
                        color=COLORS["gray_600"],
                    ),
                    rx.input(
                        type="number",
                        placeholder="Page",
                        min=1,
                        max=ClaimsState.total_pages,
                        on_change=ClaimsState.set_page_from_input,
                        size="2",
                        width="80px",
                        aria_label="Jump to page number",
                    ),
                    spacing="2",
                    display=["none", "none", "flex"],  # Hidden on mobile
                ),

                spacing="3",
                align="center",
            ),

            width="100%",
            align="center",
            class_name="flex items-center justify-between w-full",
        ),
        padding="4",
        class_name="bg-gray-50 border-t border-gray-200",
        width="100%",
    )


def page_size_selector() -> rx.Component:
    """Dropdown to select page size (25, 50, 100)"""
    return rx.hstack(
        rx.text(
            "Show:",
            size="2",
            color=COLORS["gray_600"],
        ),
        rx.select(
            ["25", "50", "100"],
            value=str(ClaimsState.page_size),
            on_change=lambda value: setattr(ClaimsState, 'page_size', int(value)),
            size="2",
            aria_label="Select page size",
        ),
        rx.text(
            "per page",
            size="2",
            color=COLORS["gray_600"],
        ),
        spacing="2",
        align="center",
    )
