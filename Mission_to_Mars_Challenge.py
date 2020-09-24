# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd

# Set the executable path and initialize the chrome browser in splinter
executable_path = {"executable_path": "chromedriver.exe"}
browser = Browser("chrome", **executable_path, headless=False)

# Visit the NASA Mars News Site

# Visit the mars nasa news site
url = "https://mars.nasa.gov/news/"
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

# Setting up the HTML parser
html = browser.html
news_soup = soup(html, "html.parser")
slide_elem = news_soup.select_one("ul.item_list li.slide")

# Begin the scraping
slide_elem.find("div", class_="content_title")

# Use the parent element to find the first "a" tag and save it as a "news_title"
news_title = slide_elem.find("div", class_="content_title").get_text()
news_title

# Use the parent element to find the paragraph get_text
news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
news_p


# JPL Space Images Featured Images

# Visit URL
url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_id("full_image")
full_image_elem.click()

# Find the more info button and click that
browser.is_element_present_by_text("more info", wait_time=1)
more_info_elem = browser.links.find_by_partial_text("more info")
more_info_elem.click()

# Parse the resulting html with news_soup
html = browser.html
img_soup = soup(html, "html.parser")

# Find the relative image url
img_url_rel = img_soup.select_one("figure.lede a img").get("src")
img_url_rel

# Use the base URL to create an absolute URL
img_url = f"https://www.jpl.nasa.gov{img_url_rel}"
img_url


# Mars Facts

# Converting the table in website into pandas friendly DF
df = pd.read_html("http://space-facts.com/mars/")[0]
df.columns = ["description", "value"]
df.set_index("description", inplace=True)
df

#Converting the dataframe back to HTML ready code
df.to_html()


# Scrape High-Resolution Mars’ Hemisphere Images and Titles

# Hemispheres

# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

# 2. Create a list to hold the images and titles.
hemisphere_images = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
links = browser.find_by_css("a.product-item h3")

# Next, loop through those links, click the link, find the sample anchor, return the href
for i in range(len(links)):
    hemisphere = {}
    
    # We have to find the elements on each loop to avoid a stale element exception
    browser.find_by_css("a.product-item h3")[i].click()
    
    # Next, we find the Sample image anchor tag and extract the href
    sample_elem = browser.links.find_by_text('Sample').first
    hemisphere['img_url'] = sample_elem['href']
    
    # Get Hemisphere title
    hemisphere['title'] = browser.find_by_css("h2.title").text
    
    # Append hemisphere object to list
    hemisphere_images.append(hemisphere)
    
    # Finally, we navigate backwards
    browser.back()

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_images

# Ending browser session 
browser.quit()