"""
Data Management Component

UI controls for loading Kaggle data, generating sample data, and clearing data.
"""

import reflex as rx
from claimsiq.state import ClaimsState
from claimsiq.theme import COLORS, SHADOWS

def data_management_panel() -> rx.Component:
    """
    Data management panel with buttons for:
    - Load Kaggle Data
    - Generate Sample Data
    - Clear All Data
    """
    return rx.vstack(
        # Header
        rx.hstack(
            rx.icon("database", size=20, color=COLORS["primary"]),
            rx.heading("Data Management", size="4", color=COLORS["gray_900"]),
            spacing="2",
            align="center",
        ),

        rx.text(
            "Load real insurance data from Kaggle or generate synthetic records for demos.",
            size="2",
            color=COLORS["gray_600"],
        ),

        rx.vstack(
            rx.button(
                rx.hstack(
                    rx.icon("cloud_download", size=16),
                    rx.text("Load Kaggle Data"),
                    spacing="2",
                ),
                on_click=ClaimsState.load_kaggle_data,
                loading=ClaimsState.is_loading_data,
                disabled=ClaimsState.is_loading_data,
                color_scheme="blue",
                size="3",
                width="100%",
            ),
            rx.button(
                rx.hstack(
                    rx.icon("sparkle", size=16),
                    rx.text("Generate Sample Data"),
                    spacing="2",
                ),
                on_click=lambda: ClaimsState.generate_sample_data(1000),
                loading=ClaimsState.is_loading_data,
                disabled=ClaimsState.is_loading_data,
                color_scheme="green",
                variant="soft",
                size="3",
                width="100%",
            ),
            rx.button(
                rx.hstack(
                    rx.icon("trash_2", size=16),
                    rx.text("Clear All Data"),
                    spacing="2",
                ),
                on_click=ClaimsState.clear_all_data,
                loading=ClaimsState.is_loading_data,
                disabled=ClaimsState.is_loading_data,
                color_scheme="red",
                variant="outline",
                size="3",
                width="100%",
            ),
            spacing="2",
            width="100%",
        ),

        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.icon("info", size=14, color=COLORS["primary"]),
                    rx.text("Kaggle dataset requires API token (see KAGGLE_SETUP.md).", size="1", color=COLORS["gray_600"]),
                    spacing="2",
                    align="center",
                ),
                rx.hstack(
                    rx.icon("info", size=14, color=COLORS["success"]),
                    rx.text("Sample data generates 1,000 demo-friendly claims.", size="1", color=COLORS["gray_600"]),
                    spacing="2",
                    align="center",
                ),
                spacing="1",
                align="start",
            ),
            padding="3",
            background=COLORS["gray_50"],
            border_radius="0.5rem",
            border=f"1px solid {COLORS['gray_200']}",
            width="100%",
        ),

        spacing="4",
        width="100%",
    )


def compact_data_buttons() -> rx.Component:
    """
    Compact version with just action buttons for the navbar or header.
    """
    return rx.hstack(
        rx.button(
            rx.hstack(
                rx.icon("cloud_download", size=16),
                rx.text("Kaggle", size="2"),
                spacing="1",
            ),
            on_click=ClaimsState.load_kaggle_data,
            loading=ClaimsState.is_loading_data,
            disabled=ClaimsState.is_loading_data,
            color_scheme="blue",
            variant="soft",
            size="2",
        ),
        rx.button(
            rx.hstack(
                rx.icon("sparkle", size=16),
                rx.text("Sample", size="2"),
                spacing="1",
            ),
            on_click=lambda: ClaimsState.generate_sample_data(1000),
            loading=ClaimsState.is_loading_data,
            disabled=ClaimsState.is_loading_data,
            color_scheme="green",
            variant="soft",
            size="2",
        ),
        spacing="2",
    )
