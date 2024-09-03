import discord
from discord.ext import commands, tasks
from discord import app_commands
import urllib.request
import time
import json
import difflib
import sqlite3
import os
import re

LastCheck=0
layers=[
    "frosting",
    "0",
    "l1",
    "layer 1",
    "layer 1 (vanilla)",
    "vanilla",
    "1",
    "l2",
    "layer 2",
    "layer 2 (chocolate)",
    "chocolate",
    "2",
    "l3",
    "layer 3",
    "layer 3 (cheesecake)",
    "cheesecake",
    "3",
    "l4",
    "layer 4",
    "layer 4 (lemon)",
    "lemon",
    "4"
]

emoji={
    "Earth":"<:Earth:1169843781579833464>",
    "Wind":"<:Wind:1169843998081421322>",
    "Water":"<:Water:1169843948508958730>",
    "Fire":"<:Fire:1169843838148419706>",
    "Light":"<:Light:1169843900001828945>",
    "Dark":"<:Dark:1169843593201066095>",
    "Divine":"<:Divine:1169843709848846356>",
    "Spell":"<:Spell:1169845291768352829>",
    "Trap":"<:Trap:1169845378342989867>",
    "Continuous":"<:Continuous:1169844987366756402>",
    "Counter":"<:Counter:1169845433049301074>",
    "Equip":"<:Equip:1169845058665730049>",
    "Field":"<:Field:1169845178140471306>",
    "Quick-Play":"<:QuickPlay:1169845111262281821>",
    "Level":"<:Level:1169849330644041768>",
    "Rank":"<:Rank:1169849378966609940>",
    "Aqua":"<:Aqua:1169847545527287818>",
    "Beast":"<:Beast:1169847486840574002>",
    "Beast-Warrior":"<:BeastWarrior:1169847419391975454>",
    "Creator God":"<:CreatorGod:1169847327800950814>",
    "Cyberse":"<:Cyberse:1169847270359973948>",
    "Dinosaur":"<:Dinosaur:1169847193134436352>",
    "Divine-Beast":"<:DivineBeast:1169847076289515630>",
    "Dragon":"<:Dragon:1169847007049941053>",
    "Fairy":"<:Fairy:1169846944366076035>",
    "Fiend":"<:Fiend:1169846891752722463>",
    "Fish":"<:Fish:1169846816485941388>",
    "Insect":"<:Insect:1169846728300695692>",
    "Machine":"<:Machine:1169846660264906822>",
    "Plant":"<:Plant:1169846581596540999>",
    "Psychic":"<:Psychic:1169846513845932172>",
    "Pyro":"<:Pyro:1169846419453132800>",
    "Reptile":"<:Reptile:1169846349538271333>",
    "Rock":"<:Rock:1169846290532802630>",
    "Sea Serpent":"<:SeaSerpent:1169846225810497626>",
    "Spellcaster":"<:Spellcaster:1169846161625067550>",
    "Thunder":"<:Thunder:1169846076791066736>",
    "Warrior":"<:Warrior:1169845908972781648>",
    "Winged Beast":"<:WingedBeast:1169845730547081278>",
    "Wyrm":"<:Wyrm:1169845646887497728>",
    "Zombie":"<:Zombie:1169845518973816863>",
    "Illusion":"<:Illusion:1171269929530556457>",#temp
    "Left Scale":"<:LeftScale:1171261697202327623>",
    "Right Scale":"<:RightScale:1171261773228294164>",
    "Ritual":"<:Ritual:1169845232855171133>"
}

colours={
    "effect":"ff8b52",
    "vanilla":"fde689",
    "spell":"1d9e75",
    "ritual":"9cb4cc",
    "link":"01008a",
    "fusion":"a086b6",
    "trap":"bc5a83",
    "synchro":"eeeeee",
    "xyz":"030201"
}

kuchenLogo="https://cdn.discordapp.com/attachments/1020726199904895017/1030482117202821232/unkown4.png"

async def cardnamegen(name):
    con = sqlite3.connect("cards.cdb")
    cur = con.cursor()
    res = cur.execute("SELECT * from texts")
    datas=res.fetchall()
    CardIDs={}
    card=""
    for i in datas:
        if i[1] not in CardIDs:
            CardIDs[i[1]]=i[0]
    for i in CardIDs:
        if name.lower()==i.lower():
            card=i
        elif name.lower() in i.lower() and card=="":
            card=i
    if card=="":
        items=difflib.get_close_matches(name, CardIDs, cutoff=0.3, n=500)
        x=False
        if len(items)>0:
            #print("a")
            for i in items:
                if name.lower() in i.lower() and x==False:
                    card=i
                    x=True
                    #print("yea?", i)
            if card=="":
                card=items[0]
    con.close()
    return card, CardIDs

async def cardembedgen(name):
    ref=["Monster", "Spell", "Trap", "Blank", "Normal", "Effect", "Fusion", "Ritual", "Trap Monster", "Spirit", "Union", "Gemini", "Tuner", "Synchro", "Token", "Maxumum", "Quick-Play", "Continuous", "Equip", "Field", "Counter", "Flip", "Toon", "Xyz", "Pendulum", "spsummon", "Link"]
    #priority={"monster":10, "spell":10, "trap":10, "effect":1, "fusion":2, "ritual":2, "synchro":2, "xyz":2, "link":2, "token":-1}
    card, CardIDs=await cardnamegen(name)
    con = sqlite3.connect("cards.cdb")
    cur = con.cursor()
    if card!="":
        #print(card)
    #name, id, type, attribute, type
        res = cur.execute(f"SELECT * FROM datas WHERE id='{CardIDs[card]}'")
        Data=res.fetchone()#ID, ot, alias, setcode, type, atk, def, level, race, attribute, catagory
        #print(Data)
        #ID=ID
        #ot=worthless
        #alias=worthless
        #setcode=Archetype
        #type=Card Type (link and all that)
        #atk=atk
        #def=def, for links this defines arrows
        #level
        #race=Type (Warrior, fiend and all that)
        races={
            1:"Warrior",
            2:"Spellcaster",
            4:"Fairy",
            8:"Fiend",
            16:"Zombie",
            32:"Machine",
            64:"Aqua",
            128:"Pyro",
            256:"Rock",
            512:"Winged Beast",
            1024:"Plant",
            2048:"Insect",
            4096:"Thunder",
            8192:"Dragon",
            16384:"Beast",
            32768:"Beast-Warrior",
            65536:"Dinosaur",
            131072:"Fish",
            262144:"Sea Serpent",
            524288:"Reptile",
            1048576:"Psychic",
            2097152:"Divine-Beast",
            4194304:"Creator God",
            8388608:"Wyrm",
            16777216:"Cyberse",
            33554432:"Illusion"
        }
        #attribute=attribute
        attributes={
            1:"Earth",
            2:"Water",
            4:"Fire",
            8:"Wind",
            16:"Light",
            32:"Dark",
            64:"Divine"
        }
        #category=Worthless
        #Type Time
        TypeDat=Data[4]
        TypeDat=str(bin(TypeDat)[2:])[::-1]
        #print(TypeDat)
        Types=[]
        count=0
        for a in TypeDat:
            if a=="1":
                Types.append(str(ref[count]))
            count+=1
        for i in ["Blank", "Trap Monster", "Maxumum", "spsummon"]:
            try:
                Types.remove(i)
            except:
                pass
        #print(Types)
        res= cur.execute(f"SELECT desc FROM texts where id='{CardIDs[card]}'")
        text=res.fetchone()[0]
        #print(text)
        Limit={"L1":3, "L2":3, "L3":3, "L4":3, "L5":3}
        order=("L1", "L2", "L3", "L4", "L5")
        count=0
        thedir=[]
        for filename in os.listdir("./banlists"):
            thedir=thedir.append(filename)
        thedir=thedir.sort()
        for filename in thedir:
            if "conf" in filename:
                with open(f"banlists/{filename}", "r",encoding="utf-8") as g:
                    r=g.read()
                    charstor=""
                    corcard=False
                    firline=True
                    z=0
                    for i in r:#check for id in file.
                        if i==" " and firline==False:
                            if z==0:
                                #print(charstor)
                                res=cur.execute(f"SELECT name FROM texts where id='{charstor}'")
                                try:
                                    if res.fetchone()[0]==card:
                                        corcard=True
                                except:
                                    pass
                            if z==1 and corcard==True:
                                Limit[order[count]]=int(charstor)
                                corcard=False
                            z+=1
                            charstor=""
                        elif i=="\n":
                            z=0
                            charstor=""
                            if firline==True:
                                firline=False
                        else:
                            charstor=str(charstor+str(i))
                count+=1
        #print(Limit)
        #emb=discord.Embed(title=card)
        #emb.add_field(name="Limit:", value=f"Fro:{Limit['Fro']}/L1:{Limit['L1']}/L2:{Limit['L2']}/L3:{Limit['L3']}/L4:{Limit['L4']}")
        emb2=None
        fucking="**Limit**:"
        for tits in order:
            if fucking =="**Limit**:":
                fucking=fucking+str(f" {tits}: {Limit[tits]}")
            else:
                fucking=fucking+str(f" / {tits}: {Limit[tits]}")
        if not "Monster" in Types:
            #print("pp")
            #if len 1: normal types0
            #else type1 type0
            if len(Types)==1:
                Type=f"{emoji[Types[0]]} Normal {Types[0]}"
            else:
                Type=f"{emoji[Types[0]]} {Types[1]} {Types[0]} {emoji[Types[1]]}"
            emb=discord.Embed(title=card, description=f"{fucking}", color=int(colours[Types[0].lower()],base=16))
            emb.add_field(name="Card Text", value=text)
        else:
            #print(races[int(Data[8])])
            race=races[int(Data[8])]
            if len(Types)==2:
                Type=f"{emoji[race]} {race} / {Types[1]}"
            elif len(Types)==3:
                Type=f"{emoji[race]} {race} / {Types[1]} / {Types[2]}"
            else:
                Type=f"{emoji[race]} {race} / {Types[1]} / {Types[2]} / {Types[3]}"
            #emb.add_field(name="Type",value=Type.title())
            #print(attributes[int(Data[9])])
            attribute=attributes[int(Data[9])]
            #emb.add_field(name="Attribute", value=attribute)
            if int(Data[5])==-2:
                #print("?")
                atk="?"
            else:
                #print(Data[5])
                atk=Data[5]
            #level
            if "Pendulum" in Types:
                Pend=str(hex(int(Data[7])))[2:]
                #print(Pend)
                #print(int(Pend[6],base=16), int(Pend[0],base=16), int(Pend[2],base=16))
                if len(Pend)!=1:
                    level=[int(Pend[6],base=16),int(Pend[0],base=16),int(Pend[2],base=16)]
                else:
                    level=[int(Pend,base=16),0,0]
                if "Link" in Types:
                    level=f"**Link Rating:** {level[0]} **Pendulum Scale:** {emoji['Left Scale']} {level[1]}/{level[2]} {emoji['Right Scale']}"
                    colour="link"
                elif "Xyz" in Types:
                    level=f"**Rank:** {emoji['Rank']} {level[0]} **Pendulum Scale:** {emoji['Left Scale']} {level[1]}/{level[2]} {emoji['Right Scale']}"
                    colour="xyz"
                else:
                    level=f"**Level:** {emoji['Level']} {level[0]} **Pendulum Scale:** {emoji['Left Scale']} {level[1]}/{level[2]} {emoji['Right Scale']}"
                    colour=""
                    for h in ["effect","fusion","synchro","ritual"]:
                        if h.title() in Types:
                            colour=h
                    if colour=="":
                        colour="vanilla"
                #text=text.replace("[ Pendulum Effect ]\n","")
                #text=text.replace("[ Monster Effect ]\n","")
                texts=text.split("----------------------------------------")
                if len(texts)==1:
                    text=""
                    text2=texts[0]
                else:
                    text=texts[0].replace((texts[0].split('\n')[0])+"\n","")
                    text2=texts[-1].replace((texts[-1].split('\n')[1])+"\n","")
                #print(text,"\n", text2)
                emb2=discord.Embed(color=int(colours["spell"],base=16))
                emb2.add_field(name="Card Text", value=text2)
            else:
                if "Link" in Types:#link colour
                    level=f"**Link Rating:** {Data[7]}"
                    colour="link"
                elif "Xyz" in Types:#xyz colour
                    level=f"**Rank:** {emoji['Rank']} {Data[7]}"
                    colour="xyz"
                else:#check if any of the others(fusion, ritual, synchro, effect, normal)
                    level=f"**Level:** {emoji['Level']} {Data[7]}"
                    colour=""
                    for h in ["effect","fusion","synchro","ritual"]:
                        if h.title() in Types:
                            colour=h
                    if colour=="":
                        colour="vanilla"
            #def
            if "Link" in Types:
                arrows=["↙","↓","↘","←","","→","↖","↑","↗"]
                Link=str(bin(Data[6])[2:])[::-1]
                #print(Link)
                count=0
                Arrow=[]
                for i in Link:
                    if i=="1":
                        Arrow.append(arrows[count])
                    count+=1
                #print(Arrow)
                fir=True
                for i in Arrow:
                    if fir==True:
                        Def=f"**Link Arrows:** {i}"
                        fir=False
                    else:
                        Def=f"{Def} {i}"
            else:
                if int(Data[6])==-2:
                    Def="**DEF**: ?"
                else:
                    Def=f"**DEF:** {Data[6]}"
                #print(Def)
            emb=discord.Embed(title=card, description=f"{fucking}\n**Type:** {Type}\n**Attribute:** {emoji[attribute]} {attribute}\n{level} **ATK**: {atk} {Def}", color=int(colours[colour],base=16))
            if emb2==None:
                emb.add_field(name="Card Text", value=text)
            else:
                emb.add_field(name="Pendulum Effect", value=text)

            #print("pp")
        emb.set_thumbnail(url=f"https://images.ygoprodeck.com/images/cards_cropped/{CardIDs[card]}.jpg")
    else:
        emb=None
        emb2=None
    con.close()
    return emb, emb2

async def DownloadandProcessReplay():
    urllib.request.urlretrieve("https://docs.google.com/spreadsheets/d/13Wd7MI58RhdhWqjCaWeZ_IBZm_1cEwr_O6z87j1i0M8/export?format=tsv", "ReplayData.tsv")
    #Timestamp, tier, winner, loser, wscore, lscore, replay, winner decklist, loser decklist, warch, larch, tourney
    with open("data.json", "r", encoding="utf-8") as g:
        data=json.load(g)
    with open("ReplayData.tsv", "r", encoding="utf-8") as g:
        CharSt=""
        ListSt=[]
        ListPos=0
        FirstLine=True
        for i in g.read():
            if i not in ["\t", "\n"]:
                CharSt=str(CharSt+i)
            else:
                if ListPos <12:
                    ListSt.append(CharSt)
                    if ListPos==11:
                        if FirstLine!=True:
                            if ListSt[0] not in data:
                                data[ListSt[0]]={
                                    "layer":ListSt[1].lower(),
                                    "winner":ListSt[2].lower(),
                                    "loser":ListSt[3].lower(),
                                    "score":f"{ListSt[4]}-{ListSt[5]}",
                                    "replays":list(ListSt[6].split(", ")),
                                    "warch":[ListSt[9].lower()],
                                    "wlink":ListSt[7],
                                    "larch":[ListSt[10].lower()],
                                    "llink":ListSt[8],
                                    "tournament":ListSt[11]
                                }
                        else:
                            FirstLine=False
                        ListSt=[]
                if i=="\n":
                    ListPos=-1
                ListPos+=1
                CharSt=""
    with open("data.json", "w", encoding="utf-8") as g:
        json.dump(data, g)

async def CardDatabaseStrip():
    ref=["Monster", "Spell", "Trap", "Blank", "Normal", "Effect", "Fusion", "Ritual", "Trap Monster", "Spirit", "Union", "Gemini", "Tuner", "Synchro", "Token", "Maxumum", "Quick-Play", "Continuous", "Equip", "Field", "Counter", "Flip", "Toon", "Xyz", "Pendulum", "spsummon", "Link"]
    #print("penis")
    con = sqlite3.connect("cards.cdb")
    cur = con.cursor()
    invalidids=[]
    cur.execute("SELECT id FROM datas WHERE ot='1'")
    datas=cur.fetchall()
    cur.execute("DELETE FROM datas WHERE ot='1'")
    for i in datas:
        invalidids.append(i[0])
    #print(invalidids)
    cur.execute("SELECT id FROM datas WHERE ot='0'")
    datas=cur.fetchall()
    cur.execute("DELETE FROM datas WHERE ot='0'")
    for i in datas:
        invalidids.append(i[0])
    #print(invalidids)
    for i in invalidids:
        cur.execute(f"DELETE FROM texts WHERE id='{i}'")
    cur.execute("SELECT name FROM texts")
    datas=cur.fetchall()
    #print(datas)
    names=[]
    for i in datas:
        if "token" in i[0].lower():
            #print(i[0])
            cur.execute(f'SELECT id FROM texts WHERE name="{i[0]}"')
            h=cur.fetchall()
            for j in h:
                cur.execute(f"SELECT type FROM datas WHERE id='{j[0]}'")
                Type=cur.fetchall()[0]
                Type=str(bin(int(Type[0]))[2:])[::-1]
                #print(Type)
                Types=[]
                count=0
                for a in Type:
                    if a=="1":
                        Types.append(str(ref[count]))
                    count+=1
                if "Token" in Types:
                    cur.execute(f"DELETE FROM datas wHERE id='{j[0]}'")
                    names.append(i[0])
                    cur.execute(f'DELETE FROM texts WHERE name="{i[0]}"')
    #print(names)
    con.commit()
    con.close()

async def downloadcdb():
    urllib.request.urlretrieve("https://github.com/ProjectIgnis/BabelCDB/raw/master/cards.cdb", "cards.cdb")
    await CardDatabaseStrip()

class client(discord.AutoShardedClient):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synched=False
    
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synched:
            await tree.sync()
            self.synched=True

    async def on_message(self,message):
        if message.author.bot==False:
            #print(message)
            a=int(message.channel.id)
            #print(message.content)
            #print(message.attachments)
            if len(message.content)>2:
                for i in re.findall("\[(.*?)\]",message.content):
                    if i.count(":")<=1:
                        emb,emb2=await cardembedgen(i.title())
                        if emb!=None:
                            if emb2!=None:
                                await message.reply(embeds=[emb,emb2])
                            else:
                                await message.reply(embed=emb)

bot=client()
tree=app_commands.CommandTree(bot)

@tree.command(name="ping", description="Sends latency")
async def self(interaction:discord.Interaction, emphemral:bool=False):
    await interaction.response.send_message(f"Pong {round(bot.latency*1000)}ms", allowed_mentions=False, ephemeral=emphemral)
    #await CardDatabaseStrip()

@tree.command(name="updatedatabase", description="does that")
async def self(interaction:discord.Interaction):
    if str (interaction.user.id)!="342940277931245568":
        await interaction.response.send_message("Missing Required Permissions", ephemeral=True)
    else:
        await interaction.response.send_message("Updating.", ephemeral=True)
        await downloadcdb()

# @tree.command(name="layer-stats", description="Sends stats for specified layer")
# async def self(interaction:discord.Interaction, layer:str, emphemral:bool=False):
#     global LastCheck
#     global layers
#     global kuchenLogo
#     if time.time()-LastCheck>=3600:
#         await DownloadandProcessReplay()
#         LastCheck=time.time()
#     if layer.lower() not in layers:
#         await interaction.response.send_message(f"{layer} is not a valid layer", ephemeral=True)
#     else:
#         await interaction.response.defer(ephemeral=emphemral)
#         if layer.lower() in ["l4", "layer 4", "layer 4 (lemon)", "lemon", "4"]:
#             layer="layer 4 (lemon)"
#         elif layer.lower() in ["l3", "layer 3", "layer 3 (cheesecake)", "cheesecake", "3"]:
#             layer="layer 3 (cheesecake)"
#         elif layer.lower() in ["l2", "layer 2", "layer 2 (chocolate)", "chocolate", "2"]:
#             layer="layer 2 (chocolate)"
#         elif layer.lower() in ["l1", "layer 1", "layer 1 (vanilla)", "vanilla", "1"]:
#             layer="layer 1 (vanilla)"
#         else:
#             layer="frosting"
#         with open ("data.json","r", encoding="utf-8")as g:
#             data=json.load(g)
#             layerdata={}
#             for i in data:
#                 if data[i]["layer"]==layer:
#                     layerdata[i]=data[i]
#             tournaments=[]
#             players={}
#             archetypes={}
#             for i in layerdata:
#                 if layerdata[i]["tournament"] not in tournaments:
#                     if layerdata[i]["tournament"] != "N/A":
#                         tournaments.append(layerdata[i]["tournament"])
#                 if layerdata[i]["winner"] not in players:
#                     players[layerdata[i]["winner"]]=0
#                 players[layerdata[i]["winner"]]+=1
#                 if layerdata[i]["loser"] not in players:
#                     players[layerdata[i]["loser"]]=0
#                 players[layerdata[i]["loser"]]+=1
#                 for k in layerdata[i]["warch"]:
#                     if k not in archetypes:
#                         archetypes[k]=0
#                     archetypes[k]+=1
#                 for k in layerdata[i]["larch"]:
#                     if k not in archetypes:
#                         archetypes[k]=0
#                     archetypes[k]+=1
#             emb=discord.Embed(title=layer.title(), description=f"**Number of Games** - {len(layerdata)}\n**Number of Players** - {len(players)}")
#             emb.set_thumbnail(url=kuchenLogo)
#             players=dict(sorted(players.items(), key=lambda x:x[1], reverse=True))
#             archetypes=dict(sorted(archetypes.items(), key=lambda x:x[1], reverse=True))
#             playerlist=""
#             count=1
#             for i in players:
#                 if count<=5:
#                     if count ==1:
#                         playerlist=f"{count}. **{i}** - {players[i]}"
#                     else:
#                         playerlist=f"{playerlist}\n{count}. **{i}** - {players[i]}"
#                 count+=1
#             while count <=5:
#                 playerlist=f"{playerlist}\n{count}. N/A"
#                 count+=1
#             archlist=""
#             count=1
#             for i in archetypes:
#                 if count<=5:
#                     if count ==1:
#                         archlist=f"{count}. **{i}** - {archetypes[i]}"
#                     else:
#                         archlist=f"{archlist}\n{count}. **{i}** - {archetypes[i]}"
#                 count+=1
#             while count <=5:
#                 archlist=f"{archlist}\n{count}. N/A"
#                 count+=1
#             emb.add_field(name="Top Players", value=playerlist, inline=True)
#             emb.add_field(name="Top Archetypes", value=archlist, inline=True)
#             tournamentstr=""
#             if len(tournaments)==0:
#                 tournamentstr="N/A"
#             else:
#                 for i in tournaments:
#                     if tournamentstr=="":
#                         tournamentstr=i
#                     else:
#                         tournamentstr=f"{tournamentstr}\n{i}"
#             emb.add_field(name="Tournaments", value=tournamentstr, inline=False)
#         await interaction.followup.send(embed=emb, ephemeral=emphemral)

# @tree.command(name="kuchen-stats",description="Server Wide Stats")
# async def self(interaction:discord.Interaction, emphemral:bool=False):
#     global LastCheck
#     global kuchenLogo
#     if time.time()-LastCheck>=1800:
#         await DownloadandProcessReplay()
#         LastCheck=time.time()
#     await interaction.response.defer(ephemeral=emphemral)
#     with open("data.json", "r", encoding="utf-8")as g:
#         data=json.load(g)
#         layer={}
#         player={}
#         archetypes={}
#         tournament=[]
#         for i in data:
#             if data[i]["layer"] not in layer:
#                 layer[data[i]["layer"]]=0
#             layer[data[i]["layer"]]+=1
#             if data[i]["winner"]not in player:
#                 player[data[i]["winner"]]=0
#             player[data[i]["winner"]]+=1
#             if data[i]["loser"]not in player:
#                 player[data[i]["loser"]]=0
#             player[data[i]["loser"]]+=1
#             for k in data[i]["warch"]:
#                 if k not in archetypes:
#                     archetypes[k]=0
#                 archetypes[k]+=1
#             for k in data[i]["larch"]:
#                 if k not in archetypes:
#                     archetypes[k]=0
#                 archetypes[k]+=1
#             if data[i]["tournament"]!="N/A":
#                 if data[i]["tournament"]not in tournament:
#                     tournament.append(data[i]["tournament"])
#         player=dict(sorted(player.items(), key=lambda x:x[1], reverse=True))
#         layer=dict(sorted(layer.items(), key=lambda x:x[1], reverse=True))
#         archetypes=dict(sorted(archetypes.items(), key=lambda x:x[1], reverse=True))
#         count=1
#         for i in layer:
#             if count==1:  
#                 emb=discord.Embed(title="Kuchen Stats", description=f"**Number of Games** - {len(data)}\n**Number of Players** - {len(player)}\n**Most Player Layer** - {i}")
#             count+=1
#         emb.set_thumbnail(url=kuchenLogo)
#         count=1
#         playerstr=""
#         for i in player:
#             if count<=5:
#                 if count==1:
#                     playerstr=f"{count}. **{i}** - {player[i]}"
#                 else:
#                     playerstr=f"{playerstr}\n{count}. **{i}** - {player[i]}"
#             count+=1
#         while count<=5:
#             playerstr=f"{playerstr}\n{count}. N/A"
#             count+=1
#         count=1
#         archstr=""
#         for i in archetypes:
#             if count<=5:
#                 if count==1:
#                     archstr=f"{count}. **{i}** - {archetypes[i]}"
#                 else:
#                     archstr=f"{archstr}\n{count}. **{i}** - {archetypes[i]}"
#             count+=1
#         while count<=5:
#             archstr=f"{archstr}\n{count}. N/A"
#             count+=1
#         tournamentstr=""
#         if len(tournament)==0:
#             tournamentstr="N/A"
#         else:
#             for i in tournament:
#                 if tournamentstr=="":
#                     tournamentstr=i
#                 else:
#                     tournamentstr=f"{tournamentstr}\n{i}"
#         emb.add_field(name="Top Players", value=playerstr, inline=True)
#         emb.add_field(name="Top Archetypes", value=archstr, inline=True)
#         #emb.add_field(name="Tournaments", value=tournamentstr, inline=False)
#     await interaction.followup.send(embed=emb, ephemeral=emphemral)

# @tree.command(name="player-stats", description="Sends stats for specified player")
# async def self(interaction:discord.Interaction, player:str, emphemral:bool=False):
#     global LastCheck
#     global kuchenLogo
#     player=player.lower()
#     if time.time()-LastCheck>=1800:
#         await DownloadandProcessReplay()
#         LastCheck=time.time()
#     await interaction.response.defer(ephemeral=emphemral)
#     with open ("data.json","r", encoding="utf-8")as g:
#         data=json.load(g)
#     playerdata={}
#     for i in data:
#         if data[i]["winner"]==player:
#             playerdata[i]=data[i]
#         elif data[i]["loser"]==player:
#             playerdata[i]=data[i]
#     if len(playerdata)==0:
#         await interaction.followup.send(f"{player} is not a valid player", ephemeral=True)
#     else:
#         archetypes={}
#         tournaments=[]
#         layer={}
#         wdl={"win":0, "draw":0, "loss":0}
#         for i in playerdata:
#             if playerdata[i]["winner"]==player:
#                 for k in playerdata[i]["warch"]:
#                     if k not in archetypes:
#                         archetypes[k]=0
#                     archetypes[k]+=1
#                 score=list(playerdata[i]["score"].split("-"))
#                 if int(score[0])>int(score[1]):
#                     wdl["win"]+=1
#                 elif int(score[0])==int(score[1]):
#                     wdl["draw"]+=1
#                 elif int(score[0])<int(score[1]):
#                     wdl["loss"]+=1
#             elif playerdata[i]["loser"]==player:
#                 for k in playerdata[i]["larch"]:
#                     if k not in archetypes:
#                         archetypes[k]=0
#                     archetypes[k]+=1
#                 score=list(playerdata[i]["score"].split("-"))
#                 if int(score[0])>int(score[1]):
#                     wdl["loss"]+=1
#                 elif int(score[0])==int(score[1]):
#                     wdl["draw"]+=1
#                 elif int(score[0])<int(score[1]):
#                     wdl["win"]+=1
#             if playerdata[i]["tournament"] not in tournaments:
#                 if playerdata[i]["tournament"]!="N/A":
#                     tournaments.append(playerdata[i]["tournament"])
#             if playerdata[i]["layer"]not in layer:
#                 layer[playerdata[i]["layer"]]=0
#             layer[playerdata[i]["layer"]]+=1
#         layer=dict(sorted(layer.items(), key=lambda x:x[1], reverse=True))
#         archetypes=dict(sorted(archetypes.items(), key=lambda x:x[1], reverse=True))
#         emb=discord.Embed(title=player.title(), description=f"**Number of Games** - {len(playerdata)}\n**Win**-**Draw**-**Loss** - **{wdl['win']}**-**{wdl['draw']}**-**{wdl['loss']}**")
#         emb.set_thumbnail(url=kuchenLogo)
#         count=1
#         layerstr=""
#         for i in layer:
#             if count<=5:
#                 if count==1:
#                     layerstr=f"{count}. **{i}** - {layer[i]}"
#                 else:
#                     layerstr=f"{layerstr}\n{count}. **{i}** - {layer[i]}"
#             count+=1
#         while count<=5:
#             layerstr=f"{layerstr}\n{count}. N/A"
#             count+=1
#         count=1
#         archstr=""
#         for i in archetypes:
#             if count<=5:
#                 if count==1:
#                     archstr=f"{count}. **{i}** - {archetypes[i]}"
#                 else:
#                     archstr=f"{archstr}\n{count}. **{i}** - {archetypes[i]}"
#             count+=1
#         while count <=5:
#             archstr=f"{archstr}\n{count}. N/A"
#             count+=1
#         tournamentstr=""
#         if len(tournaments)==0:
#             tournamentstr="N/A"
#         else:
#             for i in tournaments:
#                 if tournamentstr=="":
#                     tournamentstr=i
#                 else:
#                     tournamentstr=f"{tournamentstr}\n{i}"
#         emb.add_field(name="Top Layers", value=layerstr, inline=True)
#         emb.add_field(name="Top Archetypes", value=archstr, inline=True)
#         emb.add_field(name="Tournaments", value=tournamentstr, inline=False)
#         await interaction.followup.send(embed=emb, ephemeral=emphemral)

# @tree.command(name="archetype-stats", description="Sends stats for specified archetype")
# async def self(interaction:discord.Interaction, archetype:str, emphemral:bool=False):
#     global LastCheck
#     global kuchenLogo
#     archetype=archetype.lower()
#     if time.time()-LastCheck>=1800:
#         await DownloadandProcessReplay()
#         LastCheck=time.time()
#     await interaction.response.defer(ephemeral=emphemral)
#     with open ("data.json","r", encoding="utf-8")as g:
#         data=json.load(g)
#     archdata={}
#     for i in data:
#         if i not in archdata:
#             if archetype in data[i]["warch"]:
#                 archdata[i]=data[i]
#             elif archetype in data[i]["larch"]:
#                 archdata[i]=data[i]
#     if len(archdata)==0:
#         await interaction.followup.send(f"{archetype} is not a valid archetype", ephemeral=True)
#     else:
#         players={}
#         tournaments=[]
#         layers={}
#         playedwith={}
#         wdl={"win":0,"draw":0,"loss":0}

@tree.command(name="card-art", description="returns card art.")
async def self(interaction:discord.Interaction, card:str, emphemral:bool=False):
    await interaction.response.defer(ephemeral=emphemral)
    card2,CardIDs=await cardnamegen(card)
    if card2!="":
        await interaction.followup.send(f"https://images.ygoprodeck.com/images/cards_cropped/{CardIDs[card2]}.jpg", ephemeral=emphemral)
    else:
        await interaction.followup.send(f"Could not find card matching {card}",ephemeral=emphemral)

bot.run(open("key.txt","r").read())
