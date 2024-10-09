import st_setup as sts
import st_state_change_lib as stc
import st_function_lib as stl
import st_render_char_lib as strc
import build_char as bc
import streamlit as st
import copy

sts.appSetupKeys()
sts.appUpdatePC()
sts.appCSS()
    
char_export_yaml = strc.export_char()

col1, col2, col3 = st.columns([1,1,1],vertical_alignment="bottom")
with col1:
    st.download_button('Save Character', char_export_yaml, key = "save_character", use_container_width=True)
with col2:
    st.button('New Character', key = "new_character", on_click = stc.charReset, use_container_width=True)
with col3:
    with st.popover('Load Character', use_container_width=True):
        with st.form('load-char-form', clear_on_submit=True, border=False):
            uploadedChar = st.file_uploader("Upload file", key="file_uploader_value", label_visibility="collapsed")
            st.form_submit_button("Load", on_click=stc.processCharUpload, use_container_width=True)
    
#ROW 1 - CLASS
if st.session_state.stage >= 1:
    st.header("Class")
    if not st.session_state.select_disable_class:
        dropdownList = stl.fieldTableDB["ClassTable"]
        col1, col2, col3 = st.columns([10,2,2],vertical_alignment="bottom")
        with col1:
            st.radio('Class', dropdownList, horizontal=True, key="t_char_class", label_visibility="collapsed", index=None, disabled=st.session_state.select_disable_class)
        with col2:
            st.button('Random', key = "class_random", on_click = stl.randomSelector, args=["t_char_class",dropdownList], disabled=st.session_state.select_disable_class)
        with col3:
            st.button('Finalize', key = "class_finalize", on_click = stc.finalizeClass, disabled=st.session_state.select_disable_class)
        if st.session_state.err_text_class:
            st.error(stl.errTextDB["err_text_class"])
    else:
        with st.container(border=True):
            st.write(st.session_state.PC.pc_class)
        
#ROW 2 - STATS
if st.session_state.stage >= 2:
    st.header("Stats")
    statList = stl.fieldTableDB["StatTable"]
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
            st.error(stl.errTextDB["err_text_stat"])
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
        
if st.session_state.stage >= 3:
#ROW 3 - SECONDARY STATS
    st.header("Derived Stats")
    secondaryStatList = stl.fieldTableDB["SecondaryStatTable"]
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
            st.error(stl.errTextDB["err_text_secondary_stat"])
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
            
#ROW 4 - DESCRIPTION
if st.session_state.stage >= 4:
    st.header("Description")
    descFieldList = stl.fieldTableDB["DescTable"]
    if not st.session_state.select_disable_desc:
        col1, col2, col3 = st.columns([1,1,1],vertical_alignment="bottom")
        with col1:
            st.write(descFieldList[0]+":")
            st.text_input(descFieldList[0]+":", key = "t_char_name", label_visibility="collapsed", on_change=stl.resetErrField, args=("err_text_desc"), disabled=st.session_state.select_disable_desc)
        with col2:
            st.write(descFieldList[1]+":")
            st.text_input(descFieldList[1]+":", key = "t_char_feature", label_visibility="collapsed", disabled=st.session_state.select_disable_desc)
        with col3:
            st.write(descFieldList[2]+":")
            st.text_input(descFieldList[2]+":", key = "t_char_quirk", label_visibility="collapsed", disabled=st.session_state.select_disable_desc)
        col1, col2, col3 = st.columns([1,1,1],vertical_alignment="bottom")
        with col1:
            st.write(descFieldList[3]+":")
            st.text_input(descFieldList[3]+":", key = "t_char_style", label_visibility="collapsed", disabled=st.session_state.select_disable_desc)
        with col2:
            st.write(descFieldList[4]+":")
            st.text_input(descFieldList[4]+":", key = "t_char_obsession", label_visibility="collapsed", disabled=st.session_state.select_disable_desc)
        with col3:
            st.write(descFieldList[5]+":")
            st.text_input(descFieldList[5]+":", key = "t_char_desire", label_visibility="collapsed", disabled=st.session_state.select_disable_desc)
        st.write(descFieldList[6]+":")
        st.text_input(descFieldList[6]+":", key = "t_char_lender", label_visibility="collapsed", disabled=st.session_state.select_disable_desc)
        if "RandomClassLore" in st.session_state.class_table.keys():
            st.write(st.session_state.class_table["RandomClassLorePrompt"]+":")
            st.text_area(st.session_state.class_table["RandomClassLorePrompt"]+":", key = "t_char_class_lore", label_visibility="collapsed", disabled=st.session_state.select_disable_desc)
        col1, col2, col3, col4 = st.columns([1,1,1,1],vertical_alignment="bottom")
        with col1:
            pass
        with col2:
            st.button('Random', key = "desc_random", on_click = stl.randomDesc, disabled=st.session_state.select_disable_desc)
        with col3:
            st.button('Finalize', key = "desc_finalize", on_click = stc.finalizeDesc, disabled=st.session_state.select_disable_desc)
        with col4:
            pass
        if st.session_state.err_text_desc:
            st.error(stl.errTextDB["err_text_desc"])
    else:
        col1, col2 = st.columns([1,4],vertical_alignment="top")
        with col1:
            st.write(descFieldList[0]+":")
            with st.container(border=True):
                st.write(st.session_state.PC.pc_name)
        with col2:
            st.write("Description:")
            with st.container(border=True):
                st.write(st.session_state.PC.pc_desc)
    
        
#ROW 5 - STUFF
if st.session_state.stage >= 5:
    if not st.session_state.select_disable_stuff:
        if "RandomClassStuff" in st.session_state.class_table.keys():
            st.header(st.session_state.class_table["RandomClassStuffText"])
            stl.insertStuffEntry(bc.StuffField("RandomItem", None, {}), "RandomClassStuff", customStuffTable = st.session_state.class_table["RandomClassStuff"])
            st.header("You also have:")
        else:
            st.header("You have:")
        
        stuffList = st.session_state.class_table["Stuff"]
        if "ClassStuff" in st.session_state.class_table.keys():
            stuffList = st.session_state.class_table["ClassStuff"] + stuffList
        for stuffItem in stuffList:
            stl.insertStuffEntry(stuffItem, stuffItem.p_source)
        col1, col2, col3 = st.columns([1,1,1],vertical_alignment="bottom")
        with col1:
            pass
        with col2:
            st.button('Finalize', key = "stuff_finalize", on_click = stc.finalizeStuff, use_container_width=True, disabled=st.session_state.select_disable_stuff)
        with col3:
            pass
            
#FULL CHARACTER SHEET
if st.session_state.stage < 0:
    st.markdown('<h1 class="char_name_header">'+"You are "+st.session_state.PC.pc_name+'</h1>',unsafe_allow_html=True)
    st.divider()
    statList = stl.fieldTableDB["StatTable"]
    headerString = ""
    statString = "+"+str(st.session_state.PC.pc_agi) if st.session_state.PC.pc_agi > 0 else str(st.session_state.PC.pc_agi)
    headerString = headerString + '<div>' + statList[0]+": " + statString + '</div>'
    statString = "+"+str(st.session_state.PC.pc_knw) if st.session_state.PC.pc_knw > 0 else str(st.session_state.PC.pc_knw)
    headerString = headerString + '<div>' + statList[1]+": " + statString + '</div>'
    statString = "+"+str(st.session_state.PC.pc_pre) if st.session_state.PC.pc_pre > 0 else str(st.session_state.PC.pc_pre)
    headerString = headerString + '<div>' + statList[2]+": " + statString + '</div>'
    statString = "+"+str(st.session_state.PC.pc_str) if st.session_state.PC.pc_str > 0 else str(st.session_state.PC.pc_str)
    headerString = headerString + '<div>' + statList[3]+": " + statString + '</div>'
    statString = "+"+str(st.session_state.PC.pc_tou) if st.session_state.PC.pc_tou > 0 else str(st.session_state.PC.pc_tou)
    headerString = headerString + '<div>' + statList[4]+": " + statString + '</div>'
    st.markdown('<div class="char_stat_block">'+headerString+'</div>',unsafe_allow_html=True)
    st.divider()
    col1, col2, col3 = st.columns([1.25,0.125,2.5],vertical_alignment="top")
    with col1:
        with st.container(key="secondary_stat_sidebar"):
            #HP
            subcol1, subcol2, subcol3, subcol4 = st.columns([1,1,0.25,1.5],vertical_alignment="center")
            with subcol1:
                st.write("# HP:")
            with subcol2:
                st.number_input("HP", key="c_pc_hp_current", on_change=strc.update_char, step=1, label_visibility="collapsed")
            with subcol3:
                st.write("# /")
            with subcol4:
                with st.popover(str(st.session_state.PC.pc_hp_max)):
                    st.write("Base HP")
                    st.number_input("Base HP", key="c_pc_hp_max", on_change=strc.update_char, step=1, label_visibility="collapsed")
            st.divider()
            #Glitches
            subcol1, subcol2 = st.columns([2,1.5],vertical_alignment="center")
            with subcol1:
                st.write("# Glitches:")
            with subcol2:
                st.number_input("Glitches", key="c_pc_glitch_current", on_change=strc.update_char, step=1, label_visibility="collapsed")
            with st.container(key="glitch_reset_container"):
                st.button("Reset ("+st.session_state.PC.pc_glitch_roll+")", use_container_width=True)
            st.divider()
            #Carrying capacity
            subcol1, subcol2, subcol3, subcol4 = st.columns([2,0.5,0.5,1.5],vertical_alignment="center")
            with subcol1:
                st.write("# Carrying Capacity:")
            with subcol2:
                st.write("# " + str(st.session_state.PC.getCurrentCarry()))
            with subcol3:
                st.write("# /")
            with subcol4:
                with st.popover(str(st.session_state.PC.pc_carrying_max)):
                    st.write("Base Carrying Capacity")
                    st.number_input("Base Carry Cap", key="c_pc_carrying_max", on_change=strc.update_char, step=1, label_visibility="collapsed")
            st.divider()
            #Credits
            subcol1, subcol2 = st.columns([1,2],vertical_alignment="center")
            with subcol1:
                st.write("# Credits:")
            with subcol2:
                st.number_input("Credits", key="c_pc_creds", on_change=strc.update_char, step=1, label_visibility="collapsed")
            #Debt
            subcol1, subcol2 = st.columns([1,3],vertical_alignment="center")
            with subcol1:
                st.write("# Debt:")
            with subcol2:
                st.number_input("Debt", key="c_pc_debt", on_change=strc.update_char, step=1, label_visibility="collapsed")
    with col2:
        pass
    with col3:
        st.write(st.session_state.PC.pc_desc)