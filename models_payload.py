from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

from models_attack import Attack

class Payload(SQLModel, table=True):
    __tablename__ = "attacks_payload"
    attack_id: Optional[int] = Field(default=None, foreign_key="attacks_attack.attack_id", primary_key=True)
    payload_id: Optional[int] #= Field(default=None, foreign_key="attacks_payload.payload_id", primary_key=True)
    order_by: Optional[str]
    payload: Optional[str]
    disclosure: Optional[str]
    rank: Optional[str]
    description: Optional[str]
    check_supported: Optional[str]

    attack: Attack = Relationship(back_populates="payload_headings")

    payload_headings: List["PayloadOptionHeading"] = Relationship(back_populates="payload")


class PayloadOptionHeading(SQLModel, table=True):
    __tablename__ = "attacks_payload_option_heading"
    payload_option_heading_id: Optional[int] = Field(default=None, primary_key=True)
    payload_id: int = Field(foreign_key="attacks_payload.payload_id")
    title: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    order_by: Optional[str] = None

    payload: Payload = Relationship(back_populates="payload_headings")

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
    payload_option_heading: "PayloadOptionHeading" = Relationship(back_populates="payload_options")

class PayloadOptionResponse(SQLModel):
    id: Optional[str] = None
    order_by: Optional[str] = None
    name: Optional[str] = None
    current_setting: Optional[str] = None
    required: Optional[str] = None
    description: Optional[str] = None

class PayloadOptionHeadingResponse(SQLModel):
    payload_id: Optional[int]
    order_by: Optional[str] = None
    name: Optional[str] = None
    title: Optional[str] = None
    type: Optional[str] = None
    payload_options: List[PayloadOptionResponse] = []

class PayloadResponse(SQLModel):
    payload_id: Optional[int]
    order_by: Optional[str] = None
    payload: Optional[str] = None
    disclosure: Optional[str] = None
    rank: Optional[str] = None
    description: Optional[str] = None
    check_supported: Optional[str] = None
    payload_headings: List[PayloadOptionHeadingResponse] = []

