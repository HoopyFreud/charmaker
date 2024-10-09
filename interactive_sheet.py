import lib.util as lu
import lib.sheet as ls
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
                st.write("# HP:")
            with subcol2:
                st.number_input("HP", key="c_pc_hp_current", on_change=ls.updateChar, step=1, label_visibility="collapsed")
            with subcol3:
                st.write("# /")
            with subcol4:
                with st.popover(str(st.session_state.PC.pc_hp_max)):
                    st.write("Base HP")
                    st.number_input("Base HP", key="c_pc_hp_max", on_change=ls.updateChar, step=1, label_visibility="collapsed")
            st.divider()
            #Glitches
            subcol1, subcol2 = st.columns([2,1.5],vertical_alignment="center")
            with subcol1:
                st.write("# Glitches:")
            with subcol2:
                st.number_input("Glitches", key="c_pc_glitch_current", on_change=ls.updateChar, step=1, label_visibility="collapsed")
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
                    st.number_input("Base Carry Cap", key="c_pc_carrying_max", on_change=ls.updateChar, step=1, label_visibility="collapsed")
            st.divider()
            #Credits
            subcol1, subcol2 = st.columns([1,2],vertical_alignment="center")
            with subcol1:
                st.write("# Credits:")
            with subcol2:
                st.number_input("Credits", key="c_pc_creds", on_change=ls.updateChar, step=1, label_visibility="collapsed")
            #Debt
            subcol1, subcol2 = st.columns([1,3],vertical_alignment="center")
            with subcol1:
                st.write("# Debt:")
            with subcol2:
                st.number_input("Debt", key="c_pc_debt", on_change=ls.updateChar, step=1, label_visibility="collapsed")
    with col2:
        pass
    with col3:
        st.write(st.session_state.PC.pc_desc)
        ls.displayFeatures()