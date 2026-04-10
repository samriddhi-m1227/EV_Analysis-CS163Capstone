import dash
from dash import html

dash.register_page(__name__, path="/analysis")


def section_card(title, children):
    return html.Div(
        [
            html.H2(title, className="section-title"),
            html.Div(children, className="section-body"),
        ],
        className="card",
    )


def viz_block(title, image_file, caption, insight):
    return html.Div(
        className="viz-block",
        children=[
            html.H3(title, className="subsection-title"),
            html.Div(
                className="viz-frame",
                children=[
                    html.Img(
                        src=f"/static/images/{image_file}",
                        className="viz-image",
                        style={
                            "width": "100%",
                            "maxWidth": "950px",
                            "display": "block",
                            "margin": "0 auto",
                            "borderRadius": "12px",
                        },
                    ),
                    html.P(caption, className="viz-caption"),
                ],
            ),
            html.P(insight, className="viz-description"),
        ],
    )


layout = html.Div(
    [
        html.Div(
            className="page-container",
            children=[
                html.H1("Preliminary Results", className="page-header"),

                section_card(
                    "Overview",
                    [
                        html.P(
                            "This page presents the major preliminary results from our EV adoption analysis across California ZIP codes. "
                            "For the assignment, we focus on three key hypotheses and summarize how the visual and statistical results address each one."
                        ),
                        html.P(
                            "Overall, the analysis suggests that EV adoption is strongly associated with socioeconomic advantage, "
                            "lower in environmentally burdened communities, and shaped much more by structural conditions than by any single factor alone."
                        ),
                    ],
                ),

                section_card(
                    "Hypothesis 1: EV adoption is strongly associated with socioeconomic advantage",
                    [
                        html.H3("Summary", className="subsection-title"),
                        html.P(
                            "EV adoption increases sharply across income quintiles. The lowest-income quintile has the lowest mean EV adoption, "
                            "while the highest-income quintile shows a much larger share of EVs. The relationship is not only positive, "
                            "but also nonlinear, with adoption accelerating in higher-income communities."
                        ),
                        html.P(
                            "The correlation results support this pattern: EV adoption is strongly positively associated with education, "
                            "median household income, and home value."
                        ),

                        html.H3("Implications", className="subsection-title"),
                        html.P(
                            "These findings support the hypothesis that EV adoption is driven by socioeconomic advantage. "
                            "Higher-income and more highly educated communities appear far better positioned to adopt EVs, "
                            "likely because they have greater purchasing power, more stable housing conditions, and better access to supporting resources."
                        ),
                        html.P(
                            "A key implication is that EV adoption may behave more like a high-cost transition good than an evenly distributed climate solution. "
                            "A next step would be to test how much of this income gradient remains after controlling for infrastructure and environmental burden in the final models."
                        ),

                        viz_block(
                            "Mean EV Adoption by Income Quintile",
                            "ev_incomequintile.png",
                            "Figure 1. Mean EV adoption rises steadily across income quintiles.",
                            "This figure shows one of the clearest patterns in the dataset: as income quintile increases, EV adoption increases substantially."
                        ),

                        viz_block(
                            "EV Adoption vs Income (Quadratic Trend)",
                            "ev_income_quadratic.png",
                            "Figure 2. EV adoption increases nonlinearly with household income.",
                            "The quadratic trend suggests that adoption grows more rapidly at higher income levels, consistent with an affordability threshold effect."
                        ),
                    ],
                ),

                section_card(
                    "Hypothesis 2: Communities with greater environmental burden have lower EV adoption",
                    [
                        html.H3("Summary", className="subsection-title"),
                        html.P(
                            "The environmental burden results show a clear negative pattern. ZIP codes with higher CalEnviroScreen burden scores "
                            "tend to have lower EV adoption. This pattern appears both in the scatterplot and in the burden-quartile boxplot."
                        ),
                        html.P(
                            "As environmental burden increases, the distribution of EV adoption shifts downward, indicating that more disadvantaged communities "
                            "are less likely to benefit from EV adoption."
                        ),

                        html.H3("Implications", className="subsection-title"),
                        html.P(
                            "These findings support the environmental justice hypothesis. Communities that face greater pollution and socioeconomic stress "
                            "are also less likely to participate in the EV transition. This is important because the benefits of cleaner transportation "
                            "are not reaching all communities equally."
                        ),
                        html.P(
                            "A major implication is that clean transportation policy should prioritize high-burden communities, "
                            "not only by expanding infrastructure, but also by improving affordability and targeting public investment where current adoption remains low."
                        ),

                        viz_block(
                            "Environmental Burden vs EV Adoption",
                            "ev_burden_scatter.png",
                            "Figure 3. EV adoption tends to be lower in ZIP codes with higher CalEnviroScreen burden.",
                            "The scatterplot shows a broad downward pattern, suggesting that disadvantaged communities tend to have lower EV adoption."
                        ),

                        viz_block(
                            "EV Adoption by CalEnviroScreen Burden Quartile",
                            "ev_calenviro_boxplot.png",
                            "Figure 4. EV adoption distributions decline as environmental burden increases.",
                            "The quartile view makes the burden relationship easier to compare across groups and reinforces the environmental justice interpretation."
                        ),
                    ],
                ),

                section_card(
                    "Hypothesis 3: EV adoption is shaped by multiple structural factors, with socioeconomic variables dominating",
                    [
                        html.H3("Summary", className="subsection-title"),
                        html.P(
                            "The correlation heatmap shows that EV adoption is most strongly positively associated with educational attainment, "
                            "home value, and median household income. It is negatively associated with poverty and CalEnviroScreen burden. "
                            "Infrastructure variables, such as stations and total ports, are positively related to EV adoption, but their relationships are weaker than the core socioeconomic variables."
                        ),
                        html.P(
                            "This suggests that infrastructure matters, but it is not the main driver of disparities by itself."
                        ),

                        html.H3("Implications", className="subsection-title"),
                        html.P(
                            "These results support the broader project argument that EV adoption disparities are structural. "
                            "Socioeconomic advantage appears to be the dominant force, while infrastructure plays a secondary but supportive role. "
                            "This means that simply increasing chargers may not fully close adoption gaps if affordability, education, and housing constraints remain unaddressed."
                        ),
                        html.P(
                            "A next step would be to use multivariate regression to compare the relative contribution of these factors directly and evaluate how much explanatory power comes from socioeconomic versus infrastructure variables."
                        ),

                        viz_block(
                            "Correlation Between EV Adoption and Key Variables",
                            "ev_corr.png",
                            "Figure 5. EV adoption is most strongly associated with education, income, and home value, and negatively associated with poverty and environmental burden.",
                            "This summary figure shows that socioeconomic advantage is more strongly tied to EV adoption than infrastructure alone."
                        ),
                    ],
                ),
            ],
        )
    ]
)