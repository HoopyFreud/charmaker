import lib.class_def as lcd
import streamlit as st
import yaml

def clearCharCache(cacheType = "All"):
    saveToJson.clear()
    if cacheType == "All" or cacheType == "Stuff" or "Stuff" in cacheType:
        getFlatStuffList.clear()
    
def loadFromYaml(yamlIO):
    return yaml.load(yamlIO, Loader=yaml.Loader)
    
@st.cache_data
def saveToJson():
    if "PC" in st.session_state:
        return lcd.PC.Schema().dumps(st.session_state.PC)
    return None
    
@st.cache_resource
def getFlatStuffList(): 
    return st.session_state.PC.flatStuffList()

def updateChar(cacheType = "All"):
    st.session_state.PC.pc_hp_current = st.session_state.c_pc_hp_current
    st.session_state.PC.pc_hp_max = st.session_state.c_pc_hp_max
    st.session_state.PC.pc_glitch_current = st.session_state.c_pc_glitch_current
    st.session_state.PC.pc_carrying_max = st.session_state.c_pc_carrying_max
    st.session_state.PC.pc_creds = st.session_state.c_pc_creds
    st.session_state.PC.pc_debt = st.session_state.c_pc_debt
    st.session_state.PC.pc_desc = st.session_state.c_pc_desc
    saveToJson.clear(cacheType = cacheType)

def displayStuffDesc():
    featureStrings = []
    for item in st.session_state.c_pc_flat_stuff_list:
        try:
            if item.p_pc_desc_text is not None:
                featureStrings.append(item.p_pc_desc_text)
        except:
            pass
    if featureStrings:
        for feature in featureStrings: st.write(feature)

def displayFeatures():
    featureStrings = []
    for item in st.session_state.c_pc_flat_stuff_list:
        try:
            if item.p_feature_text is not None:
                featureStrings.append(item.p_feature_text)
        except:
            pass
    if featureStrings:
        st.header("Features:", anchor=False)
        for feature in featureStrings: st.write(feature)