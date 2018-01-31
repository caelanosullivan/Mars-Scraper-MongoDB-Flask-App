
# coding: utf-8

# In[1]:


# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # Create a dictionary for scraped data
    mars_data = {}


    # ## Scraping NASA for Mars headlines

    # In[2]:


    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'

    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')


    # In[5]:


    #print(soup.prettify())


    # In[6]:


    #list(soup.children)


    # In[7]:


    # Scrape NASA Mars News (https://mars.nasa.gov/news/) for the latest News Title and Paragragh Text

    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='rollover_description_inner').text

    ## Add to dictionary

    mars_data["news_title"] = news_title
    mars_data["summary"] = news_p

    # ## Using Splinter for JPL Mars Featured Image

    # In[8]:


    # Use Splinter to navigate to NASA's Jet Propulsion Laboratory site

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)


    # In[9]:


    # Click the 'FULL IMAGE' button to get to the featured image
    browser.click_link_by_partial_text('FULL IMAGE')


    # In[10]:


    # Click the 'more info' button to get to the feature image's article
    browser.click_link_by_partial_text('more info')


    # In[11]:


    # Design an XPATH selector to grab the featured image
    xpath = '//figure//a'


    # In[12]:


    # Use splinter to click the featured image and bring up the full resolution image
    results = browser.find_by_xpath(xpath)
    img = results[0]
    img.click()


    # In[13]:


    # Scrape the browser into soup and use soup to find the full resolution image
    # Save the image url to a variable
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    featured_img_url = soup.find("img")["src"]
    #featured_img_url

    # Add the featured image url to the dictionary
    mars_data["featured_img_url"] = featured_img_url


    # In[14]:


    # David's
    # Visit the JPL Mars URL
    # url2 = "https://jpl.nasa.gov/spaceimages/?search=&category=Mars"
    # browser.visit(url2)
    # # Scrape the browser into soup and use soup to find the image of mars
    # # Save the image url to a variable called `img_url`
    # html = browser.html
    # soup = BeautifulSoup(html, 'html.parser')
    # image = soup.find("img", class_="thumb")["src"]
    # img_url = "https://jpl.nasa.gov"+image
    # # Use the requests library to download and save the image from the `img_url` above
    # import requests
    # import shutil
    # response = requests.get(img_url, stream=True)
    # with open('img.jpg', 'wb') as out_file:
    #     shutil.copyfileobj(response.raw, out_file)
        
    # # Display the image with IPython.display
    # from IPython.display import Image
    # Image(url='img.jpg')  


    # ## Mars Weather Tweets

    # In[21]:


    # Use Splinter to navigate to Mars Weather Twitter account (@MarsWxReport)

    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)


    # In[40]:


    # Scrape the browser into soup and use soup to find the most recent Tweet
    # Save the text to a variable
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # mars_weather = soup.find("div", class_="js-tweet-text-container").text.strip()

    mars_weather_tweets = soup.find_all("div", class_="js-tweet-text-container")

    for tweet in mars_weather_tweets:
        latest_weather = tweet.text.strip()
        if latest_weather.startswith('Sol'):
            print(latest_weather)
            break


    # Add the weather to the dictionary
    mars_data["mars_weather"] = latest_weather
    
    # ## Mars Facts: Scrape and Convert to HTML Table with Pandas

    # In[98]:


    # Use Pandas read_html function to automatically scrape tabular data

    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)

    # Display 'tables' to explore and review in preparation for conversion
    # tables
    # tables[0]


    # In[99]:


    # Set tabular data to variable and cleanup dataframe

    mars_facts_df = tables[0]
    mars_facts_df.columns = ['Parameter', 'Measurement']
    mars_facts_df.set_index('Parameter', inplace=True)
    #mars_facts_df.head()


    # In[100]:


    # Use Pandas to_html method to generate HTML table from DataFrame and save as string

    html_table = mars_facts_df.to_html()
    html_table


    # In[101]:


    # Strip newlines

    html_table.replace('\n', '')

    # Add the Mars facts table to the dictionary
    mars_data["mars_table"] = html_table

    # Return the dictionary
    return mars_data