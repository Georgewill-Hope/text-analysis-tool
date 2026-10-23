import yfinance as yf
from datetime import datetime
import requests

def extractBasicInfo(data):
    keysToExtract = ["longName", "website", "sector", "fullTimeEmployees", "marketCap", "totalRevenue", "trailingEps"]

    basicInfo = {}

    for key in keysToExtract:
        if key in data:
            basicInfo[key] = data[key]   
        else:
            basicInfo[key] = ""
            
    return basicInfo

def getPriceHistory(company):
    historyDf = company.history(period='12mo')
    prices = historyDf["Open"].to_list()
    dates = historyDf.index.strftime("%y-%m-%d").to_list()
    return{
        "price": prices,
        "date": dates
    }

def getEarningsDates(company):
    earningsDatesDf = company.earnings_dates
    allDates = earningsDatesDf.index.strftime("%y-%m-%d").to_list()
    dateObjects = [datetime.strptime(date,"%y-%m-%d") for date in allDates]
    currentDate = datetime.now()
    futureDates = [date.strftime("%y-%m-%d") for date in dateObjects if date > currentDate]
    return futureDates

def getCompanyNews(company):
    companySymbol = company.info["symbol"]
    search = yf.Search(
        query=companySymbol,
        news_count=10
    )
    newsList = search.news

    allNewsArticles = []
    for newsDict in newsList:
        newsDictToAdd = {
            "title": newsDict["title"],
            "link": newsDict["link"]
        }
        allNewsArticles.append(newsDictToAdd)
    return allNewsArticles
    
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36"
}
def extractCompanyNewsArticles(newsArticle):
    url = newsArticle[0]["link"]
    page = requests.get(url, headers=headers)
    print(page.text)

def getCompanyStockInfo(tickerSymbol):
    # Get data from yahoo finance API
    company = yf.Ticker(tickerSymbol)

    # Get basic info on comapny
    basicInfo = extractBasicInfo(company.info)
    priceHistory = getPriceHistory(company)
    futureEarningsDates = getEarningsDates(company)
    newsArticle = getCompanyNews(company)
    extractCompanyNewsArticles(newsArticle)

getCompanyStockInfo("MSFT")