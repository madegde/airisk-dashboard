import streamlit as st
import pandas as pd
import math
from pathlib import Path
import plotly.graph_objects as go

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='AI Risk dashboard',
    page_icon=':earth_asia:', # This is an emoji shortcode. Could be a URL too.
)

# ----------------------------------------------------------------------------- 
# Declare some useful functions.

@st.cache_data
def get_risk_data():
    """Grab risk data from CSV files.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME1 = Path('data/risk_category.csv')
    risk_category_df = pd.read_csv(DATA_FILENAME1)

    DATA_FILENAME2 = Path('data/riskindicators_table.csv')
    risk_indicator_df = pd.read_csv(DATA_FILENAME2)

    return risk_category_df, risk_indicator_df

category_df, indicator_df = get_risk_data()
indicator_df['Risk ID'] = indicator_df['Risk ID'].astype(str)
# ----------------------------------------------------------------------------- 
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :earth_asia: AI Risk dashboard

Lorem ipsum
'''

# Add some spacing
''
''

companies = category_df['Company'].unique()

if not len(companies):
    st.warning("Select at least one company")

selected_companies = st.multiselect(
    'Which company would you like to view?',
    companies,
    ['Anthropic', 'Google DeepMind', 'Meta AI', 'OpenAI', 'x.AI'])

''
''
''

# Create a list of unique risk categories
categories = category_df['Risk Category'].unique()

# Create a radar chart for the selected companies
fig = go.Figure()

# Add a trace for each selected company
for company in selected_companies:
    company_data = category_df[category_df['Company'] == company]
    fig.add_trace(go.Scatterpolar(
        r=company_data['Standardized Value'],
        theta=company_data['Risk Category'],
        connectgaps=True,
        fill='toself',
        name=company
    ))

# Update the layout
fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 400]
        )),
    showlegend=True,
    title="Risk Index based on Category"
)

# Display the radar chart in Streamlit
st.plotly_chart(fig)

''
''
# Create a radar chart for each category
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
                range=[0, 500]
            )),
        showlegend=True,
        title=f"Risk Index for {category}",
        annotations=[dict(
            x=1.0,
            y=1.1,
            xref="paper",
            yref="paper",
            showarrow=False,
            text="<br>".join(annotations),
            align="left"
        )]
    )
    
    # Display the radar chart in Streamlit
    st.plotly_chart(fig)