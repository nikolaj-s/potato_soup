from selenium import webdriver

from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import webbrowser
import os
from pathlib import Path
from src.potato_soup import PotatoSoup
import time

browser = webdriver.Chrome('./src/driver/chromedriver')



url = input("Input the websites Url \n >>")

browser.get(url)





print("Loading More of The page")

time.sleep(2)

browser.execute_script("window.scrollTo(0, 10000)")

time.sleep(1)

browser.execute_script("window.scrollTo(0, 10000)")

time.sleep(2)

dom = browser.page_source

pre_defined_sights = ['https://www.reddit.com/']

if url in pre_defined_sights:
    dom = browser.find_element_by_id('2x-container').get_attribute('outerHTML')

path = input("Please name the folder you wish to make your soup in \n >>>")  


soup = BeautifulSoup(dom, 'html.parser')

potato_soup = PotatoSoup(path, soup, Path().absolute())

potato_soup.launch()

browser.close()
# try:
#     html = urlopen(url)
# except:
#     print("Not able to scrap this site")
# else:
    
#     file_name = input("Please name the folder you wish to create your scrapped site in\n>>>")

#     os.mkdir('./output/' + file_name)



#     encode = html.read()


    #generate css doc
 

    # generate html doc
    # with open('./output/{file_path}/index.html'.format(file_path=file_name), 'w', encoding='utf8') as file:
        
    #     soup = BeautifulSoup(encode, 'html.parser')
        
    #     html = soup.prettify()

    #     images = soup.findAll('img')

    #     potatoe_soup = BeautifulSoup(HtmlFormat(images), 'html.parser').prettify()

    #     write = file.write(potatoe_soup)

    #     webbrowser.open(str(Path().absolute()) + "/output/" + file_name+"/index.html")