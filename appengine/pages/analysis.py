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
            "1. Infrastructure Access and EV Adoption",
            "These visuals show how charging availability relates to EV adoption and how that relationship changes across income groups."
        ),

        viz_card(
            "EV Adoption vs Charging Access by Income",
            "ev_vs_chargingaccess.png",
            "This plot shows the relationship between charging access and EV adoption across income levels. Even at similar levels of infrastructure, "
            "higher-income ZIP codes consistently exhibit higher EV adoption rates. This indicates that while charging access supports adoption, "
            "income plays a more dominant role. Overall, the results suggest that infrastructure alone is not sufficient to drive equitable EV adoption."
        ),

        viz_card(
            "Charging Access by Income Quintile",
            "charging_incomequantile.png",
            "This plot shows how charging infrastructure varies across income levels. Charging access increases steadily with income, with the highest-income "
            "ZIP codes having substantially more charging ports per population than the lowest-income areas. This highlights a clear inequality in infrastructure distribution. "
            "Such disparities suggest that access to charging resources may contribute to differences in EV adoption across communities."
        ),

        section_title(
            "2. Who adopts EVs most?",
            "These results highlight the structural characteristics of the highest-adopting communities."
        ),

        viz_card(
            "Top EV-Adopting ZIP Codes",
            "zip_ev_adopting.png",
            "This table highlights the ZIP codes with the highest EV adoption rates. These areas consistently exhibit high income levels, strong educational attainment, "
            "and lower renter shares, indicating greater homeownership. They also tend to have moderate to high charging infrastructure and lower environmental burden. "
            "Overall, this shows that EV adoption is concentrated in well-resourced communities with both financial capacity and access to supporting infrastructure."
        ),

        section_title(
            "3. What Factors Matter Most?",
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
            "4. Race, income, and Structural inequality",
            "These visuals compare raw demographic patterns with income-controlled patterns to show how much of the apparent racial disparity is explained by socioeconomic conditions."
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
                        html.Div([
                            html.H4("Asian Population Share"),
                            html.Img(
                                src="/static/images/asian.png",
                                style={"width": "100%", "borderRadius": "10px"}
                            ),
                        ]),
                        html.Div([
                            html.H4("White Population Share"),
                            html.Img(
                                src="/static/images/white.png",
                                style={"width": "100%", "borderRadius": "10px"}
                            ),
                        ]),
                        html.Div([
                            html.H4("Black Population Share"),
                            html.Img(
                                src="/static/images/black.png",
                                style={"width": "100%", "borderRadius": "10px"}
                            ),
                        ]),
                        html.Div([
                            html.H4("Latino Population Share"),
                            html.Img(
                                src="/static/images/latino.png",
                                style={"width": "100%", "borderRadius": "10px"}
                            ),
                        ]),
                    ],
                ),

                html.P(
                    "These plots show EV adoption across different racial compositions while controlling for income levels. "
                    "Although the raw patterns suggest differences across racial groups, the color-coded income quintiles show that "
                    "higher EV adoption is consistently concentrated in higher-income areas across all groups. This indicates that income, "
                    "rather than race itself, plays the dominant role in explaining EV adoption patterns. Overall, the results suggest that "
                    "socioeconomic factors drive the observed disparities across racial groups."
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
            "5. Additional Structural and Behavioral Patterns",
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