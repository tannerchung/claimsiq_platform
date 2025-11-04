import reflex as rx

config = rx.Config(
    app_name="claimsiq",
    frontend_port=5000,
    backend_port=8001,
    backend_host="0.0.0.0",
    frontend_host="0.0.0.0",
    tailwind={},
    # Enable sitemap plugin (generates sitemap.xml automatically)
    plugins=[
        rx.plugins.SitemapPlugin(),
    ]
)
