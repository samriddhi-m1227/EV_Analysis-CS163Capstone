import dash
from dash import html

dash.register_page(__name__, path="/analysis")


def viz_card(title, image_file, description):
    return html.Div(
        className="card",
        children=[
            html.H3(title),
            html.Img(
                src=f"/static/images/{image_file}",
                style={
                    "width": "100%",
                    "maxWidth": "900px",
                    "display": "block",
                    "margin": "20px auto",
                    "borderRadius": "12px",
                },
            ),
            html.P(description),
        ],
    )


layout = html.Div(
    className="page-container",
    children=[

        html.H1("Analysis & Key Insights"),

        html.Div(
            className="card",
            children=[
                html.P(
                    "This section highlights key analytical findings from the EV adoption dataset. "
                    "The results focus on infrastructure inequality, socioeconomic drivers, "
                    "and how different structural factors shape EV adoption patterns across communities."
                )
            ],
        ),

        # --------------------------
        # INFRASTRUCTURE INEQUALITY
        # --------------------------
        viz_card(
            "Median Charging Access by Income Quintile",
            "charging_incomequantile.png",
            "Charging infrastructure increases sharply with income level. Higher-income ZIP codes have more than ten times "
            "the charging access compared to lower-income areas, showing a clear inequality in infrastructure distribution."
        ),

        # --------------------------
        # INFRA + INCOME INTERACTION
        # --------------------------
        viz_card(
            "EV Adoption vs Charging Access by Income",
            "ev_vs_chargingaccess.png",
            "Even when infrastructure levels are similar, higher-income communities consistently show greater EV adoption. "
            "This indicates that income and socioeconomic factors play a stronger role than infrastructure alone."
        ),

        # --------------------------
        # REGRESSION RESULTS
        # --------------------------
        viz_card(
            "Regression Results (Key Drivers)",
            "regressionresults.png",
            "Regression analysis shows that education, income, and home value are the strongest predictors of EV adoption. "
            "Infrastructure has a positive but smaller effect, while renter share negatively impacts adoption. "
            "Overall, socioeconomic advantage is the dominant driver."
        ),

        # --------------------------
        # RACE GRID (2x2)
        # --------------------------
        html.Div(
            className="card",
            children=[
                html.H2("EV Adoption by Racial Composition (Controlled by Income)"),

                html.Div(
                    style={
                        "display": "grid",
                        "gridTemplateColumns": "1fr 1fr",
                        "gap": "20px",
                    },
                    children=[

                        html.Div([
                            html.H4("Latino Population Share"),
                            html.Img(src="/static/images/latino.png", style={"width": "100%"}),
                            html.P(
                                "EV adoption appears lower in areas with higher Latino population share, but when income is considered, "
                                "the differences are largely explained by socioeconomic factors rather than race alone."
                            ),
                        ]),

                        html.Div([
                            html.H4("Black Population Share"),
                            html.Img(src="/static/images/black.png", style={"width": "100%"}),
                            html.P(
                                "Areas with higher Black population share show lower EV adoption overall, but much of this pattern "
                                "is driven by underlying income differences rather than race independently."
                            ),
                        ]),

                        html.Div([
                            html.H4("White Population Share"),
                            html.Img(src="/static/images/white.png", style={"width": "100%"}),
                            html.P(
                                "Higher EV adoption is observed in areas with larger White population shares, but this is strongly "
                                "associated with higher income levels in those areas."
                            ),
                        ]),

                        html.Div([
                            html.H4("Asian Population Share"),
                            html.Img(src="/static/images/asian.png", style={"width": "100%"}),
                            html.P(
                                "Areas with higher Asian population share tend to show higher EV adoption, but this trend is largely "
                                "explained by higher average income levels in those communities."
                            ),
                        ]),
                    ],
                ),

                html.P(
                    "Across all racial groups, income consistently explains most of the variation in EV adoption. "
                    "This indicates that structural socioeconomic factors dominate over race itself in determining EV adoption patterns."
                ),
            ],
        ),

        # --------------------------
        # RACE COEFFICIENT
        # --------------------------
        viz_card(
            "Race Coefficient Comparison",
            "race_coefficient.png",
            "When socioeconomic variables are included in the model, the effect of race decreases significantly. "
            "This suggests that observed racial disparities in EV adoption are largely driven by underlying economic differences."
        ),

        # --------------------------
        # HYBRID SHARE
        # --------------------------
        viz_card(
            "Hybrid Share vs EV Adoption",
            "hybrid_ev.png",
            "A strong positive relationship exists between hybrid vehicle share and EV adoption. "
            "This suggests that hybrid ownership may act as a transition pathway toward full EV adoption."
        ),
    ],
)