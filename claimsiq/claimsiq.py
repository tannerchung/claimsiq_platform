import reflex as rx
from claimsiq.pages.index import index

app = rx.App()
app.add_page(index, route="/", title="ClaimsIQ Dashboard")
