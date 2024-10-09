import lib.class_def as lcd
import streamlit as st
import yaml

def clearCharCache(cacheType = None):
    if cacheType is None or cacheType == "YAMLDump" or "YAMLDump" in cacheType:
        saveToYaml.clear()
    if cacheType is None or cacheType == "flatStuffList" or "flatStuffList" in cacheType:
        getFlatStuffList.clear()
    
def loadFromYaml(yamlIO):
    return yaml.load(yamlIO, Loader=yaml.Loader)
    
@st.cache_data
def saveToYaml():
    if "PC" in st.session_state:
        return yaml.dump(st.session_state.PC)
    return None
    
@st.cache_data
def getFlatStuffList():
    if "PC" in st.session_state:
        return yaml.dump(st.session_state.PC)
    return None

def updateChar(cacheType = None):
    st.session_state.PC.pc_hp_current = st.session_state.c_pc_hp_current
    st.session_state.PC.pc_hp_max = st.session_state.c_pc_hp_max
    st.session_state.PC.pc_glitch_current = st.session_state.c_pc_glitch_current
    st.session_state.PC.pc_carrying_max = st.session_state.c_pc_carrying_max
    st.session_state.PC.pc_creds = st.session_state.c_pc_creds
    st.session_state.PC.pc_debt = st.session_state.c_pc_debt
    saveToYaml.clear(cacheType = cacheType)

def displayFeatures():
    featureStrings = []
    for item in st.session_state.c_pc_flat_stuff_list:
        if isinstance(item,lcd.Feature):
            featureStrings.append(item.p_text)
    if featureStrings:
        st.header("Features:")
        for feature in featureStrings: st.write(feature)