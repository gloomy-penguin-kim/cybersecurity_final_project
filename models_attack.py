from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

#from models_payload import Payload


class AttackPayloadLink(SQLModel, table=True):
    __tablename__ = "attacks_attack_payload"
    attack_id: Optional[int] = Field(default=None, foreign_key="attacks_attack.attack_id", primary_key=True)
    payload_id: Optional[int] = Field(default=None, foreign_key="attacks_payload.payload_id", primary_key=True)



class AttackSimple(SQLModel, table=True):
    attack_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    module: str
    rank: Optional[str]
    disclosed: Optional[str]
    check_supported: Optional[str]
    type: Optional[str]


class Attack(SQLModel, table=True):
    __tablename__ = "attacks_attack"

    attack_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    module: str
    platform: Optional[str]
    arch: Optional[str]
    privileged: Optional[str]
    license: Optional[str]
    rank: Optional[str]
    disclosed: Optional[str]
    provided_by: Optional[str]
    module_side_effects: Optional[str]
    module_stability: Optional[str]
    module_reliability: Optional[str]
    check_supported: Optional[str]
    payload_information: Optional[str]
    description: Optional[str]
    refs: Optional[str]
    type: Optional[str]
    payload_default: Optional[str]

    option_headings: Optional[List["ModuleOptionHeading"]] = Relationship(back_populates="attack")
    targets: Optional[List["Target"]] = Relationship(back_populates="attack")

    payload_options: List["Payload"] = Relationship(
        back_populates="attacks",
        link_model=AttackPayloadLink
    )
