
# models/payload.py
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from .link_tables import AttackPayloadLink

if TYPE_CHECKING:
    from .attack import Attack
    from .options import PayloadOptionHeading

class Payload(SQLModel, table=True):
    __tablename__ = "attacks_payload"
    payload_id: Optional[int] = Field(default=None, primary_key=True)
    order_by: Optional[str]
    payload: Optional[str]
    disclosure: Optional[str]
    rank: Optional[str]
    description: Optional[str]
    check_supported: Optional[str]

    payload_headings: List["PayloadOptionHeading"] = Relationship(back_populates="payload")
    attacks: List["Attack"] = Relationship(back_populates="payloads", link_model=AttackPayloadLink)
