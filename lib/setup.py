import lib.creation as lc
import lib.class_def as lcd
import streamlit as st

def appSetupKeys():
    if "stage" not in st.session_state:
        st.session_state.stage = 0
    if "sheetEditStats" not in st.session_state:
        st.session_state.sheetEditStats = False
    if "sheetEditDesc" not in st.session_state:
        st.session_state.sheetEditDesc = False
        
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
    if "SheetAttributes" not in st.session_state:
        st.session_state.SheetAttributes = lcd.SheetAttributes()
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
    if "b_pc_desc" not in st.session_state:
        st.session_state.b_pc_desc = None
        
    if "c_pc_agi" not in st.session_state:
        st.session_state.c_pc_agi = None
    if "c_pc_knw" not in st.session_state:
        st.session_state.c_pc_knw = None
    if "c_pc_pre" not in st.session_state:
        st.session_state.c_pc_pre = None
    if "c_pc_str" not in st.session_state:
        st.session_state.c_pc_str = None
    if "c_pc_tou" not in st.session_state:
        st.session_state.c_pc_tou = None
    if "c_pc_hp_current" not in st.session_state:
        st.session_state.c_pc_hp_current = None
    if "c_pc_hp_max" not in st.session_state:
        st.session_state.c_pc_hp_max = None
    if "c_pc_glitch_current" not in st.session_state:
        st.session_state.c_pc_glitch_current = None
    if "c_pc_creds" not in st.session_state:
        st.session_state.c_pc_creds = None
    if "c_pc_debt" not in st.session_state:
        st.session_state.c_pc_debt = None
    if "c_pc_desc" not in st.session_state:
        st.session_state.c_pc_desc = None
    if "c_pc_equipped_armor" not in st.session_state:
        st.session_state.c_pc_equipped_armor = None
        
    if "err_text_class" not in st.session_state:
        st.session_state.err_text_class = False
    if "err_text_stat" not in st.session_state:
        st.session_state.err_text_stat = False
    if "err_text_secondary_stat" not in st.session_state:
        st.session_state.err_text_secondary_stat = False
    if "err_text_desc" not in st.session_state:
        st.session_state.err_text_desc = False
    
def appCSS():
    primaryColor = st.get_option("theme.textColor")
    secondaryBackgroundColor = st.get_option("theme.secondaryBackgroundColor")
    st.markdown(
    f"""
    <style>
        hr {{margin: 0}}
        .stFileUploader section div {{display: none}}
        .stFileUploader section {{padding: 0rem}}
        .stFileUploader section button {{width: 100%;font-size: 0}}
        .stFileUploader section button::after{{content: "Select File";display: block;position: absolute;color:{primaryColor};font-size: initial}}
        div:has(> div > .st-key-carry_creation_container) {{padding:0.5rem;background-color:{secondaryBackgroundColor};border:None}}
        .st-key-stat_header div[data-testid="stMarkdownContainer"] {{margin-bottom: initial !important}}
        .st-key-stat_header h2 {{padding:0;font-size: 1.25rem;font-weight: 400}}
        .char_name_header {{width:100%;text-align:center}}
        .char_stat_block {{width:100%;display:flex;justify-content:space-between;font-size: 1.25rem;font-weight: 400}}
        .st-key-secondary_stat_sidebar hr {{margin:0}}
        .st-key-secondary_stat_sidebar h2 {{font-size: 1.25rem;font-weight: 400}}
        .st-key-secondary_stat_sidebar div[data-testid="stMarkdownContainer"] {{margin-bottom: initial !important}}
        .st-key-secondary_stat_sidebar .st-key-glitch_reset_container {{position: relative;bottom: 1rem}}
        .st-key-desc_box h2 {{padding:0.5rem 0}}
        .st-key-desc_box div[data-testid="stMarkdownContainer"]:has(h2) {{margin-bottom: initial !important}}
        .st-key-stuff_zone summary p {{padding:0;font-size: 1.25rem !important;font-weight: 400}}
        .st-key-attack_type_box p {{margin:0}}
        .stMainBlockContainer {{max-width: 60rem}}
    </style>
    """,
    unsafe_allow_html=True,
    )
    
def appUpdatePCStateKeys(fieldType = "All"):
    if fieldType == "All" or fieldType == "stats":
        if not st.session_state.sheetEditStats:
            st.session_state.c_pc_agi = st.session_state.PC.pc_agi
            st.session_state.c_pc_knw = st.session_state.PC.pc_knw
            st.session_state.c_pc_pre = st.session_state.PC.pc_pre
            st.session_state.c_pc_str = st.session_state.PC.pc_str
            st.session_state.c_pc_tou = st.session_state.PC.pc_tou
    if fieldType == "All" or fieldType == "hp_current":
        st.session_state.c_pc_hp_current = st.session_state.PC.pc_hp_current
    if fieldType == "All" or fieldType == "hp_max":
        st.session_state.c_pc_hp_max = st.session_state.PC.pc_hp_max
    if fieldType == "All" or fieldType == "glitch_current":
        st.session_state.c_pc_glitch_current = st.session_state.PC.pc_glitch_current
    if fieldType == "All" or fieldType == "creds":
        st.session_state.c_pc_creds = st.session_state.PC.pc_creds
    if fieldType == "All" or fieldType == "debt":
        st.session_state.c_pc_debt = st.session_state.PC.pc_debt
    if fieldType == "All" or fieldType == "equipped_armor":
        st.session_state.c_pc_equipped_armor = st.session_state.PC.pc_equipped_armor
    if fieldType == "All" or fieldType == "desc":
        if not st.session_state.sheetEditDesc:
            st.session_state.c_pc_desc = st.session_state.PC.pc_desc