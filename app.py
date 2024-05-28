import streamlit as st
import pandas as pd
import altair as alt

# Load the data
df = pd.read_csv('music_data.csv')

# Title
st.title('Music Data Dashboard')

# Sidebar for filtering
st.sidebar.header('Filter Options')
selected_artist = st.sidebar.selectbox('Select Artist', df['artist(s)_name'].unique())
selected_year = st.sidebar.selectbox('Select Year', df['released_year'].unique())

# Filter data based on selections
filtered_df = df[(df['artist(s)_name'] == selected_artist) & (df['released_year'] == selected_year)]

# Display filtered data
st.subheader(f'Data for {selected_artist} in {selected_year}')
st.write(filtered_df)

# Create charts
# Streams by Month
streams_by_month = (
    filtered_df.groupby('released_month')['streams'].sum().reset_index()
)

streams_chart = alt.Chart(streams_by_month).mark_bar().encode(
    x='released_month:O',
    y='streams:Q',
    tooltip=['released_month', 'streams']
).properties(
    title='Total Streams by Month'
)

st.altair_chart(streams_chart, use_container_width=True)

# Danceability and Energy
dance_energy_chart = alt.Chart(filtered_df).mark_circle(size=60).encode(
    x='danceability_%:Q',
    y='energy_%:Q',
    color='artist(s)_name:N',
    tooltip=['track_name', 'danceability_%', 'energy_%']
).interactive().properties(
    title='Danceability vs Energy'
)

st.altair_chart(dance_energy_chart, use_container_width=True)

# Acousticness over time
acousticness_chart = alt.Chart(filtered_df).mark_line().encode(
    x='released_day:T',
    y='acousticness_%:Q',
    color='artist(s)_name:N',
    tooltip=['track_name', 'acousticness_%']
).interactive().properties(
    title='Acousticness Over Time'
)

st.altair_chart(acousticness_chart, use_container_width=True)

# Display raw data at the end
st.subheader('Raw Data')
st.write(df)
