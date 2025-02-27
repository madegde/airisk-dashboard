import streamlit as st
import pandas as pd
import math
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='AI Risk dashboard',
    page_icon=':earth_asia:', # This is an emoji shortcode. Could be a URL too.
    layout="wide",
)

# Sidebar controls
with st.sidebar:
    st.title("Rank Dashboard")
# ----------------------------------------------------------------------------- 
# Declare some useful functions.

@st.cache_data
def get_risk_data():
    DATA_FILENAME1 = Path('data/risk_category_rank.csv')
    rank_cat_df = pd.read_csv(DATA_FILENAME1)

    DATA_FILENAME2 = Path('data/riskindicators_table_rank.csv')
    rank_df = pd.read_csv(DATA_FILENAME2)

    DATA_FILENAME3 = Path('data/risk_company_rank.csv')
    rank_company_df = pd.read_csv(DATA_FILENAME3)

    return rank_cat_df, rank_df, rank_company_df

rank_cat_df, rank_df, rank_company_df = get_risk_data()
rank_df['Risk ID'] = rank_df['Risk ID'].astype(str)
# ----------------------------------------------------------------------------- 
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :earth_asia: AI Risk Dashboard

Capstone Project - LSE MPA in Data Science for Public Policy & United Nations University Centre for Policy Research (UNU-CPR)
'''

# Add some spacing
''
''
st.subheader("Competitive Dynamic Risk Ranking by Company")
# Create a horizontal bar chart
fig = go.Figure(data=[
    go.Bar(
        name='Rank', 
        x=rank_company_df['Rank'], 
        y=rank_company_df['Company'], 
        orientation='h',
        text=rank_company_df.index + 1,  # Add rank as text
        textposition='auto',
        marker=dict(color='#009edb')
    )
])

# Update the layout to remove x-axis and show y-axis with company names
fig.update_layout(
    # title='Rank by Company',
    xaxis=dict(showgrid=False, zeroline=False, visible=False),
    yaxis=dict(showgrid=False, zeroline=False, visible=True, tickmode='array', tickvals=rank_company_df.index, ticktext=rank_company_df['Company']),
    template='plotly_white',
    font=dict(color='#454545'),
)

# Display the radar chart in Streamlit
st.plotly_chart(fig)
''
''

rank_comp = rank_cat_df['Company'].unique()

if not len(rank_comp):
    st.warning("Select at least one company")

selected_companies = st.multiselect(
    'Which company would you like to view?',
    rank_comp,
    ['Anthropic', 'Google DeepMind', 'Meta AI', 'OpenAI', 'x.AI'])

''
''
st.subheader("Risk Rank based on Category")
# Create a list of unique risk categories
rank_cat = rank_cat_df['Risk Category'].unique()

# Create a radar chart
fig = go.Figure()

# Add a trace for each company
for company in rank_comp:
    company_data = rank_cat_df[rank_cat_df['Company'] == company]
    fig.add_trace(go.Scatterpolar(
        r=company_data['Rank'],
        theta=rank_cat,
        connectgaps=True,
        fill='toself',
        name=company
    ))

# Update the layout
fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 5]
        ),
        angularaxis=dict(
            rotation=90
        )
    ),
    showlegend=True,
    # title="Risk Rank based on Category",
    font=dict(color='#454545'),
    plot_bgcolor='#e4effb'
)

# Display the radar chart in Streamlit
st.plotly_chart(fig)
''
''
st.subheader("Risk Rank for each Category")
# Create a subplot with 1 row and multiple columns (one for each company)
fig = make_subplots(
    rows=1, 
    cols=len(selected_companies), 
    subplot_titles=[f"{company}" for company in selected_companies], 
    specs=[[{'type': 'polar'}] * len(selected_companies)]
)

# Add a trace for each company in its respective subplot
for i, company in enumerate(selected_companies):
    company_data = rank_cat_df[rank_cat_df['Company'] == company]
    company_data = company_data.replace({
        'Risk Category': {
            "1. Hypercompetitive behavior": "Hypercompetitive",
            "2. ​Lack of compliance and safety practices": "Unsafety",
            "3. Lack of commitment to emerging standards": "Lack of Commitment",
            "4. Incidents": "Incidents"
        }
    })
    fig.add_trace(go.Scatterpolar(
        r=company_data['Rank'],
        theta=company_data['Risk Category'],
        connectgaps=True,
        fill='toself',
        name=company
    ), row=1, col=i+1)

# Adjust the position of the subplot titles
for annotation in fig['layout']['annotations']:
    annotation['y'] += 0.1  

# Update the layout
for j in range(1, len(selected_companies) + 1):
    fig.update_layout(**{f'polar{j}': dict(
        radialaxis=dict(
            visible=True,
            range=[0, 5]
        ),
        angularaxis=dict(
            rotation=90
        ))
    })

fig.update_layout(
    width=300*len(selected_companies),
    height=300 + 250/len(selected_companies),
    showlegend=False,
    # title="Risk Index based on Category for Each Company",
    font=dict(color='#454545'),
    plot_bgcolor='#e4effb'
)

st.plotly_chart(fig)

''
''
# Create a radar chart for each category
for category in rank_cat:
    category_data = rank_df[rank_df['Risk Category'] == category]
    
    fig = go.Figure()
    
    # Add a trace for each company
    for company in selected_companies:
        company_data = category_data[category_data['Company'] == company]
        fig.add_trace(go.Scatterpolargl(
            r=company_data['Rank'],
            theta=company_data['Risk Indicator'].astype(str),
            connectgaps=True,
            fill='toself',
            name=company
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
                range=[0, 5]),
        angularaxis=dict(
            rotation=90
        )),
        showlegend=True,
        title=f"Rank Chart for {category}",
        annotations=[dict(
            x=1.0,
            y=1.1,
            xref="paper",
            yref="paper",
            showarrow=False,
            text="<br>".join(annotations),
            align="left"
        )],
        font=dict(color='#454545'),
        plot_bgcolor='#e4effb'
    )
    
    # Display the radar chart in Streamlit
    st.plotly_chart(fig)
