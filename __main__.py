import subprocess
import tkinter as tk
import json
import math
from ctypes import windll
from textwrap import TextWrapper
from PIL import ImageTk, Image
import requests
import io
import sys
import os
import atexit

window = tk.Tk()
window.title("robloxrandomizer")
window.attributes('-transparentcolor', "#010101")
window.configure(background="#010101")
window.overrideredirect(True)
window.attributes("-topmost", 1)
window.attributes("-alpha", 0.75)
windll.shcore.SetProcessDpiAwareness(1)
window.tk.call('tk', 'scaling', 3.0)

completedIMG = tk.PhotoImage(file = "robloxrandomizerimgs/completed.png")
gameinfoIMG = tk.PhotoImage(file = "robloxrandomizerimgs/gameinfo.png")
gamenumberIMG = tk.PhotoImage(file = "robloxrandomizerimgs/gamenumber.png")
nextgameIMG = tk.PhotoImage(file = "robloxrandomizerimgs/nextgame.png")
separatorIMG = tk.PhotoImage(file = "robloxrandomizerimgs/separator.png")
skipIMG = tk.PhotoImage(file = "robloxrandomizerimgs/skip.png")
startIMG = tk.PhotoImage(file = "robloxrandomizerimgs/start.png")
timerIMG = tk.PhotoImage(file = "robloxrandomizerimgs/timer.png")
welcomeIMG = tk.PhotoImage(file = "robloxrandomizerimgs/welcome.png")
winlosecountIMG = tk.PhotoImage(file = "robloxrandomizerimgs/winlosecount.png")
goalreachedIMG = tk.PhotoImage(file = "robloxrandomizerimgs/goalreached.png")
startnewIMG = tk.PhotoImage(file = "robloxrandomizerimgs/startnew.png")
continueIMG = tk.PhotoImage(file = "robloxrandomizerimgs/continue.png")


global timerredirect, timeflag, wins, finishedtime, loses, gamecount
timeflag = False
timerredirect = 0
currenttime = 0
timestr = "00:00"
finishedtime = "00:00"
timetaken = "00:00"
resultstatus = "N/A"
gamecount = 0
wins = 0
loses = 0

# CHALLENGE-MODE OPTIONS
goal = 1
saveSession = False

def update_json():
    global playtime, currentgame, favs, playing, gameimgurl
    playtime = json.load(open("robloxrandomizer.json", "r"))["playtime"]
    currentgame = json.load(open("robloxrandomizer.json", "r"))["currentGame"]
    favs = json.load(open("robloxrandomizer.json", "r"))["favs"]
    playing = json.load(open("robloxrandomizer.json", "r"))["playing"]
    gameimgurl = json.load(open("robloxrandomizer.json", "r"))["thumbnailURL"]

def reset_games():
    ogjson = json.load(open("robloxrandomizer.json", "r"))
    ogjson["PreviousGames"] = []
    json.dump(ogjson, open("robloxrandomizer.json", "w"))

def playtime_to_hour(custom_playtime = -1):
    if (custom_playtime == -1):
        text = f"{math.floor(playtime)}:{math.floor((playtime - math.floor(playtime)) * 60):02d}"
        return text
    else:
        text = f"{math.floor(custom_playtime)}:{math.floor((custom_playtime - math.floor(custom_playtime)) * 60):02d}"
        return text

def time_taken():
    p = str.split(playtime_to_hour(), ":")
    f = str.split(finishedtime, ":")
    p[0] = int(p[0]) ; p[1] = int(p[1]) ; f[0] = int(f[0]) ; f[1] = int(f[1])
    seconds = p[1] + f[1]
    minutestosec = (p[0] + f[0]) * 60
    totalsec = minutestosec + seconds
    timetakenplaytime = totalsec / 60
    return playtime_to_hour(timetakenplaytime)


def adjust_screen():
    screen_width = windll.user32.GetSystemMetrics(0)
    width = window.winfo_width()
    finalx = screen_width - width
    screenConstant = screen_width / 2560
    geometryAdd = int(150 * screenConstant * 3)
    window.geometry(f"+{finalx - geometryAdd}+50")

def get_game():
    try:
        subprocess.check_output([sys.executable, "robloxrandomizerplus.py"])
    except subprocess.CalledProcessError as e:
        print("An unknown error occurred. Trying again... Exception: " + str(e))
        get_game()

adjust_screen()
update_json()

def init():
    global startbutton, separator, welcome
    startbutton = tk.Button(master=window, image=startIMG, borderwidth=0, bg="#010101", activebackground="#010101", command=start)
    separator = tk.Label(master=window, image=separatorIMG, background="#010101", width=364)
    welcome = tk.Label(master=window, image=welcomeIMG, background="#010101")
    startbutton.pack(anchor="ne")
    separator.pack(pady=10)
    welcome.pack(anchor="ne")

def init_alt():
    global startbutton, separator, welcome
    startbutton = tk.Button(master=window, image=startnewIMG, borderwidth=0, bg="#010101", activebackground="#010101", command=search)
    continuebutton = tk.Button(master=window, image=continueIMG, borderwidth=0, bg="#010101", activebackground="#010101", command=continue_)
    separator = tk.Label(master=window, image=separatorIMG, background="#010101", width=364)
    welcome = tk.Label(master=window, image=welcomeIMG, background="#010101")
    startbutton.pack(anchor="ne")
    continuebutton.pack(anchor="ne")
    separator.pack(pady=10)
    welcome.pack(anchor="ne")

def search(completed = None):
    startbutton.pack_forget()
    separator.pack_forget()
    welcome.pack_forget()

    global timet, searchgame, winlose, gamenumber, wincount, losecount
    global wins, loses, resultstatus, finishedtime, gamecount

    if timerredirect == 2 or timerredirect == 3 or timerredirect == 4:
        completedbutton.pack_forget()
        skipbutton.pack_forget()
        filler.pack_forget()
        timet.pack_forget()
        winlose.place_forget()

    match completed:
        case None:
            resultstatus = "N/A"
        case False:
            resultstatus = "failed"
            loses = loses + 1
        case True:
            resultstatus = "completed"
            wins = wins + 1
        case -1:
            resultstatus = "skipped"
            loses = loses + 1

    timetext = f"    {finishedtime}"
    timet = tk.Label(master=window, text=timetext, image=timerIMG, compound="center", bg="#010101", activebackground="#010101", font="Outfit 25 bold", fg="#808080")
    resultstext = f"\ntime taken: {time_taken()} / {playtime_to_hour()}\nresult: {resultstatus}                                 "
    searchgame = tk.Label(master=window, image=nextgameIMG, bg="#010101", compound="center", text=resultstext, font="Outfit 7", fg="#616161")
    winlose = tk.Label(master=window, image=winlosecountIMG, bg="#010101")
    gametext = f"#{gamecount}"
    gamenumber = tk.Label(master=window, image=gamenumberIMG, bg="#010101", compound="center", text=gametext, font="Outfit 12 underline", fg="#7D7D7D")
    wincount = tk.Label(master=window, bg="#00F875", text=wins, fg="#009D4A", font="Outfit 12", borderwidth=0)
    losecount = tk.Label(master=window, bg="#FF0057", text=loses, fg="#A10037", font="Outfit 12", borderwidth=0)
    timet.pack(anchor="ne")
    separator.pack(pady=10)
    searchgame.place(x=118, y=178)
    gamenumber.pack(anchor="nw")
    winlose.pack(anchor="nw")
    wincount.place(x=92, y=302, anchor="e")
    losecount.place(x=10, y=326)

    window.update()
    get_game()
    gameinfo()

def gameinfo():
    searchgame.place_forget()
    update_json()

    textlist = TextWrapper(25, break_long_words=False).wrap(currentgame)
    global gtext, img, gameinf, timetext, favstext, playingtext, panel, gamecount
    gtext = "NULL"
    if len(textlist) == 1:
        gtext = f"{textlist[0]}"
    if len(textlist) == 2:
        gtext = f"{textlist[0]}\n{textlist[1]}"
    if len(textlist) > 2:
        gtext = f"{textlist[0]}\n{TextWrapper(20, break_long_words=True).wrap(textlist[1])[0]}..."
    gtext = f"\n\n\n\n{gtext}"
    gamecount = gamecount + 1


    gameinf = tk.Label(master=window, image=gameinfoIMG, bg="#010101", compound="center", text=gtext, font="Outfit 7")
    ttext = playtime_to_hour()
    timetext = tk.Label(master=window, font="Outfit 7", bg="#F0F0F0", text=ttext, fg="#808080")
    favstext = tk.Label(master=window, font="Outfit 7", bg="#F0F0F0", text=favs, fg="#808080")
    playingtext = tk.Label(master=window, font="Outfit 7", bg="#F0F0F0", text=playing, fg="#808080")

    response = requests.get(gameimgurl)
    img_data = response.content
    img = ImageTk.PhotoImage(Image.open(io.BytesIO(img_data)).resize((128, 72)))
    panel = tk.Label(window, image=img, width=128, height=72, borderwidth=0)
    panel.place(x=130, y=230)

    gameinf.place(x=118, y=178)
    timetext.place(x=370, y=290, anchor="e")
    favstext.place(x=370, y=263, anchor="e")
    playingtext.place(x=370, y=237, anchor="e")

    global timerredirect, timeflag
    timerredirect = 1
    timeflag = False
    timer_loop(5)

def gamedisplay():
    gamenumber.pack_forget()
    gameinf.place_forget()
    panel.place_forget()
    favstext.place_forget()
    playingtext.place_forget()
    timetext.place_forget()
    winlose.pack_forget()

    global completedbutton, skipbutton, filler
    completedbutton = tk.Button(master=window, image=completedIMG, borderwidth=0, bg="#010101", activebackground="#010101", command=complete)
    skipbutton = tk.Button(master=window, image=skipIMG, borderwidth=0, bg="#010101", activebackground="#010101", command=skip)
    filler = tk.Label(master=window, text="\n", bg="#010101")

    completedbutton.pack(anchor="e")
    skipbutton.pack(anchor="e", pady=10)
    winlose.place(x=0, y=275)
    filler.pack()

    global timerredirect, timeflag
    timerredirect = 2
    timeflag = False
    timer_loop(int(playtime * 60))
    
def goalcomplete():
    startbutton.pack_forget()
    separator.pack_forget()
    welcome.pack_forget()

    global timet, searchgame, winlose, gamenumber, wincount, losecount
    global wins, loses, resultstatus, finishedtime, gamecount


    completedbutton.pack_forget()
    skipbutton.pack_forget()
    filler.pack_forget()
    timet.pack_forget()
    winlose.place_forget()


    timetext = f"    {finishedtime}"
    timet = tk.Label(master=window, text=timetext, image=timerIMG, compound="center", bg="#010101", activebackground="#010101", font="Outfit 25 bold", fg="#808080")                             
    searchgame = tk.Label(master=window, image=goalreachedIMG, bg="#010101")
    winlose = tk.Label(master=window, image=winlosecountIMG, bg="#010101")
    gametext = f"#{gamecount}"
    gamenumber = tk.Label(master=window, image=gamenumberIMG, bg="#010101", compound="center", text=gametext, font="Outfit 12 underline", fg="#7D7D7D")
    wins = wins + 1
    wincount = tk.Label(master=window, bg="#00F875", text=wins, fg="#009D4A", font="Outfit 12", borderwidth=0)
    losecount = tk.Label(master=window, bg="#FF0057", text=loses, fg="#A10037", font="Outfit 12", borderwidth=0)
    timet.pack(anchor="ne")
    separator.pack(pady=10)
    searchgame.place(x=118, y=178)
    gamenumber.pack(anchor="nw")
    winlose.pack(anchor="nw")
    wincount.place(x=92, y=302, anchor="e")
    losecount.place(x=10, y=326)

    window.update()

    if os.path.exists("robloxrandomizerSession.json"):
        os.remove("robloxrandomizerSession.json")
    atexit.unregister(logSession)

def timer_loop(sec):
    currenttime = sec

    global finishedtime, gamecount, timestr, timerredirect, timeflag

    if currenttime == -1:
        timeflag = True

    if timeflag == False:
        timestr = playtime_to_hour(currenttime / 60)
        timetext = f"    {timestr}"
        timet.config(text=timetext)
        window.update()
    else:
        finishedtime = timestr
        match timerredirect:
            case 1:
                gamedisplay()
            case 2:
                search(False)
            case 3:
                search(True)
            case 4:
                search(-1)
            case 5:
                goalcomplete()
        return
        
    window.after(1000, timer_loop, sec - 1)

def complete():
    global timerredirect, timeflag
 
    if wins == goal - 1:
        timerredirect = 5
    else:
        timerredirect = 3
    timeflag = True

def skip():
    global timerredirect, timeflag

    timerredirect = 4
    timeflag = True

def start():
    if os.path.exists("robloxrandomizerSession.json"):
        os.remove("robloxrandomizerSession.json")

    reset_games()
    atexit.register(logSession)
    search()

def continue_():
    setSession()
    atexit.register(logSession)
    search()

def logSession():
    info = {"wins" : wins, "loses" : loses, "games" : gamecount}
    json.dump(info, open("robloxrandomizer.json", "w"))

def setSession():
    log = json.load(open("robloxrandomizer.json", "r"))
    log["wins"] = wins
    log["loses"] = loses
    log["games"] = gamecount

if os.path.exists("robloxrandomizerSession.json"):
    init_alt()
else:
    init()

window.mainloop()
