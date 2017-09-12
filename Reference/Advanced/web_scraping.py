# Python example of scraping the web, which can be a useful tool if you can't find an API.
import urllib
from bs4 import BeautifulSoup

#Simple script to get the name and price of a new laptop.
def getPrice():
    # Use URLLIB to open a webpage
    site = urllib.urlopen("http://www.dell.com/en-us/shop/dell-laptops/sc/laptops/inspiron-laptops")
    # BeautifulSoup object of the HTML code
    soup = BeautifulSoup(site, 'html.parser')
    # From the html, find an h4 attribute that has the type data-testid and the name productSeriesVariantStartingAtId
    price = soup.find("h4", attrs={"data-testid":"productSeriesVariantStartingAtId"})
    # Print the price as text, but without the html tags around it. .strip() removes the tags.
    print price.text.strip()

getPrice()