from selenium import webdriver
from selenium.webdriver.common.by import By

import time

import pandas as pd
import numpy as np

import re
import os

country_list = pd.read_csv("../data/additional/country_list.csv")
    
countries = country_list['Name'].values.tolist()
    



def url_scraping_by_country(countries,directory_path):

    n_countries = 1

    # for country in ['Afghanistan']:
    for country in countries:

        path = directory_path+country+".csv"

        
        full_df =  pd.DataFrame(columns=["Country","Section","URL","ID",])

        url = 'https://www.airbnb.com/' 
        time.sleep(5)
        # buld a driver
        
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(url)

        # print("Driver created")
        
        time.sleep(5)

        # search buttons

        input_button_xpath = '/html/body/div[5]/div/div/div[1]/div/div[2]/div[1]/div/div/div/header/div/div[2]/div[1]/div/span[2]/button[1]'
        input_xpath = '/html/body/div[5]/div/div/div[1]/div/div[2]/div[1]/div[1]/div/div/header/div/div[2]/div[2]/div/div/div/form/div[2]/div[1]/div[1]/div[1]/label/div/input'
        search_button_xpath = '/html/body/div[5]/div/div/div[1]/div/div[2]/div[1]/div/div/div/header/div/div[2]/div[2]/div/div/div/form/div[2]/div[1]/div[5]/div[1]/div[2]/button'

        
        # click on input button
        try:
            input_button = driver.find_element(By.XPATH,input_button_xpath)
            input_button.click()
            time.sleep(3)
        except:
            pass

        # input country name
        input_button = driver.find_element(By.XPATH,input_xpath)
        input_button.send_keys(country)

        # seach button 
        search_button = driver.find_element(By.XPATH,search_button_xpath)
        search_button.click()
        time.sleep(3)



        i = 2

        print("Search done")
        
        while True:

            if i % 5 == 0:
                time.sleep(60)
        

            time.sleep(3)
            section_xpath = '/html/body/div[5]/div/div/div[1]/div/div[2]/div[1]/div[2]/div[1]/div/div/div/div/div/div[1]/div/div/div/div/div[3]/div/div/div/div/label['+str(i)+']'
            i += 1
            try:
                # get the section 
                time.sleep(3)
                section = driver.find_element(By.XPATH,section_xpath)
                section_name = section.text

                print("\n\n",section_name,"\n\n")

                section.click()
            except Exception as e:
                print("Section exception")
                print(str(e))
                # driver.quit()
                break

            print("Section obtained")





            # pagination
            time.sleep(5)


            driver.execute_script("window.scrollTo(0,document.body.height);")
        
            time.sleep(2)

            # check if there is any info
            no_result_xpath = '/html/body/div[5]/div/div/div[1]/div/div[2]/div[2]/main/div[2]/div/div/div/div/div/div/div/div/div/div[1]/section/h2'

            try:
                no_result = driver.find_element(By.XPATH,no_result_xpath).text.strip()
                print(no_result)
                continue
            except:
                pass
                
            
            last_pagination = 6

            number_of_pages = 1
            
            while last_pagination >= 0:
                print("Pagination",last_pagination)
                try:
                    last_page_token = driver.find_element(By.XPATH,'/html/body/div[5]/div/div/div[1]/div/div[2]/div[2]/main/div[2]/div/div[3]/div/div/div/nav/div/a['+str(last_pagination)+']')
                    number_of_pages = int(last_page_token.text)
                except:
                    last_pagination -= 1
                    time.sleep(1)
                    continue
        
                break
        
            
        
        
            print("Before pages")

            j = 0

            while True:
        
                # print("While Loop")
        
                
                if j == 0:
                    next_page_path = None
                    
            # try to click next page bottun
                elif j == 1:
                    next_page_path = '/html/body/div[5]/div/div/div[1]/div/div[2]/div[2]/main/div[2]/div/div[3]/div/div/div/nav/div/a[1]'
                elif j == 2:
                    next_page_path = '/html/body/div[5]/div/div/div[1]/div/div[2]/div[2]/main/div[2]/div/div[3]/div/div/div/nav/div/a[3]'
                elif j == number_of_pages - 1:
                    next_page_path = '/html/body/div[5]/div/div/div[1]/div/div[2]/div[2]/main/div[2]/div/div[3]/div/div/div/nav/div/a[5]'
                else:
                    next_page_path = '/html/body/div[5]/div/div/div[1]/div/div[2]/div[2]/main/div[2]/div/div[3]/div/div/div/nav/div/a[4]'
                
                try:
                    next_page = driver.find_element(By.XPATH,next_page_path)
                    next_page.click()
                    print("Next page done")
                except:
                    pass

                time.sleep(5)
                
                if (j!=0) and (j == number_of_pages or last_pagination == -1):
                    break
                
                j+=1


                k = 1
                while True:

                    item_xpath = '/html/body/div[5]/div/div/div[1]/div/div[2]/div[2]/main/div[2]/div/div[2]/div/div/div/div/div[1]/div['+str(k)+']/div/div[2]/div/div/div/div[1]/a'
            
                    k+=1
            
                    try:
                        element = driver.find_element(By.XPATH,item_xpath)
                        href = element.get_attribute("href")
                        ID = element.id
            
                        print(f"{country}:/n{section_name}:{href}")
            
                    except:
                        break
            
                    print("\n")
            
                    inner_df = pd.DataFrame({"Country":[country],
                                            "Section":[section_name],
                                            "URL":[href],
                                            "ID":[ID]
                                            })
                    
                
                    full_df = pd.concat([full_df,inner_df])

                time.sleep(5)
                print("\n\n",section_name,': ',j,'\n\n')

        if n_countries % 10 == 0:
            time.sleep(30)
     
        n_countries += 1

        full_df.to_csv(path,index=False)

        del full_df
