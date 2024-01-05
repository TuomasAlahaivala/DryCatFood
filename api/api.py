from flask import Flask
import requests
import threading
from bs4 import BeautifulSoup
base_urls = {"https://www.zooplus.fi": "/shop/kissat/kuivaruoka", "https://www.bitiba.fi": "/shop/kissanruoka/kuivaruoka"}

app = Flask(__name__)
if __name__ == "__main__":
    app.run(debug=True)


@app.route('/api/ml')
def predict():
    siteThreads = []
    nutritional_values = []
    for base_url, part in base_urls.items():
        thread = threading.Thread(target=fetchFromService, args=(base_url, part, nutritional_values,))
        thread.start()
        siteThreads.append(thread)

    for siteThread in siteThreads:
        siteThread.join()

    return {"nutritional_values": nutritional_values}


def getSiteUrl(site, part, page):
    if page == 1:
        return site + part
    return site + part + '?p=' + str(page)


def fetchFromService(site, part, nutritional_values):
    page = 1

    all_product_urls = []
    while True:
        t1 = threading.Thread(target=getPageProductUrls, args=(site, part, page, all_product_urls,))
        page = page + 1
        t2 = threading.Thread(target=getPageProductUrls, args=(site, part, page, all_product_urls,))
        page = page + 1
        t3 = threading.Thread(target=getPageProductUrls, args=(site, part, page, all_product_urls,))
        page = page + 1

        t4 = threading.Thread(target=getPageProductUrls, args=(site, part, page, all_product_urls,))
        page = page + 1

        t5 = threading.Thread(target=getPageProductUrls, args=(site, part, page, all_product_urls,))
        page = page + 1

        t6 = threading.Thread(target=getPageProductUrls, args=(site, part, page, all_product_urls,))
        page = page + 1

        all_product_urls_len = all_product_urls.__len__()
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()

        if all_product_urls_len == all_product_urls.__len__(): break

    chunks = chunkIt(all_product_urls, 10)
    threads = []
    for chunk in chunks:
        t = threading.Thread(target=getProductUrlNutritional_values, args=(chunk, nutritional_values,))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()


def fun(product_url):
    if ("kuivaruoka" in product_url):
        return True
    else:
        return False


def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out


def getPageProductUrls(site, part, page, all_product_urls):
    url = getSiteUrl(site, part, page)
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    # Extract product URLs
    product_urls = [site + a['href'] for a in
                    soup.find_all('a', class_='ProductListItem-module_productInfoTitleLink__NAbwA')]

    all_product_urls.extend(filter(fun, product_urls))

def getConvertedKiloPrice(priceString, product_url):
    try:
        correctedPriceString = priceString \
            .replace('€', '') \
            .replace('kg', '') \
            .replace('(', '') \
            .replace(')', '') \
            .replace(',', '.') \
            .replace('/', '') \
            .replace('kappale', '') \
            .replace('l', '') \
            .strip()

        correctedPriceString = "".join(correctedPriceString.split())
        return float(correctedPriceString)
    except (ValueError):
        raise ValueError("Erikoiner priceString " + priceString + "/" + correctedPriceString + "/" + product_url)

def resolveKiloPrice(product_soup, product_url, product_response_text):

    try:
        kilo_prices = product_soup.findAll("span", class_="z-price__note z-price__note--suffix")
        price = None
        price_int = None
        kilo_price = None
        if kilo_prices is not None:
            for kilo_price in kilo_prices:
                price_int = getConvertedKiloPrice(kilo_price.get_text(), product_url)
                if price is None:
                    price = price_int
                    continue
                if price > price_int:
                    price = price_int
                    continue
        return price
    except (TypeError):
        raise TypeError("Virhe Kilopricen selvittämisessä" + str(price) +"/" + str(price_int) + "/" + str(kilo_price))
    except (AttributeError):
        raise AttributeError("AttributeError " + product_url)

def getProductUrlNutritional_values(all_product_urls, nutritional_values):
    for product_url in all_product_urls:
        procuctInfo = {}
        print(product_url)

        procuctInfo["Product URL"] = product_url
        product_response = requests.get(product_url)
        product_response_text = product_response.text
        product_soup = BeautifulSoup(product_response.text, "html.parser")

        title = product_soup.find("h1")
        procuctInfo["title"] = title.get_text()

        procuctInfo["kilo_price"] = resolveKiloPrice(product_soup,product_url,product_response_text)

        # Extract nutritional information (adjust this based on the actual HTML structure)
        nutrition_info = product_soup.find("table", class_="Table_table__jYGxt")
        if nutrition_info is None:
            continue
        nutritions = nutrition_info.findAll("tr")
        if nutritions is None:
            continue
        for nutrition in nutritions:
            values = nutrition.findAll("td")
            nutrition_name = values[0].get_text()
            nutrition_value = values[1].get_text().replace('%', '').strip()
            procuctInfo[nutrition_name] = nutrition_value

        nutritional_values.append(procuctInfo)
