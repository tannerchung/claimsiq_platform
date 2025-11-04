import reflex as rx

config = rx.Config(
    app_name="claimsiq",
    api_url="http://localhost:8000",
    frontend_port=5000,
    backend_port=8001,
    backend_host="0.0.0.0",
    frontend_host="0.0.0.0",
    tailwind={}
)
