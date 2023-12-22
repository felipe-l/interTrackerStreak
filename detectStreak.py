from modules import databaseFunctions
from modules import riotApi
import time
from urllib.parse import quote
from config import PLAYERS_TO_TRACK as players

def detectStreak(resultList: list, lastGame: str, lastStreakCount: int, lastChampionPick: str) -> dict:
    streakCount = 0
    newLastGame, newStreakTypeWin, newLastChampionPick = resultList[0]
    connected = False
    for currGameId, currStreakTypeWin, currChampionPick in resultList:
        if currStreakTypeWin == newStreakTypeWin:
            if currGameId == lastGame:
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

    return {"streakCount": streakCount, "winStreak": newStreakTypeWin, "streakChanged": not connected, "lastGame": newLastGame, "lastChampion": newLastChampionPick}

def setStreak(player: str, tagLine: str):
    puuid = riotApi.getPuuidByTagLine(quote(player), tagLine)
    games = riotApi.getGamesByPuuid(puuid)
    matchDetails = riotApi.getMatchDetails(games)
    matchResults = riotApi.getGameResults(matchDetails, puuid)

    lastGame = databaseFunctions.selectUserData(player)
    print("LAST GAME", lastGame)
    lastStreakCount = 0
    lastChampionPick = None
    if lastGame is not None:
        lastStreakCount = lastGame[2]
        lastGame = lastGame[4]
        lastChampionPick = lastGame[6]

    streakDetails = detectStreak(matchResults, lastGame, lastStreakCount, lastChampionPick)
    if streakDetails is not None:
        if lastGame is None:
            databaseFunctions.insertUserData(player, streakDetails["winStreak"], streakDetails["streakCount"], streakDetails["lastGame"], "false", streakDetails["lastChampion"])
        else:
            # Check if changes in order to prevent posting on discord multiple times, we don't want to change false.
            if str(lastGame) != str(streakDetails["lastGame"]):
                print("Update on summoner:", player)
                databaseFunctions.updateUserStreak(player, streakDetails["winStreak"], streakDetails["streakCount"], streakDetails["lastGame"], "false", streakDetails["lastChampion"])

    return streakDetails

def updateSummonerStreaks(summoners: dict):
    for summ, tag in summoners.items():
        time.sleep(30)
        try:
            setStreak(summ, tag)
        except Exception as e:
            print("Failed to set streak:", summ)
            print(e)
            import traceback
            traceback.print_exc()

def runMain():
    while True:
        updateSummonerStreaks(players)
        time.sleep(120)
runMain()