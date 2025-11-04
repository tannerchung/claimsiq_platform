import reflex as rx
import plotly.graph_objects as go
from claimsiq.theme import COLORS
from typing import List, Dict

def claims_trend_chart(data: List[Dict] = None) -> rx.Component:
    """Area chart showing claims over time"""

    # Sample data for demonstration
    if not data:
        data = [
            {"date": "Jan", "count": 120},
            {"date": "Feb", "count": 145},
            {"date": "Mar", "count": 132},
            {"date": "Apr", "count": 168},
            {"date": "May", "count": 195},
            {"date": "Jun", "count": 178},
        ]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=[d["date"] for d in data],
        y=[d["count"] for d in data],
        mode='lines',
        fill='tozeroy',
        line=dict(color=COLORS["primary"], width=3),
        fillcolor=f"rgba(37, 99, 235, 0.1)",
        name='Claims'
    ))

    fig.update_layout(
        title=None,
        xaxis_title="Month",
        yaxis_title="Claims",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", size=12, color=COLORS["gray_700"]),
        margin=dict(l=40, r=20, t=20, b=40),
        height=300,
        hovermode='x unified',
        xaxis=dict(
            showgrid=False,
            zeroline=False,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=COLORS["gray_200"],
            zeroline=False,
        ),
    )

    first_value = data[0]["count"]
    last_value = data[-1]["count"]
    delta = last_value - first_value
    delta_text = f"{abs(delta)} increase" if delta >= 0 else f"{abs(delta)} decrease"
    delta_prefix = "↗︎" if delta >= 0 else "↘︎"

    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading("Claims Trend", size="5", color=COLORS["gray_900"]),
                rx.spacer(),
                rx.badge("Last 6 months", color_scheme="blue", variant="soft"),
                width="100%",
                align="center",
                class_name="flex items-center justify-between w-full",
                margin_bottom="4",
            ),
            rx.plotly(data=fig, aria_label="Line chart showing claim volume trend over time"),
            rx.text(
                f"{delta_prefix} {delta_text} between {data[0]['date']} and {data[-1]['date']}. Hover to see monthly counts.",
                size="1",
                color=COLORS["gray_500"],
                margin_top="3",
            ),
            spacing="0",
            width="100%",
        ),
        padding="6",
        class_name="bg-white rounded-xl shadow-md w-full",
    )


def risk_distribution_chart(data: Dict = None) -> rx.Component:
    """Pie chart showing risk distribution"""

    # Sample data for demonstration
    if not data:
        data = {
            "low": 450,
            "medium": 320,
            "high": 230,
        }

    labels = ["Low Risk", "Medium Risk", "High Risk"]
    values = [data.get("low", 0), data.get("medium", 0), data.get("high", 0)]
    colors = [COLORS["success"], COLORS["warning"], COLORS["danger"]]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        hole=0.4,
        textinfo='label+percent',
        textfont=dict(size=12, color="white"),
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percent: %{percent}<extra></extra>',
    )])

    fig.update_layout(
        title=None,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", size=12, color=COLORS["gray_700"]),
        margin=dict(l=20, r=20, t=20, b=20),
        height=300,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
    )

    dominant_label = labels[values.index(max(values))] if values else "No data"

    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading("Risk Distribution", size="5", color=COLORS["gray_900"]),
                rx.spacer(),
                rx.text(
                    f"{sum(values)} total",
                    size="2",
                    color=COLORS["gray_500"],
                    weight="medium",
                    class_name="text-gray-500 font-medium",
                ),
                width="100%",
                align="center",
                class_name="flex items-center justify-between w-full",
                margin_bottom="4",
            ),
            rx.plotly(data=fig, aria_label="Donut chart showing risk distribution of claims"),
            rx.text(
                f"{dominant_label} represents the largest share. Use risk filters to drill into specific segments.",
                size="1",
                color=COLORS["gray_500"],
                margin_top="3",
            ),
            spacing="0",
            width="100%",
        ),
        padding="6",
        class_name="bg-white rounded-xl shadow-md w-full",
    )


def status_breakdown_chart(data: Dict = None) -> rx.Component:
    """Bar chart showing status breakdown"""

    # Sample data for demonstration
    if not data:
        data = {
            "approved": 520,
            "pending": 280,
            "denied": 120,
            "flagged": 80,
        }

    statuses = ["Approved", "Pending", "Denied", "Flagged"]
    values = [
        data.get("approved", 0),
        data.get("pending", 0),
        data.get("denied", 0),
        data.get("flagged", 0),
    ]
    colors = [
        COLORS["success"],
        COLORS["primary"],
        COLORS["danger"],
        COLORS["warning"],
    ]

    fig = go.Figure(data=[go.Bar(
        x=statuses,
        y=values,
        marker=dict(color=colors),
        text=values,
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>',
    )])

    fig.update_layout(
        title=None,
        xaxis_title="Status",
        yaxis_title="Count",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", size=12, color=COLORS["gray_700"]),
        margin=dict(l=40, r=20, t=20, b=40),
        height=300,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=COLORS["gray_200"],
            zeroline=False,
        ),
    )

    top_status = statuses[values.index(max(values))] if values else "No status"

    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading("Status Breakdown", size="5", color=COLORS["gray_900"]),
                rx.spacer(),
                rx.badge(
                    f"{sum(values)} total",
                    color_scheme="gray",
                    variant="soft",
                ),
                width="100%",
                align="center",
                class_name="flex items-center justify-between w-full",
                margin_bottom="4",
            ),
            rx.plotly(data=fig, aria_label="Bar chart showing counts by claim status"),
            rx.text(
                f"{top_status} leads this period. Compare bars to spot bottlenecks or review flagged claims.",
                size="1",
                color=COLORS["gray_500"],
                margin_top="3",
            ),
            spacing="0",
            width="100%",
        ),
        padding="6",
        class_name="bg-white rounded-xl shadow-md w-full",
    )
