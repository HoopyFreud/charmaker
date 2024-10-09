import st_function_lib as stl
import streamlit as st
import build_char as bc
import st_render_char_lib as strc

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
        strc.export_char.clear()
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
        
def appUpdatePC():
    st.session_state.c_pc_hp_current = st.session_state.PC.pc_hp_current
    st.session_state.c_pc_hp_max = st.session_state.PC.pc_hp_max
    st.session_state.c_pc_glitch_current = st.session_state.PC.pc_glitch_current
    st.session_state.c_pc_carrying_max = st.session_state.PC.pc_carrying_max
    st.session_state.c_pc_creds = st.session_state.PC.pc_creds
    st.session_state.c_pc_debt = st.session_state.PC.pc_debt
    
def appCSS():
    primaryColor = st.get_option("theme.primaryColor")
    st.markdown(
    f"""
    <style>
        .stFileUploader section div {{display: none}}
        .stFileUploader section {{padding: 0rem}}
        .stFileUploader section button {{width: 100%;font-size: 0}}
        .stFileUploader section button::after{{content: "Select File";display: block;position: absolute;color:{primaryColor};font-size: initial}}
        .char_name_header {{width:100%;text-align:center}}
        .char_stat_block {{width:100%;display:flex;justify-content:space-between;font-size: 1.25rem;font-weight: 400}}
        .st-key-secondary_stat_sidebar hr {{margin:0}}
        .st-key-secondary_stat_sidebar h1 {{font-size: 1.25rem;font-weight: 400}}
        .st-key-secondary_stat_sidebar div[data-testid="stMarkdownContainer"] {{margin-bottom: initial !important}}
        .st-key-secondary_stat_sidebar .st-key-glitch_reset_container {{position: relative;bottom: 1rem}}
        hr {{margin: 1em 0}}
        h1 > span {{display: none !important}}
        h2 > span {{display: none !important}}
        h3 > span {{display: none !important}}
        h4 > span {{display: none !important}}
        h5 > span {{display: none !important}}
        h6 > span {{display: none !important}}
    </style>
    """,
    unsafe_allow_html=True,
    )