import lib.state_change as lsc
import lib.creation as lc
import lib.util as lu
import lib.class_def as lcd
import streamlit as st

def dispCharCreation():
    #ROW 1 - CLASS
    if st.session_state.stage >= 1:
        if st.session_state.stage==1:
            st.header("Class:", anchor=False)
            dropdownList = lu.fieldTableDB["ClassTable"]
            col1, col2, col3 = st.columns([10,2,2],vertical_alignment="bottom")
            with col1:
                st.radio('Class', dropdownList, horizontal=True, key="t_char_class", label_visibility="collapsed", index=None)
            with col2:
                st.button('Random', key = "class_random", on_click = lu.randomSelector, args=["t_char_class",dropdownList], use_container_width=True)
            with col3:
                st.button('Finalize', key = "class_finalize", on_click = lsc.finalizeClass, use_container_width=True)
            if st.session_state.err_text_class:
                st.error(lu.errTextDB["err_text_class"], use_container_width=True)
        else:
            st.header("Class: " + st.session_state.PC.pc_class, anchor=False)
            
    #ROW 2 - STATS
    if st.session_state.stage >= 2:
        statList = lu.fieldTableDB["StatTable"]
        if st.session_state.stage==2:
            st.header("Stats:", anchor=False)
            col1, col2, col3, col4, col5, col6, col7 = st.columns([1,1,1,1,1,1,1],vertical_alignment="bottom")
            with col1:
                st.write(statList[0]+":")
                rollString = lu.statifyString(st.session_state.class_table["AgilityRoll"])
                st.text_input(statList[0]+":", key = "t_char_agi", placeholder=rollString, label_visibility="collapsed", on_change=lu.changeNumInput, args=["t_char_agi","err_text_stat"], kwargs={"roll": rollString})
            with col2:
                st.write(statList[1]+":")
                rollString = lu.statifyString(st.session_state.class_table["KnowledgeRoll"])
                st.text_input(statList[1]+":", key = "t_char_knw", placeholder=rollString, label_visibility="collapsed", on_change=lu.changeNumInput, args=["t_char_knw","err_text_stat"], kwargs={"roll": rollString})
            with col3:
                st.write(statList[2]+":")
                rollString = lu.statifyString(st.session_state.class_table["PresenceRoll"])
                st.text_input(statList[2]+":", key = "t_char_pre", placeholder=rollString, label_visibility="collapsed", on_change=lu.changeNumInput, args=["t_char_pre","err_text_stat"], kwargs={"roll": rollString})
            with col4:
                st.write(statList[3]+":")
                rollString = lu.statifyString(st.session_state.class_table["StrengthRoll"])
                st.text_input(statList[3]+":", key = "t_char_str", placeholder=rollString, label_visibility="collapsed", on_change=lu.changeNumInput, args=["t_char_str","err_text_stat"], kwargs={"roll": rollString})
            with col5:
                st.write(statList[4]+":")
                rollString = lu.statifyString(st.session_state.class_table["ToughnessRoll"])
                st.text_input(statList[4]+":", key = "t_char_tou", placeholder=rollString, label_visibility="collapsed", on_change=lu.changeNumInput, args=["t_char_tou","err_text_stat"], kwargs={"roll": rollString})
            with col6:
                st.button('Random', key = "stat_random", on_click = lc.randomStats, use_container_width=True)
            with col7:
                st.button('Finalize', key = "stat_finalize", on_click = lsc.finalizeStats, use_container_width=True)
            if st.session_state.err_text_stat:
                st.error(lu.errTextDB["err_text_stat"])
        else:
            st.header("Stat Modifiers:", anchor=False)
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
            
    if st.session_state.stage >= 3:
    #ROW 3 - SECONDARY STATS
        st.header("Derived Stats:", anchor=False)
        secondaryStatList = lu.fieldTableDB["SecondaryStatTable"]
        if st.session_state.stage==3:
            col1, col2, col3, col4, col5, col6, col7 = st.columns([1,1,1,1,1,1,1],vertical_alignment="bottom")
            with col1:
                st.write(secondaryStatList[0]+":")
                rollString = lu.statifyString(st.session_state.class_table["HPRoll"])
                st.text_input(secondaryStatList[0]+":", key = "t_char_hpmax", placeholder=rollString, label_visibility="collapsed", on_change=lu.changeNumInput, args=("t_char_hpmax","err_text_secondary_stat"), kwargs={"roll": rollString})
            with col2:
                st.write(secondaryStatList[1]+":")
                rollString = lu.statifyString(st.session_state.class_table["GlitchRoll"])
                st.text_input(secondaryStatList[1]+":", key = "t_char_glitch", placeholder=rollString, label_visibility="collapsed", on_change=lu.changeNumInput, args=("t_char_glitch","err_text_secondary_stat"), kwargs={"roll": rollString})
            with col3:
                st.write(secondaryStatList[2]+":")
                with st.container(key="carry_creation_container", border=True):
                    st.write(lu.repCarryCap(st.session_state.class_table["CarryingCapacityString"]))
            with col4:
                st.write(secondaryStatList[3]+":")
                rollString = lu.statifyString(st.session_state.class_table["CreditsRoll"])
                st.text_input(secondaryStatList[3]+":", key = "t_char_creds", placeholder=rollString, label_visibility="collapsed", on_change=lu.changeNumInput, args=("t_char_creds","err_text_secondary_stat"), kwargs={"roll": rollString})
            with col5:
                st.write(secondaryStatList[4]+":")
                rollString = lu.statifyString(st.session_state.class_table["DebtRoll"])
                st.text_input(secondaryStatList[4]+":", key = "t_char_debt", placeholder=rollString, label_visibility="collapsed", on_change=lu.changeNumInput, args=("t_char_debt","err_text_secondary_stat"), kwargs={"roll": rollString})
            with col6:
                st.button('Random', key = "sec_stat_random", on_click = lc.randomSecondaryStats, use_container_width=True)
            with col7:
                st.button('Finalize', key = "sec_stat_finalize", on_click = lsc.finalizeSecondaryStats, use_container_width=True)
            if st.session_state.err_text_secondary_stat:
                st.error(lu.errTextDB["err_text_secondary_stat"])
        else:
            headerString = ""
            headerString = headerString + '<div>' + secondaryStatList[0]+": " + str(st.session_state.PC.pc_hp_max) + '</div>'
            headerString = headerString + '<div>' + secondaryStatList[1]+": " + str(st.session_state.PC.pc_glitch_current) + '</div>'
            headerString = headerString + '<div>' + secondaryStatList[2]+": " + lu.repCarryCap(st.session_state.PC.pc_carry_max) + '</div>'
            headerString = headerString + '<div>' + secondaryStatList[3]+": " + str(st.session_state.PC.pc_creds) + '</div>'
            headerString = headerString + '<div>' + secondaryStatList[4]+": " + str(st.session_state.PC.pc_debt) + '</div>'
            st.markdown('<div class="char_stat_block">'+headerString+'</div>',unsafe_allow_html=True)
                
    #ROW 4 - DESCRIPTION
    if st.session_state.stage >= 4:
        descFieldList = lu.fieldTableDB["DescTable"]
        if st.session_state.stage==4:
            st.header("Description", anchor=False)
            col1, col2, col3 = st.columns([1,1,1],vertical_alignment="bottom")
            with col1:
                st.write(descFieldList[0]+":")
                st.text_input(descFieldList[0]+":", key = "t_char_name", label_visibility="collapsed", on_change=lu.resetErrField, args=["err_text_desc"])
            with col2:
                st.write(descFieldList[1]+":")
                st.text_input(descFieldList[1]+":", key = "t_char_feature", label_visibility="collapsed")
            with col3:
                st.write(descFieldList[2]+":")
                st.text_input(descFieldList[2]+":", key = "t_char_quirk", label_visibility="collapsed")
            col1, col2, col3 = st.columns([1,1,1],vertical_alignment="bottom")
            with col1:
                st.write(descFieldList[3]+":")
                st.text_input(descFieldList[3]+":", key = "t_char_style", label_visibility="collapsed")
            with col2:
                st.write(descFieldList[4]+":")
                st.text_input(descFieldList[4]+":", key = "t_char_obsession", label_visibility="collapsed")
            with col3:
                st.write(descFieldList[5]+":")
                st.text_input(descFieldList[5]+":", key = "t_char_desire", label_visibility="collapsed")
            st.write(descFieldList[6]+":")
            st.text_input(descFieldList[6]+":", key = "t_char_lender", label_visibility="collapsed")
            if "RandomClassLore" in st.session_state.class_table.keys():
                st.write(st.session_state.class_table["RandomClassLorePrompt"]+":")
                st.text_area(st.session_state.class_table["RandomClassLorePrompt"]+":", key = "t_char_class_lore", label_visibility="collapsed")
            col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1],vertical_alignment="bottom")
            with col1:
                pass
            with col2:
                st.button('Random', key = "desc_random", on_click = lc.randomDesc, use_container_width=True)
            with col3:
                pass
            with col4:
                st.button('Finalize', key = "desc_finalize", on_click = lsc.finalizeDesc, use_container_width=True)
            with col5:
                pass
            if st.session_state.err_text_desc:
                st.error(lu.errTextDB["err_text_desc"])
        else:
            col1, col2 = st.columns([1,2.5],vertical_alignment="top")
            with col1:
                st.header(descFieldList[0] + ":", anchor=False)
            with col2:
                st.header(st.session_state.PC.pc_name, anchor=False)
            col1, col2 = st.columns([1,2.5],vertical_alignment="top")
            with col1:
                st.header("Description:", anchor=False)
            with col2:
                st.write(st.session_state.PC.pc_desc)
        
            
    #ROW 5 - STUFF
    if st.session_state.stage >= 5:
        if st.session_state.stage==5:
            lc.writeStuffSelection()
            col1, col2, col3 = st.columns([1,1,1],vertical_alignment="bottom")
            with col1:
                pass
            with col2:
                st.button('Finalize', key = "stuff_finalize", on_click = lsc.finalizeStuff, use_container_width=True)
            with col3:
                pass