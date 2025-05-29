
# models/attack.py
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from .link_tables import AttackPayloadLink

if TYPE_CHECKING:
    from .payload import Payload
    from .options import ModuleOptionHeading
    from .target import Target

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
    target: Optional[str]

    option_headings: List["ModuleOptionHeading"] = Relationship(back_populates="attack")
    targets: List["Target"] = Relationship(back_populates="attack")
    payloads: List["Payload"] = Relationship(back_populates="attacks", link_model=AttackPayloadLink)
