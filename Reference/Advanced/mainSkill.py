from flask import Flask
from flask_ask import Ask, question, statement
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from selenium import webdriver
import os

app = Flask(__name__)
ask = Ask(app, "/")

@ask.intent("PredictIntent", convert={"zipcode":str})
def getChance(zipcode):


       zipcode = str(zipcode)
       print "{}".format(zipcode)
       chrome_options = webdriver.ChromeOptions()
       chrome_options.add_argument("--headless")
       browser = webdriver.Chrome(chrome_options=chrome_options)
       browser.get("https://snowdaypredictor.com/result.html?q="+zipcode)
       WebDriverWait(browser, timeout=10).until(
           lambda x: x.find_element_by_id('result-percent'))
       page_source = browser.page_source
       soup = BeautifulSoup(page_source, 'html.parser')

       data = soup.find('div', attrs={'class': 'weather_data'})
       if (not data):
           return question("Please enter a valid zip code. Please try again. ")
       else:
           percent = soup.find('span', attrs={'id': 'result-percent'})
           weData = data.text.strip()

           return question("{}% chance of a snow day. {}. Would you like to try again?".format(percent.text.strip(), weData))


if __name__ == "__main__":
   Flask.run(app,debug=True)
