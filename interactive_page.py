from interactive_creation import dispCharCreation
from interactive_sheet import dispCharSheet
import lib.setup as lsup
import lib.state_change as lsc
import lib.sheet as ls
import streamlit as st

lsup.appSetupKeys()
lsup.appUpdatePCStateKeys()
lsup.appCSS()

st.write(st.session_state)
    
char_export_json = ls.saveToJson()

col1, col2, col3 = st.columns([1,1,1],vertical_alignment="bottom")
with col1:
    st.download_button('Save Character', char_export_json, file_name=("cbuilder_c_b_"+(st.session_state.PC.pc_name if st.session_state.PC.pc_name is not None else "")+".json"), disabled=(st.session_state.stage>=0), key = "save_character", use_container_width=True)
with col2:
    st.button('New Character', key = "new_character", on_click = lsc.charReset, use_container_width=True)
with col3:
    with st.popover('Load Character', use_container_width=True):
        with st.form('load-char-form', clear_on_submit=True, border=False):
            st.file_uploader("Upload file", key="file_uploader_value", label_visibility="collapsed")
            st.form_submit_button("Load", on_click=lsc.processCharUpload, use_container_width=True)
            
if st.session_state.stage > 0:
    dispCharCreation()
elif st.session_state.stage < 0:
    dispCharSheet()