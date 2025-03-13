from numexpr import evaluate
import lib.class_def as lcd
import streamlit as st
import dice
import re
import copy
import json
import base64
import random

#dice roller utility functions - add zero to collapse the result to an int instead of a list
def roll(diceStr, floor = None):
    roll = dice.roll(diceStr+"+0")
    if floor:
        if roll < floor:
            roll = floor
    return roll
    
def rollMax(diceStr, floor = None):
    roll = dice.roll_max(diceStr+"+0")
    if floor:
        if roll < floor:
            roll = floor
    return roll
    
def rollMin(diceStr, floor = None):
    roll = dice.roll_min(diceStr+"+0")
    if floor:
        if roll < floor:
            roll = floor
    return roll

#callback function for input changes to reset error unconditionally
def resetErrField(errKey):
    st.session_state[errKey] = False
    
#callback function for input changes to make sure they're numbers in a valid range - return values are also used in page initialization
def changeNumInput(key,errKey,roll = None, override = False):
    try:
        val = st.session_state[key]
        if val:
            val = int(val)
            st.session_state[errKey] = (False or override)
            if roll:
                if val > rollMax(roll) or val < rollMin(roll):
                    st.session_state[errKey] = True
        else:
            st.session_state[errKey] = (False or override)
    except:
        st.session_state[errKey] = True
    return st.session_state[errKey]
    
#random selection for arbitrary and specific fields
def randomSelector(key,selectList,errKey = None):
    st.session_state[key] = random.choice(selectList)
    if errKey:
        resetErrField(errKey)
    
#random selection for arbitrary and specific fields
def randomSelectWordTable(table):
    randomEntry = random.choice(table)
    if isinstance(randomEntry,list):
        randomEntry = randomSelectWordTable(randomEntry)
    return randomEntry
    
def randomNumber(key,rollString,errKey = None,lowerLimit = None):
    rollResult = roll(statifyString(rollString))
    if lowerLimit:
        rollResult = max(lowerLimit,rollResult)
    st.session_state[key] = str(rollResult)
    if errKey:
        changeNumInput(key,errKey,roll = rollString)

#process strings with special characters and replace them with stat values
def statifyString(inString):
    statValNumList = [st.session_state.PC.pc_agi, st.session_state.PC.pc_knw, st.session_state.PC.pc_pre, st.session_state.PC.pc_str, st.session_state.PC.pc_tou]
    for index, statVal in enumerate(statValNumList):
        sign = "+"
        invSign = "-"
        if statVal is None:
            statValString = longStatTable[index]
        else:
            if statVal == 0:
                statValString = ""
                sign = ""
                invSign = ""
            else:
                statValString = str(abs(statVal))
                if statVal < 0:
                    sign = "-"
                    invSign = "+"
        #adding mods
        inString = re.sub("(\+"+shortStatTable[index]+")",sign+statValString,inString)
        #subtracting mods
        inString = re.sub("(-"+shortStatTable[index]+")",invSign+statValString,inString)
        #mod as the first value
        inString = re.sub("("+shortStatTable[index]+")",statValString,inString)
        if statVal is not None:
            if statVal == 0:
                inString = re.sub("("+shortStatTable[index]+")","",inString)
            elif statVal < 0:
                inString = re.sub("("+shortStatTable[index]+")","-"+statValString,inString)
    return inString

def repCarryCap(carryString, bonus = 0):
    carryString = evaluate(statifyString(carryString + "+" + str(bonus))).item()
    carryList = [str(carryString),str(2*carryString)]
    return " &nbsp;| &nbsp;".join(carryList)

#turn JSON dictionaries into StuffField objects
def processStuff(stuff):
    if not isinstance(stuff, lcd.StuffField):
        stuffType = list(stuff.keys())[0]
        if "Name" in list(stuff[stuffType].keys()):
            stuffName = stuff[stuffType].pop("Name")
        else:
            stuffName = None
        if "ID" in list(stuff[stuffType].keys()):
            #remove the ID field and add all fields in the stuff entry
            #need to deepcopy here so we don't accidentally change properties of things in stuffDB when we update()
            stuffFieldObj = copy.deepcopy(stuffDB[stuff[stuffType].pop("ID")])
            stuffFieldObj.p_data.update(stuff[stuffType])
            if stuffName:
                stuffFieldObj.p_name = stuffName
        else:
            stuffFieldObj =  lcd.StuffField(stuffType,stuffName,stuff[stuffType])
            if stuffFieldObj.p_type == "StuffSet":
                stuffFieldObj.p_data["StuffList"] = [processStuff(subItem) for subItem in stuffFieldObj.p_data["StuffList"]]
            if "SubStuff" in stuffFieldObj.p_data.keys():
                stuffFieldObj.p_data["SubStuff"] = processStuff(stuffFieldObj.p_data["SubStuff"])
    else:
        stuffFieldObj = stuff
    return stuffFieldObj
    
def generateObjectFromStuffField(stuff):
    match stuff.p_type:
        case "Ammo":
            stuffObj = lcd.Ammo()
        case "App":
            stuffObj = lcd.App()
        case "Armor":
            stuffObj = lcd.Armor()
        case "Cyberdeck":
            stuffObj = lcd.Cyberdeck()
        case "Cyberware":
            stuffObj = lcd.Cyberware()
        case "Drug":
            stuffObj = lcd.Drug()
        case "Infestation":
            stuffObj = lcd.Infestation()
        case "Item":
            stuffObj = lcd.Item()
        case "Nano":
            stuffObj = lcd.Nano()
        case "Unit":
            stuffObj = lcd.Unit()
        case "Vehicle":
            stuffObj = lcd.Vehicle()
        case "Weapon":
            stuffObj = lcd.Weapon()
        case "Feature":
            stuffObj = lcd.Feature()
        case _:
            st.write("Unknown Stuff Type: "+stuff.p_type)
            return None
    #fill out fields
    if "Damage" in stuff.p_data.keys():
        stuffObj.p_damage = getDamageObject(stuff.p_data["Damage"])
        
    if stuff.p_name and not isinstance(stuffObj,lcd.Feature):
        stuffObj.p_name = stuff.p_name
    if "Description" in stuff.p_data.keys():
        stuffObj.p_desc = stuff.p_data["Description"]
        
    extraData = {}
    if "Armor" in stuff.p_data.keys():
        stuffObj.p_armor = stuff.p_data["Armor"]
    if "DescText" in stuff.p_data.keys():
        if hasattr(stuffObj,"p_pc_desc_text"):
            stuffObj.p_pc_desc_text = stuff.p_data["DescText"]
        else:
            extraData["p_pc_desc_text"] = stuff.p_data["DescText"]
    if "DamageReduction" in stuff.p_data.keys():
        stuffObj.p_armor = stuff.p_data["DamageReduction"]
    if "Equipped" in stuff.p_data.keys():
        stuffObj.p_equipped = stuff.p_data["Equipped"]
    if "FeatureText" in stuff.p_data.keys():
        stuffObj.p_feature_text = stuff.p_data["FeatureText"]
    if "HP" in stuff.p_data.keys():
        stuffObj.p_hp_max = stuff.p_data["HP"]
        stuffObj.p_hp_current = stuff.p_data["HP"]
    if "Mags" in stuff.p_data.keys():
        stuffObj.p_mags = stuff.p_data["Mags"]
    if "Equipped" in stuff.p_data.keys():
        stuffObj.p_equipped = stuff.p_data["Equipped"]
    if "PropChange" in stuff.p_data.keys():
        pcData = stuff.p_data["PropChange"]
        stuffObj.p_prop_change = lcd.PropChangeField(pcData["Property"],pcData["Value"],pcData["DispName"],stuffObj.p_name)
    if "Slots" in stuff.p_data.keys():
        stuffObj.p_slot_max = stuff.p_data["Slots"]
    if "Uses" in stuff.p_data.keys():
        stuffObj.p_uses = stuff.p_data["Uses"]
    return stuffObj, extraData
    
def evalUnknownField(stuffObj, field, fieldValue):
    intCast = False
    reqInt = False
    try:
        if not isinstance(fieldValue,int):
            fieldValue = evaluate(statifyString(fieldValue)).item()
        intCast = True
    except:
        pass
    match field:
        case "Name":
            stuffObj.p_name = fieldValue
        case "Description":
            stuffObj.p_desc = fieldValue
        case "Armor":
            stuffObj.p_armor = fieldValue
        case "DescText":
            stuffObj.p_pc_desc_text = fieldValue
        case "DamageReduction":
            stuffObj.p_armor = fieldValue
        case "FeatureText":
            stuffObj.p_text = fieldValue
        case "HP":
            stuffObj.p_hp_max = fieldValue
            stuffObj.p_hp_current = fieldValue
            reqInt = True
        case "Mags":
            stuffObj.p_mags = fieldValue
            reqInt = True
        case "PropChange":
            stuffObj.p_prop_change = lcd.PropChangeField(prop["Property"],fieldValue,prop["DispName"],stuffObj.p_name)
            reqInt = True
        case "Slots":
            stuffObj.p_slot_max = fieldValue
            reqInt = True
        case "Uses":
            stuffObj.p_uses = fieldValue
            reqInt = True
        case _:
            st.write("Unknown field value: "+prop["Field"])
            return False
    return not intCast ^ reqInt
        
def getDamageObject(damageField):
    if isinstance(damageField,list):
        return [getDamageObject(damageEntry) for damageEntry in damageField]
    else:
        damageObject = lcd.DamageField()
        if "Damage" in damageField.keys():
            damageObject.p_damage = damageField["Damage"]
        if "Description" in damageField.keys():
            damageObject.p_desc = damageField["Description"]
        if "FireMode" in damageField.keys():
            damageObject.p_firemode = damageField["FireMode"]
        if "MechDamage" in damageField.keys():
            damageObject.p_mech_bonus = damageField["MechDamage"]
        return damageObject

#cache both of the functions that get json objects
@st.cache_data
def getJsonObject(objectName):
    with open('jsonDB/'+objectName, encoding='utf-8') as fh:
        jsonObject = json.loads(base64.b64decode(fh.read()).decode('utf-8'))
    return jsonObject
    
objectFieldDict = {"p_name": "Name","p_desc": "Description","p_sub_stuff": "Included item","p_prop_change": "Stat change","p_damage": "Damage","p_pc_desc_text": "Description text","p_uses": "Uses","p_equipped": "Equipped","p_armor": "Armor","p_slot_max": "Max slots","p_mags": "Mags","p_hp_max": "HP"}
damageFieldDict = {"p_damage": "Damage","p_desc": "Description","p_firemode": "Fire mode", "p_mech_bonus": "Deals double damage to mechanical targets"}
    
stuffDB = {k: processStuff(v) for k,v in getJsonObject("stuffDB").items()}
stuffTableDB = getJsonObject("stuffTables")
for table in list(stuffTableDB.keys()):
    stuffTableDB[table] = {k: processStuff(v) for k,v in stuffTableDB[table].items()}
fieldTableDB = getJsonObject("fieldTables")
shortStatTable = fieldTableDB["ShortStatTable"]
longStatTable = fieldTableDB["StatTable"]
errTextDB = fieldTableDB["ErrorText"]