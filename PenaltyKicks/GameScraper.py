from bs4 import BeautifulSoup
from PlayerPenaltyEvent import *
import urllib2
import regex as re
import os

class GameScraper:
    def __init__(self, gameId, date):
        self.gameId = gameId
        self.gameUrl = "http://www.espnfc.us/commentary?gameId=" + str(gameId)
        self.gameBeautifulSoup = None
        self.allCommentaryPenaltyEvents = None
        self.listOfPlayerPenaltyEvents = []
        self.gameDate = date

    def getGameId(self):
        return self.gameId

    def getGameUrl(self):
        return self.gameUrl

    def getGameBeautifulSoup(self):
        return self.gameBeautifulSoup

    def getAllCommentaryPenaltyEvents(self):
        return self.allCommentaryPenaltyEvents

    def getListOfPlayerPenaltyEvents(self):
        return self.listOfPlayerPenaltyEvents

    def printPenaltyEvent(self, penaltyEvent):
        print "Player: " + penaltyEvent.getPlayerName() \
              + " Foot: " + str(penaltyEvent.getFoot()) \
              + " Team: " + str(penaltyEvent.getTeam()) \
              + " GameID: " + str(penaltyEvent.getGameId()) \
              + " Outcome: " + str(penaltyEvent.getOutcome()) \
              + " Direction: " + str(penaltyEvent.getDirection())

    def printListOfPlayerPenaltyEvents(self):
        print "Total number of penalties: " + str(len(self.listOfPlayerPenaltyEvents))
        for penaltyEvent in self.listOfPlayerPenaltyEvents:
            print "Player: " + penaltyEvent.getPlayerName() \
                  + " Foot: " + str(penaltyEvent.getFoot()) \
                  + " Team: " + str(penaltyEvent.getTeam()) \
                  + " GameID: " + str(penaltyEvent.getGameId()) \
                  + " Outcome: " + str(penaltyEvent.getOutcome()) \
                  + " Direction: " + str(penaltyEvent.getDirection())

    # Make a BeautifulSoup of the game page
    def makeGameBeautifulSoup(self):
        # print BeautifulSoup(urllib2.urlopen(self.gameUrl), 'html5lib').prettify()
        # Must use html5lib to correctly scrape the page. Doesn't work without this.
        self.gameBeautifulSoup = BeautifulSoup(urllib2.urlopen(self.gameUrl), 'html5lib')

    def makeAllCommentaryPenaltyEvents(self):
        events = self.gameBeautifulSoup.find_all("td", class_="game-details")
        # print "\nPenalties:\n"
        self.allCommentaryPenaltyEvents = self.gameBeautifulSoup.find_all(text = re.compile("(?i)penalty"), class_="game-details")
        # print self.allCommentaryPenaltyEvents

    def makeListOfPlayerPenaltyEvents(self):
        allPenaltyEvents = []
        for penaltyEvent in self.allCommentaryPenaltyEvents:
            allPenaltyEvents.append(str(penaltyEvent))

        # /TODO figure out why this duplicates
        allPenaltyEvents = allPenaltyEvents[:-1]
        # get the player name
        for penaltyEvent in allPenaltyEvents:
            # added because going back to 2015 they seemed to use 'penalty area' rather than box.
            if "penalty area" in penaltyEvent:
                continue

            elif "Penalty saved!" in penaltyEvent:
                # This is a Penalty Saved
                saveFeatures = penaltyEvent.split("!")[-1][:-17]
                playerName = saveFeatures.split("(")[0][1:-1]
                currentPlayer = PlayerPenaltyEvent(playerName)
                currentPlayer.setFoot(re.findall("\w+(?=\s*foot[^/])", saveFeatures)[0])
                currentPlayer.setTeam(saveFeatures[saveFeatures.find("(") + 1:saveFeatures.find(")")])
                currentPlayer.setGameId(self.gameId)
                currentPlayer.setOutcome(0)
                direction = saveFeatures.split("in the")[-1]
                currentPlayer.setDirection(direction)
                currentPlayer.setPenaltyEventString(penaltyEvent)
                currentPlayer.setDate(self.gameDate)
                self.listOfPlayerPenaltyEvents.append(currentPlayer)

            elif "Penalty missed!" in penaltyEvent:
                # This is penalty missed
                if ("Bad penalty by" in penaltyEvent):
                    missedFeatures = penaltyEvent.split("Bad penalty by")[-1]
                    playerName = missedFeatures.split("(")[0][1:-1]
                    currentPlayer = PlayerPenaltyEvent(playerName)
                    currentPlayer.setFoot(re.findall("\w+(?=\s*foot[^/])", missedFeatures)[0])
                    currentPlayer.setTeam(missedFeatures[missedFeatures.find("(") + 1:missedFeatures.find(")")])
                    currentPlayer.setGameId(self.gameId)
                    currentPlayer.setOutcome(0)
                    if ("post" in missedFeatures):
                        currentPlayer.setDirection(re.findall("\w+(?=\s*post[^/])", missedFeatures)[0] + " post")

                    elif ("is close" in missedFeatures):
                        direction = missedFeatures.split("to the")[-1].split(".")[0]
                        currentPlayer.setDirection(direction)

                    elif ("misses" in missedFeatures):
                        direction = missedFeatures.split("to the")[-1].split(".")[0]
                        currentPlayer.setDirection(direction)
                    else:
                        direction = re.findall("^.* is (.*)\. ", missedFeatures)[0]
                        currentPlayer.setDirection(direction)
                    currentPlayer.setPenaltyEventString(penaltyEvent)
                    currentPlayer.setDate(self.gameDate)
                    self.listOfPlayerPenaltyEvents.append(currentPlayer)
                # Weird thing where if it hits a post for some reason it seems to do a different type of message. Idk why
                ## /TODO: fix the post error handling if it is true that this only happens during posts.
                else:
                    match = re.search("[0-9]\. ((?:(?!\.).)*)", penaltyEvent)
                    if match:
                        missedFeatures = penaltyEvent[2 + match.start():] + penaltyEvent[:match.end()]
                    else:
                        missedFeatures = penaltyEvent.split(").")[-1]
                    playerName = missedFeatures.split("(")[0][1:-1]
                    currentPlayer = PlayerPenaltyEvent(playerName)
                    currentPlayer.setFoot(re.findall("\w+(?=\s*foot[^/])", missedFeatures)[0])
                    currentPlayer.setTeam(missedFeatures[missedFeatures.find("(") + 1:missedFeatures.find(")")])
                    currentPlayer.setGameId(self.gameId)
                    currentPlayer.setOutcome(0)
                    if ("post" in missedFeatures):
                         currentPlayer.setDirection(re.findall("\w+(?=\s*post[^/])", missedFeatures)[0] + " post")
                    elif ("bar" in missedFeatures):
                        currentPlayer.setDirection(re.findall("\w+(?=\s*bar[^/])", missedFeatures)[0] + " bar")
                    elif ("is close" in missedFeatures):
                        direction = missedFeatures.split("to the")[-1].split(".")[0]
                        currentPlayer.setDirection(direction)
                    else:
                        direction = re.findall("^.* is (.*)\. ", missedFeatures)[0]
                        currentPlayer.setDirection(direction)
                    currentPlayer.setPenaltyEventString(penaltyEvent)
                    currentPlayer.setDate(self.gameDate)
                    self.listOfPlayerPenaltyEvents.append(currentPlayer)

            elif "Goal!" in penaltyEvent and "penalty" in penaltyEvent:
                goalFeatures = penaltyEvent.split(".")[1]
                try:
                    playerName = goalFeatures.split("(")[0][1:-1]
                    currentPlayer = PlayerPenaltyEvent(playerName)
                    currentPlayer.setFoot(re.findall("\w+(?=\s*foot[^/])", goalFeatures)[0])
                    currentPlayer.setTeam(goalFeatures[goalFeatures.find("(") + 1:goalFeatures.find(")")])
                    currentPlayer.setGameId(self.gameId)
                    currentPlayer.setOutcome(1)
                    direction = goalFeatures.split("to the")[-1]
                    currentPlayer.setDirection(direction)
                    currentPlayer.setPenaltyEventString(penaltyEvent)
                    currentPlayer.setDate(self.gameDate)
                    self.listOfPlayerPenaltyEvents.append(currentPlayer)
                except:
                    if re.search("(\w [0-9]\. (.*)\.)", penaltyEvent, overlapped=True):
                        goalFeatures = re.search("(\w [0-9]\. (.*)\.)", penaltyEvent, overlapped=True).group()[4:]
                    elif re.search("[0-9]\)\. (.*)\.", penaltyEvent, overlapped=True):
                        goalFeatures = re.search("([0-9]\)\. (.*)\.)", penaltyEvent, overlapped=True).group()[3:]
                    else:
                        goalFeatures = re.search("([A-z]\. [0-9]\. (.*)\.)", penaltyEvent, overlapped=True).group()[5:]
                    playerName = goalFeatures.split("(")[0][1:-1]
                    currentPlayer = PlayerPenaltyEvent(playerName)
                    currentPlayer.setFoot(re.findall("\w+(?=\s*foot[^/])", goalFeatures)[0])
                    currentPlayer.setTeam(goalFeatures[goalFeatures.find("(") + 1:goalFeatures.find(")")])
                    currentPlayer.setGameId(self.gameId)
                    currentPlayer.setOutcome(1)
                    direction = goalFeatures.split("to the")[-1]
                    currentPlayer.setDirection(direction)
                    currentPlayer.setPenaltyEventString(penaltyEvent)
                    currentPlayer.setDate(self.gameDate)
                    self.listOfPlayerPenaltyEvents.append(currentPlayer)

            elif "penalty kick" in penaltyEvent:
                playerName = re.search("(\w+\s\w+)[\w\s]+penalty kick", penaltyEvent).group(1)
                currentPlayer = PlayerPenaltyEvent(playerName)
                currentPlayer.setFoot(re.findall("\w+(?=\s*foot)", penaltyEvent)[0])
                currentPlayer.setTeam(None)
                currentPlayer.setGameId(self.gameId)
                if "scores" in penaltyEvent:
                    currentPlayer.setOutcome(1)
                else:
                    currentPlayer.setOutcome(0)
                if "crossbar" in penaltyEvent:
                    if "hits" in penaltyEvent:
                        currentPlayer.setDirection("the bar")
                    else:
                        currentPlayer.setDirection("too high")

                elif "wide" in penaltyEvent:
                    currentPlayer.setDirection(re.search("(?<=wide\s)(\w+)", penaltyEvent).group(1))
                else:
                    currentPlayer.setDirection(re.search("(?<=foot)(.*)(?= and )", penaltyEvent).group(1))
                currentPlayer.setPenaltyEventString(penaltyEvent)
                currentPlayer.setDate(self.gameDate)
                self.listOfPlayerPenaltyEvents.append(currentPlayer)




    def writeError(self, date):
        #Write the game Page HTML to a file
        try:
            path = "D:\Projects\penaltykicks\PenaltyKicks\Errors\%s\%s\%s" % (str(date.year), str(date.month), str(date.day))
            os.makedirs(path)
        except OSError:
            if not os.path.isdir(path):
                raise
        f = open("D:\Projects\penaltykicks\PenaltyKicks\Errors\%s\%s\%s\%s" % (str(date.year), str(date.month), str(date.day), self.gameId + '.txt'), 'w')
        f.write("GAME ERROR: " + self.gameId)
        f.close()

