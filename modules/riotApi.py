import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": "RGAPI-3883ae21-2e9a-4376-8d76-593348fa0bee"
}

def getSummonerPuuid(summoner: str, server: str = "na1") -> str:
    r = requests.get("https://" + server + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner, headers=headers)
    return r.json()['puuid']

def getSummonerByPuuid(puuid: str, server: str = "na1") -> str:
    r = requests.get("https://" + server + ".api.riotgames.com/lol/summoner/v4/summoners/by-puuid/" + puuid, headers=headers)
    return r.json()

def getGamesByPuuid(puuid: str, queue: int = 420, region: str = "americas", start: int = 0, count: str = 20):
    r = requests.get("https://" + region + ".api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuid + "/ids?" + str(queue) + "start=" + str(start) + "&count=" + str(count), headers=headers)
    return r.json()

def getMatchDetails(games: list, region: str = "americas"):
    results = []
    for game in games:
        r = requests.get("https://" + region + ".api.riotgames.com/lol/match/v5/matches/" + game, headers=headers)
        results.append(r.json()["info"])
    return results

def getGameResults(games: list, puuid: str):
    result = []
    for game in games:
        gameId = game['gameId']
        for player in game["participants"]:
            if player['puuid'] == puuid:
                result.append({gameId: bool(player['win'])})
    return result

# puuid = getSummonerPuuid("bbbitmap")
# games = getMatchDetails(getGamesByPuuid(puuid))
# print(getGameResults(games, puuid))
#TEst
