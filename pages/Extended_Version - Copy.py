import streamlit as st
import pandas as pd
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
    'Meta AI': '#34b3f0',
    'OpenAI': '#00A67E',
    'x.AI': '#000000'
}

# ========== SIDEBAR ==========
with st.sidebar:
    st.title("AI Risk Dashboard")
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
<style>
    .logo-container {
        top: 60px;
        left: 10px;
        right: 10px;
        z-index: 100;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }
    .logo-img {
        max-height: 75px;
        width: auto;
    }
</style>
  
<div class="logo-container">
    <img src="https://upload.wikimedia.org/wikipedia/commons/c/c7/London_school_of_economics_logo_with_name.svg" class="logo-img" alt="LSE Logo">
    <img src="https://upload.wikimedia.org/wikipedia/commons/4/4d/Logo_of_the_United_Nations.svg" class="logo-img" alt="UN Logo">
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1>🌍 AI Risk Dashboard</h1>
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
                        {'range': [0, 33], 'color': '#008450', },
                        {'range': [33, 66], 'color': '#EFB700', },
                        {'range': [66, 100], 'color': '#B81D13', }
                    ],
                    'threshold': {
                        'line': {'color': 'whitesmoke', 'width': 4},
                        'thickness': 0.69,
                        'value': row['Standardized Value']
                    },
                    'bordercolor':'white',
                },
                # number={'font': {'size': 24}}
            ))
            fig.update_layout(
                width=300 * len(risk_company_df),
                height=300,
                margin=dict(t=0, b=0),
                font={'family': 'Roboto', 'color': '#454545'}
            )
            st.plotly_chart(fig, use_container_width=True)

# ========== COMPARATIVE ANALYSIS ==========
    
# Company selection in sidebar
companies = category_df['Company'].unique()
if not len(companies):
    st.warning("Select at least one company")
selected_companies = st.multiselect(
    'Which company would you like to view?',
    companies,
    default=companies,
    help="Choose companies to analyze their risk profiles"
    )
''
''
st.markdown("---")
st.markdown("### Comparative Risk Analysis")

tab1, tab2, tab3 = st.tabs(["# Category Breakdown", "# Detailed Metrics", "# Tables"])

with tab1:
    # Risk Category Comparison
    st.markdown("#### Risk Category Comparison")
    fig = go.Figure()
    
    for company in selected_companies:
        company_data = category_df[category_df['Company'] == company]
        fig.add_trace(go.Scatterpolar(
            r=company_data['Standardized Value'],
            theta=company_data['Risk Category'].str.replace(r'\d+\.\s*', '', regex=True),
            connectgaps=True,
            fill='toself',
            name=company,
            line=dict(color=color_map[company], width=2),
            hoverlabel=dict(font={'family': 'Roboto'})
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100]),
            angularaxis=dict(rotation=90)
        ),
        template='plotly_white',
        height=500,
        hovermode="x unified",
        font={'family': 'Roboto', 'color': '#454545'},
        legend=dict(orientation="h", yanchor="bottom", y=-0.3,
            xanchor="center",x=0.5),
        margin=dict(t=40)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Risk Indicator Comparison
    st.markdown("---")
    st.markdown("#### Risk Indicator Comparison")
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
            font={'family': 'Roboto', 'color': '#454545'},
            legend=dict(orientation="h", yanchor="bottom", y=-0.3,
            xanchor="center",x=0.5),
            height=500,
            margin=dict(t=60)
        )
        # # Add annotations for Risk ID and Risk Indicator
        # annotations = []
        # for risk_id, risk_indicator in zip(category_data['Risk ID'].unique(), category_data['Risk Indicator'].unique()):
        #     annotations.append(f"{risk_id}: {risk_indicator}")
        
        # # Update the layout
        # fig.update_layout(
        #     polar=dict(
        #         radialaxis=dict(
        #             visible=True,
        #             range=[0, 100]),
        #     angularaxis=dict(
        #         rotation=90
        #     )),
        #     showlegend=True,
        #     title=f"{category}",
        #     annotations=[dict(
        #         x=1.0,
        #         y=1.1,
        #         xref="paper",
        #         yref="paper",
        #         showarrow=False,
        #         text="<br>".join(annotations),
        #         align="left"
        #     )],
        #     font=dict(color='#454545'),
        #     plot_bgcolor='#e4effb'
        # )
    
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Detailed Category Analysis
    st.markdown("#### Detailed Category Analysis")
    
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
            annotation['y'] += 0.1 
        
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
    st.markdown("#### Detailed Metric Analysis")
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
            marker=dict(color=color_map[company]),
            hoverinfo='x+text',
            textposition='auto'
        ))
    
    fig.update_layout(
        barmode='group',
        height=500,
        xaxis_title="Risk Score",
        yaxis_title="Indicator",
        font={'family': 'Roboto', 'color': '#454545'},
        hoverlabel=dict(font={'family': 'Roboto'}),
        margin=dict(l=150)
    )
    st.plotly_chart(fig, use_container_width=True)


with tab3:
    st.markdown("""
    <style>
        .table-container {
            padding-top: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("#### Risk Category Data")
    
    # Show category_df with scrollable container
    with st.container(height=400):
        st.dataframe(
            category_df,
            use_container_width=True,
            column_order=("Company", "Risk Category", "Standardized Value"),
            column_config={
                "Standardized Value": st.column_config.ProgressColumn(
                    "Risk Score",
                    help="Risk score percentage",
                    format="%.2f",
                    min_value=0,
                    max_value=100,
                )
            }
        )
    
    st.markdown("---")
    st.markdown("#### Risk Indicator Data")
    
    # Show indicator_df with horizontal scroll
    with st.container(height=600):
        st.dataframe(
            indicator_df,
            use_container_width=True,
            column_config={
                "Risk ID": st.column_config.TextColumn(width="small"),
                "Risk Indicator": st.column_config.TextColumn(width="large"),
                "Standardized Value": st.column_config.ProgressColumn(
                    "Score",
                    format="%.2f",
                    min_value=0,
                    max_value=100,
                )
            },
            hide_index=True
        )
# ========== FOOTER ==========
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; font-size: 0.9rem; padding: 1rem;">
    Data Source: Monitoring AI Risk Report • Updated: March 2025
</div>
""", unsafe_allow_html=True)