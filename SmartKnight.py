
import threading
import pyrogram as pyro
from time import sleep
#from TimeChecker import tc.cTime,tc.trueTime,tc.t2s,tc.s2t
import settings
import TimeChecker as tc
from firebase import firebase
from random import randint as rand
##################################################################### Pyrogram stuff
app1    = pyro.Client("Marie")
app2    = pyro.Client("Mickey")
Filters = pyro.Filters
##################################################################### Firebase stuff
fire = firebase.FirebaseApplication('https://skrevamp.firebaseio.com/', 0)
stats = fire.get("/users",None)
##################################################################### Important stuff: Marie
Mickey          = 184075777
Auction         = -1001209424945
CW              = 408101137
DHBot           = 548535953
Muskedeers      = -1001264392087
MarieUsers      = [Mickey,CW,DHBot]
MarieChats      = [Mickey,CW,DHBot,Auction,Muskedeers]
##################################################################### Important stuff: Mickey
Marie           = 598501240
PotBot          = 356088549
Jules           = 199950664
MadPlantsGroup  = -1001306916427
MickeyChats     = [Marie,PotBot,MadPlantsGroup,CW]
MickeyUsers     = [Marie,PotBot,Jules,CW]
##################################################################### Other Imported Functions
##################################################################### Locks
cond = threading.Condition()
##################################################################### Misc Global Variables
usr = str(Mickey)
try:
    settings.sniper = stats[usr]["sniper"]
    settings.sniping = stats[usr]["sniping"]
    settings.autoRes   = stats[usr]["autoRes"]
    settings.autoQuest = stats[usr]["autoQuest"]
    settings.currentQuest = stats[usr]["currentQuest"]
    settings.chainQuest = stats[usr]["chainQuest"]
    settings.master      = stats[usr]["master"]
    settings.trueOrder   = stats[usr]["trueOrder"]
except KeyError:
    settings.sniper = "None"
    settings.sniping = ["NullSnipingString"]
    settings.autoRes   = "None"
    settings.autoQuest = "None"
    settings.currentQuest = "None"
    settings.chainQuest = "None"
    settings.master      = "None"
    settings.trueOrder   = "None"

tmpMess     = None
orders      = ["🥔","🐺","🌑","🐉","🦌","🦈","🦅"]
banwords    = [
                "[",
                "squad",
                "result",
                "results"
                "]",
                "willing",
                "lot",
                "stock",
                "gold",
                "attack",
                "defend",
                "attackers",
                "defenders",
                "leaders",
                "village",
              ]
craftwords  = [
                "part",
                "blade",
                "head",
                "recipe",
                "piece",
                "fragment",
                "shaft"
              ]
##################################################################### TODO
def CurrentTime():
    while(True):
        global Marie
        this_moment = tc.cTime()
        #testSch = (((this_moment["h"] == "03") or (this_moment["h"] == "15") or (this_moment["h"] == "23")) and (this_moment["m"] == "57") and (this_moment["s"] == "15"))
        repSch  = (((this_moment["h"] == "02") or (this_moment["h"] == "10") or (this_moment["h"] == "18")) and (this_moment["m"] == "04") and (this_moment["s"] == "04"))
        warSch  = (((this_moment["h"] == "01") or (this_moment["h"] == "09") or (this_moment["h"] == "17")) and (this_moment["m"] == "38") and (this_moment["s"] == "47"))
        #print((this_moment["h"]+":"+this_moment["m"]+":"+this_moment["s"]+" UTC-5; repSch = {}; warSch = {}; testSch = {}".format(str(repSch),str(warSch),str(testSch))),end='\r')
        #print((this_moment["h"]+":"+this_moment["m"]+":"+this_moment["s"]+" UTC-5; repSch = {}; warSch = {}".format(str(repSch),str(warSch))),end='\r')
        sleep(.99)
        if(warSch):
            sO = threading.Thread(target = sendOrder)
            sO.start()
        if(repSch):
            #settings.trueOrder = None
            settings.UpDate("trueOrder","None")
            rprt = threading.Thread(target = report)
            rprt.start()
        #if(testSch):
        #    app2.send_message(Marie,"/time")
        #    app2.send_message(Marie,"Test Schedule was activated!")
    return

def schComm(name,t,comm,feedback = False):
    global CW
    if(settings.chainQuest != False):
        sleep(t)
        if(settings.need_tch != False):
            app2.send_message(CW,"/craft_tch")
            sleep(4)
            app2.send_message(CW,"/bind_tch")
            sleep(4)
            app2.send_message(CW,"/on_tch")
            settings.need_tch = False
        if(settings.master != False and settings.chainQuest != False):
            print("{} -> {}".format(CW,comm))
            app2.send_message(Marie,str(comm))
            if(feedback != False):
                app1.send_message(Mickey,"hest \"{}\" hast been hath sent!".format(str(comm)))
        del(settings.schlist[name][threading.currentThread().getName()])
        #fire.put("/tasks/"+name,threading.currentThread().getName(),None)
        settings.UpDate("schlist",settings.schlist)
        return
    else:
        sleep(t)
        if(settings.master != False):
            app2.send_message(Marie,str(comm))
            if(feedback != False):
                app1.send_message(Mickey,"hest \"{}\" hast been hath sent!".format(str(comm)))
        del(settings.schlist[name][threading.currentThread().getName()])
        #fire.put("/tasks/"+name,threading.currentThread().getName(),None)
        settings.UpDate("schlist",settings.schlist)

        return

def autoQuesting(t = 0,comm = ""):
    sleep(t)
    if((int(tc.cTime()["h"])%8 == 1) and int(tc.cTime()["m"]) > 45):
        app1.send_message(Mickey,"Battle of the seven castles is near.  I shall suspend __automatic questing__ until 15 minutes aproximately after battle.")
        sleep(1800)
    if(settings.master != False and settings.autoQuest != False):
        app2.send_message(CW,settings.currentQuest)
        if((settings.autoQuest != False)):
            """try:
                t = s2t(3600 + rand(0,600))
                T = "{}:{}:{}".format(t["h"],t["m"],t["s"])

                tc.ThreadSch("Auto Questing: {}".format(ssettings.currentQuest),autoQuesting,[T,settings.currentQuest])
            except ValueError:"""
            aq = threading.Thread(name = "autoQuesting".format(settings.currentQuest),target = autoQuesting, args = ((3600 + rand(0,600)),))
            aq.start()
    return

def reqOrder():
    ans = None
    if(settings.master != False):
        if(settings.trueOrder != "None"):
            ans = str(settings.trueOrder)
        else:
            ans = "None"
        app1.send_message(Mickey,ans)
    return

def reqTime():
    now = tc.cTime()
    Timestring = str("The current time is: "+now["h"]+":"+now["m"]+":"+now["s"]+" UTC-5")
    app1.send_message(Mickey,Timestring)
    return

def sendOrder(t = rand(10,513)):
    sleep(t)
    if(settings.master != False):
        if((settings.trueOrder != "None") and (settings.trueOrder != "🦌")):
            app1.send_message(CW,"⚔Attack")
            sleep(10)
            if(settings.master != False):
                app1.send_message(CW,settings.trueOrder)
        else:
            app1.send_message(CW,"🛡Defend")
    return

def messPrint(message):
    title = ""
    username = ""
    usernum = ""
    chatnum = ""

    try:
        username = str(message["from_user"]["username"])
        if(username == "None"):
            username = ""
    except TypeError or IndexError:
        username = ""

    try:
        title = str(message["chat"]["title"])
        if(title == "None"):
            title = ""
        if((len(title) > 0) and (len(username) > 0)):
            title = title+"@"
    except TypeError or IndexError:
        None

    try:
        usernum = str(message["from_user"]["id"])
        if(usernum == None):
            usernum = "N/A"
    except TypeError or IndexError:
        None

    chatnum = str(message["chat"]["id"])

    try:
        fullmess = "\n> "+str(title)+str(username)+" (User:"+str(usernum)+" chat:"+str(chatnum)+"): \n"+message["text"]+"\n at "+str(tc.cTime()["h"])+":"+str(tc.cTime()["m"])+":"+str(tc.cTime()["s"])+"\n"
        print("\n\n\n~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~")##~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~
        print(fullmess)
    except KeyboardInterrupt:
        return

def resume():
    t = rand(10,135)
    ans = "Mickey, __automat'd buying__ hast been suspended, I am gonna resume t in {} seconds.".format(t)
    app1.send_message(Mickey,ans)
    sleep(t)
    if(settings.master != False and settings.autoRes != False):
        ans = "/resume"
        app2.send_message(PotBot,ans)
        ans = "Lief mickey, I've just resum'd __automat'd buying__ on botato f'r thee"
        app1.send_message(Mickey,ans)
    return

def go():
    t = rand(9,157)
    ans = "Invader did detect... \nwaiting {} seconds to attack.".format(t)
    app1.send_message(Mickey,ans)
    sleep(t)
    if(settings.master != False):
        ans = "/go"
        app1.send_message(CW,ans)
        ans = "...Fighting engag'd!"
        app1.send_message(Mickey,ans)
    return

def go2():
    t = rand(9,157)
    ans = "Invader did detect... \nwaiting {} seconds to attack.".format(t)
    if(settings.master != False):
        app1.send_message(Mickey,ans)
    sleep(t)
    ans = "/go"
    if(settings.master != False):
        app2.send_message(CW,ans)
        ans = "...Fighting engag'd!"
        app1.send_message(Mickey,ans)
    return

def sendPledge():
    t = rand(5,155)
    ans = "/pledge"
    sleep(t)
    if(settings.master != False):
        app1.send_message(CW,ans)
    return

def report():
    global tmpMess
    with cond:
        cond.acquire()
        t = rand(120,600)
        ans = "Trying to sendeth report to Deerbot in {} seconds...".format(t)
        app1.send_message(Mickey,ans)
        sleep(t)
        if(settings.master != False):
            ans = "/report"
            app1.send_message(CW,ans)
            sleep(3)
            cond.wait()
            tmpMess.forward(DHBot)
            cond.release()
            ans = "Report hath sent successfully!"
        app1.send_message(Mickey,ans)



#########################################################################################################################################################################################################################################################################################################
#########################################################################################################################################################################################################################################################################################################
#########################################################################################################################################################################################################################################################################################################

@app1.on_message(Filters.user(MarieUsers) | Filters.chat(MarieChats))############################################################################ Marie
def mess_handler1(client,message):
    global tmpMess
    global orders
    global Mickey
    global CW

    if(message):

        ################################################################################################################################################################################################################################################################################################################################

        #app1.send_message(Mickey,"Auction and message id are {}".format(str(message["chat"]["id"] == Auction)))
        #print("Auction and message id are {}".format(str(message["chat"]["id"] == Auction)))
        if((message["chat"]["id"] == Auction)and (settings.master != False)):
            #app1.send_message(Mickey,"This auction is {}".format((settings.sniping.lower() in message["text"].lower())))
            try:
                if(settings.sniper != False and message["edit_date"] == None):
                    dobdot = message["text"].find(":")+2
                    ljump = message["text"].find("\n")
                    truitem = message["text"][dobdot:ljump].lower()
                    trulist = [si.lower() in truitem for si in settings.sniping]
                    if(True in trulist):
                        app1.send_message(Mickey,"Lief Mickey, I hath found the item thee wast looking f'r.")
                        message.forward(Mickey)
            except(Exception) as e:
                app1.send_message(Mickey,"aww, Snap! Something failed during searching in auction: \n`{}`".format(str(e)))

        try:
################################################################################################################################################################################################################################################################################################################################

            if((message["from_user"]["id"] == Mickey) and (settings.master != False)):
                if(message["text"] == "/help"):
                    ans ="""Alloweth me bid thee, what mine own arts can giveth thee, master:

> **/help** - I shall fain share all mine own knowledge and mine own arts with thee.

> **/ping** - doth thee wanteth to playeth some table tennis?

> **/aq** - Oft thee may feeleth not restful. Worry not, I can wend questing f'r thee. I gage to gather so many resources out thither! (Usage:\n __/aq [quest/off]__)

> **/chain** - Long journeys art exciting every time! If 't be true thee wanteth to wend out f'r a long while, I shall supply thee enow to last longer out in the wild. (Usage:\n __/chain [enable/disable]__)

> **/sl** - I shall bid thee the current stuff I am looking for, so thee can did bid f'r those folk.

> **/snipe** - oft thee may wanteth some item so much, but thee has't nay time to behold f'r t.  I can search f'r t if 't be true thee wanteth me to. (Usage:\n __/snipe [item-name/off]__)

> **/sch** - I knoweth thee shall not beest hither all the time, oft master hast much other stuff to doth.  And yond is wherefore I am hither, to help thee doing organizing stuff while thou art hence. (Usage:\n __/sch [time][command]__) (also: __/sch__ just to showeth what I am doing at this very moment. )

> **/order** - not sure which charge I am following? I shall beest fain to remind thee which one wast t. I followeth thy squad orders to eke help those folk during hurlyburly.  But if 't be true thee wanteth me to followeth any other charge, yours art mine own first priority! (Usage:\n __/so [order]__)

> **/so** - I can manually followeth orders instead.  But I doth not knoweth wherefore would thee wanteth to doth yond.

> **/ar** - I cannot buyeth all stuff, but botato snipes some resources f'r thee.  I shall just bid him at which hour not to stand ho, yond distemperate rampallian shouldst not stand ho buying just because thou art out of wage! (Usage:\n /ar [enable/disable])

> **/time** - I knoweth the exact UTC-5, I can bid thee if 't be true thee wanteth t.

> **/Master** - If 't be true thee needeth time high-lone, just bid me, I shall hapily wait f'r at which hour thee needeth me.

> **/info** - I may eke giveth thee a short resume of everything I am and I am not doing at this very moment.


Thither art many other things I can doth f'r thee, but thee doth not has't to asketh me to doth 'em.  I just behold f'r thy most wondrous comfort, belov'd master.  Eke, I am constantly learning new arts to serveth to thee."""
                    app1.send_message(Mickey,ans)

                if(message["text"] == "/ping"):
                    app1.send_message(Mickey,"***Pong!***")

                if(message["text"] == "/info"):
                    swtchs = """These art the current switches, Master:

> **Master** → `{}`
> **Sniper** → `{}`
> **Auto Resume** → `{}`
> **Auto Quest** → `{}`
> **Chain Quest** → `{}`
> **Current Quest** → `{}`
> **Current Order** → `{}`
""".format(str(settings.master),str(settings.sniper),str(settings.autoRes),str(settings.autoQuest),str(settings.chainQuest),str(settings.currentQuest),str(settings.trueOrder))
                    app1.send_message(Mickey,swtchs)

                if("/aq" in message["text"]):
                    qcomm = message["text"].split(" ")
                    if(len(qcomm) == 2):
                        if(("off" in message["text"].lower()) and (settings.autoQuest != False)):
                            #settings.autoQuest = False
                            settings.UpDate("autoQuest",False)
                            app1.send_message(Mickey,"Welcome back, Mickey!  Art thee eft f'r moo adventures? \nAutomatic questing is now [DISABLED]!")
                        elif((qcomm[1].lower() == "🌲Forest".lower()) or (qcomm[1].lower() == "🍄Swamp".lower()) or (qcomm[1].lower() == "⛰️Valley".lower())):
                            #settings.currentQuest = qcomm[1]
                            settings.UpDate("currentQuest",qcomm[1])
                            ans = "Do not worry, dear master. I will gather some resources for you while you are away. Leave everything in my hands!"
                            if(settings.autoQuest != True):
                                aq = threading.Thread(name = "AutoQuesting: {}".format(settings.currentQuest),target = autoQuesting)
                                #settings.autoQuest = True
                                settings.UpDate("autoQuest",True)
                                aq.start()
                                ans = ans+" \nAutomatic questing is now [ENABLED]!"
                            app1.send_message(Mickey,ans)
                            #settings.autoQuest = True
                            settings.UpDate("autoQuest",True)

                        else:
                            app1.send_message(Mickey,"My most humble apology, but yond's not a valid hest.")
                    else:
                        if(settings.autoQuest != False):
                            app1.send_message(Mickey,"I am currently doing some {} f'r thee. Thee doth not has't to worry at all, master.".format(settings.currentQuest))
                        else:
                            app1.send_message(Mickey,"Mine own apologies, but thee has't not hath asked me to wend out on any quest yet.")

                if("/chain" in message["text"]):
                    if(("enable" in message["text"].lower()) and (settings.chainQuest != True)):
                        #settings.chainQuest = True
                        settings.UpDate("chainQuest",True)
                        app1.send_message(Mickey,"Anon thee shall keepeth questing one time after another.  What an adventurer spirit! \n__Chain questing__ is now [ENABLED]!")
                    elif(("disable" in message["text"].lower()) and (settings.chainQuest != False)):
                        #settings.chainQuest = False
                        settings.UpDate("chainQuest",False)
                        app1.send_message(Mickey,"It is safer to cameth back after each quest, to resupply and rest a dram while between quest and quest... \n__Chain questing__ is now [DISABLED]!")
                    else:
                        if(settings.chainQuest != False):
                            state = "[ENABLED]"
                        else:
                            state = "[DISABLED]"
                        app1.send_message(Mickey,"__Chain questing__ is currently {}!".format(state))

                try:
                    if(message["text"] == "/sl"):
                        app1.send_message(Mickey,"".join(str("\n> "+i) for i in settings.sniping[1:]))
                except pyro.api.errors.exceptions.bad_request_400.MessageEmpty:
                    app1.send_message(Mickey,"Mine own apologies, but thee has't not hath asked me to seek f'r any item.")

                if("/snipe" in message["text"]):
                    text = message["text"].split(" ")
                    text2 = list()
                    text2.append(text[0])
                    text2.append(" ".join(text[1,len(text)]))
                    if(len(text2) > 1):
                        if(text2[1].lower() == "off"):
                            #settings.sniper = False
                            settings.UpDate("sniper",False)
                            #settings.sniping = ["NullSnipingString"]
                            settings.UpDate("sniping",["NullSnipingString"])
                            app1.send_message(Mickey,"Forsooth, I'll stand ho looking by anon.  Bid me if 't be true thee needeth aught else, Mickey.")

                        else:
                            settings.sniping.append(str(text2[1]))
                            settings.UpDate("sniping",sniping)
                            #settings.sniper = True
                            settings.UpDate("sniper",True)
                            app1.send_message(Mickey,"Well enow, Mickey, I will bid thee if 't be true I findeth something...")
                    else:
                        app1.send_message(Mickey,"My most humble apology, but yond's not a valid hest.")


                if("/sch" in message["text"]):
                    #print("\n>flag-1")
                    comm = message["text"].split(" ")
                    #comm[0] = "/sch"
                    #comm[1] = time
                    #comm[2:] = command
                    #print("\n>flag0")
                    if(message["text"] == "/sch"):
                        try:
                            #enum = threading.enumerate()
                            #ans = "".join("\n> "+str(i).split(",")[0] for i in enum)
                            #ans = "".join("\n> "+str(i+" -> "+j) for i,j in settings.schlist[tName].values())
                            ans = ""
                            for k in settings.schlist.keys():
                                ans = ans + "".join("\n> {}".format(k))
                                for i,j in settings.schlist[k].values():
                                    ans = ans + "".join("\n\t\t> {} -> {}".format(i,j))
                            print(ans)
                            app1.send_message(Mickey,ans)
                        except pyro.api.errors.exceptions.bad_request_400.MessageEmpty:
                            ans = "Pardon me, but thither art nay running tasks :("
                            app1.send_message(Mickey,ans)
                    else:
                        #print("\n>flag1")
                        if((len(comm) >= 3)):
                            #print("\n>flag2")
                            try:
                                #comm[1] = int(comm[1])
                                #print("\n>flag3")
                                command = "".join(str(i+" ") for i in comm[2:])
                                #print("\n>flag4")
                                nombre = "schComm".format(command,comm[1])
                                #print("\n>flag5")
                                print(command)
                                #settings.schlist.append(threading.Thread(name = nombre, target = schComm, args = (comm[1],command,True,)))
                                #settings.schlist[len(settings.schlist)-1].start()
                                #print("\n>flag6")
                                tc.ThreadSch(nombre,schComm,comm[1:])
                                app1.send_message(Mickey,"Thy hest hast been scheduled, and shall beest hath sent in {} seconds".format(tc.t2s(comm[1])))

                            except ValueError:
                                #print("\n>flag7")
                                app1.send_message(Mickey,"Pardon me, but this is not a valid hest.")
                        else:
                            #print("\n>flag8")
                            app1.send_message(Mickey,"Pardon me, but this is not a valid hest.")
                        #print("\n>flag9")
                    #print("\n>flag10")

                if(message["text"] == "/so"):
                    so = threading.Thread(target = sendOrder, args = (0,))
                    so.start()
                    app1.send_message(Mickey,"Sending charge.  This shall taketh few moments, prithee beest patient.")

                if("/order" in message["text"]):
                    print(str(orders))
                    print(str(list(message["text"])))
                    print(set(orders).intersection(set(message["text"])))
                    print(settings.trueOrder)
                    previousDiff = (list(set(orders).intersection(set(message["text"])))[0] != settings.trueOrder)
                    print(previousDiff)
                    if(set(orders).intersection(set(message["text"])) and (previousDiff != False)):
                        if(set(orders).intersection(set(message["text"])) == {"🥔"}):
                            if(settings.trueOrder == "None"):
                                #settings.trueOrder = "🛡Defend"
                                settings.UpDate("trueOrder","🛡Defend")
                            else:
                                pass
                        else:
                            #settings.trueOrder  = set(orders).intersection(set(message["text"]))
                            tO = list(set(orders).intersection(set(message["text"])))[0]
                            settings.UpDate("trueOrder",tO)
                        app1.send_message(Mickey,settings.trueOrder)
                    else:
                        pass
                        O = threading.Thread(target = reqOrder)
                        O.start()

                if("/ar" in message["text"]):
                    if(("enable" in message["text"].lower()) and (settings.autoRes != True)):
                        #settings.autoRes = True
                        settings.UpDate("autoRes",True)
                        app1.send_message(Mickey,"Haply thee shouldst stand ho buying compulsively, Master. \nAutomatic __/resume__ is now [ENABLED]!")
                    elif(("disable" in message["text"].lower()) and (settings.autoRes != False)):
                        #settings.autoRes = False
                        settings.UpDate("autoRes",False)
                        app1.send_message(Mickey,"Do not let that lazy slobtato stop doing its work! \nAutomatic __/resume__ is now [DISABLED]!")
                    else:
                        if(settings.autoRes != False):
                            state = "[ENABLED]"
                        else:
                            state = "[DISABLED]"
                        app1.send_message(Mickey,"Automatic __/resume__ is currently {}!".format(state))

                if(message["text"] == "/time"):
                    rt = threading.Thread(target = reqTime)
                    rt.start()
                settings.UpDate()

    ################################################################################################################################################################

            if((((message["from_user"]["id"] == CW)) or (message["from_user"]["id"] == Mickey)) and (settings.master != False)):
                invader = None
                if(("/go" in message["text"]) and ("bind" not in message["text"].lower()) and (("russet" in message["text"].lower()) != True)):
                    CF = threading.Thread(target = go)
                    CF.start()
                if(("terrible" in message["text"]) and ("let" in message["text"])):
                    app1.send_message(Mickey,"My most humble apology, invader did miss...")
                if(("stopping" in message["text"]) and ("hurts" in message["text"].lower())):
                    invader = message["text"][19:message["text"].find(".")]
                    app1.send_message(Mickey,"Invader **{}** combated.  Alas, square wast hath lost.".format(invader))
                if(("successfully" in message["text"]) and ("defeated" in message["text"])):
                    invader = message["text"][26:message["text"].find(".")]
                    app1.send_message(Mickey,"`[DARK SPIRIT DESTROYED]`\nDark spirit **{}** has died!".format(invader))
                if("/pledge" in message["text"]):
                    pl = threading.Thread(target = sendPledge)
                    pl.start()
                try:
                    with cond:
                        if(("result" in message["text"]) and ("battlefield" in message["text"])):
                            tmpMess = message
                            cond.release()
                except RuntimeError:
                    app1.send_message(Mickey,"Pardon me, I couldn't sendeth the hurlyburly report.  I'll tryeth again manually, Mickey.")
                    tmpMess.forward(DHBot)
                    app1.send_message(Mickey,"Hurlyburly report hath sent!!!")
    ################################################################################################################################################################

            if(message["from_user"]["id"] == Mickey):
                if("/Master" in message["text"]):
                    if("on" in message["text"].lower() and settings.master != True):
                        #settings.master = True
                        settings.UpDate("master",True)
                        app1.send_message(Mickey,"I am hither to serveth thee, Mickey. 😊")
                    elif("off" in message["text"].lower() and settings.master != False):
                        #master = False
                        settings.UpDate("master",False)
                        app1.send_message(Mickey,"As thee wish, master...")
                    else:
                        if(settings.master != False):
                            state = "ON"
                        else:
                            state = "OFF"
                        app1.send_message(Mickey,"Master control is currently {}!".format(state))

    ################################################################################################################################################################


            #Checa si el mensaje es de Julia o Botato:
            if(((message["from_user"]["id"] == DHBot)  and (message["chat"]["id"] == Muskedeers) and (settings.master != False))):
                #Pasa el mensaje de Mickey a María
                #message.forward(Marie)
                #Dice, de María a Mickey, si existe alguna banword en el mensaje pasado
                #app1.send_message(Mickey,"banword = {}".format(any(n in message["text"].lower() for n in banwords)))
                #si es falso que exista alguna banword en el mensaje:
                if(any(n in str(message["text"]).lower() for n in banwords) != True):
                    #Checa si existe una posible orden que intersecte el mensaje
                    if((set(orders).intersection(set(message["text"])))):
                        #si la orden nueva es patata
                        if(set(orders).intersection(set(message["text"])) == {"🥔"}):
                            #si la orden actual es nula
                            if(settings.trueOrder  == None):
                                #Nueva orden es ciervo
                                #settings.trueOrder  = {"🛡Defend"}
                                settings.UpDate("trueOrder","🛡Defend")
                            #sino
                            else:
                                #Deja la orden actual
                                pass
                        #sino
                        else:
                            #Checa entonces si la orden intersectada es distinta a la actual
                            if(list(set(orders).intersection(set(message["text"])))[0] != settings.trueOrder ):
                                #nueva orden es la interseccion de mensaje y ordenes posibles
                                tO = list(set(orders).intersection(set(message["text"])))[0]
                                settings.UpDate("trueOrder",tO)
                                #Envia la nueva orden
                                app1.send_message(Mickey,("New charge -> "+settings.trueOrder ))
                                #Si falta 10min o menos para la guerra
                                if((int(tc.cTime()["h"])%8 == 1) and int(tc.cTime()["m"]) > 49):
                                    #envía la orden actual inmediatamente
                                    app1.send_message(CW,settings.trueOrder )

        except Exception as e:
            print("aww, Snap!`{}`".format(str(e)))
            pass
        messPrint(message)
    return
#########################################################################################################################################################################################################################################################################################################
#########################################################################################################################################################################################################################################################################################################
#########################################################################################################################################################################################################################################################################################################

@app2.on_message(Filters.chat(MickeyChats) & Filters.user(MickeyUsers))################## Mickey
def mess_handler2(client,message):
    global orders
    awakeHours = (int(tc.cTime()["h"]) > 5)
    if(message):
        try:
    ################################################################################################################################################################
            if(((message["from_user"]["id"] == CW) or (message["from_user"]["id"] == Marie)) and (settings.master != False)):#Mickey for Testing Purposses
                #print(">>> Flag 1")
                if(awakeHours):
                    invader = None
                    if(("/go" in message["text"]) and ("bind" not in message["text"].lower())):
                        CF2 = threading.Thread(target = go2)
                        CF2.start()
                    if(("terrible" in message["text"]) and ("let" in message["text"])):
                        app1.send_message(Mickey,"My most humble apology, I could not hath caught the invader...")
                    if(("stopping" in message["text"]) and ("hurts" in message["text"].lower())):
                        invader = message["text"][19:message["text"].find(".")]
                        app1.send_message(Mickey,"I hath tried fighting **{}** f'r thee.  Alas, **{}** wast stronger.".format(invader,invader))
                    if(("successfully" in message["text"]) and ("defeated" in message["text"])):
                        invader = message["text"][26:message["text"].find(".")]
                        app1.send_message(Mickey,"`[DARK SPIRIT DESTROYED]`\n I've did banish dark spirit **{}** f'r thee!".format(invader))

                if(("earned" in message["text"].lower()) and ("received" in message["text"].lower())):
                    questr = message["text"].split("\n")
                    print("yep")
                    for q in questr:
                        print("Yep yep")
                        yep = (any(n in q.lower() for n in craftwords))
                        if(("earned" in q.lower()) and (yep != False)):
                            dobdot = q.find(":")+2
                            paren = q.find("(")-1
                            item = q[dobdot:paren]
                            app1.send_message(Mickey,"Yay! thee has't hath found a **{}** in thy last quest, at __{} UTC-5__ ".format(item,tc.trueTime()))
                            app2.send_message(CW,"/time")
                            print("Aham, aham, ahaaam")
                #else:
                    #print("resource {} earned :'v'".format((("earned" in message["text"].lower()) and ("recieved" in message["text"].lower()))))

                if(("flame" in message["text"]) and ("footing" in message["text"]) and (settings.chainQuest != False)):
                    settings.need_tch = True

                if(("adventure" in message["text"].lower()) and ("swamp" in message["text"].lower()) and (settings.chainQuest != False)):
                    #print(">>> Flag 2")
                    if(((int(tc.cTime()["h"])%8 == 1) and (int(tc.cTime()["m"]) > 45)) != True):
                        #print(">>> Flag 3")
                        aux = message["text"].find("minutes")
                        t = (int(message["text"][aux-2:aux-1])*60)+15
                        swamp = threading.Thread(name = "🍄Swamp", target = schComm, args = (t,"🍄Swamp",))
                        swamp.start()
                        #app1.send_message(Mickey,"Embrace yourself f'r next adventure in {} seconds...".format(t))
                    else:
                        app1.send_message(Mickey,"Thee has't nay time f'r games, hurlyburly is coming.")
                        #print(">>> Flag 4")

                if(("mountains" in message["text"].lower()) and ("decided" in message["text"].lower()) and (settings.chainQuest != False)):
                    #print(">>> Flag 2")
                    if(((int(tc.cTime()["h"])%8 == 1) and (int(tc.cTime()["m"]) > 45)) != True):
                        #print(">>> Flag 3")
                        aux = message["text"].find("minutes")
                        t = (int(message["text"][aux-2:aux-1])*60)+15
                        swamp = threading.Thread(name = "⛰️Valley", target = schComm, args = (t,"⛰️Valley",))
                        swamp.start()
                        #app1.send_message(Mickey,"Embrace yourself f'r next adventure in {} seconds...".format(t))
                    else:
                        app1.send_message(Mickey,"Thee has't nay time f'r games, hurlyburly is coming.")
                        #print(">>> Flag 4")

                if(("forest" in message["text"].lower()) and ("dire" in message["text"].lower()) and (settings.chainQuest != False)):
                    #print(">>> Flag 2")
                    if(((int(tc.cTime()["h"])%8 == 1) and (int(tc.cTime()["m"]) > 45)) != True):
                        #print(">>> Flag 3")
                        aux = message["text"].find("minutes")
                        t = (int(message["text"][aux-2:aux-1])*60)+15
                        swamp = threading.Thread(name = "🌲Forest", target = schComm, args = (t,"🌲Forest",))
                        swamp.start()
                        #app1.send_message(Mickey,"Embrace yourself f'r next adventure in {} seconds...".format(t))
                    else:
                        app1.send_message(Mickey,"Thee has't nay time f'r games, hurlyburly is coming.")
                        #print(">>> Flag 4")

                if("/promo" in message["text"].lower()):
                    app1.send_message(Mickey,"Colours me, thee has't ranneth out of stamina.")
                    #settings.autoQuest = False
                    settings.UpDate("autoQuest",False)
                    #settings.currentQuest = None
                    settings.UpDate("currentQuest","None")
                    #settings.chainQuest = False
                    settings.UpDate("chainQuest",False)


    ################################################################################################################################################################

            if(message["from_user"]["id"] == (PotBot) and settings.master != False):
                if("/resume" in message["text"] and settings.autoRes != False):
                    res = threading.Thread(target = resume)
                    res.start()
    ################################################################################################################################################################

            """#Checa si el mensaje es de Julia o Botato:
            if(((message["from_user"]["id"] == PotBot) or (message["from_user"]["id"] == Jules)) and (message["chat"]["id"] == MadPlantsGroup) and (settings.master != False)):
                #Pasa el mensaje de Mickey a María
                #message.forward(Marie)
                #Dice, de María a Mickey, si existe alguna banword en el mensaje pasado
                #app1.send_message(Mickey,"banword = {}".format(any(n in message["text"].lower() for n in banwords)))
                #si es falso que exista alguna banword en el mensaje:
                if(any(n in str(message["text"]).lower() for n in banwords) != True):
                    #Checa si existe una posible orden que intersecte el mensaje
                    if((set(orders).intersection(set(message["text"])))):
                        #si la orden nueva es patata
                        if(set(orders).intersection(set(message["text"])) == {"🥔"}):
                            #si la orden actual es nula
                            if(trueOrder == None):
                                #Nueva orden es ciervo
                                trueOrder = {"🦌"}
                            #sino
                            else:
                                #Deja la orden actual
                                pass
                        #sino
                        else:
                            #Checa entonces si la orden intersectada es distinta a la actual
                            if((set(orders).intersection(set(message["text"]))) != trueOrder):
                                #nueva orden es la interseccion de mensaje y ordenes posibles
                                trueOrder = set(orders).intersection(set(message["text"]))
                                #Envia la nueva orden
                                app1.send_message(Mickey,("New charge -> "+list(trueOrder)[0]))
                                #Si falta 1h10min o menos para la guerra
                                if((int(tc.cTime()["h"])%8 == 6) and int(tc.cTime()["m"]) > 49):
                                    #envía la orden actual inmediatamente
                                    app1.send_message(CW,list(trueOrder)[0])"""

        except (Exception) as e:
            print("aww, Snap!`{}`".format(str(e)))
            pass
        messPrint(message)
    return
#########################################################################################################################################################################################################################################################################################################
#########################################################################################################################################################################################################################################################################################################
#########################################################################################################################################################################################################################################################################################################


if __name__ == '__main__':
    threading.currentThread().setName(" Service")
    Now = threading.Thread(target = CurrentTime, name = "Time")
    try:
        settings.init()
    except AttributeError:
        print("\n\n\nAttributeError!!!!!!!!!!!!!!!!!!\n\n\n")
    app1.start()
    app1.send_message(Mickey,"Good morrow, Mickey! I am anon online! 😋\nHow may I serveth thee?")
    settings.master = True
    app2.start()
    app2.send_message(Marie,"/sch")
    Now.start()
