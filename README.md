# Inditex-Recommender 

![Imagen_text](https://github.com/Carmen-r/Inditex-Recommender/blob/main/image/port_inditex.jpg)

## GOAL ⚡️

This is the final [Ironhack][id] project. Among other things, it is designed to use some of the tools used throughout the course.

[id]: https://www.ironhack.com/es "Ironhack"

Many times we have bought a garment for a high price that later we see in other stores for a lower price, that is why the need for an Inditex recommender has arisen.

The main objective of this idea is to make a comparison between garments from different stores, i.e. when you want to buy a certain product you can see the different price options, available stock, store closest to your location and an image of the product. Which simplifies the search time in different stores, and the most important thing is to be able to get the updated stock. 

## WHAT IS NEED? TOOLS ⚙️

About the data and tools, I have used: 

[Selenium][id1] to extract the product information such as ID, URL, image and price.

[id1]: https://selenium-python.readthedocs.io/ "Selenium"

[API][id2] to get information about the store such as ID, street and information about the opening hours.

[id2]: https://pypi.org/project/ApiDoc/ "API"

[API][id2] for updated stock information. Extract the id of the product and the stores, in addition to the available units.

[id2]: https://pypi.org/project/ApiDoc/ "API"

[Streamlit][id3] to write the type of product and the location display the garment I have selected.

[id3]: https://streamlit.io/ "Streamlit"


## LIBRARIES 🤓

[Selenium][id1]

[Pandas][id4]

[id4]: https://pandas.pydata.org/docs/ "Pandas"

[Numpy][id5]

[id5]: https://numpy.org/doc/stable/user/whatisnumpy.html "Numpy"

[Requests][id6]

[id6]: https://docs.python-requests.org/en/master/ "Requests"

[Geocoder][id7]

[id7]: https://pypi.org/project/geocoder/ "Geocoder"

[Folium][id8]

[id8]: https://pypi.org/project/folium/ "Folium"


## STEPS 🚀

The first step was to make a project plan and to analyze which tools we were going to use to extract all the data, as well as to study its feasibility. 

Then, after handling the tools I was going to use, I extracted all the necessary information about products of the two stores with selenium, so that when I wanted to select a white t-shirt I could have the product ID, name, price, image and URL.

Thirdly, I used an internal inditex API through which I obtained information about the store: the store ID, latitude and longitude, street name, as well as the opening hours.


Finally, with an internal API common to all Inditex I obtained information about the stock availability, which had data about the ID of the store, and the stock availability at that moment.

