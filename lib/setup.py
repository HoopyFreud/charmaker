import lib.creation as lc
import lib.class_def as lcd
import lib.sheet as ls
import streamlit as st

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
    if "select_disable_sheet_desc" not in st.session_state:
        st.session_state.select_disable_sheet_desc = True
        
    if "PC" not in st.session_state:
        st.session_state.PC = lcd.PC()
        ls.clearCharCache()
    if "class_table" not in st.session_state:
        st.session_state.class_table = lc.processClassTable(lc.getClassObject(None))
        
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
    st.session_state.c_pc_desc = st.session_state.PC.pc_desc
    st.session_state.c_pc_flat_stuff_list = ls.getFlatStuffList()
    
def appCSS():
    primaryColor = st.get_option("theme.textColor")
    secondaryBackgroundColor = st.get_option("theme.secondaryBackgroundColor")
    st.markdown(
    f"""
    <style>
        .stFileUploader section div {{display: none}}
        .stFileUploader section {{padding: 0rem}}
        .stFileUploader section button {{width: 100%;font-size: 0}}
        .stFileUploader section button::after{{content: "Select File";display: block;position: absolute;color:{primaryColor};font-size: initial}}
        div:has(> div > .st-key-carry_creation_container) {{padding:0.5rem;background-color:{secondaryBackgroundColor};border:None}}
        .char_name_header {{width:100%;text-align:center}}
        .char_stat_block {{width:100%;display:flex;justify-content:space-between;font-size: 1.25rem;font-weight: 400}}
        .st-key-secondary_stat_sidebar hr {{margin:0}}
        .st-key-secondary_stat_sidebar h2 {{font-size: 1.25rem;font-weight: 400}}
        .st-key-secondary_stat_sidebar div[data-testid="stMarkdownContainer"] {{margin-bottom: initial !important}}
        .st-key-secondary_stat_sidebar .st-key-glitch_reset_container {{position: relative;bottom: 1rem}}
        hr {{margin: 1em 0}}
        .st-key-desc_box h2 {{padding:0.5rem 0}}
        .st-key-desc_box div[data-testid="stMarkdownContainer"]:has(h2) {{margin-bottom: initial !important}}
    </style>
    """,
    unsafe_allow_html=True,
    )