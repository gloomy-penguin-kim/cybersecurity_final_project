from typing import Annotated, List, Optional
from sqlalchemy.orm import load_only


import logging

from fastapi import Depends, FastAPI, Query
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select, join

from fastapi.middleware.cors import CORSMiddleware

from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles

import pexpect
import time
import os
import string
import re

from models_response import AttackResponse

# Setup logging
logger = logging.getLogger("uvicorn.error")

# --- Models ---

#from full_models import Attack, AttackSimple # Payload, PayloadOptionHeading

# --- Database setup ---

sqlite_file_name = "/home/kim/Documents/Output/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# --- App ---

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:5173/",
]
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["POST", "GET", "PUT", "DELETE", "OPTIONS"],
        allow_headers=['*']
    )
]



app = FastAPI(middleware=middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static", html=True), name="static")
 
from sqlalchemy.orm import selectinload


PAGE_SIZE = 50 

# AttackRead
# from models_attack import Attack, AttackSimple
# @app.get("/attacks/", response_model=List[AttackSimple])
# def read_attacks(
#     session: Session = Depends(get_session),
#     offset: int = 0,
#     limit: int = 100,
# ) -> List[AttackSimple]:
#     return session.exec(select(Attack.attack_id, Attack.name, Attack.module,
#                                 Attack.rank, Attack.disclosed,
#                                 Attack.check_supported, Attack.type).offset(offset).limit(limit)).all()


from sqlmodel import col

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, col, Session
from sqlalchemy.orm import selectinload
from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List

from models_payload import (
    PayloadOptionHeading, PayloadOption,
    PayloadResponse, PayloadOptionHeadingResponse, PayloadOptionResponse
)
from models_options import (
    ModuleOptionHeading,
    ModuleOptionHeadingResponse, ModuleOptionResponse
)
from models_target import (
    Target, TargetResponse
)
from models_attack import (
    Attack, AttackSimple
)
from models_response import (
    AttackResponse
)
# from models_attack_payload import (
#     AttackPayload, AttackPayloadResponse
# )

@app.get("/attacks", response_model=List[AttackSimple])
def read_attacks(
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = 100,
) -> List[AttackSimple]:
    return session.exec(select(Attack.attack_id, Attack.name, Attack.module,
                                Attack.rank, Attack.disclosed,
                                Attack.check_supported, Attack.type).offset(offset).limit(limit)).all()


@app.post("/attacks", status_code=200) # , response_model=List[AttackRead])
def post_attacks(
    attackList: List[int],
    session: Session = Depends(get_session),
):
    statement = (
        select(Attack)
        .where(Attack.attack_id.in_(attackList))
        # .options(
        #     selectinload(Attack.payloads)
        #     .selectinload(Payload.payload_headings)
        # )
    )
    results = session.exec(statement).all()
    return results




#
# @app.get("/attacks/{attack_id}")
# def getOneAttack(
#         attack_id,
#         session: Session = Depends(get_session)
#     ):
#
#     statement = (
#         select(Attack)
#         .where(Attack.attack_id == attack_id)
#         .options(
#             #selectinload(Attack.payloads
#         selectinload(Payload.payload_headings).selectinload(PayloadOptionHeading.payload_options),
#         selectinload(Attack.targets),
#         selectinload(Attack.option_headings),
#         )
#     )
#     result = session.exec(statement).first()
#
#     if not result:
#         raise HTTPException(status_code=404, detail="Attack not found")
#
#     return result
#
# def build_attack_response(attack: Attack) -> AttackResponse:
#     return AttackResponse(
#         attack_id=attack.attack_id,
#         name=attack.name,
#         module=attack.module,
#         platform=attack.platform,
#         arch=attack.arch,
#         privileged=attack.privileged,
#         license=attack.license,
#         rank=attack.rank,
#         disclosed=attack.disclosed,
#         provided_by=attack.provided_by,
#         module_side_effects=attack.module_side_effects,
#         module_stability=attack.module_stability,
#         module_reliability=attack.module_reliability,
#         check_supported=attack.check_supported,
#         payload_information=attack.payload_information,
#         description=attack.description,
#         refs=attack.refs,
#         type=attack.type,
#         payload_default=attack.payload_default,
#         option_headings=[
#             ModuleOptionHeadingResponse(
#                 attack_id=attack.attack_id,
#                 order_by=option_heading.order_by,
#                 name=option_heading.name,
#                 title=option_heading.title,
#                 type=option_heading.type
#             )
#             for option_heading in (attack.option_headings or [])
#         ],
#         payload_headings=[
#             PayloadResponse(
#                 payload_id=payload.payload_id,
#                 attack_id=payload.attack_id,
#                 order_by=payload.order_by,
#                 rank=payload.rank,
#                 description=payload.description,
#                 payload=payload.payload,
#                 check_supported=payload.check_supported,
#                 compatible_payloads=[
#                     PayloadOptionHeadingResponse(
#                         payload_id=heading.payload_id,
#                         order_by=str(heading.order_by) if heading.order_by is not None else None,
#                         name=heading.name,
#                         title=heading.title,
#                         type=heading.type,
#                         payload_options=[
#                             PayloadOptionResponse(
#                                 payload_id=heading.payload_id,
#                                 order_by=str(opt.order_by) if opt.order_by is not None else None,
#                                 name=opt.name,
#                                 current_setting=opt.current_setting,
#                                 required=opt.required,
#                                 description=opt.description,
#                             )
#                             for opt in (heading.payload_options or [])
#                         ]
#                     )
#                     for heading in (payload.payload_headings or [])
#                 ]
#
#                 )
#             for payload in (attack.payload_headings or [])
#         ],
#         targets=[
#             TargetResponse(
#                 target_id=target.target_id,
#                 id=target.id,
#                 name=target.name,
#                 default_setting=target.default_setting,
#                 order_by=target.order_by
#             )
#             for target in (attack.targets or [])
#         ]
#     )


@app.get("/targets", status_code=200, response_model=List[TargetResponse])
def get_all_taargets(session: Session = Depends(get_session)) -> List[TargetResponse]:
    statement = (
        select(Target)
    )
    return session.exec(statement).all()

@app.post("/payloads", status_code=200, response_model=list[PayloadResponse])
def get_all_payloads(
        attack_id,
        session: Session = Depends(get_session)) -> List[PayloadResponse]:
    statement = (
        select(Payload)
        .where(Payload.attack_id == attack_id)
        .options(
            selectinload(Payload.payload_headings),
            selectinload(Payload.payload_headings).selectinload(PayloadOptionHeading.payload_options)
        )
        .limit(10)
    )
    return session.exec(statement).all()

@app.get("/options", status_code=200, response_model=list[ModuleOptionHeadingResponse])
def get_all_options(session: Session = Depends(get_session)) -> List[PayloadResponse]:
    statement = (
        select(ModuleOptionHeading)
        .options(
            selectinload(ModuleOptionHeading.module_options)
        )
    )
    return session.exec(statement).all()











    # return [
    #     PayloadResponse(
    #         payload_id=payload.payload_id,
    #         order_by=payload.order_by,
    #         payload=payload.payload,
    #         disclosure=payload.disclosure,
    #         rank=payload.rank,
    #         description=payload.description,
    #         check_supported=payload.check_supported,
    #         payload_headings=[
    #             PayloadOptionHeadingResponse(
    #                 payload_id=heading.payload_id,
    #                 order_by=heading.order_by,
    #                 name=heading.name,
    #                 title=heading.title,
    #                 type=heading.type,
    #                 payload_options=[
    #                     PayloadOptionResponse(
    #                         payload_id=heading.payload_id,
    #                         order_by=opt.order_by,
    #                         name=opt.name,
    #                         current_setting=opt.current_setting,
    #                         required=opt.required,
    #                         description=opt.description,
    #                     )
    #                     for opt in heading.payload_options
    #                 ]
    #             )
    #             for heading in payload.payload_headings
    #         ]
    #     )
    #     for payload in payloads
    # ]




#
# #
# # @app.post("/run", status_code=200)
# # def read_attacks(
# #         attacks: List[AttackRequest],
# #         session: SessionDep):
# #     results = []
# #     print(len(attacks))
# #     print(attacks)
# #     for attack in attacks:
# #         filename = attack.name.replace(" ","_")+"_"+str(round(time.time() * 1000))+".rc"
# #         with open(filename, "w") as file:
# #             file.write("use " + attack.module +"\n")
# #             for option_heading in attack.option_headings:
# #                 for option in option_heading.options:
# #                     if option.current_setting != "":
# #                         file.write("set " + option.name + " " + option.current_setting + "\n")
# #             for option  in attack.extras:
# #                 if option.value != "":
# #                     file.write("set " + option.name + " " + option.value + "\n")
# #             if attack.target != "": file.write("set target " + str(attack.target) + "\n")
# #             if attack.payload != "":
# #                 file.write("set payload " + str(attack.payload) + "\n")
# #             if attack.check == "run": file.write("exploit\n")
# #             if attack.check == "check": file.write("check\n")
# #
# #         file_contents = []
# #         with open(filename, "r") as file:
# #             file_contents = file.readlines()
# #             for line in file_contents:
# #                 print(line)
# #         lines = []
# #
# #         try:
# #             child = pexpect.spawn("msfconsole -r " + filename)
# #             child.expect(pexpect.TIMEOUT, timeout=5)
# #             child.expect("Metasploit Documentation.*")
# #             print(child.after)
# #             child.expect("msf6.*")
# #             for line in child.before.splitlines():
# #                 line = line.decode('utf-8')
# #                 line = re.sub(r'\x1b\[[0-9;]*m', '', line)
# #                 lines.append(line)
# #
# #             results.append({ 'attack_id': attack.attack_id,
# #                              'module': attack.module,
# #                              'response': lines
# #                             })
# #             print(child.before.splitlines())
# #             # print(child.after.splitlines()
# #             child.send("exit")
# #             child.sendline("exit")
# #             child.close()
# #         except:
# #             results.append({ 'attack_id': attack.attack_id,
# #                              'module': attack.module,
# #                              'response': lines
# #                             })
# #
# #         if os.path.exists(filename):
# #             os.remove(filename)
# #             print(f"File '{filename}' deleted successfully.")
# #         else:
# #             print(f"File '{filename}' does not exist.")
# #
# #
# #     return results
# #
# #
# #
# #
# #     # child.expect(['msf6 >'])
# #     # # lines = child.after.splitlines()
# #     # child.sendLine('use ' + attack.module)
# #     # child.expect('msf6 >')
# #     # # lines = child.after.splitlines()
# #     #
# #     # for line in lines:
# #     #     print(line)
# #     # # lines = []
# #     # child.sendline('info ' + attack.module)
# #     # child.expect(['^msf6*'])
# #
# #     # r = { "before": child.before.splitlines(), "after": child.after.splitlines()}
# #
# #     # # # while 'msf6 ' not in lines[0].decode('utf-8'):
# #     # # #     child.expect('msf6 *')
# #     # # #     lines = child.before.splitlines()
# #
# #     # child.sendLine('exit')
# #     # lines = child.after.splitlines()
# #     # #child.expect(['^msf6*'])
# #     # child.close()
#
#
#