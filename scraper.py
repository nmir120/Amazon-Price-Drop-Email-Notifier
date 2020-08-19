import urllib.request
import bs4
import smtplib
import time
import os

email = os.environ.get('EMAILER')
password = os.environ.get('PASSWORD')

prices_list = []
url = "https://www.amazon.ca/gp/product/B074V5MMCH/ref=ox_sc_act_title_1?smid=A3TG6UNCSJC2TF&psc=1"
def price_check():
    sauce = urllib.request.urlopen(url).read()
    soup = bs4.BeautifulSoup(sauce, "html.parser")

    price = soup.find(id = "priceblock_saleprice").get_text() #price is located in span with id priceblock_saleprice
    price = float(price.replace(".", "").replace("CDN$","")) #convert html text to float, remove non-numeric
    prices_list.append(price)
    return price

def check_if_decreased(prices_list):
    if prices_list[-1] < prices_list[-2]:
        return True
    else:
        return False

def emailer(message):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(email, password)
    s.sendmail(email, "numan5383@gmail.com", message)
    s.quit()

count = 0 #to avoid index error on first run
while True:
    current_price = price_check()
    flag = check_if_decreased(prices_list)
    if count > 1:
        if flag:
            amount_decreased = prices_list[-2] - prices_list[-1]
            message = f"Your Amazon item decreased by $ {amount_decreased}!. Get it here now: {url}"
            emailer(message)
    time.sleep(43000) #once every 12 hours
    count += 1
    