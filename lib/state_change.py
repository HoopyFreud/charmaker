from lib.setup import appSetupKeys
import lib.creation as lc
import lib.sheet as ls
import lib.class_def as lcd
import streamlit as st

def charReset():
    for key in st.session_state.keys():
        del st.session_state[key]
    appSetupKeys()
    st.session_state.stage = 1
    st.session_state.select_disable_class = False
    st.session_state.select_disable_stat = True
    st.session_state.select_disable_secondary_stat = True
    st.session_state.select_disable_desc = True
    st.session_state.select_disable_stuff = True
    st.session_state.select_disable_sheet_desc = True
    st.session_state.PC = lcd.PC()
    st.session_state.class_table = lc.processClassTable(lc.getClassObject(None))
    st.session_state.class_feature = None
    ls.clearCharCache()
    
def processCharUpload():
    if st.session_state.file_uploader_value:
        st.session_state.PC = ls.loadFromYaml(st.session_state.file_uploader_value)
        setStageView()
    
def finalizeClass():
    valid_class = lc.burnPCClass()
    if valid_class:
        st.session_state.stage = 2
        st.session_state.err_text_class = None
        st.session_state.select_disable_class = True
        st.session_state.select_disable_stat = False
        st.session_state.select_disable_secondary_stat = True
        st.session_state.select_disable_desc = True
        st.session_state.select_disable_stuff = True
        st.session_state.select_disable_sheet_desc = True
    else:
        st.session_state.err_text_class = True
    
def finalizeStats():
    valid_stats = lc.burnPCStats()
    if valid_stats:
        st.session_state.stage = 3
        st.session_state.select_disable_class = True
        st.session_state.select_disable_stat = True
        st.session_state.select_disable_secondary_stat = False
        st.session_state.select_disable_desc = True
        st.session_state.select_disable_stuff = True
        st.session_state.select_disable_sheet_desc = True
    else:
        st.session_state.err_text_stat = True
        
def finalizeSecondaryStats():
    valid_secondary_stats = lc.burnPCSecondaryStats()
    if valid_secondary_stats:
        st.session_state.err_text_secondary_stat = None
        st.session_state.stage = 4
        st.session_state.select_disable_class = True
        st.session_state.select_disable_stat = True
        st.session_state.select_disable_secondary_stat = True
        st.session_state.select_disable_desc = False
        st.session_state.select_disable_stuff = True
        st.session_state.select_disable_sheet_desc = True
    else:
        st.session_state.err_text_secondary_stat = True
        
def finalizeDesc():
    valid_desc = lc.burnPCDesc()
    if valid_desc:
        st.session_state.err_text_stuff = False
        st.session_state.stage = 5
        st.session_state.select_disable_class = True
        st.session_state.select_disable_stat = True
        st.session_state.select_disable_secondary_stat = True
        st.session_state.select_disable_desc = True
        st.session_state.select_disable_stuff = False
        st.session_state.select_disable_sheet_desc = True
    else:
        st.session_state.err_text_desc = True
        
def finalizeStuff():
    valid_stuff = lc.burnPCStuff()
    if valid_stuff:
        setStageView()
        
def setStageView():
    st.session_state.stage = -1
    st.session_state.select_disable_class = True
    st.session_state.select_disable_stat = True
    st.session_state.select_disable_secondary_stat = True
    st.session_state.select_disable_desc = True
    st.session_state.select_disable_stuff = True
    st.session_state.select_disable_sheet_desc = True
    ls.clearCharCache()
        
def sheetEditDesc():
    st.session_state.stage = -2
    st.session_state.select_disable_class = True
    st.session_state.select_disable_stat = True
    st.session_state.select_disable_secondary_stat = True
    st.session_state.select_disable_desc = True
    st.session_state.select_disable_stuff = True
    st.session_state.select_disable_sheet_desc = False
        
def sheetSaveDesc():
    ls.updateChar()
    setStageView()