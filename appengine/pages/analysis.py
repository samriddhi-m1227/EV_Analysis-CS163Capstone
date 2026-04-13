import dash
from dash import html

dash.register_page(__name__, path="/analysis")


def section_title(title, subtitle=None):
    children = [html.H2(title, className="section-title")]
    if subtitle:
        children.append(html.P(subtitle, className="section-intro"))
    return html.Div(children, className="section-header")


def viz_card(title, image_file, description):
    return html.Div(
        className="card",
        children=[
            html.H3(title, className="subsection-title"),
            html.Img(
                src=f"/static/images/{image_file}",
                style={
                    "width": "100%",
                    "maxWidth": "950px",
                    "display": "block",
                    "margin": "18px auto",
                    "borderRadius": "12px",
                },
            ),
            html.P(description, className="page-text"),
        ],
    )


def two_up_card(title, left_title, left_img, left_desc, right_title, right_img, right_desc):
    return html.Div(
        className="card",
        children=[
            html.H3(title, className="subsection-title"),
            html.Div(
                style={
                    "display": "grid",
                    "gridTemplateColumns": "1fr 1fr",
                    "gap": "24px",
                    "alignItems": "start",
                },
                children=[
                    html.Div(
                        children=[
                            html.H4(left_title),
                            html.Img(
                                src=f"/static/images/{left_img}",
                                style={
                                    "width": "100%",
                                    "borderRadius": "10px",
                                    "marginBottom": "12px",
                                },
                            ),
                            html.P(left_desc, className="page-text"),
                        ]
                    ),
                    html.Div(
                        children=[
                            html.H4(right_title),
                            html.Img(
                                src=f"/static/images/{right_img}",
                                style={
                                    "width": "100%",
                                    "borderRadius": "10px",
                                    "marginBottom": "12px",
                                },
                            ),
                            html.P(right_desc, className="page-text"),
                        ]
                    ),
                ],
            ),
        ],
    )


layout = html.Div(
    className="page-container",
    children=[
        html.H1("Analysis & Insights", className="page-header"),

        html.Div(
            className="card",
            children=[
                html.P(
                    "This section synthesizes the main analytical findings from the project to explain the key drivers of EV adoption across California ZIP codes. "
                    "The results show that EV adoption is not evenly distributed, but instead closely tied to structural factors such as income, education, housing, "
                    "and access to charging infrastructure. By examining these relationships together, this analysis highlights how socioeconomic advantage, rather than "
                    "any single factor, shapes which communities are able to participate in the transition to electric vehicles."
                )
            ],
        ),

        section_title(
            "1. Infrastructure access and EV adoption",
            "These visuals examine how charging availability relates to EV adoption and how infrastructure patterns change across communities."
        ),

        two_up_card(
            "Infrastructure, Income, and EV Adoption",
            "EV Adoption vs Charging Access by Income",
            "ev_vs_chargingaccess.png",
            "This plot shows the relationship between charging access and EV adoption across income levels. Even at similar levels of infrastructure, "
            "higher-income ZIP codes consistently exhibit higher EV adoption rates. This indicates that while charging access supports adoption, "
            "income plays a more dominant role. Overall, the results suggest that infrastructure alone is not sufficient to drive equitable EV adoption.",
            "Charging Access by Income Quintile",
            "charging_incomequantile.png",
            "This plot shows how charging infrastructure varies across income levels. Charging access increases steadily with income, with the highest-income "
            "ZIP codes having substantially more charging ports per population than the lowest-income areas. This highlights a clear inequality in infrastructure distribution. "
            "Such disparities suggest that access to charging resources may contribute to differences in EV adoption across communities."
        ),

        two_up_card(
            "Alternative Infrastructure Measures",
            "EV Adoption vs Charging Ports per 10,000 People",
            "ev_charger10k.png",
            "This plot compares EV adoption with charging access measured per 10,000 people. Most ZIP codes are still clustered at low levels of both infrastructure and EV adoption, but the pattern is easier to read than the chargers-per-EV version. There is a slight positive trend, suggesting that places with more charging access per population often have somewhat higher EV adoption. At the same time, the spread of the points shows that infrastructure is only one part of the story.",
            "EV Adoption vs Chargers per 1,000 EV",
            "ev_chargers.png",
            "This plot compares EV adoption with chargers measured relative to the number of EVs already on the road. The points are much more scattered, with several extreme values, so the pattern is harder to interpret clearly. Compared with the population-based measure, this version is less stable and less useful for understanding broad differences across ZIP codes. Overall, it suggests that this metric is noisier and not as helpful for explaining EV adoption patterns."
        ),

        section_title(
            "2. Who adopts EVs most?",
            "These results show the structural characteristics shared by the ZIP codes with the highest EV adoption."
        ),

        viz_card(
            "Top EV-Adopting ZIP Codes",
            "zip_ev_adopting.png",
            "This table highlights the ZIP codes with the highest EV adoption rates and makes it easier to see which variables repeatedly appear in high-adoption communities. "
            "The strongest pattern is in Median_Household_Income: the top ZIP codes have very high incomes, often near the upper end of the dataset. They also show consistently high "
            "BachOrHigher_perc values, meaning these communities have a large share of college-educated residents. RenterShare is generally low, which suggests higher homeownership and "
            "likely better access to home charging. In addition, many of these ZIP codes have moderate to high PortsPer10kPeople and relatively low CES_Score_ZIP values, indicating more charging access "
            "and lower environmental burden. Overall, the table shows that the highest-EV ZIP codes are not random outliers; they are communities where income, education, housing stability, "
            "infrastructure access, and lower disadvantage align."
        ),

        section_title(
            "3. What factors matter most?",
            "The regression model helps identify which variables have the strongest relationship with EV adoption after accounting for multiple factors at once."
        ),

        viz_card(
            "Regression Results",
            "regressionresults.png",
            "This regression model identifies the key factors driving EV adoption while controlling for multiple variables. The results show that socioeconomic factors, "
            "especially education, income, and home value, are the strongest predictors, with education having the largest effect. Charging infrastructure also has a positive impact, "
            "but its influence is smaller compared to these structural factors. Additionally, renter share shows a negative relationship, suggesting housing constraints may limit adoption. "
            "Overall, EV adoption is primarily driven by socioeconomic advantage rather than infrastructure alone."
        ),

        section_title(
            "4. Race, income, and structural inequality",
            "These visuals compare racial composition with EV adoption while keeping income visible, showing how much of the apparent disparity is explained by socioeconomic conditions."
        ),

        html.Div(
            className="card",
            children=[
                html.H3("EV Adoption by Racial Composition (Controlled by Income)", className="subsection-title"),

                html.Div(
                    style={
                        "display": "grid",
                        "gridTemplateColumns": "1fr 1fr",
                        "gap": "20px",
                    },
                    children=[
                        html.Div(
                            children=[
                                html.H4("Asian Population Share"),
                                html.Img(
                                    src="/static/images/asian.png",
                                    style={"width": "100%", "borderRadius": "10px", "marginBottom": "10px"},
                                ),
                                html.P(
                                    "Among the four race plots, the Asian_perc plot shows one of the clearest upward patterns, with many of the highest EV_perc points appearing in ZIP codes "
                                    "that also fall into the top income quintile. This suggests that the positive association is less about Asian population share by itself and more about the fact "
                                    "that many high-Asian-share ZIP codes in the dataset are also relatively affluent."
                                ),
                            ]
                        ),
                        html.Div(
                            children=[
                                html.H4("White Population Share"),
                                html.Img(
                                    src="/static/images/white.png",
                                    style={"width": "100%", "borderRadius": "10px", "marginBottom": "10px"},
                                ),
                                html.P(
                                    "The White_perc plot shows a broad spread of EV adoption values, but the highest EV_perc points are again concentrated in higher-income ZIP codes. "
                                    "This indicates that while some high-white-share communities also have high EV adoption, income remains the main factor separating the highest-adopting areas from the rest."
                                ),
                            ]
                        ),
                        html.Div(
                            children=[
                                html.H4("Black Population Share"),
                                html.Img(
                                    src="/static/images/black.png",
                                    style={"width": "100%", "borderRadius": "10px", "marginBottom": "10px"},
                                ),
                                html.P(
                                    "The Black_perc plot is more compressed, with many observations clustered at lower Black population shares and relatively lower EV adoption. "
                                    "However, the color coding still shows that whenever EV adoption is higher, those ZIP codes tend to belong to higher income quintiles. This suggests that the pattern is primarily driven by income rather than racial composition alone."
                                ),
                            ]
                        ),
                        html.Div(
                            children=[
                                html.H4("Latino Population Share"),
                                html.Img(
                                    src="/static/images/latino.png",
                                    style={"width": "100%", "borderRadius": "10px", "marginBottom": "10px"},
                                ),
                                html.P(
                                    "The Latino_perc plot shows a noticeable downward visual pattern, where very high Latino population shares are less likely to coincide with high EV adoption. "
                                    "Still, the color-coded points reveal that income explains much of this relationship: the highest EV_perc values remain concentrated in higher-income ZIP codes, regardless of Latino population share."
                                ),
                            ]
                        ),
                    ],
                ),

                html.P(
                    "Taken together, these four plots show that while the raw distributions differ somewhat by racial composition, higher EV adoption is consistently concentrated in higher-income areas across all groups. "
                    "This indicates that income, rather than race itself, plays the dominant role in explaining EV adoption patterns. Overall, the results suggest that socioeconomic factors drive much of the observed disparity across racial groups."
                ),
            ],
        ),

        viz_card(
            "Race Coefficient Comparison",
            "race_coefficient.png",
            "This figure compares the relationship between racial composition and EV adoption before and after controlling for socioeconomic factors such as income, education, and housing. "
            "In the race-only model, several groups show noticeable positive or negative associations with EV adoption. However, once socioeconomic controls are added, these coefficients shrink toward zero. "
            "This indicates that the apparent differences across racial groups are largely explained by underlying economic and structural conditions rather than race itself. Overall, the results suggest that income, "
            "education, and housing characteristics play a dominant role in shaping EV adoption patterns across communities."
        ),

        section_title(
            "5. Additional structural and behavioral patterns",
            "These plots extend the analysis by looking at vehicle transition pathways and the role of housing form."
        ),

        viz_card(
            "Hybrid Vehicle Share vs EV Adoption",
            "hybrid_ev.png",
            "This plot shows a strong positive relationship between hybrid vehicle share and EV adoption. Areas with higher proportions of hybrid vehicles tend to have significantly higher EV adoption rates. "
            "This suggests that communities familiar with hybrid technology are more likely to transition to fully electric vehicles. Overall, hybrid adoption appears to act as a stepping stone toward broader electrification."
        ),

        viz_card(
            "Single-Family Housing Share vs EV Adoption",
            "singlefam.png",
            "This plot shows a slight negative relationship between single-family housing share and EV adoption. While single-family homes may provide better access to private charging, "
            "areas with higher single-family share tend to have lower EV adoption. This likely reflects broader factors such as lower urban density and differences in infrastructure availability. "
            "Overall, housing structure alone does not strongly determine EV adoption patterns."
        ),
    ],
)