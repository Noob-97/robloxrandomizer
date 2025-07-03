# Step 1: Enter a Roblox game with only the URL protocol
# Step 2: Get a random game ID and open it

import webbrowser
import random
import requests
import time

api_key = "YOUR_API_KEY"
currentID = 0

# GAME-FINDING OPTIONS:
minVisits = 1000

def randomID():
    universeID = []
    for i in range(0, random.randint(7, 11)):
        universeID.append(str(random.randint(1, 9)))
    universeID = "".join(universeID)
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
        else:
            if info["visibility"] == "PUBLIC":
                if info["ageRating"] == "AGE_RATING_17_PLUS":
                    print(f"ID: {universeID} is restricted due to 17+ content. Retrying...")
                    return -1
                elif "user" in info.keys():
                    userID = info['user'].replace("users/", "")
                    user = requests.get(f'https://apis.roblox.com/cloud/v2/users/{userID}', headers={
                    'x-api-key': api_key}).json()["displayName"]
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

    if proxyINFO["visits"] <= minVisits:
        print(f"ID: {universeID} has less than {minVisits} visits. Retrying...")
        return -1
    
    rootID = proxyINFO["rootPlaceId"]
    print(f"Loading ID: {rootID} | {info['displayName']}")
    return rootID


while currentID <= 0:
    currentID = randomID()
    if currentID > 0:
        break
    elif currentID == -3:
        exit(1)
    else:
        time.sleep(1)

webbrowser.open(f'roblox://placeId={currentID}')
