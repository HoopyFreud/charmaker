from lib.setup import appSetupKeys
import lib.creation as lc
import lib.sheet as ls
import lib.class_def as lcd
import streamlit as st
import json

def charReset():
    for key in st.session_state.keys():
        del st.session_state[key]
    appSetupKeys()
    st.session_state.stage = 1
    st.session_state.PC = lcd.PC()
    st.session_state.class_table = lc.processClassTable(lc.getClassObject(None))
    st.session_state.class_feature = None
    ls.clearCharCache()
    
def processCharUpload():
    if st.session_state.file_uploader_value:
        charObject = json.load(st.session_state.file_uploader_value)
        st.session_state.PC = lcd.PC.Schema().load(charObject)
        setStageView()
    
def finalizeClass():
    valid_class = lc.burnPCClass()
    if valid_class:
        st.session_state.stage = 2
    else:
        st.session_state.err_text_class = True
    
def finalizeStats():
    valid_stats = lc.burnPCStats()
    if valid_stats:
        st.session_state.stage = 3
    else:
        st.session_state.err_text_stat = True
        
def finalizeSecondaryStats():
    valid_secondary_stats = lc.burnPCSecondaryStats()
    if valid_secondary_stats:
        st.session_state.err_text_secondary_stat = None
        st.session_state.stage = 4
    else:
        st.session_state.err_text_secondary_stat = True
        
def finalizeDesc():
    valid_desc = lc.burnPCDesc()
    if valid_desc:
        st.session_state.err_text_desc = False
        st.session_state.stage = 5
    else:
        st.session_state.err_text_desc = True
        
def finalizeStuff():
    valid_stuff = lc.burnPCStuff()
    if valid_stuff:
        setStageView()
        
def setStageView():
    st.session_state.stage = -1
    ls.clearCharCache()
        
def sheetEditDesc():
    st.session_state.stage = -2
        
def sheetSaveDesc():
    ls.updateChar()
    setStageView()