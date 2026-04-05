import dash
from dash import html

dash.register_page(__name__, path="/data")


def section_card(title, children):
    return html.Div(
        [
            html.H2(title, className="section-title"),
            html.Div(children, className="section-body"),
        ],
        className="card",
    )


layout = html.Div(
    [
        html.Div(
            className="page-container",
            children=[
                html.H1("Data", className="page-header"),

                section_card(
                    "1. Data Overview",
                    [
                        html.P(
                            "This section documents how the final analytical dataset was built before exploratory analysis began. "
                            "The goal was to create a unified ZIP-code-level dataset for California that combines EV adoption, "
                            "socioeconomic conditions, housing structure, environmental burden, and charging infrastructure."
                        ),
                        html.P(
                            "Because the project depends on integrating multiple public sources reported at different levels of detail, "
                            "data acquisition, cleaning, alignment, and feature construction were a major part of the workflow."
                        ),
                    ],
                ),

                section_card(
                    "2. Data Sources",
                    [
                        html.Ul(
                            [
                                html.Li("CalMatters EV dataset: base ZIP-level dataset containing EV registration, demographic, and Zillow home value information."),
                                html.Li("American Community Survey (ACS): additional structural variables retrieved through the Census API."),
                                html.Li("CalEnviroScreen 4.0: tract-level environmental burden indicators later aggregated to ZIP level."),
                                html.Li("NREL Alternative Fuel Stations API: public EV charging infrastructure across California."),
                            ]
                        ),
                    ],
                ),

                # --- Combine sections 3-6 into a single pipeline section ---
                section_card(
                    "3. Curation Pipeline",
                    [
                        html.Div([
                            html.H4("Base Dataset: CalMatters EV Data", style={"marginBottom": "8px"}),
                            html.P(
                                "The CalMatters dataset served as the main foundation for the project. It already included ZIP-level EV registration counts and several demographic and housing-related variables, making it the natural starting point for the integration pipeline."
                            ),
                            html.P(
                                "This dataset contributed the project’s core EV adoption measures, vehicle counts, and several important community descriptors."
                            ),
                        ]),
                        html.Div(
                            "↓",
                            style={"fontSize": "2.5rem", "textAlign": "center", "color": "#2563eb", "margin": "-8px 0 8px 0"},
                        ),
                        html.Div([
                            html.H4("ACS Data Retrieval and Feature Construction", style={"marginBottom": "8px"}),
                            html.P(
                                "Additional variables were retrieved from the American Community Survey to better capture structural socioeconomic and housing conditions that may influence EV adoption and charging accessibility."
                            ),
                            html.Ul(
                                [
                                    html.Li("Income inequality (Gini index)"),
                                    html.Li("Housing tenure (rent vs. own)"),
                                    html.Li("Housing structure (single-family vs. multi-unit)"),
                                    html.Li("Vehicle availability"),
                                    html.Li("Poverty status"),
                                ]
                            ),
                            html.P(
                                "These values were retrieved programmatically through the Census API at the ZIP Code Tabulation Area level, saved locally after execution, and then transformed into normalized ZIP-level shares such as renter share, multi-unit share, zero-vehicle share, and poverty share."
                            ),
                        ]),
                        html.Div(
                            "↓",
                            style={"fontSize": "2.5rem", "textAlign": "center", "color": "#2563eb", "margin": "-8px 0 8px 0"},
                        ),
                        html.Div([
                            html.H4("CalEnviroScreen Aggregation", style={"marginBottom": "8px"}),
                            html.P(
                                "CalEnviroScreen indicators were originally reported at the census tract level, which could not be merged directly with the ZIP-level EV dataset."
                            ),
                            html.P(
                                "To align the geographies correctly, tract-level environmental indicators were aggregated to ZIP level using population-weighted averages. This preserved representativeness while avoiding duplicated ZIP rows."
                            ),
                            html.Ul(
                                [
                                    html.Li("CES 4.0 Score"),
                                    html.Li("Pollution Burden Score"),
                                    html.Li("Traffic exposure"),
                                    html.Li("County"),
                                ]
                            ),
                        ]),
                        html.Div(
                            "↓",
                            style={"fontSize": "2.5rem", "textAlign": "center", "color": "#2563eb", "margin": "-8px 0 8px 0"},
                        ),
                        html.Div([
                            html.H4("NREL Charging Infrastructure Data", style={"marginBottom": "8px"}),
                            html.P(
                                "Charging infrastructure data were pulled from the NREL Alternative Fuel Stations API and filtered to include only public, operational electric charging stations in California."
                            ),
                            html.P(
                                "To align infrastructure with the EV adoption time frame, stations were restricted to those open on or before the end of 2021."
                            ),
                            html.Ul(
                                [
                                    html.Li("Number of unique stations by ZIP"),
                                    html.Li("Total charging ports"),
                                    html.Li("Level 2 ports"),
                                    html.Li("DC Fast ports"),
                                ]
                            ),
                        ]),
                    ]
                ),

                section_card(
                    "4. Data Cleaning and Integration Decisions",
                    [
                        html.Ul(
                            [
                                html.Li("ZIP code was standardized across all datasets and used as the common merge key."),
                                html.Li("Margin-of-error ACS columns were removed before feature construction."),
                                html.Li("Detailed ACS counts were converted into interpretable normalized shares."),
                                html.Li("Invalid values were coerced or set to missing where necessary."),
                                html.Li("Infrastructure records with no matching public chargers were filled with zeros after merging."),
                                html.Li("The final table preserves one row per California ZIP code."),
                            ]
                        ),
                        html.Div(
                            "A key design choice in the pipeline was aligning all sources to the same geographic unit before analysis, rather than mixing tract-level and ZIP-level observations directly.",
                            className="insight-note",
                        ),
                    ],
                ),

                section_card(
                    "5. Final Integrated Dataset",
                    [
                        html.P(
                            "The final dataset contains EV adoption, vehicle composition, demographics, income, education, housing structure, inequality, "
                            "environmental burden, and charging infrastructure in one unified ZIP-level table."
                        ),
                        html.P(
                            "This clean merged dataset serves as the starting point for the EDA section and all later analysis."
                        ),
                    ],
                ),
            ],
        )
    ]
)