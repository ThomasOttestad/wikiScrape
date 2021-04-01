import requests
from bs4 import BeautifulSoup
import random
import json

# print("hello world")


# url = ""
# startinurl = "https://en.wikipedia.org/wiki/Same_Same"




# # result = requests.get("https://en.wikipedia.org/wiki/Same_Same")

# if(result.status_code != 200):
#     print("Error with get request")
#     exit()

# src = result.content

# soup = BeautifulSoup(src, 'lxml')


# links = soup.find_all('a')


def getText(result):
    wiki = BeautifulSoup(result.text,"html.parser")
    text = []
    for i in wiki.select('p'):
        text.append(i.getText().strip('\t\r\n,.!"+`/'))
    return text




def parseData(data, dict):
    wordList = []
    for line in data:
        wordList.append(line.split())
        # break
    
    for sublist in wordList:
        sublist.sort()
    worddict = dict

    for sublist in wordList:
        for word in sublist:
            if (word in worddict.keys()):
                temp = worddict.get(word)
                worddict.update({word: temp+1})

            else:
                worddict.update({word: 1})
    return worddict


def writeDataToFile(Parseddata):
    with open("data.json", "w") as file:
        json.dump(Parseddata, file)
    

# data = getText(result)
# Parseddata = parseData(data)
# writeDataToFile(Parseddata)

def retriveData():
    with open("data.json", "r") as file:
        data = json.load(file)
        return data








def scrapeWikiArticle(url):
    # return response
    response = requests.get(
        url=url,
    )

    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find(id="firstHeading")

    allLinks = soup.find(id="bodyContent").find_all("a")
    random.shuffle(allLinks)
    linkToScrape = 0
    for link in allLinks:
        # We are only interested in other wiki articles
        if link['href'].find("/wiki/") == -1: 
            continue
        # Use this link to scrape
        linkToScrape = link
        break
    # return response, linkToScrape
    # scrapeWikiArticle("https://en.wikipedia.org" + linkToScrape['href'])
    return response, linkToScrape

# scrapeWikiArticle("https://en.wikipedia.org/wiki/Web_scraping")



def scrapeMulti(url, counter):
    response, url = scrapeWikiArticle(url)
    # print(response)
    print(url)
    previousData = retriveData()

    data = getText(response)
    Parseddata = parseData(data ,previousData)
    writeDataToFile(Parseddata)
    
    if counter > 2:
        exit()
    else:
        counter += 1
        scrapeMulti(url, counter)






scrapeMulti("https://en.wikipedia.org/wiki/Same_Same", 0)


