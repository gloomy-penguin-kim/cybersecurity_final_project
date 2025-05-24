from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

from models_attack import Attack

class Target(SQLModel, table=True):
    __tablename__ = "attacks_target"

    target_id: Optional[int] = Field(default=None, primary_key=True)
    id: Optional[str]
    name: Optional[str]
    default_setting: Optional[str]
    order_by: Optional[str]

    attack_id: Optional[int] = Field(default=None, foreign_key="attacks_attack.attack_id")
    attack: Optional[Attack] = Relationship(back_populates="targets")


class TargetResponse(SQLModel):
    target_id: int
    id: int
    name: str
    default_setting: str
    order_by: int