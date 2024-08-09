#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 15:22:00 2024

@author: won
"""
from typing import Optional

import os
import typer
from typing_extensions import Annotated
from rich.console import Console
from rich.table import Table
from rich import print

from LocalClient import LocalClient
from ServerCore import ServerCore
from AlgoClient import AlgoClient
from GridEditer import GridEditer
from Visualizer import Visualizer

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
def pik(x: Annotated[Optional[int], typer.Argument()] = 0,
        y: Annotated[Optional[int], typer.Argument()] = 0,
        level: Annotated[Optional[int], typer.Argument()] = -1,
        comu: Annotated[Optional[bool], typer.Option()] = True,
        name: Annotated[Optional[str], typer.Option()] = ""):
    
    """
    Pick goods from (x, y, level) to (0, 0, -1)
    
    (0, 0, -1) mean top of (0, 0)
    """
    
    num = [x, y, level]
    
    algo = AlgoClient()
    algo.initWorkDq()
    
    log = algo.pickWorkDq(num, name)
    
    if comu == True:
        algo.client_start(log= log)
    view()
    
@algo_app.command()
def plc(x: Annotated[Optional[int], typer.Argument()] = 0,
        y: Annotated[Optional[int], typer.Argument()] = 0,
        level: Annotated[Optional[int], typer.Argument()] = -1,
        comu: Annotated[Optional[bool], typer.Option()] = True,
        auto: Annotated[Optional[bool], typer.Option()] = False):
    
    """
    place goods from (0, 0, -1) to (x, y, level)
    
    (0, 0, -1) mean top of (0, 0)
    """
    algo = AlgoClient()
    algo.initWorkDq()
    
    grEd = algo.work_dq.gridEditer
    pick_up_pose = tuple(grEd.config_dic["pick_up_pose"])
    grid = grEd.grid
    
    if len(grid[pick_up_pose[0]][pick_up_pose[0]]) <=0:
        add()
        
        algo.work_dq.vals()
    
    num = [x, y, level]

    log = algo.placeWorkDq(num, auto)
    
    if comu == True:
        algo.client_start(log= log)
    
    view()

@algo_app.command()
def sort(step: Annotated[Optional[int], typer.Argument()] = 1, 
         comu: Annotated[Optional[bool], typer.Option()] = True,
         loop: Annotated[Optional[bool], typer.Option()] = False):
    
    """
    Sort goods high level to low level
    
    num mean sort 
    """
    
    algo = AlgoClient()
    algo.initWorkDq()
    
    if loop:
        step = 20
    
    log = algo.sortWorkDq(step, loop= loop)
    if comu == True:
        algo.client_start(log= log)
        
    view()
    
@algo_app.command()
def home():
    """

    Back to home

    """
    
    algo = AlgoClient()
    algo.initWorkDq()
    
    log = algo.backToHome()
    algo.client_start(log=log)
    
    view()

def print_grid(gridEditer, target = (0, 0, -1)):
    grid = gridEditer.grid
    target_y = target[1]
    
    robot_pose = tuple(gridEditer.config_dic["robot_pose"])
    
    len_x = len(grid)
    # len_y = len(grid[target_y])
    
    table = Table(title = "y = "+str(target_y))
    
    for x in range(len_x):
        table.add_column("x = "+str(x))
    
    max_level = gridEditer.config_dic["grid_level"]
    col_list = [[] for level in range(max_level)]
    
    if robot_pose[1] == target_y:
        col_list = [[] for level in range(max_level+1)]
        if robot_pose[0] == 0:
            col_list[0].extend(["robot", "", ""])
        elif robot_pose[0] == 1:
            col_list[0].extend(["", "robot", ""])
        elif robot_pose[0] == 2:
            col_list[0].extend(["", "", "robot"])
    
    for x in range(len_x):
        len_level = len(grid[x][target_y])
        
        # level_diff = max_level - len_level
        
        for levelr in range(max_level):
            level = max_level-levelr
            
            levell = levelr
            if robot_pose[1] == target_y:
                levell = levelr+1
            
            #col_list[levelr].append(str(level))
            if level > len_level:
                col_list[levell].append("")
            elif level <= len_level:
                col_list[levell].append(grid[x][target_y][level-1][0])
                # print(grid[x][target_y][level-1][0])
            
    
    for col in range(len(col_list)):
        table.add_row(col_list[col][0], col_list[col][1], col_list[col][2])
    
    table.show_lines = True
    
    console = Console()
    console.print(table)
    
    
    
@editer_app.command()
def add(name: Annotated[Optional[str], typer.Argument()] = "default",
        x: Annotated[Optional[int], typer.Argument()] = 0,
                y: Annotated[Optional[int], typer.Argument()] = 0,
                level: Annotated[Optional[int], typer.Option()] = -1):
    """
    add goods
    """
    gred = GridEditer()
    gred.add_goods(name, (x, y, level))
    gred.write_files()
    
    view()
    
@editer_app.command("del")
def del_(x: Annotated[Optional[int], typer.Argument()] = 0,
                y: Annotated[Optional[int], typer.Argument()] = 0,
                level: Annotated[Optional[int], typer.Option()] = -1,
                name: Annotated[Optional[str], typer.Option()] = None ):
    """
    del goods
    """
    gred = GridEditer()
    
    if name:
        gred.del_goods_as_name(name)
    else:
        gred.del_goods_as_pose((x, y, level))
    gred.write_files()
    
    view()
    
@editer_app.command()
def view():
    """
    view grid
    """
    gred = GridEditer()
    
    print("")
    print_grid(gred, (0, 1, 0))
    print("")
    print_grid(gred)
    
    robot_orientation = gred.config_dic["robot_orientation"]
    print(f"\nrobot_orientation: [bold blue]{robot_orientation}[/bold blue]\n")
    
    gred.write_files()
    
    visualizer = Visualizer(gred)
    visualizer.run()

@editer_app.command()
def config():
    """
    view config
    """
    gred = GridEditer()
    
    print(gred.config_dic)
    gred.write_files()
    
    os.system("gedit ./config/config.json")

@editer_app.command()
def reset():
    """
    reset config and grid
    """
    gred = GridEditer()
    
    gred.make_default_files()
    view()
    
    
if __name__ == "__main__":
    app()