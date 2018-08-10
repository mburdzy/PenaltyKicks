from bs4 import BeautifulSoup
import urllib2
import os

class DateScraper:

    # Initialize a new scraper of the date page on espn.
    def __init__(self, date):
        self.date = date
        self.datePageUrl = "http://www.espnfc.us/scores?date=" + date
        self.beautifulSoup = None
        self.allGames = None

    def getDate(self):
        return self.date

    def getDatePageUrl(self):
        return self.getDatePageUrl

    def getBeautifulSoup(self):
        return self.beautifulSoup

    def getAllGames(self):
        return self.allGames

    # Make a BeautifulSoup of that date page
    def makeBeautifulSoup(self):
        # print BeautifulSoup(urllib2.urlopen(self.datePageUrl), 'html5lib').prettify()
        # Must use html5lib to correctly scrape the page. Doesn't work without this.
        self.beautifulSoup = BeautifulSoup(urllib2.urlopen(self.datePageUrl), 'html5lib')



    def makeListOfgames(self):
        listOfGames = []
        mainBody = self.beautifulSoup.find_all("div", {"id" :["main"]})
        # I have no idea why this works but it returns the list of all relevant games.
        for game in mainBody:
            individualGames = game.find_all("a", "primary-link")
            for individualGame in individualGames:
                listOfGames.append(individualGame["href"].split("=")[1])
        self.allGames = listOfGames

    def writeError(self, date):
        try:
            path = "D:\Projects\penaltykicks\PenaltyKicks\Errors\%s\%s\%s" % (str(date.year), str(date.month), str(date.day))
            os.makedirs(path)
        except OSError:
            if not os.path.isdir(path):
                raise
        f = open("D:\Projects\penaltykicks\PenaltyKicks\Errors\%s\%s\%s\%s" % (date.year, date.month, date.day, str(date) + '.txt'), 'w')
        f.write("DATE ERROR: " + str(date))
        f.close()



