import dash
from dash import html, dcc

dash.register_page(__name__, path="/ml")

RIDGE_COEFFICIENTS = [
    {"feature": "BachOrHigher_perc",       "coefficient": 1.5155},
    {"feature": "Zillow_Home_Value_Index",  "coefficient": 0.8055},
    {"feature": "Median_Household_Income",  "coefficient": 0.5566},
    {"feature": "CES_Score_ZIP",            "coefficient": 0.4261},
    {"feature": "MultiUnitShare",           "coefficient": 0.1524},
    {"feature": "PortsPer10kPeople",        "coefficient": 0.1339},
    {"feature": "Traffic_ZIP",              "coefficient": 0.0858},
    {"feature": "PollutionBurden_ZIP",      "coefficient": -0.0947},
    {"feature": "RenterShare",              "coefficient": -0.1565},
]

MODEL4_IMPORTANCE = [
    {"feature": "BachOrHigher_perc",      "importance": 0.150},
    {"feature": "MultiUnitShare",         "importance": 0.138},
    {"feature": "Traffic_ZIP",            "importance": 0.114},
    {"feature": "Zillow_Home_Value_Index","importance": 0.113},
    {"feature": "EV_perc",               "importance": 0.110},
    {"feature": "RenterShare",            "importance": 0.108},
    {"feature": "Median_Household_Income","importance": 0.092},
    {"feature": "PollutionBurden_ZIP",    "importance": 0.087},
    {"feature": "CES_Score_ZIP",          "importance": 0.087},
]

MODELS = [
    {
        "number": "01",
        "title": "EV Adoption Prediction",
        "question": "Who adopts EVs?",
        "type": "Ridge · Random Forest",
        "target": "EV_perc",
        "why": "We used Ridge Regression and Random Forest Regressor to identify which factors most strongly predict EV adoption rates across California ZIP codes.",
        "metrics": [
            {"label": "Ridge R²", "value": "0.873"},
            {"label": "RF R²", "value": "0.894"},
        ],
        "results": [
            "Top features: education level, home value, median income",
            "Education alone accounts for a large share of model variance",
            "Infrastructure plays a positive but secondary role",
        ],
        "takeaway": "EV adoption is primarily driven by socioeconomic advantage — especially education, wealth, and income. Infrastructure plays a secondary role.",
        "image": "education_vs_ev.png",
        "image_caption": "Education level vs. EV adoption rate across California ZIP codes.",
        "coeff_data": RIDGE_COEFFICIENTS,
    },
    {
        "number": "02",
        "title": "Income × Infrastructure Interaction",
        "question": "Does infrastructure help all income groups equally?",
        "type": "Ridge w/ Interaction",
        "target": "EV_perc",
        "why": "We added an interaction term between income and charging infrastructure to test whether greater access has the same effect across all income levels.",
        "metrics": [
            {"label": "R²", "value": "0.872"},
            {"label": "Income × Infra coeff", "value": "+0.106"},
        ],
        "results": [
            "Interaction term is positive and meaningful",
            "Infrastructure boosts adoption more in high-income areas",
            "Low-income communities benefit less from added charging access",
        ],
        "takeaway": "Infrastructure reinforces existing advantages rather than closing adoption gaps. High-income areas see a stronger benefit from each additional charger.",
        "image": "model2_infrastructure_income_interaction.png",
        "image_caption": "Charging infrastructure has a stronger relationship with EV adoption in high-income areas, suggesting that infrastructure benefits are not distributed equally.",
    },
    {
        "number": "03",
        "title": "EV Desert Classification",
        "question": "Who is left behind in the EV transition?",
        "type": "Logistic · RF Classifier",
        "target": "EV_desert (bottom 20%)",
        "why": "We classified which communities fall into EV deserts — the bottom 20% of adoption — using Logistic Regression and Random Forest.",
        "metrics": [
            {"label": "Logistic AUC", "value": "0.968"},
            {"label": "RF AUC", "value": "0.974"},
        ],
        "results": [
            "Strongest features: education, home value, income",
            "EV deserts are highly predictable from structural disadvantage",
            "Very high classification accuracy across both models",
        ],
        "takeaway": "EV deserts are highly predictable and concentrated in communities with lower education, lower housing wealth, and lower income.",
        "image": "model3_ev_desert_importance.png",
        "image_caption": "EV deserts are primarily driven by lower education, lower home value, and lower income.",
        "image_max_width": "580px",
    },
    {
        "number": "04",
        "title": "Infrastructure Desert Classification",
        "question": "Who lacks access to public charging?",
        "type": "Logistic · RF Classifier",
        "target": "infra_desert",
        "why": "We predicted which ZIP codes have very low or zero public charging access to understand whether infrastructure gaps follow the same logic as adoption gaps.",
        "metrics": [
            {"label": "Logistic AUC", "value": "0.714"},
            {"label": "RF AUC", "value": "0.692"},
        ],
        "results": [
            "Top features: education, multi-unit housing, traffic, home value",
            "Significantly harder to classify than EV adoption itself",
            "Infrastructure placement depends on policy and geography beyond demand",
        ],
        "takeaway": "Infrastructure access is less predictable than EV adoption. Placement likely depends on policy, funding, geography, and private investment — not just community need.",
        "image": None,
        "image_caption": None,
        "importance_data": MODEL4_IMPORTANCE,
        "importance_title": "Infrastructure Desert Feature Importance",
        "importance_caption": "Infrastructure deserts are influenced by multiple factors, with no single dominant predictor, suggesting charging access is shaped by broader planning and investment decisions.",
    },
    {
        "number": "05",
        "title": "Adoption Pathway Model",
        "question": "Are plug-in hybrids a stepping stone to full EV adoption?",
        "type": "Ridge · Random Forest",
        "target": "EV_perc",
        "why": "We tested whether PHEV (plug-in hybrid) adoption rates can predict community readiness for full battery-electric vehicle adoption.",
        "metrics": [
            {"label": "R²", "value": "0.943"},
            {"label": "PHEV_share coeff", "value": "dominant"},
        ],
        "results": [
            "PHEV_share is the single dominant predictor",
            "Gasoline_Hybrid_share carries a negative coefficient",
            "Traditional hybrids do not signal the same readiness pathway",
        ],
        "takeaway": "Plug-in hybrid adoption is strongly associated with higher EV adoption, indicating that PHEVs may reflect community readiness for full electrification. Traditional gasoline hybrids do not show the same relationship.",
        "image": "model5_phev_vs_ev.png",
        "image_caption": "ZIP codes with higher plug-in hybrid adoption also tend to have higher EV adoption, supporting the idea of a transition pathway toward full electric vehicles.",
    },
    {
        "number": "06",
        "title": "High-Income Subset Analysis",
        "question": "Within wealthy areas, what still explains variation?",
        "type": "Ridge Regression",
        "target": "EV_perc (top quintile)",
        "why": "We focused on the top income quintile to identify what differentiates high- from moderate-adopting communities even after controlling for wealth.",
        "metrics": [
            {"label": "PHEV_share", "value": "1.742"},
            {"label": "Education coeff", "value": "1.156"},
            {"label": "Infra (ports)", "value": "0.173"},
        ],
        "results": [
            "PHEV adoption and education remain the top differentiators",
            "Infrastructure (PortsPer10kPeople) still contributes positively",
            "MultiUnitShare shows a negative coefficient (−0.317)",
        ],
        "takeaway": "Even among high-income communities, EV adoption varies meaningfully. PHEV adoption, education, infrastructure, and housing structure all still matter.",
    },
]


def stat_chip(value, label):
    return html.Div(
        className="ml-stat-item",
        children=[
            html.Span(value, className="ml-stat-value"),
            html.Span(label, className="ml-stat-label"),
        ],
    )


FEATURE_LABELS = {
    "BachOrHigher_perc":      "Education (Bach+)",
    "Zillow_Home_Value_Index": "Home Value Index",
    "Median_Household_Income": "Median HH Income",
    "CES_Score_ZIP":           "CES Score",
    "MultiUnitShare":          "Multi-Unit Housing",
    "PortsPer10kPeople":       "Ports per 10k Pop.",
    "Traffic_ZIP":             "Traffic Exposure",
    "PollutionBurden_ZIP":     "Pollution Burden",
    "RenterShare":             "Renter Share",
    "EV_perc":                 "EV Adoption Rate",
}


def coeff_table(data):
    rows = []
    for i, row in enumerate(data):
        is_top3 = i < 3
        is_neg  = row["coefficient"] < 0
        label   = FEATURE_LABELS.get(row["feature"], row["feature"])
        val     = row["coefficient"]

        feature_cls = "ml-ct-feature ml-ct-bold" if is_top3 else "ml-ct-feature"
        coeff_cls   = "ml-ct-val ml-ct-neg" if is_neg else ("ml-ct-val ml-ct-bold ml-ct-pos" if is_top3 else "ml-ct-val")
        row_cls     = "ml-ct-row-hi" if is_top3 else ""

        rows.append(html.Tr([
            html.Td(label, className=feature_cls),
            html.Td(f"{val:.3f}", className=coeff_cls),
        ], className=row_cls))

    return html.Div(
        className="ml-coeff-card",
        children=[
            html.P("Ridge Regression Coefficients", className="ml-coeff-title"),
            html.Table(
                className="ml-ct",
                children=[
                    html.Thead(html.Tr([
                        html.Th("Feature", className="ml-ct-th"),
                        html.Th("Coeff.", className="ml-ct-th ml-ct-th-r"),
                    ])),
                    html.Tbody(rows),
                ],
            ),
            html.P(
                "Education, home value, and income are the strongest drivers of EV adoption.",
                className="ml-coeff-caption",
            ),
        ],
    )


def importance_table(data, title, caption):
    rows = []
    for i, row in enumerate(data):
        is_top3    = i < 3
        feature_cls = "ml-ct-feature ml-ct-bold" if is_top3 else "ml-ct-feature"
        val_cls     = "ml-ct-val ml-ct-pos ml-ct-bold" if is_top3 else "ml-ct-val"
        row_cls     = "ml-ct-row-hi" if is_top3 else ""
        label       = FEATURE_LABELS.get(row["feature"], row["feature"])
        rows.append(html.Tr([
            html.Td(label, className=feature_cls),
            html.Td(f"{row['importance']:.3f}", className=val_cls),
        ], className=row_cls))

    return html.Div(
        className="ml-coeff-card",
        style={"maxWidth": "620px", "margin": "24px auto 0 auto"},
        children=[
            html.P(title, className="ml-coeff-title"),
            html.Table(
                className="ml-ct",
                children=[
                    html.Thead(html.Tr([
                        html.Th("Feature", className="ml-ct-th"),
                        html.Th("Importance", className="ml-ct-th ml-ct-th-r"),
                    ])),
                    html.Tbody(rows),
                ],
            ),
            html.P(caption, className="ml-coeff-caption"),
        ],
    )


def tab_content(m):
    if m.get("image") and m.get("coeff_data"):
        viz = html.Div(
            style={
                "display": "flex",
                "flexDirection": "row",
                "gap": "24px",
                "alignItems": "flex-start",
                "marginTop": "24px",
            },
            children=[
                html.Div(
                    style={"flex": "3", "minWidth": "0"},
                    children=[
                        html.Img(
                            src=f"/static/images/{m['image']}",
                            className="ml-viz-image",
                        ),
                        html.P(m["image_caption"], className="viz-caption"),
                    ],
                ),
                html.Div(
                    style={"flex": "2", "minWidth": "0"},
                    children=[coeff_table(m["coeff_data"])],
                ),
            ],
        )
    elif m.get("image"):
        img_style = {"maxWidth": m["image_max_width"], "margin": "0 auto"} if m.get("image_max_width") else {}
        viz = html.Div(
            className="ml-viz-block",
            children=[
                html.Img(src=f"/static/images/{m['image']}", className="ml-viz-image", style=img_style),
                html.P(m["image_caption"], className="viz-caption"),
            ],
        )
    elif m.get("importance_data"):
        viz = importance_table(m["importance_data"], m["importance_title"], m["importance_caption"])
    elif "image" in m:
        viz = html.Div(
            className="ml-viz-placeholder",
            children=[
                html.Span("📊 ", className="ml-viz-icon"),
                html.Span(
                    "Visualization coming soon — chart will appear here once exported.",
                    className="ml-viz-label",
                ),
            ],
        )
    else:
        viz = html.Div()

    return html.Div(
        className="ml-detail-panel",
        children=[
            html.Div(
                className="ml-model-header",
                children=[
                    html.Span(m["number"], className="ml-number-badge"),
                    html.Div(
                        className="ml-title-block",
                        children=[
                            html.H3(m["title"], className="ml-card-title"),
                            html.P(f'"{m["question"]}"', className="ml-question"),
                        ],
                    ),
                    html.Div(
                        className="ml-badge-row",
                        children=[
                            html.Span(m["type"], className="ml-badge ml-badge-type"),
                            html.Span(m["target"], className="ml-badge ml-badge-target"),
                        ],
                    ),
                ],
            ),

            html.Hr(className="ml-divider"),

            html.Div(
                className="ml-body",
                children=[
                    html.Div([
                        html.P(m["why"], className="page-text"),
                        html.Ul(
                            [html.Li(r) for r in m["results"]],
                            className="ml-results-list",
                        ),
                    ]),
                    html.Div([
                        html.Div(
                            className="ml-stat-grid",
                            children=[stat_chip(s["value"], s["label"]) for s in m["metrics"]],
                        ),
                        html.Div(m["takeaway"], className="insight-note"),
                    ]),
                ],
            ),

            viz,
        ],
    )


def overview_table():
    rows = [
        ("01", "Who adopts EVs?", "EV_perc", "Ridge · RF Regressor", "Education, wealth, and income are the dominant drivers."),
        ("02", "Does infrastructure help all groups equally?", "EV_perc", "Ridge w/ Interaction", "Infrastructure benefits high-income areas more."),
        ("03", "Who is left behind?", "EV_desert", "Logistic · RF Classifier", "EV deserts are highly predictable from structural disadvantage."),
        ("04", "Who lacks charging access?", "infra_desert", "Logistic · RF Classifier", "Access is less predictable; depends on external factors."),
        ("05", "Are hybrids a stepping stone?", "EV_perc", "Ridge · RF Regressor", "PHEV adoption strongly signals readiness for full EVs."),
        ("06", "What drives adoption within wealthy areas?", "EV_perc (top quintile)", "Ridge Regression", "PHEV adoption, education, and housing still differentiate."),
    ]
    return html.Table(
        className="ml-overview-table",
        children=[
            html.Thead(
                html.Tr([html.Th(h) for h in ["#", "Research Question", "Target", "Model Type", "Key Insight"]])
            ),
            html.Tbody([
                html.Tr([html.Td(c) for c in row])
                for row in rows
            ]),
        ],
    )


layout = html.Div(
    className="page-container",
    children=[
        html.H1(
            "Modeling: Who Adopts, Who's Left Behind, and Why?",
            className="page-header",
        ),
        html.P(
            "Six models, each answering a distinct equity question. Select a model below to explore its design, "
            "results, and takeaways.",
            style={
                "textAlign": "center",
                "maxWidth": "780px",
                "margin": "0 auto 32px auto",
                "color": "var(--muted)",
                "fontSize": "15px",
                "lineHeight": "1.7",
            },
        ),

        html.Div(
            className="card",
            children=[
                html.H2("Modeling Overview", className="subsection-title"),
                html.P(
                    "Each model is designed to answer a specific question about EV equity in California.",
                    className="page-text",
                    style={"marginBottom": "18px"},
                ),
                overview_table(),
            ],
        ),

        dcc.Tabs(
            id="ml-tabs",
            value="01",
            className="ml-tabs-container",
            children=[
                dcc.Tab(
                    label=f"Model {i + 1}",
                    value=m["number"],
                    className="ml-tab",
                    selected_className="ml-tab-selected",
                    children=tab_content(m),
                )
                for i, m in enumerate(MODELS)
            ],
        ),

        html.Div(
            className="card ml-summary-card",
            children=[
                html.H2("Key Takeaways", className="subsection-title"),
                html.Ul(
                    className="ml-results-list",
                    children=[
                        html.Li("EV adoption is highly structured and strongly driven by socioeconomic factors, with education emerging as the most consistent predictor across models."),
                        html.Li("Infrastructure does influence EV adoption, but its impact is not equal — it has a stronger effect in higher-income communities, suggesting it may reinforce existing advantages."),
                        html.Li("EV deserts are highly predictable and concentrated in disadvantaged areas, indicating clear disparities in adoption across communities."),
                        html.Li("In contrast, infrastructure access is less structured and harder to predict, suggesting that charging availability is influenced by broader planning, policy, and investment decisions rather than demand alone."),
                        html.Li("Adoption follows a differentiated pathway: plug-in hybrid (PHEV) adoption is strongly associated with EV adoption, while traditional gasoline hybrids do not show the same relationship."),
                        html.Li("Even among high-income communities, EV adoption varies significantly, with infrastructure access, education, and housing constraints continuing to shape outcomes."),
                        html.Li("Overall, EV adoption disparities cannot be explained by a single factor — they emerge from a combination of socioeconomic conditions, infrastructure access, and behavioral readiness."),
                    ],
                ),
            ],
        ),
    ],
)
