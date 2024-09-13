from st_setup import appSetupKeys
import st_state_change_lib as stc
import st_function_lib as stl
import build_char as bc
import streamlit as st
import copy

appSetupKeys()    
st.write(st.session_state)
st.button('New Character', on_click = stc.charReset)
st.button('New Random Character', on_click = stl.fullRandGen)

#ROW 1 - CLASS
st.header("Class")
if not st.session_state.select_disable_class:
    dropdownList = stl.getJsonObject('classTable.json')
    col1, col2, col3 = st.columns([10,2,2],vertical_alignment="bottom")
    with col1:
        st.radio('Class', dropdownList, horizontal=True, key="t_char_class", label_visibility="collapsed", index=None, disabled=st.session_state.select_disable_class)
    with col2:
        st.button('Random', key = "class_random", on_click = stl.randomSelector, args=["t_char_class",dropdownList], disabled=st.session_state.select_disable_class)
    with col3:
        st.button('Finalize', key = "class_finalize", on_click = stc.finalizeClass, disabled=st.session_state.select_disable_class)
    if st.session_state.err_text_class:
        st.error(stl.err_text["err_text_class"])
else:
    with st.container(border=True):
        st.write(st.session_state.PC.pc_class)
        
#ROW 2 - STATS
st.header("Stats")
statList = stl.getJsonObject('statTable.json')
if not st.session_state.select_disable_stat:
    col1, col2, col3, col4, col5, col6, col7 = st.columns([1,1,1,1,1,1,1],vertical_alignment="bottom")
    with col1:
        st.write(statList[0]+":")
        rollString = stl.statifyString(st.session_state.class_table["AgilityRoll"])
        st.text_input(statList[0]+":", key = "t_char_agi", placeholder=rollString, label_visibility="collapsed", on_change=stl.changeNumInput, args=["t_char_agi","err_text_stat"], kwargs={"roll": rollString}, disabled=st.session_state.select_disable_stat)
    with col2:
        st.write(statList[1]+":")
        rollString = stl.statifyString(st.session_state.class_table["KnowledgeRoll"])
        st.text_input(statList[1]+":", key = "t_char_knw", placeholder=rollString, label_visibility="collapsed", on_change=stl.changeNumInput, args=["t_char_knw","err_text_stat"], kwargs={"roll": rollString}, disabled=st.session_state.select_disable_stat)
    with col3:
        st.write(statList[2]+":")
        rollString = stl.statifyString(st.session_state.class_table["PresenceRoll"])
        st.text_input(statList[2]+":", key = "t_char_pre", placeholder=rollString, label_visibility="collapsed", on_change=stl.changeNumInput, args=["t_char_pre","err_text_stat"], kwargs={"roll": rollString}, disabled=st.session_state.select_disable_stat)
    with col4:
        st.write(statList[3]+":")
        rollString = stl.statifyString(st.session_state.class_table["StrengthRoll"])
        st.text_input(statList[3]+":", key = "t_char_str", placeholder=rollString, label_visibility="collapsed", on_change=stl.changeNumInput, args=["t_char_str","err_text_stat"], kwargs={"roll": rollString}, disabled=st.session_state.select_disable_stat)
    with col5:
        st.write(statList[4]+":")
        rollString = stl.statifyString(st.session_state.class_table["ToughnessRoll"])
        st.text_input(statList[4]+":", key = "t_char_tou", placeholder=rollString, label_visibility="collapsed", on_change=stl.changeNumInput, args=["t_char_tou","err_text_stat"], kwargs={"roll": rollString}, disabled=st.session_state.select_disable_stat)
    with col6:
        st.button('Random', key = "stat_random", on_click = stl.randomStats, disabled=st.session_state.select_disable_stat)
    with col7:
        st.button('Finalize', key = "stat_finalize", on_click = stc.finalizeStats, disabled=st.session_state.select_disable_stat)
    if st.session_state.err_text_stat:
        st.error(stl.err_text["err_text_stat"])
else:
    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1],vertical_alignment="bottom")
    with col1:
        st.write(statList[0]+":")
        with st.container(border=True):
            st.write(st.session_state.PC.pc_agi)
    with col2:
        st.write(statList[1]+":")
        with st.container(border=True):
            st.write(st.session_state.PC.pc_knw)
    with col3:
        st.write(statList[2]+":")
        with st.container(border=True):
            st.write(st.session_state.PC.pc_pre)
    with col4:
        st.write(statList[3]+":")
        with st.container(border=True):
            st.write(st.session_state.PC.pc_str)
    with col5:
        st.write(statList[4]+":")
        with st.container(border=True):
            st.write(st.session_state.PC.pc_tou)
        
    
#ROW 3 - SECONDARY STATS
st.header("Derived Stats")
secondaryStatList = stl.getJsonObject('secondaryStatTable.json')
if not st.session_state.select_disable_secondary_stat:
    col1, col2, col3, col4, col5, col6, col7 = st.columns([1,1,1,1,1,1,1],vertical_alignment="bottom")
    with col1:
        st.write(secondaryStatList[0]+":")
        rollString = stl.statifyString(st.session_state.class_table["HPRoll"])
        st.text_input(secondaryStatList[0]+":", key = "t_char_hpmax", placeholder=rollString, label_visibility="collapsed", on_change=stl.changeNumInput, args=("t_char_hpmax","err_text_secondary_stat"), kwargs={"roll": rollString}, disabled=st.session_state.select_disable_secondary_stat)
    with col2:
        st.write(secondaryStatList[1]+":")
        rollString = stl.statifyString(st.session_state.class_table["GlitchRoll"])
        st.text_input(secondaryStatList[1]+":", key = "t_char_glitch", placeholder=rollString, label_visibility="collapsed", on_change=stl.changeNumInput, args=("t_char_glitch","err_text_secondary_stat"), kwargs={"roll": rollString}, disabled=st.session_state.select_disable_secondary_stat)
    with col3:
        st.write(secondaryStatList[2]+":")
        with st.container(border=True):
            st.write(stl.statifyString(st.session_state.class_table["CarryingCapacityRoll"]))
    with col4:
        st.write(secondaryStatList[3]+":")
        rollString = stl.statifyString(st.session_state.class_table["CreditsRoll"])
        st.text_input(secondaryStatList[3]+":", key = "t_char_creds", placeholder=rollString, label_visibility="collapsed", on_change=stl.changeNumInput, args=("t_char_creds","err_text_secondary_stat"), kwargs={"roll": rollString}, disabled=st.session_state.select_disable_secondary_stat)
    with col5:
        st.write(secondaryStatList[4]+":")
        rollString = stl.statifyString(st.session_state.class_table["DebtRoll"])
        st.text_input(secondaryStatList[4]+":", key = "t_char_debt", placeholder=rollString, label_visibility="collapsed", on_change=stl.changeNumInput, args=("t_char_debt","err_text_secondary_stat"), kwargs={"roll": rollString}, disabled=st.session_state.select_disable_secondary_stat)
    with col6:
        st.button('Random', key = "sec_stat_random", on_click = stl.randomSecondaryStats, disabled=st.session_state.select_disable_secondary_stat)
    with col7:
        st.button('Finalize', key = "sec_stat_finalize", on_click = stc.finalizeSecondaryStats, disabled=st.session_state.select_disable_secondary_stat)
    if st.session_state.err_text_secondary_stat:
        st.error(stl.err_text["err_text_secondary_stat"])
else:
    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1],vertical_alignment="bottom")
    with col1:
        st.write(secondaryStatList[0]+":")
        with st.container(border=True):
            st.write(st.session_state.PC.pc_hp_max)
    with col2:
        st.write(secondaryStatList[1]+":")
        with st.container(border=True):
            st.write(st.session_state.PC.pc_glitch_current)
    with col3:
        st.write(secondaryStatList[2]+":")
        with st.container(border=True):
            st.write(st.session_state.PC.pc_carrying_max)
    with col4:
        st.write(secondaryStatList[3]+":")
        with st.container(border=True):
            st.write(st.session_state.PC.pc_creds)
    with col5:
        st.write(secondaryStatList[4]+":")
        with st.container(border=True):
            st.write(st.session_state.PC.pc_debt)
            
#ROW 4 - STUFF
if not st.session_state.select_disable_stuff:
    if "RandomClassStuff" in st.session_state.class_table.keys():
        st.header(st.session_state.class_table["RandomClassStuffText"])
        stl.insertStuffEntry(bc.StuffField("RandomItem", None, {}), prefix = "RandomClassStuff", customStuffTable = st.session_state.class_table["RandomClassStuff"])
        st.header("You also have:")
    else:
        st.header("You have:")
    
    stuffList = st.session_state.class_table["Stuff"]
    if "ClassStuff" in st.session_state.class_table.keys():
        stuffList = st.session_state.class_table["ClassStuff"] + stuffList
    for stuffItem in stuffList:
        stl.insertStuffEntry(stuffItem, prefix = stuffItem.p_source)
    st.button('Finalize', key = "stuff_finalize", on_click = stc.finalizeStuff, disabled=st.session_state.select_disable_stuff)