# Python example of scraping the web, which can be a useful tool if you can't find an API.
import urllib
from bs4 import BeautifulSoup


def getPrediction(player1,player2):
    try:
        # Use URLLIB to open a webpage
        p1 = player1.replace(" ","-").lower()
        p2 = player2.replace(" ","-").lower()
        site = urllib.urlopen("https://www.fantasypros.com/nfl/start/"+p1+"-"+p2+".php")
        # BeautifulSoup object of the HTML code
        soup = BeautifulSoup(site, 'html.parser')
        # From the html, find an h4 attribute that has the type span and the name more
        p1_percent = soup.find("span", attrs={"class":"more"})
        p1_name = str(soup.find("div", attrs={"class":"three columns"}))
        index = p1_name.find("value")
        p1_name = p1_name[index+6:]
        p1_name = p1_name.split(">")

        # Print the price as text, but without the html tags around it. .strip() removes the tags.
        p1_percent = p1_percent.text.strip()
        p1_name = p1_name[0]
        print p1_name,"is a better start, according to",p1_percent,"of fantasy experts."

    except:
        print "Sorry, a player's name must have been typed improperly. Please try again."
getPrediction("Kelvin Benjamin","Larry Fitzgerald")

