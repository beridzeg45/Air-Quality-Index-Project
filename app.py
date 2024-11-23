#imports and defining data
import streamlit as st
import pandas as pd
import plotly.express as px


#define daatframe
all_cities_df=pd.read_csv('all_cities_df (cleaned).csv')
all_cities_df['color_category'] = pd.qcut(all_cities_df['AQI'], q=20, labels=False)
filtered_data=all_cities_df[all_cities_df['Year']==2023]
all_cities=list(all_cities_df['City'].unique())


#graphs

def return_scatter_mapbox():
    fig = px.scatter_mapbox(
    data_frame=filtered_data,
    lat="Lat",
    lon="Lon",
    color="color_category",
    size_max=10,
    color_continuous_scale='RdYlGn_r',
    title="Scatter Mapbox of Cities",
    zoom=2,
    hover_name='City',
    hover_data={'Lat':False,'Lon':False,'AQI':True,'color_category':False, 'Year':False},
    animation_frame='Year'
    )

    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(height=500,width=1000,template='plotly_white',margin=dict(l=0,r=0,t=30,b=0))
    fig.update_layout(title=dict(text='Air Qulaity Index Map (2023)',font_family='Arial Black'))
    fig.update_layout(coloraxis_colorbar=dict(orientation='h', xanchor='center', x=0.5, y=-0.2, thickness=10, showticklabels=False,title='AQI'))

    return fig

def return_choropleth_map():
    grouped=all_cities_df.groupby(['Year', all_cities_df['City'].str.split(' ').str[-1]])['AQI'].mean().round().reset_index()
    grouped=grouped.replace('Kingdom',' United Kingdom')
    fig=px.choropleth(data_frame=filtered_data,
              locations='City',locationmode='country names',
              color='color_category',color_continuous_scale='RdYlGn_r',
              #projection="natural earth",scope='world',
              animation_frame='Year',
              hover_name='City',
            hover_data={'Year':False, 'City':False,'AQI':True, 'color_category':False},

              )

    fig.update_layout(height=500,width=1000,template='plotly_white',margin=dict(l=0,r=0,t=30,b=0),geo=dict(showframe=False,))
    fig.update_layout(title=dict(text='Average Air Quality Index By Country (2023)',font_family='Arial Black'))
    fig.update_layout(coloraxis_colorbar=dict(orientation='h', xanchor='center', x=0.5, y=-0.2, thickness=10, showticklabels=False,title='AQI'))
    fig.update_traces(marker_line_width=0.1)

    return fig

def return_bar_plot(selected_values):
    filtered_cities_data=all_cities_df[all_cities_df['City'].isin(selected_values)]
    filtered_cities_data=filtered_cities_data.drop_duplicates(subset=['Year','City'])

    fig=px.bar(filtered_cities_data,x='Year',y='AQI',color='City',barmode='group',text='AQI')
    fig.update_layout(title=dict(text='AQI By Year',font_family='Arial Black'))

    return fig



# Streamlit
st.set_page_config(
    layout='wide',
    page_title='Air Quality Index - Python Project By Giorgi Beridze',
    page_icon='AQI',
    initial_sidebar_state='auto'
)

# Create two columns for the maps
col_1, col_2 = st.columns(2)

with col_1:
    scatter_mapbox_fig = return_scatter_mapbox()
    st.plotly_chart(scatter_mapbox_fig, use_container_width=True)

with col_2:
    choropleth_fig = return_choropleth_map()
    st.plotly_chart(choropleth_fig, use_container_width=True)

# Bar chart below maps

input_values_list=['Miami, USA', 'Tbilisi, Georgia','Rome, Italy','Santiago, Chile','Munich, Germany','Delhi, India']
input_values_list=st.multiselect(label='',placeholder='Type city name (or multiple names for comparison)',options=['']+all_cities)
bar_chart_fig = return_bar_plot(selected_values=input_values_list)
st.plotly_chart(bar_chart_fig, use_container_width=True)





