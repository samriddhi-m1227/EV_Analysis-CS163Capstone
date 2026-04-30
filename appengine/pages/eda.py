import os
import pandas as pd
import dash
from dash import html, dash_table

dash.register_page(__name__, path="/eda")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "final.csv")
df = pd.read_csv(DATA_PATH)

COLUMN_DEFINITIONS = {
    "ZIP": "ZIP code identifier for each observation.",
    "County": "California county corresponding to the ZIP code.",
    "Diesel": "Number of diesel vehicles registered.",
    "Electric": "Number of fully electric vehicles.",
    "Flex_Fuel": "Number of flex-fuel vehicles.",
    "Gasoline": "Number of gasoline vehicles.",
    "Gasoline_Hybrid": "Number of hybrid gasoline vehicles.",
    "Hydrogen": "Number of hydrogen fuel cell vehicles.",
    "Natural_Gas": "Number of natural gas vehicles.",
    "PHEV": "Number of plug-in hybrid electric vehicles.",
    "Propane": "Number of propane vehicles.",
    "Total_Cars": "Total number of vehicles registered in the ZIP code.",
    "Total_EV": "Total number of electric vehicles, combining battery electric and plug-in hybrid vehicles.",
    "EV_perc": "Percentage of vehicles that are electric. This is the primary target variable for analysis.",
    "Median_Household_Income": "Median household income in the ZIP code.",
    "Total_Population": "Total population residing in the ZIP code.",
    "Latino_perc": "Percentage of residents identifying as Latino.",
    "White_perc": "Percentage of residents identifying as White.",
    "Asian_perc": "Percentage of residents identifying as Asian.",
    "Black_perc": "Percentage of residents identifying as Black.",
    "BachOrHigher_perc": "Percentage of residents with a bachelor's degree or higher.",
    "Zillow_Home_Value_Index": "Estimated average housing value in the ZIP code.",
    "Gini": "Income inequality index from 0 to 1.",
    "RenterShare": "Share of households that rent their homes.",
    "SingleFamilyShare": "Share of housing units that are single-family homes.",
    "MultiUnitShare": "Share of housing units that are multi-unit buildings.",
    "ZeroVehicleShare": "Share of households without access to a vehicle.",
    "PovertyShare": "Share of residents living below the poverty line.",
    "CES_Score_ZIP": "Overall CalEnviroScreen score. Higher = worse burden.",
    "PollutionBurden_ZIP": "Pollution exposure indicator. Higher = worse.",
    "Traffic_ZIP": "Traffic-related pollution indicator.",
    "Num_Stations": "Number of EV charging stations in the ZIP code.",
    "Total_Ports": "Total number of EV charging ports.",
    "L2_Ports": "Number of Level 2 charging ports.",
    "DC_Fast_Ports": "Number of DC fast charging ports.",
}

VARIABLE_GROUPS = {
    "EV Adoption": ["EV_perc", "Total_EV", "Electric", "PHEV"],
    "Vehicle Mix": ["Gasoline", "Diesel", "Gasoline_Hybrid", "Flex_Fuel", "Natural_Gas", "Hydrogen", "Propane", "Total_Cars"],
    "Socioeconomic": ["Median_Household_Income", "BachOrHigher_perc", "PovertyShare", "Gini"],
    "Demographics": ["Total_Population", "Latino_perc", "White_perc", "Asian_perc", "Black_perc"],
    "Housing": ["Zillow_Home_Value_Index", "RenterShare", "SingleFamilyShare", "MultiUnitShare", "ZeroVehicleShare"],
    "Environment": ["CES_Score_ZIP", "PollutionBurden_ZIP", "Traffic_ZIP"],
    "Infrastructure": ["Num_Stations", "Total_Ports", "L2_Ports", "DC_Fast_Ports"],
    "Geography": ["ZIP", "County"],
}

GROUP_COLORS = {
    "EV Adoption": "chip-green",
    "Vehicle Mix": "chip-slate",
    "Socioeconomic": "chip-blue",
    "Demographics": "chip-purple",
    "Housing": "chip-orange",
    "Environment": "chip-red",
    "Infrastructure": "chip-teal",
    "Geography": "chip-slate",
}


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


def column_chip(name):
    group_color = next(
        (GROUP_COLORS[g] for g, cols in VARIABLE_GROUPS.items() if name in cols),
        "chip-slate",
    )
    return html.Span(
        name,
        className=f"column-chip {group_color}",
        title=COLUMN_DEFINITIONS.get(name, "No description available."),
    )


def dataset_preview_table(dataframe, n_rows=5):
    preview_df = dataframe.head(n_rows).copy()
    columns = [{"name": col, "id": col} for col in preview_df.columns]
    return dash_table.DataTable(
        columns=columns,
        data=preview_df.to_dict("records"),
        page_size=n_rows,
        sort_action="native",
        style_table={"overflowX": "auto", "border": "1px solid var(--border)", "borderRadius": "12px"},
        style_cell={
            "textAlign": "left", "padding": "10px", "minWidth": "120px", "maxWidth": "220px",
            "whiteSpace": "normal", "backgroundColor": "var(--surface)", "color": "var(--text)",
            "border": "1px solid var(--border)", "fontFamily": "Inter, sans-serif", "fontSize": "13px",
        },
        style_header={"backgroundColor": "var(--surface-2)", "fontWeight": "600", "color": "var(--heading)"},
    )


def viz_wide(title, image_file, caption, insight):
    """Single viz: image left, insight right."""
    return html.Div(
        className="viz-wide",
        children=[
            html.H3(title, className="subsection-title"),
            html.Div(
                className="viz-wide-row",
                children=[
                    html.Div(
                        className="viz-wide-img-col",
                        children=[
                            html.Img(src=f"/static/images/{image_file}", className="viz-image"),
                            html.P(caption, className="viz-caption"),
                        ],
                    ),
                    html.Div(
                        className="viz-wide-text-col",
                        children=[html.P(insight, className="viz-insight-text")],
                    ),
                ],
            ),
        ],
    )


def viz_paired(title, image_file, caption, insight):
    """Compact viz card for use inside a two-column grid."""
    return html.Div(
        className="viz-block",
        children=[
            html.H3(title, className="subsection-title"),
            html.Img(src=f"/static/images/{image_file}", className="viz-image"),
            html.P(caption, className="viz-caption"),
            html.P(insight, className="insight-note", style={"marginTop": "12px"}),
        ],
    )


def quality_category(label, items):
    return html.Div(
        [
            html.Span(label, className="qc-label"),
            html.Ul([html.Li(i) for i in items], className="qc-list"),
        ],
        className="qc-card",
    )


def insight_card(number, text):
    return html.Div(
        [html.Span(str(number), className="ins-number"), html.P(text, className="ins-text")],
        className="ins-card",
    )


layout = html.Div(
    [
        html.Div(
            className="page-container",
            children=[

                # BANNER
                page_banner(
                    "Exploratory Data Analysis",
                    "Uncovering patterns in EV adoption, income, environment, and infrastructure across California ZIP codes",
                    [],
                ),

                # 1. OVERVIEW + PREVIEW
                html.Div(
                    className="card",
                    children=[
                        html.H2("1. Dataset Preview", className="section-title"),
                        html.Div(className="section-body", children=[
                            html.P(
                                "Using the final integrated ZIP-level dataset, this section explores the distribution of EV adoption "
                                "and early relationships between adoption rates, socioeconomic conditions, environmental burden, housing structure, and charging infrastructure."
                            ),
                            dataset_preview_table(df),
                            html.Div(
                                "Scroll horizontally to inspect all columns. Click any header to sort.",
                                className="insight-note",
                                style={"marginTop": "12px"},
                            ),
                        ]),
                    ],
                ),

                # 2. KEY VARIABLES
                html.Div(
                    className="card",
                    children=[
                        html.H2("2. Key Variables", className="section-title"),
                        html.Div(
                            className="two-column-grid",
                            children=[
                                html.Div(
                                    className="half-card variable-card",
                                    children=[
                                        html.H3("All Dataset Columns", className="subsection-title"),
                                        html.P("Hover any chip to see its definition. Color = variable group.", className="caption-text"),
                                        html.Div(
                                            className="column-chip-container",
                                            children=[
                                                html.Div(
                                                    [
                                                        html.Span(group, className="chip-group-label"),
                                                        html.Div(
                                                            [column_chip(c) for c in cols],
                                                            className="chip-group-row",
                                                        ),
                                                    ],
                                                    className="chip-group",
                                                )
                                                for group, cols in VARIABLE_GROUPS.items()
                                            ],
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="half-card variable-card",
                                    children=[
                                        html.H3("Priority Variables", className="subsection-title"),
                                        html.Div(
                                            "EV_perc is the primary outcome — the share of registered vehicles that are electric in each ZIP code.",
                                            className="insight-note",
                                        ),
                                        html.Ul(
                                            className="priority-variable-list",
                                            children=[
                                                html.Li([html.Strong("Target: "), "EV_perc — central variable throughout EDA and modeling."]),
                                                html.Li([html.Strong("Socioeconomic: "), "Median_Household_Income and BachOrHigher_perc."]),
                                                html.Li([html.Strong("Housing: "), "Zillow_Home_Value_Index, RenterShare, SingleFamilyShare, MultiUnitShare."]),
                                                html.Li([html.Strong("Vulnerability: "), "Gini, PovertyShare, ZeroVehicleShare."]),
                                                html.Li([html.Strong("Environment: "), "CES_Score_ZIP, PollutionBurden_ZIP, Traffic_ZIP."]),
                                                html.Li([html.Strong("Infrastructure: "), "Num_Stations, Total_Ports, L2_Ports, DC_Fast_Ports."]),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),

                # 3. DATA QUALITY
                html.Div(
                    className="card",
                    children=[
                        html.H2("3. Data Overview & Quality", className="section-title"),
                        html.P(
                            "The dataset captures ZIP-level differences across California, combining socioeconomic, environmental, and infrastructure factors.",
                            className="section-body",
                        ),
                        html.Div(
                            [
                                quality_category("Feature Categories", [
                                    "Income & Wealth: income, home values, inequality, poverty",
                                    "Education: bachelor's degree attainment",
                                    "Demographics: race and ethnicity composition",
                                    "Housing: renter share, housing type, vehicle access",
                                    "Environmental Burden: CES score, pollution, traffic",
                                    "Infrastructure: charging stations and ports",
                                ]),
                                quality_category("Data Quality Checks", [
                                    "Most variables have low missingness; environmental metrics slightly higher.",
                                    "No duplicate ZIP-level records after merging.",
                                    "Share-based variables checked for valid ranges.",
                                    "EV adoption values cross-checked against registered counts.",
                                ]),
                                html.Div(
                                    [
                                        html.Span("Derived Features", className="qc-label"),
                                        html.Div(
                                            [
                                                html.Span("HomeownerShare", className="column-chip chip-orange", title="Computed from renter share — captures the proportion of homeowners in a ZIP code."),
                                                html.Span("ChargersPer1000EV", className="column-chip chip-teal", title="Number of chargers per 1,000 EV registrations — measures infrastructure relative to EV demand."),
                                                html.Span("PortsPer10kPeople", className="column-chip chip-blue", title="Charging ports per 10,000 residents — normalizes infrastructure availability by population."),
                                            ],
                                            className="chip-group-row",
                                            style={"marginTop": "8px"},
                                        ),
                                    ],
                                    className="qc-card",
                                ),
                            ],
                            className="qc-grid",
                        ),
                    ],
                ),

                # 4. VISUALIZATIONS
                html.Div(
                    className="card",
                    children=[
                        html.H2("4. Visualization Analysis", className="section-title"),
                        html.P(
                            "The visual analysis focuses on the main patterns that shaped the rest of the project: how EV adoption varies across ZIP codes, "
                            "how strongly it differs by income, how it changes under environmental burden, and whether charging access is distributed evenly.",
                            className="section-body",
                            style={"marginBottom": "28px"},
                        ),

                        # 4.1 single wide
                        viz_wide(
                            "4.1 Distribution of EV Adoption Across ZIP Codes",
                            "ev_distribution.png",
                            "Figure 1. Distribution of EV adoption across California ZIP codes.",
                            "EV adoption is highly right-skewed — most communities show low adoption rates with a smaller group reaching much higher levels. This uneven distribution motivates deeper analysis into which structural factors explain these disparities.",
                        ),

                        html.Hr(className="section-divider"),

                        # 4.2 paired
                        html.H3("4.2 Income and EV Adoption", className="subsection-title"),
                        html.P("Income was one of the clearest early signals — the next two plots examine how adoption changes across income-based community groups.", style={"marginBottom": "16px", "color": "var(--muted)", "fontSize": "14px"}),
                        html.Div(
                            className="two-column-grid",
                            children=[
                                html.Div(className="half-card", children=[
                                    viz_paired(
                                        "Mean EV Adoption by Income Quintile",
                                        "ev_incomequintile.png",
                                        "Figure 2. Average EV adoption rate across household income quintiles.",
                                        "Average EV adoption rises steadily across income quintiles, showing a strong positive relationship between household income and EV uptake.",
                                    ),
                                ]),
                                html.Div(className="half-card", children=[
                                    viz_paired(
                                        "EV Adoption Distribution by Income Quintile",
                                        "ev_incomeboxplot.png",
                                        "Figure 3. Distribution of EV adoption within each income quintile.",
                                        "Higher-income groups have consistently greater EV adoption, while lower-income communities remain concentrated at much lower levels.",
                                    ),
                                ]),
                            ],
                        ),

                        html.Hr(className="section-divider"),

                        # 4.3 paired
                        html.H3("4.3 Environmental Burden and EV Adoption", className="subsection-title"),
                        html.P("Do environmentally burdened communities also miss out on EV adoption benefits?", style={"marginBottom": "16px", "color": "var(--muted)", "fontSize": "14px"}),
                        html.Div(
                            className="two-column-grid",
                            children=[
                                html.Div(className="half-card", children=[
                                    viz_paired(
                                        "CalEnviroScreen Burden vs. EV Adoption",
                                        "ev_burden_scatter.png",
                                        "Figure 4. CalEnviroScreen burden score vs. EV adoption.",
                                        "A weak but consistent negative relationship — ZIP codes with higher combined environmental stress tend to report lower EV adoption.",
                                    ),
                                ]),
                                html.Div(className="half-card", children=[
                                    viz_paired(
                                        "EV Adoption by Environmental Burden Quartile",
                                        "ev_calenviro_boxplot.png",
                                        "Figure 5. EV adoption across CalEnviroScreen burden quartiles.",
                                        "ZIP codes with the greatest environmental burden have lower EV adoption distributions overall — EV transition benefits are not reaching all communities equally.",
                                    ),
                                ]),
                            ],
                        ),

                        html.Hr(className="section-divider"),

                        # 4.4 single wide
                        viz_wide(
                            "4.4 Charging Infrastructure Access by Income",
                            "ev_chargers1000_quintile.png",
                            "Figure 6. Charging availability relative to EV registrations across income quintiles.",
                            "Charging access is uneven and highly variable across income groups with no clear equalizing pattern. In some cases, higher-income areas show stronger availability, but the relationship is not consistent — raising questions about whether infrastructure follows demand or reinforces existing disparities.",
                        ),

                        html.Hr(className="section-divider"),

                        # 4.5 single wide
                        viz_wide(
                            "4.5 Correlation Between EV Adoption and Key Variables",
                            "ev_corr.png",
                            "Figure 7. Correlation heatmap for EV adoption and key explanatory variables.",
                            "EV adoption is most strongly correlated with education (0.87), home values (0.83), and income (0.81). It is negatively correlated with environmental burden (CES: -0.49) and poverty (-0.41). Infrastructure variables show moderate positive relationships (Total Ports: 0.33), indicating that access supports adoption but is not the primary driver of disparities.",
                        ),
                    ],
                ),

                # 5. INSIGHTS
                html.Div(
                    className="card",
                    children=[
                        html.H2("5. Preliminary Insights", className="section-title"),
                        html.P(
                            "The exploratory analysis reveals several early patterns that guide the next stage of modeling.",
                            className="section-body",
                            style={"marginBottom": "18px"},
                        ),
                        html.Div(
                            [
                                insight_card(1, "EV adoption is most strongly associated with socioeconomic advantage. Education, home values, and median household income show the strongest positive relationships."),
                                insight_card(2, "Communities with greater structural disadvantage have lower EV adoption. Poverty and higher CalEnviroScreen burden are both negatively associated."),
                                insight_card(3, "Charging infrastructure is positively associated with adoption, but this is partly expected — infrastructure tends to follow demand, raising questions about whether it also reinforces disparities."),
                                insight_card(4, "EV adoption is not evenly distributed across California and is shaped by broader differences in wealth, education, and community burden."),
                            ],
                            className="ins-grid",
                        ),
                        html.Div(
                            "Based on these findings, the next stage will test whether income, education, environmental burden, and charging infrastructure remain important predictors in regression models.",
                            className="insight-note",
                            style={"marginTop": "18px"},
                        ),
                    ],
                ),
            ],
        )
    ]
)
