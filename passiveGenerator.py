import json
import os
from urllib.request import urlopen
from urllib.error import HTTPError


def saveInfo(obj, filename):  # Save function!
    f = open(filename, 'w')
    json.dump(obj, f)
    f.close()
    print("Saved to file: " + filename)


dirpath = os.getcwd()
filename = "items.json.txt"
ls_filename = "ls.json.txt"
es_filename = "es.json.txt"
datamine_url = "https://raw.githubusercontent.com/Deathmax/bravefrontier_data/master/items.json"
ls_url = "https://raw.githubusercontent.com/Deathmax/bravefrontier_data/master/ls.json"
es_url = "https://raw.githubusercontent.com/Deathmax/bravefrontier_data/master/es.json"
errors = 0
globalArr=[]
globalBuffArr=[]
statusArr=[]
statusCheck=False
arrCount=0

items={}
try:
    #print("Attempting to load file data from " + filename + "...")
    with open(filename) as data_file:
        items = json.load(data_file)
    with open(ls_filename) as data_file:
        ls = json.load(data_file)
    with open(es_filename) as data_file:
        es = json.load(data_file)
    #print("Success loading file data!")
except FileNotFoundError:
    print("Failure to load file data. Attempting online datamine...")
    try:
        with urlopen(datamine_url) as url:
            items = json.loads(url.read().decode())
        saveInfo(items,filename)
        with urlopen(ls_url) as url:
            ls = json.loads(url.read().decode())
        saveInfo(ls,ls_filename)
        with urlopen(es_url) as url:
            es = json.loads(url.read().decode())
        saveInfo(es,es_filename)
        print("Success loading datamine!")
    except HTTPError:
        print("Failure to load datamine...")
        units = {}


def update():
    try:
        print("Attempting Update...")
        with urlopen(datamine_url) as url:
            items1 = json.loads(url.read().decode())
        print("Unit info updated")
        print("Saving files...")
        saveInfo(items1, filename)
        items = items1
        print("Completed Update")
    except:
        print("Failed Update")


effectMap = {
    '0':"null",
    '1':"[[Parameter Boost|Attack Boost]]",
    '3':"[[Parameter Boost|Defense Boost]]",
    '5':"[[Parameter Boost|Recovery Boost]]",
    '7':"[[Parameter Boost|Critical Rate Boost]]",
    '8':"[[Gradual Healing]]",
    '9':"[[Drop Rate Boost|HC Drop Rate Boost]]",
    '10':"[[Drop Rate Boost|BC Drop Rate Boost]]",
    '11':"[[Drop Rate Boost|Item Drop Rate Boost]]",
    '12':"[[Guaranteed KO Resistance]]",
    '13':"[[Elemental Parameter Boost|Elemental Attack Boost]]",
    '14':"[[Elemental Parameter Boost|Elemental Defense Boost]]",
    '15':"[[Elemental Parameter Boost|Elemental Recovery Boost]]",
    '16':"[[Elemental Parameter Boost|Elemental Critical Rate Boost]]",
    '21':"[[Elemental Mitigation|Fire Mitigation]]",
    '22':"[[Elemental Mitigation|Water Mitigation]]",
    '23':"[[Elemental Mitigation|Earth Mitigation]]",
    '24':"[[Elemental Mitigation|Thunder Mitigation]]",
    '25':"[[Elemental Mitigation|Light Mitigation]]",
    '26':"[[Elemental Mitigation|Dark Mitigation]]",
    '30':"[[Status Negation|Poison Negation]]",
    '31':"[[Status Negation|Weak Negation]]",
    '32':"[[Status Negation|Sick Negation]]",
    '33':"[[Status Negation|Injury Negation]]",
    '34':"[[Status Negation|Curse Negation]]",
    '35':"[[Status Negation|Paralysis Negation]]",
    '36':"[[Damage Mitigation|Regular Mitigation]]",
    '46':"[[Parameter Conversion|Attack Conversion]]",
    '47':"[[Parameter Conversion|Defense Conversion]]",
    '48':"[[Parameter Conversion|Recovery Conversion]]",
    '60':"[[Leader Skill Lock]]",
    '71':"[[Additional Damage|Damage over Time]]",
    '95':"[[Barrier|Fire Barrier]]",
    '96':"[[Barrier|Water Barrier]]",
    '97':"[[Barrier|Earth Barrier]]",
    '98':"[[Barrier|Thunder Barrier]]",
    '99':"[[Barrier|Light Barrier]]",
    '100':"[[Barrier|Dark Barrier]]",
    '124':"[[Conditional Effect on Guard|Attack Boost on Guard]]",
    '125':"[[Conditional Effect on Guard|Defense Boost on Guard]]",
    '126':"[[Conditional Effect on Guard|Recovery Boost on Guard]]",
    '127':"[[Conditional Effect on Guard|Critical Rate Boost on Guard]]",
    '137':"[[Self Parameter Conversion|Self Attack Conversion]]",
    '138':"[[Self Parameter Conversion|Self Defense Conversion]]",
    '139':"[[Self Parameter Conversion|Self Recovery Conversion]]",
    '147':"[[Extra Skill Lock]]",
    '157':"[[Critical & Elemental Damage Vulnerability|Critical Vulnerability]]",
    '158':"[[Critical & Elemental Damage Vulnerability|Elemental Vulnerability]]",
    '10005':"[[Turn Skip]]",
    '10511':"[[Doom]]"
}


def targetType(r):
    if r['target type'] == 'enemy':
        if r['target area'] == 'aoe':
            return "To all enemies"
        else:
            return "To a single foe"
    elif r['target type'] == 'party':
        if r['target area'] == 'aoe':
            return "For all allies"
        else:
            return "For a single ally"
    elif r['target type'] == '100':
        return "To all enemies (PvP modes only)"
    else:
        return "For self"


def header(r, s):
    addSpace = 12 - len(str(r) + "_" + str(s))
    spaceStr = ""
    for a in range(0, addSpace):
        spaceStr = spaceStr + " "
    return str(r) + "_" + str(s) + str(spaceStr)


# HELPER FUNCTIONS
def parameterBoost(r):
    tempArr = []
    # print(r)
    if 'hp% buff' in r:
        tempArr.append(str(r['hp% buff']) + "% boost to HP")
    if 'atk% buff' in r:
        tempArr.append(str(r['atk% buff']) + "% boost to Atk")
    if 'def% buff' in r:
        tempArr.append(str(r['def% buff']) + "% boost to Def")
    if 'rec% buff' in r:
        tempArr.append(str(r['rec% buff']) + "% boost to Rec")
    if 'crit% buff' in r:
        tempArr.append(str(r['crit% buff']) + "% boost to critical rate")
    bigStr = ""
    # print(tempArr)
    if len(tempArr) > 2:
        for s in range(0, len(tempArr)):
            if s == len(tempArr) - 1:
                bigStr = bigStr + tempArr[s]
            elif s != len(tempArr) - 2:
                bigStr = bigStr + tempArr[s] + ", "
            elif s == len(tempArr) - 2:
                bigStr = bigStr + tempArr[s] + " and "
            else:
                bigStr = bigStr + tempArr[s]
    elif len(tempArr) == 2:
        bigStr = tempArr[0] + " and " + tempArr[1]
    else:
        bigStr = tempArr[0]
    return bigStr


def conversions(r, mode):
    if mode == 1:
        tempArr = []
        # print(r)
        if 'hp% buff' in r:
            tempArr.append("HP")
        if 'atk% buff' in r:
            tempArr.append("Atk")
        if 'def% buff' in r:
            tempArr.append("Def")
        if 'rec% buff' in r:
            tempArr.append("Rec")
        bigStr = ""
        # print(tempArr)
        if len(tempArr) > 2:
            for s in range(0, len(tempArr)):
                if s == len(tempArr) - 1:
                    bigStr = bigStr + tempArr[s]
                elif s != len(tempArr) - 2:
                    bigStr = bigStr + tempArr[s] + ", "
                elif s == len(tempArr) - 2:
                    bigStr = bigStr + tempArr[s] + " and "
                else:
                    bigStr = bigStr + tempArr[s]
        elif len(tempArr) == 2:
            bigStr = tempArr[0] + " and " + tempArr[1]
        else:
            bigStr = tempArr[0]
        return bigStr
    else:
        for s in ['atk% buff', 'def% buff', 'rec% buff']:
            if s in r:
                return str(r[s])


def multiStr(tempArr):
    bigStr = ""
    if len(tempArr) > 2:
        for s in range(0, len(tempArr)):
            if s == len(tempArr) - 1:
                bigStr = bigStr + tempArr[s]
            elif s != len(tempArr) - 2:
                bigStr = bigStr + tempArr[s] + ", "
            elif s == len(tempArr) - 2:
                bigStr = bigStr + tempArr[s] + " and "
            else:
                bigStr = bigStr + tempArr[s]
    elif len(tempArr) == 2:
        bigStr = tempArr[0] + " and " + tempArr[1]
    else:
        bigStr = tempArr[0]
    return bigStr


def negateAll(r):
    for s in ['curse','injury','paralysis','poison','sick','weaken']:
        if s+" resist%" not in r:
            return False
    return True


def mitigateAll(r):
    if r['passive id'] == '5':
        for s in ['fire','water','earth','thunder','light','dark']:
            if s+" resist%" not in r:
                return False
    elif r['passive id'] == '62':
        for s in ['fire','water','earth','thunder','light','dark']:
            if 'mitigate '+s+' attacks' not in r:
                return False
    return True

def buffMap(r):
    if 'buff turns (1)' in r:
        if r['buff turns (1)'] == "0":
            return "Boosts Atk by " + str(r['atk% buff (1)']) + "% for 1 turn"
        else:
            return "Boosts Atk by " + str(r['atk% buff (1)']) + "% for " + str(
                int(r['buff turns (1)']) + 1) + " turns"
    elif 'buff turns (3)' in r:
        if r['buff turns (3)'] == "0":
            return "Boosts Def by " + str(r['def% buff (3)']) + "% for 1 turn"
        else:
            return "Boosts Def by " + str(r['def% buff (3)']) + "% for " + str(
                int(r['buff turns (3)']) + 1) + " turns"
    elif 'buff turns (5)' in r:
        if r['buff turns (5)'] == "0":
            return "Boosts Rec by " + str(r['rec% buff (5)']) + "% for 1 turn"
        else:
            return "Boosts Rec by " + str(r['rec% buff (5)']) + "% for " + str(
                int(r['buff turns (5)']) + 1) + " turns"
    elif 'buff turns (7)' in r:
        if r['buff turns (7)'] == "0":
            return "Boosts critical rate by " + str(r['unknown buff params']) + "% for 1 turn"
        else:
            return "Boosts critical rate by " + str(r['unknown buff params']) + "% for " + str(
                int(r['buff turns (7)']) + 1) + " turns"
    elif 'buff turns (8)' in r:
        if r['buff turns (8)'] == "1":
            return "Heals " + str(r['gradual heal low']) + "~" + str(r['gradual heal high']) + " HP each turn for 1 turn"
        else:
            return "Heals " + str(r['gradual heal low']) + "~" + str(r['gradual heal high']) + " HP each turn for " + str(r['buff turns (8)'] + " turns")
    elif 'buff turns (12)' in r:
        return "Becomes able to resist 1 KO"
    elif 'buff turns (21)' in r:
        if r['buff turns (21)'] == "1":
            return "Reduces Fire damage by " + str(r['unknown buff params']) + "% for 1 turn"
        else:
            return "Reduces Fire damage by " + str(r['unknown buff params']) + "% for " + str(r['buff turns (21)'] + " turns")
    elif 'buff turns (22)' in r:
        if r['buff turns (22)'] == "1":
            return "Reduces Water damage by " + str(r['unknown buff params']) + "% for 1 turn"
        else:
            return "Reduces Water damage by " + str(r['unknown buff params']) + "% for " + str(r['buff turns (22)'] + " turns")
    elif 'buff turns (23)' in r:
        if r['buff turns (23)'] == "1":
            return "Reduces Earth damage by " + str(r['unknown buff params']) + "% for 1 turn"
        else:
            return "Reduces Earth damage by " + str(r['unknown buff params']) + "% for " + str(r['buff turns (23)'] + " turns")
    elif 'buff turns (24)' in r:
        if r['buff turns (24)'] == "1":
            return "Reduces Thunder damage by " + str(r['unknown buff params']) + "% for 1 turn"
        else:
            return "Reduces Thunder damage by " + str(r['unknown buff params']) + "% for " + str(r['buff turns (24)'] + " turns")
    elif 'buff turns (25)' in r:
        if r['buff turns (25)'] == "1":
            return "Reduces Light damage by " + str(r['unknown buff params']) + "% for 1 turn"
        else:
            return "Reduces Light damage by " + str(r['unknown buff params']) + "% for " + str(r['buff turns (25)'] + " turns")
    elif 'buff turns (26)' in r:
        if r['buff turns (26)'] == "1":
            return "Reduces Dark damage by " + str(r['unknown buff params']) + "% for 1 turn"
        else:
            return "Reduces Dark damage by " + str(r['unknown buff params']) + "% for " + str(r['buff turns (26)'] + " turns")
    elif 'buff turns (36)' in r:
        if r['buff turns (36)'] == "0":
            return "Reduces damage taken by " + str(r['dmg reduction% buff']) + "% for 1 turn"
        else:
            return "Reduces damage taken by " + str(r['dmg reduction% buff']) + "% for " + str(
                int(r['buff turns (36)']) + 1) + " turns"
    elif 'buff turns (37)' in r:
        if r['buff turns (37)'] == "1":
            return "Boosts BB gauge by " + str(r['increase bb gauge gradual buff']) + " BC each turn for 1 turn"
        else:
            return "Boosts BB gauge by " + str(r['increase bb gauge gradual buff']) + " BC each turn for " + str(r['buff turns (37)']) + " turns"
    elif 'buff turns (40)' in r:
        if r['buff turns (40)'] == "1":
            return "Boosts spark damage by " + str(r['spark dmg% buff']) + "% for 1 turn"
        else:
            return "Boosts spark damage by " + str(r['spark dmg% buff']) + "% for " + str(r['buff turns (40)']) + " turns"
    elif 'buff turns (51)' in r:
        if r['buff turns (51)'] == "1":
            return "Adds Fire element to attacks for 1 turn"
        else:
            return "Adds Fire element to attacks for " + str(r['buff turns (51)']) + " turns"
    elif 'buff turns (52)' in r:
        if r['buff turns (52)'] == "1":
            return "Adds Water element to attacks for 1 turn"
        else:
            return "Adds Water element to attacks for " + str(r['buff turns (52)']) + " turns"
    elif 'buff turns (53)' in r:
        if r['buff turns (53)'] == "1":
            return "Adds Earth element to attacks for 1 turn"
        else:
            return "Adds Earth element to attacks for " + str(r['buff turns (53)']) + " turns"
    elif 'buff turns (54)' in r:
        if r['buff turns (54)'] == "1":
            return "Adds Thunder element to attacks for 1 turn"
        else:
            return "Adds Thunder element to attacks for " + str(r['buff turns (54)']) + " turns"
    elif 'buff turns (55)' in r:
        if r['buff turns (55)'] == "1":
            return "Adds Light element to attacks for 1 turn"
        else:
            return "Adds Light element to attacks for " + str(r['buff turns (56)']) + " turns"
    elif 'buff turns (56)' in r:
        if r['buff turns (56)'] == "1":
            return "Adds Dark element to attacks for 1 turn"
        else:
            return "Adds Dark element to attacks for " + str(r['buff turns (56)']) + " turns"
    elif 'buff turns (72)' in r:
        if r['buff turns (72)'] == "1":
            return "Boosts BB Atk by " + str(r['sbb atk% buff']) + " for 1 turn"
        else:
            return "Boosts BB Atk by " + str(r['sbb atk% buff']) + " for " + str(r['buff turns (72)']) + " turns"
    elif 'buff turns (74)' in r:
        params = r['unknown buff params'].split('&')
        if r['buff turns (74)'] == "1":
            return params[1] + "% chance of inflicting " + str(params[2]) + " turn " + str(
                int(params[0]) * -1) + " Atk reduction for 1 turn"
        else:
            return params[1] + "% chance of inflicting " + str(params[2]) + " turn " + str(int(params[0]) * -1) + "% Atk reduction for " + str(r['buff turns (74)']) + " turns"
    elif 'buff turns (84)' in r:
        params = int(float(r['unknown buff params'])*100)
        if r['buff turns (84)'] == "1":
            return "Boosts critical damage by " + str(params) + "% for 1 turn"
        else:
            return "Boosts critical damage by " + str(params) + "% for " + str(r['buff turns (84)']) + " turns"
    elif 'buff turns (91)' in r:
        params = r['unknown buff params'].split('&')
        return params[1] + "% chance of resisting 1 KO"
    elif 'buff turns (95)' in r:
        params = r['unknown buff params'].split('&')
        return "Activates Fire barrier with " + params[1] + " HP"
    elif 'buff turns (96)' in r:
        params = r['unknown buff params'].split('&')
        return "Activates Water barrier with " + params[1] + " HP"
    elif 'buff turns (97)' in r:
        params = r['unknown buff params'].split('&')
        return "Activates Earth barrier with " + params[1] + " HP"
    elif 'buff turns (98)' in r:
        params = r['unknown buff params'].split('&')
        return "Activates Thunder barrier with " + params[1] + " HP"
    elif 'buff turns (99)' in r:
        params = r['unknown buff params'].split('&')
        return "Activates Light barrier with " + params[1] + " HP"
    elif 'buff turns (100)' in r:
        params = r['unknown buff params'].split('&')
        return "Activates Dark barrier with " + params[1] + " HP"
    elif 'buff turns (132)' in r:
        params = r['unknown buff params'].split("&")
        if r['buff turns (132)'] == "0":
            return "Boosts OD fill rate by " + params[0] + "~" + params[1] + "% for 1 turn"
        else:
            return "Boosts OD fill rate by " + params[0] + "~" + params[1] + "% for " + str(int(r['buff turns (132)'] + 1)) + " turns"
    elif 'buff turns (133)' in r:
        params = r['unknown buff params'].split("&")
        if params[2] == "100":
            if r['buff turns (133)'] == "0":
                return "Heals " + params[0] + "~" + params[1] + " of damage taken as HP for 1 turn"
            else:
                return "Heals " + params[0] + "~" + params[1] + " of damage taken as HP for " + str(int(r['buff turns (133)'] + 1)) + " turns"
        else:
            if r['buff turns (133)'] == "0":
                return params[2] + "% chance of healing " + params[0] + "~" + params[1] + " of damage taken as HP for 1 turn"
            else:
                return params[2] + "% chance of healing " + params[0] + "~" + params[1] + " of damage taken as HP for " + str(int(r['buff turns (133)'] + 1)) + " turns"
    elif 'buff turns (143)' in r:
        if r['buff turns (143)'] == "0":
            return "Negates critical damage for 1 turn"
        else:
            return "Negates critical damage for " + str(int(r['buff turns (143)']) + 1) + " turns"
    elif 'buff turns (145)' in r:
        if r['buff turns (145)'] == "0":
            return "Negates elemental damage for 1 turn"
        else:
            return "Negates elemental damage for " + str(int(r['buff turns (145)']) + 1) + " turns"
    elif 'buff turns (153)' in r:
        params = r['unknown buff params'].split("&")
        if r['buff turns (153)'] == "0":
            return "Damage taken has a " + params[1] + "% chance of inflicting " + params[2] + " turn " + str(int(params[0]) * -1) + "% Atk reduction for 1 turn"
        else:
            return "Damage taken has a " + params[1] + "% chance of inflicting " + params[2] + " turn " + str(int(params[0]) * -1) + "% Atk reduction for " + str(int(r['buff turns (153)'] + 1)) + "turns"
    elif 'buff turns (10001)' in r:
        params = r['unknown buff params'].split("&")
        tempArr = []
        typeArr = ['Atk','Def','Rec','critical rate']
        count = 0
        for s in params:
            if s != "0":
                tempArr.append(typeArr[count] + " by " + s + "%")
            count = count + 1
        if r['buff turns (10001)'] == "1":
            return "Activates Stealth, also boosts " + multiStr(tempArr) + " for 1 turn"
        else:
            return "Activates Stealth, also boosts " + multiStr(tempArr) + " for " + str(int(r['buff turns (10001)'])) + " turns"


def unknownMap(r):
    params = r['unknown passive params'].split(',')
    if params[0] == '12':
        return params[1] + "% chance of resisting 1 KO, restores "+params[3] + "% of unit's HP"
    elif params[0] == '95':
        barrier = params[1].split('&')
        return "Activates Fire barrier with " + barrier[1] + " HP"
    elif params[0] == '96':
        barrier = params[1].split('&')
        return "Activates Water barrier with " + barrier[1] + " HP"
    elif params[0] == '97':
        barrier = params[1].split('&')
        return "Activates Earth barrier with " + barrier[1] + " HP"
    elif params[0] == '98':
        barrier = params[1].split('&')
        return "Activates Thunder barrier with " + barrier[1] + " HP"
    elif params[0] == '99':
        barrier = params[1].split('&')
        return "Activates Light barrier with " + barrier[1] + " HP"
    elif params[0] == '100':
        barrier = params[1].split('&')
        return "Activates Dark barrier with " + barrier[1] + " HP"
    elif params[0] == '124':
        return "Boosts Atk by " + params[1] + "%"


def leaderMap(r):
    params = r['unknown passive params'].split(',')
    if params[0] == '1':
        stats = params[1].replace('\n','').split('$')
        tempArr = []
        if stats[0] == stats[1] == stats[2] == stats[4]:
            return stats[0] + "% boost to all parameters"
        if stats[0] != '0':
            tempArr.append(stats[0] + "% boost to Atk")
        if stats[1] != '0':
            tempArr.append(stats[1] + "% boost to Def")
        if stats[2] != '0':
            tempArr.append(stats[2] + "% boost to Rec")
        if stats[4] != '0':
            tempArr.append(stats[4] + "% boost to HP")
        if stats[3] != '0':
            tempArr.append(stats[3] + "% boost to critical rate")
        return multiStr(tempArr)
    elif params[0] == '8':
        return params[1] + "% damage reduction"
    elif params[0] == '31':
        return params[1].split('$')[0] + "% boost to spark damage"
    elif params[0] == '34':
        return params[1] + "% boost to critical damage"
    elif params[0] == '41':
        stats = params[1].replace('\n', '').split('$')
        tempArr = []
        if stats[1] == stats[2] == stats[3] == stats[5]:
            return stats[1] + "% boost to all parameters"
        if stats[1] != '0':
            tempArr.append(stats[1] + "% boost to Atk")
        if stats[2] != '0':
            tempArr.append(stats[2] + "% boost to Def")
        if stats[3] != '0':
            tempArr.append(stats[3] + "% boost to Rec")
        if stats[5] != '0':
            tempArr.append(stats[5] + "% boost to HP")
        if stats[4] != '0':
            tempArr.append(stats[4] + "% boost to critical rate")
        return multiStr(tempArr) + " when "+stats[0]+" or more elements are present"
    elif params[0] == '50':
        elements = params[1].split('$')
        tempArr = []
        if '1' in elements[0:6]:
            tempArr.append("Fire")
        if '2' in elements[0:6]:
            tempArr.append("Water")
        if '3' in elements[0:6]:
            tempArr.append("Earth")
        if '4' in elements[0:6]:
            tempArr.append("Thunder")
        if '5' in elements[0:6]:
            tempArr.append("Light")
        if '6' in elements[0:6]:
            tempArr.append("Dark")
        if len(tempArr) == 6:
            return str(int(float(elements[6])*100)) + "% boost to all elemental damage"
        else:
            return str(int(float(elements[6])*100)) + "% boost to "+multiStr(tempArr)+" elemental damage"
    elif params[0] == '53':
        if params[1].split('$')[0] == '100':
            return "Negates critical damage"
        else:
            return params[1].split('$')[0] + "% resistance to critical damage"
    elif params[0] == '127':
        return params[1].split('$')[1] + "% DoT damage reduction"
    elif params[0] == '143':
        return "Raises Atk parameter limits to "+params[1]


def addBuff(tempStr, r, s, extraArg):
    if s == '11':
        tempStr = tempStr + "*" + searchBuffs(s, r['triggered effect'], extraArg) + " (" + searchBuffs(s, r[
            'triggered effect'], "target") + ", lasts " + searchBuffs(s, r['triggered effect'], extraArg+"turns") + ")\n"
        return tempStr
    if searchBuffs(s, r['triggered effect'], "target") == "—":
        tempStr = tempStr + "*" + searchBuffs(s, r['triggered effect'], extraArg) + "\n"
        return tempStr
    if searchBuffs(s, r['triggered effect'], "turns") == "—":
        tempStr = tempStr + "*" + searchBuffs(s, r['triggered effect'], extraArg) + " (" + searchBuffs(s, r['triggered effect'], "target") + ")\n"
    else:
        tempStr = tempStr + "*" + searchBuffs(s, r['triggered effect'], extraArg) + " (" + searchBuffs(s, r['triggered effect'],"target") + ", lasts " + searchBuffs(s, r['triggered effect'], "turns") + ")\n"
    return tempStr


# MAIN SEARCH FUNCTION
def searchPassives(dataID, type, procID, extraArg):
    arrCount = -1
    areaSearch = []
    if type == 'item':
        areaSearch = items[str(dataID)]['effect']
    elif type == 'ls':
        areaSearch = ls[str(dataID)]['effects']
    elif type == 'es':
        areaSearch = es[str(dataID)]['effects']
    for r in areaSearch:
        arrCount = arrCount + 1
        if globalArr[arrCount] != 1:
            if 'passive id' in r:
                if str(procID) == r['passive id'] == '1':
                    # PARAMETERS
                    if 'atk% buff' in r and 'def% buff' in r and 'rec% buff' in r and 'hp% buff' in r:
                        if r['atk% buff'] == r['def% buff'] == r['rec% buff'] == r['hp% buff']:
                            return str(r['atk% buff']) + "% boost to all parameters"
                    return parameterBoost(r)
                elif str(procID) == r['passive id'] == '2':
                    # ELEMENT PARAMETERS
                    elemArr = []
                    for s in r['elements buffed']:
                        elemArr.append(s.capitalize())
                    #print(elemArr)
                    if 'atk% buff' in r and 'def% buff' in r and 'rec% buff' in r and 'hp% buff' in r:
                        if r['atk% buff'] == r['def% buff'] == r['rec% buff'] == r['hp% buff']:
                            return str(r['atk% buff']) + "% boost to all parameters of " + multiStr(elemArr) + " units"
                    return parameterBoost(r) + " of " + multiStr(elemArr) + " units"
                elif str(procID) == r['passive id'] == '3':
                    # TYPE PARAMETERS
                    if 'atk% buff' in r and 'def% buff' in r and 'rec% buff' in r and 'hp% buff' in r:
                        if r['atk% buff'] == r['def% buff'] == r['rec% buff'] == r['hp% buff']:
                            return str(r['atk% buff']) + "% boost to all parameters of " + r['unit type buffed'].capitalize() + " units"
                    return parameterBoost(r) + " of " + r['unit type buffed'].capitalize() + " units"
                elif str(procID) == r['passive id'] == '4':
                    # STATUS NEGATION
                    if negateAll(r):
                        if r['curse resist%'] == 100:
                            return "Negates all status ailments"
                        else:
                            return "Boosts all status resistance by " + str(r['curse resist%']) + "%"
                    else:
                        tempArr = []
                        for s in ['curse','injury','paralysis','poison','sick','weaken']:
                            if s+' resist%' in r:
                                tempArr.append(s.capitalize())
                        if r[tempArr[0].lower() + ' resist%'] == 100:
                            return "Negates " + str(multiStr(tempArr)) + " effects"
                        else:
                            return "Boosts resistance to " + multiStr(tempArr) + " by " + str(r[tempArr[0].lower() + ' resist%']) + "%"
                elif str(procID) == r['passive id'] == '5':
                    # ELEMENTAL MITIGATION
                    if mitigateAll(r):
                        return "Reduces all elemental damage taken by " + str(r['fire resist%']) + "%"
                    else:
                        tempArr = []
                        for s in ['fire','water','earth','thunder','light','dark']:
                            if s+' resist%' in r:
                                tempArr.append(s.capitalize())
                        return "Reduces " + multiStr(tempArr) + " damage taken by " + str(r[tempArr[0].lower() + " resist%"]) + "%"
                elif str(procID) == r['passive id'] == '8':
                    # NORMAL MITIGATION
                    return "Reduces damage taken by " + str(r['dmg% mitigation']) + "%"
                elif str(procID) == r['passive id'] == '9':
                    # BC FILL PER TURN
                    return "Boosts BB gauge by " + str(r['bc fill per turn']) + " BC"
                elif str(procID) == r['passive id'] == '10':
                    # BC EFFICACY
                    return str(r['hc effectiveness%']) + "% boost to HC Efficacy"
                elif str(procID) == r['passive id'] == '11':
                    # HP CONDITIONAL STAT BOOST
                    if 'atk% buff' in r and 'def% buff' in r and 'rec% buff' in r:
                        if r['atk% buff'] == r['def% buff'] == r['rec% buff']:
                            return str(r['atk% buff']) + "% boost to Atk, Def, and Rec when HP is above " + str(r['hp above % buff requirement']) + "%"
                    if 'hp below % buff requirement' in r:
                        return parameterBoost(r) + " when HP is below " + str(r['hp below % buff requirement']) + "%"
                    else:
                        if r['hp above % buff requirement'] == 100:
                            return parameterBoost(r) + " when HP is full"
                        else:
                            return parameterBoost(r) + " when HP is above " + str(r['hp above % buff requirement']) + "%"
                elif str(procID) == r['passive id'] == '12':
                    # HP CONDITIONAL DROP RATE
                    tempArr = []
                    for s in ['BC','HC','Item','Zel','Karma']:
                        if s.lower()+' drop rate% buff' in r:
                            tempArr.append(s + " drop rate by " + str(r[s.lower()+' drop rate% buff']) + "%")
                    if 'hp below % buff requirement' in r:
                        return "Boosts " + multiStr(tempArr) + " when HP is below " + str(r['hp below % buff requirement']) + "%"
                    else:
                        if r['hp above % buff requirement'] == 100:
                            return "Boosts " + multiStr(tempArr) + " when HP is full"
                        else:
                            return "Boosts " + multiStr(tempArr) + " when HP is above " + str(r['hp above % buff requirement']) + "%"
                elif str(procID) == r['passive id'] == '13':
                    # BC FILL UPON ENEMY DEFEAT
                    if r['bc fill on enemy defeat%'] == 100:
                        if r['bc fill on enemy defeat low'] == r['bc fill on enemy defeat high']:
                            return "Boosts BB gauge by " + str(r['bc fill on enemy defeat high']) + " BC after defeating an enemy"
                        else:
                            return "Boosts BB gauge by " + str(r['bc fill on enemy defeat low']) + "~" + str(r['bc fill on enemy defeat high']) + " BC after defeating an enemy"
                    else:
                        if r['bc fill on enemy defeat low'] == r['bc fill on enemy defeat high']:
                            return str(r['bc fill on enemy defeat%']) + "% chance of boosting BB gauge by " + str(r['bc fill on enemy defeat high']) + " BC after defeating an enemy"
                        else:
                            return str(r['bc fill on enemy defeat%']) + "% chance of boosting BB gauge by " + str(r['bc fill on enemy defeat low']) + "~" + str(r['bc fill on enemy defeat high']) + " BC after defeating an enemy"
                elif str(procID) == r['passive id'] == '14':
                    # CHANCE MITIGATION
                    return str(r['dmg reduction chance%']) + "% chance of reducing damage taken by " + str(r['dmg reduction%']) + "%"
                elif str(procID) == r['passive id'] == '15':
                    # HEAL ON ENEMY DEFEAT
                    if r['hp% recover on enemy defeat low'] == r['hp% recover on enemy defeat high']:
                        return "Heals " + str(r['hp% recover on enemy defeat low']) + "~" + str(
                            r['hp% recover on enemy defeat high']) + "% HP after winning a battle"
                    else:
                        return "Heals " + str(r['hp% recover on enemy defeat high']) + "% HP after defeating an enemy"
                elif str(procID) == r['passive id'] == '16':
                    # HEAL ON BATTLE WON
                    if r['hp% recover on battle win low'] == r['hp% recover on battle win high']:
                        return "Heals " + str(r['hp% recover on battle win low']) + "~" + str(
                            r['hp% recover on battle win high']) + "% HP after winning a battle"
                    else:
                        return "Heals " + str(r['hp% recover on battle win high']) + "% HP after winning a battle"
                elif str(procID) == r['passive id'] == '17':
                    # HP ABSORPTION
                    if r['hp drain chance%'] == 100:
                        if r['hp drain% low'] == r['hp drain% high']:
                            return "Drains " + str(r['hp drain% high']) + "% of damage dealt as HP"
                        else:
                            return "Drains " + str(r['hp drain% low']) + "~" + str(r['hp drain% high']) + "% of damage dealt as HP"
                    else:
                        if r['hp drain% low'] == r['hp drain% high']:
                            return str(r['hp drain chance%']) + "% chance of draining " + str(r['hp drain% low']) + "% of damage dealt as HP"
                        else:
                            return str(r['hp drain chance%']) + "% chance of draining " + str(r['hp drain% low']) + "~" + str(r['hp drain% high']) + "% of damage dealt as HP"
                elif str(procID) == r['passive id'] == '19':
                    # DROP RATE
                    tempArr = []
                    for s in ['BC','HC','Item','Zel','Karma']:
                        if s.lower()+' drop rate% buff' in r:
                            tempArr.append(s + " drop rate by " + str(r[s.lower()+' drop rate% buff']) + "%")
                    return "Boosts " + multiStr(tempArr)
                elif str(procID) == r['passive id'] == '20':
                    # STATUS INFLICTION
                    check = False
                    global statusArr
                    #print(len(statusArr) != 0)
                    if len(statusArr) != 0:
                        check = True
                    for s in ['curse', 'injury', 'paralysis', 'poison', 'sick', 'weaken']:
                        if s+"%" in r:
                            statusArr.append(s+","+str(r[s+"%"]))
                    #print(statusArr)
                    if check:
                        distinct = []
                        for s in statusArr:
                            if s.split(',')[1] not in distinct:
                                distinct.append(s.split(',')[1])
                                #print(distinct)
                        bigStr = ""
                        tempArr = []
                        for s in distinct:
                            tempArr = []
                            tempCount = 0
                            for t in statusArr:
                                if t.split(',')[1] == s and t.split(',')[0].capitalize() not in tempArr:
                                    tempArr.append(t.split(',')[0].capitalize())
                            if tempCount == 0 and len(distinct) != 1:
                                bigStr = bigStr + s + "% chance of inflicting " + multiStr(tempArr) + "<br>"
                                tempCount = 1
                            else:
                                bigStr = bigStr + s + "% chance of inflicting " + multiStr(tempArr)
                        #print(bigStr)
                        statusCheck = True
                        return bigStr
                    else:
                        return "Move on"
                elif str(procID) == r['passive id'] == '21':
                    # PARAMETER FIRST X TURNS
                    tempArr = []
                    for s in ['first x turns atk% (1)','first x turns def% (3)','first x turns rec% (5)','first x turns crit% (7)']:
                        if s == 'first x turns atk% (1)' and s in r:
                            tempArr.append("Atk by " + str(r['first x turns atk% (1)']) + "%")
                        elif s == 'first x turns def% (3)' and s in r:
                            tempArr.append("Def by " + str(r['first x turns def% (3)']) + "%")
                        elif s == 'first x turns rec% (5)' and s in r:
                            tempArr.append("Rec by " + str(r['first x turns rec% (5)']) + "%")
                        elif s == 'first x turns crit% (7)' and s in r:
                            tempArr.append("critical rate by " + str(r['first x turns crit% (7)']) + "%")
                    return "Boosts " + multiStr(tempArr) + " for the first " + str(r['first x turns']) + " turns"
                elif str(procID) == r['passive id'] == '23':
                    # HEAL ON BATTLE WON
                    if r['battle end bc fill low'] == r['battle end bc fill high']:
                        return "Boosts BB gauge by " + str(r['battle end bc fill low']) + "~" + str(
                            r['battle end bc fill high']) + " BC after winning a battle"
                    else:
                        return "Boosts BB gauge by " + str(r['battle end bc fill high']) + " BC after winning a battle"
                elif str(procID) == r['passive id'] == '24':
                    # HEAL ON HIT
                    if r['dmg% to hp% when attacked low'] != r['dmg% to hp% when attacked high']:
                        if r['dmg% to hp% when attacked chance%'] == 100:
                            return "Heals " + str(r['dmg% to hp% when attacked low']) + "~" + str(
                                r['dmg% to hp% when attacked high']) + "% of damage taken as HP"
                        else:
                            return str(r['dmg% to hp% when attacked chance%']) + "% chance of healing " + str(r['dmg% to hp% when attacked low']) + "~" + str(
                                r['dmg% to hp% when attacked high']) + "% of damage taken as HP"
                    else:
                        if r['dmg% to hp% when attacked chance%'] == 100:
                            return "Heals " + str(r['dmg% to hp% when attacked high']) + "% of damage taken as HP"
                        else:
                            return str(r['dmg% to hp% when attacked chance%']) + "% chance of healing " + str(r['dmg% to hp% when attacked low']) +"~" + str(r['dmg% to hp% when attacked high']) + "% of damage taken as HP"
                elif str(procID) == r['passive id'] == '25':
                    # BC FILL ON HIT
                    if r['bc fill when attacked low'] != r['bc fill when attacked high']:
                        if r['bc fill when attacked%'] == 100:
                            return "Damage taken boosts BB gauge by " + str(r['bc fill when attacked low']) + "~" + str(
                                r['bc fill when attacked high']) + " BC"
                        else:
                            return "Damage taken has a " + str(r['bc fill when attacked%']) + "% chance of boosting BB gauge by " + str(r['bc fill when attacked low']) + "~" + str(
                                r['bc fill when attacked high']) + " BC"
                    else:
                        if r['bc fill when attacked%'] == 100:
                            return "Damage taken boosts BB gauge by " + str(r['bc fill when attacked high']) + " BC"
                        else:
                            return "Damage taken has a " + str(r['bc fill when attacked%']) + "% chance of boosting BB gauge by " + str(r['bc fill when attacked high']) + " BC"
                elif str(procID) == r['passive id'] == '26':
                    # DAMAGE REFLECT
                    if r['dmg% reflect low'] != r['dmg% reflect high']:
                        if r['dmg% to hp% when attacked%'] == 100:
                            return "Reflects " + str(r['dmg% reflect low']) + "~" + str(
                                r['dmg% reflect high']) + "% of damage taken as damage to enemies"
                        else:
                            return str(r['dmg% reflect chance%']) + "% chance of reflecting " + str(r['dmg% reflect low']) + "~" + str(
                                r['dmg% reflect high']) + "% of damage taken as damage to enemies"
                    else:
                        if r['dmg% reflect chance%'] == 100:
                            return "Reflects " + str(r['dmg% reflect high']) + "% of damage taken as damage to enemies"
                        else:
                            return str(r['dmg% reflect chance%']) + "% chance of reflecting " + str(r['dmg% reflect high']) + "% of damage taken as damage to enemies"
                elif str(procID) == r['passive id'] == '27':
                    # TARGET CHANCE
                    if r['target% chance'] < 0:
                        return "Decreases chance of being targeted by " + str(r['target% chance'] * -1) + "%"
                    else:
                        return "Increases chance of being targeted by " + str(r['target% chance']) + "%"
                elif str(procID) == r['passive id'] == '28':
                    # TARGET CHANCE BELOW HP CONDITIONAL
                    if r['target% chance'] < 0:
                        return "Decreases chance of being targeted by " + str(r['target% chance'] * -1) + "% when HP is below " + str(r['hp below % passive requirement']) + "%"
                    else:
                        return "Increases chance of being targeted by " + str(r['target% chance']) + "% when HP is below " + str(r['hp below % passive requirement']) + "%"
                elif str(procID) == r['passive id'] == '29':
                    # IGNORE DEF
                    return str(r['ignore def%']) + "% chance of ignoring enemy's Def"
                elif str(procID) == r['passive id'] == '30':
                    # BB CONDITIONAL STAT BOOST
                    if 'atk% buff' in r and 'def% buff' in r and 'rec% buff' in r:
                        if r['atk% buff'] == r['def% buff'] == r['rec% buff']:
                            if 'bb gauge above % buff requirement' in r:
                                if r['bb gauge above % buff requirement'] == 100:
                                    return str(r['atk% buff']) + "% boost to Atk, Def, and Rec when HP is full"
                                else:
                                    return str(r['atk% buff']) + "% boost to Atk, Def, and Rec when HP is above " + str(r['bb gauge above % buff requirement']) + "%"
                            elif 'bb gauge below % buff requirement' in r:
                                if r['bb gauge below % buff requirement'] == 100:
                                    return str(r['atk% buff']) + "% boost to Atk, Def, and Rec when HP is full"
                                else:
                                    return str(r['atk% buff']) + "% boost to Atk, Def, and Rec when HP is above " + str(r['bb gauge below % buff requirement']) + "%"
                    if 'bb gauge below % buff requirement' in r:
                        return parameterBoost(r) + " when HP is below " + str(r['bb gauge below % buff requirement']) + "%"
                    else:
                        if r['bb gauge above % buff requirement'] == 100:
                            return parameterBoost(r) + " when HP is full"
                        else:
                            return parameterBoost(r) + " when HP is above " + str(r['bb gauge above % buff requirement']) + "%"
                elif str(procID) == r['passive id'] == '31':
                    # SPARK DAMAGE
                    tempArr = []
                    if 'bc drop% for spark' in r:
                        tempArr.append("spark BC drop rate by "+str(r['bc drop% for spark'])+"%")
                    if 'hc drop% for spark' in r:
                        tempArr.append("spark HC drop rate by "+str(r['hc drop% for spark'])+"%")
                    if 'damage% for spark' in r:
                        tempArr.append("spark damage by "+str(r['damage% for spark'])+"%")
                    if len(tempArr) != 1:
                        return "Boosts " + multiStr(tempArr)
                    else:
                        if 'bc drop% for spark' in r:
                            return str(r['bc drop% for spark'])+"% boost to spark BC drop rate"
                        elif 'hc drop% for spark' in r:
                            return str(r['hc drop% for spark'])+"% boost to spark HC drop rate"
                        elif 'damage% for spark' in r:
                            return str(r['damage% for spark'])+"% boost to spark damage"
                elif str(procID) == r['passive id'] == '32':
                    # BC EFFICACY
                    return str(int(r['bb gauge fill rate%'])) + "% boost to BC Efficacy"
                elif str(procID) == r['passive id'] == '33':
                    # GRADUAL HEALING
                    if r['turn heal low'] == r['turn heal high']:
                        return "Heals " + str(r['turn heal high']) + " + " + str(int(r['rec% added (turn heal)'])) + "% Rec of HP each turn"
                    else:
                        return "Heals " + str(r['turn heal low']) + "~" + str(r['turn heal high']) + " + " + str(
                            int(r['rec% added (turn heal)'])) + "% Rec of HP each turn"
                elif str(procID) == r['passive id'] == '34':
                    # CRIT DAMAGE
                    return str(int(r['crit multiplier%'])) + "% boost to critical damage"
                elif str(procID) == r['passive id'] == '35':
                    # BC FILL ON ATTACK
                    if r['bc fill when attacking low'] != r['bc fill when attacking high']:
                        if r['bc fill when attacking%'] == 100:
                            return "Boosts BB gauge by " + str(r['bc fill when attacking low']) + "~" + str(
                                r['bc fill when attacking high']) + " BC when attacking"
                        else:
                            return str(r['bc fill when attacking%']) + "% chance of boosting BB gauge by " + str(r['bc fill when attacking low']) + "~" + str(
                                r['bc fill when attacking high']) + " BC when attacking"
                    else:
                        if r['bc fill when attacking%'] == 100:
                            return "Boosts BB gauge by " + str(r['bc fill when attacking high']) + " BC when attacking"
                        else:
                            return str(r['bc fill when attacking%']) + "% chance of boosting BB gauge by " + str(r['bc fill when attacking high']) + " BC when attacking"
                elif str(procID) == r['passive id'] == '36':
                    # EXTRA ACTION
                    if r['additional actions'] == 1:
                        return "50% chance of granting 1 additional action (600% total damage modifier for each action)"
                    else:
                        return "50% chance of granting " + str(r['additional actions']) + " additional actions (600% total damage modifier for each action)"
                elif str(procID) == r['passive id'] == '37':
                    # EXTRA HIT
                    if 'extra hits dmg%' in r:
                        return "+" + str(r['hit increase/hit']) + " to each normal hit (" + str(
                            int(r['extra hits dmg%'] + 100)) + "% extra hit damage modifier)"
                    else:
                        return "+" + str(r['hit increase/hit']) + " to each normal hit (100% extra hit " \
                                                                  "damage modifier)"
                elif str(procID) == r['passive id'] == '40':
                    # CONVERSION PARAMETERS
                    tempStr = ""
                    if r['converted attribute'] == 'attack':
                        tempStr = "Atk"
                    elif r['converted attribute'] == 'defense':
                        tempStr = "Def"
                    elif r['converted attribute'] == 'recovery':
                        tempStr = "Rec"
                    elif r['converted attribute'] == 'hp':
                        tempStr = "HP"
                    return "Boosts " + conversions(r,1) + " relative to " + conversions(r,2) + "% of " + tempStr
                elif str(procID) == r['passive id'] == '41':
                    # UNIQUE ELEMENTS PARAMETER
                    return "Boosts " + parameterBoost(r) + " when " + str(r['unique elements required']) + " or more elements are present"
                elif str(procID) == r['passive id'] == '42':
                    # GENDER PARAMETER BOOST
                    if 'atk% buff' in r and 'def% buff' in r and 'rec% buff' in r and 'hp% buff' in r:
                        if r['atk% buff'] == r['def% buff'] == r['rec% buff'] == r['hp% buff']:
                            return str(r['atk% buff']) + "% boost to all parameters of " + str(r['gender required']).capitalize() + " units"
                    return "Boosts " + parameterBoost(r) + " of " + str(r['gender required']).capitalize() + " units"
                elif str(procID) == r['passive id'] == '43':
                    # DMG TO 1
                    return str(r['take 1 dmg%']) + "% chance of taking 1 damage"
                elif str(procID) == r['passive id'] == '46':
                    # HP SCALING
                    tempArr = []
                    if 'atk% extra buff based on hp' in r and 'def% extra buff based on hp' in r and 'rec% extra buff based on hp' in r:
                        if r['atk% extra buff based on hp'] == r['def% extra buff based on hp'] == r['rec% extra buff based on hp'] and str(r['atk% base buff']) == str(r['def% base buff']) == str(r['rec% base buff']):
                            return str(r['atk% base buff']) + "~" + str(r['atk% extra buff based on hp']) + "% boost to Atk, Def and Rec based on HP " + str(r['buff proportional to hp'])
                    if 'atk% extra buff based on hp' in r and 'def% extra buff based on hp' in r and 'rec% extra buff based on hp' not in r:
                        if r['atk% extra buff based on hp'] == r['def% extra buff based on hp'] and str(r['atk% base buff']) == str(r['def% base buff']):
                            return str(r['atk% base buff']) + "~" + str(r['atk% extra buff based on hp']) + "% boost to Atk and Def based on HP " + str(r['buff proportional to hp'])
                    for s in ['atk% extra buff based on hp','def% extra buff based on hp','rec% extra buff based on hp']:
                        if s in r:
                            if s == 'atk% extra buff based on hp':
                                if r['atk% extra buff based on hp'] < 0:
                                    tempArr.append(str(r['atk% base buff']) + "~" + str(r['atk% extra buff based on hp'] * -1) + "% decrease to Atk based on HP " + str(r['buff proportional to hp']))
                                else:
                                    tempArr.append(str(r['atk% base buff']) + "~" + str(r['atk% extra buff based on hp']) + "% boost to Atk based on HP " + str(r['buff proportional to hp']))
                            elif s == 'def% extra buff based on hp':
                                if r['def% extra buff based on hp'] < 0:
                                    tempArr.append(str(r['def% base buff']) + "~" + str(r['def% extra buff based on hp'] * -1) + "% decrease to Def based on HP " + str(r['buff proportional to hp']))
                                else:
                                    tempArr.append(str(r['def% base buff']) + "~" + str(r['def% extra buff based on hp']) + "% boost to Def based on HP " + str(r['buff proportional to hp']))
                            elif s == 'rec% extra buff based on hp':
                                if r['rec% extra buff based on hp'] < 0:
                                    tempArr.append(str(r['rec% base buff']) + "~" + str(r['rec% extra buff based on hp'] * -1) + "% decrease to Rec based on HP " + str(r['buff proportional to hp']))
                                else:
                                    tempArr.append(str(r['rec% base buff']) + "~" + str(r['rec% extra buff based on hp']) + "% boost to Rec based on HP " + str(r['buff proportional to hp']))
                    return multiStr(tempArr)
                elif str(procID) == r['passive id'] == '47':
                    # BC FILL ON SPARK
                    if r['bc fill on spark%'] == 100:
                        if r['bc fill on spark low'] == r['bc fill on spark high']:
                            return "Boosts BB gauge by " + str(r['bc fill on spark high']) + " BC on spark"
                        else:
                            return "Boosts BB gauge by " + str(r['bc fill on spark low']) + "~" + str(r['bc fill on spark high']) + " BC on spark"
                    else:
                        if r['bc fill on spark low'] == r['bc fill on spark high']:
                            return str(r['bc fill on spark%']) + "% chance of boosting BB gauge by " + str(r['bc fill on spark high']) + " BC on spark"
                        else:
                            return str(r['bc fill on spark%']) + "% chance of boosting BB gauge by " + str(r['bc fill on spark low']) + "~" + str(r['bc fill on spark high']) + " BC on spark"
                elif str(procID) == r['passive id'] == '48':
                    # BC COST REDUCTION
                    if r['reduced bb bc cost%'] < 0:
                        return "Increases BC cost of BB gauge by " + str(r['reduced bb bc cost%'] * -1) + "%"
                    else:
                        return "Reduces BC cost of BB gauge by " + str(r['reduced bb bc cost%']) + "%"
                elif str(procID) == r['passive id'] == '49':
                    # BB CONSUMPTION REDUCTION
                    if r['reduced bb bc use chance%'] == 100:
                        if r['reduced bb bc use% low'] == r['reduced bb bc use% high']:
                            return "Reduces BB gauge consumption by " + str(r['reduced bb bc use% high']) + "%"
                        else:
                            return "Reduces BB gauge consumption by " + str(r['reduced bb bc use% low']) + "~" + str(r['reduced bb bc use% high']) + "%"
                    else:
                        if r['reduced bb bc use% low'] == r['reduced bb bc use% high']:
                            return str(r['reduced bb bc use chance%']) + "% chance of reducing BB gauge consumption by " + str(r['reduced bb bc use% high']) + "%"
                        else:
                            return str(r['reduced bb bc use chance%']) + "% chance of reducing BB gauge consumption by " + str(r['reduced bb bc use% low']) + "~" + str(r['reduced bb bc use% high']) + "%"
                elif str(procID) == r['passive id'] == '50':
                    # EWD
                    tempArr = []
                    for s in ['fire','water','earth','thunder','light','dark']:
                        if s+" units do extra elemental weakness dmg" in r:
                            tempArr.append(s.capitalize())
                    if len(tempArr) == 6:
                        return str(int(r['elemental weakness multiplier%'])) + "% boost to all elemental damage"
                    elif len(tempArr) == 0:
                        return str(int(r['elemental weakness multiplier%'])) + "% boost to all elemental damage"
                    else:
                        return str(int(r['elemental weakness multiplier%'])) + "% boost to " + multiStr(tempArr) + " elemental damage"
                elif str(procID) == r['passive id'] == '53':
                    tempArr = []
                    # BOTH
                    if 'crit dmg buffed damage resist%' in r and 'strong buffed element damage resist%' in r:
                        if r['crit dmg buffed damage resist%'] == 100 and r['strong buffed element damage resist%'] == 100:
                            return "Negates critical and elemental damage"
                    # CRIT NULL
                    if 'crit dmg buffed damage resist%' in r:
                        if r['crit dmg buffed damage resist%'] == 100:
                            tempArr.append("Negates critical damage")
                        else:
                            tempArr.append("Boosts resistance to critical damage by " + str(r['crit dmg buffed damage resist%']) + "%")
                    # EWD NULL
                    if 'strong buffed element damage resist%' in r:
                        if r['strong buffed element damage resist%'] == 100:
                            tempArr.append("Negates elemental damage")
                        else:
                            tempArr.append("Boosts resistance to elemental damage by " + str(r['strong buffed element damage resist%']) + "%")
                    if len(tempArr) > 1:
                        tempArr[1] = tempArr[1].lower()
                    return multiStr(tempArr)
                elif str(procID) == r['passive id'] == '55':
                    # EFFECT CONDITIONAL
                    return "When HP is below " + str(r['hp below % buff activation']) + "% HP, activate following effect:<br>"+buffMap(r['buff'])
                elif str(procID) == r['passive id'] == '58':
                    # GUARD MITIGATION
                    return "Reduces damage taken by " + str(r['guard increase mitigation%']) + "% when guarding"
                elif str(procID) == r['passive id'] == '59':
                    # BC FILL ON GUARD WHEN ATTACKED
                    return "Damage taken boosts BB gauge by " + str(r['bc filled when attacked while guarded']) + " BC when guarding"
                elif str(procID) == r['passive id'] == '61':
                    # BC FILL ON GUARD
                    return "Boosts BB gauge by " + str(r['bc filled on guard']) + " BC when guarding"
                elif str(procID) == r['passive id'] == '62':
                    # ELEMENTAL MITIGATION
                    if mitigateAll(r):
                        return "Reduces all elemental damage taken by " + str(int(r['dmg% mitigation for elemental attacks'])) + "%"
                    else:
                        tempArr = []
                        for s in ['fire', 'water', 'earth', 'thunder', 'light', 'dark']:
                            if 'mitigate '+s+' attacks' in r:
                                tempArr.append(s.capitalize())
                        return "Reduces " + multiStr(tempArr) + " damage taken by " + str(int(r['dmg% mitigation for elemental attacks'])) + "%"
                elif str(procID) == r['passive id'] == '63':
                    # ELEMENTAL MITIGATION FIRST X TURNS
                    if mitigateAll(r):
                        return "Reduces all elemental damage taken by " + str(int(r['dmg% mitigation for elemental attacks'])) + "% for the first " + str(r['dmg% mitigation for elemental attacks buff for first x turns']) + " turns"
                    else:
                        tempArr = []
                        for s in ['fire', 'water', 'earth', 'thunder', 'light', 'dark']:
                            if 'mitigate '+s+' attacks' in r:
                                tempArr.append(s.capitalize())
                        return "Reduces " + multiStr(tempArr) + " damage taken by " + str(int(r['dmg% mitigation for elemental attacks'])) + "% for the first " + str(r['dmg% mitigation for elemental attacks buff for first x turns']) + " turns"
                elif str(procID) == r['passive id'] == '64':
                    # BB ATK
                    if r['bb atk% buff'] == r['sbb atk% buff'] == r['ubb atk% buff']:
                        return str(r['sbb atk% buff']) + "% boost to BB Atk (BB/SBB/UBB)"
                    else:
                        return "Boosts BB Atk by " + str(r['bb atk% buff']) + "%, SBB Atk by " + str(r['sbb atk% buff']) + "% and UBB Atk by " + str(r['ubb atk% buff']) + "%"
                elif str(procID) == r['passive id'] == '65':
                    # BC FILL ON CRIT
                    if r['bc fill on crit%'] == 100:
                        if r['bc fill on crit min'] == r['bc fill on crit max']:
                            return "Boosts BB gauge by " + str(r['bc fill on crit max']) + " BC on critical hit"
                        else:
                            return "Boosts BB gauge by " + str(r['bc fill on crit min']) + "~" + str(r['bc fill on crit max']) + " BC on critical hit"
                    else:
                        if r['bc fill on crit min'] == r['bc fill on crit max']:
                            return str(r['bc fill on crit%']) + "% chance of boosting BB gauge by " + str(r['bc fill on crit max']) + " BC on critical hit"
                        else:
                            return str(r['bc fill on crit%']) + "% chance of boosting BB gauge by " + str(r['bc fill on crit min']) + "~" + str(r['bc fill on crit max']) + " BC on critical hit"
                elif str(procID) == r['passive id'] == '66':
                    # ADD TO BB
                    global globalBuffArr
                    globalBuffArr.clear()
                    globalArrCount = -1
                    triggerStr = ""
                    addBBList = [0,0,0]
                    if 'trigger on bb' in r:
                        addBBList[0] = 1
                    if 'trigger on sbb' in r:
                        addBBList[1] = 1
                    if 'trigger on ubb' in r:
                        addBBList[2] = 1
                    if addBBList == [1,1,0]:
                        triggerStr = "BB/SBB"
                    elif addBBList == [1,1,1]:
                        triggerStr = "BB/SBB/UBB"
                    elif addBBList == [0,1,1]:
                        triggerStr = "SBB/UBB"
                    elif addBBList == [1,0,1]:
                        triggerStr = "BB/UBB"
                    elif addBBList == [1,0,0]:
                        triggerStr = "BB"
                    elif addBBList == [0,1,0]:
                        triggerStr = "SBB"
                    elif addBBList == [0,0,1]:
                        triggerStr = "UBB"
                    allBuffs = []
                    for s in r['triggered effect']:
                        globalBuffArr.append(0)
                        try:
                            allBuffs.append(str(s['proc id']))
                        except:
                            allBuffs.append(str(s['unknown proc id']))
                    tempStr = ""
                    for s in allBuffs:
                        globalArrCount = globalArrCount + 1
                        if s in ['5','16','39','51','55','62','10015','10016','10017']:
                            if s == '5':
                                for t in ['', 'fire', 'water', 'earth', 'thunder', 'light', 'dark']:
                                    for u in ['atk', 'def', 'rec', 'crit']:
                                        if searchBuffs(s, r['triggered effect'], str(u) + str(t)) != 'null':
                                            tempStr = addBuff(tempStr, r, s, str(u) + str(t))
                            elif s in ['16','39','51','55','62','10015','10016','10017']:
                                for t in ['fire', 'water', 'earth', 'thunder', 'light', 'dark']:
                                    if searchBuffs(s, r['triggered effect'],  str(t)) != 'null':
                                        tempStr = addBuff(tempStr, r, s, str(t))
                        elif s == '6':
                            for t in ['bc','hc','item']:
                                if searchBuffs(s, r['triggered effect'], str(t)) != 'null':
                                    tempStr = addBuff(tempStr, r, s, str(t))
                        elif s in ['9','24','78','89','130']:
                            if s in ['9','24','89','130']:
                                for t in ['atk','def','rec']:
                                    if searchBuffs(s, r['triggered effect'], str(t)) != 'null':
                                        tempStr = addBuff(tempStr, r, s, str(t))
                            elif s in ['78']:
                                for t in ['atk','def','rec','crit']:
                                    if searchBuffs(s, r['triggered effect'], str(t)) != 'null':
                                        tempStr = addBuff(tempStr, r, s, str(t))
                        elif s in ['11','40']:
                            for t in ['curse','poison','paralysis','injury','sick','weaken']:
                                if searchBuffs(s, r['triggered effect'], str(t)) != 'null':
                                    tempStr = addBuff(tempStr, r, s, str(t))
                        elif s in ['53']:
                            for t in ['curse% (82)', 'poison% (78)', 'paralysis% (83)', 'injury% (81)', 'sick% (80)', 'weaken% (79)']:
                                if searchBuffs(s, r['triggered effect'], str(t)) != 'null':
                                    tempStr = addBuff(tempStr, r, s, str(t))
                        elif s in ['93','132']:
                            if s in ['93']:
                                for t in ['crit','ewd','spark']:
                                    if searchBuffs(s, r['triggered effect'], str(t)) != 'null':
                                        tempStr = addBuff(tempStr, r, s, str(t))
                            elif s in ['132']:
                                for t in ['crit','ewd']:
                                    if searchBuffs(s, r['triggered effect'], str(t)) != 'null':
                                        tempStr = addBuff(tempStr, r, s, str(t))
                        else:
                            tempStr = addBuff(tempStr, r, s, "")
                    return "Adds the following effect(s) to " + triggerStr + ":\n" + tempStr[:-1]
                elif str(procID) == r['passive id'] == '69':
                    # CHANCE KO RESISTANCE
                    if 'angel idol recover hp%' in r:
                        return str(
                            int(r['angel idol recover chance% high'])) + "% chance of resisting " + str(r['angel idol recover counts']) + " KO, restores " + str(
                            r['angel idol recover hp%']) + "% of unit's HP"
                    else:
                        return str(int(r['angel idol recover chance% high'])) + "% chance of resisting " + str(r['angel idol recover counts']) + " KO"
                elif str(procID) == r['passive id'] == '70':
                    # OD FILL RATE
                    return str(r['od fill rate%']) + "% boost to OD fill rate"
                elif str(procID) == r['passive id'] == '71':
                    # STATUS COUNTER
                    counterArr = []
                    for s in ['curse', 'injury', 'paralysis', 'poison', 'sick', 'weaken']:
                        if "counter inflict " + s + "%" in r:
                            counterArr.append(s + "," + str(r["counter inflict " + s + "%"]))
                    distinct = []
                    for s in counterArr:
                        if s.split(',')[1] not in distinct:
                            distinct.append(s.split(',')[1])
                    bigStr = ""
                    for s in distinct:
                        tempArr = []
                        tempCount = 0
                        for t in counterArr:
                            if t.split(',')[1] == s and t.split(',')[0].capitalize() not in tempArr:
                                tempArr.append(t.split(',')[0].capitalize())
                        bigStr = bigStr + s + "% chance of inflicting " + multiStr(tempArr) + " when damage is taken<br>"
                    return bigStr[:-4]
                elif str(procID) == r['passive id'] == '73':
                    # STATUS NEGATION AND PARAMETER REDUCTION NEGATION
                    check1 = True
                    check2 = True
                    tempArr = []
                    for s in ['curse','injury','paralysis','poison','sick','weaken']:
                        if s + " resist%" in r:
                            tempArr.append(s.capitalize())
                        if s + " resist%" not in r:
                            check1 = False
                    for s in ['atk down','def down','rec down']:
                        if s + " resist%" in r:
                            tempArr.append(s[0:3].capitalize())
                        if s + " resist%" not in r:
                            check2 = False
                    if check1 and check2:
                        return "Negates all status ailments and Atk, Def, Rec reduction effects"
                    elif check1:
                        return "Negates all status ailments"
                    elif check2:
                        return "Negates Atk, Def, Rec reduction effects"
                    else:
                        return "Negates " + multiStr(tempArr)
                elif str(procID) == r['passive id'] == '74':
                    # STATUS AFFLICTED ATK BONUS
                    return str(r['atk% buff when enemy has ailment']) + "% boost to Atk when enemy is status afflicted"
                elif str(procID) == r['passive id'] == '75':
                    # SPARK VULNERABILITY
                    tempChar = ""
                    if r['spark debuff turns'] != 0:
                        tempChar = "s"
                    if r['spark debuff chance%'] == 100:
                        return "Inflicts " + str(r['spark debuff%']) + "% spark vulnerability for " + str(int(r['spark debuff turns']) + 1) + " turn" + tempChar
                    else:
                        return str(int(r['spark debuff chance%'])) + "% chance of inflicting " + str(
                            r['spark debuff%']) + "% spark vulnerability for " + str(int(r['spark debuff turns']) + 1) + " turn" + tempChar
                elif str(procID) == r['passive id'] == '77':
                    # SPARK RESISTANCE
                    if r['buff spark dmg% resist'] == 100:
                        return "Negates spark damage"
                    else:
                        return str(r['buff spark dmg% resist']) + "% resistance to spark damage"
                elif str(procID) == r['passive id'] == '78':
                    # EFFECT CONDITIONAL
                    return "When " + str(r['damage threshold buff activation']) + " or more damage is taken, activate following effect:<br>"+buffMap(r['buff'])
                elif str(procID) == r['passive id'] == '79':
                    # EFFECT CONDITIONAL
                    return "Boosts BB gauge by " + str(r['increase bb gauge']) + " BC when " + str(r['damage threshold activation']) + " or more damage is taken"
                elif str(procID) == r['passive id'] == '80':
                    # EFFECT CONDITIONAL
                    return "When " + str(r['damage dealt threshold buff activation']) + " or more damage is dealt, activate following effect:<br>"+buffMap(r['buff'])
                elif str(procID) == r['passive id'] == '81':
                    # EFFECT CONDITIONAL
                    if r['increase bb gauge'] == 0:
                        return "Fully fills BB gauge when " + str(
                            r['damage dealt threshold activation']) + " or more damage is dealt"
                    else:
                        return "Boosts BB gauge by " + str(r['increase bb gauge']) + " BC when " + str(r['damage dealt threshold activation']) + " or more damage is dealt"
                elif str(procID) == r['passive id'] == '82':
                    # EFFECT CONDITIONAL
                    return "When " + str(r['bc receive count buff activation']) + " or more BC is collected, activate following effect:<br>"+buffMap(r['buff'])
                elif str(procID) == r['passive id'] == '84':
                    # EFFECT CONDITIONAL
                    return "When " + str(r['hc receive count buff activation']) + " or more HC is collected, activate following effect:<br>"+buffMap(r['buff'])
                elif str(procID) == r['passive id'] == '85':
                    # EFFECT CONDITIONAL
                    return "Boosts BB gauge by " + str(r['increase bb gauge']) + " BC when " + str(r['hc receive count activation']) + " or more HC is collected"
                elif str(procID) == r['passive id'] == '86':
                    # EFFECT CONDITIONAL
                    return "When " + str(r['spark count buff activation']) + " or more sparks are performed, activate following effect:<br>"+buffMap(r['buff'])
                elif str(procID) == r['passive id'] == '88':
                    # EFFECT CONDITIONAL
                    if r['on guard activation chance%'] == 100:
                        return "When guarding, activate following effect:<br>"+buffMap(r['buff'])
                    else:
                        return "Guarding has a " + str(r['on guard activation chance%']) + " activate following effect:<br>"+buffMap(r['buff'])
                elif str(procID) == r['passive id'] == '89':
                    # EFFECT CONDITIONAL
                    if r['on crit activation chance%'] == 100:
                        return "When landing a critical hit, activate following effect:<br>"+buffMap(r['buff'])
                    else:
                        return "Landing a critical hit has a " + str(r['on crit activation chance%']) + " activate following effect:<br>"+buffMap(r['buff'])
                elif str(procID) == r['passive id'] == '90':
                    # STATUS COUNTER
                    counterArr = []
                    for s in ['curse', 'injury', 'paralysis', 'poison', 'sick', 'weaken']:
                        if "inflict " + s + "%" in r:
                            counterArr.append(s + "," + str(r["inflict " + s + "%"]))
                    distinct = []
                    for s in counterArr:
                        if s.split(',')[1] not in distinct:
                            distinct.append(s.split(',')[1])
                    bigStr = ""
                    for s in distinct:
                        tempArr = []
                        tempCount = 0
                        for t in counterArr:
                            if t.split(',')[1] == s and t.split(',')[0].capitalize() not in tempArr:
                                tempArr.append(t.split(',')[0].capitalize())
                        bigStr = bigStr + s + "% chance of inflicting " + multiStr(tempArr) + " when landing a critical hit<br>"
                    return bigStr[:-4]
                elif str(procID) == r['passive id'] == '92':
                    # IGNORE DEF RESISTANCE
                    if r['ignore def resist chance%'] == 100:
                        return "Negates Def-ignoring damage"
                    else:
                        return str(r['ignore def resist chance%']) + "% resistance to Def-ignoring damage"
                elif str(procID) == r['passive id'] == '96':
                    # AOE NORMAL ATTACK
                    if r['aoe atk inc%'] == 0:
                        return str(r['chance to aoe']) + "% chance of attacking all enemies with normal attack"
                    else:
                        return str(r['chance to aoe']) + "% chance of attacking all enemies with normal attack (" + str(r['aoe atk inc%']) + "% AoE damage modifier)"
                elif str(procID) == r['passive id'] == '100':
                    # SPARK CRIT
                    return str(r['spark crit chance%']) + "% chance of dealing " + str(r['spark crit dmg%']) + "% extra spark damage"
                elif str(procID) == r['passive id'] == '101':
                    # HEAL ON SPARK
                    if r['heal on spark%'] == 100:
                        if r['heal on spark low'] == r['heal on spark high']:
                            return "Heals " + str(r['heal on spark high']) + " HP on spark"
                        else:
                            return "Heals " + str(r['heal on spark low']) + "~" + str(
                                r['heal on spark high']) + " HP on spark"
                    else:
                        if r['heal on spark low'] == r['heal on spark high']:
                            return str(r['heal on spark%']) + "% chance of healing " + str(r['heal on spark high']) + " HP on spark"
                        else:
                            return str(r['heal on spark%']) + "% chance of healing " + str(r['heal on spark low']) + "~" + str(r['heal on spark high']) + " HP on spark"
                elif str(procID) == r['passive id'] == '102':
                    # ADDED ELEMENTS
                    tempArr = []
                    for s in r['elements added']:
                        tempArr.append(s.capitalize())
                    if len(tempArr) == 1:
                        return "Adds " + multiStr(tempArr) + " element to attack"
                    else:
                        return "Adds " + multiStr(tempArr) + " elements to attack"
                elif str(procID) == r['passive id'] == '103':
                    # BB ATK CONDITIONAL
                    if 'bb atk% add' in r and 'sbb atk% add' in r and 'ubb atk% add' in r:
                        if r['bb atk% add'] == r['sbb atk% add'] == r['ubb atk% add']:
                            if r['triggered when hp'] == 'higher':
                                return "Boosts BB Atk by " + str(r['sbb atk% add']) + "% when HP is above " + str(r['hp threshold']) + "%"
                            else:
                                return "Boosts BB Atk by " + str(r['sbb atk% add']) + "% when HP is below " + str(
                                    r['hp threshold']) + "%"
                    tempArr = []
                    for s in r['bb atk% add','sbb atk% add','ubb atk% add']:
                        if s == 'bb atk% add' and s in r:
                            tempArr.append("BB Atk by " + str(r['bb atk% add']) + "%")
                        elif s == 'sbb atk% add' and s in r:
                            tempArr.append("SBB Atk by " + str(r['sbb atk% add']) + "%")
                        elif s == 'ubb atk% add' and s in r:
                            tempArr.append("UBB Atk by " + str(r['ubb atk% add']) + "%")
                    if r['triggered when hp'] == 'higher':
                        return "Boosts " + multiStr(tempArr) + " when HP is above " + str(
                            r['hp threshold']) + "%"
                    else:
                        return "Boosts " + multiStr(tempArr) + " when HP is below " + str(
                            r['hp threshold']) + "%"
                elif str(procID) == r['passive id'] == '104':
                    # SPARK WHEN BELOW THRESHOLD
                    if 'hp below % buff requirement' in r:
                        return "Boosts spark damage by " + str(r['damage% for spark']) + "% when HP is below " + str(r['hp below % buff requirement']) + "%"
                    else:
                        return "Boosts spark damage by " + str(r['damage% for spark']) + "% when HP is above " + str(r['hp above % buff requirement']) + "%"
                elif str(procID) == r['passive id'] == '105':
                    if 'atk% max buff' in r and 'def% max buff' in r and 'rec% max buff' in r:
                        if r['atk% max buff'] == r['def% max buff'] == r['rec% max buff']:
                            return str(r['atk% max buff'] / r['turn count']) + "% boost to Atk, Def, Rec (" + str(r['atk% max buff']) + "% max, up to " + str(r['turn count']) + " turns)"
                    tempArr = []
                    for s in ['atk% max buff','def% max buff','rec% max buff']:
                        if s in r:
                                tempArr.append(str(r['atk% max buff'] / r['turn count']) + "% boost to " + s[0:3].capitalize() + " (" + str(
                                r[s]) + "% max, up to " + str(r['turn count']) + " turns)")
                    return multiStr(tempArr)
                elif str(procID) == r['passive id'] == '111':
                    return "Boosts BB activation rates in Arena modes by " + str(r['increase skill activation in arena%']) + "%"
                elif str(procID) == r['passive id'] == '112':
                    return "Increases ABP gain by " + str(r['abp gain%']) + "% and CBP gain by " + str(r['cbp gain%']) + "%"
                elif str(procID) == r['passive id'] == '143':
                    return "Raises Atk parameter limit to " + str(r['increase atk cap'])
            if 'unknown passive id' in r:
                if str(procID) == r['unknown passive id'] == '72':
                    # TURN'S START
                    if r['unknown passive params'] == "1,1":
                        return "Activates [[Gradual Healing]] and [[Gradual BB Gauge Boost]] effects at the start of turn instead"
                    elif r['unknown passive params'] == "1,0":
                        return "Activates [[Gradual Healing]] effects at the start of turn instead"
                    elif r['unknown passive params'] == "0,1":
                        return "Activates [[Gradual BB Gauge Boost]] effects at the start of turn instead"
                elif str(procID) == r['unknown passive id'] == '91':
                    params = r['unknown passive params'].split(',')
                    return "Boosts spark damage by " + params[1] + " for the first " + params[2] + " turns"
                elif str(procID) == r['unknown passive id'] == '106':
                    return "When unit overdrives, activate following effect:<br>"+unknownMap(r)
                elif str(procID) == r['unknown passive id'] == '107':
                    return "Add following effect to Leader Skill:<br>"+leaderMap(r)
                elif str(procID) == r['unknown passive id'] == '109':
                    params = r['unknown passive params'].split(',')
                    return params[1] + "% chance of reducing BC efficacy by " + str(int(params[0])*-1) + "%"
                elif str(procID) == r['unknown passive id'] == '110':
                    params = r['unknown passive params'].split(',')
                    return params[4] + "% chance of reducing BC efficacy by " + str(int(params[2])) + "%"
                elif str(procID) == r['unknown passive id'] == '113':
                    params = r['unknown passive params'].split(',')
                    stats = params[1].split('$')
                    if stats[0] == stats[1] == stats[2]:
                        return "Boosts BB Atk by " + str(stats[0]) + "% when HP is above " + params[2] + "%"
                    tempArr = []
                    if stats[0] != "0":
                        tempArr.append("BB Atk by " + stats[0] + "%")
                    if stats[1] != "0":
                        tempArr.append("SBB Atk by " + stats[1] + "%")
                    if stats[2] != "0":
                        tempArr.append("UBB Atk by " + stats[2] + "%")
                    return "Boosts "+multiStr(tempArr)
                elif str(procID) == r['unknown passive id'] == '127':
                    params = r['unknown passive params'].split(',')
                    return "Reduces DoT damage by " + params[1] + "%"
                elif str(procID) == r['unknown passive id'] == '128':
                    params = r['unknown passive params'].split(',')
                    return "Reduces normal attack damage by " + params[1] + "%"
                elif str(procID) == r['unknown passive id'] == '10008':
                    params = r['unknown passive params'].split(',')
                    return "Reduces damage taken by " + params[0] + "%"
                elif str(procID) == r['unknown passive id'] == '11004':
                    params = r['unknown passive params'].split(',')
                    return params[1] + "% boost to spark damage"
                elif str(procID) == r['unknown passive id'] == '11005':
                    params = r['unknown passive params'].split(',')
                    return str(int(float(params[1])*100)) + "% boost to critical damage"
                elif str(procID) == r['unknown passive id'] == '11006':
                    params = r['unknown passive params'].split(',')
                    return "Increases Summoner EXP gain by " + str(params[0]) + "%"
                elif str(procID) == r['unknown passive id'] == '11009':
                    params = r['unknown passive params'].split(',')
                    allBuffs = params[0].split(':')
                    #print(allBuffs)
                    tempArr = []
                    for s in allBuffs:
                        tempArr.append(effectMap[s])
                    if int(params[1]) < 0:
                        if int(params[1]) == -1:
                            return "Reduces buff durations of the following effects by " + str(
                                int(params[1]) * -1) + " turn: " + multiStr(tempArr)
                        else:
                            return "Reduces buff durations of the following effects by " + str(
                                int(params[1]) * -1) + " turns: " + multiStr(tempArr)
                    else:
                        if int(params[1]) == 1:
                            return "Increases buff durations of the following effects by " + params[
                                1] + " turn: " + multiStr(
                                tempArr)
                        else:
                            return "Increases buff durations of the following effects by " + params[
                                1] + " turns: " + multiStr(
                                tempArr)



def printPassives(dataID,mode):
    #print(dataID)
    output = "{{PassiveList\n"
    count = 0
    allPassives = []
    global globalArr
    global statusCheck
    global errors
    statusCheck = False
    globalArr.clear()
    globalArrCount = -1
    if mode == 'item':
        if 'effect' in items[dataID].keys():
            for r in items[dataID]['effect']:
                globalArr.append(0)
                if 'passive id' in r:
                    allPassives.append(str(r['passive id']))
                elif 'unknown passive id' in r:
                    allPassives.append(str(r['unknown passive id']))
    elif mode == 'ls':
        if 'effects' in ls[dataID].keys():
            for r in ls[dataID]['effects']:
                globalArr.append(0)
                try:
                    allPassives.append(str(r['passive id']))
                except:
                    allPassives.append(str(r['unknown passive id']))
    elif mode == 'es':
        if 'effects' in es[dataID].keys():
            for r in es[dataID]['effects']:
                globalArr.append(0)
                try:
                    allPassives.append(str(r['passive id']))
                except:
                    allPassives.append(str(r['unknown passive id']))
    for r in allPassives:
        globalArrCount = globalArrCount + 1
        temp = ""
        success = False
        try:
            if r == '20':
                count = count + 1
                if searchPassives(dataID, "item", r, "") != "Move on":
                    #count = count + 1
                    temp = "|passive_" + header(str(count), "proc") + "= " + str(r) + "\n" + \
                           "|passive_" + header(str(count), "potency") + "= " + searchPassives(dataID, mode, r, "") + "\n"
                    success = True
            else:
                count = count + 1
                temp = "|passive_" + header(str(count), "proc") + "= " + str(r) + "\n" + \
                       "|passive_" + header(str(count), "potency") + "= " + searchPassives(dataID, mode, r, "") + "\n"
                success = True
        except:
            temp = "|passive_" + header(str(count), "proc") + "= " + str(r) + "\n" + \
                   "|passive_" + header(str(count), "potency") + "= Failed to retrieve value\n"
            print("Error on " + str(dataID) + ": Proc ID " + str(r))
            errors = errors + 1
            output = output + temp
        if (success):
            output = output + temp
        globalArr[globalArrCount] = 1
        #print(globalArr)
    output = output + "}}"
    #print(output)
    return output


def errorCheck(mode):
    if mode == 'item':
        for r in items.keys():
            printPassives(r, mode)
    print(str(errors) + " errors found")


def nameToID(input, mode):
    if mode == 'item':
        for r in items.keys():
            if items[r]['name'] == str(input) or str(input) == str(r):
                return r
    elif mode == 'ls':
        for r in ls.keys():
            if ls[r]['name'] == str(input) or str(input) == str(r):
                return r
    elif mode == 'es':
        for r in es.keys():
            if es[r]['name'] == str(input) or str(input) == str(r):
                return r


def searchBuffs(procID, area, extraArg):
    global errors
    arrCount = -1
    for r in area:
        arrCount = arrCount + 1
        if globalBuffArr[arrCount] != 1:
            if 'proc id' in r:
                # REGULAR DAMAGE
                if str(procID) == r['proc id'] == '1':
                    if extraArg == 'turns':
                        return "—"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        extraPropStr = ""
                        extraPropArr = []
                        if 'bb crit%' in r:
                            extraPropArr.append(str(r['bb crit%']) + "% innate crit rate")
                        if 'bb bc%' in r:
                            extraPropArr.append(str(r['bb bc%']) + "% innate BC drop rate")
                        if 'bb hc%' in r:
                            extraPropArr.append(str(r['bb hc%']) + "% innate HC drop rate")
                        if len(extraPropArr) == 3:
                            return str(r['bb atk%']) + "% damage modifier (" + extraPropArr[0] + ", " + \
                                   extraPropArr[1] + " and " + extraPropArr[2] + ")"
                        elif len(extraPropArr) == 2:
                            return str(r['bb atk%']) + "% damage modifier (" + extraPropArr[0] + " and " + \
                                   extraPropArr[
                                       1] + ")"
                        elif len(extraPropArr) == 1:
                            return str(r['bb atk%']) + "% damage modifier (" + extraPropArr[0] + ")"
                        else:
                            return str(r['bb atk%']) + "% damage modifier"
                # BURST HEALING
                if str(procID) == r['proc id'] == '2':
                    if extraArg == 'turns':
                        return "—"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return "Heals " + str(r['heal low']) + "~" + str(r['heal high']) + " + " + str(
                            int(r['rec added% (from healer)'])) + "% Rec of HP instantly"
                # GRADUAL HEALING
                if str(procID) == r['proc id'] == '3':
                    if extraArg == 'turns':
                        if r['gradual heal turns (8)'] == 1:
                            return str(r['gradual heal turns (8)']) + " turn"
                        else:
                            return str(r['gradual heal turns (8)']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return "Heals " + str(r['gradual heal low']) + "~" + str(
                            r['gradual heal high']) + " + " + str(
                            int(r['rec added% (from target)'])) + "% Rec of HP each turn"
                # BB GAUGE REFILL
                if str(procID) == r['proc id'] == '4':
                    if extraArg == 'turns':
                        return "—"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        if 'bb bc fill%' in r:
                            return "Refills BB gauge to " + str(r['bb bc fill%']) + "%"
                        elif 'bb bc fill' in r:
                            return "Refills BB gauge by " + str(r['bb bc fill']) + " BC"
                        else:
                            return "null"
                # PARAMETER BOOST
                if str(procID) == r['proc id'] == '5':
                    if extraArg == 'atk':
                        if 'atk% buff (1)' in r:
                            return str(r['atk% buff (1)']) + "% boost to Atk"
                        else:
                            return "null"
                    elif extraArg == 'def':
                        if 'def% buff (3)' in r:
                            return str(r['def% buff (3)']) + "% boost to Def"
                        else:
                            return "null"
                    elif extraArg == 'rec':
                        if 'rec% buff (5)' in r:
                            return str(r['rec% buff (5)']) + "% boost to Rec"
                        else:
                            return "null"
                    elif extraArg == 'crit':
                        if 'crit% buff (7)' in r:
                            return str(r['crit% buff (7)']) + "% boost to critical rate"
                        else:
                            return "null"
                    elif extraArg == 'atkfire':
                        if 'atk% buff (13)' in r and r['element buffed'] == 'fire':
                            return str(r['atk% buff (13)']) + "% boost to Atk of Fire units"
                        else:
                            return "null"
                    elif extraArg == 'deffire':
                        if 'def% buff (14)' in r and r['element buffed'] == 'fire':
                            return str(r['def% buff (14)']) + "% boost to Def of Fire units"
                        else:
                            return "null"
                    elif extraArg == 'recfire':
                        if 'rec% buff (15)' in r and r['element buffed'] == 'fire':
                            return str(r['rec% buff (15)']) + "% boost to Rec of Fire units"
                        else:
                            return "null"
                    elif extraArg == 'critfire':
                        if 'crit% buff (16)' in r and r['element buffed'] == 'fire':
                            return str(r['crit% buff (16)']) + "% boost to critical rate of Fire units"
                        else:
                            return "null"
                    elif extraArg == 'atkwater':
                        if 'atk% buff (13)' in r and r['element buffed'] == 'water':
                            return str(r['atk% buff (13)']) + "% boost to Atk of Water units"
                        else:
                            return "null"
                    elif extraArg == 'defwater':
                        if 'def% buff (14)' in r and r['element buffed'] == 'water':
                            return str(r['def% buff (14)']) + "% boost to Def of Water units"
                        else:
                            return "null"
                    elif extraArg == 'recwater':
                        if 'rec% buff (15)' in r and r['element buffed'] == 'water':
                            return str(r['rec% buff (15)']) + "% boost to Rec of Water units"
                        else:
                            return "null"
                    elif extraArg == 'critwater':
                        if 'crit% buff (16)' in r and r['element buffed'] == 'water':
                            return str(r['crit% buff (16)']) + "% boost to critical rate of Water units"
                        else:
                            return "null"
                    elif extraArg == 'atkearth':
                        if 'atk% buff (13)' in r and r['element buffed'] == 'earth':
                            return str(r['atk% buff (13)']) + "% boost to Atk of Earth units"
                        else:
                            return "null"
                    elif extraArg == 'defearth':
                        if 'def% buff (14)' in r and r['element buffed'] == 'earth':
                            return str(r['def% buff (14)']) + "% boost to Def of Earth units"
                        else:
                            return "null"
                    elif extraArg == 'recearth':
                        if 'rec% buff (15)' in r and r['element buffed'] == 'earth':
                            return str(r['rec% buff (15)']) + "% boost to Rec of Earth units"
                        else:
                            return "null"
                    elif extraArg == 'critearth':
                        if 'crit% buff (16)' in r and r['element buffed'] == 'earth':
                            return str(r['crit% buff (16)']) + "% boost to critical rate of Earth units"
                        else:
                            return "null"
                    elif extraArg == 'atkthunder':
                        if 'atk% buff (13)' in r and r['element buffed'] == 'thunder':
                            return str(r['atk% buff (13)']) + "% boost to Atk of Thunder units"
                        else:
                            return "null"
                    elif extraArg == 'defthunder':
                        if 'def% buff (14)' in r and r['element buffed'] == 'thunder':
                            return str(r['def% buff (14)']) + "% boost to Def of Thunder units"
                        else:
                            return "null"
                    elif extraArg == 'recthunder':
                        if 'rec% buff (15)' in r and r['element buffed'] == 'thunder':
                            return str(r['rec% buff (15)']) + "% boost to Rec of Thunder units"
                        else:
                            return "null"
                    elif extraArg == 'critthunder':
                        if 'crit% buff (16)' in r and r['element buffed'] == 'thunder':
                            return str(r['crit% buff (16)']) + "% boost to critical rate of Thunder units"
                        else:
                            return "null"
                    elif extraArg == 'atklight':
                        if 'atk% buff (13)' in r and r['element buffed'] == 'light':
                            return str(r['atk% buff (13)']) + "% boost to Atk of Light units"
                        else:
                            return "null"
                    elif extraArg == 'deflight':
                        if 'def% buff (14)' in r and r['element buffed'] == 'light':
                            return str(r['def% buff (14)']) + "% boost to Def of Light units"
                        else:
                            return "null"
                    elif extraArg == 'reclight':
                        if 'rec% buff (15)' in r and r['element buffed'] == 'light':
                            return str(r['rec% buff (15)']) + "% boost to Rec of Light units"
                        else:
                            return "null"
                    elif extraArg == 'critlight':
                        if 'crit% buff (16)' in r and r['element buffed'] == 'light':
                            return str(r['crit% buff (16)']) + "% boost to critical rate of Light units"
                        else:
                            return "null"
                    elif extraArg == 'atkdark':
                        if 'atk% buff (13)' in r and r['element buffed'] == 'dark':
                            return str(r['atk% buff (13)']) + "% boost to Atk of Dark units"
                        else:
                            return "null"
                    elif extraArg == 'defdark':
                        if 'def% buff (14)' in r and r['element buffed'] == 'dark':
                            return str(r['def% buff (14)']) + "% boost to Def of Dark units"
                        else:
                            return "null"
                    elif extraArg == 'recdark':
                        if 'rec% buff (15)' in r and r['element buffed'] == 'dark':
                            return str(r['rec% buff (15)']) + "% boost to Rec of Dark units"
                        else:
                            return "null"
                    elif extraArg == 'critdark':
                        if 'crit% buff (16)' in r and r['element buffed'] == 'dark':
                            return str(r['crit% buff (16)']) + "% boost to critical rate of Dark units"
                        else:
                            return "null"
                    elif extraArg == 'turns':
                        if r['buff turns'] == 1:
                            return str(r['buff turns']) + " turn"
                        else:
                            return str(r['buff turns']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return "null"
                # DROP RATE
                if str(procID) == r['proc id'] == '6':
                    if extraArg == 'bc':
                        if 'bc drop rate% buff (10)' in r:
                            return str(r['bc drop rate% buff (10)']) + "% boost to BC drop rate"
                        else:
                            return "null"
                    elif extraArg == 'hc':
                        if 'hc drop rate% buff (9)' in r:
                            return str(r['hc drop rate% buff (9)']) + "% boost to HC drop rate"
                        else:
                            return "null"
                    elif extraArg == 'item':
                        if 'item drop rate% buff (11)' in r:
                            return str(r['item drop rate% buff (11)']) + "% boost to Item drop rate"
                        else:
                            return "null"
                    elif extraArg == 'turns':
                        if r['drop rate buff turns'] == 1:
                            return str(r['drop rate buff turns']) + " turn"
                        else:
                            return str(r['drop rate buff turns']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return "null"
                # GUARANTEED KO RESISTANCE
                if str(procID) == r['proc id'] == '7':
                    if extraArg == 'turns':
                        return "—"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return "Becomes able to withstand 1 KO"
                # MAX HP BOOST
                if str(procID) == r['proc id'] == '8':
                    if extraArg == 'turns':
                        return "—"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return str(int(r['max hp% increase'])) + "% boost to max HP"
                # PARAMETER REDUCTION
                if str(procID) == r['proc id'] == '9':
                    if extraArg == 'atk':
                        if 'buff #1' in r and 'buff #2' in r:
                            if 'atk% buff (2)' in r['buff #1']:
                                return str(int(
                                    r['buff #1']['proc chance%'])) + "% chance of reducing Atk by " + str(
                                    int(r['buff #1']['atk% buff (2)'] * -1)) + "%"
                            elif 'atk% buff (2)' in r['buff #2']:
                                return str(int(
                                    r['buff #2']['proc chance%'])) + "% chance of reducing Atk by " + str(
                                    int(r['buff #2']['atk% buff (2)'] * -1)) + "%"
                            else:
                                return "null"
                        elif 'buff #1' in r and 'buff #2' not in r:
                            if 'atk% buff (2)' in r['buff #1']:
                                return str(int(
                                    r['buff #1']['proc chance%'])) + "% chance of reducing Atk by " + str(
                                    int(r['buff #1']['atk% buff (2)'] * -1)) + "%"
                            else:
                                return "null"
                        else:
                            return "null"
                    elif extraArg == 'def':
                        if 'buff #1' in r and 'buff #2' in r:
                            if 'def% buff (4)' in r['buff #1']:
                                return str(int(
                                    r['buff #1']['proc chance%'])) + "% chance of reducing Def by " + str(
                                    int(r['buff #1']['def% buff (4)'] * -1)) + "%"
                            elif 'def% buff (4)' in r['buff #2']:
                                return str(int(
                                    r['buff #2']['proc chance%'])) + "% chance of reducing Def by " + str(
                                    int(r['buff #2']['def% buff (4)'] * -1)) + "%"
                            else:
                                return "null"
                        elif 'buff #1' in r and 'buff #2' not in r:
                            if 'def% buff (4)' in r['buff #1']:
                                return str(int(
                                    r['buff #1']['proc chance%'])) + "% chance of reducing Def by " + str(
                                    int(r['buff #1']['def% buff (4)'] * -1)) + "%"
                            else:
                                return "null"
                        else:
                            return "null"
                    elif extraArg == 'rec':
                        if 'buff #1' in r and 'buff #2' in r:
                            if 'rec% buff (6)' in r['buff #1']:
                                return str(int(
                                    r['buff #1']['proc chance%'])) + "% chance of reducing Rec by " + str(
                                    int(r['buff #1']['rec% buff (6)'] * -1)) + "%"
                            elif 'rec% buff (6)' in r['buff #2']:
                                return str(int(
                                    r['buff #2']['proc chance%'])) + "% chance of reducing Rec by " + str(
                                    int(r['buff #2']['rec% buff (6)'] * -1)) + "%"
                            else:
                                return "null"
                        elif 'buff #1' in r and 'buff #2' not in r:
                            if 'rec% buff (6)' in r['buff #1']:
                                return str(int(
                                    r['buff #1']['proc chance%'])) + "% chance of reducing Rec by " + str(
                                    int(r['buff #1']['rec% buff (6)'] * -1)) + "%"
                            else:
                                return "null"
                        else:
                            return "null"
                    elif extraArg == 'turns':
                        if r['buff turns'] == 1:
                            return str(r['buff turns']) + " turn"
                        else:
                            return str(r['buff turns']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return "null"
                # STATUS CURE (OLD)
                if str(procID) == r['proc id'] == '10':
                    if extraArg == 'turns':
                        return "—"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return "Removes all status ailments"
                # STATUS INFLICTION
                if str(procID) == r['proc id'] == '11':
                    if extraArg in ['curseturns', 'paralysisturns']:
                        return "1 turn"
                    elif extraArg in ['poisonturns', 'injuryturns', 'weakenturns', 'sickturns']:
                        return "3 turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        if extraArg in ['curse', 'poison', 'paralysis', 'injury', 'sick', 'weaken']:
                            if str(extraArg) + '%' in r:
                                if extraArg == 'weaken':
                                    return str(
                                        int(r[str(extraArg) + "%"])) + "% chance of inflicting Weak"
                                else:
                                    return str(
                                        int(r[str(
                                            extraArg) + "%"])) + "% chance of inflicting " + extraArg.capitalize()
                            else:
                                return "null"
                        else:
                            return "null"
                # RANDOM TARGET DAMAGE
                if str(procID) == r['proc id'] == '13':
                    if extraArg == 'turns':
                        return "—"
                    elif extraArg == 'target':
                        return "Random enemies"
                    else:
                        extraPropStr = ""
                        extraPropArr = []
                        if 'bb crit%' in r:
                            extraPropArr.append(str(r['bb crit%']) + "% innate crit rate")
                        if 'bb bc%' in r:
                            extraPropArr.append(str(r['bb bc%']) + "% innate BC drop rate")
                        if 'bb hc%' in r:
                            extraPropArr.append(str(r['bb hc%']) + "% innate HC drop rate")
                        if len(extraPropArr) == 3:
                            return str(r['bb atk%']) + "% damage modifier (" + extraPropArr[0] + ", " + \
                                   extraPropArr[
                                       1] + " and " + extraPropArr[2] + ")"
                        elif len(extraPropArr) == 2:
                            return str(r['bb atk%']) + "% damage modifier (" + extraPropArr[0] + " and " + \
                                   extraPropArr[
                                       1] + ")"
                        elif len(extraPropArr) == 1:
                            return str(r['bb atk%']) + "% damage modifier (" + extraPropArr[0] + ")"
                        else:
                            return str(r['bb atk%']) + "% damage modifier"
                # LIFESTEAL DAMAGE
                if str(procID) == r['proc id'] == '14':
                    if extraArg == 'turns':
                        return "—"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        if 'bb crit%' in r:
                            return str(r['bb atk%']) + "% damage modifier and drains " + str(
                                r['hp drain% low']) + "~" + str(
                                r['hp drain% high']) + " of damage dealt as HP (" + str(
                                r['bb crit%']) + "% innate crit rate)"
                        else:
                            return str(r['bb atk%']) + "% damage modifier and drains " + str(
                                r['hp drain% low']) + "~" + str(
                                r['hp drain% high']) + " of damage dealt as HP"
                # ELEMENTAL MITIGATION (16)
                if str(procID) == r['proc id'] == '16':
                    if extraArg == 'fire':
                        if 'mitigate fire attacks (21)' in r:
                            return "Reduces Fire damage by " + str(r['mitigate fire attacks (21)']) + "%"
                        else:
                            return "null"
                    elif extraArg == 'water':
                        if 'mitigate water attacks (22)' in r:
                            return "Reduces Water damage by " + str(r['mitigate water attacks (22)']) + "%"
                        else:
                            return "null"
                    elif extraArg == 'earth':
                        if 'mitigate earth attacks (23)' in r:
                            return "Reduces Earth damage by " + str(r['mitigate earth attacks (23)']) + "%"
                        else:
                            return "null"
                    elif extraArg == 'thunder':
                        if 'mitigate thunder attacks (24)' in r:
                            return "Reduces Thunder damage by " + str(
                                r['mitigate thunder attacks (24)']) + "%"
                        else:
                            return "null"
                    elif extraArg == 'light':
                        if 'mitigate light attacks (25)' in r:
                            return "Reduces Light damage by " + str(r['mitigate light attacks (25)']) + "%"
                        else:
                            return "null"
                    elif extraArg == 'dark':
                        if 'mitigate dark attacks (26)' in r:
                            return "Reduces Dark damage by " + str(r['mitigate dark attacks (26)']) + "%"
                        else:
                            return "null"
                    elif extraArg == 'turns':
                        if r['buff turns'] == 1:
                            return str(r['buff turns']) + " turn"
                        else:
                            return str(r['buff turns']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return "null"
                # STATUS NEGATION
                if str(procID) == r['proc id'] == '17':
                    if extraArg == 'turns':
                        if r['resist status ails turns'] == 1:
                            return str(r['resist status ails turns']) + " turn"
                        else:
                            return str(r['resist status ails turns']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return "Negates all status ailments"
                # NORMAL MITIGATION
                if str(procID) == r['proc id'] == '18':
                    if extraArg == 'turns':
                        if r['dmg% reduction turns (36)'] == 1:
                            return str(r['dmg% reduction turns (36)']) + " turn"
                        else:
                            return str(r['dmg% reduction turns (36)']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return "Reduces damage taken by " + str(r['dmg% reduction']) + "%"
                # GRADUAL BB GAUGE BOOST
                if str(procID) == r['proc id'] == '19':
                    if extraArg == 'turns':
                        if r['increase bb gauge gradual turns (37)'] == 1:
                            return str(r['increase bb gauge gradual turns (37)']) + " turn"
                        else:
                            return str(r['increase bb gauge gradual turns (37)']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return "Boosts BB gauge by " + str(r['increase bb gauge gradual']) + " BC each turn"
                # BB WHEN HIT
                if str(procID) == r['proc id'] == '20':
                    if extraArg == 'turns':
                        if r['bc fill when attacked turns (38)'] == 1:
                            return str(r['bc fill when attacked turns (38)']) + " turn"
                        else:
                            return str(r['bc fill when attacked turns (38)']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    elif int(r['bc fill when attacked%']) != 100:
                        return str(r['bc fill when attacked%']) + "% chance of boosting BB gauge by " + str(
                            r['bc fill when attacked low']) + "~" + str(
                            r['bc fill when attacked high']) + " BC when damage is taken"
                    else:
                        if r['bc fill when attacked low'] == r['bc fill when attacked high']:
                            return "Damage taken boosts BB gauge by " + str(
                                r['bc fill when attacked high']) + " BC"
                        else:
                            return "Damage taken boosts BB gauge by " + str(
                                r['bc fill when attacked low']) + "~" + str(
                                r['bc fill when attacked high']) + " BC"
                # IGNORE DEFENSE
                if str(procID) == r['proc id'] == '22':
                    if extraArg == 'turns':
                        if r['defense% ignore turns (39)'] == 1:
                            return str(r['defense% ignore turns (39)']) + " turn"
                        else:
                            return str(r['defense% ignore turns (39)']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return str(r['defense% ignore']) + "% chance of ignoring Defense"
                # SPARK DAMAGE
                if str(procID) == r['proc id'] == '23':
                    if extraArg == 'turns':
                        if r['buff turns'] == 1:
                            return str(r['buff turns']) + " turn"
                        else:
                            return str(r['buff turns']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return str(r['spark dmg% buff (40)']) + "% boost to Spark damage"
                # PARAMETER CONVERSION
                if str(procID) == r['proc id'] == '24':
                    if extraArg == 'atk':
                        if 'atk% buff (46)' in r:
                            converted = r['converted attribute']
                            if converted == 'hp':
                                converted = 'HP'
                            else:
                                converted = converted.capitalize()
                            return "Boosts Atk relative to " + str(r['atk% buff (46)']) + "% of " + str(
                                converted)
                        else:
                            return "null"
                    elif extraArg == 'def':
                        if 'def% buff (47)' in r:
                            converted = r['converted attribute']
                            if converted == 'hp':
                                converted = 'HP'
                            else:
                                converted = converted.capitalize()
                            return "Boosts Def relative to " + str(r['def% buff (47)']) + "% of " + str(
                                converted)
                        else:
                            return "null"
                    elif extraArg == 'rec':
                        if 'rec% buff (48)' in r:
                            converted = r['converted attribute']
                            if converted == 'hp':
                                converted = 'HP'
                            else:
                                converted = converted.capitalize()
                            return "Boosts Rec relative to " + str(r['rec% buff (48)']) + "% of " + str(
                                converted)
                        else:
                            return "null"
                    elif extraArg == 'turns':
                        if r['% converted turns'] == 1:
                            return str(r['% converted turns']) + " turn"
                        else:
                            return str(r['% converted turns']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return "null"
                # HIT COUNT BOOST
                if str(procID) == r['proc id'] == '26':
                    if extraArg == 'turns':
                        if r['hit increase buff turns (50)'] == 1:
                            return str(r['hit increase buff turns (50)']) + " turn"
                        else:
                            return str(r['hit increase buff turns (50)']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        if 'extra hits dmg%' in r:
                            return "+" + str(r['hit increase/hit']) + " to each normal hit (" + str(
                                int(r['extra hits dmg%'] + 100)) + "% extra hit damage modifier)"
                        else:
                            return "+" + str(r['hit increase/hit']) + " to each normal hit (100% extra hit " \
                                                                      "damage modifier)"
                # PROPORTIONAL DAMAGE
                if str(procID) == r['proc id'] == '27':
                    if extraArg == 'turns':
                        return "—"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        if r['hp% damage high'] == r['hp% damage low']:
                            return str(r['hp% damage chance%']) + "% chance of dealing " + str(
                                r['hp% damage high']) + "% of enemy HP as damage"
                        else:
                            return str(r['bb atk%']) + "% damage modifier, or " + str(
                                r['hp% damage chance%']) + "% chance of dealing " + str(
                                r['hp% damage low']) + "~" + str(
                                r['hp% damage high']) + "% of enemy HP as damage instead"
                # FIXED DAMAGE
                if str(procID) == r['proc id'] == '28':
                    if extraArg == 'turns':
                        return "—"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return "Deals " + str(r['fixed damage']) + " damage"
                # MULTI-ELEMENT DAMAGE
                if str(procID) == r['proc id'] == '29':
                    if extraArg == 'turns':
                        return "—"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        if 'bb crit%' in r:
                            return str(r['bb atk%']) + "% damage modifier (" + str(
                                r['bb crit%']) + "% innate crit rate)"
                        else:
                            return str(r['bb atk%']) + "% damage modifier"
                # ADD ELEMENTS
                if str(procID) == r['proc id'] == '30':
                    if extraArg == 'turns':
                        if r['elements added turns'] == 1:
                            return str(r['elements added turns']) + " turn"
                        else:
                            return str(r['elements added turns']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        elembuffs = r['elements added']
                        output = ""
                        if len(elembuffs) == 6:
                            return "Adds all elements to attacks"
                        elif len(elembuffs) > 2:
                            for elem in elembuffs:
                                if elem != elembuffs[-1]:
                                    output = output + elem.capitalize() + ", "
                                else:
                                    output = output + "and " + elem.capitalize()
                            return "Adds " + output + " elements to attacks"
                        elif len(elembuffs) == 2:
                            return "Adds " + elembuffs[0].capitalize() + " and " + elembuffs[
                                1].capitalize() + " elements to attacks"
                        else:
                            return "Adds " + elembuffs[0].capitalize() + " element to attacks"
                # INSTANT BC FILL
                if str(procID) == r['proc id'] == '31':
                    if extraArg == 'turns':
                        return "—"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return "Boosts BB gauge by " + str(r['increase bb gauge']) + " BC instantly"
                # BB DRAIN
                if str(procID) == r['proc id'] == '34':
                    if extraArg == 'turns':
                        return "—"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        if r['bb gauge% reduction high'] == r['bb gauge% reduction low']:
                            if int(r['bb gauge reduction chance%']) == 100:
                                return "Reduces foe's BB gauge by " + str(
                                    r['bb gauge% reduction high']) + "%"
                            else:
                                return str(
                                    int(r[
                                            'bb gauge reduction chance%'])) + " chance of reducing foe's BB gauge by " + str(
                                    r['bb gauge% reduction high']) + "%"
                        else:
                            if int(r['bb gauge reduction chance%']) == 100:
                                return "Reduces foe's BB gauge by " + str(
                                    r['bb gauge% reduction low']) + "~" + str(
                                    r['bb gauge reduction high']) + "%"
                            else:
                                return str(
                                    int(r[
                                            'bb gauge reduction chance%'])) + " chance of reducing foe's BB gauge by " + str(
                                    r['bb gauge% reduction low']) + "~" + str(
                                    r['bb gauge% reduction high']) + "%"
                # STATUS CURE (NEW)
                if str(procID) == r['proc id'] == '38':
                    if extraArg == 'turns':
                        return "—"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return "Removes all status ailments"
                # ELEMENTAL MITIGATION
                if str(procID) == r['proc id'] == '39':
                    if extraArg == 'fire':
                        if 'mitigate fire attacks' in r:
                            return "Reduces Fire damage by " + str(
                                r['dmg% mitigation for elemental attacks']) + "%"
                        else:
                            return "null"
                    elif extraArg == 'water':
                        if 'mitigate water attacks' in r:
                            return "Reduces Water damage by " + str(
                                r['dmg% mitigation for elemental attacks']) + "%"
                        else:
                            return "null"
                    elif extraArg == 'earth':
                        if 'mitigate earth attacks' in r:
                            return "Reduces Earth damage by " + str(
                                r['dmg% mitigation for elemental attacks']) + "%"
                        else:
                            return "null"
                    elif extraArg == 'thunder':
                        if 'mitigate thunder attacks' in r:
                            return "Reduces Thunder damage by " + str(
                                r['dmg% mitigation for elemental attacks']) + "%"
                        else:
                            return "null"
                    elif extraArg == 'light':
                        if 'mitigate light attacks' in r:
                            return "Reduces Light damage by " + str(
                                r['dmg% mitigation for elemental attacks']) + "%"
                        else:
                            return "null"
                    elif extraArg == 'dark':
                        if 'mitigate dark attacks' in r:
                            return "Reduces Dark damage by " + str(
                                r['dmg% mitigation for elemental attacks']) + "%"
                        else:
                            return "null"
                    elif extraArg == 'turns':
                        if r['dmg% mitigation for elemental attacks buff turns'] == 1:
                            return str(r['dmg% mitigation for elemental attacks buff turns']) + " turn"
                        else:
                            return str(r['dmg% mitigation for elemental attacks buff turns']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return "null"
                # STATUS ADDED TO ATTACKS
                if str(procID) == r['proc id'] == '40' and extraArg in ['curse', 'paralysis', 'poison',
                                                                        'injury', 'sick', 'weaken'] and str(
                    extraArg) + '% buff' in r:
                    if extraArg == 'weaken':
                        return "Added to attack: " + str(
                            r[str(extraArg) + '% buff']) + "% chance of inflicting Weak"
                    else:
                        return "Added to attack: " + str(
                            r[str(extraArg) + '% buff']) + "% chance of inflicting " + extraArg.capitalize()
                if str(procID) == r['proc id'] == '40' and extraArg in ['curse', 'paralysis', 'poison',
                                                                        'injury', 'sick', 'weaken'] and str(
                    extraArg) + '% buff' not in r:
                    return "null"
                if str(procID) == r['proc id'] == '40' and extraArg not in ['curse', 'paralysis', 'poison',
                                                                            'injury', 'sick', 'weaken']:
                    if extraArg == 'turns':
                        if r['buff turns'] == 1:
                            return str(r['buff turns']) + " turn"
                        else:
                            return str(r['buff turns']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return "null"
                # INSTANT OD FILL
                if str(procID) == r['proc id'] == '43':
                    if extraArg == 'turns':
                        return "—"
                    elif extraArg == 'target':
                        return "—"
                    else:
                        if r['target area'] == 'single':
                            return "Fills " + str(int(r['increase od gauge%'])) + "% of the OD gauge"
                        else:
                            return "For each unit alive, fill " + str(
                                int(r['increase od gauge%'])) + "% of the OD gauge"
                # ADDITIONAL DAMAGE
                if str(procID) == r['proc id'] == '44':
                    if extraArg == 'turns':
                        if r['dot turns (71)'] == 1:
                            return str(r['dot turns (71)']) + " turn"
                        else:
                            return str(r['dot turns (71)']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        if 'dot dmg%' in r:
                            return str(r['dot atk%']) + "% DoT modifier with +" + str(
                                r['dot dmg%']) + "% multiplier bonus: " + str(
                                int(((r['dot dmg%'] + 100) / 100) * r['dot atk%'])) + "% DoT modifier total"
                        else:
                            return str(r['dot atk%']) + "% DoT modifier"
                # BB ATK BOOST
                if str(procID) == r['proc id'] == '45':
                    if extraArg == 'turns':
                        if r['buff turns (72)'] == 1:
                            return str(r['buff turns (72)']) + " turn"
                        else:
                            return str(r['buff turns (72)']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return str(r['bb atk% buff']) + "% boost to BB Atk"
                # HP SCALING
                if str(procID) == r['proc id'] == '47':
                    if extraArg == 'turns':
                        return "—"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        if r['bb added atk% proportional to hp'] == 'remaining':
                            if 'bb crit%' in r:
                                return str(r['bb base atk%']) + "% + " + str(
                                    r[
                                        'bb added atk% based on hp']) + "% * (current HP / base max HP) damage modifier (" + str(
                                    r['bb crit%']) + "% innate crit rate)"
                            else:
                                return str(r['bb base atk%']) + "% + " + str(
                                    r[
                                        'bb added atk% based on hp']) + "% * (current HP / base max HP) damage modifier"
                        else:
                            if 'bb crit%' in r:
                                return str(r['bb base atk%']) + "% + " + str(
                                    r[
                                        'bb added atk% based on hp']) + "% * (base max HP / current HP) damage modifier (" + str(
                                    r['bb crit%']) + "% innate crit rate)"
                            else:
                                return str(r['bb base atk%']) + "% + " + str(
                                    r[
                                        'bb added atk% based on hp']) + "% * (base max HP / current HP) damage modifier"
                # PARAMETER REDUCTION ADDED TO ATTACK
                if str(procID) == r['proc id'] == '51':
                    if extraArg == 'turns':
                        if r['buff turns'] == 1:
                            return str(r['buff turns']) + " turn"
                        else:
                            return str(r['buff turns']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    elif extraArg == 'atk':
                        if 'inflict atk% debuff (2)' in r:
                            return "Added to attack: " + str(
                                int(r['inflict atk% debuff chance% (74)'])) + "% chance of reducing " \
                                                                              "Atk by " + str(
                                int(r['inflict atk% debuff (2)'] * -1)) + "%"
                        else:
                            return "null"
                    elif extraArg == 'def':
                        if 'inflict def% debuff (4)' in r:
                            return "Added to attack: " + str(
                                int(r['inflict def% debuff chance% (75)'])) + "% chance of reducing " \
                                                                              "Def by " + str(
                                int(r['inflict def% debuff (4)'] * -1)) + "%"
                        else:
                            return "null"
                    elif extraArg == 'rec':
                        if 'inflict rec% debuff (6)' in r:
                            return "Added to attack: " + str(
                                int(r['inflict rec% debuff chance% (76)'])) + "% chance of reducing " \
                                                                              "Rec by " + str(
                                int(r['inflict rec% debuff (6)'] * -1)) + "%"
                        else:
                            return "null"
                    else:
                        return "null"
                # BC EFFICACY
                if str(procID) == r['proc id'] == '52':
                    if extraArg == 'turns':
                        if r['buff turns (77)'] == 1:
                            return str(r['buff turns (77)']) + " turn"
                        else:
                            return str(r['buff turns (77)']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return str(int(r['bb gauge fill rate% buff'])) + "% boost to BC Efficacy"
                # STATUS COUNTER
                if str(procID) == r['proc id'] == '53':
                    if extraArg == "turns":
                        if r['counter inflict ailment turns'] == 1:
                            return str(r['counter inflict ailment turns']) + " turn"
                        else:
                            return str(r['counter inflict ailment turns']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        if extraArg in ['curse% (82)', 'poison% (78)', 'paralysis% (83)', 'injury% (81)',
                                        'sick% (80)', 'weaken% (79)']:
                            if 'counter inflict ' + str(extraArg) in r:
                                if extraArg == 'curse% (82)':
                                    return str(int(r['counter inflict ' + str(
                                        extraArg)])) + "% chance of inflicting Curse when damage is taken"
                                elif extraArg == 'poison% (78)':
                                    return str(
                                        int(r['counter inflict ' + str(
                                            extraArg)])) + "% chance of inflicting Poison when damage is taken"
                                elif extraArg == 'paralysis% (83)':
                                    return str(
                                        int(r['counter inflict ' + str(
                                            extraArg)])) + "% chance of inflicting Paralysis when damage is taken"
                                elif extraArg == 'injury% (81)':
                                    return str(
                                        int(r['counter inflict ' + str(
                                            extraArg)])) + "% chance of inflicting Injury when damage is taken"
                                elif extraArg == 'sick% (80)':
                                    return str(
                                        int(r['counter inflict ' + str(
                                            extraArg)])) + "% chance of inflicting Sick when damage is taken"
                                elif extraArg == 'weaken% (79)':
                                    return str(
                                        int(r['counter inflict ' + str(
                                            extraArg)])) + "% chance of inflicting Weak when damage is taken"
                                else:
                                    return "null"
                            else:
                                return "null"
                        else:
                            return "null"
                # CRIT DAMAGE
                if str(procID) == r['proc id'] == '54':
                    if extraArg == "turns":
                        if r['buff turns (84)'] == 1:
                            return str(r['buff turns (84)']) + " turn"
                        else:
                            return str(r['buff turns (84)']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return str(int(r['crit multiplier%'])) + "% boost to critical damage"
                # ELEMENTAL DAMAGE
                if str(procID) == r['proc id'] == '55':
                    if extraArg == "turns":
                        if r['elemental weakness buff turns'] == 1:
                            return str(r['elemental weakness buff turns']) + " turn"
                        else:
                            return str(r['elemental weakness buff turns']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        if str(extraArg) + ' units do extra elemental weakness dmg' in r:
                            return str(int(r['elemental weakness multiplier%'])) + "% boost to " + str(
                                extraArg).capitalize() + " elemental damage"
                        else:
                            return "null"
                # CHANCE ANGEL IDOL
                if str(procID) == r['proc id'] == '56':
                    if extraArg == "turns":
                        if r['angel idol buff turns (91)'] == 1:
                            return str(r['angel idol buff turns (91)']) + " turn"
                        else:
                            return str(r['angel idol buff turns (91)']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        if 'angel idol recover hp%' in r:
                            return str(int(r[
                                               'angel idol recover chance%'])) + "% chance of resisting 1 KO, restores " + str(
                                r['angel idol recover hp%']) + "% of unit's HP"
                        else:
                            return str(int(r['angel idol recover chance%'])) + "% chance of resisting 1 KO"
                # SPARK VULNERABILITY
                if str(procID) == r['proc id'] == '58':
                    if extraArg == "turns":
                        if r['spark dmg received debuff turns (94)'] == 1:
                            return str(r['spark dmg received debuff turns (94)']) + " turn"
                        else:
                            return str(r['spark dmg received debuff turns (94)']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        if r['spark dmg received apply%'] == 100:
                            return "Inflicts " + str(r['spark dmg% received']) + "% spark vulnerability"
                        else:
                            return str(
                                int(r['spark dmg received apply%'])) + "% chance of inflicting " + str(
                                r['spark dmg% received']) + "% spark vulnerability"
                # BB SCALING
                if str(procID) == r['proc id'] == '61':
                    if extraArg == 'turns':
                        return "—"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return str(r['bb base atk%']) + "% + " + str(int(
                            r[
                                'bb max atk% based on ally bb gauge and clear bb gauges'] / 5)) + "% * (number of filled gauges)"
                # BARRIER
                if str(procID) == r['proc id'] == '62':
                    if extraArg == "turns":
                        return "—"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        if extraArg == r['elemental barrier element']:
                            return "Activates " + extraArg.capitalize() + " barrier with " + str(
                                r['elemental barrier hp']) + " HP"
                        else:
                            return "null"
                # CONSECUTIVE DAMAGE
                if str(procID) == r['proc id'] == '64':
                    if extraArg == "turns":
                        return "—"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        extraPropStr = ""
                        extraPropArr = []
                        if 'bb crit%' in r:
                            extraPropArr.append(str(r['bb crit%']) + "% innate crit rate")
                        if 'bb bc%' in r:
                            extraPropArr.append(str(r['bb bc%']) + "% innate BC drop rate")
                        if 'bb hc%' in r:
                            extraPropArr.append(str(r['bb hc%']) + "% innate HC drop rate")
                        if len(extraPropArr) == 3:
                            return str(r['bb base atk%']) + "% + " + str(
                                r['bb atk% inc per use']) + "% * (number of consecutive uses, max " + str(
                                r['bb atk% max number of inc']) + " times) damage modifier (" + \
                                   extraPropArr[0] + ", " + extraPropArr[
                                       1] + " and " + extraPropArr[2] + ")"
                        elif len(extraPropArr) == 2:
                            return str(r['bb base atk%']) + "% + " + str(
                                r['bb atk% inc per use']) + "% * (number of consecutive uses, max " + str(
                                r['bb atk% max number of inc']) + " times) damage modifier (" + \
                                   extraPropArr[0] + " and " + extraPropArr[
                                       1] + ")"
                        elif len(extraPropArr) == 1:
                            return str(r['bb base atk%']) + "% + " + str(
                                r['bb atk% inc per use']) + "% * (number of consecutive uses, max " + str(
                                r['bb atk% max number of inc']) + " times) damage modifier (" + \
                                   extraPropArr[0] + ")"
                        else:
                            return str(r['bb base atk%']) + "% + " + str(
                                r['bb atk% inc per use']) + "% * (number of consecutive uses, max " + str(
                                r['bb atk% max number of inc']) + " times) damage modifier"
                # ATK ON STATUS ENEMY
                if str(procID) == r['proc id'] == '65':
                    if extraArg == "turns":
                        if r['atk% buff turns (110)'] == 1:
                            return str(r['atk% buff turns (110)']) + " turn"
                        else:
                            return str(r['atk% buff turns (110)']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return str(r[
                                       'atk% buff when enemy has ailment']) + "% boost to Atk when enemy is status afflicted"
                # REVIVE
                if str(procID) == r['proc id'] == '66':
                    if extraArg == "turns":
                        return "—"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return str(int(r['revive unit chance%'])) + "% chance of reviving with " + str(
                            r['revive unit hp%']) + "% HP"
                # BC ON SPARK
                if str(procID) == r['proc id'] == '67':
                    if extraArg == "turns":
                        if r['bc fill on spark buff turns (111)'] == 1:
                            return str(r['bc fill on spark buff turns (111)']) + " turn"
                        else:
                            return str(r['bc fill on spark buff turns (111)']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        if r['bc fill on spark%'] == 100:
                            if r['bc fill on spark low'] == r['bc fill on spark high']:
                                return "Fills " + str(r['bc fill on spark high']) + " BC per spark"
                            else:
                                return "Fills " + str(r['bc fill on spark low']) + "~" + str(
                                    r['bc fill on spark high']) + " BC per spark"
                        else:
                            if r['bc fill on spark low'] == r['bc fill on spark high']:
                                return str(r['bc fill on spark%']) + "% chance of filling " + str(
                                    r['bc fill on spark high']) + " BC per spark"
                            else:
                                return str(r['bc fill on spark%']) + "% chance of filling " + str(
                                    r['bc fill on spark low']) + "~" + str(
                                    r['bc fill on spark high']) + " BC per spark"
                # GUARD MITIGATION
                if str(procID) == r['proc id'] == '68':
                    if extraArg == "turns":
                        if r['guard increase mitigation buff turns (113)'] == 1:
                            return str(r['guard increase mitigation buff turns (113)']) + " turn"
                        else:
                            return str(r['guard increase mitigation buff turns (113)']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return "Reduces damage taken by " + str(
                            r['guard increase mitigation%']) + "% when guarding"
                # BC ON GUARD
                if str(procID) == r['proc id'] == '69':
                    if extraArg == "turns":
                        if r['bb bc fill on guard buff turns (114)'] == 1:
                            return str(r['bb bc fill on guard buff turns (114)']) + " turn"
                        else:
                            return str(r['bb bc fill on guard buff turns (114)']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return "Fills " + str(r['bb bc fill on guard']) + " BC upon guarding"
                # BC FILL RATE DEBUFF
                if str(procID) == r['proc id'] == '71':
                    if extraArg == "turns":
                        if r['bb fill inc buff turns (112)'] == 1:
                            return str(r['bb fill inc buff turns (112)']) + " turn"
                        else:
                            return str(r['bb fill inc buff turns (112)']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return "Reduces BC efficacy by " + str(int(r['bb fill inc%'] * -1)) + "%"
                # PARAMETER REDUCTION NEGATION
                if str(procID) == r['proc id'] == '73':
                    if extraArg == 'turns':
                        if r['stat down immunity buff turns'] == 1:
                            return str(r['stat down immunity buff turns']) + " turn"
                        else:
                            return str(r['stat down immunity buff turns']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return "Negates Atk, Def, and Rec reduction effects"
                # ELEMENT SQUAD-SCALED DAMAGE
                if str(procID) == r['proc id'] == '75':
                    if extraArg == 'turns':
                        return "—"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return str(r['atk% buff (1)']) + "% + " + str(
                            r['def% buff (3)']) + "% * (number of " + str(r[
                                                                              'counted element for buff multiplier']).capitalize() + " units in party, up to 2 maximum) damage modifier"
                # EXTRA ACTION
                if str(procID) == r['proc id'] == '76':
                    if extraArg == 'turns':
                        if r['extra action buff turns (123)'] == 1:
                            return str(r['extra action buff turns (123)']) + " turn"
                        else:
                            return str(r['extra action buff turns (123)']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        if r['max number of extra actions'] == 1:
                            return str(r['chance% for extra action']) + "% chance of acting " + str(
                                r['max number of extra actions']) + " extra time"
                        else:
                            return str(r['chance% for extra action']) + "% chance of acting " + str(
                                r['max number of extra actions']) + " extra times"
                # SELF PARAMETER BOOST
                if str(procID) == r['proc id'] == '78':
                    if extraArg == 'turns':
                        if r['self stat buff turns'] == 1:
                            return str(r['self stat buff turns']) + " turn"
                        else:
                            return str(r['self stat buff turns']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        if extraArg == 'atk':
                            if 'self atk% buff' in r:
                                return str(r['self atk% buff']) + "% boost to own Atk"
                            else:
                                return "null"
                        elif extraArg == 'def':
                            if 'self def% buff' in r:
                                return str(r['self def% buff']) + "% boost to own Def"
                            else:
                                return "null"
                        elif extraArg == 'rec':
                            if 'self rec% buff' in r:
                                return str(r['self rec% buff']) + "% boost to own Rec"
                            else:
                                return "null"
                        elif extraArg == 'crit':
                            if 'self crit% buff' in r:
                                return str(r['self crit% buff']) + "% boost to own critical rate"
                            else:
                                return "null"
                        else:
                            return "null"
                # SPARK CRITICAL
                if str(procID) == r['proc id'] == '83':
                    if extraArg == 'turns':
                        if r['spark dmg inc buff turns (131)'] == 1:
                            return str(r['spark dmg inc buff turns (131)']) + " turn"
                        else:
                            return str(r['spark dmg inc buff turns (131)']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return str(r['spark dmg inc chance%']) + "% chance of dealing " + str(
                            r['spark dmg inc% buff']) + "% extra spark damage"
                # OD GAUGE FILL RATE
                if str(procID) == r['proc id'] == '84':
                    if extraArg == 'turns':
                        if r['od fill rate buff turns (132)'] == 1:
                            return str(r['od fill rate buff turns (132)']) + " turn"
                        else:
                            return str(r['od fill rate buff turns (132)']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return str(r['od fill rate% buff']) + "% boost to OD fill rate"
                # HP WHEN HIT
                if str(procID) == r['proc id'] == '85':
                    if extraArg == 'turns':
                        if r['hp recover from dmg buff turns (133)'] == 1:
                            return str(r['hp recover from dmg buff turns (133)']) + " turn"
                        else:
                            return str(r['hp recover from dmg buff turns (133)']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        if r['hp recover from dmg% low'] == r['hp recover from dmg% high']:
                            return str(r['hp recover from dmg chance']) + "% chance of recovering " + str(
                                r['hp recover from dmg% high']) + "% of damage taken as HP"
                        else:
                            return str(r['hp recover from dmg chance']) + "% chance of recovering " + str(
                                r['hp recover from dmg% low']) + "~" + str(
                                r['hp recover from dmg% high']) + "% of damage taken as HP"
                # HP ABSORPTION
                if str(procID) == r['proc id'] == '86':
                    if extraArg == 'turns':
                        if r['hp drain buff turns (134)'] == 1:
                            return str(r['hp drain buff turns (134)']) + " turn"
                        else:
                            return str(r['hp drain buff turns (134)']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        if r['hp drain chance%'] == 100:
                            return "Recovers " + str(r['hp drain% low']) + "~" + str(
                                r['hp drain% high']) + " damage dealt as HP"
                        else:
                            return str(r['hp drain chance%']) + "% chance of recovering " + str(
                                r['hp drain% low']) + "~" + str(r['hp drain% high']) + " damage dealt as HP"
                # HP ON SPARK
                if str(procID) == r['proc id'] == '87':
                    if extraArg == 'turns':
                        if r['spark recover hp buff turns (135)'] == 1:
                            return str(r['spark recover hp buff turns (135)']) + " turn"
                        else:
                            return str(r['spark recover hp buff turns (135)']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        if r['spark recover hp chance%'] == 100:
                            return "Recovers " + str(r['spark recover hp low']) + "~" + str(
                                r['spark recover hp high']) + " HP per spark"
                        else:
                            return str(r['spark recover hp chance%']) + "% chance of recovering " + str(
                                r['spark recover hp low']) + "~" + str(
                                r['spark recover hp high']) + " HP per spark"
                # SELF SPARK BOOST
                if str(procID) == r['proc id'] == '88':
                    if extraArg == 'turns':
                        if r['spark dmg inc% turns (136)'] == 1:
                            return str(r['spark dmg inc% turns (136)']) + " turn"
                        else:
                            return str(r['spark dmg inc% turns (136)']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return str(r['spark dmg inc%']) + "% boost to own Spark damage"
                # CRIT/EWD/SPARK RESIST
                if str(procID) == r['proc id'] == '93':
                    if extraArg == 'turns':
                        if r['dmg resist turns'] == 1:
                            return str(r['dmg resist turns']) + " turn"
                        else:
                            return str(r['dmg resist turns']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        if extraArg == 'crit' and 'crit dmg buffed damage resist% (143)' in r:
                            if r['crit dmg buffed damage resist% (143)'] == 100:
                                return "Negates critical damage"
                            else:
                                return str(r[
                                               'crit dmg buffed damage resist% (143)']) + "% resistance to critical damage"
                        elif extraArg == 'ewd' and 'strong buffed element damage resist% (144)' in r:
                            if r['strong buffed element damage resist% (144)'] == 100:
                                return "Negates elemental damage"
                            else:
                                return str(r[
                                               'strong buffed element damage resist% (144)']) + "% resistance to elemental damage"
                        elif extraArg == 'spark' and 'spark dmg buffed resist% (145)' in r:
                            if r['spark dmg buffed resist% (145)'] == 100:
                                return "Negates spark damage"
                            else:
                                return str(
                                    r['spark dmg buffed resist% (145)']) + "% resistance to spark damage"
                        else:
                            return "null"
                # AOE NORMAL ATTACK
                if str(procID) == r['proc id'] == '94':
                    if extraArg == 'turns':
                        return "3 turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        if 'aoe atk inc%' in r:
                            if r['aoe atk inc%'] == 0:
                                return str(r[
                                               'chance to aoe']) + "% chance of attacking all enemies with normal attack"
                            else:
                                return str(r[
                                               'chance to aoe']) + "% chance of attacking all enemies with normal attack (" + str(
                                    r['aoe atk inc%']) + "% AoE damage modifier)"
                        else:
                            return str(
                                r['chance to aoe']) + "% chance of attacking all enemies with normal attack"
                # ELEMENT TARGET DAMAGE
                if str(procID) == r['proc id'] == '97':
                    if extraArg == 'turns':
                        return "—"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        if 'bb crit%' in r:
                            return str(r['bb atk%']) + "% damage modifier (" + str(
                                r['bb crit%']) + "% innate crit rate)"
                        else:
                            return str(r['bb atk%']) + "% damage modifier"
                # GRADUAL OD FILL
                if str(procID) == r['proc id'] == '113':
                    if extraArg == 'turns':
                        if r['od fill turns (148)'] == 1:
                            return str(r['od fill turns (148)']) + " turn"
                        else:
                            return str(r['od fill turns (148)']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return "Fills " + str(r['od fill']) + " OD points at the end of each turn"
                # PARAMETER REDUCTION COUNTER
                if str(procID) == r['proc id'] == '130':
                    if extraArg == 'turns':
                        if r['buff turns'] == 1:
                            return str(r['buff turns']) + " turn"
                        else:
                            return str(r['buff turns']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        if extraArg == 'atk':
                            if 'atk% buff (153)' in r:
                                if r['debuff turns'] == 1:
                                    return "Damage taken has a " + str(
                                        r['atk buff chance%']) + "% chance of inflicting " + str(
                                        int(r['atk% buff (153)'] * -1)) + "% Atk reduction for 1 turn"
                                else:
                                    return "Damage taken has a " + str(
                                        r['atk buff chance%']) + "% chance of inflicting " + str(
                                        int(r['atk% buff (153)'] * -1)) + "% Atk reduction for " + str(
                                        r['debuff turns']) + " turns"
                            else:
                                return "null"
                        elif extraArg == 'def':
                            if 'def% buff (154)' in r:
                                if r['debuff turns'] == 1:
                                    return "Damage taken has a " + str(
                                        r['def buff chance%']) + "% chance of inflicting " + str(
                                        int(r['def% buff (154)'] * -1)) + "% Def reduction for 1 turn"
                                else:
                                    return "Damage taken has a " + str(
                                        r['def buff chance%']) + "% chance of inflicting " + str(
                                        int(r['def% buff (154)'] * -1)) + "% Def reduction for " + str(
                                        r['debuff turns']) + " turns"
                            else:
                                return "null"
                        elif extraArg == 'rec':
                            if 'rec% buff (155)' in r:
                                if r['debuff turns'] == 1:
                                    return "Damage taken has a " + str(
                                        r['rec buff chance%']) + "% chance of inflicting " + str(
                                        int(r['rec% buff (155)'] * -1)) + "% Rec reduction for 1 turn"
                                else:
                                    return "Damage taken has a " + str(
                                        r['def buff chance%']) + "% chance of inflicting " + str(
                                        int(r['rec% buff (155)'] * -1)) + "% Rec reduction for " + str(
                                        r['debuff turns']) + " turns"
                            else:
                                return "null"
                        else:
                            return "null"
                # CRIT/EWD VULNERABILITY
                if str(procID) == r['proc id'] == '132':
                    if extraArg == 'turns':
                        if r['vuln turns'] == 1:
                            return str(r['vuln turns']) + " turn"
                        else:
                            return str(r['vuln turns']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        if extraArg == "ewd" and 'elemental vuln dmg% (158)' in r:
                            if r['elemental vuln chance%'] == 100:
                                return "Inflicts " + str(
                                    r['elemental vuln dmg% (158)']) + "% elemental vulnerability"
                            else:
                                return str(
                                    int(r['elemental vuln chance%'])) + "% chance of inflicting " + str(
                                    r['elemental vuln dmg% (158)']) + "% elemental vulnerability"
                        elif extraArg == "crit" and 'crit vuln dmg% (157)' in r:
                            if r['crit vuln chance%'] == 100:
                                return "Inflicts " + str(
                                    r['crit vuln dmg% (157)']) + "% critical vulnerability"
                            else:
                                return str(int(r['crit vuln chance%'])) + "% chance of inflicting " + str(
                                    r['crit vuln dmg% (157)']) + "% critical vulnerability"
                        else:
                            return "null"
                # TAUNT
                if str(procID) == r['proc id'] == '10000':
                    if extraArg == 'turns':
                        if r['taunt turns (10000)'] == 1:
                            return str(r['taunt turns (10000)']) + " turn"
                        else:
                            return str(r['taunt turns (10000)']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        tauntList = []
                        tauntStr = ""
                        if 'atk% buff' in r:
                            tauntList.append("Atk by " + str(r['atk% buff']) + "%")
                        if 'def% buff' in r:
                            tauntList.append("Def by " + str(r['def% buff']) + "%")
                        if 'rec% buff' in r:
                            tauntList.append("Rec by " + str(r['rec% buff']) + "%")
                        if 'crit% buff' in r:
                            tauntList.append("critical rate by " + str(r['crit% buff']) + "%")
                        if len(tauntList) == 2:
                            tauntStr = tauntList[0] + " and " + tauntList[1]
                        elif len(tauntList) > 2:
                            for a in range(0, len(tauntList) - 1):
                                tauntStr = tauntStr + tauntList[a] + ", "
                            tauntStr = tauntStr + "and " + tauntList[len(tauntList) - 1]
                        elif len(tauntList) == 1:
                            tauntStr = tauntList[0]
                        else:
                            return "null"
                        return "Activates Taunt, also boosts " + tauntStr
                # STEALTH
                if str(procID) == r['proc id'] == '10001':
                    if extraArg == 'turns':
                        if r['stealth turns (10001)'] == 1:
                            return str(r['stealth turns (10001)']) + " turn"
                        else:
                            return str(r['stealth turns (10001)']) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        stealthList = []
                        stealthStr = ""
                        if 'atk% buff' in r:
                            stealthList.append("Atk by " + str(r['atk% buff']) + "%")
                        if 'def% buff' in r:
                            stealthList.append("Def by " + str(r['def% buff']) + "%")
                        if 'rec% buff' in r:
                            stealthList.append("Rec by " + str(r['rec% buff']) + "%")
                        if 'crit% buff' in r:
                            stealthList.append("critical rate by " + str(r['crit% buff']) + "%")
                        if len(stealthList) == 2:
                            stealthStr = stealthList[0] + " and " + stealthList[1]
                        elif len(stealthList) > 2:
                            for a in range(0, len(stealthList) - 1):
                                stealthStr = stealthStr + stealthList[a] + ", "
                            stealthStr = stealthStr + "and " + stealthList[len(stealthList) - 1]
                        elif len(stealthList) == 1:
                            stealthStr = stealthList[0]
                        else:
                            return "null"
                        return "Activates Stealth, also boosts " + stealthStr
                # NEGATIVE HP SCALING
                if str(procID) == r['proc id'] == '11000':
                    if extraArg == 'turns':
                        return "—"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        if 'bb crit%' in r:
                            return str(r['bb base atk%']) + "% + " + str(
                                r[
                                    'bb added atk% based on hp']) + "% * (percentage of HP lost) damage modifier (" + str(
                                r['bb crit%']) + "% innate crit rate)"
                        else:
                            return str(r['bb base atk%']) + "% + " + str(
                                r[
                                    'bb added atk% based on hp']) + "% * (percentage of HP lost) damage modifier"
            # UNKNOWN
            else:
                # SELF CONVERSION
                if str(procID) == r['unknown proc id'] == '89':
                    params = r['unknown proc param'].split(',')
                    stats = ['Atk', 'Def', 'Rec', 'HP']
                    if extraArg == 'turns':
                        if params[4] == '1':
                            return str(params[4]) + " turn"
                        else:
                            return str(params[4]) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        if extraArg == 'atk':
                            if params[1] != '0':
                                return "Boosts own Atk relative to " + str(params[1]) + "% of " + str(
                                    stats[int(params[0]) - 1])
                            else:
                                return "null"
                        elif extraArg == 'def':
                            if params[2] != '0':
                                return "Boosts own Def relative to " + str(params[2]) + "% of " + str(
                                    stats[int(params[0]) - 1])
                            else:
                                return "null"
                        elif extraArg == 'rec':
                            if params[3] != '0':
                                return "Boosts own Rec relative to " + str(params[3]) + "% of " + str(
                                    stats[int(params[0]) - 1])
                            else:
                                return "null"
                        else:
                            return "null"
                # SELF MAX HP BOOST
                if str(procID) == r['unknown proc id'] == '92':
                    params = r['unknown proc param'].split(',')
                    if extraArg == 'turns':
                        return "—"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return str(params[1]) + "% boost to own HP"
                # DOT MITIGATION
                if str(procID) == r['unknown proc id'] == '126':
                    params = r['unknown proc param'].split(',')
                    if extraArg == 'turns':
                        if params[1] == '1':
                            return str(params[1]) + " turn"
                        else:
                            return str(params[1]) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return "Reduces DoT damage by " + str(params[0]) + "%"
                # EVASION
                if str(procID) == r['unknown proc id'] == '10007':
                    params = r['unknown proc param'].split(',')
                    if extraArg == 'turns':
                        if params[1] == '1':
                            return str(params[1]) + " turn"
                        else:
                            return str(params[1]) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return str(params[3]) + "% chance of evading hits from an attack"
                # ELEMENTAL SPARK BOOST
                if str(procID) == r['unknown proc id'] == '10015':
                    params = r['unknown proc param'].split(',')
                    if extraArg == 'turns':
                        if params[1] == '1':
                            return str(params[1]) + " turn"
                        else:
                            return str(params[1]) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        if extraArg == 'fire' and str(params[3]) == '1':
                            return str(int(float(params[0]))) + "% boost to spark damage of Fire units"
                        elif extraArg == 'water' and str(params[3]) == '2':
                            return str(int(float(params[0]))) + "% boost to spark damage of Water units"
                        elif extraArg == 'earth' and str(params[3]) == '3':
                            return str(int(float(params[0]))) + "% boost to spark damage of Earth units"
                        elif extraArg == 'thunder' and str(params[3]) == '4':
                            return str(int(float(params[0]))) + "% boost to spark damage of Thunder units"
                        elif extraArg == 'light' and str(params[3]) == '5':
                            return str(int(float(params[0]))) + "% boost to spark damage of Light units"
                        elif extraArg == 'dark' and str(params[3]) == '6':
                            return str(int(float(params[0]))) + "% boost to spark damage of Dark units"
                        else:
                            return "null"
                # ELEMENTAL CRIT BOOST
                if str(procID) == r['unknown proc id'] == '10016':
                    params = r['unknown proc param'].split(',')
                    if extraArg == 'turns':
                        if params[1] == '1':
                            return str(params[1]) + " turn"
                        else:
                            return str(params[1]) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        if extraArg == 'fire' and str(params[3]) == '1':
                            return str(
                                int(float(params[0]) * 100)) + "% boost to critical damage of Fire units"
                        elif extraArg == 'water' and str(params[3]) == '2':
                            return str(
                                int(float(params[0]) * 100)) + "% boost to critical damage of Water units"
                        elif extraArg == 'earth' and str(params[3]) == '3':
                            return str(
                                int(float(params[0]) * 100)) + "% boost to critical damage of Earth units"
                        elif extraArg == 'thunder' and str(params[3]) == '4':
                            return str(
                                int(float(params[0]) * 100)) + "% boost to critical damage of Thunder units"
                        elif extraArg == 'light' and str(params[3]) == '5':
                            return str(
                                int(float(params[0]) * 100)) + "% boost to critical damage of Light units"
                        elif extraArg == 'dark' and str(params[3]) == '6':
                            return str(
                                int(float(params[0]) * 100)) + "% boost to critical damage of Dark units"
                        else:
                            return "null"
                # ELEMENTAL SHIELD
                if str(procID) == r['unknown proc id'] == '10017':
                    params = r['unknown proc param'].split(',')
                    if extraArg == 'turns':
                        if params[1] == '1':
                            return str(params[3]) + " turn"
                        else:
                            return str(params[3]) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        if extraArg == 'fire' and str(params[0]) == '1':
                            return "Activates Fire Shield (" + str(params[1]) + " HP & " + str(
                                params[2]) + " Def)"
                        elif extraArg == 'water' and str(params[0]) == '2':
                            return "Activates Water Shield (" + str(params[1]) + " HP & " + str(
                                params[2]) + " Def)"
                        elif extraArg == 'earth' and str(params[0]) == '3':
                            return "Activates Earth Shield (" + str(params[1]) + " HP & " + str(
                                params[2]) + " Def)"
                        elif extraArg == 'thunder' and str(params[0]) == '4':
                            return "Activates Thunder Shield (" + str(params[1]) + " HP & " + str(
                                params[2]) + " Def)"
                        elif extraArg == 'light' and str(params[0]) == '5':
                            return "Activates Light Shield (" + str(params[1]) + " HP & " + str(
                                params[2]) + " Def)"
                        elif extraArg == 'dark' and str(params[0]) == '6':
                            return "Activates Dark Shield (" + str(params[1]) + " HP & " + str(
                                params[2]) + " Def)"
                        else:
                            return "null"
                # MAX HP REDUCTION
                if str(procID) == r['unknown proc id'] == '10018':
                    params = r['unknown proc param'].split(',')
                    if extraArg == 'turns':
                        if params[1] == '1':
                            return str(params[1]) + " turn"
                        else:
                            return str(params[1]) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return "Reduces max HP by " + str(params[0]) + "%"
                # EFFECT PURGE
                if str(procID) == r['unknown proc id'] == '10019':
                    params = r['unknown proc param'].split(',')
                    if extraArg == 'turns':
                        return "—"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        purgeStr = ""
                        purgeArr = []
                        for a in range(0, 9):
                            if effectMap[params[a]] != 'null':
                                purgeArr.append(effectMap[params[a]])
                        if len(purgeArr) > 2:
                            for b in range(0, len(purgeArr)):
                                if b == len(purgeArr) - 1:
                                    purgeStr = purgeStr + "and " + purgeArr[b]
                                else:
                                    purgeStr = purgeStr + purgeArr[b] + ", "
                        elif len(purgeArr) == 2:
                            purgeStr = purgeArr[0] + " and " + purgeArr[1]
                        elif len(purgeArr) == 1:
                            purgeStr = purgeArr[0]
                        else:
                            purgeStr = "N/A"
                        if str(params[9]) == '100':
                            return "Purges effects: " + purgeStr
                        else:
                            return str(params[9]) + "% chance of purging effects: " + purgeStr
                # PIERCING DAMAGE
                if str(procID) == r['unknown proc id'] == '10020':
                    params = r['unknown proc param'].split(',')
                    if extraArg == 'turns':
                        return "—"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        pierceArr = []
                        pierceStr = ""
                        elementArr = ['Fire', 'Water', 'Earth', 'Thunder', 'Light', 'Dark']
                        for a in range(3, 9):
                            if params[a] == '1':
                                pierceArr.append(elementArr[a - 3])
                        if len(pierceArr) > 2:
                            for b in range(0, len(pierceArr) - 1):
                                pierceStr = pierceStr + pierceArr[b] + ", "
                            pierceStr = pierceStr + "and " + pierceArr[b]
                        elif len(pierceArr) == 2:
                            pierceStr = pierceArr[0] + " and " + pierceArr[1]
                        elif len(pierceArr) == 1:
                            pierceStr = pierceArr[0]
                        else:
                            pierceStr = "N/A"
                        return str(params[0]) + "% damage modifier, deals " + str(
                            params[2]) + "% piercing damage against " + str(pierceStr) + " enemies"
                # ACTIVE HEALING REDUCTION
                if str(procID) == r['unknown proc id'] == '10021':
                    params = r['unknown proc param'].split(',')
                    if extraArg == 'turns':
                        if params[1] == '1':
                            return str(params[1]) + " turn"
                        else:
                            return str(params[1]) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return "Reduces active healing effects by " + str(params[0]) + "%"
                # PASSIVE HEALING REDUCTION
                if str(procID) == r['unknown proc id'] == '10022':
                    params = r['unknown proc param'].split(',')
                    if extraArg == 'turns':
                        if params[1] == '1':
                            return str(params[1]) + " turn"
                        else:
                            return str(params[1]) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return "Reduces passive healing effects by " + str(params[0]) + "%"
                # HC HEALING REDUCTION
                if str(procID) == r['unknown proc id'] == '10023':
                    params = r['unknown proc param'].split(',')
                    if extraArg == 'turns':
                        if params[1] == '1':
                            return str(params[1]) + " turn"
                        else:
                            return str(params[1]) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return "Reduces HC efficacy effects by " + str(params[0]) + "%"
                # KO RESISTANCE NEGATION
                if str(procID) == r['unknown proc id'] == '10025':
                    params = r['unknown proc param'].split(',')
                    if extraArg == 'turns':
                        if params[2] == '1':
                            return str(params[2]) + " turn"
                        else:
                            return str(params[2]) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return str(params[1]) + "% chance of negating KO Resistance effects"
                # RECAST
                if str(procID) == r['unknown proc id'] == '70002':
                    params = r['unknown proc param'].split(',')
                    if extraArg == 'turns':
                        if params[1] == '1':
                            return str(params[1]) + " turn"
                        else:
                            return str(params[1]) + " turns"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return str(int(float(params[0]) * 100)) + "% chance of recasting BB/SBB/UBB"
