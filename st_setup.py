import st_function_lib as stl
import streamlit as st
import build_char as bc

def appSetupKeys():
    if "stage" not in st.session_state:
        st.session_state.stage = 0
        
    if "select_disable_class" not in st.session_state:
        st.session_state.select_disable_class = True
    if "select_disable_stat" not in st.session_state:
        st.session_state.select_disable_stat = True
    if "select_disable_secondary_stat" not in st.session_state:
        st.session_state.select_disable_secondary_stat = True
    if "select_disable_desc" not in st.session_state:
        st.session_state.select_disable_desc = True
    if "select_disable_stuff" not in st.session_state:
        st.session_state.select_disable_stuff = True
        
    if "PC" not in st.session_state:
        st.session_state.PC = bc.PC()
    if "class_table" not in st.session_state:
        st.session_state.class_table = stl.processClassTable(stl.getClassObject(None))
    
        
    if "t_char_class" not in st.session_state:
        st.session_state.t_char_class = None
    if "t_char_agi" not in st.session_state:
        st.session_state.t_char_agi = None
    if "t_char_knw" not in st.session_state:
        st.session_state.t_char_knw = None
    if "t_char_pre" not in st.session_state:
        st.session_state.t_char_pre = None
    if "t_char_str" not in st.session_state:
        st.session_state.t_char_str = None
    if "t_char_tou" not in st.session_state:
        st.session_state.t_char_tou = None
    if "t_char_hpmax" not in st.session_state:
        st.session_state.t_char_hpmax = None
    if "t_char_glitch" not in st.session_state:
        st.session_state.t_char_glitch = None
    if "t_char_creds" not in st.session_state:
        st.session_state.t_char_creds = None
    if "t_char_debt" not in st.session_state:
        st.session_state.t_char_debt = None
        
    if "err_text_class" not in st.session_state:
        st.session_state.err_text_class = False
    if "err_text_stat" not in st.session_state:
        st.session_state.err_text_stat = False
    if "err_text_secondary_stat" not in st.session_state:
        st.session_state.err_text_secondary_stat = False
    if "err_text_desc" not in st.session_state:
        st.session_state.err_text_desc = False