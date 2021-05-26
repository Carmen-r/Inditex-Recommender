from time import sleep
from src.driver import driver
import os
import re
import ast
import requests


def get_info_pull(search_item):
    
    driver.get("https://www.pullandbear.com/es/")
    sleep(5)
    try:
        driver.find_element_by_id("onetrust-accept-btn-handler").click()
        sleep(2)
        driver.find_element_by_id("saveStore").click()
        sleep(5)
        driver.find_element_by_css_selector("#subhome-cont > div.m-genre-selector > div:nth-child(1)").click()
        
        
    except: pass
    
    sleep(5)
    driver.find_element_by_css_selector('#secondary-nav > div.menu.menu-search > button').click()
    sleep(2)
    driver.find_element_by_css_selector("#empathy-x > header > div > div > input").send_keys(f"{search_item}")
    sleep(5)
    url_prods = driver.find_elements_by_css_selector("section > section > article")

    total_prod = []
    
    for url in url_prods:
        
        dic_prod = {"url": [] ,"image": [],"product_name": [], "price": []}
    
        dic_prod["url"] = url.find_element_by_css_selector("section > section > article > a").get_attribute("href")
         
        dic_prod["image"] = url.find_element_by_css_selector("section > section > article > a > section > img").get_attribute("src")
    
        dic_prod["product_name"] = url.find_element_by_css_selector("#ebx-grid > article > a > h1").text
    
        dic_prod["price"] = url.find_element_by_css_selector("#ebx-grid > article > a > p > strong").text
    
        total_prod.append(dic_prod)
        
   
    return total_prod



def get_id_pull(search_item):
    
    driver.get("https://www.pullandbear.com/es/")
    sleep(5)
    try:
        driver.find_element_by_id("onetrust-accept-btn-handler").click()
        sleep(2)
        driver.find_element_by_id("saveStore").click()
        sleep(1)
        driver.find_element_by_css_selector("#subhome-cont > div.m-genre-selector > div:nth-child(1)").click()
    
    except: pass 
    
    sleep(5)
    driver.find_element_by_css_selector("#secondary-nav > div.menu.menu-search > button").click()
    sleep(2)
    driver.find_element_by_css_selector("#empathy-x > header > div > div > input").send_keys(f"{search_item}")
    sleep(5)
    driver.find_element_by_css_selector("#ebx-grid > article > a > h1").click()
    description = driver.find_element_by_css_selector("#productCard > div > div.c-product-info > div.c-product-info--description > div.c-product-info--description-description > span").text
    print(description)
    

    ids_prod = driver.find_elements_by_css_selector("#productCard > div > div.c-product-info > div.c-product-info--description > div.c-product-info--description-header > span")
    id_ = driver.find_elements_by_css_selector("#productCard > div > div.c-product-info > div.c-product-info--header > div.product-card-color-selector.desktop-inline > div.product-card-color-selector--popup > div > div.product-card-color-selector--popup-colors-color.selected > img")
    
    for my_href in id_:
            d = (my_href.get_attribute("data-color-id"))

    type(d)
    id_prod = [a.text.replace("Ref. ", "") for a in ids_prod][0]
    id_prod =[id_prod + d]
    return id_prod

def get_id_info(search_item):
    products = get_info_pull(search_item)
    for a,product in enumerate(products):
        
        product_name = product["product_name"]
        
        name_ids = get_id_pull(product_name)
     
        products[a]["id_prod"] = name_ids
    
    return products

def get_store_pull(lat,lng):
  
    loc = {
    "lat":{lat},
    "lng":{lng}}   
    
    stores = f"https://www.pullandbear.com/itxrest/2/bam/store/24009400/physical-store?favouriteStores=true&lastStores=false&closerStores=true&latitude={lat}&longitude={lng}&min=0&max=15&receiveEcommerce=true&countryCode=ES&languageId=-5&appId=1"
    
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"}
    
    stores_id = requests.get(stores, params=loc, headers=headers).json()
    stores_ = stores_id["closerStores"]
    store = []
    
    for i in stores_:
        for k,v in i.items():
            if k == "id":
                id_ = v
            elif k == "latitude":
                latitud = v
            elif k == "longitude":
                longitude = v
            elif k == "addressLines":
                address = v
           
        

        
        dr_store = {"id": id_,"latitude":latitud ,"longitude": longitude, "address": address}
        store.append(dr_store)
        
    return store
    

def get_stock_pull(search_item,lat,lng):
        

    products = get_id_info(search_item)

        
    store_info = get_store_pull(lat, lng)
    store_ids = [element["id"] for element in store_info]

    stock_url = "https://itxrest.inditex.com/LOMOServiciosRESTCommerce-ws/common/1/stock/campaign/V2021/product/part-number/{}"
    headers ={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}
    stock_params = {"physicalStoreId": store_ids}

    urls = [stock_url.format("".join(p["id_prod"]).rjust(11,"0")) for p in products]
    print(urls)
        
    for i,product in enumerate(products):
        headers ={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}
    
        products[i]["stock"] = requests.get(urls[i],params=stock_params,headers=headers).json()
        
    return products
