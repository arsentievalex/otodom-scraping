from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import pandas as pd
import os


def write_to_excel(file, df, sheet_name):
    # if file does not exist, then write to a new excel file, if it already exists, write to an existing one
    with pd.ExcelWriter(file, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)



# initiate the chrome driver and declare the url
website = 'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/warszawa?&market=SECONDARY&&limit=72'
path = 'chromedriver.exe'
driver = webdriver.Chrome(path)
driver.maximize_window()
driver.get(website)

time.sleep(2)

# clicking through the accept cookies button
cookies_button = driver.find_element(by=By.XPATH, value='//button[@id="onetrust-accept-btn-handler"]')
cookies_button.click()

time.sleep(2)

# get total number of results
total = driver.find_element(by=By.XPATH, value='//strong[@data-cy="search.listing-panel.label.ads-number"]')
total_num = re.findall(r'\d+', total.text)


# calculate the number of pages
num_of_pages = round(int(total_num[0]) / 72)

# initiate lists to store data
location = []
prices = []
m2_price = []
rooms = []
m2 = []
urls = []


# define main function
def scrape():
    # scroll down the webpage to get all results
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    # listings = driver.find_elements(by=By.XPATH, value='//div[@data-cy="search.listing"]')
    # li_obj = listings[1].find_elements(by=By.TAG_NAME, value='article')

    loc = driver.find_elements(by=By.XPATH, value='//p[@class="css-14aokuk e1ualqfi4"]')
    details = driver.find_elements(by=By.XPATH, value='//span[@class="css-1on0450 ei6hyam2"]')
    links = driver.find_elements(by=By.XPATH, value='//a[@data-cy="listing-item-link"]')

    # create a list of locations
    for t in loc:
        location.append(t.text)

    # create a list of listing details
    x = 0
    while x < len(details):
        prices.append(details[x].text)
        m2_price.append(details[x+1].text)
        rooms.append(details[x + 2].text)
        m2.append(details[x + 3].text)
        x += 4

    for l in links:
        urls.append(l.get_attribute('href'))

    # click on the next button
    next_button = driver.find_element(by=By.XPATH, value='//button[@data-cy="pagination.next-page"]')
    driver.execute_script("arguments[0].click();", next_button)
    time.sleep(5)


# run the function on each page
i = 1
while i <= num_of_pages:
    print('Working on page ' + str(i) + ' of ' + str(num_of_pages))
    try:
        scrape()
    except Exception as e:
        # print error code
        print(e)
        pass
    i += 1


# convert the lists into a dataframe
data = {'Location': location, 'Price': prices, 'Price per m2': m2_price, 'Rooms': rooms, 'm2': m2 , 'URL': urls}
df = pd.DataFrame(data)

# write the dataframe to an excel file
df.to_excel('data July 23.xlsx', index=False)


#close the browser
driver.quit()
