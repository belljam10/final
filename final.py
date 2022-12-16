"""Class: CS230--Section XXX 
Name: Isabella Jamnaprasad
Description: (Give a brief description for Exercise name--See below)
I pledge that I have completed the programming assignment independently. 
I have not copied the code from a student or any source.
I have not given my code to any student. 
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pydeck as pdk
from PIL import Image
from streamlit_option_menu import option_menu


def getData():
    data = pd.read_csv("Skyscrapers.csv")

    # remove redundant data
    data.drop(columns=["Height"])
    # rename columns
    data = data.rename(columns={'RANK': 'rank', 'NAME': 'name', 'CITY': 'city', 'Full Address': 'address',
                                'Latitude': 'lat', 'Longitude': 'lon', 'COMPLETION': 'complete',
                                'FLOORS': 'fl', 'MATERIAL': 'mat', 'FUNCTION': 'func'})
    # remove potential strings from numeric values
    data = data.dropna(subset=['fl', 'complete'])
    data.fl = data.fl.astype(int)
    data.complete = data.complete.astype(int)
    data.Feet = data.Feet.map(lambda x: x.strip(' ft').replace(',', '')).astype(float)
    data.Meters = data.Meters.map(lambda x: x.rstrip(' m').replace(',', '')).astype(float)
    data.lat = data.lat.astype(float)
    data.lon = data.lon.astype(float)
    # return data
    return data


def getMap(data):
    dfMap = data[['lat', 'lon']]
    st.title("Cities with Skyscrapers Throughout the World")
    st.write("On this webpage, there's a map that allows you to see all the skyscrapers throughout the world and "
             "each city they're in. Enjoy!")
    st.map(dfMap)


def coolMap(data, lat, lon):
    dfMap = data[['lat', 'lon']]
    st.pydeck_chart(pdk.Deck(map_style=None,
                             initial_view_state=pdk.ViewState(
                                 latitude=lat,
                                 longitude=lon,
                                 zoom=10,
                                 pitch=20,
                             ),
                             layers=[
                                 pdk.Layer(
                                     'HexagonLayer',
                                     data=dfMap,
                                     radius=150,
                                     get_position='[lon,lat]',
                                     elevation_scale=10,
                                     elevation_range=[100, 500],
                                     pickable=True,
                                     extruded=True, ),
                                 pdk.Layer(
                                     'ScatterplotLayer',
                                     data=dfMap,
                                     get_position='[lon,lat]',
                                     get_color='[200, 30, 10, 160]',
                                     get_radius=100,
                                     ), ], ))


def getSearch(data):
    search_res = pd.DataFrame()
    city = st.checkbox("City", value=False, key=1)
    material = st.checkbox("Material", value=False, key=2)
    function = st.checkbox("Function", value=False, key=3)
    if city:
        city_search = st.text_input("City")
    else:
        city_search = ''
    if material:
        mat_search = st.text_input("Material")
    else:
        mat_search = ''
    if function:
        func_search = st.text_input("Function")
    else:
        func_search = ''
    if st.button("search"):
        if city:
            if city_search != '':
                search_res = data[data['city'].str.contains(city_search, case=False, na=False)]
            else:
                st.warning('Please enter a city')
        elif material:
            if mat_search != '':
                search_res = data[data['mat'].str.contains(mat_search, case=False, na=False)]
            else:
                st.warning('Please enter a material')
        elif function:
            if func_search != '':
                search_res = data[data['func'].str.contains(func_search, case=False, na=False)]
            else:
                st.warning('Please enter a function')
        else:
            pass
        st.write("{} Skyscrapers".format(str(search_res.shape[0])))
        st.dataframe(search_res)


def getMaterials(data):
    df = data
    df['Steel'] = np.where(df.mat.str.contains('steel'), 1, 0)
    df['Concrete'] = np.where(df.mat.str.contains('concrete'), 1, 0)
    df['Composite'] = np.where(df.mat.str.contains('composite'), 1, 0)
    df = df.drop(columns=['mat'])
    st.write(df)
    materials = df[['Steel', 'Concrete', 'Composite']]
    materials = materials.sum().rename('Material Count')
    fig, ax = plt.subplots()
    plt.title('Bar Graph of Skyscraper Materials')
    plt.xlabel('Materials')
    plt.ylabel('Count')
    plt.xticks(rotation=60)
    plt.bar(materials.index, materials)
    st.pyplot(fig)
    st.write(materials)


def getTimeline(data, yearsRange):
    df = data[data.complete >= yearsRange[0]]
    df = df[df.complete <= yearsRange[1]]
    avg = df.groupby('complete').mean()
    feet = st.checkbox("Feet", value=False, key=1)
    meters = st.checkbox("Meters", value=False, key=2)
    if feet:
        fig, ax = plt.subplots()
        plt.bar(avg.index, avg.Feet)
        plt.xlabel("Year")
        plt.ylabel("feet")
        st.pyplot(fig)
    elif meters:
        fig, ax = plt.subplots()
        plt.bar(avg.index, avg.Meters)
        plt.xlabel("Year")
        plt.ylabel("Meters")
        st.pyplot(fig)
    else:
        pass


def getFunc(data):
    df = data
    df['Office'] = np.where(df.func.str.contains('office'), 1, 0)
    df['Residential'] = np.where(df.func.str.contains('residential'), 1, 0)
    df['Hotel'] = np.where(df.func.str.contains('hotel'), 1, 0)
    df['Retail'] = np.where(df.func.str.contains('retail'), 1, 0)
    df['Apartments'] = np.where(df.func.str.contains('serviced apartments'), 1, 0)
    df['Other'] = np.where(df.func.str.contains('other'), 1, 0)
    df = df.drop(columns=['func'])
    st.write(df)
    functions = df[['Office', 'Residential', 'Hotel', 'Retail', 'Apartments', 'Other']]
    functions = functions.sum().rename('Function Count')
    fig, ax = plt.subplots()
    plt.title('Bar Graph of Skyscraper Functions')
    plt.xlabel('Functions')
    plt.ylabel('Count')
    plt.xticks(rotation=60)
    plt.bar(functions.index, functions)
    st.pyplot(fig)
    st.write(functions)


def main():
    data = getData()
    img = Image.open('skyscrapers2.jpg')

    with st.sidebar:
        chose = option_menu("Learn more about Skyscrapers!",
                            ["About",
                             "Check out the Map!",
                             "What Skyscrapers are in your Favorite City?",
                             "How are these Skyscrapers Made?",
                             "How have Skyscrapers Changed Throughout the Years?",
                             "Why are these Skyscrapers here?",
                             "Click for More Information on Skyscrapers!"],
                            icons=['house', 'globe', 'building', 'bar-chart-line-fill', 'graph-up', 'layers-half',
                                   'info-lg'],
                            menu_icon='app-indicator', default_index=0,
                            styles={
                                "container": {"padding": "5!important", "background-color": "#fafafa"},
                                "icon": {"color": "#00BFFF", "font-size": "25px"},
                                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
                                             "--hover-color": "#eee"},
                                "nav-link-selected": {"background-color": "#87CEFA"},
                            }, )

    if chose == "About":
        st.markdown('<p class="font">All About Skyscrapers!</p>', unsafe_allow_html=True)
        st.markdown(""" <style> .font {font-size:42px ; font-family: 'Cooper Black'; color: #87CEFA;}</style>""",
                    unsafe_allow_html=True)
        st.write("Welcome to the homepage! On this website you'll learn all about skyscrapers throughout the world. "
                 "I hope you enjoy!")
        st.image(img, width=700)
        st.write("By: Isabella Jamnaprasad")
    elif chose == "Check out the Map!":
        getMap(data)
        st.header("Check out this 3D Map!")
        st.write("Pick a city from the options below to see some of the skyscrapers on the map in 3D:")
        Dubai = st.checkbox("Dubai", value=False, key=1)
        NY = st.checkbox("New York", value=False, key=2)
        Chi = st.checkbox("Chicago", value=False, key=3)
        Tia = st.checkbox("Tianjin", value=False, key=4)
        if Dubai:
            lat = 25.2694
            lon = 55.3087
            coolMap(data, lat, lon)
        elif NY:
            lat = 40.7146
            lon = -74.0071
            coolMap(data, lat, lon)
        elif Chi:
            lat = 41.8842
            lon = -87.6324
            coolMap(data, lat, lon)
        elif Tia:
            lat = 39.1284
            lon = 117.1851
            coolMap(data, lat, lon)

    elif chose == "What Skyscrapers are in your Favorite City?":
        st.title("Filter Through Your Favorites!")
        st.write("On this webpage, you'll be able to select an option to filter the data. "
                 "The options listed are City, Material, and Function. You'll check the option you"
                 " want to filter, then type in the specific filter.")
        st.write("For Example: If I check City, and type Dubai, a list of all the skyscrapers in Dubai will appear.")
        st.write("Try it out for yourself!")
        getSearch(data)
    elif chose == "How are these Skyscrapers Made?":
        st.title("Materials in Our Skyscrapers")
        st.write("On this webpage, you can find out what the main materials used in Skyscrapers are, and what's used"
                 "most in building these magnificent buildings!")
        getMaterials(data)
    elif chose == "How have Skyscrapers Changed Throughout the Years?":
        st.title("Height of Skyscrapers Overtime")
        st.write("On this webpage you can move the slide to select a year range, this will modify the "
                 "graph in accordance with the year range you set. With this graph you'll learn"
                 "about how the height of skyscrapers has changed throughout the years.")
        start = data.complete.min()
        end = data.complete.max()
        yearsRange = st.slider("Set the Year Range to Graph", int(start), int(end), (int(start), int(end)), step=1)
        getTimeline(data, yearsRange)
    elif chose == "Why are these Skyscrapers here?":
        st.title("Function of these Skyscrapers")
        st.write("On this webpage, you can learn about why these skyscrapers were built, and what purpose"
                 "they serve in the city they're in.")
        getFunc(data)
    elif chose == "Click for More Information on Skyscrapers!":
        st.write("This wepbage contains all the information regarding the skyscrapers on this website."
                 "Thanks for visiting!")
        st.write(data)


main()
