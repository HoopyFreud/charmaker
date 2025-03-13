import lib.util as lu
import lib.class_def as lcd
import streamlit as st
import re
import copy
        
firemodeStringDict = {"melee":"Melee<br />(+ Strength)","throw":"Thrown<br />(+ Strength)","single":"Single-shot<br />(+ Presence)","auto":"Autofire<br />(+ Agility)","remote":"Remote control<br />(+ Knowledge)"}
stuffTypeList = ["Ammo","App","Armor","Cyberdeck","Cyberware","Drug","Infestation","Item","Nano","Unit","Vehicle","Weapon"]

def clearCharCache(cacheType = "All"):
    if cacheType == "All" or cacheType == "Stuff" or (isinstance(cacheType,list) and "Stuff" in cacheType):
        st.session_state.SheetAttributes.updateStuff(st.session_state.PC.pc_stuff)
    
def saveToJson():
    if "PC" in st.session_state:
        return lcd.PC.Schema().dumps(st.session_state.PC)
    return None
    
def getFlatStuffList(): 
    return st.session_state.SheetAttributes.flatStuffList
    
def getCarryWeight(): 
    return str(st.session_state.SheetAttributes.currentCarry)

def updateChar(fieldType = "All", cacheType = "All"):
    if fieldType == "All" or fieldType == "stats":
        st.session_state.PC.pc_agi = st.session_state.c_pc_agi
        st.session_state.PC.pc_knw = st.session_state.c_pc_knw
        st.session_state.PC.pc_pre = st.session_state.c_pc_pre
        st.session_state.PC.pc_str = st.session_state.c_pc_str
        st.session_state.PC.pc_tou = st.session_state.c_pc_tou
    if fieldType == "All" or fieldType == "hp_current":
        st.session_state.PC.pc_hp_current = st.session_state.c_pc_hp_current
    if fieldType == "All" or fieldType == "hp_max":
        st.session_state.PC.pc_hp_max = st.session_state.c_pc_hp_max
    if fieldType == "All" or fieldType == "glitch_current":
        st.session_state.PC.pc_glitch_current = st.session_state.c_pc_glitch_current
    if fieldType == "All" or fieldType == "creds":
        st.session_state.PC.pc_creds = st.session_state.c_pc_creds
    if fieldType == "All" or fieldType == "debt":
        st.session_state.PC.pc_debt = st.session_state.c_pc_debt
    if fieldType == "All" or fieldType == "desc":
        st.session_state.PC.pc_desc = st.session_state.c_pc_desc
    if fieldType == "All" or fieldType == "equipped_armor":
        st.session_state.PC.equipNewArmor(st.session_state.c_pc_equipped_armor)
        cacheType = addCacheType(cacheType, "Stuff")
    clearCharCache(cacheType = cacheType)

def updateItem(item, itemID, fieldType = "All"):
    if fieldType == "All" or fieldType == "equipped":
        item.p_equipped = st.session_state["i_equipped_"+itemID]
    if fieldType == "All" or fieldType == "hp_current":
        item.p_hp_current = st.session_state["i_hp_current_"+itemID]
    if fieldType == "All" or fieldType == "hp_max":
        item.p_hp_max = st.session_state["i_hp_max_"+itemID]
    if fieldType == "All" or fieldType == "uses":
        item.p_uses = st.session_state["i_uses_"+itemID]
    if fieldType == "All" or fieldType == "mags":
        item.p_mags = st.session_state["i_mags_"+itemID]
    if fieldType == "All" or fieldType == "slots":
        #needs to be assigned first to avoid problems when changing number of max slots
        item.p_slots = [st.session_state["i_slots_" + itemID + "_" + str(i)] for i in range(item.p_slot_max)]
        item.p_slot_max = st.session_state["i_slots_"+itemID]
    clearCharCache(cacheType = "Stuff")
    
def addCacheType(oldType, newType):
    if isinstance(oldType,list):
        if newType not in oldType:
            oldType.append(newType)
    elif oldType != "All" and oldType != newType:
        if oldType is None:
            oldType = newType
        else:
            oldType = [oldType,newType]
    return oldType

def rollGlitch():
    st.session_state.c_pc_glitch_current = lu.roll(lu.statifyString(st.session_state.PC.pc_glitch_roll))
    updateChar(fieldType = "glitch_current", cacheType = None)

def updateEquippedArmor():
    st.session_state.PC.equipNewArmor(st.session_state.c_pc_equipped_armor)
    updateChar(fieldType = "equipped_armor")

def writeStuffDesc():
    featureStrings = []
    for item in getFlatStuffList():
        try:
            if item.p_pc_desc_text is not None:
                featureStrings.append(item.p_pc_desc_text)
        except:
            pass
    if featureStrings:
        for feature in featureStrings: st.write(feature)

def writeFeatures():
    featureStrings = []
    for item in getFlatStuffList():
        try:
            if item.p_feature_text is not None:
                featureStrings.append(item.p_feature_text)
        except:
            pass
    if featureStrings:
        st.header("Features:", anchor=False)
        for feature in featureStrings: st.write(feature)

def writeArmor():
    with st.container(border=True):
        st.subheader("Armor")
        st.selectbox("Armor", st.session_state.SheetAttributes.armorList, format_func=(lambda entry: entry.p_name), key="c_pc_equipped_armor", on_change=updateChar, kwargs={"fieldType":"equipped_armor","cacheType":None}, label_visibility="collapsed")
        item = st.session_state.c_pc_equipped_armor
        if item.p_equipped is None:
            st.write("No equip cost")
        if item.p_desc:
            st.write(item.p_desc)
        if hasattr(item,"p_armor") and item.p_armor is not None:
            st.write("Damage reduction: " + item.p_armor)
        if item.p_name != "No armor":
            with st.popover("Delete", use_container_width=True):
                st.write("Warning: deletion is **permanent**")
                st.button("Delete", key="del_armor", on_click=deleteItem, args=[item], kwargs={"armor":True}, use_container_width=True)
        
def writeStuff(item, itemCounter, prefix = None, invManagement = True, useBorder = True):
    itemID = str(itemCounter.getNext())
    if prefix is not None:
        itemID = prefix + "_" + itemID
    with st.container(border=useBorder):
        if isinstance(item,lcd.Feature):
            st.subheader("Feature", anchor=False)
        else:
            st.subheader(item.p_name, anchor=False)
            st.write(type(item).__name__)
        if invManagement:
            if hasattr(item,"p_equipped"):
                if item.p_equipped is not None:
                    col1, col2 = st.columns([3,1],vertical_alignment="center")
                    with col1:
                        st.write("Equipped:")
                    with col2:
                        st.session_state["i_equipped_"+itemID] = item.p_equipped
                        st.checkbox("Equipped", key="i_equipped_"+itemID, on_change=updateItem, args=[item,itemID], kwargs={"fieldType":"equipped"}, label_visibility="collapsed")
                else:
                    st.write("No equip cost")
        if hasattr(item,"p_desc") and item.p_desc is not None:
            st.write(item.p_desc)
        if hasattr(item,"p_feature_text") and item.p_feature_text is not None:
            st.write("_" + item.p_feature_text + "_")
        if hasattr(item,"p_hp_max") and item.p_hp_max is not None:
            subcol1, subcol2, subcol3, subcol4 = st.columns([2,3,1,3],vertical_alignment="center")
            with subcol1:
                st.write("HP:")
            with subcol2:
                st.session_state["i_hp_current_"+itemID] = item.p_hp_current
                st.number_input("HP", key="i_hp_current_"+itemID, on_change=updateItem, args=[item,itemID], kwargs={"fieldType":"hp_current"}, step=1, min_value=0, label_visibility="collapsed")
            with subcol3:
                st.write("/")
            with subcol4:
                st.session_state["i_hp_max_"+itemID] = item.p_hp_max
                st.number_input("HP", key="i_hp_max_"+itemID, on_change=updateItem, args=[item,itemID], kwargs={"fieldType":"hp_max"}, step=1, min_value=0, label_visibility="collapsed")
        if hasattr(item,"p_armor") and item.p_armor is not None:
            st.write("Armor: " + item.p_armor)
        if hasattr(item,"p_slot_max") and hasattr(item,"p_slots"):
            writeCyberdeckSlots(item, itemID)
        if hasattr(item,"p_pc_desc_text") and item.p_pc_desc_text is not None:
            st.write("_" + item.p_pc_desc_text + "_")
        if hasattr(item,"p_uses") and item.p_uses is not None:
            col1, col2 = st.columns([1,2.5],vertical_alignment="center")
            with col1:
                st.write("Uses:")
            with col2:
                st.session_state["i_uses_"+itemID] = item.p_uses
                st.number_input("Uses", key="i_uses_"+itemID, on_change=updateItem, args=[item,itemID], kwargs={"fieldType":"uses"}, step=1, min_value=0, label_visibility="collapsed")
        if hasattr(item,"p_damage") and item.p_damage is not None:
            writeDamageField(item.p_damage)
        if hasattr(item,"p_mags") and item.p_mags is not None:
            col1, col2 = st.columns([1,2.5],vertical_alignment="center")
            with col1:
                st.write("Mags:")
            with col2:
                st.session_state["i_mags_"+itemID] = item.p_mags
                st.number_input("Mags", key="i_mags_"+itemID, on_change=updateItem, args=[item,itemID], kwargs={"fieldType":"mags"}, step=1, min_value=0, label_visibility="collapsed")
        if hasattr(item,"p_sub_stuff") and item.p_sub_stuff is not None:
            itemCounter.getSubCounter().reset()
            if isinstance(item.p_sub_stuff,list):
                for subStuffItem in item.p_sub_stuff:
                    writeStuff(subStuffItem, itemCounter.getSubCounter(), prefix = itemID, invManagement = False)
            else:
                writeStuff(item.p_sub_stuff, itemCounter.getSubCounter(), prefix = itemID, invManagement = False)
        if invManagement:
            with st.popover("Delete", use_container_width=True):
                st.write("Warning: deletion is **permanent**")
                st.button("Delete", key="del_"+itemID, on_click=deleteItem, args=[item], use_container_width=True)
        
def writeDamageField(damageField):
    if isinstance(damageField,list):
        for damageFieldInstance in damageField:
            writeDamageField(damageFieldInstance)
    else:
        with st.container(border=True):
            if damageField.p_desc is not None:
                st.write(damageField.p_desc)
            if damageField.p_damage is not None:
                st.write("Damage: " + damageField.p_damage)
            if damageField.p_mech_bonus:
                st.write("Deals double damage to mechanical targets")
            if damageField.p_firemode is not None:
                if isinstance(damageField.p_firemode,list):
                    attackString = "<p style='margin:0'>Attack types:</p><ul>"
                    for mode in damageField.p_firemode:
                        attackString = attackString + "<li>" + firemodeStringDict[mode] + "</li>"
                    attackString = attackString + "</ul>"
                    st.write(attackString, unsafe_allow_html=True)
                else:
                    st.write("Attack type: " + firemodeStringDict[damageField.p_firemode], unsafe_allow_html=True)
                    
def writeCyberdeckSlots(item, itemID):
    col1, col2 = st.columns([1,1.5],vertical_alignment="center")
    with col1:
        st.write("Max slots:")
    with col2:
        st.session_state["i_slots_"+itemID] = item.p_slot_max
        st.number_input("Slots", key="i_slots_"+itemID, on_change=updateItem, args=[item,itemID], kwargs={"fieldType":"slots"}, step=1, min_value=0, label_visibility="collapsed")
    st.write("Slotted apps:")
    for i in range(item.p_slot_max):
        slotKey = "i_slots_" + itemID + "_" + str(i)
        if len(item.p_slots) > i:
            st.session_state[slotKey] = item.p_slots[i]
        else:
            st.session_state[slotKey] = None
        st.selectbox("Slot"+str(i), st.session_state.SheetAttributes.appList, index=None, placeholder="No app", format_func=(lambda entry: entry.p_name), key=slotKey, on_change=updateItem, args=[item,itemID], kwargs={"fieldType":"slots"}, label_visibility="collapsed")
        
def writeAddItem(itemCounter, suffix=""):
    st.subheader("Item type", anchor=False)
    stuffType = st.selectbox("Item type", stuffTypeList, index=None, key="t_add_item_type"+suffix, on_change=resetAddItem, kwargs={"stage":1}, label_visibility="collapsed")
    #itemList = list(filter(lambda entry:entry.p_type==stuffType,lu.stuffDB.values())) + [lcd.getCustomStuffField(stuffType)]
    itemList = list(filter(lambda entry:entry.p_type==stuffType,lu.stuffDB.values())) + [lcd.getCustomStuffField(stuffType)]
    if stuffType=="Armor":
        itemList = [itemEntry for itemEntry in itemList if itemEntry.p_name != "No armor"]
    if stuffType is not None:
        st.subheader("Item", anchor=False)
        selectItem = st.selectbox("Add item", itemList, index=None, format_func=lambda entry:entry.p_name, key="t_add_item_entry"+suffix, on_change=resetAddItem, kwargs={"stage":2}, disabled=(stuffType is None), label_visibility="collapsed")
        if selectItem is not None:
            if "add_obj" not in st.session_state or st.session_state.add_obj is None:
                st.session_state.add_obj = convertAndProcessFieldObj(selectItem)
            if selectItem.p_name is "Custom":
                st.divider()
                for prop in vars(st.session_state.add_obj):
                    if prop in lu.objectFieldDict:
                        propname = lu.objectFieldDict[prop]
                        col1, col2 = st.columns([1,1.5],vertical_alignment="center")
                        with col1:
                            st.write(propname)
                        with col2:
                            keyID = "c_custom_add_item_"+prop+suffix
                            if prop in ["p_name", "p_desc", "p_pc_desc_text", "p_armor"]:
                                st.text_input(propname, key=keyID, on_change=updateCustomAddItemField, args=[prop,keyID], value=None, label_visibility="collapsed")
                            elif prop in ["p_uses", "p_slot_max", "p_mags", "p_hp_max"]:
                                st.number_input(propname, key=keyID, on_change=updateCustomAddItemField, args=[prop,keyID], min_value=0, value=None, step=1, label_visibility="collapsed")
                col1, col2, col3 = st.columns([1,1,1],vertical_alignment="top")
                with col2:
                    with st.container(border=True):
                        disableAdd = False
                        writeStuff(st.session_state.add_obj, itemCounter, invManagement = False, useBorder = False)
                        if "SubStuff" in selectItem.p_data.keys():
                            prevCount = itemCounter.getNext() - 1
                            itemCounter.reset(resetVal = prevCount)
                            prevCount = str(prevCount)
                            disableAdd = writeAddSubStuff(selectItem, itemCounter.getSubCounter(), prevCount)
                        st.button("Add", key="add_new_item", on_click=addNewItem, disabled=disableAdd, use_container_width=True)
            else:
                col1, col2, col3 = st.columns([1,1,1],vertical_alignment="top")
                with col2:
                    with st.container(border=True):
                        disableAdd = False
                        writeStuff(st.session_state.add_obj, itemCounter, invManagement = False, useBorder = False)
                        if "SubStuff" in selectItem.p_data.keys():
                            prevCount = itemCounter.getNext() - 1
                            itemCounter.reset(resetVal = prevCount)
                            prevCount = str(prevCount)
                            disableAdd = writeAddSubStuff(selectItem, itemCounter.getSubCounter(), prevCount)
                        st.button("Add", key="add_new_item", on_click=addNewItem, disabled=disableAdd, use_container_width=True)
                
def updateCustomAddItemField(field,key):
    setattr(st.session_state.add_obj,field,st.session_state[key])
    
def convertAndProcessFieldObj(stuffFieldObj):
    selectObj,_ = lu.generateObjectFromStuffField(stuffFieldObj)
    if "Unknown" in stuffFieldObj.p_data.keys():
        for prop in stuffFieldObj.p_data["Unknown"]:
            lu.evalUnknownField(selectObj,prop["Field"],prop["Value"])
    return selectObj
    
def writeAddSubStuff(selectItem, itemCounter, prefix):
    disableAdd = False
    subStuff = selectItem.p_data["SubStuff"]
    if isinstance(subStuff,list):
        for subStuffItem in subStuff:
            disableAdd = disableAdd or writeAddSubStuff(subStuffItem, itemCounter, prefix)
    else:
        itemID = itemCounter.getNext()
        itemCounter.reset(resetVal = itemID)
        itemID = str(itemID)
        itemID = prefix + "_" + itemID
        objKey = "add_sub_obj_" + itemID
        if subStuff.p_type == "RandomItem":
            dropdownKey = "t_add_sub_item_" + itemID
            dropdownTable = lu.stuffTableDB[subStuff.p_data["RandomTable"]]
            if "Roll" in subStuff.p_data.keys():
                rollString = stuff.p_data["Roll"]
                dropdownTable = {k: v for k,v in dropdownTable.items() if int(k) in range(lu.rollMin(rollString),lu.rollMax(rollString)+1)}
            dropdownList = list(dropdownTable.values())
            rollString = "1d"+str(len(dropdownList))
            st.subheader(subStuff.p_name, anchor=False)
            selectSubStuff = st.selectbox(subStuff.p_name, dropdownList, format_func=(lambda entry: str(dropdownList.index(entry)+1)+" - "+entry.p_name), key=dropdownKey, index=None, placeholder=rollString, on_change=resetAddItem, kwargs={"itemID":itemID}, label_visibility="collapsed")
            st.button('Random', key=dropdownKey+"_random", on_click=chooseNewAddItemDropdown, args=[dropdownList, dropdownKey, itemID], use_container_width=True)
            subStuff = selectSubStuff
            if subStuff is None:
                return True
        if objKey not in st.session_state or st.session_state[objKey] is None:
            st.session_state[objKey] = convertAndProcessFieldObj(subStuff)
        writeStuff(st.session_state[objKey], itemCounter, prefix = prefix, invManagement = False)
        if "SubStuff" in subStuff.p_data.keys():
            itemCounter.getSubCounter().reset()
            disableAdd = writeAddSubStuff(subStuff, itemCounter.getSubCounter(), itemID)
    return disableAdd
    
def chooseNewAddItemDropdown(dropdownList, dropdownKey, itemID):
    resetAddItem(itemID=itemID)
    lu.randomSelector(dropdownKey, dropdownList)
    
def resetAddItem(stage = 3, itemID = None):
    for key in st.session_state.keys():
        if (
            (key=="t_add_item_type" and stage < 1) or 
            (key=="t_add_item_entry" and stage < 2) or 
            (stage < 3 and (
                key=="add_obj" or
                key.startswith("t_add_sub_item_") or
                key.startswith("add_sub_obj_")
            )) or
            (itemID is not None and key.startswith("add_sub_obj_" + itemID))
        ):
            st.session_state[key] = None
            
def addNewItem():
    if "add_obj" in st.session_state and st.session_state.add_obj is not None:
        newItemObject = copy.deepcopy(st.session_state.add_obj)
        subObjKeyList = [key for key in st.session_state.keys() if key.startswith("add_sub_obj_")]
        newItemObject.p_sub_stuff = recursiveSubStuffBuilder(subObjKeyList)
        st.session_state.PC.pc_stuff.append(newItemObject)
        resetAddItem(stage=0)
        clearCharCache(cacheType = "Stuff")
        
def recursiveSubStuffBuilder(keyList, keyRoot = None):
    if keyRoot is None:
        reFilterExp = re.compile("add_sub_obj_\d+_\d+")
    else:
        reFilterExp = re.compile(keyRoot + "_\d+")
    filterList = [key for key in keyList if reFilterExp.fullmatch(key) and st.session_state[key] is not None]
    if filterList:
        if len(filterList) == 1:
            filterKey = filterList[0]
            returnObject = copy.deepcopy(st.session_state[filterKey])
            returnObject.p_sub_stuff = recursiveSubStuffBuilder(keyList, keyRoot=filterKey)
            return returnObject
        else:
            returnList = []
            for filterKey in filterList:
                returnList.append(recursiveSubStuffBuilder(keyList, keyRoot=filterKey))
            return returnList
    return None
                
                    
def deleteItem(item, armor = False):
    st.session_state.PC.pc_stuff.remove(item)
    clearCharCache(cacheType = "Stuff")
    if armor:
        st.session_state.c_pc_equipped_armor = st.session_state.SheetAttributes.armorList[0]
        st.session_state.PC.equipNewArmor(st.session_state.c_pc_equipped_armor)