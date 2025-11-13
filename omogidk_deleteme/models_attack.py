# from typing import List, Optional
# from sqlmodel import SQLModel, Field, Relationship
# from pydantic import BaseModel
#
#
# class AttackSimple(BaseModel):
#     attack_id: Optional[int] = Field(default=None, primary_key=True)
#     name: str
#     module: str
#     rank: Optional[str]
#     disclosed: Optional[str]
#     check_supported: Optional[str]
#     type: Optional[str]


# class AttackPayloadLink(SQLModel, table=True):
#     __tablename__ = "attacks_attack_payload"
#     attack_id: Optional[int] = Field(default=None, foreign_key="attacks_attack.attack_id", primary_key=True)
#     payload_id: Optional[int] = Field(default=None, foreign_key="attacks_payload.payload_id", primary_key=True)
#
#     attack: "Attack" = Relationship(back_populates="payload_links")
#     payload: "Payload" = Relationship(back_populates="attack_links")

#
# class Attack(SQLModel, table=True):
#     __tablename__ = "attacks_attack"
#
#     attack_id: Optional[int] = Field(default=None, primary_key=True)
#     name: str
#     module: str
#     platform: Optional[str]
#     arch: Optional[str]
#     privileged: Optional[str]
#     license: Optional[str]
#     rank: Optional[str]
#     disclosed: Optional[str]
#     provided_by: Optional[str]
#     module_side_effects: Optional[str]
#     module_stability: Optional[str]
#     module_reliability: Optional[str]
#     check_supported: Optional[str]
#     payload_information: Optional[str]
#     description: Optional[str]
#     refs: Optional[str]
#     type: Optional[str]
#     payload_default: Optional[str]
#     option_headings: Optional[List["ModuleOptionHeading"]] = Relationship(back_populates="attack")
#     #payload_headings: Optional[List["Payload"]] = Relationship(back_populates="attack")
#     targets: Optional[List["Target"]] = Relationship(back_populates="attack")
#
#     payloads: List["Payload"] = Relationship(back_populates="attacks", link_model=AttackPayloadLink)
#
# from models_payload import PayloadOptionHeadingResponse
# class PayloadResponse(BaseModel):
#     payload_id: Optional[int]
#     order_by: Optional[str] = None
#     payload: Optional[str] = None
#     disclosure: Optional[str] = None
#     rank: Optional[str] = None
#     description: Optional[str] = None
#     check_supported: Optional[str] = None
#     payload_headings: List[PayloadOptionHeadingResponse] = []
#
#
# class ModuleOptionResponse(SQLModel):
#     id: Optional[str] = None
#     order_by: Optional[str] = None
#     name: Optional[str] = None
#     current_setting: Optional[str] = None
#     required: Optional[str] = None
#     description: Optional[str] = None
#
#
# class ModuleOptionHeadingResponse(SQLModel):
#     attack_id: Optional[int]
#     order_by: Optional[int] = None
#     name: Optional[str] = None
#     title: Optional[str] = None
#     type: Optional[str] = None
#     module_options: List[ModuleOptionResponse] = []
#
# from models_target import TargetResponse
# class AttackResponse(BaseModel):
#     attack_id: int
#     name: Optional[str]
#     module: Optional[str]
#     platform: Optional[str]
#     arch: Optional[str]
#     privileged: Optional[str]
#     license: Optional[str]
#     rank: Optional[str]
#     disclosed: Optional[str]
#     provided_by: Optional[str]
#     module_side_effects: Optional[str]
#     module_stability: Optional[str]
#     module_reliability: Optional[str]
#     check_supported: Optional[str]
#     payload_information: Optional[str]
#     description: Optional[str]
#     refs: Optional[str]
#     type: Optional[str]
#     payload_default: Optional[str]
#     option_headings: List[ModuleOptionHeadingResponse] = []
#     payload_headings: List[PayloadResponse] = []
#     targets: List[TargetResponse] = []
#
#
# class AttackPayloadLinkResponse(BaseModel):
#     attack_payload_link_id: Optional[int]  # if you have an ID field
#     attack_id: int
#     payload_id: int
#     # add any link-specific fields here, if any
#     # attack: AttackResponse
#     payload: PayloadResponse
#
#
# class ModuleOptionHeading(SQLModel, table=True):
#     __tablename__ = "attacks_option_heading"
#     option_heading_id: Optional[int] = Field(default=None, primary_key=True)
#     attack_id: int = Field(foreign_key="attacks_attack.attack_id")
#     title: Optional[str] = None
#     name: Optional[str] = None
#     type: Optional[str] = None
#     order_by: Optional[str] = None
#
#     attack: Attack = Relationship(back_populates="option_headings")
#
#     module_options: List["ModuleOption"] = Relationship(back_populates="option_heading")
#
# class ModuleOption(SQLModel, table=True):
#     __tablename__ = "attacks_option"
#     option_id: Optional[int] = Field(default=None, primary_key=True)
#     name: Optional[str]
#     current_setting: Optional[str]
#     required: Optional[str]
#     description: Optional[str]
#     order_by: Optional[str]
#     option_heading_id: int = Field(foreign_key="attacks_option_heading.option_heading_id")
#     option_heading: "ModuleOptionHeading" = Relationship(back_populates="module_options")
#
#
#
# class Payload(SQLModel, table=True):
#     __tablename__ = "attacks_payload"
#     payload_id: Optional[int] = Field(default=None, primary_key=True)
#     order_by: Optional[str]
#     payload: Optional[str]
#     disclosure: Optional[str]
#     rank: Optional[str]
#     description: Optional[str]
#     check_supported: Optional[str]
#
#     #attack: Attack = Relationship(back_populates="payload_headings")
#
#     payload_headings: List["PayloadOptionHeading"] = Relationship(back_populates="payload")
#
#
#     attacks: List["Attack"] = Relationship(back_populates="payloads", link_model=AttackPayloadLink)
#
# class PayloadOptionHeading(SQLModel, table=True):
#     __tablename__ = "attacks_payload_option_heading"
#     payload_option_heading_id: Optional[int] = Field(default=None, primary_key=True)
#     payload_id: int = Field(foreign_key="attacks_payload.payload_id")
#     title: Optional[str] = None
#     name: Optional[str] = None
#     type: Optional[str] = None
#     order_by: Optional[str] = None
#
#     payload: Payload = Relationship(back_populates="payload_headings")
#
#     payload_options: List["PayloadOption"] = Relationship(back_populates="payload_option_heading")
#
# class PayloadOption(SQLModel, table=True):
#     __tablename__ = "attacks_payload_option"
#     payload_option_id: Optional[int] = Field(default=None, primary_key=True)
#     name: Optional[str]
#     current_setting: Optional[str]
#     required: Optional[str]
#     description: Optional[str]
#     order_by: Optional[str]
#     payload_option_heading_id: int = Field(foreign_key="attacks_payload_option_heading.payload_option_heading_id")
#     payload_option_heading: "PayloadOptionHeading" = Relationship(back_populates="payload_options")
#
# class PayloadOptionResponse(BaseModel):
#     id: Optional[str] = None
#     order_by: Optional[str] = None
#     name: Optional[str] = None
#     current_setting: Optional[str] = None
#     required: Optional[str] = None
#     description: Optional[str] = None
#
# class PayloadOptionHeadingResponse(BaseModel):
#     payload_id: Optional[int]
#     order_by: Optional[int] = None
#     name: Optional[str] = None
#     title: Optional[str] = None
#     type: Optional[str] = None
#     payload_options: List[PayloadOptionResponse] = []
#
# # class PayloadResponse(BaseModel):
# #     payload_id: Optional[int]
# #     order_by: Optional[str] = None
# #     payload: Optional[str] = None
# #     disclosure: Optional[str] = None
# #     rank: Optional[str] = None
# #     description: Optional[str] = None
# #     check_supported: Optional[str] = None
# #     payload_headings: List[PayloadOptionHeadingResponse] = []