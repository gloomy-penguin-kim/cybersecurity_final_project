from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel

#from models_response import AttackResponse
#from models_response import PayloadResponse
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



#from models_payload import Payload

#
# class AttackPayload(SQLModel, table=True):
#     __tablename__ = "attacks_attack_payload2"
#     attack_id: Optional[int] = Field(default=None, foreign_key="attacks_attack.attack_id", primary_key=True)
#     payload_id: Optional[int]
#     payload: Optional[str]
#     disclosure: Optional[str]
#     rank: Optional[int]
#     check_supported: Optional[str]
#     order_by: Optional[str]
#     description: Optional[str]
#
#     payload_headings: List["PayloadOptionHeading"] = Relationship(back_populates="payload")
#
#
# class AttackPayloadResponse(SQLModel):
#     payload_id: Optional[int]
#     payload: Optional[str]
#     disclosure: Optional[str]
#     rank: Optional[int]
#     check_supported: Optional[str]
#     order_by: Optional[str]
#     description: Optional[str]
