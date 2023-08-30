from . import databaseFunctions
from . import riotApi

players = ["roxas"]

def detectStreak(resultList: list, lastGame: str) -> dict:
    streakCount = 0
    newLastGame, streakTypeWin = resultList[0]
    connected = False
    for gameId,winStreak in resultList:
        if gameId == lastGame:
            connected = True
            break
        else:
            if winStreak == streakTypeWin:
                streakCount += 1
            else:
                break

    #No changes, prevents database update when not necessary
    if connected and streakCount == 0:
        print("NO CHANGES")
        return None

    totalStreak = streakCount
    if connected:
        # ADD DATABASE VALUE AND CHANGE STREAK COUNT
        totalStreak += 0
    else:
        # STREAK TYPE CHANGED SO ADD STREAK TYPE AND TOTALSTREAK TO DB
        pass
    return {"streakCount": streakCount, "winStreak": streakTypeWin, "streakChanged": not connected, "lastGame": newLastGame}
def setStreak(player: str, ):
    puuid = riotApi.getSummonerPuuid(player)
    games = riotApi.getGamesByPuuid(puuid)
    matchDetails = riotApi.getMatchDetails(games)
    matchResults = riotApi.getGameResults(matchDetails, puuid)

    lastGame = databaseFunctions.selectUserData(player)
    if lastGame is not None:
        lastGame = lastGame[-1]

    streakDetails = detectStreak(matchResults, lastGame)

    print("DATA HERE:", lastGame, streakDetails)
    if streakDetails is not None:
        if lastGame is None:
            print("ADDED TO DB")
            databaseFunctions.insertUserData(player, streakDetails["winStreak"], streakDetails["streakCount"], streakDetails["lastGame"])
        else:
            print("UPDATED DB")
            databaseFunctions.updateUserStreak(player, streakDetails["winStreak"], streakDetails["streakCount"], streakDetails["lastGame"])

    return streakDetails

def updateSummonerStreaks(summoners):
    for summ in summoners:
        setStreak(summ)