from dataclasses import field
from marshmallow_dataclass import dataclass
from typing import Union,Any
import marshmallow
import marshmallow_dataclass
import copy
import itertools
import streamlit as st

def serializeSuff(value):
    if value is None:
        return None
    return {type(value).__name__:value.Schema().dump(value)}
    
def deserializeSuff(value):
    (classID, data), = value.items()
    match classID:
        case "Stuff":
            return Stuff.Schema().load(data)
        case "App":
            return App.Schema().load(data)
        case "Feature":
            return Feature.Schema().load(data)
        case "Item":
            return Item.Schema().load(data)
        case "Ammo":
            return Ammo.Schema().load(data)
        case "Armor":
            return Armor.Schema().load(data)
        case "Cyberdeck":
            return Cyberdeck.Schema().load(data)
        case "Cyberware":
            return Cyberware.Schema().load(data)
        case "Drug":
            return Drug.Schema().load(data)
        case "Weapon":
            return Weapon.Schema().load(data)
        case "Nano":
            return Nano.Schema().load(data)
        case "Infestation":
            return Infestation.Schema().load(data)
        case "Unit":
            return Unit.Schema().load(data)
        case "Vehicle":
            return Vehicle.Schema().load(data)
        case _:
            return None

class AnyStuffField(marshmallow.fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if isinstance(value,list):
            return [serializeSuff(subValue) for subValue in value]
        else:
            return serializeSuff(value)
    def _deserialize(self, value, attr, obj, **kwargs):
        if isinstance(value,list):
            return [deserializeSuff(subValue) for subValue in value]
        else:
            return deserializeSuff(value)

class AppOrNoneField(marshmallow.fields.Field):
    def __init__(self, *args, **kwargs):
        kwargs['allow_none'] = True
        super().__init__(*args, **kwargs)
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return value.Schema().dump(value)
    def _deserialize(self, value, attr, obj, **kwargs):
        return App.Schema().load(value)

class BoolOrNoneField(marshmallow.fields.Field):
    def __init__(self, *args, **kwargs):
        kwargs['allow_none'] = True
        super().__init__(*args, **kwargs)
        
class AnyStuffType():
    pass
        
class AppOrNoneType():
    pass
        
class BoolOrNoneType():
    pass

class BaseSchema(marshmallow.Schema):
    TYPE_MAPPING = {AnyStuffType: AnyStuffField, AppOrNoneType: AppOrNoneField, BoolOrNoneType: BoolOrNoneField}

@dataclass(base_schema=BaseSchema)
class PC():
    pc_name:str = None
    pc_desc:str = None
    pc_class:str = None
    pc_agi:int = None
    pc_knw:int = None
    pc_pre:int = None
    pc_str:int = None
    pc_tou:int = None
    pc_hp_max:int = None
    pc_hp_current:int = None
    pc_carry_max:str = None
    pc_glitch_current:int = None
    pc_glitch_roll:str = None
    pc_creds:int = None
    pc_debt:int = None
    pc_stuff:AnyStuffType = field(default_factory=list)
    pc_equipped_armor:AnyStuffType = None
        
    def equipNewArmor(self,newArmor):
        self.pc_equipped_armor = newArmor
        for stuffItem in self.pc_stuff:
            if isinstance(stuffItem,Armor):
                if stuffItem == newArmor:
                    if stuffItem.p_equipped is not None:
                        stuffItem.p_equipped = True
                elif stuffItem.p_equipped is not None:
                    stuffItem.p_equipped = False
    
@dataclass(base_schema=BaseSchema)
class DamageField():
    p_damage:str = None
    p_desc:str = None
    p_firemode:Union[list[str],str] = None
    p_mech_bonus:bool = False
    
@dataclass(base_schema=BaseSchema)
class PropChangeField():
    p_property:str = None
    p_value:str = None
    p_dispName:str = None
    p_source:str = None
    
@dataclass(base_schema=BaseSchema)
class Stuff():
    p_name:str = None
    p_desc:str = None
    p_sub_stuff:AnyStuffType = None
    p_prop_change:PropChangeField = None
    
@dataclass(base_schema=BaseSchema)
class App(Stuff):
    p_damage:DamageField = None
    
@dataclass(base_schema=BaseSchema)
class Nano(Stuff):
    pass

@dataclass(base_schema=BaseSchema)
class Infestation(Stuff):
    p_pc_desc_text:str = None
    
@dataclass(base_schema=BaseSchema)
class Feature():
    p_feature_text:str = None
    p_pc_desc_text:str = None
    
@dataclass(base_schema=BaseSchema)    
class Item(Stuff):
    p_uses:int = None
    p_equipped:BoolOrNoneType = True
    
@dataclass(base_schema=BaseSchema)    
class Ammo(Item):
    pass
    
@dataclass(base_schema=BaseSchema)
class Armor(Item):
    p_armor:str = None
    
@dataclass(base_schema=BaseSchema)
class Cyberdeck(Item):
    p_slot_max:int = None
    p_slots:list[AppOrNoneType] = field(default_factory=list)
    
@dataclass(base_schema=BaseSchema)
class Cyberware(Item):
    p_pc_desc_text:str = None
    
@dataclass(base_schema=BaseSchema)    
class Drug(Item):
    pass
    
@dataclass(base_schema=BaseSchema)
class Weapon(Item):
    p_mags:int = None
    p_damage:Union[list[DamageField],DamageField] = None
    
@dataclass(base_schema=BaseSchema)
class Unit(Stuff):
    p_damage:DamageField = None
    p_armor:str = None
    p_hp_current:int = None
    p_hp_max:int = None

@dataclass(base_schema=BaseSchema)
class Vehicle(Unit):
    pass

@dataclass(base_schema=BaseSchema)
class StuffField:
    p_type:str = None
    p_name:str = None
    p_data:dict[str, Any] = None

@dataclass(base_schema=BaseSchema)
class SheetAttributes():
    stuff:AnyStuffType = field(default_factory=list)
    flatStuffList:AnyStuffType = field(default_factory=list)
    appList:AnyStuffType = field(default_factory=list)
    armorList:AnyStuffType = field(default_factory=list)
    cyberwareList:AnyStuffType = field(default_factory=list)
    itemList:AnyStuffType = field(default_factory=list)
    nanoInfestationList:AnyStuffType = field(default_factory=list)
    unitList:AnyStuffType = field(default_factory=list)
    weaponList:AnyStuffType = field(default_factory=list)
    propChangeList:list[PropChangeField] = field(default_factory=list)
    currentCarry:int = 0

    def __post_init__(self):
        self.updateStuff(self.stuff)
            
    def updateStuff(self,stuffList):
        self.stuff = stuffList
        self.callAllUpdates()
        
    def callAllUpdates(self):
        self.updateFlatStuffList()
        self.updateAppList()
        self.updateArmorList()
        self.updateCyberwareList()
        self.updateItemList()
        self.updateNanoInfestationList()
        self.updateUnitList()
        self.updateWeaponList()
        self.updateCurrentCarry()
        self.updatePropChangeList()
            
    def updateAppList(self):
        self.appList = [stuffItem for stuffItem in self.stuff if isinstance(stuffItem,App)]
            
    def updateArmorList(self):
        self.armorList = [stuffItem for stuffItem in self.stuff if isinstance(stuffItem,Armor)]
            
    def updateCyberwareList(self):
        self.cyberwareList = [stuffItem for stuffItem in self.stuff if isinstance(stuffItem,Cyberware)]
            
    def updateItemList(self):
        self.itemList = [stuffItem for stuffItem in self.stuff if isinstance(stuffItem,Item) and (not isinstance(stuffItem,Armor)) and (not isinstance(stuffItem,Ammo)) and (not isinstance(stuffItem,Weapon)) and (not isinstance(stuffItem,Cyberware))]
        self.itemList.sort(key = lambda item: str(type(item)))
            
    def updateNanoInfestationList(self):
        self.nanoInfestationList = [stuffItem for stuffItem in self.stuff if isinstance(stuffItem,Nano) or isinstance(stuffItem,Infestation)]
            
    def updateUnitList(self):
        self.unitList = [stuffItem for stuffItem in self.stuff if isinstance(stuffItem,Unit)]
            
    def updateWeaponList(self):
        self.weaponList = [stuffItem for stuffItem in self.stuff if (isinstance(stuffItem,Weapon) or isinstance(stuffItem,Ammo))]
        
    def updateCurrentCarry(self):
        self.currentCarry = sum(1 for stuffItem in self.stuff if isinstance(stuffItem,Item) and stuffItem.p_equipped and not isinstance(stuffItem,Cyberware))
        
    def updatePropChangeList(self):
        self.propChangeList = []
        for item in self.flatStuffList:
            if isinstance(item,Stuff) and item.p_prop_change is not None:
                self.propChangeList.append(item.p_prop_change)
            
    def recursiveListFlatten(self,inItem):
        self.flatStuffList.append(inItem)
        if isinstance(inItem,Stuff) and inItem.p_sub_stuff is not None:
            self.recursiveListFlatten(inItem.p_sub_stuff)
            
    def updateFlatStuffList(self):
        if self.stuff:
            self.flatStuffList = []
            for item in self.stuff:
                self.recursiveListFlatten(item)

def getEmptyRandomItem():
    return StuffField("RandomItem", None, {})

def getCustomStuffField(stuffType):
    return StuffField(stuffType, "Custom", {})
    
class ItemCounter():
    def __init__(self):
        self.subCounter = None
        self.reset()
    def reset(self, resetVal = 0):
        self.c = itertools.count(start = resetVal)
        if self.subCounter is not None:
            self.subCounter.reset()
    def getNext(self):
        return next(self.c)
    def getSubCounter(self):
        if self.subCounter is None:
            self.subCounter = ItemCounter()
        return self.subCounter