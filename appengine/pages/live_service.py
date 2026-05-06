import os
import dash
from dash import html, dcc, Input, Output, State, callback
import requests

dash.register_page(__name__, path="/live-service", name="Live Service")

CLOUD_RUN_URL = os.environ.get(
    "CLOUD_RUN_URL",
    "https://ev-desert-700424293646.us-west2.run.app",
)

layout = html.Div([
    html.Div(
        className="page-container",
        children=[

            # BANNER
            html.Div(
                className="page-banner",
                children=[
                    html.Div(className="hero-dot-grid"),
                    html.H1("Live Model Service", className="page-banner-title"),
                    html.P(
                        "Real-time EV desert predictions powered by a Logistic Regression classifier "
                        "deployed as a live inference service on Google Cloud Run.",
                        className="page-banner-sub",
                    ),
                ],
            ),

            # PREDICTOR
            html.Div(
                className="card",
                children=[
                    html.H2("Live EV Desert Predictor", className="section-title"),
                    html.P(
                        "Enter community characteristics below and get a real-time prediction from the "
                        "EV Desert Classifier running as a live inference service on Google Cloud Run.",
                        className="section-body",
                        style={"marginBottom": "24px"},
                    ),
                    html.Div(
                        className="predictor-grid",
                        children=[
                            # Left: sliders
                            html.Div(
                                className="predictor-inputs",
                                children=[
                                    html.Div([
                                        html.Label("Median Household Income ($)", className="predictor-label"),
                                        dcc.Slider(id="pred-income", min=20000, max=250000, step=5000, value=75000,
                                                   marks={20000: "$20k", 100000: "$100k", 200000: "$200k", 250000: "$250k"},
                                                   tooltip={"placement": "bottom", "always_visible": True}),
                                    ], className="predictor-field"),
                                    html.Div([
                                        html.Label("Bachelor's Degree or Higher (%)", className="predictor-label"),
                                        dcc.Slider(id="pred-bach", min=0, max=80, step=1, value=30,
                                                   marks={0: "0%", 40: "40%", 80: "80%"},
                                                   tooltip={"placement": "bottom", "always_visible": True}),
                                    ], className="predictor-field"),
                                    html.Div([
                                        html.Label("Poverty Rate (%)", className="predictor-label"),
                                        dcc.Slider(id="pred-poverty", min=0, max=50, step=1, value=15,
                                                   marks={0: "0%", 25: "25%", 50: "50%"},
                                                   tooltip={"placement": "bottom", "always_visible": True}),
                                    ], className="predictor-field"),
                                    html.Div([
                                        html.Label("Renter Share (%)", className="predictor-label"),
                                        dcc.Slider(id="pred-renter", min=0, max=100, step=1, value=50,
                                                   marks={0: "0%", 50: "50%", 100: "100%"},
                                                   tooltip={"placement": "bottom", "always_visible": True}),
                                    ], className="predictor-field"),
                                    html.Div([
                                        html.Label("CalEnviroScreen Score (0-100)", className="predictor-label"),
                                        dcc.Slider(id="pred-ces", min=0, max=100, step=1, value=50,
                                                   marks={0: "0", 50: "50", 100: "100"},
                                                   tooltip={"placement": "bottom", "always_visible": True}),
                                    ], className="predictor-field"),
                                    html.Div([
                                        html.Label("Total Public Charging Ports", className="predictor-label"),
                                        dcc.Slider(id="pred-ports", min=0, max=200, step=5, value=10,
                                                   marks={0: "0", 100: "100", 200: "200"},
                                                   tooltip={"placement": "bottom", "always_visible": True}),
                                    ], className="predictor-field"),
                                    html.Button("Run Prediction", id="pred-btn", className="pred-run-btn", n_clicks=0),
                                ],
                            ),
                            # Right: result
                            html.Div(
                                id="pred-result",
                                className="predictor-result-panel",
                                children=[
                                    html.P(
                                        "Adjust the sliders and click Run Prediction to get a live result from the Cloud Run inference service.",
                                        style={"color": "var(--muted)", "fontSize": "13px", "textAlign": "center", "margin": "auto"},
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),

            # WHY LOGISTIC REGRESSION
            html.Div(
                className="card",
                children=[
                    html.H2("Why Logistic Regression?", className="section-title"),
                    html.P(
                        "The inference service uses Logistic Regression to classify ZIP codes as EV deserts "
                        "(bottom 20% of EV adoption). We chose it for three reasons: it produces well-calibrated "
                        "probabilities that are easy to interpret, it trains instantly on startup with no stored "
                        "model artifact, and it achieved a 0.968 AUC on this task — competitive with the Random "
                        "Forest classifier (0.974 AUC) while being far simpler to serve. "
                        "StandardScaler normalization is applied before fitting so that the penalty term treats "
                        "all features on equal footing.",
                        className="section-body",
                        style={"marginBottom": "16px"},
                    ),
                    html.A(
                        "View inference_service/main.py on GitHub →",
                        href="https://github.com/samriddhi-m1227/EV_Analysis-CS163Capstone/blob/main/inference_service/main.py",
                        target="_blank",
                        className="insight-note",
                        style={"display": "inline-block", "textDecoration": "none", "fontWeight": "600"},
                    ),
                ],
            ),

        ],
    )
])


@callback(
    Output("pred-result", "children"),
    Input("pred-btn", "n_clicks"),
    State("pred-income", "value"),
    State("pred-bach", "value"),
    State("pred-poverty", "value"),
    State("pred-renter", "value"),
    State("pred-ces", "value"),
    State("pred-ports", "value"),
    prevent_initial_call=True,
)
def run_prediction(n_clicks, income, bach, poverty, renter, ces, ports):
    payload = {
        "Median_Household_Income": income,
        "BachOrHigher_perc": bach,
        "PovertyShare": poverty / 100,
        "RenterShare": renter / 100,
        "CES_Score_ZIP": ces,
        "Total_Ports": ports,
    }
    try:
        resp = requests.post(f"{CLOUD_RUN_URL}/predict", json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        is_desert = data["ev_desert"]
        prob = data["probability_ev_desert"]
        label = data["label"]
        result_cls = "pred-result-desert" if is_desert else "pred-result-ok"
        return html.Div(
            className=f"pred-result-box {result_cls}",
            children=[
                html.Div(label, className="pred-result-label"),
                html.Div(f"{prob * 100:.1f}% probability of being an EV desert", className="pred-result-prob"),
                html.Hr(style={"margin": "14px 0", "opacity": "0.2"}),
                html.Div("Prediction served live from Google Cloud Run", className="pred-result-source"),
            ],
        )
    except Exception as e:
        return html.Div(
            f"Service unavailable: {str(e)}",
            style={"color": "var(--muted)", "fontSize": "13px", "padding": "20px", "textAlign": "center"},
        )
