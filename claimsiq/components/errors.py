"""
Enhanced Error Messaging Components

Provides visible, actionable error messages with:
- Color-coded severity (error, warning, info)
- Icons for visual emphasis
- Retry buttons for failed actions
- Troubleshooting tips
"""
import reflex as rx
from claimsiq.theme import COLORS
from claimsiq.state import ClaimsState


def error_callout_with_retry(
    message: str,
    action_text: str = "Retry",
    on_retry = None,
    troubleshooting: str = "",
) -> rx.Component:
    """
    Enhanced error callout with retry button and troubleshooting tips.

    Args:
        message: Error message to display
        action_text: Text for the retry button
        on_retry: Function to call when retry is clicked
        troubleshooting: Optional troubleshooting tip
    """
    return rx.box(
        rx.vstack(
            # Error header with icon
            rx.hstack(
                rx.icon("circle-alert", size=24, color=COLORS["danger"]),
                rx.heading(
                    "Error",
                    size="4",
                    color=COLORS["danger"],
                ),
                spacing="2",
                align="center",
                margin_bottom="2",
            ),

            # Error message
            rx.text(
                message,
                size="2",
                color=COLORS["gray_900"],
                weight="medium",
                margin_bottom="3",
            ),

            # Troubleshooting tip (if provided)
            rx.cond(
                troubleshooting != "",
                rx.box(
                    rx.hstack(
                        rx.icon("lightbulb", size=16, color=COLORS["primary"]),
                        rx.text(
                            "Tip:",
                            size="2",
                            weight="bold",
                            color=COLORS["primary"],
                        ),
                        spacing="1",
                        margin_bottom="1",
                    ),
                    rx.text(
                        troubleshooting,
                        size="2",
                        color=COLORS["gray_700"],
                    ),
                    padding="3",
                    class_name="bg-blue-50 rounded-lg border border-blue-200",
                    margin_bottom="3",
                ),
                rx.fragment(),
            ),

            # Action buttons
            rx.hstack(
                rx.button(
                    rx.hstack(
                        rx.icon("refresh-cw", size=16),
                        rx.text(action_text, size="2"),
                        spacing="2",
                    ),
                    on_click=on_retry if on_retry else ClaimsState.load_all_data,
                    color_scheme="red",
                    size="2",
                ),
                rx.button(
                    rx.hstack(
                        rx.icon("x", size=16),
                        rx.text("Dismiss", size="2"),
                        spacing="2",
                    ),
                    on_click=lambda: ClaimsState.set_error_message(""),
                    variant="outline",
                    color_scheme="gray",
                    size="2",
                ),
                spacing="2",
            ),

            spacing="0",
            align="start",
            width="100%",
        ),
        padding="4",
        class_name="bg-red-50 border-2 border-red-300 rounded-xl shadow-md",
        margin_bottom="4",
        width="100%",
    )


def data_load_error() -> rx.Component:
    """Specific error for data loading failures with actionable steps"""
    return error_callout_with_retry(
        message="Failed to load data from the API server.",
        action_text="Retry Loading Data",
        on_retry=ClaimsState.load_all_data,
        troubleshooting="Check that the FastAPI backend is running on port 8000. Run: uvicorn backend.app:app --port 8000",
    )


def sample_data_error() -> rx.Component:
    """Error for sample data generation with helpful tips"""
    return error_callout_with_retry(
        message="Failed to generate sample data.",
        action_text="Try Again",
        on_retry=lambda: ClaimsState.generate_sample_data(1000),
        troubleshooting="The backend API may not be responding. Check that uvicorn is running and /api/data/generate-sample is accessible.",
    )


def enhanced_error_display() -> rx.Component:
    """
    Enhanced error display that shows appropriate error based on error message.
    Replaces the simple callout in dashboard.
    """
    return rx.cond(
        ClaimsState.error_message != "",
        error_callout_with_retry(
            message=ClaimsState.error_message,
            action_text="Retry",
            on_retry=ClaimsState.load_all_data,
            troubleshooting="Check that the FastAPI backend is running on port 8000. If the error persists, check the browser console and API logs for more details.",
        ),
        rx.fragment(),
    )


def set_error_message(message: str):
    """Helper to set error message in state"""
    ClaimsState.error_message = message
