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
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.icon("database", size=24, color=COLORS["primary"]),
                rx.heading("Data Management", size="5", color=COLORS["gray_900"]),
                spacing="2",
                align="center",
            ),

            # Description
            rx.text(
                "Load real insurance data from Kaggle or generate synthetic data for testing.",
                size="2",
                color=COLORS["gray_600"],
            ),

            # Action buttons
            rx.hstack(
                # Load Kaggle Data button
                rx.button(
                    rx.hstack(
                        rx.icon("download-cloud", size=18),
                        rx.text("Load Kaggle Data"),
                        spacing="2",
                    ),
                    on_click=ClaimsState.load_kaggle_data,
                    loading=ClaimsState.is_loading_data,
                    disabled=ClaimsState.is_loading_data,
                    color_scheme="blue",
                    size="3",
                ),

                # Generate Sample Data button
                rx.button(
                    rx.hstack(
                        rx.icon("sparkles", size=18),
                        rx.text("Generate Sample Data"),
                        spacing="2",
                    ),
                    on_click=lambda: ClaimsState.generate_sample_data(1000),
                    loading=ClaimsState.is_loading_data,
                    disabled=ClaimsState.is_loading_data,
                    color_scheme="green",
                    variant="soft",
                    size="3",
                ),

                # Clear Data button
                rx.button(
                    rx.hstack(
                        rx.icon("trash-2", size=18),
                        rx.text("Clear All Data"),
                        spacing="2",
                    ),
                    on_click=ClaimsState.clear_all_data,
                    loading=ClaimsState.is_loading_data,
                    disabled=ClaimsState.is_loading_data,
                    color_scheme="red",
                    variant="outline",
                    size="3",
                ),

                spacing="3",
                wrap="wrap",
            ),

            # Help text
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon("info", size=16, color=COLORS["primary"]),
                        rx.text("Kaggle Data:", weight="bold", size="2"),
                        spacing="1",
                    ),
                    rx.text(
                        "Downloads real insurance claims from ravalsmit/insurance-claims-and-policy-data. "
                        "Requires kaggle.json configuration (see KAGGLE_SETUP.md).",
                        size="2",
                        color=COLORS["gray_600"],
                    ),
                    rx.hstack(
                        rx.icon("info", size=16, color=COLORS["success"]),
                        rx.text("Sample Data:", weight="bold", size="2"),
                        spacing="1",
                    ),
                    rx.text(
                        "Generates 1,000 realistic synthetic claims with ICD-10 codes, CPT codes, "
                        "patient demographics, and processing metrics.",
                        size="2",
                        color=COLORS["gray_600"],
                    ),
                    spacing="2",
                ),
                padding="3",
                background=COLORS["gray_50"],
                border_radius="0.5rem",
                border=f"1px solid {COLORS['gray_200']}",
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


def compact_data_buttons() -> rx.Component:
    """
    Compact version with just action buttons for the navbar or header.
    """
    return rx.hstack(
        rx.button(
            rx.hstack(
                rx.icon("download-cloud", size=16),
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
                rx.icon("sparkles", size=16),
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
