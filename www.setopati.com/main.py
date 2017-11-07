'''
#!/usr/bin/env python
Created on Jan 5, 2016
"""main.py: Sacraping www.setopati.com."""
__author__      = "Saurab Dulal"
__copyright__   = "..Bam.."

'''
# process of extraction
    # first get main page url
    # crul through each url in the page and store them into certain data structure
    # and using such url find the articles inside those urls

    # id = content -- pull everything out of it
    # id="header_box" -> h1 link
    # id = highlights ->samachar, mainfeatured, right_side
    # class="news_list -> li -> a"
    # class first get link of all

# possible lib's

import requests
from lxml import html
from lxml.cssselect import CSSSelector
from bs4 import BeautifulSoup
from lxml import html, etree
import re
import codecs


totalArticleCollectionDict = list()
#itemId = '14423840'
headers = {'Host': 'setopati.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'en-US,en;q=0.5',
           'Accept-Encoding': 'gzip, deflate',
           'Content-Type': 'application/x-www-form-urlencoded',
           'Connection': 'keep-alive',
           'Cache-Control': 'max-age=0'}


def startScraping():

    urlList = list()
    requestURLs = 'http://setopati.com/'       #url to scrape review

    response = requests.get(url=requestURLs,headers=headers)

    if response.status_code==200:

        data = response.text
        soup = BeautifulSoup(data)
        # print(soup)

        allMenuURLs  = soup.find_all("ul",class_="menu")
        for menu in allMenuURLs:
            raw = menu.select('li') #this will construct a list of li's and now we will extract url from li's
            for rawMenu in raw:
                # print(rawMenu.find('a').get('href'))
                urlList.append(rawMenu.find('a').get('href'))
    else:
        print(response.status_code)

    # reconstructing list to ignore home page

    urlList = urlList[1:] #ignoring the first link

    #now we need to go through each url to fetch the post text

    for eachMenu in urlList:
        outputText = forEachMenuInMenuList(eachMenu)
        # there are 30 articles per page in setopati dated to 2015/01/26
        if outputText:
            articlesLinkList = findAllArticlesInEachPage(outputText)
            # now for all this alrticle list we need find the articles
            articlesFromLink(articlesLinkList)
    print (len(totalArticleCollectionDict))


def getCategoryFromURL(url):

    category = url.split('/')
    return category[3]


def articlesFromLink(articlesLinkList):

    for link in articlesLinkList:
        url = link
        print(url)
        response = requests.get(url=url,headers=headers)
        category = getCategoryFromURL(url)

        if response.status_code==200:

            data = response.text
            soup = BeautifulSoup(data)
            # first we need to calculate no of pages for the articles and need to reconstruct the url to get articles from each page

            article  = soup.find_all(id = "newsbox")

            # soup.find("div", {"id": "articlebody"})

            for details in article:
                #create a folder and keep respective articles category in respective folder
                article = details.text.encode('latin-1', 'ignore').decode('utf-8', 'ignore')
                totalArticleCollectionDict.append({'category':category,'article':article})
                 print (article)
                 exit();
		# # writing to csv file
                # # article = 'a'
                #
                # with open('setopatiArticles.csv', 'a',encoding='utf-8') as csvfile:
                #     handler = csv.writer(csvfile)
                #     handler.writerow(['Category','Article'])
                #     a = [category,article]
                #     handler.writerow(a)

                # exit()
# I need to extract empty divs with no class or ids, and <p> tags, and <h> tags.



def findAllArticlesInEachPage(outputText):


    articlesLinkList = list()
    for x in range(1,int(outputText['numberOfPages'])):
    # for x in range(1,2):
        url = outputText['link']+'/'+str(x)
        response = requests.get(url=url,headers=headers)


        if response.status_code==200:

            data = response.text
            soup = BeautifulSoup(data)
            # first we need to calculate no of pages for the articles and need to reconstruct the url to get articles from each page

            allArticles  = soup.find_all("ul",class_="news_list")
            for articles in allArticles:
                raw = articles.select('li') #this will construct a list of li's and now we will extract url from li's
                # print(raw)
                for rawLink in raw:
                    # print(rawLink)
                    temp = rawLink.select('h2')

                    for aLink in temp:                  #article links
                        try:
                            print(aLink.find('a').get('href'))
                            articlesLinkList.append(aLink.find('a').get('href'))
                        except Exception as e:
                            print(e)
                    # allArticlesLink.append(rawLink.find('a').get('href'))
    return articlesLinkList





def forEachMenuInMenuList(requestURL):

    response = requests.get(url=requestURL,headers=headers)
    pageUrlList = list()
    if response.status_code==200:

        data = response.text
        soup = BeautifulSoup(data)
        # first we need to calculate no of pages for the articles and need to reconstruct the url to get articles from each page

        allPages  = soup.find_all("ul",class_="pagination")
        for menu in allPages:
            raw = menu.select('li') #this will construct a list of li's and now we will extract url from li's
            for rawPage in raw:
                # print(rawPage.find('a').get('href'))
                pageUrlList.append(rawPage.find('a').get('href'))

    # tempList = list()
    try:
        tempList = pageUrlList[len(pageUrlList)-1].split('/')
        totalNumberOfPages = tempList[len(tempList)-2]
        link = '/'.join(tempList[0:len(tempList)-2])
        return {'link':link,'numberOfPages':totalNumberOfPages}
    # need to send one url and total number of pages
    except Exception as e:
        # print (e)
        return None


        # return soup


def main():
    startScraping()


if __name__ == '__main__':main()
