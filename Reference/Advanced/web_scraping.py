import urllib
from bs4 import BeautifulSoup

def getPrediction(playerone, playertwo):
    try:
        print "{} and {}".format(playerone,playertwo)
        p1 = playerone.replace(" ","-",1).lower()
        p1 = p1.replace(" ","",1)
        p2 = playertwo.replace(" ","-").lower()
        web = "https://www.fantasypros.com/nfl/start/"+p1+"-"+p2+".php"
        print web
        site = urllib.urlopen(web)
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
        print(str(p1_name+" is a better start, according to "+p1_percent+" of fantasy experts. Would you like to ask again?"))

    except Exception as ex:
        print("I couldn't understand which players you said. Please make sure both players names are said clearly. Can you repeat that?")

getPrediction("Greg Olsen","Rob Gronkowski")