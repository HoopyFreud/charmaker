from dataclasses import field
from marshmallow_dataclass import dataclass
from typing import Union,Any
import marshmallow
import marshmallow_dataclass
import copy
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
        case "Armor":
            return Armor.Schema().load(data)
        case "Cyberdeck":
            return Cyberdeck.Schema().load(data)
        case "Cyberware":
            return Cyberware.Schema().load(data)
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
        
class AnyStuffType():
    pass

class BaseSchema(marshmallow.Schema):
    TYPE_MAPPING = {AnyStuffType: AnyStuffField}

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
    pc_carrying_max:int = None
    pc_carrying_current:int = None
    pc_glitch_current:int = None
    pc_glitch_roll:str = None
    pc_creds:int = None
    pc_debt:int = None
    pc_debt_lender:str = None
    pc_stuff:AnyStuffType = field(default_factory=list)
    
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
    
@dataclass(base_schema=BaseSchema)
class DamageField():
    p_damage:str = None
    p_desc:str = None
    p_firemode:Union[list[str],str] = None
    p_mech_bonus:bool = False
    
@dataclass(base_schema=BaseSchema)
class PropChangeField():
    p_property:str = None
    p_value:Union[int,str] = None
    p_dispName:str = None
    
@dataclass(base_schema=BaseSchema)
class Stuff():
    p_name:str = None
    p_desc:str = None
    p_sub_stuff:AnyStuffType = None
    
@dataclass(base_schema=BaseSchema)
class App(Stuff):
    p_damage:DamageField = None
    
@dataclass(base_schema=BaseSchema)
class Feature():
    p_feature_text:str = None
    p_pc_desc_text:str = None
    
@dataclass(base_schema=BaseSchema)    
class Item(Stuff):
    p_uses:int = None
    p_equipped:bool = True
    
@dataclass(base_schema=BaseSchema)
class Armor(Item):
    p_armor:str = None
    
@dataclass(base_schema=BaseSchema)
class Cyberdeck(Item):
    p_slot_max:int = None
    p_slots:list[App] = field(default_factory=list)
    
@dataclass(base_schema=BaseSchema)
class Cyberware(Item):
    p_pc_desc_text:str = None
    p_prop_change:list[PropChangeField] = field(default_factory=list)
    
@dataclass(base_schema=BaseSchema)
class Weapon(Item):
    p_mags:int = None
    p_damage:DamageField = None
    
@dataclass(base_schema=BaseSchema)
class Nano(Stuff):
    pass

@dataclass(base_schema=BaseSchema)
class Infestation(Stuff):
    p_pc_desc_text:str = None
    p_prop_change:list[PropChangeField] = field(default_factory=list)

@dataclass(base_schema=BaseSchema)
class Unit(Stuff):
    p_damage:DamageField = None
    p_armor:str = None
    p_hp_max:int = None
    p_hp_current:int = None

@dataclass(base_schema=BaseSchema)
class Vehicle(Unit):
    pass

@dataclass(base_schema=BaseSchema)
class StuffField:
    p_type:str = None
    p_name:str = None
    p_data:dict[str, Any] = None

def getEmptyRandomItem():
    return StuffField("RandomItem", None, {})