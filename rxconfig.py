import reflex as rx

config = rx.Config(
    app_name="CarMar",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)