from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import requests
import numpy as np
import lxml.html as lh


#click through each whiskey and scrape inventory
def scrape_olcc_whiskey_inv(URL):

    # setting up selenium web scraper parameters
    # clicking through age verification page, and to whiskey page
    print("starting whiskey inv processing...")
    options = Options()
    options.headless = True #comment out to view browser navigation
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    click1 = driver.find_element_by_xpath("//input[@name='btnSubmit']").click() #click "I'm 21 or older"
    click2 = driver.find_element_by_xpath("//*[@id='browse-content']/ul[1]/li[5]/a").click() #click "Domestic Whiskey"
    click3 = driver.find_element_by_xpath("//*[@id='browse-content']/ul/li[1]/a").click() #click "Domestic Whiskey - ALL"
    whiskey_inv=[]
    whiskey_inv.clear()

    # Scrape headers' clicks
    # Store the contents of the website under doc
    # Parse through the //tr elements
    click_n = driver.find_element_by_xpath(f"//*[@id='browse-content']/table/tbody/tr[2]/td[1]/span").click()
    current_page = driver.page_source
    whiskey_list_doc = lh.fromstring(current_page)
    tr_elements_1 = whiskey_list_doc.xpath('//tr')

    # loop over olcc whiskey table and scrap headers,
    # append whiskey_ inv list with column headers
    for t in tr_elements_1[10]:
        name=t.text_content()
        whiskey_inv.append((name,[]))
    print("scraped headers:", whiskey_inv)
    back_button = driver.back()

    # Store the contents of the website under doc
    # Parse through the //tr elements
    n=2
    while n<10:
        try:
            click_n = driver.find_element_by_xpath(f"//*[@id='browse-content']/table/tbody/tr[{n}]/td[1]/span").click()
            current_page = driver.page_source
            whiskey_list_doc = lh.fromstring(current_page)
            tr_elements_1 = whiskey_list_doc.xpath('//tr')

            # iterate throught each //tr row and check for data
            # T is the tr_element of our j'th row
            for j in range(11,len(tr_elements_1)):
                T=tr_elements_1[j]

                # If row is not of size 7,
                # the //tr data is not from our table
                if len(T)!=7:
                    break
                i=0

                # Iterate through each column value
                # Append the data to the empty list of the i'th column
                for t in T.iterchildren():
                    data=t.text_content()

                    # Check if row is empty
                    # Convert any numerical value to integers
                    # Append data into whiskey_inv list
                    # Increment i for the next column
                    if i>0:
                        try:
                            data=int(data)
                        except:
                            pass
                    whiskey_inv[i][1].append(data)
                    i+=1

            # save data into data dictionary and dataframe
            # print the whiskey that was just scrapped
            whiskey_inv_dict={title:column for (title,column) in whiskey_inv}
            whiskey_df = pd.DataFrame(whiskey_inv_dict)
            whiskey_name = driver.find_element_by_xpath("//*[@id='product-desc']/h2")
            print("scrapped inv of whiskey =" + str(whiskey_name.text))
            back_button = driver.back()
            n+=1
            print("Collected " + str(len(tr_elements_1)-11-1) + "rows")

        # If the element isn't found,
        # exit from the loop
        except NoSuchElementException:
            driver.close()
            print("There are no remaining whiskeys to scrape.  Exiting function.")
            break

        finally:
            return(whiskey_df)

    whiskey_df.head()
    print("starting whiskey inv processing COMPLETE!")
