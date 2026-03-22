from dash import Dash, html

app = Dash(__name__)
server = app.server

app.layout = html.Div(
    [
        html.H1("CS 163 Capstone Project", style={"textAlign": "center"}),
        html.H2("EV Charging Disparities Across California Communities", style={"textAlign": "center"}),
        html.P(
            "This website is currently under development for our capstone project.",
            style={"textAlign": "center", "fontSize": "18px"},
        ),
        html.Hr(),
        html.P(
            "More coming soon.",
            style={
                "textAlign": "center",
                "fontStyle": "italic",
                "color": "#555"
            },
        ),
    ],
    style={"maxWidth": "900px", "margin": "60px auto", "padding": "20px"},
)

if __name__ == "__main__":
    app.run(debug=True)