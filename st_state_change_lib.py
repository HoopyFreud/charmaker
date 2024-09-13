import st_function_lib as stl
import streamlit as st
import build_char as bc

def charReset():
    st.session_state.stage = 1
    st.session_state.select_disable_class = False
    st.session_state.select_disable_stat = True
    st.session_state.select_disable_secondary_stat = True
    st.session_state.select_disable_stuff = True
    st.session_state.PC = bc.PC()
    st.session_state.class_table = stl.processClassTable(stl.getClassObject(None))
    st.session_state.class_feature = None
    
def finalizeClass():
    if st.session_state.t_char_class:
        st.session_state.stage = 2
        st.session_state.PC.pc_class = st.session_state.t_char_class
        st.session_state.err_text_class = None
        st.session_state.select_disable_class = True
        st.session_state.select_disable_stat = False
        st.session_state.select_disable_secondary_stat = True
        st.session_state.select_disable_stuff = True
        st.session_state.class_table = stl.processClassTable(stl.getClassObject(stl.mapClassTable(st.session_state.PC.pc_class)))
    else:
        st.session_state.err_text_class = True
    
def finalizeStats():
    valid_stats = stl.burnPCStats()
    if valid_stats:
        st.session_state.stage = 3
        st.session_state.select_disable_class = True
        st.session_state.select_disable_stat = True
        st.session_state.select_disable_secondary_stat = False
        st.session_state.select_disable_stuff = True
    else:
        st.session_state.err_text_stat = True
        
def finalizeSecondaryStats():
    valid_secondary_stats = stl.burnPCSecondaryStats()
    if valid_secondary_stats:
        st.session_state.err_text_secondary_stat = None
        st.session_state.stage = 4
        st.session_state.select_disable_class = True
        st.session_state.select_disable_stat = True
        st.session_state.select_disable_secondary_stat = True
        st.session_state.select_disable_stuff = False
    else:
        st.session_state.err_text_secondary_stat = True
        
def finalizeStuff():
    valid_stuff = stl.burnPCStuff()
    if valid_stuff:
        st.session_state.err_text_stuff = False
        st.session_state.stage = 5
        st.session_state.select_disable_class = True
        st.session_state.select_disable_stat = True
        st.session_state.select_disable_secondary_stat = True
        st.session_state.select_disable_stuff = True
    else:
        st.session_state.err_text_secondary_stat = True