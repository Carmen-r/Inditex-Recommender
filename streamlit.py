import streamlit as st
from selenium import webdriver
import geocoder
from time import sleep
from PIL import Image
import os
import re
import pandas as pd
import requests
import folium
import ast
import pandas as pd
import numpy as np
from src.driver import driver
from src.todas_zara import *
from src.todas_pull import *
from streamlit_folium import folium_static
from folium import Choropleth, Circle, Marker, Icon, Map
st.set_page_config(layout="wide")

col7,col8,col9=st.beta_columns([1, 6, 1])

with col7:
    st.write("")
with col8:
    st.markdown("""
# Recommender Inditex
""")
with col9:
    st.write("")
    
col1,col2,col3=st.beta_columns([1, 6, 1])

with col1:
    st.write("")
with col2:
    image = Image.open('image/proj_inditex.jpg')
    st.image(image, width=None)
with col3:
    st.write("")

col5,col6=st.beta_columns(2)

st.header("¿Dónde estás?")
location = st.text_input("Escribe una calle:")

if st.button("Continuar"):
    with col5:
        st.write("### Zara")

        loc = geocoder.osm(location)
        cordenadas = loc.latlng
        lat = cordenadas[0]
        lng = cordenadas[1]

        locat = get_stores_zara(lat,lng)
        df2 = pd.DataFrame(locat)
    

        map_1 = folium.Map(location = [lat,lng], zoom_start = 12)

        icono = Icon(color = "blue",
             prefix = "fa",
             icon = "fa-map-marker",
             icon_color = "white",)

        loc = {"location":[lat,lng],
             "tooltip": "Mi ubicación"}
   
        marker_ = Marker(**loc, icon = icono).add_to(map_1)

        for i,row in df2.iterrows():
        
            location_ = {"location" : [row["latitude"],row["longitude"]], "tooltip" : row["id"]}
        
            icon = Icon(color = "yellow",
                    prefix = "fa",
                    icon = "shopping-bag",
                    icon_color = "black")

            Marker(**location_,icon=icon,popup=row["address"]).add_to(map_1)

        folium_static(map_1)

    with col6:
        st.write("### Pull & Bear")
        loc = geocoder.osm(location)
        cordenadas = loc.latlng
        lat = cordenadas[0]
        lng = cordenadas[1]

        locat = get_store_pull(lat, lng)
        df3 = pd.DataFrame(locat)
        
    

        map_2 = folium.Map(location = [lat,lng], zoom_start = 12)

        icono = Icon(color = "blue",
                prefix = "fa",
                icon = "fa-map-marker",
                icon_color = "white",)

        loc = {"location":[lat,lng],
            "tooltip": "Mi ubicación"}
   
        marker_ = Marker(**loc, icon = icono).add_to(map_2)
        

        for i,row in df3.iterrows():
        
            location_ = {"location" : [row["latitude"],row["longitude"]], "tooltip" : row["id"]}
        
            icon = Icon(color = "yellow",
                    prefix = "fa",
                    icon = "shopping-bag",
                    icon_color = "black")
            
            Marker(**location_,icon=icon,popup=row["address"]).add_to(map_2)

        folium_static(map_2)

        for i,row in df3.iterrows():
        
            location_ = {"location" : [row["latitude"],row["longitude"]], "tooltip" : row["id"]}
        
            icon = Icon(color = "yellow",
                    prefix = "fa",
                    icon = "shopping-bag",
                    icon_color = "black")


st.header("¿Qué quieres comprar?")
search_items = st.text_input("Escribe una prenda:")
if st.button("Aceptar"):
    with col5:

        loc = geocoder.osm(location)
        cordenadas = loc.latlng
        lat = cordenadas[0]
        lng = cordenadas[1]

        prod_stock = get_stock_zara(search_items,lat,lng)

        for product in prod_stock:

            #Image
            img= product["image"]
            st.image(img, width=300)

            #Product Name
            st.write(product["product_name"])
        
            #Product Price
            st.write(product["price"])

            #Stock
            for stock in product["stock"]["stocks"]:
            
                size_stk = []

                for sizeStock in stock["sizeStocks"]:

                    size_stock = {}

                    #Product size
                    size_ = {101:"XS", 102:"S", 103:"M", 104:"L", 105:"XL", 106:"XXL",125:"S-M",131:"L-XL"}
                    if sizeStock["size"] in size_:
                        sizeStock["size"] = size_[sizeStock["size"]]
                
                        size_stock["Talla"] = sizeStock["size"]
                    else:
                        size_stock["Talla"] = sizeStock["size"]

                    #Normalize quantity:
                    if sizeStock["quantity"] <= 0:
                        size_stock["Stock"] = "El producto no está disponible 😭"
                    elif sizeStock["quantity"] == 1:
                        size_stock["Stock"] = "Quedan pocos productos 👀"
                    
                    elif sizeStock["quantity"] >= 2:
                        size_stock["Stock"] = "El producto está disponible 😁"
                    
                    elif sizeStock["quantity"] >= 4:
                        size_stock["Stock"] = "El producto está disponible 🥳"


                    #Check if there is stock
                    if size_stock["Stock"] == "Sin existencias":
                        pass
                    else: 
                        size_stk.append(size_stock)
            

                if len(size_stk) > 0:
                    st.write("id tienda:",stock["physicalStoreId"])
                    df1 = pd.DataFrame(size_stk)
                    st.table(df1)
    
    
    

    with col6:
         loc = geocoder.osm(location)
         cordenadas = loc.latlng
         lat = cordenadas[0]
         lng = cordenadas[1]

         stock = get_stock_pull(search_items,lat,lng)

         for product in stock:
    
            #Image
            img= product["image"]
            st.image(img, width=300)

            #Product Name
            st.write(product["product_name"])
            
            #Product Price
            st.write(product["price"])

            #Stock
            for stock in product["stock"]["stocks"]:
                
                size_stk = []

                for sizeStock in stock["sizeStocks"]:

                    size_stock = {}

                    #Product size
                    size_ = {101:"XS", 102:"S", 103:"M", 104:"L", 105:"XL", 106:"XXL",125:"S-M",131:"L-XL"}
                    if sizeStock["size"] in size_:
                        sizeStock["size"] = size_[sizeStock["size"]]
                    
                        size_stock["Talla"] = sizeStock["size"]
                    else:
                        size_stock["Talla"] = sizeStock["size"]

                    #Normalize quantity:
                    if sizeStock["quantity"] <= 0:
                        size_stock["Stock"] = "El producto no está disponible 😭"
                    elif sizeStock["quantity"] == 1:
                        size_stock["Stock"] = "Quedan pocos productos 👀"
                        
                    elif sizeStock["quantity"] >= 2:
                        size_stock["Stock"] = "El producto está disponible 😁"
                        
                    elif sizeStock["quantity"] >= 4:
                        size_stock["Stock"] = "El producto está disponible 🥳"


                    #Check if there is stock
                    if size_stock["Stock"] == "Sin existencias":
                        pass
                    else: 
                        size_stk.append(size_stock)
                

                if len(size_stk) > 0:
                    st.write("id tienda:",stock["physicalStoreId"])
                    df4 = pd.DataFrame(size_stk)
                    st.table(df4)




