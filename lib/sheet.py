import lib.util as lu
import lib.class_def as lcd
import streamlit as st
        
ic = lcd.ItemCounter()
firemodeStringDict = {"melee":"Melee<br />(+ Strength)","throw":"Thrown<br />(+ Strength)","single":"Single-shot<br />(+ Presence)","auto":"Autofire<br />(+ Agility)","remote":"Remote control<br />(+ Knowledge)"}

def clearCharCache(cacheType = "All"):
    saveToJson.clear()
    if cacheType == "All" or cacheType == "Stuff" or (isinstance(cacheType,list) and "Stuff" in cacheType):
        st.session_state.SheetAttributes.updateStuff(st.session_state.PC.pc_stuff)
        getFlatStuffList.clear()
        getCarryWeight.clear()
    
@st.cache_data
def saveToJson():
    if "PC" in st.session_state:
        return lcd.PC.Schema().dumps(st.session_state.PC)
    return None
    
@st.cache_resource
def getFlatStuffList(): 
    return st.session_state.SheetAttributes.flatStuffList
    
@st.cache_resource
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
        
def writeStuff(item, itemCounter = ic, prefix = None, isSubItem = False):
    itemID = str(ic.getNext())
    if prefix is not None:
        itemID = prefix + "_" + itemID
    with st.container(border=True):
        if isinstance(item,lcd.Feature):
            st.subheader("Feature", anchor=False)
        else:
            st.subheader(item.p_name, anchor=False)
            st.write(type(item).__name__)
        if not isSubItem:
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
            subcol1, subcol2, subcol3, subcol4 = st.columns([3,3,1,4],vertical_alignment="center")
            with subcol1:
                st.write("HP:")
            with subcol2:
                st.session_state["i_hp_current_"+itemID] = item.p_hp_current
                st.number_input("HP", key="i_hp_current_"+itemID, on_change=updateItem, args=[item,itemID], kwargs={"fieldType":"hp_current"}, step=1, min_value=0, label_visibility="collapsed")
            with subcol3:
                st.write("/", anchor=False)
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
            writeStuff(item.p_sub_stuff, itemCounter=itemCounter.getSubCounter(), prefix = itemID, isSubItem = True)
        if not isSubItem:
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
                    
def deleteItem(item, armor = False):
    st.session_state.PC.pc_stuff.remove(item)
    clearCharCache(cacheType = "Stuff")
    if armor:
        st.session_state.c_pc_equipped_armor = st.session_state.SheetAttributes.armorList[0]
        st.session_state.PC.equipNewArmor(st.session_state.c_pc_equipped_armor)