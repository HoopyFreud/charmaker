import lib.util as lu
import lib.sheet as ls
import lib.state_change as lsc
import streamlit as st

def dispCharSheet():
    st.markdown('<h1 class="char_name_header">'+"You are "+st.session_state.PC.pc_name+'</h1>',unsafe_allow_html=True)
    st.divider()
    statList = lu.fieldTableDB["StatTable"]
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
                st.header("HP:", anchor=False)
            with subcol2:
                st.number_input("HP", key="c_pc_hp_current", on_change=ls.updateChar, kwargs={"fieldType":"hp_current","cacheType":None}, step=1, label_visibility="collapsed")
            with subcol3:
                st.header("/", anchor=False)
            with subcol4:
                with st.popover(str(st.session_state.PC.pc_hp_max)):
                    st.write("Base HP")
                    st.number_input("Base HP", key="c_pc_hp_max", on_change=ls.updateChar, kwargs={"fieldType":"hp_max","cacheType":None}, step=1, label_visibility="collapsed")
            st.divider()
            #Glitches
            subcol1, subcol2 = st.columns([1,1.5],vertical_alignment="center")
            with subcol1:
                st.header("Glitches:", anchor=False)
            with subcol2:
                st.number_input("Glitches", key="c_pc_glitch_current", on_change=ls.updateChar, kwargs={"fieldType":"glitch_current","cacheType":None}, step=1, label_visibility="collapsed")
            with st.container(key="glitch_reset_container"):
                st.button("Reset ("+st.session_state.PC.pc_glitch_roll+")", use_container_width=True)
            st.divider()
            #Carrying capacity
            subcol1, subcol2, subcol3, subcol4 = st.columns([2,0.5,0.5,1.5],vertical_alignment="center")
            with subcol1:
                st.header("Carrying Capacity:", anchor=False)
            with subcol2:
                st.header(ls.getCarryWeight(), anchor=False)
            with subcol3:
                st.header("/", anchor=False)
            with subcol4:
                st.header(lu.repCarryCap(st.session_state.PC.pc_carry_max), anchor=False)
            st.divider()
            #Credits
            subcol1, subcol2 = st.columns([1,2],vertical_alignment="center")
            with subcol1:
                st.header("Credits:", anchor=False)
            with subcol2:
                st.number_input("Credits", key="c_pc_creds", on_change=ls.updateChar, kwargs={"fieldType":"creds","cacheType":None}, step=1, label_visibility="collapsed")
            #Debt
            subcol1, subcol2 = st.columns([1,3],vertical_alignment="center")
            with subcol1:
                st.header("Debt:", anchor=False)
            with subcol2:
                st.number_input("Debt", key="c_pc_debt", on_change=ls.updateChar, kwargs={"fieldType":"debt","cacheType":None}, step=1, label_visibility="collapsed")
    with col2:
        pass
    with col3:
        with st.container(key="desc_box"):
            subcol1, subcol2, subcol3 = st.columns([2,1,1],vertical_alignment="center")
            with subcol1:
                st.header("Description:", anchor=False)
            with subcol2:
                if st.session_state.stage==-1:
                    pass
                else:
                    st.button("Cancel", key="sheet_cancel_desc", on_click=lsc.sheetCancelDesc, use_container_width=True)
            with subcol3:
                if st.session_state.stage==-1:
                    st.button("Edit", key="sheet_edit_desc", on_click=lsc.sheetEditDesc, use_container_width=True)
                else:
                    st.button("Save", key="sheet_save_desc", on_click=lsc.sheetSaveDesc, use_container_width=True)
            if st.session_state.stage==-1:
                if st.session_state.PC.pc_desc:
                    for descLine in st.session_state.PC.pc_desc.splitlines(): st.write(descLine)
            else:
                st.text_area("Description", height=275, key="c_pc_desc", label_visibility="collapsed")
            ls.writeStuffDesc()
            ls.writeFeatures()
    st.divider()
    ls.writeStuff()