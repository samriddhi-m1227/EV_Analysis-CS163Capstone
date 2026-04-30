import dash
from dash import html

dash.register_page(__name__, path="/data")


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


def pipeline_step(number, title, body_children):
    return html.Div(
        [
            html.Div(
                [
                    html.Div(str(number), className="pipe-number"),
                    html.Div(className="pipe-line"),
                ],
                className="pipe-left",
            ),
            html.Div(
                [
                    html.Span(title, className="pipe-title"),
                    html.Div(body_children, className="pipe-body"),
                ],
                className="pipe-right",
            ),
        ],
        className="pipe-step",
    )


def check_item(text):
    return html.Div(
        [html.Span("✓", className="check-icon"), html.Span(text, className="check-text")],
        className="check-item",
    )


def src_card(name, description, tag):
    return html.Div(
        [
            html.Div(
                [html.Span(name, className="src-name"), html.Span(tag, className="src-tag")],
                className="src-card-header",
            ),
            html.Span(description, className="src-desc"),
        ],
        className="src-card-data",
    )


layout = html.Div(
    [
        html.Div(
            className="page-container",
            children=[

                # BANNER
                page_banner(
                    "Data",
                    "How we built the unified California EV dataset from four public sources",
                    [
                        banner_chip("4", "Data Sources"),
                        banner_chip("1,800+", "ZIP Codes"),
                        banner_chip("34", "Features"),
                    ],
                ),

                # 1. OVERVIEW
                html.Div(
                    className="card",
                    children=[
                        html.H2("1. Data Overview", className="section-title"),
                        html.Div(className="section-body", children=[
                            html.P(
                                "This section documents how the final analytical dataset was built before exploratory analysis began. "
                                "The goal was a unified ZIP-code-level dataset for California combining EV adoption, "
                                "socioeconomic conditions, housing structure, environmental burden, and charging infrastructure."
                            ),
                            html.P(
                                "Because the project integrates multiple public sources reported at different geographic levels, "
                                "data acquisition, cleaning, alignment, and feature construction were a major part of the workflow."
                            ),
                        ]),
                    ],
                ),

                # 2. DATA SOURCES
                html.Div(
                    className="card",
                    children=[
                        html.H2("2. Data Sources", className="section-title"),
                        html.Div(
                            [
                                src_card("CalMatters EV Dataset", "ZIP-level EV registration counts, demographics, and Zillow home value indicators.", "Primary"),
                                src_card("American Community Survey (ACS)", "Structural socioeconomic and housing variables retrieved via the Census API.", "Census"),
                                src_card("CalEnviroScreen 4.0", "Tract-level environmental burden indicators aggregated to ZIP level.", "Environmental"),
                                src_card("NREL Alt Fuel Stations API", "Public EV charging station and port availability across California.", "Infrastructure"),
                            ],
                            className="src-grid-data",
                        ),
                    ],
                ),

                # 3. PIPELINE
                html.Div(
                    className="card",
                    children=[
                        html.H2("3. Curation Pipeline", className="section-title"),
                        html.P(
                            "Each source was acquired, cleaned, and joined into a single ZIP-level table.",
                            className="section-body",
                            style={"marginBottom": "24px"},
                        ),
                        html.Div(
                            [
                                pipeline_step(1, "CalMatters EV Data — Base Layer", [
                                    html.P("The CalMatters dataset served as the primary foundation. It already included ZIP-level EV registration counts and several demographic and housing-related variables, making it the natural starting point for the integration pipeline."),
                                ]),
                                pipeline_step(2, "ACS Feature Construction", [
                                    html.P("Additional variables were retrieved from the American Community Survey to better capture structural socioeconomic and housing conditions:"),
                                    html.Div(
                                        [
                                            html.Span("Gini Index", className="pipe-chip"),
                                            html.Span("Housing Tenure", className="pipe-chip"),
                                            html.Span("Housing Structure", className="pipe-chip"),
                                            html.Span("Vehicle Availability", className="pipe-chip"),
                                            html.Span("Poverty Status", className="pipe-chip"),
                                        ],
                                        className="pipe-chips",
                                    ),
                                    html.P("Values were retrieved at the ZCTA level, then transformed into normalized ZIP-level shares such as renter share, multi-unit share, and poverty share."),
                                ]),
                                pipeline_step(3, "CalEnviroScreen Aggregation", [
                                    html.P("CalEnviroScreen indicators were originally at the census tract level. Tract-level data were aggregated to ZIP level using population-weighted averages to preserve representativeness."),
                                    html.Div(
                                        [
                                            html.Span("CES 4.0 Score", className="pipe-chip"),
                                            html.Span("Pollution Burden", className="pipe-chip"),
                                            html.Span("Traffic Exposure", className="pipe-chip"),
                                            html.Span("County", className="pipe-chip"),
                                        ],
                                        className="pipe-chips",
                                    ),
                                ]),
                                pipeline_step(4, "NREL Charging Infrastructure", [
                                    html.P("Charging data were pulled from the NREL API and filtered to public, operational stations in California open on or before end of 2021."),
                                    html.Div(
                                        [
                                            html.Span("Num Stations", className="pipe-chip"),
                                            html.Span("Total Ports", className="pipe-chip"),
                                            html.Span("L2 Ports", className="pipe-chip"),
                                            html.Span("DC Fast Ports", className="pipe-chip"),
                                        ],
                                        className="pipe-chips",
                                    ),
                                ]),
                            ],
                            className="pipeline",
                        ),
                    ],
                ),

                # 4. CLEANING
                html.Div(
                    className="card",
                    children=[
                        html.H2("4. Cleaning & Integration Decisions", className="section-title"),
                        html.Div(
                            [
                                check_item("ZIP code standardized across all datasets as the common merge key."),
                                check_item("Margin-of-error ACS columns removed before feature construction."),
                                check_item("Detailed ACS counts converted into normalized interpretable shares."),
                                check_item("Invalid values coerced or set to missing where necessary."),
                                check_item("Infrastructure records with no matching chargers filled with zeros after merging."),
                                check_item("Final table preserves one row per California ZIP code — no duplicates."),
                                check_item("Most variables have low missingness; environmental metrics slightly higher but within acceptable range."),
                            ],
                            className="check-list",
                        ),
                        html.Div(
                            "A key design choice was aligning all sources to the same geographic unit before analysis, rather than mixing tract-level and ZIP-level observations directly.",
                            className="insight-note",
                            style={"marginTop": "18px"},
                        ),
                    ],
                ),

                # 5. FINAL DATASET
                html.Div(
                    className="card",
                    children=[
                        html.H2("5. Final Integrated Dataset", className="section-title"),
                        html.P(
                            "The final dataset contains EV adoption, vehicle composition, demographics, income, education, housing structure, inequality, "
                            "environmental burden, and charging infrastructure in one unified ZIP-level table. "
                            "This clean merged dataset is the starting point for all EDA and modeling.",
                            className="section-body",
                        ),
                    ],
                ),

            ],
        )
    ]
)
