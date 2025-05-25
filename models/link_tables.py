# models/link_tables.py
from sqlmodel import SQLModel, Field
from typing import Optional

class AttackPayloadLink(SQLModel, table=True):
    __tablename__ = "attacks_attack_payload"
    __table_args__ = {'extend_existing': True}
    attack_id: Optional[int] = Field(default=None, foreign_key="attacks_attack.attack_id", primary_key=True)
    payload_id: Optional[int] = Field(default=None, foreign_key="attacks_payload.payload_id", primary_key=True)
