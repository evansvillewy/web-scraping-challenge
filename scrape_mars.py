import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import time
import os
def get_browser(browserEXE):
    executable_path = {'executable_path': browserEXE}
    time.sleep(1)
    return Browser('chrome', **executable_path, headless=False)

def scrape_mars_news(browser):

    news_dict={}
    # NASA Mars News
    url='https://mars.nasa.gov/news/'

    #visit the url
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    time.sleep(1)
    soup = bs(html, 'html.parser')
    time.sleep(1)

    #collect the latest News Title and Paragraph Text.
    news_title = soup.find('div', class_='content_title')
    news_dict["news_title"] = news_title.text
    time.sleep(1)
    news_paragraph = soup.find('div', class_='article_teaser_body')
    news_dict["news_paragraph"] = news_paragraph.text

    return news_dict

def scrape_jpl_image(browser):
    url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    base_url='https://www.jpl.nasa.gov'

    #visit the url
    browser.visit(url)
    time.sleep(10)

    #Use splinter to navigate the site and find the image url for the current Featured Mars Image and 
    #assign the url string to a variable called featured_image_url
    html = browser.html
    soup = bs(html, 'html.parser')
    image = soup.find('a', {"class": "button"})['data-fancybox-href']
    featured_image_url = base_url+image 

    return featured_image_url

def scrape_latest_twitter_wx():

    from selenium import webdriver
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get('https://twitter.com/marswxreport?lang=en')
    time.sleep(2)

    # use selenium to get the html for the weather tweets
    results=driver.find_element_by_xpath('//div[@aria-label="Timeline: Mars Weather’s Tweets"]').get_attribute('innerHTML')

    # use beautiful soup to get the span elements
    soup = bs(results, 'html')
    results=soup.find('span')
    time.sleep(2)

    # get the fifth span element
    results=soup.find_all('span')[4]

    driver.quit()

    return(results.text)

def scrape_mars_facts(browser):
    # Visit the Mars Facts webpage
    #use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    #https://space-facts.com/mars/

    url='https://space-facts.com/mars/'
    browser.visit(url)
    time.sleep(2)
    html = browser.html
    soup = bs(html, 'html.parser')
    time.sleep(2)

    #source: https://beenje.github.io/blog/posts/parsing-html-tables-in-python-with-pandas/
    mars_facts = pd.read_html(url)
    mars_facts_df = pd.DataFrame(mars_facts[0])
    mars_facts_df.columns = ["Measure","Value"]
    mars_facts_html = mars_facts_df.to_html(index=False)

    return mars_facts_html

def scrape_mars_hemis(browser):
    #Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
    url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    base_url="https://astrogeology.usgs.gov"

    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')  
    time.sleep(5)  

    results = soup.find_all("div", class_="description")
    mars_hemispheres=[]
    time.sleep(1)

    for result in results:
        img_dict = {}
        link = result.h3.text
        browser.click_link_by_partial_text(f'{link}')
        time.sleep(2)
        html = browser.html
        time.sleep(2)
        soup = bs(html, 'html.parser')
        time.sleep(2)
        img_url = base_url+soup.find('img', class_='wide-image')['src']
        img_dict["title"] = link
        img_dict["img_url"] = img_url
        mars_hemispheres.append(img_dict)
        browser.back()

    return mars_hemispheres

def scrape():
    
    mars_dict = {}

    # get the shared browser
    browserEXE = 'chromedriver.exe'
    browser = get_browser(browserEXE)

    #call each scrape function
    mars_dict["news_title"] = scrape_mars_news(browser)["news_title"]
    mars_dict["news_paragraph"] = scrape_mars_news(browser)["news_paragraph"]
    mars_dict["featured_image_url"] = scrape_jpl_image(browser)

    # the wx function uses selenium, couldn't get splinter to work
    mars_dict["mars_weather"] = scrape_latest_twitter_wx()

    mars_dict["mars_facts_table"] = scrape_mars_facts(browser)
    mars_dict["mars_hemispheres"] = scrape_mars_hemis(browser)

    #close the browser when done
    browser.quit()
    os.system("taskkill /f /im "+browserEXE)

    # Return the dictionary o fmars info
    return mars_dict        
