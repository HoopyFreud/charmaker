import lib_class_def as lcd
import lib_creation as lc
import streamlit as st
import dice
import re
import copy
import json
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
def resetErrField(errField):
    st.write("Resetting field: "+errField)
    st.session_state[errField] = False
    
#callback function for input changes to make sure they're numbers in a valid range - return values are also used in page initialization
def changeNumInput(key,errField,roll = None, override = False):
    try:
        val = st.session_state[key]
        if val:
            val = int(val)
            st.session_state[errField] = (False or override)
            if roll:
                if val > rollMax(roll) or val < rollMin(roll):
                    st.session_state[errField] = True
        else:
            st.session_state[errField] = (False or override)
    except:
        st.session_state[errField] = True
    return st.session_state[errField]
    
#random selection for arbitrary and specific fields
def randomSelector(key,selectList,errField = None):
    st.session_state[key] = random.choice(selectList)
    if errField:
        resetErrField(errField)
    
#random selection for arbitrary and specific fields
def randomSelectWordTable(table):
    randomEntry = random.choice(table)
    if isinstance(randomEntry,list):
        randomEntry = randomSelectWordTable(randomEntry)
    return randomEntry
    
def randomNumber(key,rollString,errField = None,lowerLimit = None):
    rollResult = roll(statifyString(rollString))
    if lowerLimit:
        rollResult = max(lowerLimit,rollResult)
    st.session_state[key] = str(rollResult)
    if errField:
        changeNumInput(key,errField,roll = rollString)

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

#turn JSON dictionaries into StuffField objects
def processStuff(stuff, source = None):
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
            stuffFieldObj.p_source = source
            if stuffName:
                stuffFieldObj.p_name = stuffName
        else:
            stuffFieldObj =  lcd.StuffField(stuffType,stuffName,stuff[stuffType],p_source=source)
            if stuffFieldObj.p_type == "StuffSet":
                stuffFieldObj.p_data["StuffList"] = [processStuff(subItem, source = source) for subItem in stuffFieldObj.p_data["StuffList"]]
            if "SubStuff" in stuffFieldObj.p_data.keys():
                stuffFieldObj.p_data["SubStuff"] = processStuff(stuffFieldObj.p_data["SubStuff"], source = source)
    else:
        stuffFieldObj = stuff
        if source:
            stuffFieldObj.p_source = source
    return stuffFieldObj
    
def generateObjectFromStuffField(stuff):
    match stuff.p_type:
        case "Ammo":
            stuffObj = lcd.Item()
        case "App":
            stuffObj = lcd.App()
        case "Armor":
            stuffObj = lcd.Armor()
        case "Cyberdeck":
            stuffObj = lcd.Cyberdeck()
        case "Cyberware":
            stuffObj = lcd.Cyberware()
        case "Drug":
            stuffObj = lcd.Item()
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
        
    if stuff.p_name:
        stuffObj.p_name = stuff.p_name
    if "Description" in stuff.p_data.keys():
        stuffObj.p_desc = stuff.p_data["Description"]
        
    if "Armor" in stuff.p_data.keys():
        stuffObj.p_armor = stuff.p_data["Armor"]
    if "DescText" in stuff.p_data.keys():
        stuffObj.p_pc_desc_text = stuff.p_data["DescText"]
    if "DamageReduction" in stuff.p_data.keys():
        stuffObj.p_armor = stuff.p_data["DamageReduction"]
    if "FeatureText" in stuff.p_data.keys():
        stuffObj.p_text = stuff.p_data["FeatureText"]
    if "HP" in stuff.p_data.keys():
        stuffObj.p_hp_max = fieldValue
        stuffObj.p_hp_current = fieldValue
    if "Mags" in stuff.p_data.keys():
        stuffObj.p_mags = stuff.p_data["Mags"]
    if "PropChange" in stuff.p_data.keys():
        stuffObj.p_prop_change.append(lcd.PropChangeField(stuff.p_data["PropChange"]["Property"],stuff.p_data["PropChange"]["Value"],stuff.p_data["PropChange"]["DispName"]))
    if "Slots" in stuff.p_data.keys():
        stuffObj.p_slot_max = stuff.p_data["Slots"]
    if "Uses" in stuff.p_data.keys():
        stuffObj.p_uses = stuff.p_data["Uses"]
    return stuffObj
        
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
        jsonObject = json.load(fh)
    return jsonObject
    
stuffDB = {k: processStuff(v) for k,v in getJsonObject("stuffDB.json").items()}
fieldTableDB = getJsonObject("fieldTables.json")
shortStatTable = fieldTableDB["ShortStatTable"]
longStatTable = fieldTableDB["StatTable"]
errTextDB = fieldTableDB["ErrorText"]