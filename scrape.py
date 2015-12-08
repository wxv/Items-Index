# Scrapes Auction House and stores today's standing offers
# Current time resolution: 1 day (without automated script)

# Current data_list format:
# Item name, user, quantity, offer price, price/unit, offer date, image ID, date accessed
from bs4 import BeautifulSoup
import requests
import re

FILE_PATH = "data/new.csv"

def process_int(s):
    return int(s.replace(',', ''))

def process_float(s):
    return float(s.replace(',', ''))


def scrape():
    data_list = []
    print("Starting...")
    for i in range(1, 30):
        response = requests.get("http://www.funnyjunk.com/item/auction/date/desc/120/%s" % i)
        html = response.content
        soup = BeautifulSoup(html)

        # Manual parsing horror is gone!
        if soup.find("li", attrs={"class": "offerNotFound"}):
            print("Done scraping!")
            break

        table = soup.find("ul", attrs={"class": "offerList"})
        for entry in table.findAll("li"):  # div offerInfo and img src
            #print(entry.prettify())
            item_name = entry.find("span", attrs={"class": "pinkLight"}).text
            if not item_name:
                print("Cancelled")
                continue

            user = entry.find("a").text
            entry_text = str(entry)
            #print(entry_text)
            quantity = process_int(re.search("Quantity: (.*)<br", entry_text).group(1))
            price = process_int(re.search("Points: (.*)<br", entry_text).group(1))
            ppu = process_float(re.search("Price per unit:: (.*)<br", entry_text).group(1))

            # Offer date not done calculating
            offer_date_text = re.search("Offered date: (.*)</div>", entry_text).group(1)

            img_src = entry.find("img")["src"]
            try:
                img_code = re.search("(.{8})\.(gif|png|jpg)", img_src).group(1)
            except:
                print("Image code error:", img_src)
                break

            print("...", item_name, user, quantity, price, ppu, offer_date_text, img_code)

        print("Done page %s\t" % i)

    return data_list

def file_write(data_list):
    # Deprecated
    import os, csv
    file_write = True

    if os.path.isfile(FILE_PATH):
        with open(FILE_PATH, 'r', newline='') as f:
            r = csv.reader(f) # Works in 'r' mode
            for row in r:
                if row[-1] == today:
                    print("Today has already been logged!")
                    file_write = False
                    break


    if file_write:
        with open(FILE_PATH, 'a', newline='') as f:
            print("Appending data...")
            wr = csv.writer(f)
            wr.writerows(data_list)


        print("Done appending!")




def main():
    scrape()



main()