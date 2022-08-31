
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


### Featured Images


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


## Challenge Code Begins



# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager



# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


### Visit the NASA Mars News Site


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)



# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')



slide_elem.find('div', class_='content_title')



# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title



# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


### JPL Space Images Featured Image



# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)



# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()



# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup



# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel



# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


### Mars Facts


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()



df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df



df.to_html()


## D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

### Hemispheres



# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)



# Parse the data.
hemi_html = browser.html
hemi_soup = soup(hemi_html,'html.parser')



# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
hemi_urls = hemi_soup.find_all('div', class_='item')

# Loop through the page.
for hemi_url in hemi_urls:

    # Create an empty dictionary.
    hemispheres = {}
    
    # Find the photo URL on home page.
    hemi_link = hemi_url.find('a', class_='itemLink product-item')['href']
    
    # Merge the base URL with photo URL and visit photo page.
    browser.visit(url + hemi_link)
    
    # Parse the photo data.
    photo_html = browser.html
    photo_soup = soup(photo_html,'html.parser')
    
    # Retrieve the relative photo URL.
    img_url_rel = photo_soup.find('img', class_='wide-image').get('src')
    
    # Retrieve the title.
    title = browser.find_by_css('h2.title').text
    
    # Create the absolute photo URL.
    img_url = f'https://marshemispheres.com/{img_url_rel}'

    # Save back to the dictionary.
    hemispheres['title'] = title
    hemispheres['img_url'] = img_url
    
    # Append to the list.
    hemisphere_image_urls.append(hemispheres)
    
    # Use the "back button" to move to the next image.
    browser.back()
    
    # Print for confirmation.
    print(title)
    print(img_url)



# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls



# 5. Quit the browser
browser.quit()





