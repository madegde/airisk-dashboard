import streamlit as st
import pandas as pd
import math
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='AI Risk Dashboard Extended Version',
    page_icon=':earth_asia:', # This is an emoji shortcode. Could be a URL too.
    layout="wide",
)
# Sidebar controls
with st.sidebar:
    st.title("AI Risk Dashboard Extended")
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
    DATA_FILENAME1 = Path('data/risk_category_full.csv')
    risk_category_df = pd.read_csv(DATA_FILENAME1)

    DATA_FILENAME2 = Path('data/riskindicators_table_full.csv')
    risk_indicator_df = pd.read_csv(DATA_FILENAME2)

    DATA_FILENAME3 = Path('data/risk_company_full.csv')
    risk_company_df = pd.read_csv(DATA_FILENAME3)

    return risk_category_df, risk_indicator_df, risk_company_df

risk_category_df, risk_indicator_df, risk_company_df = get_risk_data()
indicator_df['Risk ID'] = indicator_df['Risk ID'].astype(str)
# ----------------------------------------------------------------------------- 
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :earth_asia: AI Risk Dashboard Extended Version

Capstone Project - LSE MPA in Data Science for Public Policy & United Nations University Centre for Policy Research (UNU-CPR)
'''


''
''
# GAUGE CHART
# Create gauge charts for each company horizontally
fig = make_subplots(
    rows=1, cols=len(risk_company_df),
    horizontal_spacing=0.05,
    # subplot_titles=risk_company_df['Company'].tolist(),
    specs=[[{'type': 'domain'} for _ in range(len(risk_company_df))]]
)

for i, row in risk_company_df.iterrows():
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=row['Standardized Value'],
            title={'text': f"{row['Company']}"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "whitesmoke"},
                'steps': [
                    {'range': [0, 33], 'color': "#008450"},
                    {'range': [33, 66], 'color': "#EFB700"},
                    {'range': [66, 100], 'color': "#B81D13"}
                ],
                'threshold': {
                    'line': {'color': "whitesmoke", 'width': 5},
                    'thickness': 0.69,
                    'value': row['Standardized Value']
                },
                'bordercolor':'white',


            }
        ),
        row=1, col=i+1
    )

fig.update_layout(
    width=300 * len(risk_company_df),
    height=400,
    showlegend=False,
    title="Competitive Dynamic Risk Scores"
)

st.plotly_chart(fig)
''
''
# TABLE RISK INDEX
col1, col2 = st.columns([3, 3], vertical_alignment='center')

with col1:
    st.subheader("Table Risk Index")
    # Sort the DataFrame by 'Standardized Value' in descending order
    sorted_risk_company_df = risk_company_df.sort_values(by='Standardized Value', ascending=False)

    # Create a table
    table = go.Figure(data=[go.Table(
        header=dict(values=['Company', 'Risk Index'],
                    fill_color='#009edb',
                    font=dict(color='#ffffff'),
                    align='center'),
        cells=dict(values=[sorted_risk_company_df['Company'], sorted_risk_company_df['Standardized Value'].map('{:.2f}'.format)],
                fill_color='#e4effb',
                font=dict(color='#454545'),
                align='center'))
    ])

    # Update the layout
    table.update_layout(
        autosize=False,
        width=500,
        height=200,
        margin=dict(l=10, r=10, t=40, b=0),
        # paper_bgcolor='#ffffff'
    )

    # Show the table
    st.plotly_chart(table)

with col2:
    st.subheader("Risk by Company")
    # Create a horizontal bar chart
    fig = go.Figure(data=[
        go.Bar(
            name='Standardized Value', 
            x=risk_company_df['Standardized Value'], 
            y=risk_company_df['Company'], 
            orientation='h',
            text=risk_company_df.index + 1,  # Add rank as text
            textposition='auto',
            marker=dict(color='#009edb')  # Set the bar color
        )
    ])

    # Update the layout to remove x-axis and show y-axis with company names
    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=True, tickmode='array', tickvals=risk_company_df.index, ticktext=risk_company_df['Company']),
        template='plotly_white',
        # plot_bgcolor='#e4effb',  # Set the background color
        # paper_bgcolor='#ffffff',  # Set the secondary background color
        font=dict(color='#454545')  # Set the text color and font
    )
    st.plotly_chart(fig)
''
''
# DROPDOWN MENU
# Create a list of unique companies
companies = category_df['Company'].unique()

if not len(companies):
    st.warning("Select at least one company")

selected_companies = st.multiselect(
    'Which company would you like to view?',
    companies,
    ['Anthropic', 'Google DeepMind', 'Meta AI', 'OpenAI', 'x.AI'])

''
''
# RISK INDEX BASED ON CATEGORY
# Create a list of unique risk categories
categories = category_df['Risk Category'].unique()

# Create a radar chart for the selected companies
# Create a radar chart
fig = go.Figure()

# Add a trace for each company
for company in companies:
    company_data = risk_category_df[risk_category_df['Company'] == company]
    fig.add_trace(go.Scatterpolar(
        r=company_data['Standardized Value'],
        theta=categories,
        connectgaps=True,
        fill='toself',
        name=company
    ))

# Update the layout
fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 100]
        )),
    showlegend=True,
    title="Risk Index based on Category",
    plot_bgcolor='#e4effb',  # Set the background color
    font=dict(color='#454545')  # Set the text color
)

# Display the radar chart in Streamlit
st.plotly_chart(fig)

''
''
# RISK CATEGORY FOR EACH COMPANY
# Create a subplot with 1 row and multiple columns (one for each company)
fig = make_subplots(
    rows=1, 
    cols=len(companies), 
    subplot_titles=[f"{company}" for company in companies], 
    specs=[[{'type': 'polar'}] * len(companies)]
)

# Add a trace for each company in its respective subplot
for i, company in enumerate(companies):
    company_data = risk_category_df[risk_category_df['Company'] == company]
    company_data = company_data.replace({
        'Risk Category': {
            "1. Hypercompetitive behavior": "Hypercompetitive",
            "2. ​Lack of compliance and safety practices": "Unsafety",
            "3. Lack of commitment to emerging standards": "Lack of Commitment",
            "4. Incidents": "Incidents"
        }
    })
    fig.add_trace(go.Scatterpolar(
        r=company_data['Standardized Value'],
        theta=company_data['Risk Category'],
        connectgaps=True,
        fill='toself',
        name=company
    ), row=1, col=i+1)

# Adjust the position of the subplot titles
for annotation in fig['layout']['annotations']:
    annotation['y'] += 0.1  

# Update the layout
for j in range(1, len(companies) + 1):
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
    width=3500,  # Adjust width as needed
    showlegend=False,
    # title="Risk Index based on Category for Each Company"
    plot_bgcolor='#e4effb',  # Set the background color
    font=dict(color='#454545')  # Set the text color
)

st.plotly_chart(fig)
''
''
# RISK INDICATOR CHART FOR EACH CATEGORY
# Create a radar chart for each category
for category in categories:
    category_data = df[df['Risk Category'] == category]
    
    fig = go.Figure()
    
    # Add a trace for each company
    for company in companies:
        company_data = category_data[category_data['Company'] == company]
        fig.add_trace(go.Scatterpolargl(
            r=company_data['Standardized Value'],
            theta=company_data['Risk ID'],
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
                range=[0, 100]
            )),
        showlegend=True,
        title=f"Radar Chart for {category}",
        annotations=[dict(
            x=1.0,
            y=1.1,
            xref="paper",
            yref="paper",
            showarrow=False,
            text="<br>".join(annotations),
            align="left"
        )],
        plot_bgcolor='#e4effb',
        font=dict(color='#454545')
    )
    
    
    # Display the radar chart in Streamlit
    st.plotly_chart(fig)