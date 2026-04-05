from dash import Dash, html, dcc, Input, Output, State
import dash

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)
server = app.server

navbar = html.Div(
    [
        html.Div(
            [
                dcc.Link("Home", href="/", className="nav-link"),

                html.Div(
                    [
                        html.Span("EDA", className="nav-link dropdown-label"),
                        html.Div(
                            [
                                dcc.Link("Data", href="/data", className="dropdown-link"),
                                dcc.Link("EDA", href="/eda", className="dropdown-link"),
                            ],
                            className="dropdown-menu",
                        ),
                    ],
                    className="dropdown",
                ),

                dcc.Link("Analysis", href="/analysis", className="nav-link"),
                dcc.Link("ML", href="/ml", className="nav-link"),
                dcc.Link("Findings", href="/findings", className="nav-link"),
            ],
            className="nav-links",
        ),
        html.Button(
            "🌙 Dark Mode",
            id="theme-toggle",
            n_clicks=0,
            className="theme-toggle-btn",
        ),
    ],
    className="navbar",
)

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        dcc.Store(id="theme-store", storage_type="local", data="light"),
        html.Div(
            [
                navbar,
                dash.page_container,
            ],
            id="app-wrapper",
            className="light-mode",
        ),
    ],
    className="app-shell",
)

@app.callback(
    Output("theme-store", "data"),
    Input("theme-toggle", "n_clicks"),
    State("theme-store", "data"),
    prevent_initial_call=True,
)
def toggle_theme(n_clicks, current_theme):
    if current_theme == "light":
        return "dark"
    return "light"

@app.callback(
    Output("app-wrapper", "className"),
    Output("theme-toggle", "children"),
    Input("theme-store", "data"),
)
def apply_theme(theme):
    if theme == "dark":
        return "dark-mode", "☀️ Light Mode"
    return "light-mode", "🌙 Dark Mode"

if __name__ == "__main__":
    app.run(debug=True)