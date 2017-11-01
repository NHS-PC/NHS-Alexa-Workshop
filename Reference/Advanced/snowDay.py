from selenium import webdriver
 
from selenium.webdriver.support.ui import WebDriverWait
import urllib


def getChance(zipcode):
    webpage = "https://www.snowdaycalculator.com/prediction.php?zipcode="+zipcode+"&snowdays=0&extra=0&"
    print webpage
    page_source = urllib.urlopen(webpage)
    soup = BeautifulSoup(page_source, 'html.parser')
    data = soup.find('table', attrs={'class': "prediction"})

    return data


print getChance("02494")
