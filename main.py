import discord
from discord.ext import commands, tasks
from discord import app_commands
import urllib.request
import json
import difflib
import sqlite3
import os
import re

emoji={
    "Earth":"<:AttributeEARTH:1557737634577776691>",
    "Wind":"<:AttributeWIND:1557737774533054586>",
    "Water":"<:AttributeWATER:1557737752974327939>",
    "Fire":"<:AttributeFIRE:1557737653363937322>",
    "Light":"<:AttributeLIGHT:1557737672368201849>",
    "Dark":"<:AttributeDARK:1557737581305667614>",
    "Divine":"<:AttributeDIVINE:1557737617271951360>",
    "Spell":"<:AttributeSPELL:1557737697399934999>",
    "Trap":"<:AttributeTRAP:1557737717352243261>",
    "Continuous":"<:TypeContinuous:1557737962429485177>",
    "Counter":"<:TypeCounter:1557738003080945694>",
    "Equip":"<:TypeEquip:1557738036652146719>",
    "Ritual":"<:TypeRitual:1557738158161006633>",
    "Field":"<:TypeField:1557738071385047071>",
    "Quick-Play":"<:TypeQuickPlay:1557738106638172170>",
    "Level":"<:Level:1557743264507891835>",
    "Rank":"<:Rank:1557743285693583422>",
    "Left Scale":"<:PendulumScaleL:1557743326252376144>",
    "Right Scale":"<:PendulumScaleR:1557743354140434553>",
    "Aqua":"<:TypeAqua:1557739582227751044>",
    "Beast":"<:TypeBeast:1557739622899908681>",
    "Beast-Warrior":"<:TypeBeastWarrior:1557739680907272202>",
    "Creator God":"<:TypeCreatorGod:1557739737933029486>",
    "Cyberse":"<:TypeCyberse:1557739814412095548>",
    "Dinosaur":"<:TypeDinosaur:1557739892929204275>",
    "Divine-Beast":"<:TypeDivineBeast:1557739980133109791>",
    "Dragon":"<:TypeDragon:1557740065898102845>",
    "Fairy":"<:TypeFairy:1557740133569134712>",
    "Fiend":"<:TypeFiend:1557740191467180082>",
    "Fish":"<:TypeFish:1557740264389484616>",
    "Illusion":"<:TypeIllusion:1557740336690757694>",
    "Insect":"<:TypeInsect:1557740422665732139>",
    "Machine":"<:TypeMachine:1557740632234131486>",
    "Plant":"<:TypePlant:1557740712903188652>",
    "Psychic":"<:TypePsychic:1557740781454893078>",
    "Pyro":"<:TypePyro:1557740852833550397>",
    "Reptile":"<:TypeReptile:1557740903840612362>",
    "Rock":"<:TypeRock:1557740511278923916>",
    "Sea Serpent":"<:TypeSeaSerpent:1557740966520033293>",
    "Spellcaster":"<:TypeSpellcaster:1557741025752121344>",
    "Thunder":"<:TypeThunder:1557741068156407808>",
    "Warrior":"<:TypeWarrior:1557741121457750166>",
    "Winged Beast":"<:TypeWingedBeast:1557741181058818203>",
    "Wyrm":"<:TypeWyrm:1557741237635780749>",
    "Zombie":"<:TypeZombie:1557741270087245934>"
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
        thedir=os.listdir("./banlists")
        thedir.sort()
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
            emb=discord.Embed(title=card, description=f"{fucking}\n{Type}", color=int(colours[Types[0].lower()],base=16))
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

@tree.command(name="card-art", description="returns card art.")
async def self(interaction:discord.Interaction, card:str, emphemral:bool=False):
    await interaction.response.defer(ephemeral=emphemral)
    card2,CardIDs=await cardnamegen(card)
    if card2!="":
        await interaction.followup.send(f"https://images.ygoprodeck.com/images/cards_cropped/{CardIDs[card2]}.jpg", ephemeral=emphemral)
    else:
        await interaction.followup.send(f"Could not find card matching {card}",ephemeral=emphemral)

bot.run(open("key.txt","r").read())