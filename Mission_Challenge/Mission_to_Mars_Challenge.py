# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

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

# ### JPL Space Images Featured Image

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

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()

df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df

df.to_html()


# D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# Hemispheres

# 1. Use browser to visit the URL 
url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

html = browser.html
news_soup = soup(html, 'html.parser')

# Scrape all items that contain mars hemispheres information
results = news_soup.find_all("div", class_="item")

# Sign main url for loop
hemispheres_url = "https://astrogeology.usgs.gov"

# Loop through the list of all hemispheres information
for result in results:
    title = result.find('h3').text
    hemispheres_img = result.find("a", class_="itemLink product-item")["href"]
    
    # Visit the link that of the full image website
    browser.visit(hemispheres_url + hemispheres_img)
    
    # HTML Object
    image_html = browser.html
    web_info = soup(image_html, "html.parser")
    
    # Create full image url
    img_url = hemispheres_url + web_info.find("img", class_="wide-image")["src"]
    
    hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    
    print(title)
    print(img_url)
    print("-----------------------------------------")

# 5. Quit the browser
browser.quit()

