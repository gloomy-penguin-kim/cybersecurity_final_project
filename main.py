from typing import Annotated, List, Optional

import logging

from fastapi import Depends, FastAPI, Query
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

from fastapi.middleware.cors import CORSMiddleware

from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles

import pexpect
import time
import os
import string
import re

# Setup logging
logger = logging.getLogger("uvicorn.error")

# --- Models ---
class AttackSimple(SQLModel, table=True): 
    attack_id: Optional[int] = Field(default=None, primary_key=True)
    name: str 
    module: str  
    rank: Optional[str]
    disclosed: Optional[str] 
    check_supported: Optional[str] 
    type: Optional[str]

class Attack(SQLModel, table=True):
    __tablename__ = "attacks_attack"

    attack_id: Optional[int] = Field(default=None, primary_key=True)
    name: str 
    module: str 
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

    option_headings: List["OptionHeading"] = Relationship(back_populates="attack")
    targets: List["Target"] = Relationship(back_populates="attack")

class Option(SQLModel, table=True):
    __tablename__ = "attacks_option"

    option_id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str]
    current_setting: Optional[str]
    required: Optional[str]
    description: Optional[str]
    order_by: Optional[str]

    option_heading_id: Optional[int] = Field(default=None, foreign_key="attacks_option_heading.option_heading_id")
    option_heading: Optional["OptionHeading"] = Relationship(back_populates="options")

class OptionHeading(SQLModel, table=True):
    __tablename__ = "attacks_option_heading"

    option_heading_id: Optional[int] = Field(default=None, primary_key=True)
    title: Optional[str]

    attack_id: Optional[int] = Field(default=None, foreign_key="attacks_attack.attack_id")
    attack: Optional["Attack"] = Relationship(back_populates="option_headings")

    options: List["Option"] = Relationship(back_populates="option_heading")


class Target(SQLModel, table=True):
    __tablename__ = "attacks_target"

    target_id: Optional[int] = Field(default=None, primary_key=True)
    id: Optional[str]
    name: Optional[str]
    default_setting: Optional[str]
    order_by: Optional[str]

    attack_id: Optional[int] = Field(default=None, foreign_key="attacks_attack.attack_id")
    attack: Optional[Attack] = Relationship(back_populates="targets")


class TargetRead(SQLModel):
    target_id: int
    id: int  
    name: str
    default_setting: str 
    order_by: int


class OptionRead(SQLModel):
    option_id: int
    name: Optional[str]
    current_setting: Optional[str]
    required: Optional[str]
    description: Optional[str]
    order_by: Optional[str]

class OptionHeadingRead(SQLModel):
    option_heading_id: int
    title: str
    options: List[OptionRead] = []

class AttackRead(SQLModel):
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
    option_headings: List[OptionHeadingRead] = []
    targets: List[TargetRead] = []

class OptionExtraRead(SQLModel):
    id: str
    name: str
    value: str

class AttackRequest(SQLModel):
    attack_id: int
    name: str
    module: str
    option_headings: List[OptionHeadingRead] = []
    target: Optional[str]
    payload: Optional[str]
    extras: List[OptionExtraRead] = []
    check: Optional[str]

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
 

PAGE_SIZE = 50 

# AttackRead 
@app.get("/attacks/", response_model=List[AttackSimple])
def read_attacks(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=500)] = 10,
) -> List[AttackRead]:
    attacks = session.exec(select(Attack).offset(offset).limit(limit)).all()
    return attacks 

@app.get("/attacks/{attack_id}", response_model=AttackRead)
def getOneAttack(
        attack_id,
        session: SessionDep
    ):
    attacks = session.exec(select(Attack).where(Attack.attack_id==attack_id))
    return attacks.first()


@app.post("/run", status_code=200)
def read_attacks(
        attacks: List[AttackRequest],
        session: SessionDep):
    results = []
    print(len(attacks))
    print(attacks)
    for attack in attacks:
        filename = attack.name.replace(" ","_")+"_"+str(round(time.time() * 1000))+".rc"
        with open(filename, "w") as file:
            file.write("use " + attack.module +"\n")
            for option_heading in attack.option_headings:
                for option in option_heading.options:
                    if option.current_setting != "":
                        file.write("set " + option.name + " " + option.current_setting + "\n")
            for option  in attack.extras:
                if option.value != "":
                    file.write("set " + option.name + " " + option.value + "\n")
            if attack.target != "": file.write("set target " + str(attack.target) + "\n")
            if attack.payload != "":
                file.write("set payload " + str(attack.payload) + "\n")
            if attack.check == "run": file.write("exploit\n")
            if attack.check == "check": file.write("check\n")

        file_contents = []
        with open(filename, "r") as file:
            file_contents = file.readlines()
            for line in file_contents:
                print(line)
        lines = []

        try:
            child = pexpect.spawn("msfconsole -r " + filename)
            child.expect(pexpect.TIMEOUT, timeout=5)
            child.expect("Metasploit Documentation.*")
            print(child.after)
            child.expect("msf6.*")
            for line in child.before.splitlines():
                line = line.decode('utf-8')
                line = re.sub(r'\x1b\[[0-9;]*m', '', line)
                lines.append(line)

            results.append({ 'attack_id': attack.attack_id,
                             'module': attack.module,
                             'response': lines
                            })
            print(child.before.splitlines())
            # print(child.after.splitlines()
            child.send("exit")
            child.sendline("exit")
            child.close()
        except:
            results.append({ 'attack_id': attack.attack_id,
                             'module': attack.module,
                             'response': lines
                            })

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

 
 