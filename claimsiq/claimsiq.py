import reflex as rx
from claimsiq.pages.dashboard import dashboard
from claimsiq.pages.dashboard_v2 import dashboard_v2
from claimsiq.pages.dashboard_v3 import dashboard_v3
from claimsiq.pages.dashboard_v4 import dashboard_v4
from claimsiq.pages.dashboard_dark import dashboard_dark

app = rx.App()
app.add_page(dashboard, route="/", title="ClaimsIQ - Dashboard")
app.add_page(dashboard_v2, route="/v2", title="ClaimsIQ - Dashboard V2")
app.add_page(dashboard_v3, route="/v3", title="ClaimsIQ - Dashboard V3")
app.add_page(dashboard_v4, route="/v4", title="ClaimsIQ - Dashboard V4 (Production)")
app.add_page(dashboard_dark, route="/dark", title="ClaimsIQ - Dark Mode")
