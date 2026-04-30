import dash
from dash import html

dash.register_page(__name__, path="/analysis")


def page_banner(title, subtitle, chips):
    return html.Div(
        className="page-banner",
        children=[
            html.Div(className="hero-dot-grid"),
            html.H1(title, className="page-banner-title"),
            html.P(subtitle, className="page-banner-sub"),
            html.Div(chips, className="page-banner-stats"),
        ],
    )


def banner_chip(value, label):
    return html.Div(
        [html.Span(value, className="hero-stat-value"), html.Span(label, className="hero-stat-label")],
        className="hero-stat-chip",
    )


def section_header(number, title, subtitle=None):
    return html.Div(
        [
            html.Div(
                [
                    html.Span(str(number), className="an-sec-num"),
                    html.Div(
                        [
                            html.H2(title, className="an-sec-title"),
                            html.P(subtitle, className="an-sec-sub") if subtitle else None,
                        ],
                        className="an-sec-text",
                    ),
                ],
                className="an-sec-header",
            ),
        ],
        className="an-sec-wrapper",
    )


def viz_wide(title, image_file, description):
    """Single viz: image left, insight right."""
    return html.Div(
        className="card",
        children=[
            html.H3(title, className="subsection-title"),
            html.Div(
                className="viz-wide-row",
                children=[
                    html.Div(
                        className="viz-wide-img-col",
                        children=[
                            html.Img(src=f"/static/images/{image_file}", className="viz-image"),
                        ],
                    ),
                    html.Div(
                        className="viz-wide-text-col",
                        children=[html.P(description, className="viz-insight-text")],
                    ),
                ],
            ),
        ],
    )


def viz_pair_card(section_title_text, subtitle, left_title, left_img, left_desc, right_title, right_img, right_desc):
    return html.Div(
        className="card",
        children=[
            html.H3(section_title_text, className="subsection-title"),
            html.P(subtitle, className="an-pair-sub") if subtitle else None,
            html.Div(
                className="two-column-grid",
                children=[
                    html.Div(
                        className="half-card",
                        children=[
                            html.H4(left_title, className="an-img-title"),
                            html.Img(src=f"/static/images/{left_img}", className="viz-image"),
                            html.P(left_desc, className="insight-note", style={"marginTop": "12px"}),
                        ],
                    ),
                    html.Div(
                        className="half-card",
                        children=[
                            html.H4(right_title, className="an-img-title"),
                            html.Img(src=f"/static/images/{right_img}", className="viz-image"),
                            html.P(right_desc, className="insight-note", style={"marginTop": "12px"}),
                        ],
                    ),
                ],
            ),
        ],
    )


def race_plot(title, image_file, description):
    return html.Div(
        className="half-card",
        children=[
            html.H4(title, className="an-img-title"),
            html.Img(src=f"/static/images/{image_file}", className="viz-image"),
            html.P(description, className="insight-note", style={"marginTop": "10px"}),
        ],
    )


layout = html.Div(
    [
        html.Div(
            className="page-container",
            children=[

                # BANNER
                page_banner(
                    "Analysis & Insights",
                    "Examining the structural drivers of EV adoption disparities across California communities",
                    [],
                ),

                # INTRO
                html.Div(
                    className="card",
                    children=[
                        html.H2("Overview", className="section-title"),
                        html.P(
                            "This section synthesizes the main analytical findings from the project to explain the key drivers of EV adoption across California ZIP codes. "
                            "The results show that EV adoption is not evenly distributed, but instead closely tied to structural factors such as income, education, housing, "
                            "and access to charging infrastructure. By examining these relationships together, this analysis highlights how socioeconomic advantage, rather than "
                            "any single factor, shapes which communities are able to participate in the transition to electric vehicles.",
                            className="section-body",
                        ),
                    ],
                ),

                # SECTION 1
                section_header(1, "Infrastructure Access and EV Adoption",
                    "How charging availability relates to EV adoption and how infrastructure patterns shift across communities."),

                viz_pair_card(
                    "Infrastructure, Income, and EV Adoption",
                    None,
                    "EV Adoption vs Charging Access by Income",
                    "ev_vs_chargingaccess.png",
                    "Even at similar levels of infrastructure, higher-income ZIP codes consistently exhibit higher EV adoption rates. Income plays a more dominant role than charging access alone.",
                    "Charging Access by Income Quintile",
                    "charging_incomequantile.png",
                    "Charging access increases steadily with income — the highest-income ZIPs have substantially more ports per population than the lowest. This highlights a clear inequality in infrastructure distribution.",
                ),

                viz_pair_card(
                    "Alternative Infrastructure Measures",
                    None,
                    "EV Adoption vs Charging Ports per 10,000 People",
                    "ev_charger10k.png",
                    "Most ZIP codes cluster at low levels of both infrastructure and EV adoption, but a slight positive trend is visible. Infrastructure is one part of the story — not the whole picture.",
                    "EV Adoption vs Chargers per 1,000 EV",
                    "ev_chargers.png",
                    "Points are much more scattered with extreme values, making this metric noisier and less useful for explaining broad adoption patterns compared to the population-based measure.",
                ),

                # SECTION 2
                section_header(2, "Who Adopts EVs Most?",
                    "The structural characteristics shared by the ZIP codes with the highest EV adoption."),

                viz_wide(
                    "Top EV-Adopting ZIP Codes",
                    "zip_ev_adopting.png",
                    "The top ZIP codes share very high median household incomes and consistently high bachelor's degree attainment. Renter share is generally low (indicating homeownership and likely home charging access), and many show moderate-to-high charging ports per population with lower environmental burden. The highest-EV ZIP codes are not random outliers — they are communities where income, education, housing stability, infrastructure access, and lower disadvantage all align.",
                ),

                # SECTION 3
                section_header(3, "What Factors Matter Most?",
                    "Regression modeling identifies which variables have the strongest relationship with EV adoption after accounting for multiple factors simultaneously."),

                viz_wide(
                    "Regression Results",
                    "regressionresults.png",
                    "Socioeconomic factors — especially education, income, and home value — are the strongest predictors, with education having the largest effect. Charging infrastructure has a positive impact but is smaller in magnitude compared to these structural factors. Renter share shows a negative relationship, suggesting housing constraints may limit adoption. Overall, EV adoption is primarily driven by socioeconomic advantage rather than infrastructure alone.",
                ),

                # SECTION 4
                section_header(4, "Race, Income, and Structural Inequality",
                    "Comparing racial composition with EV adoption while keeping income visible — showing how much of the apparent disparity is explained by socioeconomic conditions."),

                html.Div(
                    className="card",
                    children=[
                        html.H3("EV Adoption by Racial Composition (Controlled by Income)", className="subsection-title"),
                        html.Div(
                            className="two-column-grid",
                            children=[
                                race_plot("Asian Population Share", "asian.png",
                                    "The clearest upward pattern among the four — highest EV points appear in ZIP codes also in the top income quintile. The association is driven more by affluence than Asian share itself."),
                                race_plot("White Population Share", "white.png",
                                    "Broad spread of EV values, but the highest points are concentrated in higher-income ZIP codes. Income remains the main factor separating top-adopting areas from the rest."),
                                race_plot("Black Population Share", "black.png",
                                    "Many observations cluster at lower Black population shares with relatively lower EV adoption. Yet whenever adoption is higher, those ZIP codes belong to higher income quintiles."),
                                race_plot("Latino Population Share", "latino.png",
                                    "Very high Latino shares are less likely to coincide with high EV adoption, but income explains much of this — the highest EV_perc values remain in higher-income ZIP codes across all groups."),
                            ],
                        ),
                        html.Div(
                            "Taken together, these four plots show that higher EV adoption is consistently concentrated in higher-income areas across all racial groups — income, not race itself, plays the dominant role.",
                            className="insight-note",
                            style={"marginTop": "18px"},
                        ),
                    ],
                ),

                viz_wide(
                    "Race Coefficient Comparison",
                    "race_coefficient.png",
                    "In the race-only model, several groups show noticeable positive or negative associations with EV adoption. Once socioeconomic controls (income, education, housing) are added, these coefficients shrink toward zero — confirming that the apparent racial differences are largely explained by underlying economic and structural conditions rather than race itself.",
                ),

                # SECTION 5
                section_header(5, "Additional Structural and Behavioral Patterns",
                    "Extending the analysis to vehicle transition pathways and the role of housing form."),

                viz_pair_card(
                    "Housing and Transition Patterns",
                    None,
                    "Hybrid Vehicle Share vs EV Adoption",
                    "hybrid_ev.png",
                    "Areas with higher proportions of hybrid vehicles have significantly higher EV adoption rates — suggesting that communities already familiar with hybrid technology are more likely to transition to fully electric vehicles.",
                    "Single-Family Housing Share vs EV Adoption",
                    "singlefam.png",
                    "A slight negative relationship — areas with higher single-family share tend to have lower EV adoption, likely reflecting lower urban density and differences in infrastructure availability rather than housing access to chargers.",
                ),

                # SECTION 6
                section_header(6, "Further Analysis",
                    "How income, infrastructure, and transition behavior interact to shape EV adoption patterns across California ZIP codes."),

                viz_wide(
                    "Infrastructure × Income Interaction",
                    "infra_income.png",
                    "Higher-income ZIP codes consistently exhibit higher EV adoption even at similar levels of infrastructure. Income plays a dominant role in determining how effectively communities can utilize available charging access — infrastructure investments alone may not eliminate disparities.",
                ),

                viz_wide(
                    "Hybrid Share vs EV Adoption",
                    "hybridev.png",
                    "ZIP codes with higher hybrid vehicle shares tend to have significantly higher EV adoption rates, suggesting that hybrid vehicles act as a transition pathway toward full electrification. Behavioral familiarity and gradual adoption patterns play an important role in EV uptake.",
                ),

                viz_wide(
                    "Infrastructure Effect within High-Income Areas",
                    "high_infrabox.png",
                    "Among high-income ZIP codes, areas with greater infrastructure show noticeably higher median EV adoption — the entire distribution shifts upward. Even among wealthy communities, infrastructure still plays an important supporting role.",
                ),

                viz_wide(
                    "Polynomial Income Effect on EV Adoption",
                    "polyEV.png",
                    "The curved trend shows EV adoption increasing at an accelerating rate as income rises — a threshold effect where once income reaches a certain level, adoption grows more rapidly. Income is a dominant and nonlinear driver.",
                ),

                viz_wide(
                    "Vehicle Transition Pathway by Income",
                    "vehicle_byincome.png",
                    "While gasoline vehicles remain dominant, hybrid adoption increases slightly and EV adoption rises sharply with income, suggesting a gradual gasoline → hybrid → electric transition pathway. Lower-income communities move more slowly along this pathway, indicating meaningful barriers to full electrification.",
                ),
            ],
        )
    ]
)
