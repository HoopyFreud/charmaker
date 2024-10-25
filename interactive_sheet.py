import lib.util as lu
import lib.sheet as ls
import lib.state_change as lsc
import lib.class_def as lcd
import streamlit as st

def dispCharSheet():
    with st.container(key="char_name_header"):
        st.title("You are "+st.session_state.PC.pc_name, anchor=False)
    st.divider()
    statList = lu.fieldTableDB["StatTable"]
    with st.container(key="stat_header"):
        if st.session_state.sheetEditStats:
            col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1],vertical_alignment="bottom")
            with col1:
                st.header(statList[0]+":", anchor=False)
                st.number_input(statList[0]+":", key = "c_pc_agi", step=1, label_visibility="collapsed")
            with col2:
                st.header(statList[1]+":", anchor=False)
                st.number_input(statList[1]+":", key = "c_pc_knw", step=1, label_visibility="collapsed")
            with col3:
                st.header(statList[2]+":", anchor=False)
                st.number_input(statList[2]+":", key = "c_pc_pre", step=1, label_visibility="collapsed")
            with col4:
                st.header(statList[3]+":", anchor=False)
                st.number_input(statList[3]+":", key = "c_pc_str", step=1, label_visibility="collapsed")
            with col5:
                st.header(statList[4]+":", anchor=False)
                st.number_input(statList[4]+":", key = "c_pc_tou", step=1, label_visibility="collapsed")
            col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1],vertical_alignment="center")
            with col1:
                pass
            with col2:
                st.button("Cancel", key="sheet_cancel_stats", on_click=lsc.sheetCancelStats, use_container_width=True)
            with col3:
                pass
            with col4:
                st.button("Save", key="sheet_save_stats", on_click=lsc.sheetSaveStats, use_container_width=True)
            with col5:
                pass
        else:
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
            col1, col2 = st.columns([5,1],vertical_alignment="center")
            with col1:
                st.markdown('<div class="char_stat_block">'+headerString+'</div>',unsafe_allow_html=True)
            with col2:
                st.button("Edit", key="sheet_edit_stats", on_click=lsc.sheetEditStats, use_container_width=True)
    st.divider()
    col1, col2, col3 = st.columns([1.25,0.125,2.5],vertical_alignment="top")
    with col1:
        with st.container(key="secondary_stat_sidebar"):
            #HP
            subcol1, subcol2, subcol3, subcol4 = st.columns([3,3,1,4],vertical_alignment="center")
            with subcol1:
                st.header("HP:", anchor=False)
            with subcol2:
                st.number_input("HP", key="c_pc_hp_current", on_change=ls.updateChar, kwargs={"fieldType":"hp_current","cacheType":None}, step=1, min_value=0, label_visibility="collapsed")
            with subcol3:
                st.header("/", anchor=False)
            with subcol4:
                totalVal = st.session_state.PC.pc_hp_max
                entries = []
                for change in filter(lambda change: change.p_property == "pc_hp_max", st.session_state.SheetAttributes.propChangeList):
                    newBonus = lu.evaluate(lu.statifyString(change.p_value)).item()
                    totalVal = totalVal + newBonus
                    entries.append([change.p_source,str(newBonus)])
                with st.popover(str(totalVal), use_container_width=True):
                    st.write("Base HP:")
                    st.number_input("Base HP", key="c_pc_hp_max", on_change=ls.updateChar, kwargs={"fieldType":"hp_max","cacheType":None}, step=1, min_value=0, label_visibility="collapsed")
                    if len(entries) > 0:
                        st.subheader("Bonuses and penalties", anchor=False)
                        for entry in entries:
                            st.write(entry[0] + ": " + entry[1])
            st.divider()
            #Glitches
            subcol1, subcol2 = st.columns([1,1.5],vertical_alignment="center")
            with subcol1:
                st.header("Glitches:", anchor=False)
            with subcol2:
                st.number_input("Glitches", key="c_pc_glitch_current", on_change=ls.updateChar, kwargs={"fieldType":"glitch_current","cacheType":None}, step=1, min_value=0, label_visibility="collapsed")
            with st.container(key="glitch_reset_container"):
                st.button("Reset ("+st.session_state.PC.pc_glitch_roll+")", on_click=ls.rollGlitch, use_container_width=True)
            st.divider()
            #Carrying capacity
            subcol1, subcol2, subcol3, subcol4 = st.columns([4,1,1,4],vertical_alignment="center")
            with subcol1:
                st.header("Carrying Capacity:", anchor=False)
            with subcol2:
                st.header(ls.getCarryWeight(), anchor=False)
            with subcol3:
                st.header("/", anchor=False)
            with subcol4:
                bonus = 0
                entries = []
                for change in filter(lambda change: change.p_property == "pc_carry_max", st.session_state.SheetAttributes.propChangeList):
                    newBonus = lu.evaluate(lu.statifyString(change.p_value)).item()
                    bonus = bonus + newBonus
                    entries.append([change.p_source,str(newBonus)])
                with st.popover(lu.repCarryCap(st.session_state.PC.pc_carry_max, bonus=bonus), use_container_width=True):
                    st.write("Base Capacity: " + lu.repCarryCap(st.session_state.PC.pc_carry_max))
                    if len(entries) > 0:
                        st.subheader("Bonuses and penalties", anchor=False)
                        for entry in entries:
                            st.write(entry[0] + ": " + entry[1])
            st.divider()
            #Credits
            subcol1, subcol2 = st.columns([1,2],vertical_alignment="center")
            with subcol1:
                st.header("Credits:", anchor=False)
            with subcol2:
                st.number_input("Credits", key="c_pc_creds", on_change=ls.updateChar, kwargs={"fieldType":"creds","cacheType":None}, step=1, min_value=0, label_visibility="collapsed")
            #Debt
            subcol1, subcol2 = st.columns([1,3],vertical_alignment="center")
            with subcol1:
                st.header("Debt:", anchor=False)
            with subcol2:
                st.number_input("Debt", key="c_pc_debt", on_change=ls.updateChar, kwargs={"fieldType":"debt","cacheType":None}, step=1, min_value=0, label_visibility="collapsed")
    with col2:
        pass
    with col3:
        with st.container(key="desc_box"):
            subcol1, subcol2, subcol3 = st.columns([2,1,1],vertical_alignment="center")
            with subcol1:
                st.header("Description:", anchor=False)
            if st.session_state.sheetEditDesc:
                with subcol2:
                        st.button("Cancel", key="sheet_cancel_desc", on_click=lsc.sheetCancelDesc, use_container_width=True)
                with subcol3:
                        st.button("Save", key="sheet_save_desc", on_click=lsc.sheetSaveDesc, use_container_width=True)
                st.text_area("Description", height=275, key="c_pc_desc", label_visibility="collapsed")
            else:
                with subcol2:
                    pass
                with subcol3:
                    st.button("Edit", key="sheet_edit_desc", on_click=lsc.sheetEditDesc, use_container_width=True)
                if st.session_state.PC.pc_desc:
                    for descLine in st.session_state.PC.pc_desc.splitlines(): st.write(descLine)
            ls.writeStuffDesc()
            ls.writeFeatures()
    st.divider()
    itemCounter = lcd.ItemCounter()
    tabList = [["Armor and weapons"]]
    if st.session_state.SheetAttributes.itemList:
        tabList.append(["Items",st.session_state.SheetAttributes.itemList])
    if st.session_state.SheetAttributes.cyberwareList:
        tabList.append(["Cyberware",st.session_state.SheetAttributes.cyberwareList])
    if st.session_state.SheetAttributes.appList:
        tabList.append(["Apps",st.session_state.SheetAttributes.appList])
    if st.session_state.SheetAttributes.nanoInfestationList:
        tabList.append(["Nano Powers and Infestations",st.session_state.SheetAttributes.nanoInfestationList])
    if st.session_state.SheetAttributes.unitList:
        tabList.append(["Units and Vehicles",st.session_state.SheetAttributes.unitList])
    tabList.append(["Add Item"])
    tabHolder = st.tabs([tabEntry[0] for tabEntry in tabList])
    with tabHolder[0]:
        #Armor and weapons
        col1, col2, col3 = st.columns([1,1,1],vertical_alignment="top")
        with col1:
            ls.writeArmor()
        for itemIndex,item in enumerate(st.session_state.SheetAttributes.weaponList, start=1):
            if itemIndex%3 == 0:
                col1, col2, col3 = st.columns([1,1,1],vertical_alignment="top")
                column = col1
            elif itemIndex%3 == 1:
                column = col2
            else:
                column = col3
            with column:
                ls.writeStuff(item, itemCounter)
    for tabIndex,tab in enumerate(tabHolder[1:-1],start=1):
        itemList = tabList[tabIndex][1]
        with tab:
            for itemIndex,item in enumerate(itemList):
                if itemIndex%3 == 0:
                    col1, col2, col3 = st.columns([1,1,1],vertical_alignment="top")
                    column = col1
                elif itemIndex%3 == 1:
                    column = col2
                else:
                    column = col3
                with column:
                    ls.writeStuff(item, itemCounter)
    with tabHolder[-1]:
        ls.writeAddItem(itemCounter)