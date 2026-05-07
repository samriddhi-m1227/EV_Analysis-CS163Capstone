import dash
from dash import html

dash.register_page(__name__, path="/methods")


def section_card(number, title, children):
    return html.Div(
        className="card",
        children=[
            html.Div(
                className="an-sec-header",
                children=[
                    html.Span(str(number), className="an-sec-num"),
                    html.Div(html.H2(title, className="an-sec-title"), className="an-sec-text"),
                ],
            ),
            html.Div(children, style={"marginTop": "18px"}),
        ],
    )


def method_block(term, paras):
    return html.Div(
        style={"marginBottom": "22px"},
        children=[
            html.H4(term, style={"margin": "0 0 8px 0", "color": "var(--accent)", "fontSize": "14px", "fontWeight": "600"}),
            *[html.P(p, style={"margin": "0 0 8px 0", "fontSize": "13.5px", "lineHeight": "1.72", "color": "var(--text)"}) for p in paras],
        ],
    )


def ref_item(number, citation, href=None):
    return html.Li(
        className="fd-ref-item",
        children=[
            html.Span(f"[{number}]", className="fd-ref-num"),
            html.A(citation, href=href, target="_blank", className="fd-ref-link") if href
            else html.Span(citation, className="fd-ref-text"),
        ],
    )


layout = html.Div([
    html.Div(
        className="page-container",
        children=[

            html.Div(
                className="page-banner",
                children=[
                    html.Div(className="hero-dot-grid"),
                    html.H1("Analytical Methods", className="page-banner-title"),
                    html.P(
                        "Technical overview of the statistical and machine learning methods used in this project, including motivation, assumptions, and references",
                        className="page-banner-sub",
                    ),
                ],
            ),

            # OVERVIEW
            html.Div(
                className="card",
                children=[
                    html.H2("Overview", className="section-title"),
                    html.P(
                        "This project uses a layered analytical approach: beginning with exploratory data analysis to understand distributions and correlations, "
                        "moving to regression modeling to quantify structural associations, and extending to machine learning to build predictive classifiers and identify feature importance. "
                        "All analysis is conducted at the ZIP code level across 1,800+ California ZIP codes. Because the data are cross-sectional and observational, "
                        "all findings are interpreted as associations rather than causal effects.",
                        className="section-body",
                    ),
                    html.P(
                        "The target variable throughout is EV_perc : the share of registered vehicles in a ZIP code that are fully electric, "
                        "sourced from the California DMV via the CalMatters dataset.",
                        className="section-body",
                    ),
                ],
            ),

            # 1. DATA INTEGRATION
            section_card(1, "Data Integration & Feature Engineering", [
                method_block("Geographic Aggregation", [
                    "The four source datasets operate at different geographic levels. CalMatters EV data and NREL charging stations are at the ZIP code level. "
                    "ACS data are at the ZCTA (ZIP Code Tabulation Area) level, which closely but not perfectly overlaps with ZIP codes. "
                    "CalEnviroScreen 4.0 operates at the census tract level, which is finer-grained than ZIP codes.",
                    "To bring CalEnviroScreen to the ZIP level, tract-level scores were aggregated using population-weighted averages: "
                    "each tract's score is weighted by the fraction of its population that falls within the target ZIP code. "
                    "This preserves the relative burden of high-population tracts but introduces noise where tract and ZIP boundaries do not align well.",
                    "NREL charging station point locations were assigned to ZIP codes using the station's reported ZIP code field, then summed to produce total port counts per ZIP. "
                    "Unmatched ZIP codes were filled with zero after the merge.",
                ]),
                method_block("Feature Engineering", [
                    "Raw ACS count variables were converted to normalized shares to ensure comparability across ZIP codes of different population sizes: "
                    "RenterShare (renters / occupied units), MultiUnitShare (multi-unit structures / total units), PovertyShare (below poverty / total population), "
                    "and ZeroVehicleShare (zero-vehicle households / total households).",
                    "Infrastructure features were derived post-merge: PortsPer10kPeople (total ports / population * 10,000) captures per-capita access. "
                    "ChargersPer1000EV (total ports / EV count * 1,000) measures infrastructure relative to current EV demand.",
                    "These derived features were preferred over raw totals in regression models to control for population size effects and avoid spurious correlations driven by ZIP code size.",
                ]),
            ]),

            # 2. EXPLORATORY ANALYSIS
            section_card(2, "Exploratory Data Analysis", [
                method_block("Distributional Analysis", [
                    "EV adoption rates are right-skewed across ZIP codes — most ZIPs have low adoption with a long tail of high-adoption outliers. "
                    "Log transformation was considered but raw rates were retained to preserve interpretability of regression coefficients.",
                    "Continuous predictors (income, home value, education) were examined for multicollinearity using correlation matrices and variance inflation factors. "
                    "High correlations among income, home value, and education motivated the use of Ridge regression rather than OLS in the predictive models.",
                ]),
                method_block("Bivariate and Group Comparisons", [
                    "Scatter plots with income quintile overlays were used to examine whether infrastructure access and racial composition effects on EV adoption "
                    "persist after conditioning on income. This visual mediation check was formalized in the regression models.",
                    "Box plots stratified by income quintile were used to compare EV adoption and infrastructure distributions across the income spectrum, "
                    "capturing distributional shape rather than just means.",
                ]),
            ]),

            # 3. REGRESSION METHODS
            section_card(3, "Regression Modeling", [
                method_block("OLS Baseline (Ordinary Least Squares)", [
                    "OLS is the standard starting point for regression — it fits a line (or plane) through the data that minimizes the total squared error between "
                    "predicted and actual EV adoption rates. It gives us a coefficient for each predictor, telling us how much EV adoption changes on average "
                    "for a one-unit increase in that variable, holding everything else constant.",
                    "The issue with OLS here is that income, education, and home value are highly correlated with each other — when predictors move together, "
                    "OLS struggles to isolate the effect of each one individually, producing unstable estimates. This motivated us to use Ridge regression as the main model.",
                ]),
                method_block("Ridge Regression (L2 Regularization)", [
                    "Ridge regression is a refinement of OLS designed for situations where predictors are correlated. It works by adding a small penalty for large coefficients — "
                    "this forces the model to spread the 'credit' more evenly across correlated variables rather than over-attributing the effect to whichever one happens to "
                    "correlate slightly more in the training data. The result is more stable, reliable estimates.",
                    "The strength of this penalty (called lambda) was tuned using cross-validation. We chose Ridge over LASSO (a related technique that zeros out some predictors entirely) "
                    "because all our variables are theoretically meaningful — we want to keep them all and compare their relative importance, not drop any automatically.",
                    "Ridge was used for the main EV adoption model, the income-infrastructure interaction model, the high-income subset model, and the PHEV pathway model.",
                ]),
                method_block("Polynomial Regression (Nonlinear Income Effect)", [
                    "Standard regression assumes that the relationship between income and EV adoption is a straight line — every additional dollar of income produces the same "
                    "increase in adoption. But we suspected the relationship curves upward: EV adoption might be low and relatively flat at lower incomes, then accelerate "
                    "sharply once households cross an affordability threshold.",
                    "To test this, we added a quadratic income term (income²) to the model. A positive coefficient on that term confirms the relationship is convex — "
                    "adoption rises faster at higher income levels — which is consistent with EVs behaving more like a luxury good than a linear function of purchasing power.",
                ]),
                method_block("Interaction Terms (Income × Infrastructure)", [
                    "A standard regression model assumes that the effect of charging infrastructure on EV adoption is the same regardless of a community's income level. "
                    "An interaction term relaxes that assumption — it lets the effect of infrastructure vary depending on income.",
                    "We added an interaction between income and charging port density (income × PortsPer10kPeople). A positive coefficient on this term means that "
                    "infrastructure has a stronger effect in higher-income communities — in other words, adding more chargers in a wealthy area boosts adoption more than "
                    "adding the same number of chargers in a lower-income area. This is a direct test of whether infrastructure investment closes or widens equity gaps.",
                ]),
                method_block("Sequential Regression for Racial Disparity", [
                    "To understand whether observed racial disparities in EV adoption reflect race itself or underlying socioeconomic differences, we ran two models in sequence. "
                    "First, we regressed EV adoption on racial composition variables alone. Then we re-ran the same model but added income, education, and housing controls.",
                    "If the racial composition coefficients shrink substantially when the socioeconomic controls are added, it suggests the disparity is largely explained by "
                    "structural economic differences rather than race directly. This approach — called partial mediation — is a standard way to decompose an observed association "
                    "into its direct and indirect components.",
                ]),
            ]),

            # 4. MACHINE LEARNING
            section_card(4, "Machine Learning", [
                method_block("Random Forest Regressor", [
                    "Random forests are an ensemble method that builds many decision trees on bootstrapped subsets of the data and averages their predictions. "
                    "Each split considers a random subset of features, reducing correlation between trees. "
                    "This produces a low-variance estimator that captures nonlinear relationships and feature interactions without explicit specification.",
                    "Random forest was used alongside Ridge regression for EV adoption prediction. Feature importance scores (mean decrease in impurity) "
                    "provide a model-agnostic measure of predictor relevance that complements the interpretable coefficients from Ridge.",
                ]),
                method_block("Logistic Regression (Binary Classification)", [
                    "Logistic regression models the log-odds of a binary outcome as a linear combination of predictors. "
                    "It was used to classify ZIP codes as EV deserts (bottom 20% by adoption) and infrastructure deserts (bottom quintile by charging access). "
                    "Coefficients are interpretable as log-odds ratios, and the model is well-suited for identifying which features most strongly push a ZIP toward the disadvantaged class.",
                ]),
                method_block("Random Forest Classifier", [
                    "Random forest classification was used in parallel with logistic regression for each binary task. "
                    "The classifier captures nonlinear boundaries — for example, the interaction between poverty and renter share that logistic regression treats as additive. "
                    "Comparing logistic regression and Random Forest results cross-validates the feature importance findings.",
                ]),
                method_block("Train/Test Split & Evaluation", [
                    "All models used a stratified 80/20 train-test split to evaluate out-of-sample performance. "
                    "Regression models were assessed using R-squared on the held-out test set. Classification models were assessed using accuracy, "
                    "precision, recall, F1-score, and ROC-AUC. AUC is reported as the primary metric for classifiers because it is threshold-independent "
                    "and robust to class imbalance — relevant here because EV deserts represent only 20% of the dataset by construction.",
                ]),
            ]),

            # 5. LIMITATIONS
            section_card(5, "Methodological Limitations", [
                method_block("Cross-Sectional Design", [
                    "All data reflect a single point in time (approximately 2021). Associations between predictors and EV adoption cannot be interpreted as causal — "
                    "reverse causality is plausible (e.g., high-income communities may attract charging infrastructure because they already have high EV demand).",
                ]),
                method_block("Geographic Aggregation Bias", [
                    "ZIP codes can contain very heterogeneous neighborhoods. Aggregation to the ZIP level masks within-ZIP variation — "
                    "a ZIP with mixed high- and low-income neighborhoods will appear as a moderate-income ZIP, losing the distributional information. "
                    "The CalEnviroScreen tract-to-ZIP aggregation introduces additional noise where tract and ZIP boundaries misalign.",
                ]),
                method_block("Omitted Variable Bias", [
                    "Several theoretically relevant variables are not captured: consumer attitudes toward EVs, proximity to EV dealerships, "
                    "local electricity rates, employer EV incentives, and building permit requirements for EV-ready construction. "
                    "Their omission means that regression coefficients for included variables may be biased if they correlate with these unobserved factors.",
                ]),
            ]),

            # REFERENCES
            html.Div(
                className="card",
                children=[
                    html.H2("References", className="section-title"),
                    html.Ol(
                        className="fd-ref-list",
                        children=[
                            ref_item(1, "Hoerl, A. E., & Kennard, R. W. (1970). Ridge regression: Biased estimation for nonorthogonal problems. Technometrics, 12(1), 55-67.", "https://doi.org/10.1080/00401706.1970.10488634"),
                            ref_item(2, "Lopez, N., & Yee, E. (2023). Who buys electric cars in California — and who doesn't? CalMatters.", "https://calmatters.org/environment/2023/03/california-electric-cars-demographics/"),
                            ref_item(3, "U.S. Census Bureau. (2023). American Community Survey 5-Year Estimates. Retrieved via Census API.", "https://www.census.gov/data/developers/data-sets/acs-5year.html"),
                            ref_item(4, "California OEHHA. (2021). CalEnviroScreen 4.0 Methodology. Office of Environmental Health Hazard Assessment.", "https://oehha.ca.gov/calenviroscreen/report/calenviroscreen-40"),
                            ref_item(5, "National Renewable Energy Laboratory. (2021). Alternative Fuel Stations API. U.S. Department of Energy.", "https://developer.nrel.gov/docs/transportation/alt-fuel-stations-v1/"),
                        ],
                    ),
                ],
            ),
        ],
    )
])
