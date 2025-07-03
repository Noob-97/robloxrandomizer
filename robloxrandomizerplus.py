# This tries to replicate robloxrandomizer.py but opts to take a different method to ensure the good result of games.
# Instead of checking for every random game, it checks for a random USER and then gets a random favourite game from it.
# This makes trash/default games to be far less likely to appear, and decent but also interesting new games to get - 
# - as every user has its own taste in their type of games.

# nEverMinD itS UsINg bAgDeS bEcAuSe sUch API foR GeTTiNG fAvOURiTE gAMeS DoEsN't ExiSt...

import webbrowser
import random
import requests
import time
import json

api_key = "YOUR_API_KEY"
currentID = 0

# GAME-FINDING OPTIONS:
minVisits = 1000
minUsers = 300
skipAlreadyPlayedGames = True
playedgames = json.load(open("robloxrandomizer.json", "r"))["previousGames"]

# CHALLENGE: Complete the random given ROBLOX game under its "average playtime".
# Um the "average playtime" its not actually the average playtime because it isn't accesibble to non-devs of the games
# so its pretty much... an invented number????
# This playtime value is based on the game DOORS, which's playtime has been considered to be around 45 minutes to beat and 
# at the time of writting this now has 18836 visits.
playtime = 0
playtimeConstant = 1
playtimes30 = False

if "YOUR_API_KEY" in api_key or "" in api_key:
    print('⚠️ WARNING: variable "api_key" has not been configured.\nRetrieving games essential information requires an API key for HTTP requests. Before executing any of the scripts you will need to add your own key to the "api_key" string variable inside. You can create an API key on: https://create.roblox.com/dashboard/credentials?activeTab=ApiKeysTab')


def GetIDwUser():
    userID = []
    for i in range(0, random.randint(3, 12)):
        userID.append(str(random.randint(1, 9)))
    userID = "".join(userID)
    #userID = 1349960429
    info = requests.get(f'https://badges.roblox.com/v1/users/{userID}/badges?limit=100')
    if info.status_code == 200:
        info = info.json()
        if "creator" not in str(info["data"]):
            print(f"User ID: {userID} has no badges. Retrying...")
            return -1
        else:
            luckynum = random.choice(range(0, len(info["data"])))
            placeID = info["data"][luckynum]["awarder"]["id"]
            return placeID
    else:
        print(f"User ID: {userID} doesn't exist or is unavailable. Retrying...")
        return -1

def ValidateID(universeID):
    info = requests.get(f'https://apis.roblox.com/cloud/v2/universes/{universeID}', headers={
        'x-api-key': api_key})
    if info.status_code == 200:
        info = info.json()
        if "'s Place" in info["displayName"]: 
            print(f"Skipping ID: {universeID} because it appears to be a user's default place. Retrying...")
            return -1
        elif "#####" in info["displayName"]:
            print(f"ID: {universeID} 's name is censored. Retrying...")
            return -1
        elif "[ Content Deleted ]" in info["displayName"]:
            print(f"ID: {universeID} has been moderated and is now content deleted. Retrying...")
            return -1
        elif skipAlreadyPlayedGames and playedgames.__contains__(info["displayName"]):
            print(f"ID: {universeID} has already been played and is set to be skipped. Retrying...")
            return -1
        else:
            if info["visibility"] == "PUBLIC":
                if info["ageRating"] == "AGE_RATING_17_PLUS":
                    print(f"ID: {universeID} is restricted due to 17+ content. Retrying...")
                    return -1
                elif "user" in info.keys():
                    userID = info['user'].replace("users/", "")
                    user = requests.get(f'https://apis.roblox.com/cloud/v2/users/{userID}', headers={
                    'x-api-key': api_key}).json()["name"]
                    if user in info['displayName']:
                        print(f"ID: {universeID} is a user's default place. Retrying...")
                        return -1
                    else:
                        return LoadGame(info, universeID)
                else:
                    return LoadGame(info, universeID)
            else:
                print(f"ID: {universeID} is not public. Retrying...")
                return -1
    else:
        print(f"ID: {universeID} doesn't exist or is unavailable. Retrying...")
        return -1

def LoadGame(info, universeID):
    proxyINFO = requests.get(f"https://games.roblox.com/v1/games?universeIds={universeID}").json()["data"][0]
    thumbnail = requests.get(f"https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds={universeID}&size=768x432&format=Png&isCircular=false").json()["data"][0]["thumbnails"][0]["imageUrl"]

    if proxyINFO["visits"] <= minVisits:
        print(f"ID: {universeID} has less than {minVisits} visits. Retrying...")
        return -1
    if proxyINFO["playing"] <= minUsers:
        print(f"ID: {universeID} has less than {minUsers} users playing. Retrying...")
        return -1
    
    rootID = proxyINFO["rootPlaceId"]
    text = (f"Loading ID: {rootID} | {info['displayName']}").encode('ascii', 'ignore').decode('ascii')
    print(text)

    if playtimes30 == False:
        playtime = proxyINFO["playing"] * 45 / 18836  # Average playtime based on DOORS
        print(playtime)
        if playtime <= 10:
            global playtimeConstant
            playtimeConstant = proxyINFO["playing"] * (proxyINFO["favoritedCount"] / 500000)
        playtime = playtime * playtimeConstant
        if playtimeConstant >= 500: 
            playtimeConstant = playtimeConstant / 3
            playtime = playtime / playtimeConstant
        if playtime >= 60:
            if playtimeConstant == 1:
                print(f"Playtime: {playtime} is too big by default, setting to a random value between 50 and 60 minutes.")
                playtime = random.uniform(50, 60)
            else:
                print(f"Playtime: {playtime} is too big with favourites buff, setting to a random value between 20 and 30 minutes.")
                playtime = random.uniform(20, 30)
    else:
        playtime = 30

    ogjson = json.load(open("robloxrandomizer.json", "r"))
    ogjson["playtime"] = playtime
    ogjson["currentGame"] = proxyINFO["name"]
    ogjson["favs"] = proxyINFO["favoritedCount"]
    ogjson["playing"] = proxyINFO["playing"]
    ogjson["thumbnailURL"] = thumbnail
    ogjson["previousGames"].append(proxyINFO["name"])
    json.dump(ogjson, open("robloxrandomizer.json", "w"))

    return rootID


while currentID <= 0:
    placeID = GetIDwUser()
    if placeID > 0:
        universeID = requests.get(f"https://apis.roblox.com/universes/v1/places/{placeID}/universe").json()["universeId"]
        currentID = ValidateID(universeID)
        if currentID > 0:
            break
        elif currentID == -3:
            exit(1)
        else:
            time.sleep(1)

webbrowser.open(f'roblox://placeId={currentID}')
