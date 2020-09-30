
import time
import threading
from firebase import firebase
import settings

fire = firebase.FirebaseApplication('https://skrevamp.firebaseio.com/', 0)
tasks = fire.get("/tasks",None)

settings.schlist = dict()
settings.schcount = 0

def cTime():
    gmtime = time.gmtime
    strftime = time.strftime
    th = int(strftime("%H",gmtime())) - 5
    th = "{:02}".format(th)
    if(int(th) >= 24): th = "{:02}".format(int(th) - 24)
    if(int(th) < 0): th = "{:02}".format(int(th) + 24)
    tm = strftime("%M",gmtime())
    ts = strftime("%S",gmtime())
    t = {
        "h":th,
        "m":tm,
        "s":ts
        }
    return t

def trueTime(t = cTime()):
    st = "{}:{}:{}".format(str(t["h"]),str(t["m"]),str(t["s"]))
    return st

def t2s(ft,echo = False):
    now = cTime()
    if echo == True: print("La hora exacta es {} UTC".format(trueTime(now)))
    future = ft.split(":")

    if(len(future) == 3):
        if(int(now["h"]) >= int(future[0])):
            hours = 24 - int(now["h"])
            hours = hours + (int(future[0]))
            if((hours == 24) and (int(now["m"]) < int(future[1]))): hours = 0
        else:
            hours = int(future[0]) - int(now["h"])

        if(int(now["m"]) >= int(future[1])):
            minutes = 60 - int(now["m"])
            minutes = minutes + (int(future[1]))
            if((minutes == 60) and (int(now["s"]) < int(future[2]))): minutes = 0;hours +=1
            hours = hours - 1
        else:
            minutes = int(future[1]) - int(now["m"])

        if(int(now["s"]) >= int(future[2])):
            seconds = 60 - int(now["s"])
            seconds = seconds + (int(future[2]))
            if(seconds == 60): seconds = 0
            minutes = minutes - 1
        else:
            seconds = int(future[2]) - int(now["s"])

        if(seconds >= 60): seconds = seconds - 60; minutes+=1
        if(minutes >= 60): minutes = minutes - 60; hours+=1
        if(hours >= 24): hours = hours - 24

        hr_sec = hours*60*60
        min_sec = minutes*60
        total_sec = hr_sec+min_sec+seconds

        if echo == True: print("Faltan \n\t{} hrs, \n\t\t{} min \n\t\t\ty \n\t\t\t\t{} seg \n\t\t\t\t\tdesde las \n\t\t\t\t\t\t{} UTC \n\t\t\t\t\t\t\thasta las \n\t\t\t\t\t\t\t\t{} UTC".format(hours,minutes,seconds,trueTime(now),ft))
        if echo == True: print("Esto se puede traducir como un total de {} segundos hasta ese momento.\n\n\n".format(int(total_sec)))

        return total_sec
    else:
        print(future)
        raise ValueError

def s2t(seconds, echo = False):
    sec = seconds
    hr = (sec // 60) // 60
    sec = sec - (hr*60*60)
    min = sec // 60
    sec = sec - (min*60)
    seconds = "{:02}".format(seconds)
    hr = "{:02}".format(hr)
    min = "{:02}".format(min)
    sec = "{:02}".format(sec)

    if(echo == True):
        print("El total de {} segundos es igual a {} horas, {} minutos y {} segundos.".format(seconds,hr,min,sec))
    return { "h":hr, "m":min, "s":sec }

def testThread(tName,t,comm = ""):
    print("Enabled! waiting {} seconds".format(t))
    time.sleep(t)
    print("\n>>>>>>>>>>>>>>>>>>>>>>>>> "+str(comm))
    del(settings.schlist[tName][threading.currentThread().getName()])
    fire.put("/tasks/"+tName,threading.currentThread().getName(),None)

def ThreadSch(tName, Target, ft, echo= False):
    try:
        settings.schlist[tName]["{:02}".format(settings.schcount)] = ft
        fire.put("/tasks/"+tName,"{:02}".format(settings.schcount),ft)
    except KeyError:
        settings.schlist[tName] = dict()
        settings.schlist[tName]["{:02}".format(settings.schcount)] = ft
        fire.put("/tasks/"+tName,"{:02}".format(settings.schcount),ft)
    try:
        #print(ft[0])
        threading.Thread(target = Target, name = "{:02}".format(settings.schcount) , args = (tName,t2s(str(ft[0])),ft[1],)).start() #Monitoreo ambiental, efectos de la contaminación en la salud
        ans = "".join("\n> "+str(i+" -> "+j) for i,j in settings.schlist[tName].values())
        if(echo == True): print(ans)
    except ValueError:
        del(settings.schlist[tName]["{:02}".format(settings.schcount)])
        print("Por favor ingrese un valor válido de tiempo!")
    return


def UpDate():
    tasks = fire.get("/tasks",None)
    #print(str(tasks))
    auxnum = 0
    for supkey,supval in tasks.items():
        settings.schlist[supkey] = supval
        print("{}:".format(supkey))
        for infkey,infval in supval.items():
            print("\t{} -> {}".format(infkey,str(infval)))
            settings.schcount = int(infkey)
            ThreadSch(supkey,testThread,infval)
            if(settings.schcount > auxnum):
                auxnum = settings.schcount
        #auxnum = int(list(settings.schlist[supkey].keys())[len(settings.schlist[supkey])-1])
    settings.schcount = auxnum
    settings.schcount+=1

    return


if __name__ == '__main__':
    settings.init()
    try:
        UpDate()
    except AttributeError:
        None
    while(True):
        mess = [0]
        messs = list()
        while(len(mess) < 2):
            print("right now: "+trueTime(cTime()))
            mess = input("Por favor ingrese un recordatorio y una hora en el futuro (formato - \"hh:mm:ss recordatorio\"): ").split(" ")
        messs.append(mess[0])
        messs.append(" ".join(mess[1:len(mess)]))

        ThreadSch("Prueba", testThread, messs, echo = True)
        settings.schcount+=1
        if(settings.schcount > 999): settings.schcount = 0
        #print(str(settings.schlist))



    #return
