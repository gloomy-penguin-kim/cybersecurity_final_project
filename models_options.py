from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

from models_attack import Attack

class ModuleOptionHeading(SQLModel, table=True):
    __tablename__ = "attacks_option_heading"
    option_heading_id: Optional[int] = Field(default=None, primary_key=True)
    attack_id: int = Field(foreign_key="attacks_attack.attack_id")
    title: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    order_by: Optional[str] = None

    attack: Attack = Relationship(back_populates="option_headings")

    module_options: List["ModuleOption"] = Relationship(back_populates="option_heading")

class ModuleOption(SQLModel, table=True):
    __tablename__ = "attacks_option"
    option_id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str]
    current_setting: Optional[str]
    required: Optional[str]
    description: Optional[str]
    order_by: Optional[str]
    option_heading_id: int = Field(foreign_key="attacks_option_heading.option_heading_id")
    option_heading: "ModuleOptionHeading" = Relationship(back_populates="module_options")

class ModuleOptionResponse(SQLModel):
    id: Optional[str] = None
    order_by: Optional[str] = None
    name: Optional[str] = None
    current_setting: Optional[str] = None
    required: Optional[str] = None
    description: Optional[str] = None

class ModuleOptionHeadingResponse(SQLModel):
    attack_id: Optional[int]
    order_by: Optional[int] = None
    name: Optional[str] = None
    title: Optional[str] = None
    type: Optional[str] = None
    module_options: List[ModuleOptionResponse] = []
#
# class PayloadResponse(SQLModel):
#     payload_id: Optional[int]
#     order_by: Optional[str] = None
#     payload: Optional[str] = None
#     disclosure: Optional[str] = None
#     rank: Optional[str] = None
#     description: Optional[str] = None
#     check_supported: Optional[str] = None
#     payload_headings: List[PayloadOptionHeadingResponse] = []
#
