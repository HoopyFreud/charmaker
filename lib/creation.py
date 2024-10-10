from itertools import count
import lib.util as lu
import lib.class_def as lcd
import streamlit as st
import numexpr as ne
import json

#calculate the mod value for a given stat roll
def mapStatMod(stat):
    if isinstance(stat, int):
        if stat <= 4:
            return -3
        elif stat <= 6:
            return -2
        elif stat <= 8:
            return -1
        elif stat <= 12:
            return 0
        elif stat <= 14:
            return 1
        elif stat <= 16:
            return 2
        elif stat <= 20:
            return 3
        else:
            return None
    else:
        return None

def burnPCClass():
    if st.session_state.t_char_class:
        try:
            st.session_state.PC.pc_class = st.session_state.t_char_class
            st.session_state.class_table = processClassTable(getClassObject(mapClassTable[st.session_state.PC.pc_class]))
            st.session_state.PC.pc_glitch_roll = st.session_state.class_table["GlitchRoll"]
            return True
        except:
            return False
    return False

#calculate stat mods for raw stat rolls - return true if successful
def burnPCStats():
    try:
        c_stats = [st.session_state.t_char_agi, st.session_state.t_char_knw, st.session_state.t_char_pre, st.session_state.t_char_str, st.session_state.t_char_tou]
        c_stats = list(map(mapStatMod,[int(v) for v in c_stats]))
        if None in c_stats:
            return False
        st.session_state.PC.pc_agi, st.session_state.PC.pc_knw, st.session_state.PC.pc_pre, st.session_state.PC.pc_str, st.session_state.PC.pc_tou = c_stats
        return True
    except:
        return False

#calculate secondary stats - return true if successful
def burnPCSecondaryStats():
    try:
        c_s_stats = [st.session_state.t_char_hpmax,st.session_state.t_char_glitch,st.session_state.t_char_creds,st.session_state.t_char_debt]
        if None in c_s_stats:
            return False
        st.session_state.PC.pc_hp_max, st.session_state.PC.pc_glitch_current, st.session_state.PC.pc_creds, st.session_state.PC.pc_debt = [int(v) for v in c_s_stats]
        st.session_state.PC.pc_hp_max = max(1,st.session_state.PC.pc_hp_max)
        st.session_state.PC.pc_hp_current = st.session_state.PC.pc_hp_max
        st.session_state.PC.pc_glitch_roll = lu.statifyString(st.session_state.class_table["GlitchRoll"])
        st.session_state.PC.pc_carrying_max = ne.evaluate(lu.statifyString(st.session_state.class_table["CarryingCapacityRoll"])).item()
        return True
    except:
        return False

#calculate secondary stats - return true if successful
def burnPCDesc():
    try:
        st.session_state.PC.pc_name = st.session_state.t_char_name
        st.session_state.PC.pc_desc = st.session_state.t_char_style.capitalize()
        st.session_state.PC.pc_desc = st.session_state.PC.pc_desc + " " + st.session_state.PC.pc_class
        st.session_state.PC.pc_desc = st.session_state.PC.pc_desc + "; " + st.session_state.t_char_feature.lower()
        st.session_state.PC.pc_desc = st.session_state.PC.pc_desc + ", " + st.session_state.t_char_quirk.lower()
        st.session_state.PC.pc_desc = st.session_state.PC.pc_desc + lu.randomSelectWordTable(wordTableDB["PreFieldObsession"])
        st.session_state.PC.pc_desc = st.session_state.PC.pc_desc + " " + st.session_state.t_char_obsession.lower()
        st.session_state.PC.pc_desc = st.session_state.PC.pc_desc + lu.randomSelectWordTable(wordTableDB["PreFieldDesire"])
        st.session_state.PC.pc_desc = st.session_state.PC.pc_desc + " " + st.session_state.t_char_desire.lower()
        st.session_state.PC.pc_desc = st.session_state.PC.pc_desc + ".  \nYou owe money to " + st.session_state.t_char_lender.lower() + "."
        if "RandomClassLore" in st.session_state.class_table:
            st.session_state.PC.pc_desc = st.session_state.PC.pc_desc + "  \n" + st.session_state.class_table["RandomClassLorePrompt"] + " " + st.session_state.t_char_class_lore
        if "ClassLore" in st.session_state.class_table:
            st.session_state.PC.pc_desc = st.session_state.PC.pc_desc + "  \n" + st.session_state.class_table["ClassLore"]
        return True
    except:
        return False

#calculate secondary stats - return true if successful
def burnPCStuff():
    st.session_state.PC.pc_stuff = []
    enumStart = 0
    if "RandomClassStuff" in st.session_state.class_table.keys():
        enumStart = 1
        appendOrExtendStuffList(getStuffFromField(lcd.getEmptyRandomItem(),"0"))
    stuffList = st.session_state.class_table["Stuff"]
    if "ClassStuff" in st.session_state.class_table.keys():
        stuffList = st.session_state.class_table["ClassStuff"] + stuffList
    for stuffNumber,stuffItem in enumerate(stuffList, start=enumStart):
        appendOrExtendStuffList(getStuffFromField(stuffItem,str(stuffNumber)))
    if None in st.session_state.PC.pc_stuff:
        return False
    return True
    
#calculate secondary stats - return true if successful
def appendOrExtendStuffList(newStuff):
    if isinstance(newStuff,list):
        st.session_state.PC.pc_stuff.extend(newStuff)
    else:
        st.session_state.PC.pc_stuff.append(newStuff)
    
#calculate secondary stats - return true if successful
def traceStuff(entryID, subEntryID):
    stuffFieldObj = st.session_state[getOptionKey(entryID)]
    if not stuffFieldObj:
        st.session_state[getErrKey(entryID)] = True
        return None
    return getStuffFromField(stuffFieldObj, subEntryID)
    
def getStuffFromField(stuff, entryID):
    subPrefix = entryID
    subEntryID = subPrefix + "_0"
    if stuff.p_type == "StuffSet":
        returnList = []
        for stuffNumber,stuffItem in enumerate(stuff.p_data["StuffList"]):
            subEntryID = subPrefix + "_" + str(stuffNumber)
            returnList.append(getStuffFromField(stuffItem,subEntryID))
        if None in returnList:
            return None
        return returnList
    elif stuff.p_type == "RandomItem":
        return traceStuff(entryID, subEntryID)
    else:
        stuffObj = lu.generateObjectFromStuffField(stuff)
        if stuffObj is None:
            return None
        #look for sub-stuff
        if "SubStuff" in stuff.p_data.keys():
            stuffObj.p_sub_stuff = getStuffFromField(stuff.p_data["SubStuff"],subEntryID)
            if not stuffObj.p_sub_stuff:
                return None
        if "Unknown" in stuff.p_data.keys():
            if not getUnknownFieldValues(stuffObj,stuff.p_data["Unknown"],entryID): 
                return None
        return stuffObj
        
def getUnknownFieldValues(stuffObj,unknownPropList,entryID):
    errKey = getErrKey(entryID)
    errCheck = st.session_state[errKey]
    for propID, prop in enumerate(unknownPropList):
        propKey = getPropKey(entryID, str(propID))
        if prop["Entry"] == "FixedText":
            fieldValue = prop["Value"]
        else:
            fieldValue = st.session_state[propKey]
        if fieldValue is None:
            st.session_state[errKey] = True
            return False
        if prop["Entry"] != "Dropdown":
            try:
                fieldValue = ne.evaluate(lu.statifyString(fieldValue)).item()
            except:
                st.session_state[errKey] = True
                return False
        match prop["Field"]:
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
            case "Mags":
                stuffObj.p_mags = fieldValue
            case "PropChange":
                stuffObj.p_prop_change.append(lcd.PropChangeField(prop["Property"],fieldValue,prop["DispName"]))
            case "Slots":
                stuffObj.p_slot_max = fieldValue
            case "Uses":
                stuffObj.p_uses = fieldValue
            case _:
                st.write("Unknown field value: "+prop["Field"])
                st.session_state[errKey] = True
                return False
    return True
            
#process all stuff in each class table
def processClassTable(classTable):
    if "Stuff" in classTable.keys():
        classTable["Stuff"] = [lu.processStuff(stuffEntry) for stuffEntry in classTable["Stuff"]]
    if "ClassStuff" in classTable.keys():
        classTable["ClassStuff"] = [lu.processStuff(stuffEntry) for stuffIndex,stuffEntry in enumerate(classTable["ClassStuff"])]
    if "RandomClassStuff" in classTable.keys():
        classTable["RandomClassStuff"] = {k: lu.processStuff(v) for k,v in classTable["RandomClassStuff"].items()}
    if "StuffReplacement" in classTable.keys():
        classTable["StuffReplacement"] = {k: lu.processStuff(v) for k,v in classTable["StuffReplacement"].items()}
    return classTable

#replace a stuff entry with a different stuff entry that should replace it. Stuff replacement is by name.
def processStuffReplacement(stuffTableEntry):
    if stuffTableEntry.p_name in st.session_state.class_table["StuffReplacement"].keys():
        stuffTableEntry = lu.processStuff(st.session_state.class_table["StuffReplacement"][stuffTableEntry.p_name])
    return stuffTableEntry

def writeStuffSelection():
    enumStart = 0
    if "RandomClassStuff" in st.session_state.class_table.keys():
        enumStart = 1
        st.header(st.session_state.class_table["RandomClassStuffText"] + ":")
        entryID = "0"
        insertStuffEntry(lcd.getEmptyRandomItem(), entryID, customStuffTable = st.session_state.class_table["RandomClassStuff"])
        st.header("You also have:")
    else:
        st.header("You have:")
    stuffList = st.session_state.class_table["Stuff"]
    if "ClassStuff" in st.session_state.class_table.keys():
        stuffList = st.session_state.class_table["ClassStuff"] + stuffList
    for stuffNumber,stuffItem in enumerate(stuffList, start=enumStart):
        entryID = str(stuffNumber)
        insertStuffEntry(stuffItem, entryID)

#Insert a stuff entry into the character builder UI
def insertStuffEntry(stuff, entryID, customStuffTable = None):
    errKey = getErrKey(entryID)
    if errKey not in st.session_state:
        st.session_state[errKey] = False
    with st.container(border=True):
        writeFixedText(stuff)
        if "Unknown" in stuff.p_data.keys():
            writeUnknownFields(stuff, entryID)
        writeChildStuff(stuff, entryID, customStuffTable)
        #set up the error box
        if st.session_state[errKey]:
            st.error(lu.errTextDB["err_text_stuff"])
    
def getErrKey(entryID):
    return "stuffErr_" + entryID

def getOptionKey(entryID):
    return "t_stuffOption_" + entryID
    
def getPropKey(entryID, propID):
    return "t_stuffProp_" + entryID + "_" + propID

#fixed text is stuff like name and description - no lists, no unknowns, no subfields
def writeFixedText(stuff):
    if stuff.p_name:
        st.subheader(stuff.p_name)
    if "Description" in stuff.p_data.keys():
        st.write(stuff.p_data["Description"])
    if stuff.p_type == "Feature":
        if stuff.p_name:
            with st.container(border=True):
                st.subheader("Feature")
                st.write(stuff.p_data["FeatureText"])
        else:
            st.subheader("Feature")
            st.write(stuff.p_data["FeatureText"])
    if "Damage" in stuff.p_data.keys():
        if isinstance(stuff.p_data["Damage"],list):
            for damageInstance in stuff.p_data["Damage"]:
                writeDamage(damageInstance)
        else:
            writeDamage(stuff.p_data["Damage"])
    if stuff.p_type == "Armor":
        if "DamageReduction" in stuff.p_data.keys():
            st.write("Damage reduction: "+stuff.p_data["DamageReduction"])
    if stuff.p_type == "Infestation":
        st.markdown(":radioactive_sign:: "+stuff.p_data["Trigger"])
    if "DescText" in stuff.p_data.keys():
        st.markdown("_"+stuff.p_data["DescText"]+"_")

#write damage inside of a StuffFixedText call
def writeDamage(damageField):
    fireModeDict = {"melee": "Melee", "throw": "Thrown", "single": "Single-shot", "auto": "Autofire", "remote": "Remote control"}
    with st.container(border=True):
        if "Name" in damageField.keys():
            st.subheader(damageField["Name"])
        if "FireMode" in damageField.keys():
            if isinstance(damageField["FireMode"],list):
                st.write("/".join([fireModeDict[mode] for mode in damageField["FireMode"]]))
            else:
                st.write(fireModeDict[damageField["FireMode"]])
        if "Damage" in damageField.keys():
            st.write("Damage: "+damageField["Damage"])
        if "Mags" in damageField.keys():
            st.write("Mags: "+damageField["Mags"])
        if "Description" in damageField.keys():
            st.write(damageField["Description"])

#write unknown fields - stuff like mags and number of uses and undetermined bonuses
def writeUnknownFields(stuff, entryID):
    #need this to check for errors in multiple subfields on page load
    errKey = getErrKey(entryID)
    errCheck = st.session_state[errKey]
    for propID, prop in enumerate(stuff.p_data["Unknown"]):
        dispName = prop["Field"]+":"
        if "DispName" in prop.keys():
            dispName = prop["DispName"]+":"
        propKey = getPropKey(entryID, str(propID))
        if propKey not in st.session_state:
            st.session_state[propKey] = None
        #select data entry method
        st.write(dispName)
        if prop["Entry"] == "Number":
            rollString = lu.statifyString(prop["Value"])
            col1, col2 = st.columns([5,1],vertical_alignment="bottom")
            with col1:
                st.text_input(dispName, key=propKey, label_visibility="collapsed", placeholder=rollString, on_change=lu.changeNumInput, args=[propKey,errKey], kwargs={"roll": rollString})
            with col2:
                st.button('Random', key=propKey+"_random", on_click=lu.randomNumber, args=[propKey,rollString], kwargs={"errKey": errKey,"lowerLimit":1})
            #check for errors on page load
            errCheck = lu.changeNumInput(propKey,errKey,roll=rollString,override=errCheck)
        elif prop["Entry"] == "FixedText":
            with st.container(border=True):
                st.write(lu.statifyString(prop["Value"]))
        elif prop["Entry"] == "Dropdown":
            dropdownList = prop["Value"]
            rollString = "1d"+str(len(dropdownList))
            col1, col2 = st.columns([5,1],vertical_alignment="bottom")
            with col1:
                st.selectbox(dispName, dropdownList, format_func=(lambda entry: str(dropdownList.index(entry)+1)+" - "+entry), key=propKey, label_visibility="collapsed", index=None, placeholder=rollString, on_change=lu.resetErrField, args=[errKey])
            with col2:
                st.button('Random', key=propKey+"_random", on_click=lu.randomSelector, args=[propKey,dropdownList], kwargs={"errKey": errKey})

#write subfields - objects within the object
def writeChildStuff(stuff, entryID, customStuffTable):
    errKey = getErrKey(entryID)
    subPrefix = entryID
    subEntryID = subPrefix + "_0"
    #if the object is a list of things, give them each an entry
    if stuff.p_type == "StuffSet":
        for stuffNumber,stuffItem in enumerate(stuff.p_data["StuffList"]):
            subEntryID = subPrefix + "_" + str(stuffNumber)
            insertStuffEntry(stuffItem, subEntryID)
    elif stuff.p_type == "RandomItem":
        #set up the key if it doesn't already exist and get the table
        optionKey = getOptionKey(entryID)
        if optionKey not in st.session_state:
            st.session_state[optionKey] = None
        if customStuffTable:
            dropdownTable = customStuffTable
        else:
            dropdownTable = stuffTableDB[stuff.p_data["RandomTable"]]
        #restrict the table range based on the roll parameter if one exists
        if ("Roll" in stuff.p_data.keys() or "RollProp" in stuff.p_data.keys()):
            rollString = stuff.p_data["Roll"] if "Roll" in stuff.p_data.keys() else st.session_state.class_table[stuff.p_data["RollProp"]]
            dropdownTable = {k: v for k,v in dropdownTable.items() if int(k) in range(lu.rollMin(rollString),lu.rollMax(rollString)+1)}
        #execute stuff replacement
        if "StuffReplacement" in st.session_state.class_table.keys():
            dropdownTable = {k: processStuffReplacement(v) for k,v in dropdownTable.items()}
        #build the fields
        labelString = stuff.p_name if stuff.p_name else stuff.p_type
        dropdownList = list(dropdownTable.values())
        rollString = "1d"+str(len(dropdownList))
        col1, col2 = st.columns([5,1],vertical_alignment="bottom")
        with col1:
            selectedStuffObject = st.selectbox(labelString, dropdownList, format_func=(lambda entry: str(dropdownList.index(entry)+1)+" - "+entry.p_name), key=optionKey, index=None, placeholder=rollString, on_change=resetStuffSelector, args=[subEntryID,errKey], label_visibility="collapsed")
        with col2:
            st.button('Random', key=optionKey+"_random", on_click=lu.randomSelector, args=[optionKey,dropdownList], kwargs={"errKey": errKey})
        if selectedStuffObject:
            insertStuffEntry(selectedStuffObject, subEntryID)
    #SubStuff gets a double-name for the same reason as above
    elif "SubStuff" in stuff.p_data.keys():
        insertStuffEntry(stuff.p_data["SubStuff"], subEntryID)

#callback function for input changes to reset error unconditionally
def resetStuffSelector(subEntryID,errKey):
    for key in st.session_state.keys():
        if key.startswith("stuffErr_"+subEntryID) or key.startswith("t_stuffOption_"+subEntryID) or key.startswith("t_stuffProp_"+subEntryID):
            del st.session_state[key]
    lu.resetErrField(errKey)
    
    
def randomStats():
    st.session_state.t_char_agi = str(lu.roll(lu.statifyString(st.session_state.class_table["AgilityRoll"])))
    st.session_state.t_char_knw = str(lu.roll(lu.statifyString(st.session_state.class_table["KnowledgeRoll"])))
    st.session_state.t_char_pre = str(lu.roll(lu.statifyString(st.session_state.class_table["PresenceRoll"])))
    st.session_state.t_char_str = str(lu.roll(lu.statifyString(st.session_state.class_table["StrengthRoll"])))
    st.session_state.t_char_tou = str(lu.roll(lu.statifyString(st.session_state.class_table["ToughnessRoll"])))
    lu.changeNumInput("t_char_agi","err_text_stat")
    lu.changeNumInput("t_char_knw","err_text_stat")
    lu.changeNumInput("t_char_pre","err_text_stat")
    lu.changeNumInput("t_char_str","err_text_stat")
    lu.changeNumInput("t_char_tou","err_text_stat")
    
def randomSecondaryStats():
    st.session_state.t_char_hpmax = str(max(1,lu.roll(lu.statifyString(st.session_state.class_table["HPRoll"]))))
    st.session_state.t_char_glitch = str(lu.roll(lu.statifyString(st.session_state.class_table["GlitchRoll"])))
    st.session_state.t_char_creds = str(lu.roll(lu.statifyString(st.session_state.class_table["CreditsRoll"])))
    st.session_state.t_char_debt = str(lu.roll(lu.statifyString(st.session_state.class_table["DebtRoll"])))
    lu.changeNumInput("t_char_hpmax","err_text_secondary_stat")
    lu.changeNumInput("t_char_glitch","err_text_secondary_stat")
    lu.changeNumInput("t_char_creds","err_text_secondary_stat")
    lu.changeNumInput("t_char_debt","err_text_secondary_stat")
    
def randomDesc():
    st.session_state.t_char_name = lu.randomSelectWordTable(wordTableDB["Name"]).lower()
    st.session_state.t_char_style = lu.randomSelectWordTable(wordTableDB["Style"]).lower()
    st.session_state.t_char_feature = lu.randomSelectWordTable(wordTableDB["Feature"]).lower()
    st.session_state.t_char_quirk = lu.randomSelectWordTable(wordTableDB["Quirk"]).lower()
    st.session_state.t_char_obsession = lu.randomSelectWordTable(wordTableDB["Obsession"]).lower()
    st.session_state.t_char_desire = lu.randomSelectWordTable(wordTableDB["Desire"]).lower()
    st.session_state.t_char_lender = lu.randomSelectWordTable(wordTableDB["Lender"]).lower()
    if "RandomClassLore" in st.session_state.class_table.keys():
        st.session_state.t_char_class_lore = lu.randomSelectWordTable(st.session_state.class_table["RandomClassLore"])
    
@st.cache_data
def getClassObject(tableName: str):
    with open('jsonDB/classBaseClass.json', encoding='utf-8') as fh:
        classDict = json.load(fh)
    if tableName:
        with open('jsonDB/'+tableName, encoding='utf-8') as fh:
            newClassDict = json.load(fh)
            classDict.update(newClassDict)
    return classDict
    
mapClassTable = lu.fieldTableDB["ClassTableDict"]
stuffTableDB = lu.getJsonObject("stuffTables.json")
for table in list(stuffTableDB.keys()):
    stuffTableDB[table] = {k: lu.processStuff(v) for k,v in stuffTableDB[table].items()}
wordTableDB = lu.getJsonObject("wordTables.json")