#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 15:22:00 2024

@author: won
"""
from typing import Optional

import typer
from typing_extensions import Annotated

from LocalClient import LocalClient
from ServerCore import ServerCore
from AlgoClient import AlgoClient

app = typer.Typer()
algo_app = typer.Typer()
editer_app = typer.Typer()

app.add_typer(algo_app, name="algo", help="")
app.add_typer(editer_app, name="edit")

@app.command()
def core():
    core = ServerCore()
    
    core.set_robot_host_port()
    core.set_local_host_port()
    
    core.start_server()

@app.command()
def raw(commend: Annotated[Optional[str],typer.Argument(help="pov: move position way\n\n"
                                          +"mov: move negative way\n\n"
                                          +"rol: rotate direction\n\n"
                                          +"pik: pick load\n\n"
                                          +"plc: place load")] = None,
    num: Annotated[Optional[str],typer.Argument(help="pov and mov -> [block num]\n\n"
                                      +"rol -> (x to y/ y to x) [0/1]\n\n"
                                      +"pik and plc -> [pick or place level]\n\n/*warning! ground level is 1*/")] = None,
    long: Annotated[Optional[str], typer.Option(help="send long str\n\neach commends split by #")]=None):
    local_client = LocalClient()
    if long:
        local_client.is_long = True
        local_client.client_start(log= long)
    else:
        local_client.is_typer = True
        local_client.client_start(commend= commend, num= num)
        
@algo_app.command()
def pik(x: Annotated[Optional[int], typer.Argument()] = None,
        y: Annotated[Optional[int], typer.Argument()] = None,
        level: Annotated[Optional[int], typer.Argument()] = None):
    
    """
    pick goods from (x, y, level) to (0, 0, -1)
    
    (0, 0, -1) mean top of (0, 0)
    """
    
    num = [x, y, level]
    
    algo = AlgoClient()
    algo.initWorkDq()
    
    log = algo.pickWorkDq(num)
    algo.client_start(log= log)
    
@algo_app.command()
def plc(x: Annotated[Optional[int], typer.Argument()] = None,
        y: Annotated[Optional[int], typer.Argument()] = None,
        level: Annotated[Optional[int], typer.Argument()] = None):
    
    """
    place goods from (0, 0, -1) to (x, y, level)
    
    (0, 0, -1) mean top of (0, 0)
    """
    
    num = [x, y, level]
    
    algo = AlgoClient()
    algo.initWorkDq()
    
    log = algo.placeWorkDq(num)
    algo.client_start(log= log)
    
@algo_app.command()
def sort(step: Annotated[Optional[int], typer.Argument()] = 1):
    
    print(f"sort {step} time")
    
# def main(
#     part: str,
#     commend: Annotated[Optional[str],typer.Argument(help="pov: move position way\n"
#                                          +"mov: move negative way\n"
#                                          +"rol: rotate direction\n"
#                                          +"pik: pick load\n"
#                                          +"plc: place load")] = None,
#     num: Annotated[Optional[str],typer.Argument(help="pov and mov -> [block num]\n"
#                                      +"rol -> (x to y/ y to x) [0/1]\n"
#                                      +"pik and plc -> [pick or place level] warning! ground level is 1\n")] = None,
#     # formal: Annotated[
#     #     bool,
#     #     typer.Option(
#     #         help="Say hi formally.", rich_help_panel="Customization and Utils"
#     #     ),
#     # ] = False,
#     # debug: Annotated[
#     #     bool,
#     #     typer.Option(
#     #         help="Enable debugging.", rich_help_panel="Customization and Utils"
#     #     ),
#     # ] = False,
# ):
#     # """
#     # Say hi to NAME, optionally with a --lastname.

#     # If --formal is used, say hi very formally.
#     # """
#     # if formal:
#     #     print(f"Good day Ms. {name} {lastname}.")
#     # else:
#     #     print(f"Hello {name} {lastname}")
    
    
#     if part == "raw":
#         local_client = LocalClient()
#         local_client.is_typer = True
#         local_client.client_start(commend= commend, num= num)
#     elif part == "alg":
#         print("alg!")
        


if __name__ == "__main__":
    app()