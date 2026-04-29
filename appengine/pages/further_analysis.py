import dash

from dash import html
dash.register_page(
    __name__,
    path="/further-analysis",
    name="Further Analysis"
)

def analysis_card(title, image_src, description):
    return html.Div(
        [
            html.H3(title, style={"marginBottom": "12px"}),
            html.Img(
                src=image_src,
                style={
                    "width": "100%",
                    "maxWidth": "850px",
                    "display": "block",
                    "margin": "0 auto 18px auto",
                    "borderRadius": "10px",
                    "boxShadow": "0 4px 12px rgba(0,0,0,0.12)"
                }
            ),

            html.P(
                description,
                style={
                    "fontSize": "17px",
                    "lineHeight": "1.8",
                    "marginBottom": "40px",
                    "color": "#333"
                }
            ),
        ],

        style={
            "backgroundColor": "white",
            "padding": "28px",
            "borderRadius": "14px",
            "boxShadow": "0 4px 14px rgba(0,0,0,0.08)",
            "marginBottom": "32px"
        }
    )

layout = html.Div(
    [
        html.H1(
            "Further Analysis / ML Modeling",
            style={
                "textAlign": "center",
                "marginBottom": "12px"
            }
        ),

        html.P(
            "This section extends the main analysis by examining how income, infrastructure, and adoption behavior interact to shape electric vehicle uptake across California ZIP codes. These results move beyond descriptive trends and focus on deeper patterns that help explain why EV adoption remains uneven across communities.",
            style={
                "maxWidth": "950px",
                "margin": "0 auto 35px auto",
                "textAlign": "center",
                "fontSize": "18px",
                "lineHeight": "1.8",
                "color": "#444"
            }
        ),

        analysis_card(
            "1. EV Adoption by Income Quintile",
            "/images/equity_gap.png",
            "This visualization highlights disparities in EV adoption across income levels. EV adoption increases steadily from the lowest to highest income quintile, with the highest-income areas showing significantly higher adoption rates. The gap between the top and bottom quintiles is substantial, with high-income ZIP codes exhibiting several times higher adoption than low-income areas. This provides strong evidence that EV adoption is highly unequal and strongly influenced by socioeconomic factors."
        ),

        analysis_card(
            "2. Infrastructure × Income Interaction",
            "/images/infra_income.png",
            "This plot examines the relationship between charging infrastructure and EV adoption across income groups. A clear separation is visible, where higher-income ZIP codes consistently exhibit higher EV adoption rates compared to lower-income areas, even at similar levels of infrastructure. This indicates that infrastructure alone does not drive EV adoption equally across communities. Instead, income plays a dominant role in determining how effectively communities can utilize available charging access. Overall, the results suggest that infrastructure investments alone may not eliminate disparities in EV adoption."
        ),

        analysis_card(
            "3. Hybrid Share vs EV Adoption",
            "/images/hybridev.png",
            "This visualization shows a strong positive relationship between hybrid vehicle share and EV adoption. ZIP codes with higher proportions of hybrid vehicles tend to have significantly higher EV adoption rates. This suggests that hybrid vehicles may act as a transition pathway toward full electrification, where communities already familiar with hybrid technology are more likely to adopt EVs. Overall, behavioral familiarity and gradual adoption patterns play an important role in EV uptake."
        ),

        analysis_card(
            "4. Infrastructure Effect within High-Income Areas",
            "/images/high_infrabox.png",
            "This plot compares EV adoption within high-income ZIP codes based on charging infrastructure availability. The results show that areas with higher infrastructure levels have noticeably higher median and mean EV adoption rates than those with lower infrastructure. The entire distribution shifts upward for high-infrastructure areas, indicating a consistent positive effect. This demonstrates that even among wealthy communities, infrastructure still plays an important role in supporting EV adoption."

        ),

        analysis_card(

            "5. Polynomial Income Effect on EV Adoption",
            "/images/polyEV.png",
            "This plot examines the nonlinear relationship between income and EV adoption. The curved trend shows that EV adoption increases at an accelerating rate as income rises, indicating that higher-income communities experience stronger gains in adoption. This suggests a threshold effect, where once income reaches a certain level, EV adoption grows more rapidly. Overall, income is a dominant and nonlinear driver of EV adoption."
        ),

        analysis_card(
            "6. Vehicle Transition Pathway by Income",
            "/images/vehicle_byincome.png",
            "This visualization shows how vehicle composition changes across income levels. While gasoline vehicles remain dominant, hybrid adoption increases slightly and EV adoption rises sharply with income. This suggests a gradual transition pathway from gasoline to hybrid to electric vehicles. However, lower-income communities appear to move more slowly along this pathway, indicating barriers to full electrification."
        ),
    ],

    style={
        "maxWidth": "1100px",
        "margin": "0 auto",
        "padding": "30px 20px 60px 20px",
        "backgroundColor": "#f7f9fc"
    }
)
