import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

st.title('Uber pickups in NYC')
st.title('Create by')
'Narubet Intraprasit'

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')

#data
if st.checkbox('Show raw data'):
    st.subheader('Raw data Frame')
    st.write(data)

if st.checkbox('Histogram Chart'):
    st.subheader('Number of pickups by hour')
    hist_values = np.histogram(
        data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

    st.bar_chart(hist_values)


#st.subheader('Map of all pickups')
#st.map(data)

#hour_to_filter = 17
#hour_to_filter = st.slider('hour', 0, 23, 17)
#filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
#st.subheader(f'Map of all pickups at {hour_to_filter}:00')
#st.map(filtered_data)
#hour_to_filter = st.slider('hour', 0, 23, 17)


#if st.checkbox('Show raw data'):
    #st.subheader('Raw data')
    #st.write(data)


#if st.checkbox('show mapp'):
    #st.write(filtered_data)
    #st.map(filtered_data)



# 2
# 5
#st.header(f"Count_button clicked: {st.session_state.count_button}")
if "count_button" not in st.session_state:
    st.session_state.count_button = 0

if st.button("Run it again"):
    st.session_state.count_button += 1

if st.button("Reset"):
    st.session_state.count_button = 0

st.header(f"Count_button clicked: {st.session_state.count_button}")


# 4

#streamlit run uber_pickups.py


# Date filter input
min_date = data[DATE_COLUMN].dt.date.min()
max_date = data[DATE_COLUMN].dt.date.max()

date_range = st.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    format="MM.DD.YYYY"
)

# Filter data by selected date range
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_data = data[
        (data[DATE_COLUMN].dt.date >= start_date) &
        (data[DATE_COLUMN].dt.date <= end_date)
    ]
else:
    filtered_data = data  # fallback

st.subheader('Filtered raw data')
st.write(filtered_data)

#----------------
hour_range = st.slider(
    "Select pickup hour range",
    min_value=0,
    max_value=23,
    value=(0, 23),
    format="%02d:00"
)

filtered_data = filtered_data[
    filtered_data[DATE_COLUMN].dt.hour.between(hour_range[0], hour_range[1])
]

#-----------
if st.checkbox("Show map with pydeck"):
    st.subheader('Map of pickups in selected date range')
    st.pydeck_chart(
        pdk.Deck(
            map_style=None,
            initial_view_state=pdk.ViewState(
                latitude=40.73,
                longitude=-73.935242,
                zoom=11,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    "HexagonLayer",
                    data=filtered_data,
                    get_position="[lon, lat]",
                    radius=200,
                    elevation_scale=4,
                    elevation_range=[0, 1000],
                    pickable=True,
                    extruded=True,
                ),
                pdk.Layer(
                    "ScatterplotLayer",
                    data=filtered_data,
                    get_position="[lon, lat]",
                    get_color="[200, 30, 0, 160]",
                    get_radius=200,
                ),
            ],
        )
    )



#---------


