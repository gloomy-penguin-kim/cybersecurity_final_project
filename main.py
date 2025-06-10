#!/usr/bin/env python3
# 
from typing import Annotated


# uvicorn main:app --reload
 

from fastapi import FastAPI, Depends
from sqlmodel import Session, SQLModel, create_engine

from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles

# Setup logging 

# --- Models ---

# from full_models import Attack, AttackSimple # Payload, PayloadOptionHeading

# --- Database setup ---

sqlite_file_name = "database-exploit.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


# SessionDep = Annotated[Session, Depends(get_session)]

# --- App ---

origins = [
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

from fastapi.responses import HTMLResponse
app.mount("/app", StaticFiles(directory="app", html=True), name="app")
 
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

from fastapi import HTTPException
from sqlmodel import select, Session
from models.attack import Attack  # AttackPayloadLink
from models.payload import Payload
from models.options import ModuleOptionHeading, PayloadOptionHeading
from models.target import Target
from models.responses import PayloadResponse, AttackSimple, ModuleOptionHeadingResponse, TargetResponse, \
    ModuleOptionResponse
from typing import List

session = get_session() 

@app.get("/attacks", response_model=List[AttackSimple])
def read_attacks(
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = 100 
) -> List[AttackSimple]:  
    return session.exec(select(Attack.attack_id, 
                               Attack.name, 
                               Attack.module,
                               Attack.rank, 
                               Attack.disclosed,
                               Attack.session_required, 
                               Attack.type, 
                               Attack.refs,
                               Attack.description).offset(offset).limit(limit)).all()


@app.post("/attacks")
def get_multiple_attacks_for_attack(
        attackList: List[int],
        session: Session = Depends(get_session)):
    response = []

    for attack_id in attackList:
        attack = session.get(Attack, attack_id)
        if not attack:
            continue  # or collect error info if you want

        response.append(get_single_attack(attack))

    return response


@app.get("/attacks/{attack_id}")
def get_payload_options_for_attack(
        attack_id: int,
        session: Session = Depends(get_session)):
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
            "target": attack.target,
            "session_required": attack.session_required}


@app.get("/targets", status_code=200, response_model=List[TargetResponse])
def get_all_targets() -> List[TargetResponse]:
    statement = (
        select(Target)
    )
    return Session(engine).exec(statement).all()


@app.get("/payloads", status_code=200, response_model=list[PayloadResponse])
def get_all_payloads() -> List[PayloadResponse]:
    statement = (
        select(Payload)
        .options(
            selectinload(Payload.payload_headings),
            selectinload(Payload.payload_headings).selectinload(PayloadOptionHeading.payload_options)
        )
        .limit(10)
    )
    return Session(engine).exec(statement).all()


@app.post("/payloads/{attack_id}", status_code=200, response_model=list[PayloadResponse])
def get_all_payloads(
        attakc_id) -> List[PayloadResponse]:
    statement = (
        select(Payload)
        .options(
            selectinload(Payload.payload_headings),
            selectinload(Payload.payload_headings).selectinload(PayloadOptionHeading.payload_options)
        )
        .limit(10)
    )
    return Session(engine).exec(statement).all()


@app.get("/options", status_code=200, response_model=list[ModuleOptionHeadingResponse])
def get_all_options() -> List[PayloadResponse]:
    statement = (
        select(ModuleOptionHeading)
        .options(
            selectinload(ModuleOptionHeading.module_options)
        )
    )
    return Session(engine).exec(statement).all()


@app.post("/options/{attack_id}", status_code=200, response_model=list[ModuleOptionHeadingResponse])
def get_all_options(
        attack_id,
        ) -> List[PayloadResponse]:
    statement = (
        select(ModuleOptionHeading)
        .where(ModuleOptionHeading.attack_id == attack_id)
        .options(
            selectinload(ModuleOptionHeading.module_options)
        )
    )
    return Session(engine).exec(statement).all()


import time
import pexpect
import os
import re
from pydantic import BaseModel
import pexpectfile as p


class AttackSubmission(BaseModel):
    attack_id: int
    attack_module: str
    attack_name: str
    RCinfo: str


@app.get('/stop_button', status_code=200)
def stop_button():
    stop_pexpect = True
    return "okay, process stopped"

@app.get("/close_session/{session_id}", status_code=200, response_model=None)
def get_open_sesssions(session_id):
    try: 
        p.child.expect(pexpect.TIMEOUT, timeout=3)
        p.child.sendline('sessions -K -S "session_id:' + str(int(session_id)) + '"')
        p.child.expect("msf6.*")
        print(p.child.before.splitlines()) 
        print(len(p.child.before.splitlines()) )
    except Exception as e: 
        p.spawn_msf_child() 
        get_open_sesssions()
 

@app.get("/get_sessions", status_code=200, response_model=None)
def get_open_sesssions(): 

    p.child.expect(pexpect.TIMEOUT, timeout=3)
    p.child.sendline('sessions -v')
    p.child.expect("msf6.*")
    print(p.child.before.splitlines()) 
    print(len(p.child.before.splitlines()) )

    lines = p.child.before.splitlines() 

    if len(lines) > 6 and 'No active sessions' in lines[6].decode('utf-8'):
        return [] 
    
    lines = lines[6:]

    i = 0 
    results = [] 
    row = {} 
    for line in lines: 
        line = line.decode('utf-8')

        if "Session ID:" in line: 
            row["session_id"] = line.split(':')[1].strip() 
        if "Name:" in line: 
            if len(line.split(':')) >= 2: 
                row["name"] = line.split(':')[1].strip() 
        if "Type:" in line: 
            row["type"] = line.split(':')[1].strip() 
        if "Info:" in line: 
            row["info"] = line.split(':')[1].strip() 
        if "Tunnel:" in line: 
            row["tunnel"] = line.split(':')[1].strip() 
        if "Via:" in line: 
            row["via"] = line.split(':')[1].strip() 
        if "Encrypted:" in line: 
            row["encrypted"] = line.split(':')[1].strip() 
        if "UUID:" in line: 
            if len(line.split(':')) >= 2: 
                row["uuid"] = line.split(':')[1].strip() 
        if "CheckIn:" in line: 
            row["checkin"] = line.split(':')[1].strip() 
        if "Registered:" in line: 
            row["registered"] = line.split(':')[1].strip() 

        if line == "":
            if row != {}: results.append(row) 
            row = {} 

    return results

@app.get("/send_control_z") 
def send_control_z(): 
    print("PID => "+ str(p.child.pid))
    p.child.sendcontrol('z')
    p.child.sendcontrol('Z')
    p.child.close() 

# [
#     "sessions -v",
#     "","[0m",
#     "Active sessions",
#     "===============",
#     "",
#     "  Session ID: 1",
#     "        Name: ",
#     "        Type: postgresql Linux",
#     "        Info: PostgreSQL postgres @ 127.0.0.1:5432",
#     "      Tunnel: 127.0.0.1:36633 -> 127.0.0.1:5432 (127.0.0.1)",
#     "         Via: auxiliary/scanner/postgres/postgres_login",
#     "   Encrypted: No",
#     "        UUID: ",
#     "     CheckIn: <none>",
#     "  Registered: No",
#     "",
#     "",
#     "","[4m"


@app.post("/run_single_attack", status_code=200, response_model=None)
def run_attacks(
        attacks: List[AttackSubmission]):
    results = []
    print(attacks)

    for attack in attacks:
        filename = re.sub("[^a-zA-Z0-9-_]", "_", attack.attack_name)
        filename = re.sub("\\s+", "_", filename)
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
 
 

            # child = pexpect.spawn("msfconsole")  
            # line_number = 1

            # print(str(child))

            p.child.expect(pexpect.TIMEOUT, timeout=20)
            # #child.expect("Metasploit Documentation.*")
            # line_number = 2
            # child.expect("msf6.*")
            line_number = 3

            p.child.sendline("resource " + filename)
            line_number = 4
            # child.expect(pexpect.TIMEOUT, timeout=20)
            # child.expect("Metasploit Documentation.*")
            p.child.expect("msf6.*")
            line_number = 5
  
            successful_session_id = ""
            for line in p.child.before.splitlines():
                line = line.decode('utf-8')
                line = re.sub(r'\x1b\[[0-9;]*m', '', line)
                lines.append(line)
                matches = re.match(".*session ([0-9]+) opened.*", line)
                if matches:
                    successful_session_id = matches.group(1)

            result = {'attack_id': attack.attack_id,
                      'module': attack.attack_module,
                      'response': lines,
                      'PID': p.child.pid,
                      'session': successful_session_id,
                      'section': 1,
                      'error': False
                      }
            print(results)

            # child.send("exit")
            # child.sendline("exit")
            # child.close()
        except Exception as err:
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            print(err) 
            result = {'attack_id': attack.attack_id,
                      'module': attack.attack_module,
                      'response': ["Unexpected " + str(err) + ", " + str(type(err))],
                      "error": True,
                      'line_number': line_number
                      }
            p.spawn_msf_child() 

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

import uvicorn 

port_number = os.environ.get("VITE_METASPLOIT_PORT") or 8084

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(port_number), reload=True)