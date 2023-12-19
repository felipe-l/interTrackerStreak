from modules import databaseFunctions
from modules import riotApi
import time
from urllib.parse import quote
from config import PLAYERS_TO_TRACK as players

def detectStreak(resultList: list, lastGame: str, lastStreakCount: int) -> dict:
    streakCount = 0
    newLastGame, streakTypeWin = resultList[0]
    connected = False
    for gameId,winStreak in resultList:
        if winStreak == streakTypeWin:
            if gameId == lastGame:
                connected = True
                break
            else:
                streakCount += 1
        else:
            break

    #No changes, prevents database update when not necessary
    if connected and streakCount == 0:
        return None

    totalStreak = streakCount
    if connected:
        totalStreak += lastStreakCount

    return {"streakCount": streakCount, "winStreak": streakTypeWin, "streakChanged": not connected, "lastGame": newLastGame}

def setStreak(player: str, tagLine: str):
    puuid = riotApi.getPuuidByTagLine(quote(player), tagLine)
    games = riotApi.getGamesByPuuid(puuid)
    matchDetails = riotApi.getMatchDetails(games)
    matchResults = riotApi.getGameResults(matchDetails, puuid)

    lastGame = databaseFunctions.selectUserData(player)
    print("LAST GAME", lastGame)
    lastStreakCount = 0
    if lastGame is not None:
        lastStreakCount = lastGame[2]
        lastGame = lastGame[4]

    streakDetails = detectStreak(matchResults, lastGame, lastStreakCount)
    if streakDetails is not None:
        if lastGame is None:
            databaseFunctions.insertUserData(player, streakDetails["winStreak"], streakDetails["streakCount"], streakDetails["lastGame"], "false")
        else:
            # Check if changes in order to prevent posting on discord multiple times, we don't want to change false.
            if str(lastGame) != str(streakDetails["lastGame"]):
                print("Update on summoner:", sum)
                databaseFunctions.updateUserStreak(player, streakDetails["winStreak"], streakDetails["streakCount"], streakDetails["lastGame"], "false")

    return streakDetails

def updateSummonerStreaks(summoners: dict):
    for summ, tag in summoners.items():
        time.sleep(30)
        try:
            setStreak(summ, tag)
        except Exception as e:
            print("Failed to set streak:", summ)
            print(e)

def runMain():
    while True:
        updateSummonerStreaks(players)
        time.sleep(120)
runMain()