from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

# class AttackSimple(SQLModel, table=True):
#     attack_id: Optional[int] = Field(default=None, primary_key=True)
#     name: str
#     module: str
#     rank: Optional[str]
#     disclosed: Optional[str]
#     check_supported: Optional[str]
#     type: Optional[str]
#
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
#
#     option_headings: List["OptionHeading"] = Relationship(back_populates="attack")
#     targets: List["Target"] = Relationship(back_populates="attack")

#
# class Option(SQLModel, table=True):
#     __tablename__ = "attacks_option"
#
#     option_id: Optional[int] = Field(default=None, primary_key=True)
#     name: Optional[str]
#     current_setting: Optional[str]
#     required: Optional[str]
#     description: Optional[str]
#     order_by: Optional[str]
#
#     option_heading_id: Optional[int] = Field(default=None, foreign_key="attacks_option_heading.option_heading_id")
#     option_heading: Optional["OptionHeading"] = Relationship(back_populates="options")
#
#
# class OptionHeading(SQLModel, table=True):
#     __tablename__ = "attacks_option_heading"
#
#     option_heading_id: Optional[int] = Field(default=None, primary_key=True)
#     title: Optional[str]
#     name: Optional[str]
#     type: Optional[str]
#
#     attack_id: Optional[int] = Field(default=None, foreign_key="attacks_attack.attack_id")
#     attack: Optional["Attack"] = Relationship(back_populates="option_headings")
#
#     options: List["Option"] = Relationship(back_populates="option_heading")
#
#
# class Target(SQLModel, table=True):
#     __tablename__ = "attacks_target"
#
#     target_id: Optional[int] = Field(default=None, primary_key=True)
#     id: Optional[str]
#     name: Optional[str]
#     default_setting: Optional[str]
#     order_by: Optional[str]
#
#     attack_id: Optional[int] = Field(default=None, foreign_key="attacks_attack.attack_id")
#     attack: Optional[Attack] = Relationship(back_populates="targets")
#
#
# class TargetRead(SQLModel):
#     target_id: int
#     id: int
#     name: str
#     default_setting: str
#     order_by: int
#
#
# class OptionRead(SQLModel):
#     option_id: int
#     name: Optional[str]
#     current_setting: Optional[str]
#     required: Optional[str]
#     description: Optional[str]
#     order_by: Optional[str]
#
#
# class OptionHeadingRead(SQLModel):
#     option_heading_id: int
#     title: str
#     name: str
#     type: str
#     options: List[OptionRead] = []
#
#
# class PayloadOptionRead(SQLModel):
#     payload_option_id: int
#     name: Optional[str]
#     current_setting: Optional[str]
#     required: Optional[str]
#     description: Optional[str]
#     order_by: Optional[str]
#
#
# class PayloadHeadingRead(SQLModel):
#     payload_option_heading_id: int
#     payload_title: str  # Maps to title from DB
#     payload_options: List[PayloadOptionRead] = []
#
#
# class AttackRead(SQLModel):
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
#     option_headings: List[OptionHeadingRead] = []
#     payload_headings: List[PayloadHeadingRead] = []
#     targets: List[TargetRead] = []
#
#
# # class PayloadOption(SQLModel, table=True):
# #     __tablename__ = "attacks_payload_option"
# #
# #     payload_option_id: Optional[int] = Field(default=None, primary_key=True)
# #     name: Optional[str]
# #     current_setting: Optional[str]
# #     required: Optional[str]
# #     description: Optional[str]
# #     payload_option_heading_id: Optional[int] = Field(default=None,
# #                                                      foreign_key="attacks_payload_option_heading.payload_option_heading")
# #     order_by: Optional[str]
# #
# #     heading: Optional["PayloadOptionHeading"] = Relationship(back_populates="payload_options")
# #
# #
# # class PayloadOptionHeading(SQLModel, table=True):
# #     __tablename__ = "attacks_payload_option_heading"
# #
# #     payload_option_heading: Optional[int] = Field(default=None, primary_key=True)
# #     name: Optional[str]
# #     title: Optional[str]
# #
# #     payload_options: List["PayloadOption"] = Relationship(back_populates="heading")
#
#
# class OptionExtraRead(SQLModel):
#     id: str
#     name: str
#     value: str
#
#
# class AttackRequest(SQLModel):
#     attack_id: int
#     name: str
#     module: str
#     option_headings: List[OptionHeadingRead] = []
#     target: Optional[str]
#     payload: Optional[str]
#     extras: List[OptionExtraRead] = []
#     check: Optional[str]
#
#
