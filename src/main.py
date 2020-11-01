import liquor_search_scraping

print("Running scrape_olcc_whiskey_list & scrape_olcc_whiskey_inv")
print(liquor_search_scraping.scrape_olcc_whiskey_list("http://www.oregonliquorsearch.com/"))
print(liquor_search_scraping.scrape_olcc_whiskey_inv("http://www.oregonliquorsearch.com/"))
