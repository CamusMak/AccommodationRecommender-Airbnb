from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import html5lib

import re
import time
import os

import pandas as pd
import numpy as np
import datetime as dt

from operator import itemgetter

def content_scraper(df,path_to_save):


    
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    
    close_translate_button_xpath = '/html/body/div[10]/section/div/div/div[2]/div/div[1]/button'

    item_title_xpath = '/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[1]/div[1]/div/div/div/div/div/section/div[1]/span/h1'
    item_review_xpath = '/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[1]/div[1]/div/div/div/div/div/section/div[2]/div[1]/span[1]/span[2]'
    item_ratings_xpath = '/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[1]/div[1]/div/div/div/div/div/section/div[2]/div[1]/span[1]/span[3]/button'
    host_level_xpath = '/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[1]/div[1]/div/div/div/div/div/section/div[2]/div[1]/span[3]/span[2]'
    
    location_xpath  = '/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[1]/div[1]/div/div/div/div/div/section/div[2]/div[1]/span[5]/button/span'
    
    guest_xpath = '/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/div/div/div[1]/ol/li[1]/span[1]'
    bedrooms_xpath = '/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/div/div/div[1]/ol/li[2]/span[2]'
    beds_xpath = '/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/div/div/div[1]/ol/li[3]/span[2]'
    baths_xpath = '/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/div/div/div[1]/ol/li[4]/span[2]'
    
    price_xpath = '/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div[1]/div[1]/div/span/span'
    price_review_xpath = '/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div[1]/div[2]/span/span[2]'
    price_ratings_xpath = '/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div[1]/div[2]/span/span[3]'
    item_unit_xpath = '/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div[1]/div/div/span/div/span[2]'
    
    show_desciption_xpath = '/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[1]/div/div[3]/div/div[2]/div[2]/button'
    about_place_xpath_1 = '/html/body/div[10]/section/div/div/div[2]/div/div[2]/div/div/div/div/div/div/div/section/div[2]/div/span'
    about_place_xpath_2 = '/html/body/div[10]/section/div/div/div[2]/div/div[2]/div/div/div/div/div/div/div/section/div[3]/div/span'
    addition_information_about_place_xpath = '/html/body/div[10]/section/div/div/div[2]/div/div[2]/div/div/div/div/div/div/div/section/div[4]/div/span'
    close_description_xpath = '/html/body/div[10]/section/div/div/div[2]/div/div[1]/button'
    show_amenities_xpath = '/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[1]/div/div[5]/div/div[2]/section/div[3]/button'
    close_amenities_xpath = '/html/body/div[10]/section/div/div/div[2]/div/div[1]/button'
    amenity_div_xpath ='/html/body/div[10]/section/div/div/div[2]/div/div[3]/div/div/div/section/div[2]'
    
    review_div_xpath_1 = '/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[4]/div/div/div/div[2]/div/section/div[2]/div'
    review_div_xpath_2 = '/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[4]/div/div/div/div[2]/div/section/div[2]/div/div/div[3]/div/div/div/div'
    
    show_all_comments_xpath = '/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[4]/div/div/div/div[2]/div/section/div[4]/button'
    comment_div_xpath = '/html/body/div[10]/section/div/div/div[2]/div/div[3]/div/div/div/section/div/div/div[2]/div[2]/div'
    close_comment_xpath = '/html/body/div[10]/section/div/div/div[2]/div/div[1]/button'

    
    now = dt.datetime.now()
    now_str = dt.datetime.today().strftime("%b-%d-%Y")
    
    total_urls = len(df)

    full_df = None

    # time.sleep(100)
    i = 1
    
    for url,ID,section,country_from_df in df[['URL','ID','Section','Country']].values:
        
        driver = webdriver.Chrome()
        driver.maximize_window()
        time.sleep(3)
    
        print("\n\n")
        print("-"*50,i,"/",total_urls,":",round(i/total_urls*100,5),"%","-"*50,"\n")
        i+=1
        driver.get(url)
        time.sleep(3)
    
        try:
            close = driver.find_element(By.XPATH,close_translate_button_xpath)
            close.click()
            time.sleep(1)
        except:
            pass
    
        
        try:    
            item_title = driver.find_element(By.XPATH,item_title_xpath).text
            print("Title: ",item_title)
    
        except:
            item_title = np.nan
    
    
    
        time.sleep(2)
        
        try:
            item_review = float(driver.find_element(By.XPATH,item_review_xpath).text.split(" ")[0])
            item_ratings = float(driver.find_element(By.XPATH,item_ratings_xpath).text.split(" ")[0])
    
            print("Review: ",item_review,
                  "\nRatings: ",item_ratings)
        except:
            item_review = np.nan
            item_ratings = np.nan
    
        
        time.sleep(2)
    
        try:
            host_level = driver.find_element(By.XPATH,host_level_xpath).text.strip().strip()
            print("Host: ",host_level)
        except:
            host_level = np.nan
    
    
    
        
        
        try:
            location = driver.find_element(By.XPATH,location_xpath).text.strip()
            print("Location: ",location)
    
            try:
                city,state,country = [val.strip() for val in location.split(",")]
            except:
                city,country = [val.strip() for val in location.split(",")]
                state = np.nan        
        except:
            location = np.nan
            city = np.nan
            state = np.nan
            country = country_from_df
    
    
    
        
        try:
            n_guest = driver.find_element(By.XPATH,guest_xpath).text
            try:
                n_guest = int(n_guest.split(" ")[0])
                print("Guests: ",n_guest)
            except:
                n_guest = np.nan
                
        except:
            n_guest = np.nan
    
        time.sleep(2)
    
    
        
        try:
            bedrooms = driver.find_element(By.XPATH,bedrooms_xpath).text
            try:
                bedrooms = int(beds.split(" ")[0])
            except:
                bedrooms = 1
    
            print("Bedrooms: ",bedrooms)
        except:
            bedrooms = np.nan
        
    
    
    
        
        try:
            beds = driver.find_element(By.XPATH,beds_xpath).text
            
            try:
                beds = int(beds.split(" "))
            except:
                beds = 2
    
            print("Beds: ",beds)
        except:
            beds = np.nan
    
    
    
        
        try:
            baths = driver.find_element(By.XPATH,baths_xpath).text
            
            try:
                baths = int(baths.split(" ")[0])
            except:
                baths = 1
            print("Baths: ",baths)
        except:
            baths = np.nan
    
    
    
        time.sleep(2)
        try:
            price_section = driver.find_element(By.XPATH,price_xpath).text.split(" ")
            price = price_section[0]
            currency = "USD" if price[0] == "$" else "Other"
            current_price = float(price[1:])
    
            item_unit = price_section[2]
    
                    
            print("Current price: ",current_price,
                  "\nCurrency: ",currency,
                  "\nPrice for per: ",item_unit)
    
            try:
                price_before = float(price_section[-1][1:])
                print("Price before: ",price_before)
            except:
                price_before = current_price
                print("Price before: ",price_before)
    
        except:
            try:
                price_path = '/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div[1]/div[1]/div/span/div/span[1]'
                price = driver.find_element(By.XPATH,price_path).text.strip()
                currency = "USD" if price[0] == "$" else "Other"
                price = float(price[1:])
                price_before = current_price
                item_unit = "night"
    
    
            except:
                
                continue
                
                current_price = np.nan
                currency = np.nan
                price_before = np.nan
                item_unit = np.nan
    
    
    
        driver.execute_script("window.scrollTo(0,1000);")
    
    
        time.sleep(2)
        try:
            price_review = float(driver.find_element(By.XPATH,price_review_xpath).text.strip().split(" ")[0])
            price_ratings = int(driver.find_element(By.XPATH,price_ratings_xpath).text.strip().split(" ")[0])
        except:
            price_review = np.nan
            price_ratings = np.nan
    
    
        try:
            item_unit = driver.find_element(By.XPATH,item_unit_xpath).text.strip()
        except:
            item_unit = 'night'
            
    
    
        time.sleep(2)
    
    
        # description
    
        
        try:
            # driver.execute_script("window.scrollTo(0,document.body.scrollHeight-5000);")
            # time.sleep(2)
            show_description = driver.find_element(By.XPATH,show_desciption_xpath)
            # time.sleep(2)
            show_description.click()
            time.sleep(2)
        except:
            try:
                buttons = driver.find_elements(By.CSS_SELECTOR,"button")
                for button in buttons:
                    if button.text == 'Show more':
                        break
    
                # time.sleep(1)
                button.click()
                time.sleep(3)
            except:
                
                pass
    
        time.sleep(2)
        try:
            about_place_1 = driver.find_element(By.XPATH,about_place_xpath_1).text
        except:
            about_place_1 = ''
        try:
            about_place_2 = driver.find_element(By.XPATH,about_place_xpath_2).text
        except:
            about_place_2 = ''
        try:
            additional_info = driver.find_element(By.XPATH,addition_information_about_place_xpath).text
        except:
            additional_info = ''
    
        description = " ".join([about_place_1,about_place_2,additional_info])
        print("\nDescription: ",description)
    
    
        try:
            close_tab = driver.find_element(By.XPATH,close_description_xpath)
            # time.sleep(1)
            close_tab.click()
            time.sleep(1)
    
        except:
            pass
    
    
    
        # what this place offers
    
        time.sleep(2)
        
        try:
            button = driver.find_element(By.XPATH,show_amenities_xpath)
            # time.sleep(1)
            button.click()
        except:
            try:
                buttons = driver.find_elements(By.CSS_SELECTOR,"button")
    
                for button in buttons:
                    name = button.text
                    # name = " ".join(name.split(" ")
                    try:
                        name = " ".join(list(map(name.split(" ").__getitem__,[0,1,3])))
                    except:
                        pass
                    if name == 'Show all amenities':
                        break
                button.click()
                time.sleep(1)
            except:
                pass
    
    
        time.sleep(2)
        try:
            div = driver.find_element(By.XPATH,amenity_div_xpath)
            divs = div.find_elements(By.CSS_SELECTOR,'div')
                                     
            
            amenities_dict = {}
            amenities_list = []
            for div in divs:
                
                try:
                    h3 = div.find_element(By.CSS_SELECTOR,'h3')
                    h3 = h3.text
                    amenities_dict[h3] = []
                except:
                    pass
                clas = div.get_attribute("class")
                if clas == 'twad414 dir dir-ltr':
                    item = div.text
            
            
                    if h3 == "Not included":
                        el = "/n"
                        if "\n" in item:
                            el = "\n"
                    
                
                        item_list = "".join(item.split(el)[0])
                        item = item_list.split(":")[1].strip()
                    
                    amenities_dict[h3].append(item)
                    if h3 == "Not included":
                        amenities_list.append(item_list)
                    else:
                        amenities_list.append(item)
    
            amenities_list = ", ".join(amenities_list)
            not_included = amenities_dict['Not included']
        except:
            amenities_list = np.nan
            amenities_dict = np.nan
            not_included = np.nan
    
        print("\nAmenities: ",amenities_dict)
        time.sleep(2)
    
    
        try:
            close = driver.find_element(By.XPATH,close_amenities_xpath)
            # time.sleep(1)
            close.click()
            time.sleep(1)
    
        except:
            pass
    
        driver.execute_script("window.scrollTo(0,2000);")
    
    
        time.sleep(2)
        try:
            divs = driver.find_element(By.XPATH,review_div_xpath_1)
            divs = divs.find_elements(By.CSS_SELECTOR,'div')
            
            review_section = {}
            for div in divs:
                clas = div.get_attribute("class")
                if clas == '_a3qxec':
                    key = div.text
                    el = "/n"
                    
                    if "\n" in key:
                        el = "\n"
                    
                    key,value = key.split(el)
    
                    review_section[key] = float(value)
    
                    if len(list(review_section.values())) == 0:
                        raise Exception
            
            
        except:
            try:
                time.sleep(1)
                divs = driver.find_element(By.XPATH,review_div_xpath_2)
                divs = divs.find_elements(By.CSS_SELECTOR,'div')
                review_section = {}
                for div in divs:
                    clas = div.get_attribute("class")
                    if clas == 'l925rvg dir dir-ltr':
                        
                        key = div.text
                        el = "/n"
                        
                        if "\n" in key:
                            el = "\n"
                        
                        key,value = key.split(el)
                        value = float(value)
                        review_section[key]=value
                                                
            except:
                review_section = np.nan
    
        print("\nReview sections: ",review_section)
    
    
        # comment section
        driver.execute_script("window.scrollTo(0,2500);")
        time.sleep(2)
    
        try:
            show = driver.find_element(By.XPATH,show_all_comments_xpath)
            # time.sleep(1)
            show.click()
            time.sleep(1)
    
        except:
            buttons = driver.find_elements(By.CSS_SELECTOR,"button")
            for button in buttons:
                name = button.text
                # name = " ".join(name.split(" ")
                try:
                    name = " ".join(list(map(name.split(" ").__getitem__,[0,1,3])))
                except:
                    pass
                    pass
                if name == 'Show all reviews':
                    break
    
        
        try:
            comments_div = driver.find_element(By.XPATH,comment_div_xpath)
            comments_divs = comments_div.find_elements(By.CSS_SELECTOR,'span')
            comments = []
            for span in comments_div:
                clas = span.get_attribute("class")
                if clas == 'll4r2nl dir dir-ltr':
                    comment = span.text
                    comments.append(comment)
        except:
            try:
                comment_div_xpath = '/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[4]/div/div/div/div[2]/div/section/div[3]/div/div'
                comments_div = driver.find_element(By.XPATH,comment_div_xpath)
                comments_divs = comments_div.find_elements(By.CSS_SELECTOR,'span')
                comments = []
                for span in comments_divs:
                    clas = span.get_attribute("class")
                    if clas == 'll4r2nl dir dir-ltr':
                        comment = span.text
                        comments.append(comment)
            except:
                comments = np.nan
                pass
    
    
        try:
            close = driver.find_element(By.XPATH,close_comment_xpath)
            close.click()
        except:
            pass
        print("\nComments",comments)
                    
    
            
    
        # concate
    
        inner_df = pd.DataFrame(
            {
                "ID":[ID]
                ,"ItemTitle":[item_title]
                ,"Section":[section]
                ,"ItemReview":[item_review]
                ,"ItemReviewBySections":[review_section]
                ,"ItemRatings":[item_ratings]
                ,"HostLevel":[host_level]
                ,"Location":[location]
                ,"Country":[country]
                ,"State":[state]
                ,"City":[city]
                ,"NumberOfGuest":[n_guest]
                ,"NumberOfBedrooms":[bedrooms]
                ,"NumberOfBeds":[beds]
                ,"NumberOfBaths":[baths]
                ,"CurrentPrice":[current_price]
                ,"PriceBefore":[price_before]
                ,"Currency":[currency]
                ,"ItemUnit":[item_unit]
                ,"PriceReview":[price_review]
                ,"PriceRatings":[price_ratings]
                ,"ItemDescription":[description]
                ,"Amenities":amenities_list
                ,"AmenitiesWithCategories":[amenities_dict]
                ,"NotIncludedAmenity":[not_included]
                ,"Comments":[comments]
                ,"URL":[url]
            }
        )
    
    
    
        if i % 10 == 0:
            driver.quit()
    
            time.sleep(20)
    
            driver = webdriver.Chrome()
            
        then = dt.datetime.now()
    
        driver.quit()
    
        if full_df is None:
            full_df = inner_df.copy()
            continue
    
        full_df = pd.concat([full_df,inner_df])
    
        
    
        
        full_df.to_csv(path_to_save,index=False)
        
    return full_df