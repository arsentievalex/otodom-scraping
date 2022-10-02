from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import pandas as pd


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

    loc = driver.find_elements(by=By.XPATH, value='//p[@class="css-80g06k es62z2j12"]')
    details = driver.find_elements(by=By.XPATH, value='//span[@class="css-s8wpzb eclomwz2"]')
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
    next_button.click()

    time.sleep(5)



# run the function on each page
i = 1
while i < num_of_pages:
    scrape()
    i += 1


#convert the lists into a dataframe
df = pd.DataFrame(list(zip(location, prices, m2_price, m2, rooms, urls)),
               columns =['Location', 'Price', 'Price per m2', 'Size M2', 'Rooms', 'URL'])

# save the output to xlsx
df.to_excel("data.xlsx", index=False)

# close the browser
driver.quit()
