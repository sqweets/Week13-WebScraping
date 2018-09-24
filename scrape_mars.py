
# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import requests
import pymongo
import time

def scrape_all():

    # Set the chromedriver path
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

    mars_news_data = mars_news(browser)
    featured_img_data = featured_image(browser)
    weather_data = mars_weather(browser)
    facts_data = mars_facts(browser)
    hemis_data = mars_hemispheres(browser)


    mars_dictionary = {"mars_news": mars_news_data,
                       "featured_image": featured_img_data,
                       "mars_weather": weather_data,
                       "mars_facts": facts_data,
                       "mars_hemispheres": hemis_data}

    browser.quit()
    return mars_dictionary                      


    ###############
    # Get mars news
    ###############
def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find the Title and Description of the first news entry in the returned response
    ret_val =[]
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='rollover_description_inner').text

    ret_val.append(news_title)
    ret_val.append(news_p)

    return ret_val


    #######################################
    #JPL Mars Space Images - Featured Image
    #######################################
def featured_image(browser):
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    base_url = "https://www.jpl.nasa.gov"
    browser.visit(url)

    # Design an XPATH selector open full image button
    xpath = '//a[@id="full_image"]'

    try:
        # Use splinter to bring up the full resolution image
        results = browser.find_by_xpath(xpath)
        img = results[0]
        img.click()

        # Scrape the browser into soup and use soup to find the full resolution image of mars
        # Save the image url to a variable called `img_url`
        time.sleep(5)  # Give browser time to load full page
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_url = soup.find("img", class_="fancybox-image")["src"]
        featured_image_url = base_url + img_url
    except AttributeError:
        print("There was an error in featured_image")

    return featured_image_url


    #############
    #Mars Weather
    #############
def mars_weather(browser):
    url = 'https://twitter.com/marswxreport?lang=en'

    # Retrieve page with the requests module
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    # Find the latest weather tweet
    weather_tweet = soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})

    mars_weather = weather_tweet.find('p', 'tweet-text').get_text()

    return mars_weather


    ###########
    #Mars Facts
    ###########
def mars_facts(browser):

    try:
        url = 'http://space-facts.com/mars/'
        tables = pd.read_html(url)
        tables_df = pd.DataFrame(tables[0])
        tables_df.rename(index=str, columns={0: "", 1: "value"}, inplace=True)

        # Convert to hmtl table string
        mars_facts_table = tables_df.to_html(index = False)
    except BaseException:
        print("There was an error in mars_facts")

    return mars_facts_table


    #################
    #Mars Hemispheres
    #################
def mars_hemispheres(browser):
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    base_url = "https://astrogeology.usgs.gov"
    browser.visit(url)
    hemisphere_image_urls = []
    img_titles = []

    # Design an XPATH selector to grab the images
    xpath_img = '//div[@class="collapsible results"]//div[@class="item"]//a[@class="itemLink product-item"]/img'

    try:
        # Scrape the browser into soup and use soup to get the titles
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        descriptions = soup.findAll("h3")
        for description in descriptions:
            img_titles.append(description.text)

        # click through the 4 images
        for x in range(0, 4):
            # Click each one to get the larger image
            results_img = browser.find_by_xpath(xpath_img)
            img = results_img[x]    
            img.click()

            # Click the open button
            xpath_open = '//a[@id="wide-image-toggle"]'
            results = browser.find_by_xpath(xpath_open)
            open_btn = results[0]
            open_btn.click()

            # Scrape the browser into soup and use soup to find the full resolution images
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
            img_url = soup.find("img", class_="wide-image")["src"]
            full_img_path = base_url + img_url
            
            hemisphere_image_urls.append({img_titles[x]: full_img_path})

            browser.back()

    except AttributeError:
        print("There was an error in mars_hemispheres")
      

    return hemisphere_image_urls





