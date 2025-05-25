
# models/responses.py
from typing import List, Optional
from pydantic import BaseModel

class PayloadOptionResponse(BaseModel):
    id: Optional[str]
    order_by: Optional[str]
    name: Optional[str]
    current_setting: Optional[str]
    required: Optional[str]
    description: Optional[str]

class PayloadOptionHeadingResponse(BaseModel):
    payload_id: Optional[int]
    order_by: Optional[str]
    name: Optional[str]
    title: Optional[str]
    type: Optional[str]
    payload_options: List[PayloadOptionResponse] = []

class PayloadResponse(BaseModel):
    payload_id: Optional[int]
    order_by: Optional[str]
    payload: Optional[str]
    disclosure: Optional[str]
    rank: Optional[str]
    description: Optional[str]
    check_supported: Optional[str]
    payload_headings: List[PayloadOptionHeadingResponse] = []

class ModuleOptionResponse(BaseModel):
    id: Optional[str]
    order_by: Optional[str]
    name: Optional[str]
    current_setting: Optional[str]
    required: Optional[str]
    description: Optional[str]

class ModuleOptionHeadingResponse(BaseModel):
    attack_id: Optional[int]
    order_by: Optional[int]
    name: Optional[str]
    title: Optional[str]
    type: Optional[str]
    module_options: List[ModuleOptionResponse] = []

class TargetResponse(BaseModel):
    target_id: Optional[int]
    id: Optional[int]
    name: Optional[str]
    default_setting: Optional[str]
    order_by: Optional[int]

class AttackResponse(BaseModel):
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
    payload_options: List[PayloadResponse] = []
    targets: List[TargetResponse] = []


class AttackSimple(BaseModel):
    attack_id: Optional[int]
    name: str
    module: str
    rank: Optional[str]
    disclosed: Optional[str]
    check_supported: Optional[str]
    type: Optional[str]

class TargetResponse(BaseModel):
    target_id: int
    id: int
    name: str
    default_setting: str
    order_by: int