from DateScraper import *
from GameScraper import *
from SQL import *
from datetime import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from Tkinter import *
import Tkinter as Tk


def main():
    print "Hello World."
    #dataDownloader(datetime(2017,12, 10), datetime(2017,12, 12))
    drawPenaltyHistory("Lionel Messi")


def sumPenaltyLocations(penalties):
    penaltyMadeDict = {'left': 0,
                   'high': 0,
                   'right': 0,
                   'leftPost': 0,
                   'rightPost': 0,
                   'bar': 0,
                   'bottomLeftCorner': 0,
                   'topLeftCorner': 0,
                   'bottomRightCorner': 0,
                   'topRightCorner': 0,
                   'highCenter': 0,
                   'center': 0}
    penaltyMissedDict = {'left': 0,
                       'high': 0,
                       'right': 0,
                       'leftPost': 0,
                       'rightPost': 0,
                       'bar': 0,
                       'bottomLeftCorner': 0,
                       'topLeftCorner': 0,
                       'bottomRightCorner': 0,
                       'topRightCorner': 0,
                       'highCenter': 0,
                       'center': 0}
    for penalty in penalties:
        penaltyOutcome = penalty.__getitem__(5)
        penaltyLocation = penalty.__getitem__(6).replace(" ", "").replace(".", "").replace("tothe", "").replace("lower", "bottom")
        if penaltyOutcome == "1":
            if penaltyLocation == "bottomleftcorner":
                penaltyMadeDict['bottomLeftCorner'] += 1
            elif penaltyLocation == "topleftcorner":
                penaltyMadeDict['topLeftCorner'] += 1
            elif penaltyLocation == "bottomrightcorner":
                penaltyMadeDict["bottomRightCorner"] += 1
            elif penaltyLocation == "toprightcorner":
                penaltyMadeDict["topRightCorner"] += 1
            elif "highcentre" in penaltyLocation:
                penaltyMadeDict['highCenter'] += 1
            else:
                print "MADE:     " + penaltyLocation
                penaltyMadeDict["center"] += 1
        else:
            if "toohigh" in penaltyLocation:
                penaltyMissedDict['high'] += 1
            elif penaltyLocation == "right":
                penaltyMissedDict['right'] += 1
            elif penaltyLocation == "left":
                penaltyMissedDict['left'] += 1
            elif penaltyLocation == "thebar":
                penaltyMissedDict['bar'] += 1
            elif penaltyLocation == "leftpost":
                penaltyMissedDict['leftPost'] += 1
            elif penaltyLocation == "rightpost":
                penaltyMissedDict['rightPost'] += 1
            elif penaltyLocation == "bottomleftcorner":
                penaltyMissedDict['bottomLeftCorner'] += 1
            elif penaltyLocation == "topleftcorner":
                penaltyMissedDict['topLeftCorner'] += 1
            elif penaltyLocation == "bottomrightcorner":
                penaltyMissedDict["bottomRightCorner"] += 1
            elif penaltyLocation == "toprightcorner":
                penaltyMissedDict["topRightCorner"] += 1
            elif "highcentre" in penaltyLocation:
                penaltyMissedDict['highCenter'] += 1
            else:
                print "MISSED:   " + penaltyLocation
                penaltyMissedDict["center"] += 1

    return [penaltyMadeDict, penaltyMissedDict]

def drawPenaltyHistory(playerName):
    sqlDownload = SQL("D:\Projects\penaltykicks\PenaltyKicks\penaltyKicks.db")
    playerPenalties = sqlDownload.getPlayerData(playerName)
    penaltyData = sumPenaltyLocations(playerPenalties)
    madePenalties = penaltyData[0]
    missedPenalties = penaltyData[1]
    print penaltyData

    hPositions = 5
    vPositions = 7


    # matrix = [["", "", "", madePenalties['high'], "", "", ""],
    #           ["", "", "", madePenalties['bar'], "", "", ""],
    #           ["", "", madePenalties['topLeftCorner'], madePenalties['highCenter'], madePenalties["topRightCorner"], "",
    #            ""],
    #           [madePenalties['left'], madePenalties['leftPost'], "", madePenalties['center'], "",
    #            madePenalties['rightPost'], madePenalties['right']],
    #           ["", "", madePenalties['bottomLeftCorner'], "", madePenalties['bottomRightCorner'], "", ""]]

    matrix = [["", "", "", missedPenalties['high'], "", "", ""],
              ["", "", "", missedPenalties['bar'], "", "", ""],
              ["", "", str(madePenalties['topLeftCorner']) + "\nSaved: " + str(missedPenalties['topLeftCorner']),
               str(madePenalties['highCenter']) + "\nSaved: " + str(missedPenalties['highCenter']),
               str(madePenalties["topRightCorner"]) + "\nSaved: " + str(missedPenalties['topRightCorner']), "",
               ""],
              [missedPenalties['left'], missedPenalties['leftPost'], "", str(madePenalties['center']) + "\nSaved: " + str(missedPenalties["center"]), "",
               missedPenalties['rightPost'], missedPenalties['right']],
              ["", "", str(madePenalties['bottomLeftCorner']) + "\nSaved: " + str(missedPenalties['bottomLeftCorner']), "", str(madePenalties['bottomRightCorner']) + "\nSaved: " + str(missedPenalties['bottomRightCorner']), "", ""]]

    f = plt.figure()
    plt.title(playerName)
    tb = plt.table(cellText=matrix, loc=(0, 0), cellLoc='center')

    tc = tb.properties()['child_artists']
    for cell in tc:
        cell.set_height(1.0 / hPositions)
        cell.set_width(1.0 / vPositions)

    ax = plt.gca()
    ax.set_xticks([])
    ax.set_yticks([])
    # plt.show()

    root = Tk.Tk()
    root.wm_title("Penalty Visualization")

    Label(root, text="Start Date").grid(row=0)
    Label(root, text="End Date").grid(row=1)
    startDate = Entry(root)
    endDate = Entry(root)

    startDate.grid(row=0, column=1)
    endDate.grid(row=1, column=1)
    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.show()
    canvas.get_tk_widget().pack(side=Tk.LEFT)
    Tk.mainloop()



def dataDownloader(date1, date2):
    sqlUpload = SQL("D:\Projects\penaltykicks\PenaltyKicks\penaltyKicks.db")
    for dt in dateGenerator(date1, date2):
        currentDate = str(dt).replace("-", "")
        print "Beginning ESPN Scrape of day: " + currentDate
        currentDay = DateScraper(currentDate)
        try:
            currentDay.makeBeautifulSoup()
            currentDay.makeListOfgames()
        except:
            print "Error in DATE Scraping: " + currentDay.getDate()
            currentDay.writeError(dt)
            continue

        for gameID in  currentDay.getAllGames():
            # print gameID
            currentGame = GameScraper(gameID, currentDate)
            try:
                currentGame.makeGameBeautifulSoup()
                currentGame.makeAllCommentaryPenaltyEvents()
                currentGame.makeListOfPlayerPenaltyEvents()
            except:
                print "Error in GAME Scraping: " + currentGame.gameId
                currentGame.writeError(dt)
                continue

            currentGamePenalties = currentGame.getListOfPlayerPenaltyEvents()
            for eachPlayer in currentGamePenalties:
                try:
                    sqlUpload.addNewPlayer(eachPlayer)
                except:
                    print "SQL UPLOAD ERROR"
                    continue
        sqlUpload.commitChanges()

    sqlUpload.closeConnection()

    #
    # Test Code
    # sqlUpload = SQLUploader("D:\Projects\penaltykicks\PenaltyKicks\penaltyKicksTest.db")
    # for dt in dateGenerator(date(2013, 1, 1), date(2013, 12, 31)):
    #     currentDate = str(dt).replace("-", "")
    #     print currentDate
    #     print "Beginning ESPN Scrape of day: " + currentDate
    #     currentDay = DateScraper(currentDate)
    #     try:
    #         currentDay.makeBeautifulSoup()
    #         currentDay.makeListOfgames()
    #     except:
    #         print "Error in DATE Scraping: " + currentDay.getDate()
    #         continue
    #
    #     for gameID in  currentDay.getAllGames():
    #         print gameID
    #         currentGame = GameScraper(gameID, currentDate)
    #         try:
    #             currentGame.makeGameBeautifulSoup()
    #             currentGame.makeAllCommentaryPenaltyEvents()
    #             currentGame.makeListOfPlayerPenaltyEvents()
    #             currentGame.printListOfPlayerPenaltyEvents()
    #         except:
    #             print "Error in GAME Scraping: " + currentGame.gameId
    #             # currentGame.writeError(dt)
    #             continue
    #         currentGamePenalties = currentGame.getListOfPlayerPenaltyEvents()
    #         for eachPlayer in currentGamePenalties:
    #             try:
    #                 sqlUpload.addNewPlayerTest(eachPlayer)
    #             except:
    #                 print "SQL UPLOAD ERROR"
    #                 continue
    #         sqlUpload.commitChanges()
    # sqlUpload.closeConnection()


    # # single game test code
    # currentGame = GameScraper("411842", "20170415")
    # currentGame.makeGameBeautifulSoup()
    # currentGame.makeAllCommentaryPenaltyEvents()
    # currentGame.makeListOfPlayerPenaltyEvents()
    # currentGame.printListOfPlayerPenaltyEvents()



def dateGenerator(start, end):
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)

if __name__ == "__main__":
    main()