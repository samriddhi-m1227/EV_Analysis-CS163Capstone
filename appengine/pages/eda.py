import os
import pandas as pd
import dash
from dash import html, dash_table

dash.register_page(__name__, path="/eda")

# --- Load dataset ---
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # appengine/
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
    "Gini": "Income inequality index from 0 to 1. Lower values indicate more equal income distribution, while higher values indicate greater inequality.",
    "RenterShare": "Share of households that rent their homes.",
    "SingleFamilyShare": "Share of housing units that are single-family homes.",
    "MultiUnitShare": "Share of housing units that are multi-unit buildings.",
    "ZeroVehicleShare": "Share of households without access to a vehicle.",
    "PovertyShare": "Share of residents living below the poverty line. Higher values indicate greater economic disadvantage.",

    "CES_Score_ZIP": "Overall CalEnviroScreen score representing environmental and socioeconomic vulnerability. Higher scores indicate worse burden.",
    "PollutionBurden_ZIP": "Pollution exposure indicator. Higher values indicate worse pollution burden.",
    "Traffic_ZIP": "Traffic-related pollution indicator. Higher values indicate greater exposure to traffic burden.",

    "Num_Stations": "Number of EV charging stations in the ZIP code.",
    "Total_Ports": "Total number of EV charging ports across all stations in the ZIP code.",
    "L2_Ports": "Number of Level 2 charging ports.",
    "DC_Fast_Ports": "Number of DC fast charging ports.",
}


def section_card(title, children):
    return html.Div(
        [
            html.H2(title, className="section-title"),
            html.Div(children, className="section-body"),
        ],
        className="card",
    )


def dataset_preview_table(dataframe, n_rows=5):
    preview_df = dataframe.head(n_rows).copy()
    columns = [{"name": col, "id": col} for col in preview_df.columns]

    return dash_table.DataTable(
        columns=columns,
        data=preview_df.to_dict("records"),
        page_size=n_rows,
        sort_action="native",
        style_table={
            "overflowX": "auto",
            "border": "1px solid var(--border)",
            "borderRadius": "12px",
        },
        style_cell={
            "textAlign": "left",
            "padding": "10px",
            "minWidth": "120px",
            "maxWidth": "220px",
            "whiteSpace": "normal",
            "backgroundColor": "var(--surface)",
            "color": "var(--text)",
            "border": "1px solid var(--border)",
            "fontFamily": "Inter, sans-serif",
            "fontSize": "13px",
        },
        style_header={
            "backgroundColor": "var(--surface-2)",
            "fontWeight": "600",
            "color": "var(--heading)",
        },
    )


def column_chip(name):
    return html.Span(
        name,
        className="column-chip",
        title=COLUMN_DEFINITIONS.get(name, "No description available."),
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
                html.H1("Exploratory Data Analysis", className="page-header"),

                section_card(
                    "1. EDA Overview",
                    [
                        html.P(
                            "Using the final integrated ZIP-level dataset, this section explores the overall distribution of EV adoption and the early relationships between EV adoption, socioeconomic conditions, environmental burden, housing structure, and charging infrastructure."
                        ),
                        html.P(
                            "Below is a preview of the final merged dataset used for all analysis."
                        ),
                        dataset_preview_table(df),
                        html.Div(
                            "The table above shows a small sample of the merged dataset and can be scrolled horizontally to inspect the full structure.",
                            className="insight-note",
                        ),
                    ],
                ),

                html.Div(
                    className="card",
                    children=[
                        html.H2("2. Key Variables Used in EDA", className="section-title"),
                        html.Div(
                            className="two-column-grid",
                            children=[
                                html.Div(
                                    className="half-card variable-card",
                                    children=[
                                        html.H3("Full Dataset Columns", className="subsection-title"),
                                        html.P(
                                            "The final integrated dataset contains variables related to vehicle composition, EV adoption, demographics, housing, inequality, environmental burden, and charging infrastructure."
                                        ),
                                        html.P(
                                            "Hover over any variable below to view its definition.",
                                            className="caption-text",
                                        ),
                                        html.Div(
                                            className="column-chip-container",
                                            children=[
                                                column_chip("ZIP"),
                                                column_chip("Diesel"),
                                                column_chip("Electric"),
                                                column_chip("Flex_Fuel"),
                                                column_chip("Gasoline"),
                                                column_chip("Gasoline_Hybrid"),
                                                column_chip("Hydrogen"),
                                                column_chip("Natural_Gas"),
                                                column_chip("PHEV"),
                                                column_chip("Propane"),
                                                column_chip("Total_Cars"),
                                                column_chip("Total_EV"),
                                                column_chip("EV_perc"),
                                                column_chip("Median_Household_Income"),
                                                column_chip("Latino_perc"),
                                                column_chip("White_perc"),
                                                column_chip("Asian_perc"),
                                                column_chip("Black_perc"),
                                                column_chip("BachOrHigher_perc"),
                                                column_chip("Total_Population"),
                                                column_chip("Zillow_Home_Value_Index"),
                                                column_chip("Gini"),
                                                column_chip("RenterShare"),
                                                column_chip("SingleFamilyShare"),
                                                column_chip("MultiUnitShare"),
                                                column_chip("ZeroVehicleShare"),
                                                column_chip("PovertyShare"),
                                                column_chip("CES_Score_ZIP"),
                                                column_chip("PollutionBurden_ZIP"),
                                                column_chip("Traffic_ZIP"),
                                                column_chip("County"),
                                                column_chip("Num_Stations"),
                                                column_chip("Total_Ports"),
                                                column_chip("L2_Ports"),
                                                column_chip("DC_Fast_Ports"),
                                            ],
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="half-card variable-card",
                                    children=[
                                        html.H3("Priority Variables for Interpretation", className="subsection-title"),
                                        html.Div(
                                            "EV_perc is the primary outcome variable in this project and serves as the main measure of EV adoption across California ZIP codes.",
                                            className="insight-note",
                                        ),
                                        html.Ul(
                                            className="priority-variable-list",
                                            children=[
                                                html.Li(
                                                    [
                                                        html.Strong("Target / Outcome: "),
                                                        "EV_perc captures the share of registered vehicles in a ZIP code that are electric and is the central variable used throughout EDA and later modeling.",
                                                    ]
                                                ),
                                                html.Li(
                                                    [
                                                        html.Strong("Socioeconomic context: "),
                                                        "Median_Household_Income and BachOrHigher_perc help represent economic capacity and educational advantage.",
                                                    ]
                                                ),
                                                html.Li(
                                                    [
                                                        html.Strong("Housing context: "),
                                                        "Zillow_Home_Value_Index, RenterShare, SingleFamilyShare, and MultiUnitShare help describe affordability, tenure, and whether home charging may be more or less feasible.",
                                                    ]
                                                ),
                                                html.Li(
                                                    [
                                                        html.Strong("Structural vulnerability: "),
                                                        "Gini, PovertyShare, and ZeroVehicleShare capture inequality and socioeconomic disadvantage.",
                                                    ]
                                                ),
                                                html.Li(
                                                    [
                                                        html.Strong("Environmental burden: "),
                                                        "CES_Score_ZIP, PollutionBurden_ZIP, and Traffic_ZIP measure exposure to environmental disadvantage and pollution-related burden.",
                                                    ]
                                                ),
                                                html.Li(
                                                    [
                                                        html.Strong("Charging infrastructure: "),
                                                        "Num_Stations, Total_Ports, L2_Ports, and DC_Fast_Ports capture the availability and type of public EV charging access.",
                                                    ]
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),

                section_card(
                    "3. Data Overview & Quality",
                    [
                        html.P(
                            "The dataset captures ZIP-level differences in EV adoption across California, combining socioeconomic, environmental, and infrastructure factors."
                        ),

                        html.Div(
                            [
                                html.B("Feature Categories:"),
                                html.Ul(
                                    [
                                        html.Li("Income & Wealth: income, home values, inequality, poverty"),
                                        html.Li("Education: bachelor's degree attainment"),
                                        html.Li("Demographics: race and ethnicity composition"),
                                        html.Li("Housing: renter share, housing type, vehicle access"),
                                        html.Li("Environmental Burden: CES score, pollution, traffic"),
                                        html.Li("Infrastructure: charging stations and ports"),
                                    ]
                                ),
                            ],
                            style={"marginBottom": "10px"},
                        ),

                        html.Div(
                            [
                                html.B("Data Quality Checks:"),
                                html.Ul(
                                    [
                                        html.Li("Most variables have low missingness, though environmental metrics have moderately higher missing values."),
                                        html.Li("No duplicate ZIP-level records were identified after merging."),
                                        html.Li("Share-based variables were checked for valid ranges."),
                                        html.Li("EV adoption values were cross-checked against registered EV counts and total vehicles."),
                                    ]
                                ),
                            ],
                            style={"marginBottom": "10px"},
                        ),

                        html.Div(
                            [
                                html.B("Derived Features:"),
                                html.Ul(
                                    [
                                        html.Li("HomeownerShare computed from renter share"),
                                        html.Li("ChargersPer1000EV to measure infrastructure relative to EV demand"),
                                        html.Li("PortsPer10kPeople to normalize charging infrastructure by population"),
                                    ]
                                ),
                            ],
                            style={"marginBottom": "10px"},
                        ),

                        html.Div(
                            [
                                html.B("Key Takeaways:"),
                                html.Ul(
                                    [
                                        html.Li("Median EV adoption remains low across most ZIP codes."),
                                        html.Li("Income varies widely across California ZIP codes, indicating strong inequality."),
                                        html.Li("A substantial share of ZIP codes have no charging stations after merging."),
                                        html.Li("Infrastructure and environmental burden vary significantly across regions."),
                                    ]
                                ),
                            ]
                        ),
                    ],
                ),

                section_card(
                    "4. Visualization Analysis",
                    [
                        html.P(
                            "The visual analysis below focuses on the main patterns that shaped the rest of the project: how EV adoption varies across ZIP codes, how strongly it differs by income, how it changes under environmental burden, and whether charging access is distributed evenly."
                        ),

                        viz_block(
                            "4.1 Distribution of EV Adoption Across ZIP Codes",
                            "ev_distribution.png",
                            "Figure 1. Distribution of EV adoption across California ZIP codes.",
                            "EV adoption is highly right-skewed across ZIP codes, with most communities showing relatively low adoption rates and a smaller group reaching much higher levels. This indicates that EV adoption is not evenly shared across California and motivates deeper analysis into which structural factors help explain these disparities."
                        ),

                        html.Div(
                            className="card subsection-card",
                            children=[
                                html.H2("4.2 Income and EV Adoption", className="section-title"),
                                html.P(
                                    "Income was one of the clearest early signals in the data, so the next two plots examine how EV adoption changes across income-based community groups."
                                ),
                                html.Div(
                                    className="two-column-grid",
                                    children=[
                                        html.Div(
                                            className="half-card",
                                            children=[
                                                viz_block(
                                                    "Mean EV Adoption by Income Quintile",
                                                    "ev_incomequintile.png",
                                                    "Figure 2. Average EV adoption rate across household income quintiles.",
                                                    "Average EV adoption rises steadily across income quintiles, showing a strong positive relationship between household income and EV uptake. This suggests that higher-income communities are better positioned to adopt EVs, likely due to differences in affordability, home charging access, and overall resource availability."
                                                )
                                            ],
                                        ),
                                        html.Div(
                                            className="half-card",
                                            children=[
                                                viz_block(
                                                    "EV Adoption Distribution by Income Quintile",
                                                    "ev_incomeboxplot.png",
                                                    "Figure 3. Distribution of EV adoption within each income quintile.",
                                                    "The box plot shows that the income relationship is not only visible in averages but also throughout the full distribution. Higher-income groups tend to have consistently greater EV adoption, while lower-income communities remain concentrated at much lower levels."
                                                )
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),

                        html.Div(
                            className="card subsection-card",
                            children=[
                                html.H2("4.3 Environmental Burden and EV Adoption", className="section-title"),
                                html.P(
                                    "To complement the income story, the next visuals examine whether environmentally burdened communities are also less likely to benefit from EV adoption."
                                ),
                                html.Div(
                                    className="two-column-grid",
                                    children=[
                                        html.Div(
                                            className="half-card",
                                            children=[
                                                viz_block(
                                                    "CalEnviroScreen Burden vs. EV Adoption",
                                                    "ev_burden_scatter.png",
                                                    "Figure 4. Relationship between CalEnviroScreen burden score and EV adoption.",
                                                    "The scatterplot suggests a weak but consistent negative relationship between environmental burden and EV adoption. ZIP codes facing higher combined environmental and socioeconomic stress tend to report lower EV adoption, suggesting that communities already exposed to greater disadvantage are also less likely to access clean transportation benefits."
                                                )
                                            ],
                                        ),
                                        html.Div(
                                            className="half-card",
                                            children=[
                                                viz_block(
                                                    "EV Adoption by Environmental Burden Quartile",
                                                    "ev_calenviro_boxplot.png",
                                                    "Figure 5. EV adoption across CalEnviroScreen burden quartiles.",
                                                    "Grouping communities into burden quartiles makes the disparity clearer: ZIP codes with the greatest environmental burden tend to have lower EV adoption distributions overall. This reinforces the idea that EV transition benefits are not reaching all communities equally."
                                                )
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),

                        html.Div(
                            className="card subsection-card",
                            children=[
                                html.H2("4.4 Charging Infrastructure Access", className="section-title"),
                                html.P(
                                    "Charging access is an important part of EV feasibility, so infrastructure was examined alongside socioeconomic differences."
                                ),
                                viz_block(
                                    "Chargers per 1,000 EV Registrations by Income Quintile",
                                    "ev_chargers1000_quintile.png",
                                    "Figure 6. Charging availability relative to EV registrations across income quintiles.",
                                    "Charging access appears uneven and highly variable across income groups, with no clear equalizing pattern. In some cases, higher-income areas show stronger availability, but the relationship is not consistent."
                                ),
                            ],
                        ),

                        html.Div(
                            className="card subsection-card",
                            children=[
                                html.H2("4.5 Correlation Overview", className="section-title"),
                                html.P(
                                    "The final visualization summarizes how EV adoption moves with several major variables at once."
                                ),
                                viz_block(
                                    "Correlation Between EV Adoption and Key Variables",
                                    "ev_corr.png",
                                    "Figure 7. Correlation heatmap for EV adoption and key explanatory variables.",
                                    " The correlation results highlight several clear drivers of EV adoption. EV adoption is strongly positively correlated with education (0.87), home values (0.83), and median household income (0.81), indicating that higher socioeconomic status is closely associated with greater EV adoption across ZIP codes. In contrast, EV adoption is moderately negatively correlated with environmental burden (CES score: -0.49) and poverty (-0.41), suggesting that more disadvantaged communities are less likely to adopt EVs. Charging infrastructure variables such as total ports (0.33) and number of stations (0.31) show moderate positive relationships with EV adoption, indicating that infrastructure availability supports adoption but is not the primary driver of disparities. Other variables, such as inequality (Gini: 0.29), show weaker relationships, while measures like pollution burden (-0.11) and chargers per 1,000 EVs (-0.08) have relatively small correlations. Overall, these results suggest that EV adoption is most strongly shaped by socioeconomic advantage, with infrastructure playing a secondary but supportive role."
                                ),
                                
                            ],
                        ),
                    ],
                ),

                                section_card(
                    "5. Preliminary Insights",
                    [
                        html.P(
                            "The exploratory analysis reveals several early patterns that guide the next stage of modeling and interpretation."
                        ),
                        html.Ul(
                            [
                                html.Li(
                                    "EV adoption is most strongly associated with socioeconomic advantage. Education, home values, and median household income show the strongest positive relationships with EV adoption."
                                ),
                                html.Li(
                                    "Communities with greater structural disadvantage tend to have lower EV adoption. Poverty and higher CalEnviroScreen burden are both negatively associated with EV adoption across ZIP codes."
                                ),
                                html.Li(
                                    "While charging infrastructure is positively associated with EV adoption, this relationship is partly expected, as infrastructure is often built in response to existing demand. This raises a deeper question of whether structural socioeconomic and environmental factors influence where infrastructure is deployed in the first place."
                                ),
                                html.Li(
                                    "The overall pattern suggests that EV adoption is not distributed evenly across California and is shaped by broader differences in wealth, education, and community burden."
                                ),
                            ],
                            className="insight-bullet-list",
                        ),
                        html.Div(
                            "Based on these findings, the next stage of analysis will test whether income, education, environmental burden, and charging infrastructure remain important predictors of EV adoption in the regression models.",
                            className="insight-note",
                        ),
                    ],
                ),
            ],
        )
    ]
)