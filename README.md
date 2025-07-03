# robloxrandomizer
A random roblox game searcher with an included GUI made with Tkinter in Python (gui only available for challenge mode).

### How to install
**⚠️ WARNING:** This is a python program. Having a recent version of python is required for the script to run. You can download Python here: https://www.python.org/downloads/

If you wish to use the Challenge Mode GUI version (refer to "Challenge Mode" below), during the installation please check "tcl/tk and IDLE" in "Optional Features" for installing tkinter. You can do this even if you already have python installed, if you still have this installer file and go to "Modify".

These scripts also uses certain modules like requests and Pillow. If you don't have them already, you may install them using pip.
```
pip install requests pillow
```
### How to USE
Once having downloaded the repo by zip install [https://github.com/Noob-97/robloxrandomizer/archive/refs/heads/main.zip] or by other method, you can run robloxrandomizer.py, robloxrandomizerplus.py or \__main__\.py

When robloxrandomizer.py or robloxrandomizerplus.py are ran, a console window will appear with information about all the searched and discarded IDs. The scripts include a criteria for game-finding that has been implemented to avoid executing a non-accesible game or people's default places (as they appear very often), but you can of course change them according to your needs.

**➡️ IMPORTANT:** Retrieving games' essential information requires an API key for HTTP requests. Before executing any of the scripts you'll need to add your own key to the "api_key" string variable inside. You can create an API key on: https://create.roblox.com/dashboard/credentials?activeTab=ApiKeysTab

The difference between robloxrandomizer.py and robloxrandomizerplus.py are their game-finding method, the basic version only searching with pure random number IDs, and the plus version guaranteeing a selection of games with more quality and popularity being based of random people's badges.

If you want a fully random game selection of Roblox, choose robloxrandomizer.py.
If you prefer to just search a bunch of random games to play and have fun while maybe discovering other cool games you didn't know about, choose robloxrandomizerplus.py

| Game-Finding Criteria                 | About/Info                                                                                                                    |
| ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| "'s Place" in info["displayName"] & user in info['displayName']    | Not recommended to remove. Prevents someone's default place to appear on the randomizer, as they as very common to encounter. |
| "#####" in info["displayName"]                  | Not recommended to remove. Omits games with censored titles that are probable of also being default places, but with the owner's username hashtagged.
| "[ Content Deleted ]" in info["displayName"]    | Not recommended to remove. Skip games deleted by Roblox's moderation team, since they are unavailable.                        |
| info["visibility"] == "PUBLIC"        | Not recommended to remove. Doesn't go through games that aren't public yet and non-accesible.                                 |
| info["ageRating"] == "AGE_RATING_17_PLUS"     | Only remove if your account is registered as +17. This setting has been made to make sure all games selected from the randomizer are playable under the average account. |
| minVisits = int                       | Optional. Discards games that don't meet the minimum visits threshold that serve as a "quality" minimum. Don't recommended to set over 10 in robloxrandomizer.py. |
| minUsers = int                       | Optional. Only available in robloxrandomizerplus.py. Discards games that don't meet the minimum visits threshold that serve as an extra "quality" measure. |
| skipAlreadyPlayedGames = bool       | Optional. Only available in robloxrandomizerplus.py. Skips games that have already been selected once before. This list is on robloxrandomizer.json. To reset the game list, it must be done by manually editing the json file and deleting all the list's elements. This is handled automatically when ran on challenge mode with \__main__\.py |
| playtimes30 = bool       | Only for Challenge Mode. Found on robloxrandomizerplus.py. Sets the playtime timers of all games to 30 minutes. Is best to activate this option if you're feeling like the playtime times are getting too unmanageable. |

### Challenge Mode
How many games are you able to beat within their expected playtime? Are you truly a Roblox expert?

To start Challenge Mode, open \__main__\.py and a GUI window will appear on the top-right side of your screen. Click "start" to start searching games. Challenge Mode uses robloxrandomizerplus.py by default.

The Challenge consists on beating (or considered completed) the most amount of games under a certain time calculated with the Players Playing and Game Favourited stats of the game, representing its average playtime (as you can't obtain a game's avearge playtime directly). 

When a game loads, you'll have the option to mark the game as completed or to skip it at any time. If you opt to skip a game or you fail to complete it over the specified time, you fail and a new game is searched to play. The goal is to have more games completed than failed, represented by the red and green number counters.

Playtimes are based of Roblox's game DOORS, which the average time to beat for a normal player would be of 45 minutes and at the time of writing this, it has 18836 active players. However, sometimes this isn't enough and playtimes are too short. A favorites buff has been implemented so that if a playtime is below 10 minutes, its amount of favorites are able to give it a boost, but now there's the probability of playtimes being too long.

If a playtime is longer than an hour by default, it resets to be a random number between 50 and 60 minutes.
But if it's longer because of the favorites buff, it will reset to be a random number between 20 and 30 minutes.

```
playtimes30 = False
playtimeBUFF = 1
playtime = ([activePlayers] * 45 / 18836) * playtimeBUFF
if playtime <= 10:
    playtimeBUFF = [activePlayers] * ([favorites] / 500000)
    playtime *= playtimeBUFF
if playtimeBUFF >= 500:
    playtimeBUFF /= 3
    playtime /= playtimeBUFF

if playtime >= 60:
    if playtimeConstant == 1:
        playtime = random.uniform(50, 60)
    else:
        playtime = random.uniform(20, 30)
```

Since this system is way too messy and sometimes too unreliable, an option for just setting every game's playtime to 30 minutes has been added. Use this if you don't want the challenge times to get too unfair.
```
playtimes30 = True
playtime = 30
```

### Other Files
- robloxrandomizer.json : Manages all the game data that the \__main__\.py script needs to get the current game's title, thumbnail and info. Also manages the "already played games" list.
- robloxrandomizerimgs : Images for the \__main__\.py's GUI. This script uses relative paths to get the image and other important files (like robloxrandomizerplus.py and robloxrandomizer.json), so please keep the repo or least these three items next to eachother all in the same directory/folder.
- icon.png : Logo for robloxrandomizer. It actually isn't used anywhere in the application, but it can be used for representing it in other sources (like this one!).

### robloxrandomizer
### by noob_97
![icon](https://github.com/user-attachments/assets/b4c0fdce-f31b-446d-a3d9-b4a81f135b80)

