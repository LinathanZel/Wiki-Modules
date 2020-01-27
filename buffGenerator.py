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
filename = "unit.json.txt"
datamine_url = "https://raw.githubusercontent.com/Deathmax/bravefrontier_data/master/info.json"
errors = 0
globalArr=[]
arrCount=0

data={}
try:
    #print("Attempting to load file data from " + filename + "...")
    with open(filename) as data_file:
        data = json.load(data_file)
    #print("Success loading file data!")
except FileNotFoundError:
    print("Failure to load file data. Attempting online datamine...")
    try:
        with urlopen(datamine_url) as url:
            data = json.loads(url.read().decode())
        saveInfo(data,filename)
        print("Success loading datamine!")
    except HTTPError:
        print("Failure to load datamine...")
        units = {}


def update():
    try:
        print("Attempting Update...")
        with urlopen(datamine_url) as url:
            data1 = json.loads(url.read().decode())
        print("Unit info updated")
        print("Saving files...")
        saveInfo(data1, filename)
        data = data1
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
            return "All enemies"
        else:
            return "Single enemy"
    elif r['target type'] == 'party':
        if r['target area'] == 'aoe':
            return "All allies"
        else:
            return "Single ally"
    elif r['target type'] == '100':
        return "All enemies (PvP modes only)"
    else:
        return "To self"


def searchBuffs(unitID, skill, procID, extraArg):
    global errors
    arrCount = -1
    for r in data[str(unitID)][str(skill)]['levels'][-1]['effects']:
        arrCount = arrCount + 1
        if globalArr[arrCount] != 1:
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
                            return str(r['bb atk%']) + "% damage modifier (" + extraPropArr[0] + ", " + extraPropArr[1] + " and " + extraPropArr[2] + ")"
                        elif len(extraPropArr) == 2:
                            return str(r['bb atk%']) + "% damage modifier (" + extraPropArr[0] + " and " + extraPropArr[
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
                        return "Heals " + str(r['gradual heal low']) + "~" + str(r['gradual heal high']) + " + " + str(
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
                                return str(int(r['buff #1']['proc chance%'])) + "% chance of reducing Atk by " + str(
                                    int(r['buff #1']['atk% buff (2)'] * -1)) + "%"
                            elif 'atk% buff (2)' in r['buff #2']:
                                return str(int(r['buff #2']['proc chance%'])) + "% chance of reducing Atk by " + str(
                                    int(r['buff #2']['atk% buff (2)'] * -1)) + "%"
                            else:
                                return "null"
                        elif 'buff #1' in r and 'buff #2' not in r:
                            if 'atk% buff (2)' in r['buff #1']:
                                return str(int(r['buff #1']['proc chance%'])) + "% chance of reducing Atk by " + str(
                                    int(r['buff #1']['atk% buff (2)'] * -1)) + "%"
                            else:
                                return "null"
                        else:
                            return "null"
                    elif extraArg == 'def':
                        if 'buff #1' in r and 'buff #2' in r:
                            if 'def% buff (4)' in r['buff #1']:
                                return str(int(r['buff #1']['proc chance%'])) + "% chance of reducing Def by " + str(
                                    int(r['buff #1']['def% buff (4)'] * -1)) + "%"
                            elif 'def% buff (4)' in r['buff #2']:
                                return str(int(r['buff #2']['proc chance%'])) + "% chance of reducing Def by " + str(
                                    int(r['buff #2']['def% buff (4)'] * -1)) + "%"
                            else:
                                return "null"
                        elif 'buff #1' in r and 'buff #2' not in r:
                            if 'def% buff (4)' in r['buff #1']:
                                return str(int(r['buff #1']['proc chance%'])) + "% chance of reducing Def by " + str(
                                    int(r['buff #1']['def% buff (4)'] * -1)) + "%"
                            else:
                                return "null"
                        else:
                            return "null"
                    elif extraArg == 'rec':
                        if 'buff #1' in r and 'buff #2' in r:
                            if 'rec% buff (6)' in r['buff #1']:
                                return str(int(r['buff #1']['proc chance%'])) + "% chance of reducing Rec by " + str(
                                    int(r['buff #1']['rec% buff (6)'] * -1)) + "%"
                            elif 'rec% buff (6)' in r['buff #2']:
                                return str(int(r['buff #2']['proc chance%'])) + "% chance of reducing Rec by " + str(
                                    int(r['buff #2']['rec% buff (6)'] * -1)) + "%"
                            else:
                                return "null"
                        elif 'buff #1' in r and 'buff #2' not in r:
                            if 'rec% buff (6)' in r['buff #1']:
                                return str(int(r['buff #1']['proc chance%'])) + "% chance of reducing Rec by " + str(
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
                                        int(r[str(extraArg) + "%"])) + "% chance of inflicting " + extraArg.capitalize()
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
                            return str(r['bb atk%']) + "% damage modifier (" + extraPropArr[0] + ", " + extraPropArr[
                                1] + " and " + extraPropArr[2] + ")"
                        elif len(extraPropArr) == 2:
                            return str(r['bb atk%']) + "% damage modifier (" + extraPropArr[0] + " and " + extraPropArr[
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
                            return str(r['bb atk%']) + "% damage modifier and drains " + str(r['hp drain% low']) + "~" + str(r['hp drain% high']) + " of damage dealt as HP (" + str(r['bb crit%']) + "% innate crit rate)"
                        else:
                            return str(r['bb atk%']) + "% damage modifier and drains " + str(
                                r['hp drain% low']) + "~" + str(r['hp drain% high']) + " of damage dealt as HP"
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
                            return "Reduces Thunder damage by " + str(r['mitigate thunder attacks (24)']) + "%"
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
                            return "Damage taken boosts BB gauge by " + str(r['bc fill when attacked low']) + "~" + str(
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
                            return "Boosts Atk relative to " + str(r['atk% buff (46)']) + "% of " + str(converted)
                        else:
                            return "null"
                    elif extraArg == 'def':
                        if 'def% buff (47)' in r:
                            converted = r['converted attribute']
                            if converted == 'hp':
                                converted = 'HP'
                            else:
                                converted = converted.capitalize()
                            return "Boosts Def relative to " + str(r['def% buff (47)']) + "% of " + str(converted)
                        else:
                            return "null"
                    elif extraArg == 'rec':
                        if 'rec% buff (48)' in r:
                            converted = r['converted attribute']
                            if converted == 'hp':
                                converted = 'HP'
                            else:
                                converted = converted.capitalize()
                            return "Boosts Rec relative to " + str(r['rec% buff (48)']) + "% of " + str(converted)
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
                            return str(r['bb atk%']) + "% damage modifier, or " + str(r['hp% damage chance%']) + "% chance of dealing " + str(
                                r['hp% damage low']) + "~" + str(r['hp% damage high']) + "% of enemy HP as damage instead"
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
                            return str(r['bb atk%']) + "% damage modifier (" + str(r['bb crit%']) + "% innate crit rate)"
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
                                return "Reduces foe's BB gauge by " + str(r['bb gauge% reduction high']) + "%"
                            else:
                                return str(
                                    int(r['bb gauge reduction chance%'])) + " chance of reducing foe's BB gauge by " + str(
                                    r['bb gauge% reduction high']) + "%"
                        else:
                            if int(r['bb gauge reduction chance%']) == 100:
                                return "Reduces foe's BB gauge by " + str(r['bb gauge% reduction low']) + "~" + str(
                                    r['bb gauge reduction high']) + "%"
                            else:
                                return str(
                                    int(r['bb gauge reduction chance%'])) + " chance of reducing foe's BB gauge by " + str(
                                    r['bb gauge% reduction low']) + "~" + str(r['bb gauge% reduction high']) + "%"
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
                            return "Reduces Fire damage by " + str(r['dmg% mitigation for elemental attacks']) + "%"
                        else:
                            return "null"
                    elif extraArg == 'water':
                        if 'mitigate water attacks' in r:
                            return "Reduces Water damage by " + str(r['dmg% mitigation for elemental attacks']) + "%"
                        else:
                            return "null"
                    elif extraArg == 'earth':
                        if 'mitigate earth attacks' in r:
                            return "Reduces Earth damage by " + str(r['dmg% mitigation for elemental attacks']) + "%"
                        else:
                            return "null"
                    elif extraArg == 'thunder':
                        if 'mitigate thunder attacks' in r:
                            return "Reduces Thunder damage by " + str(r['dmg% mitigation for elemental attacks']) + "%"
                        else:
                            return "null"
                    elif extraArg == 'light':
                        if 'mitigate light attacks' in r:
                            return "Reduces Light damage by " + str(r['dmg% mitigation for elemental attacks']) + "%"
                        else:
                            return "null"
                    elif extraArg == 'dark':
                        if 'mitigate dark attacks' in r:
                            return "Reduces Dark damage by " + str(r['dmg% mitigation for elemental attacks']) + "%"
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
                if str(procID) == r['proc id'] == '40' and extraArg in ['curse','paralysis','poison','injury','sick','weaken'] and str(extraArg) + '% buff' in r:
                    if extraArg == 'weaken':
                        return "Added to attack: " + str(
                            r[str(extraArg) + '% buff']) + "% chance of inflicting Weak"
                    else:
                        return "Added to attack: " + str(
                            r[str(extraArg) + '% buff']) + "% chance of inflicting " + extraArg.capitalize()
                if str(procID) == r['proc id'] == '40' and extraArg in ['curse','paralysis','poison','injury','sick','weaken'] and str(extraArg) + '% buff' not in r:
                    return "null"
                if str(procID) == r['proc id'] == '40' and extraArg not in ['curse','paralysis','poison','injury','sick','weaken']:
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
                            return "For each unit alive, fill " + str(int(r['increase od gauge%'])) + "% of the OD gauge"
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
                            return str(r['dot atk%']) + "% DoT modifier with +" + str(r['dot dmg%']) + "% multiplier bonus: " + str(int(((r['dot dmg%'] + 100) / 100) * r['dot atk%'])) + "% DoT modifier total"
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
                                    r['bb added atk% based on hp']) + "% * (current HP / base max HP) damage modifier (" + str(r['bb crit%']) + "% innate crit rate)"
                            else:
                                return str(r['bb base atk%']) + "% + " + str(
                                    r['bb added atk% based on hp']) + "% * (current HP / base max HP) damage modifier"
                        else:
                            if 'bb crit%' in r:
                                return str(r['bb base atk%']) + "% + " + str(
                                    r[
                                        'bb added atk% based on hp']) + "% * (base max HP / current HP) damage modifier (" + str(
                                    r['bb crit%']) + "% innate crit rate)"
                            else:
                                return str(r['bb base atk%']) + "% + " + str(
                                    r['bb added atk% based on hp']) + "% * (base max HP / current HP) damage modifier"
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
                            return "Added to attack: " + str(int(r['inflict atk% debuff chance% (74)'])) + "% chance of reducing " \
                                                                                                  "Atk by " + str(int(r['inflict atk% debuff (2)'] * -1)) + "%"
                        else:
                            return "null"
                    elif extraArg == 'def':
                        if 'inflict def% debuff (4)' in r:
                            return "Added to attack: " + str(int(r['inflict def% debuff chance% (75)'])) + "% chance of reducing " \
                                                                                                  "Def by " + str(int(r['inflict def% debuff (4)'] * -1)) + "%"
                        else:
                            return "null"
                    elif extraArg == 'rec':
                        if 'inflict rec% debuff (6)' in r:
                            return "Added to attack: " + str(int(r['inflict rec% debuff chance% (76)'])) + "% chance of reducing " \
                                                                                                  "Rec by " + str(int(r['inflict rec% debuff (6)'] * -1)) + "%"
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
                        if extraArg in ['curse% (82)', 'poison% (78)', 'paralysis% (83)', 'injury% (81)', 'sick% (80)', 'weaken% (79)']:
                            if 'counter inflict ' + str(extraArg) in r:
                                if extraArg == 'curse% (82)':
                                    return str(int(r['counter inflict ' + str(extraArg)])) + "% chance of inflicting Curse when damage is taken"
                                elif extraArg == 'poison% (78)':
                                    return str(
                                        int(r['counter inflict ' + str(extraArg)])) + "% chance of inflicting Poison when damage is taken"
                                elif extraArg == 'paralysis% (83)':
                                    return str(
                                        int(r['counter inflict ' + str(extraArg)])) + "% chance of inflicting Paralysis when damage is taken"
                                elif extraArg == 'injury% (81)':
                                    return str(
                                        int(r['counter inflict ' + str(extraArg)])) + "% chance of inflicting Injury when damage is taken"
                                elif extraArg == 'sick% (80)':
                                    return str(
                                        int(r['counter inflict ' + str(extraArg)])) + "% chance of inflicting Sick when damage is taken"
                                elif extraArg == 'weaken% (79)':
                                    return str(
                                        int(r['counter inflict ' + str(extraArg)])) + "% chance of inflicting Weak when damage is taken"
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
                            return str(int(r['elemental weakness multiplier%'])) + "% boost to " + str(extraArg).capitalize() + " elemental damage"
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
                            return str(int(r['angel idol recover chance%'])) + "% chance of resisting 1 KO, restores " + str(r['angel idol recover hp%']) + "% of unit's HP"
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
                            return str(int(r['spark dmg received apply%'])) + "% chance of inflicting " + str(r['spark dmg% received']) + "% spark vulnerability"
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
                            return "Activates " + extraArg.capitalize() + " barrier with " + str(r['elemental barrier hp']) + " HP"
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
                                r['bb atk% max number of inc']) + " times) damage modifier (" + extraPropArr[0] + ", " + extraPropArr[
                                1] + " and " + extraPropArr[2] + ")"
                        elif len(extraPropArr) == 2:
                            return str(r['bb base atk%']) + "% + " + str(
                                r['bb atk% inc per use']) + "% * (number of consecutive uses, max " + str(
                                r['bb atk% max number of inc']) + " times) damage modifier (" + extraPropArr[0] + " and " + extraPropArr[
                                1] + ")"
                        elif len(extraPropArr) == 1:
                            return str(r['bb base atk%']) + "% + " + str(
                                r['bb atk% inc per use']) + "% * (number of consecutive uses, max " + str(
                                r['bb atk% max number of inc']) + " times) damage modifier (" + extraPropArr[0] + ")"
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
                        return str(r['atk% buff when enemy has ailment']) + "% boost to Atk when enemy is status afflicted"
                # REVIVE
                if str(procID) == r['proc id'] == '66':
                    if extraArg == "turns":
                        return "—"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        return str(int(r['revive unit chance%'])) + "% chance of reviving with " + str(r['revive unit hp%']) + "% HP"
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
                                return "Fills " + str(r['bc fill on spark low']) + "~" + str(r['bc fill on spark high']) + " BC per spark"
                        else:
                            if r['bc fill on spark low'] == r['bc fill on spark high']:
                                return str(r['bc fill on spark%']) + "% chance of filling " + str(r['bc fill on spark high']) + " BC per spark"
                            else:
                                return str(r['bc fill on spark%']) + "% chance of filling " + str(r['bc fill on spark low']) + "~" + str(r['bc fill on spark high']) + " BC per spark"
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
                        return "Reduces damage taken by " + str(r['guard increase mitigation%']) + "% when guarding"
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
                        return str(r['atk% buff (1)']) + "% + " + str(r['def% buff (3)']) + "% * (number of " + str(r['counted element for buff multiplier']).capitalize() + " units in party, up to 2 maximum) damage modifier"
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
                            return str(r['chance% for extra action']) + "% chance of acting " + str(r['max number of extra actions']) + " extra time"
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
                        return str(r['spark dmg inc chance%']) + "% chance of dealing " + str(r['spark dmg inc% buff']) + "% extra spark damage"
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
                            return "Recovers " + str(r['hp drain% low']) + "~" + str(r['hp drain% high']) + " damage dealt as HP"
                        else:
                            return str(r['hp drain chance%']) + "% chance of recovering " + str(r['hp drain% low']) + "~" + str(r['hp drain% high']) + " damage dealt as HP"
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
                            return "Recovers " + str(r['spark recover hp low']) + "~" + str(r['spark recover hp high']) + " HP per spark"
                        else:
                            return str(r['spark recover hp chance%']) + "% chance of recovering " + str(r['spark recover hp low']) + "~" + str(r['spark recover hp high']) + " HP per spark"
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
                                return str(r['crit dmg buffed damage resist% (143)']) + "% resistance to critical damage"
                        elif extraArg == 'ewd' and 'strong buffed element damage resist% (144)' in r:
                            if r['strong buffed element damage resist% (144)'] == 100:
                                return "Negates elemental damage"
                            else:
                                return str(r['strong buffed element damage resist% (144)']) + "% resistance to elemental damage"
                        elif extraArg == 'spark' and 'spark dmg buffed resist% (145)' in r:
                            if r['spark dmg buffed resist% (145)'] == 100:
                                return "Negates spark damage"
                            else:
                                return str(r['spark dmg buffed resist% (145)']) + "% resistance to spark damage"
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
                                return str(r['chance to aoe']) + "% chance of attacking all enemies with normal attack"
                            else:
                                return str(r['chance to aoe']) + "% chance of attacking all enemies with normal attack (" + str(r['aoe atk inc%']) + "% AoE damage modifier)"
                        else:
                            return str(r['chance to aoe']) + "% chance of attacking all enemies with normal attack"
                # ELEMENT TARGET DAMAGE
                if str(procID) == r['proc id'] == '97':
                    if extraArg == 'turns':
                        return "—"
                    elif extraArg == 'target':
                        target = str(targetType(r))
                        return target
                    else:
                        if 'bb crit%' in r:
                            return str(r['bb atk%']) + "% damage modifier (" + str(r['bb crit%']) + "% innate crit rate)"
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
                                    return "Damage taken has a " + str(r['atk buff chance%']) + "% chance of inflicting " + str(
                                        int(r['atk% buff (153)'] * -1)) + "% Atk reduction for 1 turn"
                                else:
                                    return "Damage taken has a " + str(r['atk buff chance%']) + "% chance of inflicting " + str(
                                        int(r['atk% buff (153)'] * -1)) + "% Atk reduction for " + str(
                                        r['debuff turns']) + " turns"
                            else:
                                return "null"
                        elif extraArg == 'def':
                            if 'def% buff (154)' in r:
                                if r['debuff turns'] == 1:
                                    return "Damage taken has a " + str(r['def buff chance%']) + "% chance of inflicting " + str(
                                        int(r['def% buff (154)'] * -1)) + "% Def reduction for 1 turn"
                                else:
                                    return "Damage taken has a " + str(r['def buff chance%']) + "% chance of inflicting " + str(
                                        int(r['def% buff (154)'] * -1)) + "% Def reduction for " + str(
                                        r['debuff turns']) + " turns"
                            else:
                                return "null"
                        elif extraArg == 'rec':
                            if 'rec% buff (155)' in r:
                                if r['debuff turns'] == 1:
                                    return "Damage taken has a " + str(r['rec buff chance%']) + "% chance of inflicting " + str(
                                        int(r['rec% buff (155)'] * -1)) + "% Rec reduction for 1 turn"
                                else:
                                    return "Damage taken has a " + str(r['def buff chance%']) + "% chance of inflicting " + str(
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
                                return "Inflicts " + str(r['elemental vuln dmg% (158)']) + "% elemental vulnerability"
                            else:
                                return str(int(r['elemental vuln chance%'])) + "% chance of inflicting " + str(
                                    r['elemental vuln dmg% (158)']) + "% elemental vulnerability"
                        elif extraArg == "crit" and 'crit vuln dmg% (157)' in r:
                            if r['crit vuln chance%'] == 100:
                                return "Inflicts " + str(r['crit vuln dmg% (157)']) + "% critical vulnerability"
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
                                r['bb added atk% based on hp']) + "% * (percentage of HP lost) damage modifier (" + str(r['bb crit%']) + "% innate crit rate)"
                        else:
                            return str(r['bb base atk%']) + "% + " + str(
                                r['bb added atk% based on hp']) + "% * (percentage of HP lost) damage modifier"
            # UNKNOWN
            else:
                # SELF CONVERSION
                if str(procID) == r['unknown proc id'] == '89':
                    params = r['unknown proc param'].split(',')
                    stats = ['Atk','Def','Rec','HP']
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
                                return "Boosts own Atk relative to " + str(params[1]) + "% of " + str(stats[int(params[0]) - 1])
                            else:
                                return "null"
                        elif extraArg == 'def':
                            if params[2] != '0':
                                return "Boosts own Def relative to " + str(params[2]) + "% of " + str(stats[int(params[0]) - 1])
                            else:
                                return "null"
                        elif extraArg == 'rec':
                            if params[3] != '0':
                                return "Boosts own Rec relative to " + str(params[3]) + "% of " + str(stats[int(params[0]) - 1])
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
                            return str(int(float(params[0]) * 100)) + "% boost to critical damage of Fire units"
                        elif extraArg == 'water' and str(params[3]) == '2':
                            return str(int(float(params[0]) * 100)) + "% boost to critical damage of Water units"
                        elif extraArg == 'earth' and str(params[3]) == '3':
                            return str(int(float(params[0]) * 100)) + "% boost to critical damage of Earth units"
                        elif extraArg == 'thunder' and str(params[3]) == '4':
                            return str(int(float(params[0]) * 100)) + "% boost to critical damage of Thunder units"
                        elif extraArg == 'light' and str(params[3]) == '5':
                            return str(int(float(params[0]) * 100)) + "% boost to critical damage of Light units"
                        elif extraArg == 'dark' and str(params[3]) == '6':
                            return str(int(float(params[0]) * 100)) + "% boost to critical damage of Dark units"
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
                            return "Activates Fire Shield (" + str(params[1]) + " HP & " + str(params[2]) + " Def)"
                        elif extraArg == 'water' and str(params[0]) == '2':
                            return "Activates Water Shield (" + str(params[1]) + " HP & " + str(params[2]) + " Def)"
                        elif extraArg == 'earth' and str(params[0]) == '3':
                            return "Activates Earth Shield (" + str(params[1]) + " HP & " + str(params[2]) + " Def)"
                        elif extraArg == 'thunder' and str(params[0]) == '4':
                            return "Activates Thunder Shield (" + str(params[1]) + " HP & " + str(params[2]) + " Def)"
                        elif extraArg == 'light' and str(params[0]) == '5':
                            return "Activates Light Shield (" + str(params[1]) + " HP & " + str(params[2]) + " Def)"
                        elif extraArg == 'dark' and str(params[0]) == '6':
                            return "Activates Dark Shield (" + str(params[1]) + " HP & " + str(params[2]) + " Def)"
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
                        return "Reduces max HP by " +  str(params[0]) + "%"
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
                        for a in range(0,9):
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
                        elementArr = ['Fire','Water','Earth','Thunder','Light','Dark']
                        for a in range(3,9):
                            if params[a] == '1':
                                pierceArr.append(elementArr[a - 3])
                        if len(pierceArr) > 2:
                            for b in range(0,len(pierceArr) - 1):
                                pierceStr = pierceStr + pierceArr[b] + ", "
                            pierceStr = pierceStr + "and " + pierceArr[b]
                        elif len(pierceArr) == 2:
                            pierceStr = pierceArr[0] + " and " + pierceArr[1]
                        elif len(pierceArr) == 1:
                            pierceStr = pierceArr[0]
                        else:
                            pierceStr = "N/A"
                        return str(params[0]) + "% damage modifier, deals " + str(params[2]) + "% piercing damage against " + str(pierceStr) + " enemies"
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


def header(r, s):
    addSpace = 15 - len(str(r) + "_" + str(s))
    spaceStr = ""
    for a in range(0, addSpace):
        spaceStr = spaceStr + " "
    return str(r) + "_" + str(s) + str(spaceStr)


def printBuffs(unitID, skill):
    output = "{{UnitBuffList\n"
    count = 0
    allBuffs = []
    global globalArr
    globalArr.clear()
    globalArrCount = -1
    for r in data[str(unitID)][str(skill)]['levels'][-1]['effects']:
        globalArr.append(0)
        try:
            allBuffs.append(str(r['proc id']))
        except:
            allBuffs.append(str(r['unknown proc id']))
    #print(allBuffs)
    for r in allBuffs:
        globalArrCount = globalArrCount + 1
        temp = ""
        success = False
        #print("Printing " + r)
        additionalArg = ""
        try:
            if r == '5':
                for s in ['', 'fire', 'water', 'earth', 'thunder', 'light', 'dark']:
                    for t in ['atk', 'def', 'rec', 'crit']:
                        if searchBuffs(unitID, skill, r, str(t) + str(s)) != 'null':
                            count = count + 1
                            if s == '':
                                temp = "|buff_" + header(str(count), "proc") + "= " + str(r) + "_" + str(t) + "\n" + \
                                       "|buff_" + header(str(count), "potency") + "= " + searchBuffs(unitID, skill, r, str(t) + str(s)) + "\n" + \
                                       "|buff_" + header(str(count), "duration") + "= " + searchBuffs(unitID, skill, r, "turns") + "\n" + \
                                       "|buff_" + header(str(count), "target") + "= " + searchBuffs(unitID, skill, r, "target") + "\n"
                            else:
                                temp = "|buff_" + header(str(count), "proc") + "= " + str(r) + "_" + str(s) + "_" + str(
                                    t) + "\n" + \
                                       "|buff_" + header(str(count), "potency") + "= " + searchBuffs(unitID, skill, r,
                                                                                                     str(t) + str(
                                                                                                         s)) + "\n" + \
                                       "|buff_" + header(str(count), "duration") + "= " + searchBuffs(unitID, skill, r,
                                                                                                      "turns") + "\n" + \
                                       "|buff_" + header(str(count), "target") + "= " + searchBuffs(unitID, skill, r,
                                                                                                    "target") + "\n"
                            output = output + temp
                            success = False
            elif r == '6':
                for s in ['bc', 'hc', 'item']:
                    if searchBuffs(unitID, skill, r, s) != 'null':
                        count = count + 1
                        temp = "|buff_" + header(str(count), "proc") + "= " + str(r) + "_" + str(s) + "\n" +\
                               "|buff_" + header(str(count), "potency") + "= " + searchBuffs(unitID, skill, r,
                                                                                                  s) + "\n" + \
                               "|buff_" + header(str(count), "duration") + "= " + searchBuffs(unitID, skill, r,
                                                                                                   "turns") + "\n" + \
                               "|buff_" + header(str(count), "target") + "= " + searchBuffs(unitID, skill, r,
                                                                                                 "target") + "\n"
                        output = output + temp
                        success = False
            elif r == '9':
                for s in ['atk', 'def', 'rec']:
                    if searchBuffs(unitID, skill, r, s) != 'null':
                        count = count + 1
                        temp = "|buff_" + header(str(count), "proc") + "= " + str(r) + "_" + str(s) + "\n" +\
                               "|buff_" + header(str(count), "potency") + "= " + searchBuffs(unitID,
                                                                                                           skill, r,
                                                                                                           s) + "\n" + \
                               "|buff_" + header(str(count), "duration") + "= " + searchBuffs(unitID,
                                                                                                            skill, r,
                                                                                                            "turns") + "\n" + \
                               "|buff_" + header(str(count), "target") + "= " + searchBuffs(unitID, skill,
                                                                                                          r,
                                                                                                          "target") + "\n"
                        output = output + temp
                        success = False
            elif r == '11':
                for s in ['curse', 'poison', 'paralysis', 'injury', 'sick', 'weaken']:
                    if searchBuffs(unitID, skill, r, s) != 'null':
                        count = count + 1
                        temp = "|buff_" + header(str(count), "proc") + "= " + str(r) + "_" + str(s) + "\n" +\
                               "|buff_" + header(str(count), "potency") + "= " + searchBuffs(unitID, skill, r,
                                                                                                  s) + "\n" + \
                               "|buff_" + header(str(count), "duration") + "= " + searchBuffs(unitID, skill, r,
                                                                                                   str(
                                                                                                       s) + "turns") + "\n" + \
                               "|buff_" + header(str(count), "target") + "= " + searchBuffs(unitID, skill, r,
                                                                                                 "target") + "\n"
                        output = output + temp
                        success = False
            elif r == '16':
                for s in ['fire', 'water', 'earth', 'thunder', 'light', 'dark']:
                    if searchBuffs(unitID, skill, r, s) != 'null':
                        count = count + 1
                        temp = "|buff_" + header(str(count), "proc") + "= " + str(r) + "_" + str(s) + "\n" +\
                               "|buff_" + header(str(count), "potency") + "= " + searchBuffs(unitID,
                                                                                                           skill, r,
                                                                                                           s) + "\n" + \
                               "|buff_" + header(str(count), "duration") + "= " + searchBuffs(unitID,
                                                                                                            skill, r,
                                                                                                            "turns") + "\n" + \
                               "|buff_" + header(str(count), "target") + "= " + searchBuffs(unitID, skill,
                                                                                                          r,
                                                                                                          "target") + "\n"
                        output = output + temp
                        success = False
            elif r == '24':
                for s in ['atk', 'def', 'rec']:
                    if searchBuffs(unitID, skill, r, s) != 'null':
                        count = count + 1
                        temp = "|buff_" + header(str(count), "proc") + "= " + str(r) + "_" + str(s) + "\n" +\
                               "|buff_" + header(str(count), "potency") + "= " + searchBuffs(unitID, skill, r,
                                                                                                  s) + "\n" + \
                               "|buff_" + header(str(count), "duration") + "= " + searchBuffs(unitID, skill, r,
                                                                                                   "turns") + "\n" + \
                               "|buff_" + header(str(count), "target") + "= " + searchBuffs(unitID, skill, r,
                                                                                                 "target") + "\n"
                        output = output + temp
                        success = False
            elif r == '39':
                for s in ['fire', 'water', 'earth', 'thunder', 'light', 'dark']:
                    if searchBuffs(unitID, skill, r, s) != 'null':
                        count = count + 1
                        temp = "|buff_" + header(str(count), "proc") + "= " + str(r) + "_" + str(s) + "\n" +\
                               "|buff_" + header(str(count), "potency") + "= " + searchBuffs(unitID,
                                                                                                           skill, r,
                                                                                                           s) + "\n" + \
                               "|buff_" + header(str(count), "duration") + "= " + searchBuffs(unitID,
                                                                                                            skill, r,
                                                                                                            "turns") + "\n" + \
                               "|buff_" + header(str(count), "target") + "= " + searchBuffs(unitID, skill,
                                                                                                          r,
                                                                                                          "target") + "\n"
                        output = output + temp
                        success = False
            elif r == '40':
                for s in ['curse', 'poison', 'paralysis', 'injury', 'sick', 'weaken']:
                    if searchBuffs(unitID, skill, r, s) != 'null':
                        count = count + 1
                        temp = "|buff_" + header(str(count), "proc") + "= " + str(r) + "_" + str(s) + "\n" +\
                               "|buff_" + header(str(count), "potency") + "= " + searchBuffs(unitID, skill, r,
                                                                                                  s) + "\n" + \
                               "|buff_" + header(str(count), "duration") + "= " + searchBuffs(unitID, skill, r,
                                                                                                   "turns") + "\n" + \
                               "|buff_" + header(str(count), "target") + "= " + searchBuffs(unitID, skill, r,
                                                                                                 "target") + "\n"
                        output = output + temp
                        success = False
            elif r == '51':
                for s in ['atk','def','rec']:
                    if searchBuffs(unitID, skill, r, s) != 'null':
                        count = count + 1
                        temp = "|buff_" + header(str(count), "proc") + "= " + str(r) + "_" + str(s) + "\n" +\
                               "|buff_" + header(str(count), "potency") + "= " + searchBuffs(unitID, skill, r,
                                                                                                  s) + "\n" + \
                               "|buff_" + header(str(count), "duration") + "= " + searchBuffs(unitID, skill, r,
                                                                                                   "turns") + "\n" + \
                               "|buff_" + header(str(count), "target") + "= " + searchBuffs(unitID, skill, r,
                                                                                                 "target") + "\n"
                        output = output + temp
                        success = False
            elif r == '53':
                for s in ['curse% (82)', 'poison% (78)', 'paralysis% (83)', 'injury% (81)', 'sick% (80)', 'weaken% (79)']:
                    if searchBuffs(unitID, skill, r, s) != 'null':
                        temp = ""
                        count = count + 1
                        if s == 'curse% (82)':
                            temp = "|buff_" + header(str(count), "proc") + "= " + str(r) + "_curse\n" +\
                                   "|buff_" + header(str(count), "potency") + "= " + searchBuffs(unitID, skill, r,
                                                                                                      s) + "\n" + \
                                   "|buff_" + header(str(count), "duration") + "= " + searchBuffs(unitID, skill, r,
                                                                                                       "turns") + "\n" + \
                                   "|buff_" + header(str(count), "target") + "= " + searchBuffs(unitID, skill, r,
                                                                                                     "target") + "\n"
                        elif s == 'poison% (78)':
                            temp = "|buff_" + header(str(count), "proc") + "= " + str(r) + "_poison\n" +\
                                   "|buff_" + header(str(count), "potency") + "= " + searchBuffs(unitID, skill, r,
                                                                                                      s) + "\n" + \
                                   "|buff_" + header(str(count), "duration") + "= " + searchBuffs(unitID, skill, r,
                                                                                                       "turns") + "\n" + \
                                   "|buff_" + header(str(count), "target") + "= " + searchBuffs(unitID, skill, r,
                                                                                                     "target") + "\n"
                        elif s == 'paralysis% (83)':
                            temp = "|buff_" + header(str(count), "proc") + "= " + str(r) + "_paralysis\n" +\
                                   "|buff_" + header(str(count), "potency") + "= " + searchBuffs(unitID, skill, r,
                                                                                                      s) + "\n" + \
                                   "|buff_" + header(str(count), "duration") + "= " + searchBuffs(unitID, skill, r,
                                                                                                       "turns") + "\n" + \
                                   "|buff_" + header(str(count), "target") + "= " + searchBuffs(unitID, skill, r,
                                                                                                     "target") + "\n"
                        elif s == 'injury% (81)':
                            temp = "|buff_" + header(str(count), "proc") + "= " + str(r) + "_injury\n" +\
                                   "|buff_" + header(str(count), "potency") + "= " + searchBuffs(unitID, skill, r,
                                                                                                      s) + "\n" + \
                                   "|buff_" + header(str(count), "duration") + "= " + searchBuffs(unitID, skill, r,
                                                                                                       "turns") + "\n" + \
                                   "|buff_" + header(str(count), "target") + "= " + searchBuffs(unitID, skill, r,
                                                                                                     "target") + "\n"
                        elif s == 'sick% (80)':
                            temp = "|buff_" + header(str(count), "proc") + "= " + str(r) + "_sick\n" +\
                                   "|buff_" + header(str(count), "potency") + "= " + searchBuffs(unitID, skill, r,
                                                                                                      s) + "\n" + \
                                   "|buff_" + header(str(count), "duration") + "= " + searchBuffs(unitID, skill, r,
                                                                                                       "turns") + "\n" + \
                                   "|buff_" + header(str(count), "target") + "= " + searchBuffs(unitID, skill, r,
                                                                                                     "target") + "\n"
                        elif s == 'weaken% (79)':
                            temp = "|buff_" + header(str(count), "proc") + "= " + str(r) + "_weaken\n" +\
                                   "|buff_" + header(str(count), "potency") + "= " + searchBuffs(unitID, skill, r,
                                                                                                      s) + "\n" + \
                                   "|buff_" + header(str(count), "duration") + "= " + searchBuffs(unitID, skill, r,
                                                                                                       "turns") + "\n" + \
                                   "|buff_" + header(str(count), "target") + "= " + searchBuffs(unitID, skill, r,
                                                                                                     "target") + "\n"
                        output = output + temp
                        success = False
            elif r == '55':
                for s in ['fire', 'water', 'earth', 'thunder', 'light', 'dark']:
                    if searchBuffs(unitID, skill, r, s) != 'null':
                        count = count + 1
                        temp = "|buff_" + header(str(count), "proc") + "= " + str(r) + "_" + str(s) + "\n" +\
                               "|buff_" + header(str(count), "potency") + "= " + searchBuffs(unitID,
                                                                                                           skill, r,
                                                                                                           s) + "\n" + \
                               "|buff_" + header(str(count), "duration") + "= " + searchBuffs(unitID,
                                                                                                            skill, r,
                                                                                                            "turns") + "\n" + \
                               "|buff_" + header(str(count), "target") + "= " + searchBuffs(unitID, skill,
                                                                                                          r,
                                                                                                          "target") + "\n"
                        output = output + temp
                        success = False
            elif r == '62':
                for s in ['fire', 'water', 'earth', 'thunder', 'light', 'dark']:
                    if searchBuffs(unitID, skill, r, s) != 'null':
                        count = count + 1
                        temp = "|buff_" + header(str(count), "proc") + "= " + str(r) + "_" + str(s) + "\n" +\
                               "|buff_" + header(str(count), "potency") + "= " + searchBuffs(unitID,
                                                                                                           skill, r,
                                                                                                           s) + "\n" + \
                               "|buff_" + header(str(count), "duration") + "= " + searchBuffs(unitID,
                                                                                                            skill, r,
                                                                                                            "turns") + "\n" + \
                               "|buff_" + header(str(count), "target") + "= " + searchBuffs(unitID, skill,
                                                                                                          r,
                                                                                                          "target") + "\n"
                        output = output + temp
                        success = False
            elif r == '78':
                for s in ['atk','def','rec','crit']:
                    if searchBuffs(unitID, skill, r, s) != 'null':
                        count = count + 1
                        temp = "|buff_" + header(str(count), "proc") + "= " + str(r) + "_" + str(s) + "\n" +\
                               "|buff_" + header(str(count), "potency") + "= " + searchBuffs(unitID, skill, r,
                                                                                                  s) + "\n" + \
                               "|buff_" + header(str(count), "duration") + "= " + searchBuffs(unitID, skill, r,
                                                                                                   "turns") + "\n" + \
                               "|buff_" + header(str(count), "target") + "= " + searchBuffs(unitID, skill, r,
                                                                                                 "target") + "\n"
                        output = output + temp
                        success = False
            elif r == '89':
                for s in ['atk','def','rec']:
                    if searchBuffs(unitID, skill, r, s) != 'null':
                        count = count + 1
                        temp = "|buff_" + header(str(count), "proc") + "= " + str(r) + "_" + str(s) + "\n" +\
                               "|buff_" + header(str(count), "potency") + "= " + searchBuffs(unitID, skill, r,
                                                                                                  s) + "\n" + \
                               "|buff_" + header(str(count), "duration") + "= " + searchBuffs(unitID, skill, r,
                                                                                                   "turns") + "\n" + \
                               "|buff_" + header(str(count), "target") + "= " + searchBuffs(unitID, skill, r,
                                                                                                 "target") + "\n"
                        output = output + temp
                        success = False
            elif r == '93':
                for s in ['crit','ewd','spark']:
                    if searchBuffs(unitID, skill, r, s) != 'null':
                        count = count + 1
                        temp = "|buff_" + header(str(count), "proc") + "= " + str(r) + "_" + str(s) + "\n" +\
                               "|buff_" + header(str(count), "potency") + "= " + searchBuffs(unitID, skill, r,
                                                                                                  s) + "\n" + \
                               "|buff_" + header(str(count), "duration") + "= " + searchBuffs(unitID, skill, r,
                                                                                                   "turns") + "\n" + \
                               "|buff_" + header(str(count), "target") + "= " + searchBuffs(unitID, skill, r,
                                                                                                 "target") + "\n"
                        output = output + temp
                        success = False
            elif r == '130':
                for s in ['atk','def','rec']:
                    if searchBuffs(unitID, skill, r, s) != 'null':
                        count = count + 1
                        temp = "|buff_" + header(str(count), "proc") + "= " + str(r) + "_" + str(s) + "\n" +\
                               "|buff_" + header(str(count), "potency") + "= " + searchBuffs(unitID, skill, r,
                                                                                                  s) + "\n" + \
                               "|buff_" + header(str(count), "duration") + "= " + searchBuffs(unitID, skill, r,
                                                                                                   "turns") + "\n" + \
                               "|buff_" + header(str(count), "target") + "= " + searchBuffs(unitID, skill, r,
                                                                                                 "target") + "\n"
                        output = output + temp
                        success = False
            elif r == '132':
                for s in ['ewd','crit']:
                    if searchBuffs(unitID, skill, r, s) != 'null':
                        count = count + 1
                        temp = "|buff_" + header(str(count), "proc") + "= " + str(r) + "_" + str(s) + "\n" +\
                               "|buff_" + header(str(count), "potency") + "= " + searchBuffs(unitID, skill, r,
                                                                                                  s) + "\n" + \
                               "|buff_" + header(str(count), "duration") + "= " + searchBuffs(unitID, skill, r,
                                                                                                   "turns") + "\n" + \
                               "|buff_" + header(str(count), "target") + "= " + searchBuffs(unitID, skill, r,
                                                                                                 "target") + "\n"
                        output = output + temp
                        success = False
            elif r == '10015':
                for s in ['fire', 'water', 'earth', 'thunder', 'light', 'dark']:
                    if searchBuffs(unitID, skill, r, s) != 'null':
                        count = count + 1
                        temp = "|buff_" + header(str(count), "proc") + "= " + str(r) + "_" + str(s) + "\n" +\
                               "|buff_" + header(str(count), "potency") + "= " + searchBuffs(unitID,
                                                                                                           skill, r,
                                                                                                           s) + "\n" + \
                               "|buff_" + header(str(count), "duration") + "= " + searchBuffs(unitID,
                                                                                                            skill, r,
                                                                                                            "turns") + "\n" + \
                               "|buff_" + header(str(count), "target") + "= " + searchBuffs(unitID, skill,
                                                                                                          r,
                                                                                                          "target") + "\n"
                        output = output + temp
                        success = False
            elif r == '10016':
                for s in ['fire', 'water', 'earth', 'thunder', 'light', 'dark']:
                    if searchBuffs(unitID, skill, r, s) != 'null':
                        count = count + 1
                        temp = "|buff_" + header(str(count), "proc") + "= " + str(r) + "_" + str(s) + "\n" +\
                               "|buff_" + header(str(count), "potency") + "= " + searchBuffs(unitID,
                                                                                                           skill, r,
                                                                                                           s) + "\n" + \
                               "|buff_" + header(str(count), "duration") + "= " + searchBuffs(unitID,
                                                                                                            skill, r,
                                                                                                            "turns") + "\n" + \
                               "|buff_" + header(str(count), "target") + "= " + searchBuffs(unitID, skill,
                                                                                                          r,
                                                                                                          "target") + "\n"
                        output = output + temp
                        success = False
            elif r == '10017':
                for s in ['fire', 'water', 'earth', 'thunder', 'light', 'dark']:
                    if searchBuffs(unitID, skill, r, s) != 'null':
                        count = count + 1
                        temp = "|buff_" + header(str(count), "proc") + "= " + str(r) + "_" + str(s) + "\n" +\
                               "|buff_" + header(str(count), "potency") + "= " + searchBuffs(unitID,
                                                                                                           skill, r,
                                                                                                           s) + "\n" + \
                               "|buff_" + header(str(count), "duration") + "= " + searchBuffs(unitID,
                                                                                                            skill, r,
                                                                                                            "turns") + "\n" + \
                               "|buff_" + header(str(count), "target") + "= " + searchBuffs(unitID, skill,
                                                                                                          r,
                                                                                                          "target") + "\n"
                        output = output + temp
                        success = False
            else:
                count = count + 1
                temp = "|buff_" + header(str(count), "proc") + "= " + str(r) + "\n" +\
                       "|buff_" + header(str(count), "potency") + "= " + searchBuffs(unitID, skill, r, "") + "\n" + \
                       "|buff_" + header(str(count), "duration") + "= " + searchBuffs(unitID, skill, r, "turns") + "\n" + \
                       "|buff_" + header(str(count), "target") + "= " + searchBuffs(unitID, skill, r, "target") + "\n"
                success = True
        except:
            temp = "|buff_" + header(str(count), "proc") + "= Failed to retrieve value\n" + \
                   "|buff_" + header(str(count), "potency") + "= Failed to retrieve value\n" + \
                   "|buff_" + header(str(count), "duration") + "= Failed to retrieve value\n" + \
                   "|buff_" + header(str(count), "target") + "= Failed to retrieve value\n"
            print("Error on " + str(unitID) + " in " + str(skill).upper() + ": Proc ID " + str(r))
            errors = errors + 1
            output = output + temp
        if (success):
            output = output + temp
        globalArr[globalArrCount] = 1
        #print(globalArr)
    output = output + "}}"
    #print(output)
    return output


def findErrors():
    global errors
    for unit in data.keys():
        for a in ['bb', 'sbb', 'ubb']:
            if a in data[unit].keys():
                printBuffs(unit, a)
    print(str(errors) + " errors found")


def printStuff(x):
    for a in ['bb', 'sbb', 'ubb']:
        if a in data[x].keys():
            printBuffs(x, a)


def findName(x):
    for r in data.keys():
        if str(x) == data[r]['name']:
            return r
    return x

#findErrors()
#printBuffs('9850167','bb')
#printStuff('810808')