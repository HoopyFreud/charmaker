import streamlit as st
import build_char as bc

def update_char():
    st.session_state.PC.pc_hp_current = st.session_state.c_pc_hp_current
    st.session_state.PC.pc_hp_max = st.session_state.c_pc_hp_max
    st.session_state.PC.pc_glitch_current = st.session_state.c_pc_glitch_current
    st.session_state.PC.pc_carrying_max = st.session_state.c_pc_carrying_max
    st.session_state.PC.pc_creds = st.session_state.c_pc_creds
    st.session_state.PC.pc_debt = st.session_state.c_pc_debt
    export_char.clear()
    
@st.cache_data
def export_char():
    if "PC" in st.session_state:
        return st.session_state.PC.as_yaml()
    return None