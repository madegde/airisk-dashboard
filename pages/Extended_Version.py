import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ========== INITIAL SETUP ==========
st.set_page_config(
    page_title='AI Risk Extended Dashboard',
    page_icon=':earth_asia:',
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== DATA LOADING ==========
@st.cache_data
def get_risk_data():
    DATA_FILENAME1 = Path('data/risk_category_full.csv')
    risk_category_df = pd.read_csv(DATA_FILENAME1)

    DATA_FILENAME2 = Path('data/riskindicators_table_full.csv')
    risk_indicator_df = pd.read_csv(DATA_FILENAME2)

    DATA_FILENAME3 = Path('data/risk_company_full.csv')
    risk_company_df = pd.read_csv(DATA_FILENAME3)

    return risk_category_df, risk_indicator_df, risk_company_df

category_df, indicator_df, risk_company_df = get_risk_data()
indicator_df['Risk ID'] = indicator_df['Risk ID'].astype(str)

# ========== COLOR SCHEME ==========
color_map = {
    'Anthropic': '#da7756',
    'Google DeepMind': '#4285F4',
    'Meta AI': '#34b3f0',
    'OpenAI': '#00A67E',
    'xAI': '#000000'
}

# ========== SIDEBAR ==========
with st.sidebar:
    st.title("AI Risk Dashboard Extended Version")
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
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    h1 {
        color: #2c3e50;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        border-bottom: 2px solid #009edb;
        padding-bottom: 0.3rem;
        color: #2c3e50;
        margin-top: 1.5rem;
    }
    
    .metric-card {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stPlotlyChart {
        border-radius: 8px;
    }
    
    [data-testid="stTabs"] {
        margin-top: 2rem;
    }
    
    [data-testid="stTab"] {
        padding: 15px 25px;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease;
    }

    [data-testid="stTab"]:hover {
        background-color: #f0f2f6;
    }

    [aria-selected="true"] {
        color: #009edb !important;
        border-bottom: 3px solid #009edb !important;
    }

    .chart-header {
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        color: #2c3e50 !important;
        margin-bottom: 1.5rem !important;
    }

    .dataframe th {
        background-color: #009edb !important;
        color: white !important;
        font-size: 1.1rem !important;
    }

    .dataframe td {
        font-size: 1rem !important;
    }

    .logo-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }
    .logo-img {
        max-height: 75px;
        width: auto;
    }
    .quote-box {
        border-left: 4px solid #009edb;
        background-color: #f0f9ff;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border-radius: 4px;
        color: #2c3e50;
        position: relative;
        min-height: 120px;
    }
    .attribution {
        position: absolute;
        bottom: 10px;
        right: 20px;
        font-style: normal;
        font-size: 0.9em;
        color: #6c757d;
    }
</style>
""", unsafe_allow_html=True)

# ========== MAIN CONTENT ==========
st.markdown("""
<div class="logo-container">
    <img src="https://upload.wikimedia.org/wikipedia/commons/c/c7/London_school_of_economics_logo_with_name.svg" class="logo-img" alt="LSE Logo">
    <img src="https://unu.edu/sites/default/files/2023-03/UNU-CPR_LOGO_NV.svg" class="logo-img" alt="UNU Logo">
</div>

<div style="text-align: center; margin-bottom: 2rem;">
    <h1>AI Risk Dashboard</h1>
    <h3>Extended Version</h3>
    <p style="color: #7f8c8d; font-size: 1.1rem;">
        Capstone Project <br> 
        LSE - MPA in Data Science for Public Policy & 
        United Nations University - Centre for Policy Research (UNU-CPR)
    </p>
</div>
""", unsafe_allow_html=True)

# ========== GAUGE SECTION ==========
st.markdown("### Competitive Dynamics Risk Scores")
with st.expander("Understanding Risk Scores", expanded=False):
    st.markdown("""
    <div class="quote-box">
        <div style="font-style: italic; margin-bottom: 30px;">
            "Competitive Dynamics" — AI developers or state-like actors competing in an AI ‘race’ 
            by rapidly developing, deploying, and applying AI systems to maximize strategic 
            or economic advantage, increasing the risk they release unsafe and error-prone systems.
        </div>
        <div class="attribution">
            - MIT AI Risk Repository
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    - **0-33**: Have Lower Risk among Companies (Green)
    - **34-66**: Have Moderate Risk among Companies (Yellow)
    - **67-100**: Have Higher Risk among Companies (Red)
    """)

gauge_container = st.container()
with gauge_container:
    cols = st.columns(len(risk_company_df))
    for idx, (_, row) in enumerate(risk_company_df.iterrows()):
        with cols[idx]:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=row['Standardized Value'],
                title={'text': f"{row['Company']}"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "whitesmoke"},
                    'steps': [
                        {'range': [0, 33], 'color': '#008450'},
                        {'range': [33, 66], 'color': '#EFB700'},
                        {'range': [66, 100], 'color': '#B81D13'}
                    ],
                    'threshold': {
                        'line': {'color': 'whitesmoke', 'width': 4},
                        'thickness': 0.69,
                        'value': row['Standardized Value']
                    }
                }
            ))
            fig.update_layout(
                width=300 * len(risk_company_df),
                height=300,
                margin=dict(t=0, b=0),
                font={'family': 'Roboto', 'color': '#454545'}
            )
            st.plotly_chart(fig, use_container_width=True)

# ========== COMPARATIVE ANALYSIS ==========
st.markdown("---")
st.markdown("### Comparative Score Analysis")

companies = category_df['Company'].unique()
selected_companies = st.multiselect(
    'Select Companies to Compare',
    companies,
    default=companies,
    help="Choose companies to analyze their risk profiles"
)

tab1, tab2, tab3 = st.tabs(["📊 Score Comparisons", "🔍 Detailed Metrics", "📋 Tables"])

with tab1:
    # Risk Category Comparison
    st.markdown('<div class="chart-header">Risk Category Comparison</div>', unsafe_allow_html=True)
    fig = go.Figure()
    
    for company in selected_companies:
        company_data = category_df[category_df['Company'] == company]
        fig.add_trace(go.Scatterpolar(
            r=company_data['Standardized Value'],
            theta=company_data['Risk Category'].str.replace(r'\d+\.\s*', '', regex=True),
            fill='toself',
            name=company,
            line=dict(color=color_map[company], width=2)
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(range=[0, 100]),
            angularaxis=dict(rotation=90)
        ),
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=-0.3,
            xanchor="center",x=0.5),
        margin=dict(t=40)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Risk Indicator Comparison
    st.markdown("---")
    st.markdown('<div class="chart-header">Risk Indicator Comparison</div>', unsafe_allow_html=True)
    categories = category_df['Risk Category'].unique()
    
    for category in categories:
        category_data = indicator_df[indicator_df['Risk Category'] == category]
        fig = go.Figure()
        
        for company in selected_companies:
            company_data = category_data[category_data['Company'] == company]
            fig.add_trace(go.Scatterpolar(
                r=company_data['Standardized Value'],
                theta=company_data['Risk Indicator'],
                connectgaps=True,
                fill='toself',
                name=company,
                line=dict(color=color_map[company]),
                hoverlabel=dict(font={'family': 'Roboto'})
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(range=[0, 100]),
                angularaxis=dict(rotation=90)
            ),
            title=category,
            legend=dict(orientation="h", yanchor="bottom", y=-0.3,
            xanchor="center",x=0.5),
            height=500,
            margin=dict(t=60)
        )
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown('<div class="chart-header">Company Comparison</div>', unsafe_allow_html=True)
    # Company-specific Radar Charts
    if len(selected_companies) > 0:
        fig = make_subplots(
            rows=1, 
            cols=len(selected_companies),
            specs=[[{'type': 'polar'}]*len(selected_companies)],
            subplot_titles=selected_companies
        )
        
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
                line=dict(color=color_map[company]),
                name=company
            ), 1, i+1)
        # Adjust the position of the subplot titles
        for annotation in fig['layout']['annotations']:
            annotation['y'] += 0.3 
        
        # Update the layout
        for j in range(1, len(selected_companies) + 1):
            fig.update_layout(**{f'polar{j}': dict(
                radialaxis=dict(visible=True, range=[0, 100]),
                angularaxis=dict(rotation=90))
            })
        
        fig.update_layout(
            width=200*len(selected_companies),
            height=200 + 300/len(selected_companies),
            showlegend=False,
            font={'family': 'Roboto', 'color': '#454545'},
            margin=dict(t=60)
        )
        st.plotly_chart(fig, use_container_width=True)

    # Detailed Metric Analysis
    st.markdown("---")
    st.markdown('<div class="chart-header">Detailed Risk Metrics</div>', unsafe_allow_html=True)
    selected_category = st.selectbox(
        "Select Risk Category",
        category_df['Risk Category'].unique(),
        index=0
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
            marker=dict(color=color_map[company])
        ))
    
    fig.update_layout(
        barmode='group',
        height=500,
        xaxis_title="Risk Score",
        yaxis_title="Indicator",
        margin=dict(l=150)
    )
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("Understanding Scoring Methodology", expanded=False):
        st.markdown("""
        The scoring method uses a min-max scaler to rate companies by risk. For each risk indicator, we take a company’s measurement, subtract by the lowest value across all companies, divide by the difference between the highest and lowest values, and multiply by 100. This gives a 0-100 score showing how the company compare to others.""")

with tab3:
    st.markdown('<div class="chart-header">Data Tables</div>', unsafe_allow_html=True)
    
    with st.expander("Company Data", expanded=True):
        st.dataframe(
            risk_company_df,
            use_container_width=True,
            column_config={
                "Standardized Value": st.column_config.ProgressColumn(
                    "Risk Score",
                    format="%.2f",
                    min_value=0,
                    max_value=100,
                )
            }
        )

    with st.expander("Category Data", expanded=True):
        st.dataframe(
            category_df,
            use_container_width=True,
            column_config={
                "Standardized Value": st.column_config.ProgressColumn(
                    "Risk Score",
                    format="%.2f",
                    min_value=0,
                    max_value=100,
                )
            }
        )
    
    with st.expander("Indicator Data", expanded=True):
        st.dataframe(
            indicator_df,
            use_container_width=True,
            column_config={
                "Standardized Value": st.column_config.ProgressColumn(
                    "Score",
                    format="%.2f",
                    min_value=0,
                    max_value=100,
                )
            }
        )

# ========== FOOTER ==========
st.markdown("---")
st.markdown("""
<div style="text-align: left; color: #7f8c8d; font-size: 0.9rem;">
    Data Source: Monitoring AI Risk: Corporate Competitive Dynamics - Capstone Project Report <br/> 
    Updated: March 2025
</div>
""", unsafe_allow_html=True)