
# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By


# def image_scraper(URL_ID_DF,directory_path):

#     while True:
#         try:
#             for ID, url in URL_ID_DF.values:
        
#                 if ID in existing_ids:
#                     continue
            
#                 driver = webdriver.Chrome()
#                 driver.get(url)
#                 driver.maximize_window()
#                 time.sleep(2)
        
#                 try:
#                     driver.find_element(By.XPATH,close_translate_button_xpath).click()
#                 except:
#                     pass
#                 try:
#                     show_all = driver.find_element(By.XPATH,show_all_photos_xpath)
#                     show_all.click()
#                 except:
#                     pass
        
#                 time.sleep(2)
#                 image_div = driver.find_element(By.XPATH,image_div_xpath)
#                 divs = image_div.find_elements(By.CSS_SELECTOR,'div')
            
            
#                 images_link = set()
#                 for div in divs:
#                     ims = div.find_elements(By.CSS_SELECTOR,'img')
#                     for im in ims:
#                         image_link = im.get_attribute("src")
#                         images[ID] = image_link
#                         break
#                     break
        
#                 driver.get(image_link)

#                 driver.save_screenshot("../Data/Images/"+ID+".png")
        
#                 driver.quit()
#             break
#         except:
#             time.sleep(60)
#             existing_images = os.listdir("../Data/Images")
#             existing_ids = [image.split(".")[0] for image in existing_images]
#             continue