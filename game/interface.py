import tkinter as tk
from tkinter import PhotoImage
import random
import math
import time
import os


xp=0
lvl=1
ad=20
maxhp=100
hp=100
ar=15
gold=0
potion=3
escape=3
chest_types=["common","uncommon","epic","legendary"]
monster_types=["slime", "zombie", "spider", "golem", "dragon"]
escaped=False

root = tk.Tk()


def level(lvl):
    xp_required=int(1000*(1.3**lvl))
    return xp_required

def resist(armor):
    if (armor<1000):
        return int(1.2*math.log(armor, 1.08)-15)
    else:
        return 99

def levelup():
    global xp, hp, maxhp, ar, ad, lvl
    xp=xp-level(lvl)
    lvl+=1
    lvlup_label=tk.Label(root, text="You've leveld up, all stats +10%", font=("Arial", 18))
    lvlup_label.place(relx=0.5, rely=0.3, anchor="center")
    root.after(1200, lvlup_label.destroy)
    hp=hp+int(0.1*maxhp)
    maxhp=int(1.1*maxhp)
    ar=int(1.1*ar)
    ad=int(1.1*ad)
    hp_label.config(text="HP: "+str(hp)+"/"+str(maxhp))
    ad_label.config(text="AD: "+str(ad))
    lvl_label.config(text="LVL: "+str(lvl)+" XP: "+str(xp)+"/"+str(level(lvl)))
    ar_label.config(text="Armor: "+str(ar)+" = "+str(resist(ar))+"% DMG resistance")



button_pressed = tk.BooleanVar()
button_pressed.set(False)

button2_pressed = tk.BooleanVar()
button2_pressed.set(False)

button3_pressed = tk.BooleanVar()
button3_pressed.set(False)

def continue_click():
    button_pressed.set(True)

def continue2_click():
    button2_pressed.set(True)

def escape_click():
    global escape, escaped
    button_pressed.set(True)
    escape-=1
    escaped=True
    
def gold_in_chest(type):
    if (type=="common"):
        return random.randint(900,1100)
    elif (type=="uncommon"):
        return random.randint(3000,4000)
    elif (type=="epic"):
        return random.randint(6000,8000)
    elif (type=="legendary"):
        return random.randint(13000,17000)


def chest_content(round):
    global chest_label, gold_get
    chest_type=random.choices(chest_types, [75, 20, 4, 1])[0]
    print("You found", chest_type, "chest")
    gold_ret=gold_in_chest(chest_type)
    chest_label= tk.Label(root, text="You found "+str(chest_type)+" chest", font=("Arial", 24))
    chest_label.place(x=500, y=500)
    if (round<31):
        print("You get", gold_in_chest(chest_type), "gold")
        gold_get= tk.Label(root, text="You get "+str(gold_ret)+" gold", font=("Arial", 24))
        gold_get.place(x=500, y=550)
        return gold_ret
    elif (round>30 and round<51):
        print("You get", 2*gold_in_chest(chest_type), "gold")
        gold_get= tk.Label(root, text="You get "+str(2*gold_ret)+" gold", font=("Arial", 24))
        gold_get.place(x=500, y=550)
        return 2*gold_ret
    else:
        print("You get", 3*gold_in_chest(chest_type), "gold")
        gold_get= tk.Label(root, text="You get "+str(3*gold_ret)+" gold", font=("Arial", 24))
        gold_get.place(x=500, y=550)
        return 3*gold_ret

def monster_type(round):
    if (round<21):
        monster=random.choices(monster_types, \
                               [100-round*2.5, round*2, round*0.5, 0, 0])[0]
    elif (round>20 and round<41):
        monster=random.choices(monster_types, \
                               [100-round*2.5, 100-round*1.2, round*1, round*0.3, 0])[0]
    elif (round>40 and round<81):
        monster=random.choices(monster_types, \
                               [0, 0, 100-round, round*0.7, round*0.3])[0]
    elif (round>80 and round<151):
        monster=random.choices(monster_types, \
                               [0, 0, 0, 100-round*0.6, round*0.6])[0]
    else:
        monster="dragon"
    return monster



def monsters_lvl(round):
    return int(1+round/3)

def slime(round):
    lvl=monsters_lvl(round)
    multi=1
    if (round>80 and round<121):
        multi=1.5
    elif (round>120 and round<161):
        multi=2
    elif (round>160 and round<201):
        multi=3
    elif (round>200):
        multi=5
    hp=40+5*lvl*multi
    ad=10+lvl*multi
    ar=10+4*lvl*multi
    gold=200+30*lvl
    xp=300+70*lvl
    return {"lvl":lvl, "hp":hp, "ad":ad, "ar":ar, "gold":gold, "xp":xp}

def zombie(round):
    lvl=monsters_lvl(round)
    multi=1
    if (round>80 and round<121):
        multi=1.5
    elif (round>120 and round<161):
        multi=2
    elif (round>160):
        multi=3
    hp=70+20*lvl*multi
    ad=10+2*lvl*multi
    ar=15+4*lvl*multi
    gold=300+50*lvl
    xp=500+100*lvl
    return {"lvl":lvl, "hp":hp, "ad":ad, "ar":ar, "gold":gold, "xp":xp}

def spider(round):
    lvl=monsters_lvl(round)
    multi=1
    if (round>80 and round<121):
        multi=1.5
    elif (round>120 and round<161):
        multi=2
    elif (round>160):
        multi=3
    hp=int(50+14*lvl*multi)
    ad=int(30+8*lvl*multi)
    ar=int(10+4*lvl*multi)
    gold=500+100*lvl
    xp=700+200*lvl
    return {"lvl":lvl, "hp":hp, "ad":ad, "ar":ar, "gold":gold, "xp":xp}

def golem(round):
    lvl=monsters_lvl(round)
    multi=1
    if (round>80 and round<121):
        multi=1.5
    elif (round>120 and round<161):
        multi=2
    elif (round>160):
        multi=3
    hp=int(200+60*lvl*multi)
    ad=int(20+4*lvl*multi)
    ar=int(30+10*lvl*multi)
    gold=1000+200*lvl
    xp=1500+300*lvl
    return {"lvl":lvl, "hp":hp, "ad":ad, "ar":ar, "gold":gold, "xp":xp}

def dragon(round):
    lvl=monsters_lvl(round)
    multi=1
    if (round>80 and round<121):
        multi=1.5
    elif (round>120 and round<161):
        multi=2
    elif (round>160):
        multi=3
    hp=int(300+80*lvl*multi)
    ad=int(50+16*lvl*multi)
    ar=int(20+9*lvl*multi)
    gold=2000+300*lvl
    xp=3000+700*lvl
    return {"lvl":lvl, "hp":hp, "ad":ad, "ar":ar, "gold":gold, "xp":xp}


ex=False
def shop():
    global gold, ad, maxhp, ar, xp, potion, esape, ex, round

    while True:
        def exit_shop():
            global ex
            ex=True
            button_pressed.set(True)
        def ad1():
            global button_pressed, gold, ad
            button_pressed.set(True)
            gold-=1000
            ad+=10
        def ad10():
            global button_pressed, gold, ad
            button_pressed.set(True)
            gold-=10000
            ad+=100
        def ad100():
            global button_pressed, gold, ad
            button_pressed.set(True)
            gold-=100000
            ad+=1000
        def ar1():
            global button_pressed, gold, ar
            button_pressed.set(True)
            gold-=1000
            ar+=10
        def ar10():
            global button_pressed, gold, ar
            button_pressed.set(True)
            gold-=10000
            ar+=100
        def ar100():
            global button_pressed, gold, ar
            button_pressed.set(True)
            gold-=100000
            ar+=1000
        def hp1():
            global button_pressed, gold, maxhp, hp
            button_pressed.set(True)
            gold-=1000
            maxhp+=20
            hp+=20
        def hp10():
            global button_pressed, gold, maxhp, hp
            button_pressed.set(True)
            gold-=10000
            maxhp+=200
            hp+=200
        def hp100():
            global button_pressed, gold, maxhp, hp
            button_pressed.set(True)
            gold-=100000
            maxhp+=2000
            hp+=2000
        def xp1():
            global button_pressed, gold, xp
            button_pressed.set(True)
            gold-=1000
            xp+=2000
        def xp10():
            global button_pressed, gold, xp
            button_pressed.set(True)
            gold-=10000
            xp+=20000
        def xp100():
            global button_pressed, gold, xp
            button_pressed.set(True)
            gold-=100000
            xp+=200000
        def pot1():
            global button_pressed, gold, potion
            button_pressed.set(True)
            gold-=1000
            potion+=1
        def pot10():
            global button_pressed, gold, potion
            button_pressed.set(True)
            gold-=10000
            potion+=10
        def pot100():
            global button_pressed, gold, potion
            button_pressed.set(True)
            gold-=100000
            potion+=100
        def esc1():
            global button_pressed, gold, escape, round
            button_pressed.set(True)
            gold=gold-(2000+50*round)
            escape+=1
        def esc10():
            global button_pressed, gold, escape, round
            button_pressed.set(True)
            gold=gold-(20000+500*round)
            escape+=10
        def esc100():
            global button_pressed, gold, escape, round
            button_pressed.set(True)
            gold=gold-(200000+5000*round)
            escape+=100
        cont = tk.Button(root, text='Exit shop and continue', command=exit_shop)
        cont.pack()
        
        shop_ad=tk.Label(root, text="10 AD - 1000 gold", font=("Arial", 18))
        shop_ad.place(x=400, y=390)
        ad_button1 = tk.Button(root, text='Buy 1', command=ad1)
        ad_button1.place(x=400, y=420)
        ad_button10 = tk.Button(root, text='Buy 10', command=ad10)
        ad_button10.place(x=400, y=440)
        ad_button100 = tk.Button(root, text='Buy 100', command=ad100)
        ad_button100.place(x=400, y=460)
        
        shop_esc=tk.Label(root, text="1 Escape - "+str(2000+50*round)+" gold", font=("Arial", 18))
        shop_esc.place(x=1300, y=390)
        esc_button1 = tk.Button(root, text='Buy 1', command=esc1)
        esc_button1.place(x=1300, y=420)
        esc_button10 = tk.Button(root, text='Buy 10', command=esc10)
        esc_button10.place(x=1300, y=440)
        esc_button100 = tk.Button(root, text='Buy 100', command=esc100)
        esc_button100.place(x=1300, y=460)

        shop_ar=tk.Label(root, text="10 Armor - 1000 gold", font=("Arial", 18))
        shop_ar.place(x=400, y=490)
        ar_button1 = tk.Button(root, text='Buy 1', command=ar1)
        ar_button1.place(x=400, y=520)
        ar_button10 = tk.Button(root, text='Buy 10', command=ar10)
        ar_button10.place(x=400, y=540)
        ar_button100 = tk.Button(root, text='Buy 100', command=ar100)
        ar_button100.place(x=400, y=560)

        shop_hp=tk.Label(root, text="20 maxHP - 1000 gold", font=("Arial", 18))
        shop_hp.place(x=400, y=590)
        hp_button1 = tk.Button(root, text='Buy 1', command=hp1)
        hp_button1.place(x=400, y=620)
        hp_button10 = tk.Button(root, text='Buy 10', command=hp10)
        hp_button10.place(x=400, y=640)
        hp_button100 = tk.Button(root, text='Buy 100', command=hp100)
        hp_button100.place(x=400, y=660)

        shop_pot=tk.Label(root, text="1 Health potion - 1000 gold", font=("Arial", 18))
        shop_pot.place(x=1300, y=490)
        pot_button1 = tk.Button(root, text='Buy 1', command=pot1)
        pot_button1.place(x=1300, y=520)
        pot_button10 = tk.Button(root, text='Buy 10', command=pot10)
        pot_button10.place(x=1300, y=540)
        pot_button100 = tk.Button(root, text='Buy 100', command=pot100)
        pot_button100.place(x=1300, y=560)

        shop_xp=tk.Label(root, text="2000 XP - 1000 gold", font=("Arial", 18))
        shop_xp.place(x=1300, y=590)
        xp_button1 = tk.Button(root, text='Buy 1', command=xp1)
        xp_button1.place(x=1300, y=620)
        xp_button10 = tk.Button(root, text='Buy 10', command=xp10)
        xp_button10.place(x=1300, y=640)
        xp_button100 = tk.Button(root, text='Buy 100', command=xp100)
        xp_button100.place(x=1300, y=660)
        
        if gold<100000:
            ad_button100.config(state='disable')
        if gold<10000:
            ad_button10.config(state='disable')
        if gold<1000:
            ad_button1.config(state='disable')

        if gold<100000:
            ar_button100.config(state='disable')
        if gold<10000:
            ar_button10.config(state='disable')
        if gold<1000:
            ar_button1.config(state='disable')

        if gold<100000:
            hp_button100.config(state='disable')
        if gold<10000:
            hp_button10.config(state='disable')
        if gold<1000:
            hp_button1.config(state='disable')

        if gold<100000:
            xp_button100.config(state='disable')
        if gold<10000:
            xp_button10.config(state='disable')
        if gold<1000:
            xp_button1.config(state='disable')

        if gold<100000:
            pot_button100.config(state='disable')
        if gold<10000:
            pot_button10.config(state='disable')
        if gold<1000:
            pot_button1.config(state='disable')

        if gold<200000+5000*round:
            esc_button100.config(state='disable')
        if gold<20000+500*round:
            esc_button10.config(state='disable')
        if gold<2000+50*round:
            esc_button1.config(state='disable')

            



        ad_label.config(text="AD: "+str(ad))
        potion_label.config(text="Potions: "+str(potion))
        ar_label.config(text="Armor: "+str(ar)+" = "+str(resist(ar))+"% DMG resistance")
        while (xp>level(lvl)):
            levelup()
    
        lvl_label.config(text="LVL: "+str(lvl)+" XP: "+str(xp)+"/"+str(level(lvl)))
        hp_label.config(text="HP: "+str(hp)+"/"+str(maxhp))
        escape_label.config(text="Escapes: "+str(escape))
        gold_label.config(text="Gold: "+str(gold))


        
        if ex:
            cont.destroy()
                         
            ad_button1.destroy()
            ad_button10.destroy()
            ad_button100.destroy()
            shop_ad.destroy()

            esc_button1.destroy()
            esc_button10.destroy()
            esc_button100.destroy()
            shop_esc.destroy()

            ar_button1.destroy()
            ar_button10.destroy()
            ar_button100.destroy()
            shop_ar.destroy()

            hp_button1.destroy()
            hp_button10.destroy()
            hp_button100.destroy()
            shop_hp.destroy()

            xp_button1.destroy()
            xp_button10.destroy()
            xp_button100.destroy()
            shop_xp.destroy()

            pot_button1.destroy()
            pot_button10.destroy()
            pot_button100.destroy()
            shop_pot.destroy()
                         
            ex=False
            break
        
        cont.wait_variable(button_pressed)
        cont.destroy()
        
        ad_button1.destroy()
        ad_button10.destroy()
        ad_button100.destroy()
        shop_ad.destroy()

        esc_button1.destroy()
        esc_button10.destroy()
        esc_button100.destroy()
        shop_esc.destroy()

        ar_button1.destroy()
        ar_button10.destroy()
        ar_button100.destroy()
        shop_ar.destroy()

        hp_button1.destroy()
        hp_button10.destroy()
        hp_button100.destroy()
        shop_hp.destroy()

        xp_button1.destroy()
        xp_button10.destroy()
        xp_button100.destroy()
        shop_xp.destroy()

        pot_button1.destroy()
        pot_button10.destroy()
        pot_button100.destroy()
        shop_pot.destroy()
        
        button_pressed.set(False)
        
stats={}
monster="slime"
name2='a'

def fight():
    global round, ad, ar, hp, gold, xp, potion, esape, stats, escaped, monster, name2


    def combat():
        cont.destroy()
        esc_button.destroy()
        global round, ad, ar, hp, gold, xp, potion, esape, stats, monster, name2
        dmg_multiplication=1
        while (stats["hp"]>0):

            cont2 = tk.Button(root, text='Continue', command=continue2_click)
            cont2.pack()
            
            dmg_dealt=int(5*dmg_multiplication*ad*(1-resist(stats["ar"])/100))
            print("\nYou deal", dmg_dealt, "dmg")
            dmg1_label=tk.Label(root, text="-"+str(dmg_dealt), font=("Arial", 20), bg="red")
            dmg1_label.place(x=1500, y=590)
            
            stats["hp"]=stats["hp"]-dmg_dealt
            monhp_label.config(text="HP: "+str(stats["hp"])+"/"+str(mon_maxhp))
            
            cont2.wait_variable(button2_pressed)
            dmg1_label.destroy()
            cont2.destroy()
            button2_pressed.set(False)
            
            if (stats["hp"]<=0):

                cont2 = tk.Button(root, text='Continue', command=continue2_click)
                cont2.pack()
                print("You have slain an enemy")
                slain_label=tk.Label(root, text="You have slain an enemy", font=("Arial", 20))
                slain_label.place(relx=0.5, rely=0.5, anchor="center")
                reward=tk.Label(root, text="You earn "+ str(stats["gold"])+ " gold and "+ str(stats["xp"])+ " xp", font=("Arial", 20))
                goldget_label=tk.Label(root, text="+"+str(stats["gold"]), font=("Arial", 20), bg="yellow")
                goldget_label.place(x=220, y=50)
                root.after(1200, goldget_label.destroy)
                reward.pack()
                gold+=stats["gold"]
                xp+=stats["xp"]
                while (xp>level(lvl)):
                    levelup()

                gold_label.config(text="Gold: "+str(gold))
                lvl_label.config(text="LVL: "+str(lvl)+" XP: "+str(xp)+"/"+str(level(lvl)))
                
                cont2.wait_variable(button2_pressed)
                slain_label.destroy()
                cont2.destroy()
                reward.destroy()
                button2_pressed.set(False)
                
                break
            else:

                cont2 = tk.Button(root, text='Continue', command=continue2_click)
                cont2.pack()
                
                print("Enemy has", stats["hp"], "HP left")
                dmg_dealt2=int(5*dmg_multiplication*stats["ad"]*(1-resist(ar)/100))
                dmg2_label=tk.Label(root, text="-"+str(dmg_dealt2), font=("Arial", 20), bg="red")
                dmg2_label.place(x=220, y=80)
                
                hp=hp-dmg_dealt2
                hp_label.config(text="HP: "+str(hp)+"/"+str(maxhp))
                
                print("\nEnemy deals you", dmg_dealt2, "dmg")
                if (hp<=0):
                    print("You have died")
                    hp_label.destroy()
                    lvl_label.destroy()
                    ar_label.destroy()
                    ad_label.destroy()
                    escape_label.destroy()
                    potion_label.destroy()
                    mon_label1.destroy()
                    mon_label2.destroy()
                    monlvl_label.destroy()
                    monhp_label.destroy()
                    monad_label.destroy()
                    monar_label.destroy()
                    esc_button.destroy()
                    cont.destroy()
                    cont2.destroy()
                    gold_label.destroy()
                    dmg2_label.destroy()
                    
                    match monster:
                        case "slime":
                            slime_label.destroy()

                        case "zombie":
                            zombie_label.destroy()

                        case "spider":
                            spider_label.destroy()
                        
                        case "golem":
                            golem_label.destroy()

                        case "dragon":
                            dragon_label.destroy()

                    background_label.config(image=black)

                    died = tk.Label(root, text="You have died", font=("Arial", 25))
                    died.place(relx=0.5, rely=0.1, anchor="center")

                    name = tk.Label(root, text="Enter your name (no spaces)", font=("Arial", 20))
                    name.place(relx=0.5, rely=0.15, anchor="center")

                    
                
                    entry = tk.Entry(root)
                    entry.place(relx=0.5, rely=0.18, anchor="center")

                    def retrieve_input():
                        global name2
                        name2 = entry.get()
                        button3_pressed.set(True)
                        

                    submit_button = tk.Button(root, text="Submit", command=retrieve_input)
                    submit_button.place(relx=0.5, rely=0.21, anchor="center")

                    submit_button.wait_variable(button3_pressed)
                    submit_button.destroy()
                    entry.destroy()
                    name.destroy()
                
                    
                    with open("scores.txt", "a") as f:
                        
                        f.write(str(name2)+" "+str(round)+"\n")

                    scores = []
                    with open("scores.txt") as f:
                        for line in f:
                            name, score = line.split(' ')
                            score = int(score)
                            scores.append((name, score))

                    scores.sort(key=lambda s: s[1], reverse=True)

                    highscores = tk.Label(root, text="Highscores", font=("Arial", 20))
                    highscores.place(relx=0.5, rely=0.3, anchor="center")

                    score1 = tk.Label(root, text=""+str(scores[0][0])+" "+str(scores[0][1]), font=("Arial", 15))
                    score1.place(relx=0.5, rely=0.35, anchor="center")

                    score2 = tk.Label(root, text=""+str(scores[1][0])+" "+str(scores[1][1]), font=("Arial", 15))
                    score2.place(relx=0.5, rely=0.40, anchor="center")

                    score3 = tk.Label(root, text=""+str(scores[2][0])+" "+str(scores[2][1]), font=("Arial", 15))
                    score3.place(relx=0.5, rely=0.45, anchor="center")

                    score4 = tk.Label(root, text=""+str(scores[3][0])+" "+str(scores[3][1]), font=("Arial", 15))
                    score4.place(relx=0.5, rely=0.50, anchor="center")

                    score5 = tk.Label(root, text=""+str(scores[4][0])+" "+str(scores[4][1]), font=("Arial", 15))
                    score5.place(relx=0.5, rely=0.55, anchor="center")

                    def quitw():
                         os._exit(0)
                    exit_button = tk.Button(root, text="exit", command=quitw)
                    exit_button.place(relx=0.5, rely=0.6, anchor="center")
                    
                    
                else:
                    print("You have", hp, "HP left")


                cont2.wait_variable(button2_pressed)
                cont2.destroy()
                dmg2_label.destroy()
                button2_pressed.set(False)
            
            dmg_multiplication=dmg_multiplication+0.5

            
        button_pressed.set(True)

    
    cont = tk.Button(root, text='Fight', command=combat)
    cont.pack()
    
    monster_stats={"slime":slime(round), "zombie":zombie(round),\
                   "spider":spider(round), "golem":golem(round), "dragon":dragon(round)}

    monster=monster_type(round)
    stats=monster_stats[monster]
    mon_maxhp=stats["hp"]
   

    match monster:
        case "slime":
            slime_label = tk.Label(root, image=slime_image, bd=0)
            slime_label.place(x=743, y=605)

        case "zombie":
            zombie_label = tk.Label(root, image=zombie_image, bd=0)
            zombie_label.place(x=805, y=445)

        case "spider":
            spider_label = tk.Label(root, image=spider_image, bd=0)
            spider_label.place(x=709, y=581)
        
        case "golem":
            golem_label = tk.Label(root, image=golem_image, bd=0)
            golem_label.place(x=565, y=365)

        case "dragon":
            dragon_label = tk.Label(root, image=dragon_image, bd=0)
            dragon_label.place(x=347, y=298)

            
    mon_label1 = tk.Label(root, text="You encountered a "+str(monster), font=("Arial", 20))
    mon_label1.place(x=1300, y=500)

    mon_label2 = tk.Label(root, text="Monster stats:", font=("Arial", 20))
    mon_label2.place(x=1300, y=530)
    
    monlvl_label = tk.Label(root, text="LVL: "+str(stats["lvl"]), font=("Arial", 20))
    monlvl_label.place(x=1300, y=560)

    monhp_label = tk.Label(root, text="HP: "+str(stats["hp"])+"/"+str(mon_maxhp), font=("Arial", 20))
    monhp_label.place(x=1300, y=590)

    monad_label = tk.Label(root, text="AD: "+str(stats["ad"]), font=("Arial", 20))
    monad_label.place(x=1300, y=620)

    monar_label = tk.Label(root, text="Armor: "+str(stats["ar"]), font=("Arial", 20))
    monar_label.place(x=1300, y=650)

    esc_button = tk.Button(root, text='Escape', command=escape_click)
    esc_button.place(x=1300, y=700)
    
    if escape<=0:
        esc_button.config(state='disable')

    cont.wait_variable(button_pressed)
    if escaped:
        cont.destroy()
    mon_label1.destroy()
    mon_label2.destroy()
    monlvl_label.destroy()
    monhp_label.destroy()
    monad_label.destroy()
    monar_label.destroy()
    esc_button.destroy()

    match monster:
        case "slime":
            slime_label.destroy()

        case "zombie":
            zombie_label.destroy()

        case "spider":
            spider_label.destroy()
        
        case "golem":
            golem_label.destroy()

        case "dragon":
            dragon_label.destroy()
    

    
    button_pressed.set(False)


round=0


slime_image = tk.PhotoImage(file="slime.png")
zombie_image = tk.PhotoImage(file="zombie.png")
spider_image = tk.PhotoImage(file="spider.png")
golem_image = tk.PhotoImage(file="golem.png")
dragon_image = tk.PhotoImage(file="dragon.png")
chest_image = tk.PhotoImage(file="chest.png")
black = tk.PhotoImage(file="black.png")



shop_bg = PhotoImage(file="shop_bg.png")

root.title("GAME")

# Create a PhotoImage object from the image file
image = PhotoImage(file="background.png")

# Create a label with the image and set it as the background of the root window
background_label = tk.Label(root, image=image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create corner labels displaying values of a, b, and c
hp_label = tk.Label(root, text="HP: "+str(hp)+"/"+str(maxhp), font=("Arial", 20))
hp_label.place(x=20, y=80)

ad_label = tk.Label(root, text="AD: "+str(ad), font=("Arial", 20))
ad_label.place(x=20, y=110)

gold_label = tk.Label(root, text="Gold: "+str(gold), font=("Arial", 20))
gold_label.place(x=20, y=50)

lvl_label = tk.Label(root, text="LVL: "+str(lvl)+" XP: "+str(xp)+"/"+str(level(lvl)), font=("Arial", 20))
lvl_label.place(x=20, y=20)

ar_label = tk.Label(root, text="Armor: "+str(ar)+" = "+str(resist(ar))+"% DMG resistance", font=("Arial", 15))
ar_label.place(x=20, y=140)

potion_label = tk.Label(root, text="Potions: "+str(potion), font=("Arial", 15))
potion_label.place(x=20, y=165)

escape_label = tk.Label(root, text="Escapes: "+str(escape), font=("Arial", 15))
escape_label.place(x=20, y=190)

slime_image = tk.PhotoImage(file="slime.png")



potion_used=False



def start():
    start.destroy()
    global round, gold, chest_label, gold_get, ad, maxhp, ar, xp, potion, esape, escaped, hp, potion_used
    button_pressed = tk.BooleanVar()
    
    button_pressed.set(False)
    def continue_click():
        button_pressed.set(True)

    noshop=0
        
    while True:
        x=random.randint(0,99)
        if noshop>=15:
            x=5
            
        round+=1
        if round>1:
            round_label.destroy()
        round_label = tk.Label(root, text="Round: "+str(round), font=("Arial", 24))
        round_label.place(relx=0.5, rely=0.03, anchor="center")
        round_label.pack()
        noshop+=1
        #shop
        if x<17:
            noshop=0
            background_label.config(image=shop_bg)
            shop()
            background_label.config(image=image)
    
        #Nothing
        elif (x>16 and x<31):
            cont = tk.Button(root, text='Continue', command=continue_click)
            cont.pack()

            nothing = tk.Label(root, text="There is nothing here", font=("Arial", 24))
            nothing.place(relx=0.5, rely=0.1, anchor="center")
            
            cont.wait_variable(button_pressed)
            cont.destroy()
            button_pressed.set(False)
            nothing.destroy()
        #chest
        elif (x>30 and x<51):
            goldget=chest_content(round)
            gold=gold+goldget
            gold_label.config(text="Gold: "+str(gold))
            
            goldget_label=tk.Label(root, text="+"+str(goldget), font=("Arial", 20), bg="yellow")
            goldget_label.place(x=220, y=50)
            root.after(1200, goldget_label.destroy)
            
            cont = tk.Button(root, text='Continue', command=continue_click)
            cont.pack()
            
            chest_image_label = tk.Label(root, image=chest_image, bd=0)
            chest_image_label.place(x=763, y=580)
            
            cont.wait_variable(button_pressed)
            cont.destroy()
            chest_label.destroy()
            chest_image_label.destroy()
            gold_get.destroy()
            button_pressed.set(False)
        #monster
        else:


            fight()
            escape_label.config(text="Escapes: "+str(escape))
            escaped=False                  


        cont = tk.Button(root, text='Continue', command=continue_click)
        cont.pack()

        if (hp<maxhp):       
            print("You passively heal", int(maxhp/20), "HP")
            if (hp+int(maxhp/20)>maxhp):
                heal_label = tk.Label(root, text="+"+str(maxhp-hp), font=("Arial", 20), bg="green")
                heal_label.place(x=220, y=80)
                root.after(1200, heal_label.destroy)
                hp=maxhp
                
            else:
                heal_label = tk.Label(root, text="+"+str(int(maxhp/20)), font=("Arial", 20), bg="green")
                heal_label.place(x=220, y=80)
                root.after(1200, heal_label.destroy)
                hp+=int(maxhp/20)
                
            hp_label.config(text="HP: "+str(hp)+"/"+str(maxhp))
            
        
        def potion_use():
            global potion, potion_used, maxhp, hp
            potion-=1
            potion_used=True

            if (hp+int(maxhp/4)>maxhp):
                heal_label = tk.Label(root, text="+"+str(maxhp-hp), font=("Arial", 20), bg="green")
                heal_label.place(x=220, y=80)
                root.after(1200, heal_label.destroy)
                hp=maxhp
                
            else:
                heal_label = tk.Label(root, text="+"+str(int(maxhp/4)), font=("Arial", 20), bg="green")
                heal_label.place(x=220, y=80)
                root.after(1200, heal_label.destroy)
                hp+=int(maxhp/4)

            hp_label.config(text="HP: "+str(hp)+"/"+str(maxhp))
            potion_label.config(text="Potions: "+str(potion))
            potion_button.destroy()
            
        potion_button = tk.Button(root, text='Use heal potion', command=potion_use)
        potion_button.pack()

        if potion<=0:
            potion_button.config(state='disable')

        cont.wait_variable(button_pressed)
        cont.destroy()
        if not(potion_used):
            potion_button.destroy()
        potion_used=False
        button_pressed.set(False)


            

start=tk.Button(root, text="Start", command=start)
start.place(relx=0.5, rely=0.5, anchor="center")

root.state("zoomed")

root.mainloop()
