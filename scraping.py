# Import dependencies.
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# Set up executable path.
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# Visit the Mars NASA news site.
url = 'https://redplanetscience.com'
browser.visit(url)

# Set up delay for loading the page - optional.
browser.is_element_present_by_css('div.list_text', wait_time=1)


# Set up the HTML parser.
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# Create scraping code.
slide_elem.find('div', class_='content_title')


# Use the parent element to find the first 'a' tag and save it as 'news_title'.
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# Find the news article summary.
news_summary = slide_elem.find('div', class_='article_teaser_body').get_text()
news_summary


# ### Featured Images# 


# Visit URL for images.
url = 'https://spaceimages-mars.com'
browser.visit(url)


# Find and click the full image button. 
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# Parse the resulting html with soup.
html = browser.html
img_soup = soup(html, 'html.parser')


# Find the relative image url.
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# Use the base URL to create an absolute URL. 
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# Scrape the entire table of Mars facts.
df = pd.read_html('https://galaxyfacts-mars.com')[0] #using [0] pulls the first table/item in the list.
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# Convert the DataFrame back into HTML code.
df.to_html()


# End session/call.
browser.quit
