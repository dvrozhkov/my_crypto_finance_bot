import requests
from bs4 import BeautifulSoup
import os

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

main_url = "https://myfin.by"
url = "https://myfin.by/crypto-rates"
req = requests.get(url, headers)
soup = BeautifulSoup(req.content, 'html.parser')

crypto_set = []


class Crypto:

    more_info = dict()

    def __init__(self, name, iname, link, cost, fact_cost, rise_in_cost, capitalisation, volume, changes):
        self.name = name
        self.iname = iname
        self.link = link
        self.cost = cost
        self.fact_cost = fact_cost
        self.rise_in_cost =  rise_in_cost
        self.capitalisation = capitalisation
        self.volume = volume
        self.changes = changes


    def __repr__(self):
        return (f"Crypto('{self.name}', '{self.iname}', '{self.link}',"
                f" '{self.cost}', '{self.cost}', '{self.rise_in_cost}',"
                f" '{self.capitalisation}', '{self.volume}', '{self.changes}')")

def parse_list_of_crypto(url):
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    data = soup.find_all("tr", {"class": "odd"})
    data += soup.find_all("tr", {"class": "even"})

    crypto_set = []

    for i in range(len(data)):
        data2 = data[i].find_all("td")
        name = data2[0].find("div").find("a").text
        iname = data2[0].find("div").find("div").text
        link = main_url + data2[0].find("div").find("a").get("href")
        cost = data2[1].text.split()[0]
        rise_in_cost = data2[1].find("div").text
        capitalisation = data2[2].text
        volume = data2[3].text
        try:
            changes = data2[4].find("span").text
        except:
            changes = "NoData"
        crypto_set.append(Crypto(name,
                                 iname,
                                 link,
                                 cost,
                                 cost,
                                 rise_in_cost,
                                 capitalisation,
                                 volume,
                                 changes))
    return crypto_set

def parse_all_crypto_pages():
    new_crypto_set = []
    new_crypto_set += parse_list_of_crypto("https://myfin.by/crypto-rates")
    new_crypto_set += parse_list_of_crypto("https://myfin.by/crypto-rates?page=2")
    new_crypto_set += parse_list_of_crypto("https://myfin.by/crypto-rates?page=3")

    for i in range(len(new_crypto_set)):
        req1 = requests.get(new_crypto_set[i].link, headers)
        soup1 = BeautifulSoup(req1.content, 'html.parser')
        data3 = soup1.find("table", {"class": "rates-table-nbrb"}).find("tbody").find_all("tr")
        for j in data3:
            q = j.find_all("td")
            if(len(q) == 1):
                new_crypto_set[i].more_info[0] = q[0].text.strip("\n").strip("\r").lstrip(" ").rstrip(" ")
            else:
                ke = q[0].text.strip("\n").strip("\r").lstrip(" ").rstrip(" ")
                if "Сейчас в обороте" not in ke:
                    new_crypto_set[i].more_info[ke] = q[1].text.strip("\n").strip("\r").lstrip(" ").rstrip(" ")

        print(new_crypto_set[i].more_info)

        #i.more_info.append(data3[0].find("td").text.strip("\n").strip("\r").lstrip(" ").rstrip(" "))
        #i.more_info.append(data3[1].find_all("td")[1].text.strip("\n").strip("\r"))
        #i.more_info.append(data3[2].find_all("td")[1].text.strip("\n").strip("\r"))
        #i.more_info.append(data3[3].find_all("td")[1].text.strip("\n").strip("\r"))
        #i.more_info.append(data3[4].find_all("td")[1].text.strip("\n").strip("\r"))
        #i.more_info.append(data3[5].find_all("td")[1].text.strip("\n").strip("\r"))
        #i.more_info.append(data3[6].find_all("td")[1].find("span").
        #                                   text.strip("\n").strip("\r").lstrip(" ").rstrip(" "))
        #i.more_info.append(data3[7].find_all("td")[1].text.strip("\n").strip("\r"))
        #i.more_info.append(data3[8].find_all("td")[1].text.strip("\n").strip("\r"))
        #print("1")

    #os.system(r'nul>output.out')
    f_out = open("output.out", "w")
    for i in range(len(new_crypto_set)):
        f_out.write(f"{new_crypto_set[i].name};{new_crypto_set[i].iname};{new_crypto_set[i].link};"
                    f"{new_crypto_set[i].cost};{new_crypto_set[i].fact_cost};"
                    f"{new_crypto_set[i].rise_in_cost};{new_crypto_set[i].capitalisation};{new_crypto_set[i].volume};"
                    f"{new_crypto_set[i].changes}\n")
        for k, v in new_crypto_set[i].more_info.items():
            f_out.write(f"{k}:{v};")
        f_out.write("\n")

parse_all_crypto_pages()