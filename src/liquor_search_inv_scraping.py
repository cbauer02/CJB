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
    driver = webdriver.Chrome(options=options) #webdriver ran from local executable_path
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

def scrape_olcc_whiskey_inv(URL): #click through each whiskey and scrape inventory
    print("starting whiskey inv processing...")
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    click1 = driver.find_element_by_xpath("//input[@name='btnSubmit']").click() #click "I'm 21 or older"
    click2 = driver.find_element_by_xpath("//*[@id='browse-content']/ul[1]/li[5]/a").click() #click "Domestic Whiskey"
    click3 = driver.find_element_by_xpath("//*[@id='browse-content']/ul/li[1]/a").click() #click "Domestic Whiskey - ALL"

    n=2
    whiskey_inv=[] #Create empty list
    whiskey_inv.clear()

    while n<10: #scraping 10 whiskeys, as a test. loop is scraping blank lists into whiskey_inv causing nothing to be inserted into whiskey_inv_df
        try:
            click_n = driver.find_element_by_xpath(f"//*[@id='browse-content']/table/tbody/tr[{n}]/td[1]/span").click()
            #time.sleep(5)
            current_page = driver.page_source
            whiskey_list_doc = lh.fromstring(current_page) #Store the contents of the website under doc
            tr_elements_1 = whiskey_list_doc.xpath('//tr') #Parse data that are stored between <tr>..</tr> of HTML
            #For each row, store each first element (header) and an empty list
            for t in tr_elements_1[10]:
                name=t.text_content()
                whiskey_inv.append((name,[]))

            #Since our first row is the header, data is stored on the second row onwards
            for j in range(11,len(tr_elements_1)):
                T=tr_elements_1[j] #T is our j'th row
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
                    whiskey_inv[i][1].append(data) #Append the data to the empty list of the i'th column
                    i+=1 #Increment i for the next column
            whiskey_inv_dict={title:column for (title,column) in whiskey_inv}
            back_button = driver.back()
            n+=1
            print("starting whiskey inv processing COMPLETE!")
            return pd.DataFrame(whiskey_inv_dict)
        except NoSuchElementException: # the element wasn't found
            driver.close()
            break # exit from the loop
