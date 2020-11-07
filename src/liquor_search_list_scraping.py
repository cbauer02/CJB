from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import requests
import numpy as np
import lxml.html as lh

def scrape_olcc_whiskey_list(URL): #scrape landing whiskey list
    print("starting whiskey list processing...")
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    click1 = driver.find_element_by_xpath("//input[@name='btnSubmit']").click() #click "I'm 21 or older"
    click2 = driver.find_element_by_xpath("//*[@id='browse-content']/ul[1]/li[5]/a").click() #click "Domestic Whiskey"
    click3 = driver.find_element_by_xpath("//*[@id='browse-content']/ul/li[1]/a").click() #click "Domestic Whiskey - ALL"
    current_page = driver.page_source

    whiskey_doc = lh.fromstring(current_page) #Store the contents of the website under doc

    tr_elements = whiskey_doc.xpath('//tr') #Parse data that are stored between <tr>..</tr> of HTML
    booze=[]#Create empty list
    booze.clear()
    i=0

    #For each row, store each first element (header) and an empty list
    for t in tr_elements[4]:
        i+=1
        name=t.text_content()
        booze.append((name,[]))

    #Since our first row is the header, data is stored on the second row onwards
    for j in range(5,len(tr_elements)):
        T=tr_elements[j] #T is our j'th row
        if len(T)!=7:
            break #If row is not of size 7, the //tr data is not from our table
        i=0 #i is the index of our column

        #Iterate through each element of the row
        for t in T.iterchildren():
            data=t.text_content()
            if i>0: #Check if row is empty
                try:
                    data=int(data) #Convert any numerical value to integers
                except:
                    pass
            booze[i][1].append(data) #Append the data to the empty list of the i'th column
            i+=1 #Increment i for the next column
    driver.quit()
    whiskey_dict={title:column for (title,column) in booze}
    print("starting whiskey list processing COMPLETE!")
    return pd.DataFrame(whiskey_dict)
