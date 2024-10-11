import lib.class_def as lcd
import streamlit as st

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
        st.session_state.PC.pc_equipped_armor = st.session_state.c_pc_equipped_armor
    clearCharCache(cacheType = cacheType)

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

def writeStuff():
    st.header("Armor and weapons", anchor=False)
    col1, col2, col3 = st.columns([1,1,1],vertical_alignment="top")
    with col1:
        with st.container(border=True):
            equippedArmor = st.selectbox("Armor", st.session_state.SheetAttributes.armorList, index=None, format_func=(lambda entry: entry.p_name), key="c_pc_equipped_armor", on_change=updateChar, kwargs={"fieldType":"equipped_armor","cacheType":None}, label_visibility="collapsed")
            st.write(str(equippedArmor))
    for itemIndex,item in enumerate(st.session_state.SheetAttributes.weaponList, start=1):
        if itemIndex%3 == 0:
            col1, col2, col3 = st.columns([1,1,1],vertical_alignment="top")
            column = col1
        elif itemIndex%3 == 1:
            column = col2
        else:
            column = col3
        with column:
            with st.container(border=True):
                st.write(str(item))
    st.header("Items", anchor=False)
    for itemIndex,item in enumerate(st.session_state.SheetAttributes.itemList):
        if itemIndex%3 == 0:
            col1, col2, col3 = st.columns([1,1,1],vertical_alignment="top")
            column = col1
        elif itemIndex%3 == 1:
            column = col2
        else:
            column = col3
        with column:
            with st.container(border=True):
                st.write(str(item))
    st.header("Cyberware", anchor=False)
    for itemIndex,item in enumerate(st.session_state.SheetAttributes.cyberwareList):
        if itemIndex%3 == 0:
            col1, col2, col3 = st.columns([1,1,1],vertical_alignment="top")
            column = col1
        elif itemIndex%3 == 1:
            column = col2
        else:
            column = col3
        with column:
            with st.container(border=True):
                st.write(str(item))
    st.header("Nano power and infestations", anchor=False)
    for itemIndex,item in enumerate(st.session_state.SheetAttributes.nanoInfestationList):
        if itemIndex%3 == 0:
            col1, col2, col3 = st.columns([1,1,1],vertical_alignment="top")
            column = col1
        elif itemIndex%3 == 1:
            column = col2
        else:
            column = col3
        with column:
            with st.container(border=True):
                st.write(str(item))
    st.header("Apps", anchor=False)
    for itemIndex,item in enumerate(st.session_state.SheetAttributes.appList):
        if itemIndex%3 == 0:
            col1, col2, col3 = st.columns([1,1,1],vertical_alignment="top")
            column = col1
        elif itemIndex%3 == 1:
            column = col2
        else:
            column = col3
        with column:
            with st.container(border=True):
                st.write(str(item))
    st.header("Units and vehicles", anchor=False)
    for itemIndex,item in enumerate(st.session_state.SheetAttributes.unitList):
        if itemIndex%3 == 0:
            col1, col2, col3 = st.columns([1,1,1],vertical_alignment="top")
            column = col1
        elif itemIndex%3 == 1:
            column = col2
        else:
            column = col3
        with column:
            with st.container(border=True):
                st.write(str(item))