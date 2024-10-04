import streamlit as st
import pandas as pd
import plotly.express as px

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

# Choropleth Map
st.plotly_chart(px.scatter_geo(
    selected_data,
    locations='Nationality',
    locationmode='country names',
    color='Player Count',
    color_continuous_scale=px.colors.sequential.amp
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

# Scatter Plots Section
Value_per_Nation_chart, Value_per_Club_chart = st.columns(2)

with Value_per_Nation_chart:
    st.header('The Value per Nation')
    nation_value = data.groupby('Nationality')['Value'].mean().reset_index()
    st.plotly_chart(px.scatter(nation_value, x='Nationality', y='Value'))

with Value_per_Club_chart:
    st.header('The Value per Club')
    club_value = data.groupby('Club')['Value'].mean().reset_index()
    st.plotly_chart(px.bar(club_value, x='Club', y='Value'))

st.divider()

# Preferred Foot Section
Leg_percentage_chart, Effect_of_legs_chart = st.columns(2)

with Leg_percentage_chart:
    st.header('Percentage of Preferred Leg')
    st.plotly_chart(px.pie(names=data['Preferred Foot'], color_discrete_sequence=['#0F67B1', '#EDE8DC']))

with Effect_of_legs_chart:
    st.header('Effect of the Leg on')
    effect = st.radio('Select Value', ['Skill Moves', 'Potential'], horizontal=True)
    foot_skill = data.groupby(['Preferred Foot', effect]).size().unstack()
    st.plotly_chart(px.bar(foot_skill, labels={effect: effect, 'Preferred Foot': 'Preferred Foot', 'value': 'Count'}, barmode='group'))

st.divider()

# Position Distribution Section
st.header('The Proportion of the Positions')
count_pos = data.groupby('Position').size()

# Polar Bar Chart
fig = px.bar_polar(
    r=count_pos.values, 
    theta=count_pos.index, 
    color=count_pos.index,  
    title="Count of Each Position", 
    template="plotly_dark", 
    labels={'color': 'Positions'}
)

# Customize layout of polar chart
fig.update_polars(
    radialaxis_showline=False,  
    radialaxis_ticks='',        
    radialaxis_showticklabels=False
)

st.plotly_chart(fig)
