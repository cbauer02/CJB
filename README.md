# Liquor Search README.md

## SETUP:
* -python 3
* -terminal: Anaconda: jupyter
 
## INSTALLS required:

* https://chromedriver.chromium.org/getting-started
* #conda install pip
* #pip install selenium
* #pip install bs4
* #pip install pandas
* #pip install requests
* #pip install numpy
* #pip install lxml

## How do I run the script in the terminal?

* liquor_search_scraping.py

## DATABASE schema:

CREATE TABLE whiskey_list (
    item_code VARCHAR(5) PRIMARY KEY,
    description VARCHAR(70),
    size DECIMAL(4,1),
    proof DECIMAL(3,1),
    age VARCHAR(6),
    case_price DECIMAL(8,2),
    bottle_price DECIMAL(7,2),
    rare_hooch BIT
);

CREATE TABLE liquor_stores (
    store_no INT PRIMARY KEY,
    store_loc VARCHAR(30),
    address VARCHAR(60),
    zip INT(5),
    telephone VARCHAR(12),
    store_hours VARCHAR(50),
    delivery_weekdays VARCHAR(12)
);

CREATE TABLE whiskey_inv (
    id INT(10) NOT NULL AUTO_INCREMENT,
    item_code VARCHAR(5),
    store_no INT(4),
    qty INT(3),
    time_stamp DATETIME,
    PRIMARY KEY(id),
    FOREIGN KEY(item_code) REFERENCES whiskey_list(item_code) ON DELETE SET NULL,
    FOREIGN KEY(store_no) REFERENCES liquor_stores(store_no) ON DELETE SET NULL
);


