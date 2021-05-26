from selenium import webdriver
from time import sleep
import os
import re
import requests
from src.driver import driver
import ast
import requests


def get_info_zara(search_item):
    
    driver.get("https://www.zara.com/es/es/search")
    sleep(5)
    try:
        driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
         
    except: pass
    
    sleep(2)
    driver.find_element_by_css_selector('#search-products-form-combo-input').click()
    driver.find_element_by_class_name("search-products-form__input").send_keys(f"{search_item}")
    sleep(5)
    url_prods = driver.find_elements_by_css_selector("div > section > ul > li")

    total_prod = []
    
    for url in url_prods:
        
        dic_prod = {"url": [] ,"image": [],"product_name": [], "price": []}
    
        dic_prod["url"] = url.find_element_by_css_selector("div > div > a").get_attribute("href")
    
        dic_prod["image"] = url.find_element_by_css_selector("a > div > div > div > img").get_attribute("src")
    
        dic_prod["product_name"] = url.find_element_by_css_selector("div > div > a > span").text
    
        dic_prod["price"] = url.find_element_by_class_name("price__amount").text
    
        total_prod.append(dic_prod)
    
    return total_prod

def get_id_zara(search_item):
    
    driver.get("https://www.zara.com/es/es/search")
    sleep(5)
    try:
        driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
         
    except: pass
    
    sleep(2)
    driver.find_element_by_css_selector('#search-products-form-combo-input').click()
    driver.find_element_by_class_name("search-products-form__input").send_keys(f"{search_item}")
    sleep(5)
    driver.find_element_by_css_selector("#main > article > div > div > div.search-products-view__search-results > section.product-grid > ul > li > div > div > a").click()
    sleep(5)
    driver.find_element_by_class_name("expandable-text__content").text
    

    driver.find_element_by_class_name("product-detail-actions__action-button").click()
    sleep(2)

    ids_prod = driver.find_element_by_css_selector("#theme-modal-container > div > div > div > div > div.modal__body.modal__body--spacer-bottom > div")

    idss_prod = ids_prod.find_elements_by_css_selector("p")
    
    id_prod = [a.text.split("_")[-1] for a in idss_prod]

    id_prod = ["".join([i for i in a if i.isnumeric()]) for a in id_prod]
    
    return id_prod

def get_id_info(search_item):
    products = get_info_zara(search_item)
    for a,product in enumerate(products):
        
        product_name = product["product_name"]
        
        name_ids = get_id_zara(product_name)
     
        products[a]["id_prod"] = name_ids
    
    return products


def get_stores_zara(lat,lng):
  
    loc = {
    "lat":{lat},
    "lng":{lng}}   
    
    stores = "https://www.zara.com/es/es/stores-locator/search"
    
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"}
    
    stores_id = requests.get(stores, params=loc, headers=headers).json()

    store = []

    for i in range(0,len(stores_id)):
    
        id_ = stores_id[i]["id"]
        latitud = stores_id[i]["latitude"]
        longitude = stores_id[i]["longitude"]
        address = stores_id[i]["addressLines"][0]
        days = stores_id[i]["openingHours"]

        week_days_dic = {1:"L", 2:"M", 3:"X", 4:"J", 5:"V", 6:"S", 7:"D"}
        day_hour = {}

        for i in days:
            try:
                wd = week_days_dic[i["weekDay"]]
                open_ = i["openingHoursInterval"][0]["openTime"]
                close = i["openingHoursInterval"][0]["closeTime"]

                day_hour[wd]=[open_,close]

            except:
                pass

        dr_store = {"id": id_,"latitude":latitud ,"longitude": longitude, "address":address, "days": day_hour}
        store.append(dr_store)

    return store

def get_stock_zara(search_terms,lat,lng):
        
    products = get_id_info(search_terms)

    store_info = get_stores_zara(lat, lng)
    store_ids = [element["id"] for element in store_info]

    stock_url = "https://itxrest.inditex.com/LOMOServiciosRESTCommerce-ws/common/1/stock/campaign/V2021/product/part-number/{}"
    headers ={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}
    stock_params = {"physicalStoreId": store_ids}

    urls = [stock_url.format("".join(p["id_prod"]).rjust(11,"0")) for p in products]
        
    for i,product in enumerate(products):
        headers ={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}
        products[i]["stock"] = requests.get(urls[i],params=stock_params,headers=headers).json()
        
    return products