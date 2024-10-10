import copy

class PC():
    pc_name = None
    pc_desc = None
    pc_class = None
    pc_agi = None
    pc_knw = None
    pc_pre = None
    pc_str = None
    pc_tou = None
    pc_hp_max = None
    pc_hp_current = None
    pc_carrying_max = None
    pc_carrying_current = None
    pc_glitch_current = None
    pc_glitch_roll = None
    pc_creds = None
    pc_debt = None
    pc_debt_lender = None
    pc_stuff = []
    
    def flatStuffList(self):
        return self.recursiveListFlatten(copy.deepcopy(self.pc_stuff))

    def recursiveListFlatten(self,inList):
        if isinstance(inList,list):
            for item in inList:
                if not isinstance(item,Feature):
                    if item.p_sub_stuff is not None:
                        inList.append(self.recursiveListFlatten(item.p_sub_stuff))
        return inList
        
    def getCurrentCarry(self):
        return 5
    
class DamageField():
    p_damage = None
    p_desc = None
    p_firemode = None
    p_mech_bonus = False
    
class PropChangeField():
    p_property = None
    p_value = None
    p_dispName = None
    
    def __init__(self, p_property, p_value, p_dispName):
        self.p_property = p_property
        self.p_value = p_value
        self.p_dispName = p_dispName
    
class Stuff():
    p_name = None
    p_desc = None
    p_sub_stuff = None
    
class Feature():
    p_feature_text = None
    p_pc_desc_text = None
    
class Nano(Stuff):
    pass

class Infestation(Stuff):
    p_pc_desc_text = None
    p_prop_change = []
    
class App(Stuff):
    p_damage = None

class Unit(Stuff):
    p_damage = None
    p_armor = None
    p_hp_max = None
    p_hp_current = None

class Vehicle(Unit):
    pass

class Item(Stuff):
    p_uses = None
    p_equipped = True
    
class Armor(Item):
    p_armor = None
    
class Cyberdeck(Item):
    p_slot_max = None
    p_slots = None
    
class Cyberware(Item):
    p_pc_desc_text = None
    p_prop_change = []
    
class Weapon(Item):
    p_mags = None
    p_damage = None
    
class StuffField:
    p_type = None
    p_name = None
    p_data = None
    p_source = None
    
    def __init__(self, p_type, p_name, p_data, p_source = None):
        self.p_type = p_type
        self.p_name = p_name
        self.p_data = p_data
        self.p_source = p_source
        
    def __eq__(self, other):
        if self and other:
            return [self.p_type, self.p_name, self.p_data, self.p_source] == [other.p_type, other.p_name, other.p_data, other.p_source]
        return False
        
    def as_dict(self):
        return {"Type":self.p_type, "Name":self.p_name, "Data":self.p_data, "Source":self.p_source}

def getEmptyRandomItem():
    return StuffField("RandomItem", None, {})