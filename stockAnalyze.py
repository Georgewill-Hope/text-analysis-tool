import yfinance as yf
from datetime import datetime

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
    historyDf = company.history(period='1mo')
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
    newsList = company.news
    allNewsArticles = []
    for newsDict in newsList:
        newsDictToAdd = {
            "title": newsDict["title"],
            "link": newsDict["link"]
        }
        allNewsArticles.append(newsDictToAdd)
    return allNewsArticles
    

def getCompanyStockInfo(tickerSymbol):
    # Get data from yahoo finance API
    company = yf.Ticker(tickerSymbol)

    # Get basic info on comapny
    basicInfo = extractBasicInfo(company.info)
    priceHistory = getPriceHistory(company)
    futureEarningsDates = getEarningsDates(company)
    newsArticle = getCompanyNews(company)

getCompanyStockInfo("MSFT")