from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

from models_options import  ModuleOptionHeadingResponse
from models_payload import PayloadResponse
from models_target import TargetResponse

class AttackResponse(SQLModel):
    attack_id: int
    name: Optional[str]
    module: Optional[str]
    platform: Optional[str]
    arch: Optional[str]
    privileged: Optional[str]
    license: Optional[str]
    rank: Optional[str]
    disclosed: Optional[str]
    provided_by: Optional[str]
    module_side_effects: Optional[str]
    module_stability: Optional[str]
    module_reliability: Optional[str]
    check_supported: Optional[str]
    payload_information: Optional[str]
    description: Optional[str]
    refs: Optional[str]
    type: Optional[str]
    payload_default: Optional[str]
    option_headings: List[ModuleOptionHeadingResponse] = []
    payload_headings: List[PayloadResponse] = []
    targets: List[TargetResponse] = []


