import streamlit as st
import build_char as bc
import numexpr as ne
import dice
import re
import copy
import json
import functools
import random
    
#placeholder
def fullRandGen():
    return True

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

#map between internal and display names for classes
def mapClassTable(className: str):
    classTableDict = getJsonObject('classTableDict.json')
    return classTableDict[className]

#process strings with special characters and replace them with stat values
def statifyString(in_string):
    stat_vals = [st.session_state.PC.pc_agi, st.session_state.PC.pc_knw, st.session_state.PC.pc_pre, st.session_state.PC.pc_str, st.session_state.PC.pc_tou]
    stat_short_strings = ["_a","_k","_p","_s","_t"]
    stat_long_string = getJsonObject('statTable.json')
    sign_vec = ["+"] * 5
    inv_sign_vec = ["-"] * 5
    string_vec = [None] * 5
    for index, stat_val in enumerate(stat_vals):
        if stat_val == None:
            string_vec[index] = stat_long_string[index]
        else:
            if stat_val == 0:
                string_vec[index] = ""
                sign_vec[index] = ""
                inv_sign_vec[index] = ""
            else:
                string_vec[index] = str(abs(stat_val))
                if stat_val < 0:
                    sign_vec[index] = "-"
                    inv_sign_vec[index] = "+"
        
        #adding mods
        in_string = re.sub("(\+"+stat_short_strings[index]+")",sign_vec[index]+string_vec[index],in_string)
        #subtracting mods
        in_string = re.sub("(-"+stat_short_strings[index]+")",inv_sign_vec[index]+string_vec[index],in_string)
        #mod as the first value
        in_string = re.sub("("+stat_short_strings[index]+")",string_vec[index],in_string)
        if stat_val is not None:
            if stat_val == 0:
                in_string = re.sub("("+stat_short_strings[index]+")","",in_string)
            elif stat_val < 0:
                in_string = re.sub("("+stat_short_strings[index]+")","-"+string_vec[index],in_string)
    return in_string

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

#calculate stat mods for raw stat rolls - return true if successful
def burnPCStats():
    try:
        c_stats = [st.session_state.t_char_agi, st.session_state.t_char_knw, st.session_state.t_char_pre, st.session_state.t_char_str, st.session_state.t_char_tou]
        c_stats = list(map(mapStatMod,[int(v) for v in c_stats]))
        if None in c_stats:
            return False
        else:
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
        else:
            st.session_state.PC.pc_hp_max, st.session_state.PC.pc_glitch_current, st.session_state.PC.pc_creds, st.session_state.PC.pc_debt = [int(v) for v in c_s_stats]
            st.session_state.PC.pc_hp_max = max(1,st.session_state.PC.pc_hp_max)
            st.session_state.PC.pc_hp_current = st.session_state.PC.pc_hp_max
            st.session_state.PC.pc_glitch_roll = statifyString(st.session_state.class_table["GlitchRoll"])
            st.session_state.PC.pc_carrying_max = ne.evaluate(statifyString(st.session_state.class_table["CarryingCapacityRoll"])).item()
            return True
    except:
        return False

#calculate secondary stats - return true if successful
def burnPCStuff():
    if "RandomClassStuff" in st.session_state.class_table.keys():
        traceStuff("RandomClassStuff")
    
#calculate secondary stats - return true if successful
def traceStuff(prefix):
    stuffFieldObj = st.session_state["t_"+prefix]
    st.write(prefix)
    st.write(stuffFieldObj.as_dict())
    if stuffFieldObj.p_source:
        objectSource = stuffFieldObj.p_source
    if "SubStuff" in stuffFieldObj.p_data.keys():
        if stuffFieldObj.p_type == "Cyberware":
            tracedObj.p_sub_stuff = traceStuff(newPrefix)
        elif stuffFieldObj.p_type == "Nano":
            tracedObj.p_infestation = traceStuff(newPrefix)
            
def getObjectFromStuffField(stuff):
    match stuff.p_type:
        case "Feature":
            tracedObj = bc.Feature()
        case "Nano":
            tracedObj = bc.Nano()
        case "Infestation":
            tracedObj = bc.Infestation()
        case "App":
            tracedObj = bc.App()
        case "Unit":
            tracedObj = bc.Unit()
        case "Vehicle":
            tracedObj = bc.Vehicle()
        case "Item":
            tracedObj = bc.Item()
        case "Weapon":
            tracedObj = bc.Weapon()
        case "Cyberware":
            tracedObj = bc.Cyberware()
        case "Cyberdeck":
            tracedObj = bc.Cyberdeck()
        case _:
            tracedObj = None
    if tracedObj:
        if stuff.p_name:
            tracedObj.p_name = stuff.p_name
        if "Description" in stuff.p_data.keys():
            tracedObj.p_desc = stuff.p_data["Description"]
    else:
        st.write(stuff.p_name)
            
#process all stuff in each class table
def processClassTable(classTable):
    if "Stuff" in classTable.keys():
        classTable["Stuff"] = [processStuff(stuffEntry, source = "Stuff") for stuffEntry in classTable["Stuff"]]
    if "ClassStuff" in classTable.keys():
        #we add a number to the source here to ensure that we will be able to set up unique IDs for these fields later. Stuff is already uniquely identified and RandomClassStuff is a single field, so neither of them need it.
        classTable["ClassStuff"] = [processStuff(stuffEntry, source = "ClassStuff"+"."+str(stuffIndex)) for stuffIndex,stuffEntry in enumerate(classTable["ClassStuff"])]
    if "RandomClassStuff" in classTable.keys():
        classTable["RandomClassStuff"] = {k: processStuff(v, source = "RandomClassStuff") for k,v in classTable["RandomClassStuff"].items()}
    if "StuffReplacement" in classTable.keys():
        classTable["StuffReplacement"] = {k: processStuff(v) for k,v in classTable["StuffReplacement"].items()}
    return classTable

#turn JSON dictionaries into StuffField objects
def processStuff(stuff, source = None):
    if not isinstance(stuff, bc.StuffField):
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
            stuffFieldObj =  bc.StuffField(stuffType,stuffName,stuff[stuffType],p_source=source)
            if stuffFieldObj.p_type == "StuffSet":
                stuffFieldObj.p_data["StuffList"] = [processStuff(subItem, source = source) for subItem in stuffFieldObj.p_data["StuffList"]]
            if "SubStuff" in stuffFieldObj.p_data.keys():
                stuffFieldObj.p_data["SubStuff"] = processStuff(stuffFieldObj.p_data["SubStuff"], source = source)
    else:
        stuffFieldObj = stuff
        if source:
            stuffFieldObj.p_source = source
    return stuffFieldObj

#replace a stuff entry with a different stuff entry that should replace it. Stuff replacement is by name.
def processStuffReplacement(stuffTableEntry):
    if stuffTableEntry.p_name in st.session_state.class_table["StuffReplacement"].keys():
        stuffTableEntry = processStuff(st.session_state.class_table["StuffReplacement"][stuffTableEntry.p_name], source=stuffTableEntry.p_source)
    return stuffTableEntry

#Insert a stuff entry into the character builder UI
#the prefix we pass into the sub-builders is just the prefix we get
#at top level this will be the name of the character sheet *field* we are filling out
#ie gear3, or ClassStuff.1
def insertStuffEntry(stuff, prefix = None, customStuffTable = None):
    st.session_state["err_text_"+prefix] = False
    with st.container(border=True):
        writeStuffFixedText(stuff)
        if "Unknown" in stuff.p_data.keys():
            writeStuffUnknownFields(stuff, prefix)
        writeStuffChildStuff(stuff, prefix, customStuffTable)
        #set up the error box
        if st.session_state["err_text_"+prefix]:
            st.error(err_text["err_text_stuff"])

#fixed text is stuff like name and description - no lists, no unknowns, no subfields
def writeStuffFixedText(stuff):
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
def writeStuffUnknownFields(stuff, prefix):
    #need this to check for errors in multiple subfields on page load
    errCheck = False
    for prop in stuff.p_data["Unknown"]:
        dispName = prop["Field"]+":"
        if "DispName" in prop.keys():
            dispName = prop["DispName"]+":"
        #session state key is built from the parent element's viewstate key, plus the name of the *object* that the field belongs to, plus the name of the field
        #note that part 2 is omitted if it does not exist
        #this means that if we change the name of the object (by selecting a new one) the error state should not persist
        keyName = prefix
        if stuff.p_name:
            keyName = keyName+"."+stuff.p_name
        keyName = keyName+"."+prop["Field"]
        if "t_"+keyName not in st.session_state:
            st.session_state["t_"+keyName] = None
        #select data entry method
        st.write(dispName)
        if prop["Entry"] == "Number":
            rollString = statifyString(prop["Value"])
            col1, col2 = st.columns([5,1],vertical_alignment="bottom")
            with col1:
                st.text_input(dispName, key = "t_"+keyName, label_visibility="collapsed", placeholder=rollString, on_change=changeNumInput, args=["t_"+keyName,"err_text_"+prefix], kwargs={"roll": rollString}, disabled=st.session_state.select_disable_stuff)
            with col2:
                st.button('Random', key = keyName+"_random", on_click = randomNumber, args=["t_"+keyName,rollString], kwargs={"errField": "err_text_"+prefix,"lowerLimit":1}, disabled=st.session_state.select_disable_stuff)
            #check for errors on page load
            errCheck = changeNumInput("t_"+keyName,"err_text_"+prefix,roll = rollString,override=errCheck)
        elif prop["Entry"] == "FixedText":
            with st.container(border=True):
                st.write(statifyString(prop["Value"]))
        elif prop["Entry"] == "Dropdown":
            dropdownList = prop["Value"]
            rollString = "1d"+str(len(dropdownList))
            col1, col2 = st.columns([5,1],vertical_alignment="bottom")
            with col1:
                st.selectbox(dispName, dropdownList, format_func=(lambda entry: str(dropdownList.index(entry)+1)+" - "+entry), key="t_"+keyName, label_visibility="collapsed", index=None, placeholder=rollString, disabled=st.session_state.select_disable_stuff)
            with col2:
                st.button('Random', key = keyName+"_random", on_click = randomSelector, args=["t_"+keyName,dropdownList], disabled=st.session_state.select_disable_stuff)

#write subfields - objects within the object
def writeStuffChildStuff(stuff, prefix, customStuffTable):
    #if the object is a list of things, give them each an entry
    #the prefix should just be the parent prefix with a .index inserted for uniqueness
    if stuff.p_type == "StuffSet":
        setPrefix = prefix+"."+stuff.p_name if stuff.p_name else prefix+"."+prefix
        for subIndex, stuffItem in enumerate(stuff.p_data["StuffList"]):
            insertStuffEntry(stuffItem, prefix = setPrefix+"."+str(subIndex))
    #if the object is a random item, create a selectbox for it
    #the session state ID for the selector should be the parent's prefix, plus the random table we consult. The subprefix will be the same as the state ID selector, UNLESS there is no random table given, in which case we repeat the prefix again
    #this sounds insane, but!
    #for the key, we want to avoid name clashes with cousin objects from different tables with the same name. For the prefix, we want to avoid name clashes with the parent.
    elif stuff.p_type == "RandomItem":
        keyName = prefix+"."+stuff.p_data["RandomTable"] if "RandomTable" in stuff.p_data.keys() else prefix
        subPrefix = prefix+"."+stuff.p_data["RandomTable"] if "RandomTable" in stuff.p_data.keys() else prefix+"."+prefix
        #set up the key if it doesn't already exist and get the table
        if "t_"+keyName not in st.session_state:
            st.session_state["t_"+keyName] = None
        if customStuffTable:
            dropdownTable = customStuffTable
        else:
            dropdownTable = stuffTableDB[stuff.p_data["RandomTable"]]
        #restrict the table range based on the roll parameter if one exists
        if ("Roll" in stuff.p_data.keys() or "RollProp" in stuff.p_data.keys()):
            rollString = stuff.p_data["Roll"] if "Roll" in stuff.p_data.keys() else st.session_state.class_table[stuff.p_data["RollProp"]]
            dropdownTable = {k: v for k,v in dropdownTable.items() if int(k) in range(rollMin(rollString),rollMax(rollString)+1)}
        #execute stuff replacement
        if "StuffReplacement" in st.session_state.class_table.keys():
            dropdownTable = {k: processStuffReplacement(v) for k,v in dropdownTable.items()}
        #build the fields
        labelString = stuff.p_name if stuff.p_name else stuff.p_type
        dropdownList = list(dropdownTable.values())
        rollString = "1d"+str(len(dropdownList))
        col1, col2 = st.columns([5,1],vertical_alignment="bottom")
        with col1:
            st.selectbox(labelString, dropdownList, format_func=(lambda entry: str(dropdownList.index(entry)+1)+" - "+entry.p_name), key="t_"+keyName, index=None, placeholder=rollString, label_visibility="collapsed", disabled=st.session_state.select_disable_stuff)
        with col2:
            st.button('Random', key = keyName+"_random", on_click = randomSelector, args=["t_"+keyName,dropdownList], disabled=st.session_state.select_disable_stuff)
        if st.session_state["t_"+keyName]:
            selectedStuffObject = st.session_state["t_"+keyName]
            insertStuffEntry(selectedStuffObject, prefix = subPrefix)
    #SubStuff gets a double-name for the same reason as above
    if "SubStuff" in stuff.p_data.keys():
        insertStuffEntry(stuff.p_data["SubStuff"], prefix = prefix+"."+prefix)

#callback function for input changes to make sure they're numbers in a valid range - return values are also used in page initialization
def changeNumInput(key,err_field,roll = None, override = False):
    try:
        val = st.session_state[key]
        if val:
            val = int(val)
            st.session_state[err_field] = (False or override)
            if roll:
                if val > rollMax(roll) or val < rollMin(roll):
                    st.session_state[err_field] = True
        else:
            st.session_state[err_field] = (False or override)
    except:
        st.session_state[err_field] = True
    return st.session_state[err_field]
    
#random selection for arbitrary and specific fields
def randomSelector(key,selectList):
    st.session_state[key] = random.choice(selectList)
    
def randomNumber(key,rollString,errField = None,lowerLimit = None):
    rollResult = roll(statifyString(rollString))
    if lowerLimit:
        rollResult = max(lowerLimit,rollResult)
    st.session_state[key] = str(rollResult)
    if errField:
        changeNumInput(key,errField,roll = rollString)
    
def randomStats():
    st.session_state.t_char_agi = str(roll(statifyString(st.session_state.class_table["AgilityRoll"])))
    st.session_state.t_char_knw = str(roll(statifyString(st.session_state.class_table["KnowledgeRoll"])))
    st.session_state.t_char_pre = str(roll(statifyString(st.session_state.class_table["PresenceRoll"])))
    st.session_state.t_char_str = str(roll(statifyString(st.session_state.class_table["StrengthRoll"])))
    st.session_state.t_char_tou = str(roll(statifyString(st.session_state.class_table["ToughnessRoll"])))
    changeNumInput("t_char_agi","err_text_stat")
    changeNumInput("t_char_knw","err_text_stat")
    changeNumInput("t_char_pre","err_text_stat")
    changeNumInput("t_char_str","err_text_stat")
    changeNumInput("t_char_tou","err_text_stat")
    
def randomSecondaryStats():
    st.session_state.t_char_hpmax = str(max(1,roll(statifyString(st.session_state.class_table["HPRoll"]))))
    st.session_state.t_char_glitch = str(roll(statifyString(st.session_state.class_table["GlitchRoll"])))
    st.session_state.t_char_creds = str(roll(statifyString(st.session_state.class_table["CreditsRoll"])))
    st.session_state.t_char_debt = str(roll(statifyString(st.session_state.class_table["DebtRoll"])))
    changeNumInput("t_char_hpmax","err_text_secondary_stat")
    changeNumInput("t_char_glitch","err_text_secondary_stat")
    changeNumInput("t_char_creds","err_text_secondary_stat")
    changeNumInput("t_char_debt","err_text_secondary_stat")

#cache both of the functions that get json objects
@functools.cache
def getJsonObject(objectName):
    with open('jsonDB/'+objectName, encoding='utf-8') as fh:
        jsonObject = json.load(fh)
    return jsonObject
    
@functools.cache
def getClassObject(tableName: str):
    with open('jsonDB/classBaseClass.json', encoding='utf-8') as fh:
        classDict = json.load(fh)
    if tableName:
        with open('jsonDB/'+tableName, encoding='utf-8') as fh:
            newClassDict = json.load(fh)
            classDict.update(newClassDict)
    return classDict
    

err_text = {"err_text_stat": "Enter valid stat rolls", "err_text_class": "Select a class", "err_text_secondary_stat": "Enter valid secondary stat rolls", "err_text_stuff": "Invalid field entry"}
stuffDB = {k: processStuff(v) for k,v in getJsonObject("stuffDB.json").items()}
stuffTableDB = getJsonObject("stuffTables.json")
for table in list(stuffTableDB.keys()):
    stuffTableDB[table] = {k: processStuff(v, source = table) for k,v in stuffTableDB[table].items()}