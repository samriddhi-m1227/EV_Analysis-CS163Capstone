import dash
from dash import html

dash.register_page(__name__, path="/")


def source_item(title, subtitle):
    return html.Li(
        [
            html.Span(title, className="source-title"),
            html.Br(),
            html.Span(subtitle, className="source-subtitle"),
        ],
        className="source-item",
    )


layout = html.Div(
    [
        html.Div(
            className="page-container",
            children=[
                # =========================
                # HERO
                # =========================
                html.Div(
                    className="hero-banner",
                    children=[
                        html.H1(
                            "Electric Vehicle Adoption & Infrastructure Disparities in California",
                            className="hero-title",
                        ),
                        html.P(
                            "Group ID: 14",
                            className="hero-group-id",
                        ),
                        html.P(
                            "Contributors: Samriddhi Matharu, Bhavya",
                            className="hero-members",
                        ),
                    ],
                ),

                # =========================
                # PROJECT OVERVIEW
                # =========================
                html.Div(
                    className="card",
                    children=[
                        html.H2("Project Summary", className="section-title"),
                        html.Div(
                            className="section-body",
                            children=[
                                html.P(
                                    "California is undergoing a large-scale transition toward electric vehicles (EVs), with statewide goals aimed at reducing emissions and expanding clean transportation. However, EV adoption and public charging infrastructure may not be evenly distributed across communities. Socioeconomic conditions, housing characteristics, environmental disadvantage, and infrastructure availability may shape which communities adopt EVs more rapidly and which lag behind."
                                ),
                                html.P(
                                    "This project analyzes EV adoption and community-level disparities across California ZIP codes. Using vehicle registration data, demographic, housing and income variables, environmental justice indicators, and public charging (infrastructure) data from which we construct a unified ZIP-code-level dataset."
                                ),
                                html.P(
                                    "The project begins with exploratory data analysis to identify spatial and demographic patterns in EV adoption and charging infrastructure access. We then develop regression models to evaluate how income, race and ethnicity composition, education levels, housing tenure, income inequality, environmental burden (pollution exposure, traffic density, etc.), and infrastructure availability are associated with EV adoption rates. In addition, we examine whether \"low-adoption\" ZIP codes (EV deserts) and low-infrastructure ZIP codes are systematically concentrated in more disadvantaged communities."
                                ),
                                html.P(
                                    "All modeling focuses on recent cross-sectional data, emphasizing structural differences across communities rather than time-series trends. This project showcases an end to end data scinece workflow from ingestion and curation to analysis and modeling."
                                ),
                            ],
                        ),
                    ],
                ),

                # =========================
                # ROW 1
                # =========================
                html.Div(
                    className="two-column-grid",
                    children=[
                        html.Div(
                            className="half-card",
                            children=[
                                html.H2("Why This Matters", className="section-title"),
                                html.P(
                                    "Understanding EV disparities is essential for evaluating whether California’s clean transportation transition is equitable. If EV adoption and charging access remain concentrated in wealthier or structurally advantaged communities, the benefits of electrification may not be shared broadly."
                                ),
                                html.P(
                                    "Looking beyond statewide averages helps reveal how local conditions such as income, education, housing tenure, and access to charging infrastructure shape participation in the EV transition."
                                ),
                            ],
                        ),
                        html.Div(
                            className="half-card",
                            children=[
                                html.H2("Key Research Questions", className="section-title"),
                                html.Ul(
                                    [
                                        html.Li("How are EV adoption rates associated with income, education, housing value, and homeownership?"),
                                        html.Li("Do communities with greater environmental burden and socioeconomic vulnerability show lower EV adoption?"),
                                        html.Li("Is the relationship between income and EV adoption nonlinear, suggesting affordability thresholds?"),
                                        html.Li("Is charging infrastructure distributed unevenly across California ZIP codes?"),
                                        html.Li("Do structural socioeconomic factors explain much of the disparity that appears across racial and ethnic composition?"),
                                    ]
                                ),
                            ],
                        ),
                    ],
                ),

                # =========================
                # ROW 2
                # =========================
                html.Div(
                    className="two-column-grid",
                    children=[
                        html.Div(
                            className="half-card",
                            children=[
                                html.H2("Broader Impact", className="section-title"),
                                html.P(
                                    "The findings can support policymakers, planners, researchers, and community organizations seeking to identify underserved communities, understand infrastructure gaps, and design more equity-focused clean transportation strategies."
                                ),
                                html.P(
                                    "More broadly, this project demonstrates how data-driven analysis can make climate transitions more transparent and help ensure that clean technology adoption does not unintentionally reinforce existing socioeconomic and environmental inequalities."
                                ),
                            ],
                        ),
                        html.Div(
                            className="half-card",
                            children=[
                                html.H2("Data Sources", className="section-title"),
                                html.P(
                                    "We use publicly available datasets from official California state agencies and federal government sources. All datasets are integrated at the ZIP code level to construct a unified dataset for California."
                                ),
                                html.Div(
                                    [
                                        html.A("CalMatters", href="https://github.com/CalMatters/ev-zipcode-demographics-data", target="_blank"),
                                        html.Br(),
                                        "Main Dataset: EV adoption rates, vehicle counts, Zilow home indicators"
                                    ]
                                ),
                                html.Br(),
                                html.Div(
                                    [
                                        html.A("American Community Survey (ACS)", href="https://www.census.gov/data/developers/data-sets/acs-5year.html", target="_blank"),
                                        html.Br(),
                                        "Demographic, socioeconomic, education, and housing characteristics"
                                    ]
                                ),
                                html.Br(),
                                html.Div(
                                    [
                                        html.A("CalEnviroScreen", href="https://oehha.ca.gov/calenviroscreen", target="_blank"),
                                        html.Br(),
                                        "Environmental burden scores and breakdowns of vulnerability indicators"
                                    ]
                                ),
                                html.Br(),
                                html.Div(
                                    [
                                        html.A("NREL Alternative Fuel Stations Database", href="https://developer.nlr.gov/docs/transportation/alt-fuel-stations-v1/", target="_blank"),
                                        html.Br(),
                                        "Public EV charging station and charging port availability"
                                    ]
                                ),
                            ],
                        ),
                    ],
                ),

                # =========================
                # OPTIONAL PLACEHOLDER ROW
                # =========================
                html.Div(
                    className="card",
                    children=[
                        html.H2("Project Workflow", className="section-title"),
                        html.Div(
                            className="section-body",
                            children=[
                                html.P(
                                    "This section will be expanded as the project pages are completed."
                                ),
                                html.Ul(
                                    [
                                        html.Li("EDA: dataset structure, distributions, and early patterns"),
                                        html.Li("Analysis: comparative methods and relationship analysis"),
                                        html.Li("ML: predictive modeling and interpretation"),
                                        html.Li("Findings: major conclusions, implications, and limitations"),
                                    ]
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )
    ]
)