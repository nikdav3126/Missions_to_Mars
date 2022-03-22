#import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt

def scrape_all():

    #set up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless = False)

    latest_title, latest_p = scrape_news(browser)

    mars_data = {
        "latestTitle": latest_title,
        "latestParagraph": latest_p,
        "featuredImage": scrape_feature_img(browser),
        "facts":scrape_facts(browser),
        "hemispheres": scrape_hemispheres(browser),
        "lastUpdate":dt.datetime.now()
        }

    browser.quit()

    return mars_data

def scrape_news(browser):
    #visit the mars news site
    url = "https://redplanetscience.com"
    browser.visit(url)
    browser.is_element_present_by_css('div.list_text', wait_time =1)

    html= browser.html
    news_soup = soup(html, "html.parser")

    latest = news_soup.select_one("div.list_text")
    latest_title = latest.find("div", class_= "content_title").get_text()

    latest_p = latest.find("div", class_= "article_teaser_body").get_text()

    return latest_title, latest_p

def scrape_feature_img(browser):
    #go to website for space images
    url="https://spaceimages-mars.com/"
    browser.visit(url)

    featured_img = browser.find_by_tag("button")[1]
    featured_img.click()

    html= browser.html
    image_soup = soup(html, "html.parser")

    featured_img_find = image_soup.find("img", class_= "fancybox-image").get("src")

    featured_img_url = f'https://spaceimages-mars.com/{featured_img_find}'

    return featured_img_url

def scrape_facts(browser):
    url="https://galaxyfacts-mars.com/"
    browser.visit(url)

    html= browser.html
    facts_soup = soup(html, "html.parser")

    facts_find = facts_soup.find("div", class_ = "diagram mt-4")
    fact_table = facts_find.find("table")

    facts = ""

    facts += str(fact_table)

    return facts

def scrape_hemispheres(browser):
    url = "https://marshemispheres.com/"
    browser.visit(url)

    hemisphere_image_urls = []
    for i in range (4):

        hemi_url = {}

        browser.find_by_css("a.product-item img")[i].click()
        
        sample = browser.links.find_by_text("Sample").first
        
        hemi_url["title"]=browser.find_by_css("h2.title").text
        
        hemi_url["img_url"] = sample["href"]
        
        hemisphere_image_urls.append(hemi_url)
        
        browser.back()

    return hemisphere_image_urls

if __name__ == "__main__":
     print(scrape_all())
