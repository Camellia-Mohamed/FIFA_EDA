import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
data = pd.read_csv("fifa_eda.csv")

# Sidebar Content
st.sidebar.image("https://play-lh.googleusercontent.com/NcrdWFjmF2GPRlif4xC-9WM4bQXxHjU4yuWVQjsdDh7xtKPc6nVSRhp-iOlFnpuepg")
st.sidebar.markdown("<h4 style='text-align: center; color: #A9A9A9; font-style: italic;'>For the Game. For the World.</h4>", unsafe_allow_html=True)
st.sidebar.header("", divider='rainbow')

# Main Title
st.markdown("<h1 style='text-align: center; font-weight: bold;'>FIFA Dashboard</h1>", unsafe_allow_html=True)
st.divider()

# Players Distribution Section
st.header("Players Distribution")
select_nations = st.multiselect('Select Country:', data['Nationality'].unique())
nations = data['Nationality'].value_counts().reset_index()
nations.columns = ['Nationality', 'Player Count']

# Filter by selected nations
selected_data = nations if not select_nations else nations[nations['Nationality'].isin(select_nations)]

#label data
mean_value_of_Players = data.groupby('Nationality')['Value'].mean()
mean_overall = data.groupby('Nationality')['Overall'].mean()
mean_wage = data.groupby('Nationality')['Wage'].mean()
mean_clause = data.groupby('Nationality')['Release Clause'].mean()

# Merge the calculated means with the selected data
selected_data = selected_data.merge(mean_value_of_Players, on='Nationality', how='left',suffixes=('', '_mean'))
selected_data = selected_data.merge(mean_overall, on='Nationality', how='left', suffixes=('', '_mean'))
selected_data = selected_data.merge(mean_wage, on='Nationality', how='left', suffixes=('', '_mean'))
selected_data = selected_data.merge(mean_clause, on='Nationality', how='left', suffixes=('', '_mean'))
# Choropleth Map
st.plotly_chart(px.choropleth(
    selected_data,
    locations='Nationality',
    locationmode='country names',
    color='Player Count',
    hover_data={
        'Nationality': True,
        'Player Count':True,
        'Value':':.2f',
        'Overall':':.2f',
        'Wage':':.2f',
        'Release Clause':':.2f'
    },
    color_continuous_scale=['#FCDE70','green']
))
st.divider()

# Top 10 Players Section
st.header('Top 10 Players According to')
top_per = st.selectbox('Select Value', options=['Value', 'Overall', 'Wage', 'Release Clause', 'Potential'])

# Create tabs for diagram and table
diagram, table = st.tabs(['Diagram', 'Table'])
top_table = data.sort_values(top_per, ascending=False)[['Name', top_per]].head(10)

with diagram:
    st.plotly_chart(px.bar(top_table, x='Name', y=top_per, color='Name'))

with table:
    st.dataframe(top_table.set_index('Name'))

st.divider()


# Preferred Foot Section
Leg_percentage_chart, Effect_of_legs_chart = st.columns(2)

with Leg_percentage_chart:
    st.header('Percentage of Preferred Leg')
    st.plotly_chart(px.pie(names=data['Preferred Foot'], color_discrete_sequence=['#0F67B1', '#EDE8DC']))

with Effect_of_legs_chart:
    st.header('Effect of the Leg on')
    effect = st.radio('Select Value', ['Skill Moves', 'Potential'], horizontal=True)
    if effect=='Skill Moves':
        foot_skill = data.groupby(['Preferred Foot'])[effect].mean().reset_index()
        st.plotly_chart(
            px.bar(
                foot_skill,
                x='Preferred Foot', 
                y=effect,
                labels={effect: f'Mean {effect}', 'Preferred Foot': 'Preferred Foot'},
                title=f'Average {effect} by Preferred Foot',
                color='Preferred Foot',
                color_discrete_sequence=['#EDE8DC','#0F67B1' ]
            )
        )
    else:
        left_leg=data[data['Preferred Foot']=='Left']
        right_leg=data[data['Preferred Foot']=='Right']
        # Create a figure
        fig = go.Figure()


        # Add the first histogram
        fig.add_trace(go.Histogram(
            x=right_leg['Potential'],
            name='Right leg',
            opacity=0.75,
            marker=dict(color='#0F67B1'),
            nbinsx=30  # Number of bins for the second histogram
        ))

        # Add the second histogram
        fig.add_trace(go.Histogram(
            x=left_leg['Potential'],
            name='left Leg',
            opacity=0.90,  # Adjust opacity to see overlap
            marker=dict(color='#EDE8DC'),
            nbinsx=30, # Number of bins for the first histogram
        ))

        
       

        # Update layout
        fig.update_layout(
            title='Two Histograms in One Figure',
            xaxis_title='Value',
            yaxis_title='Count',
            barmode='overlay'  # Overlay the bars for comparison
        )
        st.plotly_chart(fig)



st.divider()

