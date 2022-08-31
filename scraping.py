# Import dependencies.
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():

    # Set up executable path.
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_summary = mars_news(browser)

    # Run all scraping functions and store results in dictionary.
    data = {
        'news_title': news_title,
        'news_summary': news_summary,
        'featured_image': featured_image(browser),
        'facts': mars_facts(),
        'hemispheres': hemispheres(browser),
        'last_modified': dt.datetime.now()
        }

    # End session/call.
    browser.quit
    return data


def mars_news(browser):

    # Visit the Mars NASA news site.
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Set up delay for loading the page - optional.
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    # Set up the HTML parser.
    html = browser.html
    news_soup = soup(html, 'html.parser')
    

    # Add try/except for error handling. 
    try:
        # Set variables and start scraping. 
        slide_elem = news_soup.select_one('div.list_text')

        # Set variables and start scraping. 
        slide_elem.find('div', class_='content_title')


        # Use the parent element to find the first 'a' tag and save it as 'news_title'.
        news_title = slide_elem.find('div', class_='content_title').get_text()
    

        # Find the news article summary.
        news_summary = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_summary

### Featured Images

def featured_image(browser):

    # Visit URL for images.
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    # Find and click the full image button. 
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # Parse the resulting html with soup.
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling.
    try:

        # Find the relative image url.
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL. 
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


def mars_facts():
    # Add try/except for error handling.
    try:
        # Use 'read_html' to scrape the facts table into a DataFrame.
        df = pd.read_html('https://galaxyfacts-mars.com')[0] #using [0] pulls the first table/item in the list.

    except BaseException:
        return None

    # Assign columns and set index of DataFrame.
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)



    # Convert the DataFrame back into HTML code, add bootstrap.
    return df.to_html(classes="table table-striped")

def hemispheres(browser):

# Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)

# Parse the data.
    hemi_html = browser.html
    hemi_soup = soup(hemi_html,'html.parser')

# Create a list to hold the images and titles.
    hemisphere_image_urls = []

# Write code to retrieve the image urls and titles for each hemisphere.
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
    
# Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls

# Final step.
if __name__ == "__main__":
    
    # If running as script, print scraped data.
    print(scrape_all())

