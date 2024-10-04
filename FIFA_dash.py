import streamlit as st
import pandas as pd
import plotly.express as px

data=pd.read_csv("D:\\AI_track\\fifa_eda.csv")
st.sidebar.image("https://play-lh.googleusercontent.com/NcrdWFjmF2GPRlif4xC-9WM4bQXxHjU4yuWVQjsdDh7xtKPc6nVSRhp-iOlFnpuepg")
st.sidebar.html(" <h4 style='text-align: center; color: #A9A9A9; font-style: italic;'>For the Game.For the World.</h4>")
st.sidebar.header("",divider='rainbow')
st.html(" <h1 style='text-align: center;font-style:bold'>FIFA Dashboard</h1>")
st.divider()

st.header("Players Distibution")
select_nations=st.multiselect('Select country:',data['Nationality'].unique())
nations=data['Nationality'].value_counts().reset_index()
nations.columns = ['Nationality', 'Player Count']
if not select_nations:
    selected_data = nations
else:
    selected_data = nations[nations['Nationality'].isin(select_nations)]

st.plotly_chart(px.choropleth(selected_data,
                              locations='Nationality',
                              locationmode='country names',
                              color='Player Count',
                              color_continuous_scale=px.colors.sequential.amp))
st.divider()



top10H=st.header('Top 10 Players according to')
top_per=st.selectbox('Select Value',options=['Value','Overall','Wage','Release Clause','Potential'])
tab1,tab2=st.tabs(['Diagram','Table'])
top_table=data.sort_values(top_per,ascending=False)[['Name',top_per]].head(10)
with tab1:
    st.plotly_chart(px.bar(top_table,x='Name',y=top_per,color='Name'))
with tab2:
    st.dataframe(top_table.set_index('Name'))
st.divider()


col1,col2=st.columns(2)

with col1:
    st.header('The value per Nations')
    st.plotly_chart(px.scatter(data,x='Nationality',y='Value'))
with col2:
    st.header('The value per')
    st.header('Clubs')
    st.plotly_chart(px.scatter(data,x='Club',y='Value',height=500))
st.divider()


col11,col22=st.columns(2)
with col11:
    st.header('Percentage of Preffered leg')
    st.plotly_chart(px.pie(names=data['Preferred Foot'],color_discrete_sequence=['#0F67B1','#EDE8DC']))

with col22:
    st.header('Effect of the leg on')
    effect=st.radio('Select Value',['Skill Moves','Potential'],horizontal=True)
    Foot_skill=data.groupby(['Preferred Foot',effect]).size().unstack()
    st.plotly_chart(px.bar(Foot_skill,labels={effect: effect, 'Preferred Foot': 'Preferred Foot', 'value':'Count'},barmode='group'))
st.divider()


st.header('The proportion of the positions')
st.plotly_chart(px.pie(names=data['Position']))


