#!/usr/bin/env python
# 
from typing import Annotated


# uvicorn main:app --reload

import logging

from fastapi import Depends, FastAPI
from sqlmodel import Session, SQLModel, create_engine

from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles

# Setup logging
logger = logging.getLogger("uvicorn.error")

# --- Models ---

# from full_models import Attack, AttackSimple # Payload, PayloadOptionHeading

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

from fastapi import Depends, HTTPException
from sqlmodel import select, Session
from models.attack import Attack  # AttackPayloadLink
from models.payload import Payload
from models.options import ModuleOptionHeading, PayloadOptionHeading
from models.target import Target
from models.responses import PayloadResponse, AttackSimple, ModuleOptionHeadingResponse, TargetResponse, \
    ModuleOptionResponse
from typing import List


@app.get("/attacks", response_model=List[AttackSimple])
def read_attacks(
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = 100,
) -> List[AttackSimple]:
    return session.exec(select(Attack.attack_id, Attack.name, Attack.module,
                               Attack.rank, Attack.disclosed,
                               Attack.check_supported, Attack.type).offset(offset).limit(limit)).all()


@app.post("/attacks")
def get_multiple_attacks_for_attack(attackList: List[int],
                                    session: Session = Depends(get_session)):
    response = []

    for attack_id in attackList:
        attack = session.get(Attack, attack_id)
        if not attack:
            continue  # or collect error info if you want

        response.append(get_single_attack(attack))

    return response


@app.get("/attacks/{attack_id}")
def get_payload_options_for_attack(attack_id: int, session: Session = Depends(get_session)):
    # Get the attack
    attack = session.get(Attack, attack_id)
    if not attack:
        raise HTTPException(status_code=404, detail="Attack not found")

    return get_single_attack(attack)

def get_single_attack(attack: Attack):

    attack_id = attack.attack_id

    payload_options = []

    for payload_loop in attack.payloads:
        for heading in payload_loop.payload_headings:
            heading_options = []
            for option in heading.payload_options:
                heading_options.append({
                    "option_name": option.name,
                    "option_value": option.current_setting,
                    "option_required": option.required,
                    "option_description": option.description,
                    "option_order_by": option.order_by})

            payload_options.append({
                "payload_id": heading.payload_id,
                "payload_name": heading.payload.payload,
                "payload_order_by": heading.order_by,
                "payload_options": heading_options
            })

    option_headings = []
    for option_heading in attack.option_headings:
        heading_options = []
        if "Payload" not in option_heading.title:
            for option in option_heading.module_options:
                heading_options.append({
                    "option_name": option.name,
                    "option_value": option.current_setting,
                    "option_required": option.required,
                    "option_description": option.description,
                    "option_order_by": option.order_by})

            option_headings.append({
                "module_name": option_heading.name,
                "module_title": option_heading.title,
                "module_order_by": option_heading.order_by,
                "module_options": heading_options
            })

    targets = []
    for target in attack.targets:
        targets.append({
            "target_id": target.target_id,
            "id": target.id,
            "name": target.name,
            "default_setting": target.default_setting,
            "order_by": target.order_by
        })

    return {"attack_id": attack_id,
            "module": attack.module,
            "name": attack.name,
            "platform": attack.platform,
            "arch": attack.arch,
            "privileged": attack.privileged,
            "license": attack.license,
            "rank": attack.rank,
            "disclosed": attack.disclosed,
            "provided_by": attack.provided_by,
            "module_side_effects": attack.module_side_effects,
            "module_stability": attack.module_stability,
            "module_reliability": attack.module_reliability,
            "check_supported": attack.check_supported,
            "payload_information": attack.payload_information,
            "description": attack.description,
            "refs": attack.refs,
            "type": attack.type,
            "payload_default": attack.payload_default,
            "payload_options": payload_options,
            "module_options": option_headings,
            "target_options": targets,
            "target": attack.target}


@app.get("/targets", status_code=200, response_model=List[TargetResponse])
def get_all_taargets(session: Session = Depends(get_session)) -> List[TargetResponse]:
    statement = (
        select(Target)
    )
    return session.exec(statement).all()


@app.get("/payloads", status_code=200, response_model=list[PayloadResponse])
def get_all_payloads(
        session: Session = Depends(get_session)) -> List[PayloadResponse]:
    statement = (
        select(Payload)
        .options(
            selectinload(Payload.payload_headings),
            selectinload(Payload.payload_headings).selectinload(PayloadOptionHeading.payload_options)
        )
        .limit(10)
    )
    return session.exec(statement).all()


@app.post("/payloads/{attack_id}", status_code=200, response_model=list[PayloadResponse])
def get_all_payloads(
        attakc_id,
        session: Session = Depends(get_session)) -> List[PayloadResponse]:
    statement = (
        select(Payload)
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


@app.post("/options/{attack_id}", status_code=200, response_model=list[ModuleOptionHeadingResponse])
def get_all_options(
        attack_id,
        session: Session = Depends(get_session)) -> List[PayloadResponse]:
    statement = (
        select(ModuleOptionHeading)
        .where(ModuleOptionHeading.attack_id == attack_id)
        .options(
            selectinload(ModuleOptionHeading.module_options)
        )
    )
    return session.exec(statement).all()


import time
import pexpect
import os
import re
from pydantic import BaseModel


class AttackSubmission(BaseModel):
    attack_id: int
    attack_module: str
    attack_name: str
    RCinfo: str


@app.get('/stop_button', status_code=200)
def stop_button():
    stop_pexpect = True
    return "okay, process stopped"


@app.post("/run_single_attack", status_code=200, response_model=None)
def run_attacks(
        attacks: List[AttackSubmission],
        session: SessionDep):
    results = []
    print(attacks)

    for attack in attacks:
        filename = re.sub("[^a-zA-Z0-9-_]", "_", attack.attack_name)
        filename = os.path.join('temp',
                                filename + "_" + str(round(time.time() * 1000)) + ".rc")
        with open(filename, "w") as file:
            file.write(attack.RCinfo)
        #     file.write("use " + attack.module +"\n")
        #     for option_heading in attack.option_headings:
        #         for option in option_heading.options:
        #             if option.current_setting != "":
        #                 file.write("set " + option.name + " " + option.current_setting + "\n")
        #     for option  in attack.extras:
        #         if option.value != "":
        #             file.write("set " + option.name + " " + option.value + "\n")
        #     if attack.target != "": file.write("set target " + str(attack.target) + "\n")
        #     if attack.payload != "":
        #         file.write("set payload " + str(attack.payload) + "\n")
        #     if attack.check == "run": file.write("exploit\n")
        #     if attack.check == "check": file.write("check\n")

        file_contents = []
        with open(filename, "r") as file:
            file_contents = file.readlines()
            for line in file_contents:
                print(line)
        lines = []

        line_number = 0;

        try:

            result = {}


            stop_pexpect = False

            if stop_pexpect: raise Exception("Stop Button was Pressed.")

            child = pexpect.spawn("msfconsole")
            line_number = 1

            print(str(child))

            child.expect(pexpect.TIMEOUT, timeout=20)
            #child.expect("Metasploit Documentation.*")
            line_number = 2
            child.expect("msf6.*")
            line_number = 3

            child.sendline("resource " + filename)
            line_number = 4
            # child.expect(pexpect.TIMEOUT, timeout=20)
            # child.expect("Metasploit Documentation.*")
            child.expect("msf6.*")
            line_number = 5

            if stop_pexpect: raise Exception("Stop Button was Pressed.")

            successful_session_id = ""
            for line in child.before.splitlines():
                line = line.decode('utf-8')
                line = re.sub(r'\x1b\[[0-9;]*m', '', line)
                lines.append(line)
                matches = re.match("session ([0-9]+) opened", line)
                if matches:
                    successful_session_id = matches.group(1)

            result = {'attack_id': attack.attack_id,
                      'module': attack.attack_module,
                      'response': lines,
                      'PID': "",
                      'session': successful_session_id,
                      'section': 1,
                      'error': False
                      }
            print(results)

            child.send("exit")
            child.sendline("exit")
            child.close()
        except Exception as err:
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            print(err)
            result = {'attack_id': attack.attack_id,
                      'module': attack.attack_module,
                      'response': lines + err,
                      "error": True,
                      'line_number': line_number
                      }
        finally:
            results.append(result)

        if os.path.exists(filename):
            os.remove(filename)
            print(f"File '{filename}' deleted successfully.")
        else:
            print(f"File '{filename}' does not exist.")

    return results

    # child.expect(['msf6 >'])
    # # lines = child.after.splitlines()
    # child.sendLine('use ' + attack.module)
    # child.expect('msf6 >')
    # # lines = child.after.splitlines()
    #
    # for line in lines:
    #     print(line)
    # # lines = []
    # child.sendline('info ' + attack.module)
    # child.expect(['^msf6*'])

    # r = { "before": child.before.splitlines(), "after": child.after.splitlines()}

    # # # while 'msf6 ' not in lines[0].decode('utf-8'):
    # # #     child.expect('msf6 *')
    # # #     lines = child.before.splitlines()

    # child.sendLine('exit')
    # lines = child.after.splitlines()
    # #child.expect(['^msf6*'])
    # child.close()


