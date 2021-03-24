from re import T
import requests
from bs4 import BeautifulSoup as bs
import copy
from random import choices, randint

def initialize(monster):
    
    url = "https://oldschool.runescape.wiki/w/" + str(monster)
    data = requests.get(url)
    if not data.ok:
        quit
    data = bs(data.text, 'html.parser')
    
    global dropMultiplier
    dropMultiplier = 1
    
    nonmembersItems =   data.findAll(class_ = "nonmembers-item")
    membersItems    =   data.findAll(class_ = "members-item")
    return nonmembersItems, membersItems




def getItems(membersItems, nonmembersItems):
    dropDict = {}
    for n, item in enumerate(membersItems):
        newItem = []
        noted = [0]
        for what in item:
            for x in what.descendants:
                if str(x)[0] != "<" and str(x)[0] != "[" and str(x)[0] != ";" and str(x)[0] != "–":
                    if str(x)[0] == "(":
                        noted = [1]
                    else:
                        newItem.append(str(x))

        if len(newItem) == 6:
            del newItem[3]
            
        dropDict[n]                 = {}
        dropDict[n]["itemName"]     = newItem[0]
        dropDict[n]["dropAmount"]   = newItem[1]
        dropDict[n]["dropRate"]     = newItem[2]
        dropDict[n]["itemValue"]    = newItem[3]
        dropDict[n]["alchPrice"]    = newItem[4]
        dropDict[n]["noted"]        = noted
        
    if len(membersItems) < 1:
        n = 0
        
    for n, item in enumerate(nonmembersItems, n):
        newItem = []
        noted = [0]
        for what in item:
            for x in what.descendants:
                if str(x)[0] != "<" and str(x)[0] != "[" and str(x)[0] != ";" and str(x)[0] != "–":
                    if str(x)[0] == "(":
                        noted = [1]
                    else:
                        newItem.append(str(x))

        if len(newItem) == 6:
            del newItem[3]
    
        dropDict[n]                 = {}
        dropDict[n]["itemName"]     = newItem[0]
        dropDict[n]["dropAmount"]   = newItem[1]
        dropDict[n]["dropRate"]     = newItem[2]
        dropDict[n]["itemValue"]    = newItem[3]
        dropDict[n]["alchPrice"]    = newItem[4]
        dropDict[n]["noted"]        = noted
    
    return dropDict

def fixDropDict(dropDict):
    
    for drop in dropDict:
        
        # DropAmount FIX
        dropDict[drop]["dropAmount"] = dropDict[drop]["dropAmount"].replace(",", "")
        dropDict[drop]["dropAmount"] = dropDict[drop]["dropAmount"].split("–")
        for index in range(len(dropDict[drop]["dropAmount"])):
            if dropDict[drop]["dropAmount"][index][0].isdigit():
                dropDict[drop]["dropAmount"][index] = int(dropDict[drop]["dropAmount"][index])
            else:
                dropDict[drop]["dropAmount"] = [0]
        
        # DropRate FIX
        dropDict[drop]["dropRate"] = dropDict[drop]["dropRate"].replace(",", "")
        dropDict[drop]["dropRate"] = dropDict[drop]["dropRate"].replace(" ", "")
        dropDict[drop]["dropRate"] = dropDict[drop]["dropRate"].replace("×", "/")
        dropDict[drop]["dropRate"] = dropDict[drop]["dropRate"].split("/")
        if dropDict[drop]["dropRate"][0] != "Always":
            if len(dropDict[drop]["dropRate"]) == 3:
                global dropMultiplier
                dropMultiplier = dropDict[drop]["dropRate"][0]
                del dropDict[drop]["dropRate"][0]
            for index in range(len(dropDict[drop]["dropRate"])):
                dropDict[drop]["dropRate"][index] = float(dropDict[drop]["dropRate"][index])
            dropDict[drop]["dropRate"] = [dropDict[drop]["dropRate"][0] / dropDict[drop]["dropRate"][1]]
            
        # ItemValue FIX
        dropDict[drop]["itemValue"] = dropDict[drop]["itemValue"].replace(",", "")
        dropDict[drop]["itemValue"] = dropDict[drop]["itemValue"].split("–")
        if dropDict[drop]["itemValue"][0][0].isdigit():
            for index in range(len(dropDict[drop]["itemValue"])):
                dropDict[drop]["itemValue"][index] = float(dropDict[drop]["itemValue"][index])
        else: 
            dropDict[drop]["itemValue"] = [0]
            
        # AlchPrice FIX
        dropDict[drop]["alchPrice"] = dropDict[drop]["alchPrice"].replace(",", "")
        dropDict[drop]["alchPrice"] = dropDict[drop]["alchPrice"].split("–")
        if dropDict[drop]["alchPrice"][0][0].isdigit():
            for index in range(len(dropDict[drop]["alchPrice"])):
                dropDict[drop]["alchPrice"][index] = float(dropDict[drop]["alchPrice"][index])
        else: 
            dropDict[drop]["alchPrice"] = [0]
        
        # Add UnitPrice
        try:
            dropDict[drop]["unitPrice"] = [dropDict[drop]["itemValue"][0] / dropDict[drop]["dropAmount"][0]]
        except ZeroDivisionError:
            dropDict[drop]["unitPrice"] = [0]
        
        dropDict[drop]["itemName"] = dropDict[drop]["itemName"] + "_" + str(dropDict[drop]["dropAmount"][0])
        
    # Remove Duplicates
    """for drop in dropDict:
        for check in dropDict:
            if dropDict[drop]["itemName"] == dropDict[check]["itemName"]:
                if drop != check:
                    del dropDict[check]"""
    
    return dropDict
    
def finDropDict(dropDict):
    newDict = copy.deepcopy(dropDict)
    for item in newDict:
        newDict[item]["dropAmount"] = 0
        newDict[item]["itemValue"]  = 0
        newDict[item]["unitPrice"]  = 0
        del newDict[item]["dropRate"]
        del newDict[item]["noted"]
        del newDict[item]["alchPrice"]

    return newDict

def dropAmounts(dropDict, newDict, killCount=1):
    
    nameList    = []
    weightList  = []
    
    # Always dropping items
    for kill in range(killCount):
        for drop in dropDict:
            if dropDict[drop]["dropRate"][0] == "Always":
                if len(dropDict[drop]["dropAmount"]) == 2:
                    newDict[drop]["dropAmount"] += randint(dropDict[drop]["dropAmount"][0], dropDict[drop]["dropAmount"][1])
                else:
                    newDict[drop]["dropAmount"] += dropDict[drop]["dropAmount"][0]
            
    # % drops
    for drop in dropDict:
        if dropDict[drop]["dropRate"][0] != "Always":
            nameList.append(dropDict[drop]["itemName"])
            weightList.append(dropDict[drop]["dropRate"][0])
            
    global dropMultiplier
    killCount *= int(dropMultiplier)
    drops = choices(nameList, weightList, k=killCount)
    killCount /= int(dropMultiplier)
    killCount = int(killCount)
    
    for drop in range(len(drops)):
        for ndrop in newDict:
            if drops[drop] == newDict[ndrop]["itemName"]:
                if len(dropDict[ndrop]["dropAmount"]) == 2:
                    newDict[ndrop]["dropAmount"] += randint(dropDict[ndrop]["dropAmount"][0], dropDict[ndrop]["dropAmount"][1])
                else:
                    newDict[ndrop]["dropAmount"] += dropDict[ndrop]["dropAmount"][0]
    
    return newDict, killCount

def itemValues(dropDict, newDict):
    
    for item in newDict:
        if newDict[item]["dropAmount"] > 0:
            newDict[item]["itemValue"] = int(newDict[item]["dropAmount"]) * int(dropDict[item]["unitPrice"][0])
        newDict[item]["unitPrice"] = int(dropDict[item]["unitPrice"][0])
        
    return newDict

def sortByHighestValue(newDict):
    
    newDict = sorted(newDict, key=lambda x: (newDict[x]['itemValue']))
    return newDict

def totalAndAverageValue(newDict, killCount):
    total = 0
    for item in newDict:
        if newDict[item]["dropAmount"] > 0:
            total += int(newDict[item]["itemValue"])
    
    average = int(round((total / killCount), 0))
    
    if len(str(total)) > 7:
        total = str(total)
        total = str(total[:-6])+"M"
    
    elif len(str(total)) > 4:
        total = str(total)
        total = str(total[:-3])+"K"
        
    if len(str(average)) > 7:
        average = str(average)
        average = str(average[:-6])+"M"
    
    elif len(str(average)) > 4:
        average = str(average)
        average = str(average[:-3])+"K"
    
    return total, average
    
    
if __name__ == "__main__":
    nmi, mi     = initialize("kreearra")
    dropDict    = getItems(mi, nmi)
    dropDict    = fixDropDict(dropDict)
    newDict     = finDropDict(dropDict)
    newDict, kc = dropAmounts(dropDict, newDict, killCount=1337)
    newDict     = itemValues(dropDict, newDict)
    drops       = sortByHighestValue(newDict)
    total, avg  = totalAndAverageValue(newDict, kc)
    
    for drop in drops:
        if newDict[drop]["dropAmount"] > 0:
            print(newDict[drop])
    
    print(f"Kills :\t\t{kc}")
    print(f"Total :\t\t{total} gp")
    print(f"Average :\t{avg} gp")
