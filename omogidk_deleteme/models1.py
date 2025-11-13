# from typing import List, Optional
# from sqlmodel import SQLModel, Field, Relationship
#
#
# class AttackPayloadLink(SQLModel, table=True):
#     __tablename="attacks_attack_payload"
#     attack_id: int = Field(foreign_key="attacks_attack.attack_id", primary_key=True)
#     payload_id: int = Field(foreign_key="attacks_payload.payload_id", primary_key=True)
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
#     #option_headings: List["OptionHeading"] = Relationship(back_populates="attack")
#     #payloads: List["AttackPayloadLink"] = Relationship(back_populates="attacks") # , link_model=AttackPayloadLink)
#
#
#     payloads: List["Payload"] = Relationship(
#         back_populates="attacks",
#         link_model=AttackPayloadLink
#     )
#
# #
# # class OptionHeading(SQLModel, table=True):
# #     option_heading_id: int = Field(primary_key=True)
# #     title: str
# #     attack_id: int = Field(foreign_key="attacks_attack.attack_id")
# #
# #     attack: Attack = Relationship(back_populates="option_headings")
# #     options: List["Option"] = Relationship(back_populates="option_heading")
# #
# # class Option(SQLModel, table=True):
# #     option_id: int = Field(primary_key=True)
# #     name: str
# #     option_heading_id: int = Field(foreign_key="attacks_option_heading.option_heading_id")
# #
# #     option_heading: OptionHeading = Relationship(back_populates="options")
#
# # class Payload(SQLModel, table=True):
# #     payload_id: int = Field(primary_key=True)
# #     payload: str
# #
# #     attacks: List[Attack] = Relationship(back_populates="payloads", link_model=AttackPayloadLink)
# #     payload_headings: List["PayloadOptionHeading"] = Relationship(back_populates="payload")
#
# class Payload(SQLModel, table=True):
#     __tablename__ = "attacks_payload"
#
#     payload_id: Optional[int] = Field(default=None, primary_key=True)
#     order_by: Optional[str]
#     payload: Optional[str]
#     disclosure: Optional[str]
#     rank: Optional[str]
#     check_supported: Optional[str]
#     description: Optional[str]
#
#     attacks: List["Attack"] = Relationship(
#         back_populates="payloads",
#         link_model=AttackPayloadLink
#     )
#     payload_headings: List["PayloadOptionHeading"] = Relationship(back_populates="payload")
#
# class PayloadOptionHeading(SQLModel, table=True):
#     payload_option_heading_id: int = Field(primary_key=True)
#     payload_id: int = Field(foreign_key="attacks_payload.payload_id")
#     title: str
#
#     payload: Payload = Relationship(back_populates="payload_headings")
#     payload_options: List["PayloadOption"] = Relationship(back_populates="payload_option_heading")
#
# class PayloadOption(SQLModel, table=True):
#     payload_option_heading_id: int = Field(primary_key=True)
#     payload_id: int = Field(foreign_key="attacks_payload.payload_id")
#     title: str
#     payload_option_heading_id: int = Field(foreign_key="attacks_payload_option_heading.payload_option_heading_id")
#
#     payload_option_heading: PayloadOptionHeading = Relationship(back_populates="payload_options")
#
#     payload: Payload = Relationship(back_populates="payload_headings")
#     payload_options: List["PayloadOption"] = Relationship(back_populates="payload_option_heading")
#
#
# # -----------------------------------------------------------------------------------------------------
#
#
# class AttackSimple(SQLModel, table=True):
#     attack_id: Optional[int] = Field(default=None, primary_key=True)
#     name: str
#     module: str
#     rank: Optional[str]
#     disclosed: Optional[str]
#     check_supported: Optional[str]
#     type: Optional[str]
