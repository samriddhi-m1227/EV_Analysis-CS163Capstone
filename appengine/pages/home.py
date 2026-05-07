import dash
from dash import html, dcc

dash.register_page(__name__, path="/")


def stat_chip(value, label):
    return html.Div(
        [
            html.Span(value, className="hero-stat-value"),
            html.Span(label, className="hero-stat-label"),
        ],
        className="hero-stat-chip",
    )


def rq_card(number, text):
    return html.Div(
        [
            html.Span(str(number), className="rq-number"),
            html.P(text, className="rq-text"),
        ],
        className="rq-card",
    )


def source_card(name, description, href):
    return html.A(
        [
            html.Span(name, className="src-name"),
            html.Span(description, className="src-desc"),
        ],
        href=href,
        target="_blank",
        className="src-card",
    )


def step_item(number, title, desc):
    return html.Div(
        [
            html.Div(str(number), className="step-number"),
            html.Div(
                [
                    html.Span(title, className="step-title"),
                    html.Span(desc, className="step-desc"),
                ],
                className="step-text",
            ),
        ],
        className="step-item",
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
                        html.Div(className="hero-dot-grid"),
                        html.H1(
                            "Electric Vehicle Adoption & Infrastructure Disparities in California",
                            className="hero-title",
                        ),
                        html.P("Group 14  ·  Samriddhi Matharu & Bhavya", className="hero-byline"),

                        # Stat strip
                        html.Div(
                            [
                                stat_chip("1,800+", "ZIP Codes"),
                                stat_chip("4", "Datasets Merged"),
                                stat_chip("6", "ML Models"),
                                stat_chip("California", "Statewide"),
                            ],
                            className="hero-stats",
                        ),

                        # CTA
                        dcc.Link(
                            "Explore the Project →",
                            href="/data",
                            className="hero-cta",
                        ),
                    ],
                ),

                # =========================
                # PROJECT OVERVIEW
                # =========================
                html.Div(
                    className="card",
                    children=[
                        html.Div(
                            className="home-intro-row",
                            children=[
                                html.Div(
                                    className="home-intro-text",
                                    children=[
                                        html.H2("Project Summary", className="section-title"),
                                        html.P(
                                            "California is undergoing a large-scale transition toward electric vehicles, with statewide goals aimed at reducing emissions and expanding clean transportation. However, EV adoption and public charging infrastructure may not be evenly distributed across communities. Socioeconomic conditions, housing characteristics, environmental disadvantage, and infrastructure availability shape which communities adopt EVs more rapidly and which lag behind.",
                                            className="section-body",
                                        ),
                                        html.P(
                                            "This project analyzes EV adoption and community-level disparities across California ZIP codes — applying an end-to-end data science workflow from data curation through exploratory analysis, regression modeling, and machine learning.",
                                            className="section-body",
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="home-intro-img-col",
                                    children=[
                                        html.Img(
                                            src="/assets/images/car_bg.png",
                                            className="home-intro-photo",
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),

                # =========================
                # WHY THIS MATTERS + IMAGES
                # =========================
                html.Div(
                    className="card",
                    children=[
                        html.H2("Why This Matters", className="section-title"),

                        # Images side by side
                        html.Div(
                            className="wtm-img-row",
                            children=[
                                html.Div(
                                    className="wtm-img-item",
                                    children=[
                                        html.Img(src="/assets/images/forecast.png", className="home-viz-img"),
                                        html.P(
                                            ["Source: ", html.A("Exploding Topics, 2024", href="https://explodingtopics.com/blog/electric-vehicles-stats", target="_blank")],
                                            className="home-viz-source",
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="wtm-img-item",
                                    children=[
                                        html.Img(src="/assets/images/change.png", className="home-viz-img"),
                                        html.P(
                                            ["Source: ", html.A("Axios SF, 2025", href="https://www.axios.com/local/san-francisco/2025/03/20/california-ev-chargers-increase-statewide", target="_blank")],
                                            className="home-viz-source",
                                        ),
                                    ],
                                ),
                            ],
                        ),

                        # Text below
                        html.P(
                            "EV adoption in California is growing fast — projected to reach 3 million vehicles by 2028. But aggregate growth figures obscure a sharper question: who is actually participating in that growth, and who is being left behind?",
                            className="section-body",
                        ),
                        html.P(
                            "Understanding EV disparities is essential for evaluating whether California's clean transportation transition is equitable. If EV adoption and charging access remain concentrated in wealthier or structurally advantaged communities, the benefits of electrification may not be shared broadly.",
                            className="section-body",
                        ),
                        html.P(
                            "Looking beyond statewide averages reveals how local conditions — income, education, housing tenure, and charging infrastructure — shape which communities participate in the EV transition and which are left out.",
                            className="section-body",
                        ),
                    ],
                ),

                # =========================
                # ROW 1
                # =========================
                html.Div(
                    className="card",
                    children=[
                        html.H2("Key Research Questions", className="section-title"),
                        html.Div(
                            [
                                rq_card(1, "How are EV adoption rates associated with income, education, housing value, and homeownership?"),
                                rq_card(2, "Do communities with greater environmental burden and socioeconomic vulnerability show lower EV adoption?"),
                                rq_card(3, "Is the relationship between income and EV adoption nonlinear, suggesting affordability thresholds?"),
                                rq_card(4, "Is charging infrastructure distributed unevenly across California ZIP codes?"),
                                rq_card(5, "Do structural socioeconomic factors explain the disparity that appears across racial and ethnic composition?"),
                            ],
                            className="rq-grid",
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
                                html.Div(
                                    [
                                        source_card(
                                            "CalMatters",
                                            "EV adoption rates, vehicle counts, Zillow home indicators by ZIP code",
                                            "https://github.com/CalMatters/ev-zipcode-demographics-data",
                                        ),
                                        source_card(
                                            "American Community Survey (ACS)",
                                            "Demographic, socioeconomic, education, and housing characteristics",
                                            "https://www.census.gov/data/developers/data-sets/acs-5year.html",
                                        ),
                                        source_card(
                                            "CalEnviroScreen",
                                            "Environmental burden scores and vulnerability indicators",
                                            "https://oehha.ca.gov/calenviroscreen",
                                        ),
                                        source_card(
                                            "NREL Alt Fuel Stations",
                                            "Public EV charging station and port availability",
                                            "https://developer.nrel.gov/docs/transportation/alt-fuel-stations-v1/",
                                        ),
                                    ],
                                    className="src-grid",
                                ),
                            ],
                        ),
                    ],
                ),

                # =========================
                # PROJECT WORKFLOW STEPPER
                # =========================
                html.Div(
                    className="card",
                    children=[
                        html.H2("Project Workflow", className="section-title"),
                        html.Div(
                            [
                                step_item(1, "Data Ingestion", "Sourced & merged 4 public datasets at ZIP-code level"),
                                html.Div(className="step-connector"),
                                step_item(2, "EDA", "Distributions, spatial patterns, and early correlations"),
                                html.Div(className="step-connector"),
                                step_item(3, "Analysis", "Comparative methods and relationship analysis"),
                                html.Div(className="step-connector"),
                                step_item(4, "ML Modeling", "6 predictive models with interpretation"),
                                html.Div(className="step-connector"),
                                step_item(5, "Findings", "Conclusions, equity implications, and limitations"),
                            ],
                            className="stepper",
                        ),
                    ],
                ),

                # =========================
                # CONTRIBUTORS
                # =========================
                html.Div(
                    className="card contributors-card",
                    children=[
                        html.H2("About the Contributors", className="section-title"),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Img(src="/assets/images/sam.png", className="contributor-avatar"),
                                        html.H3("Samriddhi Matharu", className="contributor-name"),
                                        html.P(
                                            "Samriddhi is a B.S. Data Science '26 student at San Jose State University with experience across data, software, and product roles. She holds leadership roles in technical consulting on campus and is passionate about responsible computing. She led the data pipeline, exploratory analysis, modeling, and website development for this project.",
                                            className="contributor-bio",
                                        ),
                                    ],
                                    className="contributor-card",
                                ),
                                html.Div(
                                    [
                                        html.Img(src="/assets/images/bhavya.png", className="contributor-avatar"),
                                        html.H3("Bhavya", className="contributor-name"),
                                        html.P(
                                            "Bhavya is a B.S. Data Science 26' student at San Jose State University with experience across data analytics, BI, and ML focused roles. She holds leadership roles in research, analytics and excel. For this project, led the data pipeline, exploratory analysis, and further analysis to support the development and validation of the machine learning model and its findings.",
                                            className="contributor-bio",
                                        ),
                                    ],
                                    className="contributor-card",
                                ),
                            ],
                            className="contributors-grid",
                        ),
                    ],
                ),
            ],
        )
    ]
)
