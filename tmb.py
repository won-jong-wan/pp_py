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

app = typer.Typer(rich_markup_mode="rich")
algo_app = typer.Typer()
editer_app = typer.Typer()

app.add_typer(algo_app, name="algo", help="Running algorithm")
app.add_typer(editer_app, name="edit", help="Edit all grid")

@app.command()
def core():
    """
    Start server between [bold red]robot and local[/bold red]
    """
    
    core = ServerCore()
    
    core.set_robot_host_port()
    core.set_local_host_port()
    
    core.start_server()

@app.command()
def raw(commend: Annotated[Optional[str],typer.Argument(help="[bold green]pov:[/bold green] move position way\n\n"
                                          +"[bold green]mov:[/bold green] move negative way\n\n"
                                          +"[bold green]rol:[/bold green] rotate direction\n\n"
                                          +"[bold green]pik:[/bold green] pick load\n\n"
                                          +"[bold green]plc:[/bold green] place load")] = None,
    num: Annotated[Optional[str],typer.Argument(help="[bold green]pov and mov =>[/bold green] \[block num] \n\n"
                                      +"[bold green]rol(x to y/ y to x) =>[/bold green] \[0/1] \n\n"
                                      +"[bold green]pik and plc =>[/bold green] \[pick or place level]\n\n[bold red]\[warning! ground level is 1][bold red]")] = None,
    long: Annotated[Optional[str], typer.Option(help="send [bold]long str[/bold]\n\n each commends split by \"#\"")]=None):
    
    """
    Send single commend and num
    
    use --long to send long str 
        
    [italic]ex: python tmb.py raw --long "rol 0#mov 1"[/italic]
    """
    
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
    Pick goods from (x, y, level) to (0, 0, -1)
    
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
    
    """
    Sort goods
    """
    
    print(f"sort {step} time")

if __name__ == "__main__":
    app()