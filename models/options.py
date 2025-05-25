from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .attack import Attack
    from .payload import Payload

class ModuleOptionHeading(SQLModel, table=True):
    __tablename__ = "attacks_option_heading"
    option_heading_id: Optional[int] = Field(default=None, primary_key=True)
    attack_id: int = Field(foreign_key="attacks_attack.attack_id")
    title: Optional[str]
    name: Optional[str]
    type: Optional[str]
    order_by: Optional[str]

    attack: "Attack" = Relationship(back_populates="option_headings")
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

    option_heading: ModuleOptionHeading = Relationship(back_populates="module_options")

class PayloadOptionHeading(SQLModel, table=True):
    __tablename__ = "attacks_payload_option_heading"
    payload_option_heading_id: Optional[int] = Field(default=None, primary_key=True)
    payload_id: int = Field(foreign_key="attacks_payload.payload_id")
    title: Optional[str]
    name: Optional[str]
    type: Optional[str]
    order_by: Optional[str]

    payload: "Payload" = Relationship(back_populates="payload_headings")
    payload_options: List["PayloadOption"] = Relationship(back_populates="payload_option_heading")

class PayloadOption(SQLModel, table=True):
    __tablename__ = "attacks_payload_option"
    payload_option_id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str]
    current_setting: Optional[str]
    required: Optional[str]
    description: Optional[str]
    order_by: Optional[str]
    payload_option_heading_id: int = Field(foreign_key="attacks_payload_option_heading.payload_option_heading_id")

    payload_option_heading: PayloadOptionHeading = Relationship(back_populates="payload_options")
