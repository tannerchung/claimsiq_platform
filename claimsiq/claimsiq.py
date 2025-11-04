import reflex as rx
from claimsiq.pages.dashboard import dashboard

app = rx.App()
app.add_page(dashboard, route="/", title="ClaimsIQ - Dashboard")
