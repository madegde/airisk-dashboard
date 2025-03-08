import streamlit as st
import pandas as pd
import math
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ========== INITIAL SETUP ==========
st.set_page_config(
    page_title='AI Risk Dashboard',
    page_icon=':earth_asia:',
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== DATA LOADING ==========
@st.cache_data
def get_risk_data():
    DATA_FILENAME1 = Path('data/risk_category_std.csv')
    risk_category_df = pd.read_csv(DATA_FILENAME1)

    DATA_FILENAME2 = Path('data/riskindicators_table_std.csv')
    risk_indicator_df = pd.read_csv(DATA_FILENAME2)

    DATA_FILENAME3 = Path('data/risk_company_std.csv')
    risk_company_df = pd.read_csv(DATA_FILENAME3)

    return risk_category_df, risk_indicator_df, risk_company_df

category_df, indicator_df, risk_company_df = get_risk_data()
indicator_df['Risk ID'] = indicator_df['Risk ID'].astype(str)

# ========== COLOR SCHEME ==========
color_map = {
    'Anthropic': '#da7756',
    'Google DeepMind': '#4285F4',
    'Meta AI': '#34b3f0', #1877F2
    'OpenAI': '#00A67E',
    'x.AI': '#000000'
}

# ========== SIDEBAR ==========
with st.sidebar:
    st.title("AI Risk Dashboard")
    # st.markdown("""
    # **Capstone Project**  
    # LSE MPA in Data Science for Public Policy  
    # United Nations University Centre for Policy Research (UNU-CPR)
    # """)
    
    # companies = category_df['Company'].unique()
    # selected_companies = st.multiselect(
    #     'Select Companies',
    #     companies,
    #     default=companies,
    #     help="Compare risk profiles across different AI companies"
    # )
    
    st.markdown("---")
    st.markdown("**Color Legend**")
    for company, color in color_map.items():
        st.markdown(f"<span style='color: {color};'>■</span> {company}", unsafe_allow_html=True)

# ========== CUSTOM STYLES ==========
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    * {
        font-family: 'Roboto', sans-serif !important;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Roboto', sans-serif !important;
        font-weight: 700 !important;
    }
    
    .metric-card {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    h2 {
        border-bottom: 2px solid #009edb;
        padding-bottom: 0.3rem;
        color: #2c3e50;
    }
    
    .dataframe {
        font-family: 'Roboto', sans-serif !important;
    }
    
    .table-style {
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ========== HELPER FUNCTIONS ==========
def get_risk_color(value):
    """Determine color based on risk score"""
    if value <= 33:
        return '#008450'  # Green
    elif value <= 66:
        return '#EFB700'  # Yellow
    else:
        return '#B81D13'  # Red

# ========== MAIN CONTENT ==========
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="color: #2c3e50; font-size: 2.5rem; margin-bottom: 0.5rem;">
        🌍 AI Risk Dashboard
    </h1>
    <p style="color: #7f8c8d; font-size: 1.1rem;">
        **Capstone Project**  
        LSE MPA in Data Science for Public Policy & United Nations University Centre for Policy Research (UNU-CPR)
    </p>
</div>
""", unsafe_allow_html=True)

# ========== GAUGE SECTION ==========
gauge_container = st.container()
with gauge_container:
    cols = st.columns(len(risk_company_df))
    for idx, (_, row) in enumerate(risk_company_df.iterrows()):
        with cols[idx]:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=row['Standardized Value'],
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1},
                    'bar': {'color': color_map[row['Company']]},
                    'steps': [
                        {'range': [0, 33], 'color': '#008450', 'oppacity': 0.5},
                        {'range': [33, 66], 'color': '#EFB700', 'oppacity': 0.5},
                        {'range': [66, 100], 'color': '#B81D13', 'oppacity': 0.5}
                    ],
                    'threshold': {
                        'line': {'color': 'whitesmoke', 'width': 4},
                        'thickness': 0.69,
                        'value': row['Standardized Value']
                    }
                }
            ))
            fig.update_layout(
                height=250,
                margin=dict(t=0, b=0),
                font=dict(
                        family="Roboto",
                        color='#2c3e50',
                        size=14
                        )
            )
            st.plotly_chart(fig, use_container_width=True)

st.markdown("### Competitive Dynamics Risk Scores")
with st.expander("Understanding Comparative Risk Scores", expanded=False):
    st.markdown("""
    - **0-33**: Low Risk among Companies (Green)
    - **34-66**: Moderate Risk among Companies (Yellow)
    - **67-100**: High Risk among Companies (Red)
    """)

# ========== DROPDOWN MENU ==========
companies = category_df['Company'].unique()

if not len(companies):
    st.warning("Select at least one company")

selected_companies = st.multiselect(
    'Which company would you like to view?',
    companies,
    default=companies,
    help="Compare risk profiles across different AI companies"
    )


# ========== COMPARATIVE ANALYSIS ==========
st.markdown("---")
st.markdown("### Comparative Risk Analysis")

tab1, tab2 = st.tabs(["Category Breakdown", "Detailed Metrics"])

# with tab1:
#     st.markdown("#### Company Risk Index Ranking")
#     sorted_df = risk_company_df.sort_values('Standardized Value', ascending=False)
#     sorted_df['Rank'] = range(1, len(sorted_df)+1)
    
#     # Create styled dataframe
#     styled_df = (
#         sorted_df[['Rank', 'Company', 'Standardized Value']]
#         .rename(columns={'Standardized Value': 'Risk Score'})
#         .style
#         .format({'Risk Score': '{:.1f}'})
#         .apply(lambda x: [
#             f'background: {color_map[val]}; color: white' 
#             if x.name == 'Company' else 
#             f'background: {get_risk_color(val)}; color: white' 
#             for val in x
#         ], axis=0)
#     )
    
#     st.dataframe(styled_df, use_container_width=True)

with tab1:
    st.markdown("#### Risk Category Comparison")
    fig = go.Figure()
    for company in selected_companies:
        company_data = category_df[category_df['Company'] == company]
        fig.add_trace(go.Scatterpolar(
            r=company_data['Standardized Value'],
            theta=company_data['Risk Category'].str.replace(r'\d+\.\s*', '', regex=True),
            fill='toself',
            name=company,
            line=dict(color=color_map[company], width=2),
            # hoverlabel=dict(bgcolor=color_map[company])
        ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        template='plotly_white',
        angularaxis=dict(rotation=90),
        height=500,
        hovermode="x unified",
        showlegend=True,
        font=dict(family="Roboto", color='#454545'),
        hoverlabel=dict(bgcolor="white"),
        plot_bgcolor='#e4effb'
        # legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Risk Indicator Comparison")
    for category in categories:
        category_data = indicator_df[indicator_df['Risk Category'] == category]
        
        fig = go.Figure()
        
        # Add a trace for each selected company
        for company in selected_companies:
            company_data = category_data[category_data['Company'] == company]
            fig.add_trace(go.Scatterpolar(
                r=company_data['Standardized Value'],
                theta=company_data['Risk Indicator'].astype(str),  # Ensure Risk ID is treated as a string
                connectgaps=True,
                fill='toself',
                name=company,
                line=dict(color=color_map[company])
            ))

        # Update the layout to move the legend to the bottom
        fig.update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5
            )
        )
        
        # Add annotations for Risk ID and Risk Indicator
        annotations = []
        for risk_id, risk_indicator in zip(category_data['Risk ID'].unique(), category_data['Risk Indicator'].unique()):
            annotations.append(f"{risk_id}: {risk_indicator}")
        
        # Update the layout
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]),
            angularaxis=dict(
                rotation=90
            )),
            showlegend=True,
            title=f"{category}",
            annotations=[dict(
                x=1.0,
                y=1.1,
                xref="paper",
                yref="paper",
                showarrow=False,
                text="<br>".join(annotations),
                align="left"
            )],
            font=dict(family="Roboto", color='#454545'),
            plot_bgcolor='#e4effb'
        )
        
        # Display the radar chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("#### Detailed Category Analysis")
    fig = make_subplots(
        rows=1, 
        cols=len(selected_companies), 
        subplot_titles=[f"{company}" for company in selected_companies], 
        specs=[[{'type': 'polar'}] * len(selected_companies)]
    )

    # Add a trace for each company in its respective subplot
    for i, company in enumerate(selected_companies):
        company_data = category_df[category_df['Company'] == company]
        company_data = company_data.replace({
            'Risk Category': {
                "1. Hypercompetitive behavior": "Hypercompetitive",
                "2. ​Lack of compliance and safety practices": "Lack of Safety",
                "3. Lack of commitment to emerging standards": "Lack of Commitment",
                "4. Incidents": "Incidents"
            }
        })
        fig.add_trace(go.Scatterpolar(
            r=company_data['Standardized Value'],
            theta=company_data['Risk Category'],
            connectgaps=True,
            fill='toself',
            name=company,
            line=dict(color=color_map[company])
        ), row=1, col=i+1)

    # Adjust the position of the subplot titles
    for annotation in fig['layout']['annotations']:
        annotation['y'] += 0.1  

    # Update the layout
    for j in range(1, len(selected_companies) + 1):
        fig.update_layout(**{f'polar{j}': dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            ),
            angularaxis=dict(
                rotation=90
            ))
        })

    fig.update_layout(
        width=250*len(selected_companies),
        height=250 + 300/len(selected_companies),
        showlegend=False,
        # title="Risk Index based on Category for Each Company",
        font=dict(family="Roboto", color='#454545'),
        plot_bgcolor='#e4effb'
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Detailed Metric Analysis")
    selected_category = st.selectbox(
        "Select Risk Category",
        category_df['Risk Category'].unique(),
        index=0,
        key='category_selector'
    )
    
    category_data = indicator_df[indicator_df['Risk Category'] == selected_category]
    fig = go.Figure()
    for company in selected_companies:
        company_data = category_data[category_data['Company'] == company]
        fig.add_trace(go.Bar(
            x=company_data['Standardized Value'],
            y=company_data['Risk Indicator'],
            name=company,
            orientation='h',
            marker=dict(color=color_map[company]),
            hoverinfo='x+text',
            textposition='auto'
        ))
    
    fig.update_layout(
        barmode='group',
        height=500,
        xaxis_title="Risk Score",
        yaxis_title="Indicator",
        font=dict(family="Roboto", color='#454545'),
        hoverlabel=dict(bgcolor="white")
        
    )
    st.plotly_chart(fig, use_container_width=True)

# ========== FOOTER ==========
st.markdown("---")
st.markdown("""
<div style="text-align: right; color: #7f8c8d; font-size: 0.9rem;">
    Data Source: Monitoring AI Risk Report • Updated: March 2025
</div>
""", unsafe_allow_html=True)