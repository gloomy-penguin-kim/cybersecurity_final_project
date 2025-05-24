from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship




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
