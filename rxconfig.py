import reflex as rx

config = rx.Config(
    app_name="claimsiq",
    frontend_port=3000,
    backend_port=8001,
    backend_host="0.0.0.0",
    frontend_host="0.0.0.0",
    tailwind={
        "theme": {
            "extend": {
                "colors": {
                    "primary": "#2563eb",
                    "secondary": "#64748b",
                    "success": "#10b981",
                    "warning": "#f59e0b",
                    "danger": "#ef4444",
                },
            }
        },
        "plugins": ["@tailwindcss/forms", "@tailwindcss/typography"],
    },
    # Enable sitemap plugin (generates sitemap.xml automatically)
    plugins=[
        rx.plugins.SitemapPlugin(),
    ]
)
