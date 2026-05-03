import dash
from dash import html

dash.register_page(__name__, path="/findings")


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


def finding_card(number, title, text):
    return html.Div(
        [
            html.Div(
                [html.Span(str(number), className="ins-number"), html.Span(title, className="fd-finding-title")],
                className="fd-finding-header",
            ),
            html.P(text, className="ins-text"),
        ],
        className="ins-card fd-finding-card",
    )


def rq_card(question, answer):
    return html.Div(
        [
            html.Div(
                [html.Span("Q", className="fd-rq-badge"), html.P(question, className="fd-rq-question")],
                className="fd-rq-top",
            ),
            html.Div(
                [html.Span("A", className="fd-rq-badge fd-rq-a"), html.P(answer, className="fd-rq-answer")],
                className="fd-rq-bottom",
            ),
        ],
        className="fd-rq-card",
    )


def implication_card(icon, title, text):
    return html.Div(
        [
            html.Span(icon, className="fd-imp-icon"),
            html.Span(title, className="fd-imp-title"),
            html.P(text, className="fd-imp-text"),
        ],
        className="fd-imp-card",
    )


def surprise_item(text):
    return html.Div(
        [html.Span("!", className="fd-surprise-icon"), html.P(text, className="fd-surprise-text")],
        className="fd-surprise-item",
    )


def limit_item(text):
    return html.Div(
        [html.Span("o", className="fd-limit-icon"), html.Span(text, className="check-text")],
        className="check-item",
    )


def future_item(text):
    return html.Div(
        [html.Span("->", className="fd-future-icon"), html.Span(text, className="check-text")],
        className="check-item",
    )


layout = html.Div(
    [
        html.Div(
            className="page-container",
            children=[

                # BANNER
                page_banner(
                    "Findings",
                    "What we learned about EV adoption disparities across California — and what it means.",
                    [
                        banner_chip("5", "Research Questions"),
                        banner_chip("8", "Key Findings"),
                        banner_chip("6", "ML Models"),
                    ],
                ),

                # 0. CONTEXT CARD
                html.Div(
                    className="card fd-context-row",
                    children=[
                        html.Div(
                            style={"flexShrink": "0"},
                            children=[
                                html.Img(
                                    src="/assets/images/forecast.png",
                                    className="fd-forecast-img",
                                ),
                                html.P(
                                    [
                                        "Source: ",
                                        html.A(
                                            "Exploding Topics, 2024",
                                            href="https://explodingtopics.com/blog/electric-vehicles-stats",
                                            target="_blank",
                                        ),
                                    ],
                                    className="fd-forecast-source",
                                ),
                            ],
                        ),
                        html.Div(
                            className="fd-context-text",
                            children=[
                                html.H2("Why This Matters Now", className="section-title"),
                                html.P(
                                    "EV adoption in California is growing fast — projected to reach 3 million vehicles by 2028. But aggregate growth figures obscure a sharper question: who is actually participating in that growth, and who is being left behind?",
                                    className="section-body",
                                ),
                                html.P(
                                    "As adoption scales, the communities still on the outside of the transition face compounding disadvantages — less exposure to the technology, fewer infrastructure investments, and weaker policy signals. The window to address these gaps equitably is narrowing.",
                                    className="section-body",
                                ),
                            ],
                        ),
                    ],
                ),

                # 1. KEY FINDINGS — 2-col grid
                html.Div(
                    className="card",
                    children=[
                        html.H2("Key Findings", className="section-title"),
                        html.P(
                            "Eight consistent patterns emerged across our exploratory analysis, regression models, and machine learning experiments.",
                            className="section-body",
                            style={"marginBottom": "20px"},
                        ),
                        html.Div(
                            [
                                finding_card(1, "Education leads the way",
                                    "Of all the factors we examined, how educated a community is turned out to be the single strongest predictor of EV adoption — even stronger than income. This held up across every model we ran."),
                                finding_card(2, "Wealth and housing follow closely",
                                    "Home values and household income are nearly as predictive as education. EV adoption is not random — it follows the geography of economic and educational advantage."),
                                finding_card(3, "Environmental burden works the other way",
                                    "Communities that already bear more pollution and poverty adopt EVs at lower rates. The places that would benefit most from cleaner transportation are the least likely to have access to it."),
                                finding_card(4, "Infrastructure helps — but not equally",
                                    "More charging stations do increase adoption, but the benefit is strongest in higher-income areas. Infrastructure alone does not close the gap; it can actually widen it if placed where demand already exists."),
                                finding_card(5, "Low-adoption areas are highly predictable",
                                    "The ZIP codes with the lowest EV adoption can be identified with remarkable accuracy. They are not scattered randomly — they cluster tightly around communities with lower education, lower income, and lower home values."),
                                finding_card(6, "Charging deserts are harder to predict",
                                    "Areas with little charging infrastructure are much less predictable than EV adoption patterns. Charger placement reflects private investment and policy decisions more than community need."),
                                finding_card(7, "Plug-in hybrids signal readiness",
                                    "Communities with more plug-in hybrid vehicles are far more likely to have high EV adoption. Hybrids appear to serve as a stepping stone — once people try partial electrification, full EVs follow."),
                                finding_card(8, "Income's effect is nonlinear",
                                    "EV adoption does not rise steadily with income — it accelerates. Once a community crosses a certain income threshold, adoption takes off rapidly. Lower-income areas face compounding barriers, not just a simple affordability gap."),
                            ],
                            className="fd-findings-grid",
                        ),
                    ],
                ),

                # 2. RESEARCH QUESTIONS REVISITED
                html.Div(
                    className="card",
                    children=[
                        html.H2("Research Questions Revisited", className="section-title"),
                        html.P(
                            "How our original questions held up against the data.",
                            className="section-body",
                            style={"marginBottom": "20px"},
                        ),
                        html.Div(
                            [
                                rq_card(
                                    "How are EV adoption rates associated with income, education, housing value, and homeownership?",
                                    "All four factors show meaningful positive associations. Education emerged as the single strongest predictor, followed by home value and income. Areas with more renters tend to have lower adoption, likely because renters can't easily install home chargers.",
                                ),
                                rq_card(
                                    "Do communities with greater environmental burden and socioeconomic vulnerability show lower EV adoption?",
                                    "Yes. Communities already facing more pollution and poverty are the least likely to be participating in the clean transportation transition — the communities that could benefit most are the furthest behind.",
                                ),
                                rq_card(
                                    "Is the relationship between income and EV adoption nonlinear, suggesting affordability thresholds?",
                                    "Yes. Income's effect accelerates at higher levels — consistent with a threshold where EVs only become a realistic option after basic affordability conditions are met. It's not a straight line.",
                                ),
                                rq_card(
                                    "Is charging infrastructure distributed unevenly across California ZIP codes?",
                                    "Yes. Higher-income ZIP codes have far more charging access per person. But infrastructure alone doesn't close adoption gaps — its impact is greatest where adoption is already strong.",
                                ),
                                rq_card(
                                    "Do structural socioeconomic factors explain the disparity that appears across racial and ethnic composition?",
                                    "Largely yes. Once we account for income, education, and housing, the apparent differences across racial groups shrink substantially. The disparities are driven more by economic structure than by race itself.",
                                ),
                            ],
                            className="fd-rq-grid",
                        ),
                    ],
                ),

                # 3 + 4. SURPRISES and IMPLICATIONS side by side
                html.Div(
                    className="fd-two-col-section",
                    children=[

                        # What Surprised Us
                        html.Div(
                            className="card",
                            style={"flex": "1", "minWidth": "0"},
                            children=[
                                html.H2("What Surprised Us", className="section-title"),
                                html.P(
                                    "A few findings diverged from what we expected going in.",
                                    className="section-body",
                                    style={"marginBottom": "18px"},
                                ),
                                html.Div(
                                    [
                                        surprise_item("Education beat income. We assumed income would dominate, but educational attainment consistently explained more variation — suggesting culture and information access matter alongside pure purchasing power."),
                                        surprise_item("Charging deserts don't mirror EV deserts. We assumed infrastructure gaps would track adoption gaps closely, but charger placement follows its own logic driven by private investment and policy rather than community need."),
                                        surprise_item("Race effects largely disappeared once we controlled for socioeconomics. The raw differences were real, but they reflected economic structure far more than racial composition itself."),
                                        surprise_item("A single behavioral variable — whether a community had already adopted plug-in hybrids — explained more than any socioeconomic factor when predicting full EV readiness."),
                                    ],
                                    className="fd-surprise-grid",
                                ),
                            ],
                        ),

                        # Policy Implications
                        html.Div(
                            className="card",
                            style={"flex": "1", "minWidth": "0"},
                            children=[
                                html.H2("Policy Implications", className="section-title"),
                                html.P(
                                    "What these findings suggest for equitable electrification in California.",
                                    className="section-body",
                                    style={"marginBottom": "20px"},
                                ),
                                html.Div(
                                    [
                                        implication_card("01", "Target incentives by income",
                                            "Flat EV rebates and credits mostly benefit communities already primed to adopt. Income-weighted incentives would reach those who need them most."),
                                        implication_card("02", "Rethink where chargers go",
                                            "Building chargers in high-income areas reinforces existing advantages. Infrastructure investment should lead demand in underserved communities, not follow it."),
                                        implication_card("03", "Use PHEVs as a bridge",
                                            "Plug-in hybrid programs in lower-income areas could lower the barrier to electrification and build familiarity that makes a full EV transition more likely."),
                                        implication_card("04", "Fix the renter problem",
                                            "Renters and apartment dwellers face real structural barriers to home charging. Funding building-level charging in multi-unit housing could open EV access to a large excluded population."),
                                    ],
                                    className="fd-imp-grid",
                                ),
                            ],
                        ),
                    ],
                ),

                # 5 + 6. LIMITATIONS and FUTURE DIRECTIONS side by side
                html.Div(
                    className="card",
                    children=[
                        html.Div(
                            className="fd-two-col-section",
                            children=[

                                html.Div(
                                    style={"flex": "1", "minWidth": "0"},
                                    children=[
                                        html.H2("Limitations", className="section-title"),
                                        html.P(
                                            "Every analysis has boundaries. These are ours.",
                                            className="section-body",
                                            style={"marginBottom": "16px"},
                                        ),
                                        html.Div(
                                            [
                                                limit_item("We observe associations, not causes. Income may drive adoption, but high-adoption areas may also attract wealthier residents over time."),
                                                limit_item("ZIP codes are large and varied. Averaging across them can hide very different neighborhoods sitting inside the same ZIP boundary."),
                                                limit_item("Key variables are missing: consumer attitudes, dealership proximity, utility electricity rates, and which EV models are actually available locally."),
                                                limit_item("The data reflects a 2021 snapshot. EV prices have fallen and infrastructure has grown since then — the patterns may be shifting."),
                                                limit_item("Our data came from different geographic levels — EV registrations and demographics were at the ZIP code level, while CalEnviroScreen environmental data was collected at the census tract level. We aggregated tract data up to ZIP codes using population weights, which introduces some mismatch and noise, especially in areas where tracts and ZIP boundaries don't align well."),
                                            ],
                                            className="check-list",
                                        ),
                                    ],
                                ),

                                html.Div(
                                    className="fd-col-divider",
                                ),

                                html.Div(
                                    style={"flex": "1", "minWidth": "0"},
                                    children=[
                                        html.H2("Future Directions", className="section-title"),
                                        html.P(
                                            "Extensions that would deepen or sharpen these findings.",
                                            className="section-body",
                                            style={"marginBottom": "16px"},
                                        ),
                                        html.Div(
                                            [
                                                future_item("Track how adoption and infrastructure change year over year across the same ZIP codes — a panel approach instead of a snapshot."),
                                                future_item("Work at the census tract level to capture finer-grained variation that ZIP code averages obscure."),
                                                future_item("Use natural experiments — like the rollout of a specific incentive program — to move from association toward causation."),
                                                future_item("Add survey data on what consumers actually cite as barriers: cost, range anxiety, access, awareness."),
                                                future_item("Test whether these patterns hold in other states with different policy environments and demographics."),
                                            ],
                                            className="check-list",
                                        ),
                                        html.Div(
                                            "This project shows how a structured data science workflow — from raw data through EDA, regression, and machine learning — can reveal equity patterns that aggregate statistics miss.",
                                            className="insight-note",
                                            style={"marginTop": "20px"},
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),

                # REFERENCES
                html.Div(
                    className="card",
                    children=[
                        html.H2("References", className="section-title"),
                        html.Div(
                            [
                                html.Div([
                                    html.Span("01", className="fd-ref-num"),
                                    html.Span([
                                        "Lopez, Nadia, and Erica Yee. ",
                                        html.Em("Who Buys Electric Cars in California — and Who Doesn't?"),
                                        " CalMatters, 22 Mar. 2023. ",
                                        html.A("calmatters.org", href="https://calmatters.org/environment/2023/03/california-electric-cars-demographics/", target="_blank", className="fd-ref-link"),
                                    ], className="fd-ref-text"),
                                ], className="fd-ref-item"),
                                html.Div([
                                    html.Span("02", className="fd-ref-num"),
                                    html.Span([
                                        "U.S. Census Bureau. ",
                                        html.Em("American Community Survey 5-Year Estimates (2023)."),
                                        " Accessed via Census API. ",
                                        html.A("census.gov", href="https://www.census.gov/data/developers/data-sets/acs-5year.html", target="_blank", className="fd-ref-link"),
                                    ], className="fd-ref-text"),
                                ], className="fd-ref-item"),
                                html.Div([
                                    html.Span("03", className="fd-ref-num"),
                                    html.Span([
                                        "California OEHHA. ",
                                        html.Em("CalEnviroScreen 4.0."),
                                        " Accessed Dec. 2025. ",
                                        html.A("oehha.ca.gov", href="https://oehha.ca.gov/calenviroscreen", target="_blank", className="fd-ref-link"),
                                    ], className="fd-ref-text"),
                                ], className="fd-ref-item"),
                                html.Div([
                                    html.Span("04", className="fd-ref-num"),
                                    html.Span([
                                        "National Renewable Energy Laboratory. ",
                                        html.Em("Alternative Fuel Stations API."),
                                        " ",
                                        html.A("developer.nrel.gov", href="https://developer.nrel.gov/docs/transportation/alt-fuel-stations-v1/", target="_blank", className="fd-ref-link"),
                                    ], className="fd-ref-text"),
                                ], className="fd-ref-item"),
                                html.Div([
                                    html.Span("05", className="fd-ref-num"),
                                    html.Span([
                                        "Exploding Topics. ",
                                        html.Em("Electric Vehicle Statistics & Trends (2024)."),
                                        " ",
                                        html.A("explodingtopics.com", href="https://explodingtopics.com/blog/electric-vehicles-stats", target="_blank", className="fd-ref-link"),
                                    ], className="fd-ref-text"),
                                ], className="fd-ref-item"),
                            ],
                            className="fd-ref-list",
                        ),
                    ],
                ),
            ],
        )
    ]
)
