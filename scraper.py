import urllib.request
import bs4
import smtplib

from os import environ as env
from dotenv import load_dotenv, find_dotenv
import constants

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

email = env.get(constants.EMAIL)
password = env.get(constants.PASSWORD)


prices_list = []

def price_check():
    url = "https://www.amazon.ca/gp/product/B074V5MMCH/ref=ox_sc_act_title_1?smid=A3TG6UNCSJC2TF&psc=1"

    sauce = urllib.request.urlopen(url).read()
    soup = bs4.BeautifulSoup(sauce, "html.parser")

    price = soup.find(id = "priceblock_saleprice").get_text() #price is located in span with id priceblock_saleprice
    price = float(price.replace(".", "").replace("CDN$","")) #convert html text to float, remove non-numeric
    prices_list.append(price)

def emailer(message):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(email,password) #dotenv to use variable instead of email and pass?