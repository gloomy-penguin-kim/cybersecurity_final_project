from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

#from models_options import  ModuleOptionHeadingResponse
#from models_target import TargetResponse

from pydantic import BaseModel

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
#
# class AttackPayloadLink(SQLModel, table=True):
#     __tablename__ = "attacks_attack_payload"
#     attack_id: Optional[int] = Field(default=None, foreign_key="attacks_attack.attack_id", primary_key=True)
#     payload_id: Optional[int] = Field(default=None, foreign_key="attacks_payload.payload_id", primary_key=True)
#
#     attack: "Attack" = Relationship(back_populates="payload_links")
#     payload: "Payload" = Relationship(back_populates="attack_links")
#
# class AttackPayloadLinkResponse(BaseModel):
#     attack_payload_link_id: Optional[int]  # if you have an ID field
#     attack_id: int
#     payload_id: int
#     # add any link-specific fields here, if any
#     #attack: AttackResponse
#     payload: PayloadResponse