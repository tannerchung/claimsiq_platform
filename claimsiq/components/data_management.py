"""
Data Management Component

UI controls for loading Kaggle data, generating sample data, and clearing data.
"""

import reflex as rx
from claimsiq.state import ClaimsState
from claimsiq.theme import COLORS


def data_management_panel() -> rx.Component:
    """Primary data management panel used on the dashboard."""
    header = rx.hstack(
        rx.icon("database", size=20, color=COLORS["primary"]),
        rx.heading("Data Management", size="4", class_name="text-lg font-semibold text-slate-800 dark:text-slate-100"),
        spacing="2",
        align="center",
    )

    description = rx.text(
        "Load real insurance data from Kaggle or generate synthetic records for demos.",
        size="2",
        class_name="text-sm text-slate-500 dark:text-slate-300",
    )

    actions = rx.vstack(
        rx.button(
            rx.hstack(
                rx.icon("cloud-download", size=16),
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
                rx.icon("sparkles", size=16),
                rx.text("Generate Sample Data"),
                spacing="2",
            ),
            on_click=ClaimsState.generate_sample_data(1000),
            loading=ClaimsState.is_loading_data,
            disabled=ClaimsState.is_loading_data,
            color_scheme="green",
            variant="soft",
            size="3",
            width="100%",
        ),
        rx.button(
            rx.hstack(
                rx.icon("trash-2", size=16),
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
    )

    helper_box = rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon("info", size=14, color=COLORS["primary"]),
                rx.text("Kaggle dataset requires API token (see KAGGLE_SETUP.md).", size="1", class_name="text-xs text-slate-500 dark:text-slate-300"),
                spacing="2",
                align="center",
            ),
            rx.hstack(
                rx.icon("info", size=14, color=COLORS["success"]),
                rx.text("Sample data generates 1,000 demo-friendly claims.", size="1", class_name="text-xs text-slate-500 dark:text-slate-300"),
                spacing="2",
                align="center",
            ),
            spacing="1",
            align="start",
        ),
        padding="3",
        class_name="bg-slate-50/80 dark:bg-slate-800/60 border border-slate-200/70 dark:border-slate-700/60 rounded-xl",
        width="100%",
    )

    disabled_message = rx.callout(
        "Data operations are disabled in this environment.",
        icon="shield-alert",
        color_scheme="blue",
        variant="soft",
    )

    enabled_body = rx.vstack(
        header,
        description,
        actions,
        helper_box,
        spacing="4",
        width="100%",
    )

    disabled_body = rx.vstack(
        header,
        description,
        disabled_message,
        spacing="4",
        width="100%",
    )

    return rx.box(
        rx.cond(ClaimsState.data_ops_enabled, enabled_body, disabled_body),
        padding="6",
        class_name="w-full bg-white/90 dark:bg-slate-800/95 border border-slate-200/70 dark:border-slate-700/60 rounded-2xl shadow-md backdrop-blur",
    )


def compact_data_buttons() -> rx.Component:
    """Compact action buttons rendered in the header."""
    return rx.cond(
        ClaimsState.data_ops_enabled,
        rx.hstack(
            rx.button(
                rx.hstack(
                    rx.icon("cloud-download", size=16),
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
                on_click=ClaimsState.generate_sample_data(1000),
                loading=ClaimsState.is_loading_data,
                disabled=ClaimsState.is_loading_data,
                color_scheme="green",
                variant="soft",
                size="2",
            ),
            spacing="2",
        ),
        rx.fragment(),
    )
