

from firebase import firebase
#fire = firebase.FirebaseApplication('https://skrevamp.firebaseio.com/', 0)
import TimeChecker as tc
import SmartKnight as sk


schlist = dict()
schcount = 0
sniper = None
sniping = ["NullSnipingString"]
autoRes   = None
autoQuest = None
currentQuest = None
chainQuest = None
master      = None
trueOrder   = None
need_tch = None
usr = "184075777"

def UpDate(keyword = "Online",value = True):
    dir = ""
    if("sch" in keyword.lower()):
        dir = "/tasks/"
    else:
        dir = "/users/"
    fire.put(dir+usr,keyword,value)
    stats = fire.get("/users",None)

    sniper = stats[usr]["sniper"]
    sniping = stats[usr]["sniping"]
    autoRes   = stats[usr]["autoRes"]
    autoQuest = stats[usr]["autoQuest"]
    currentQuest = stats[usr]["currentQuest"]
    chainQuest = stats[usr]["chainQuest"]
    master      = stats[usr]["master"]
    trueOrder   = stats[usr]["trueOrder"]
    schcount = stats[usr]["schcount"]
    schlist = stats[usr]["schlist"]

    return

def init():
    UpDate()
    dispatcher = {
                    "schComm":sk.schComm,
                    "autoQuesting":sk.autoQuesting
                }
    tasks = fire.get("/tasks",None)
    #print(str(tasks))
    auxnum = 0
    for supkey,supval in tasks.items():
        schlist[supkey] = supval
        print("{}:".format(supkey))
        for infkey,infval in supval.items():
            print("\t{} -> {}".format(infkey,str(infval)))
            schcount = int(infkey)
            tc.ThreadSch(supkey,dispatcher[supkey],infval)
            if(schcount > auxnum):
                auxnum = schcount
        #auxnum = int(list(schlist[supkey].keys())[len(schlist[supkey])-1])
    schcount = auxnum
    schcount+=1

    return
