#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 16:38:11 2024

@author: won
"""

from WorkDq import WorkDq
from LocalClient import LocalClient
from GridEditer import GridEditer
from rich import print

class AlgoClient(LocalClient):
    def initWorkDq(self):
        self.grid_edit = GridEditer()
        
        self.work_dq = WorkDq(self.grid_edit)
        
        # with open('grid.csv', 'r', encoding='utf-8') as file:
        #     csv_reader = csv.reader(file)
        #     for row in csv_reader:
        #         self.work_dq.grid.append(row)
            
        # self.work_dq.grid[0][0].append(("001", 0))
        # self.work_dq.grid[0][0].append(("001", 0))
        # # self.work_dq.grid[0][1].append(("011", 1))
        # # self.work_dq.grid[0][1].append(("012", 1.5))
        # self.work_dq.grid[1][0].append(("101", 2))
        # self.work_dq.grid[1][0].append(("102", 3))
        # self.work_dq.grid[2][0].append(("201", 4))
        # self.work_dq.grid[2][0].append(("202", 5))
        # self.work_dq.grid[1][1].append(("111", 6))
        # self.work_dq.grid[1][1].append(("112", 7))
        # self.work_dq.grid[2][1].append(("211", 8))
        # self.work_dq.grid[2][1].append(("212", 9))
        
        # self.work_dq.grid[2][1].append(("test3", 2, 1))
        # self.work_dq.grid[2][1].append(("test3", 2, 1))
        # grid[2][1].append(("test3", 2, 1))
    
    def pickWorkDq(self, input_num = None, name= ""):
        grEd = self.work_dq.gridEditer
        
        grid = grEd.grid
        
        num = input_num
        
        if name != "":
            len_x = len(grid)
            len_y = len(grid[0])
            
            for x in range(len_x):
                for y in range(len_y):
                    len_level = len(grid[x][y])
                    if len_level <= 0:
                        continue
                    for level in range(len_level):
                        is_target = grid[x][y][level][0] == name
                        if is_target:
                            num = [x, y, level+1]
            num = tuple(num)
                    
        
        pick_order = ("pick", (num[0], num[1]), num[2]) # (2, 2)의 1층을 집음
        place_order = ("place", self.work_dq.pick_up_pose, -1) # level이 -1인 경우 기존 층 위에 쌓음

        self.work_dq.work_dq.appendleft(pick_order) # que처럼 사용
        self.work_dq.work_dq.appendleft(place_order)
        
        print("\n\nlog: ")
        
        message = self.work_dq.run()
        
        print(f"\n\nsend message: [green]{message}[/green]\n")
        
        return message
    
    def placeWorkDq(self, input_num, is_auto):
        pick_order = ("pick", self.work_dq.pick_up_pose, -1) # (2, 2)의 1층을 집음
        place_order = ("place", (input_num[0], input_num[1]), input_num[2]) # level이 -1인 경우 기존 층 위에 쌓음
        
        if is_auto:
            grEd = self.work_dq.gridEditer
            auto_target = self.work_dq.find_accord_grid(tuple(grEd.config_dic["pick_up_pose"]), "low")
            
            place_order = ("place", auto_target[0], -1)
        
        self.work_dq.work_dq.appendleft(pick_order) # que처럼 사용
        self.work_dq.work_dq.appendleft(place_order)
        
        print("\n\nlog: ")
        
        message = self.work_dq.run()
        
        print(f"\n\nsend message: [green]{message}[/green]\n")
    
        return message
    
    def sortWorkDq(self, input_num, loop = False):
        is_need_sort = self.work_dq.sort_ord_generator()
        message = ""
        tmp = 0
        
        print("\n\nlog: ")
        
        message = message + self.work_dq.run()
        
        print(f"\n\nsend message: [green]{message}[/green]\n")
        
        while loop and is_need_sort and tmp < input_num:
            print("\n\nlog: ")
            
            message = self.work_dq.run()
            
            print(f"\n\nsend message: [green]{message}[/green]\n")
            
            tmp = tmp +1
            is_need_sort = self.work_dq.sort_ord_generator()
            
        return message
    
    # def resetWorkDq(self):
    #     self.work_dq.black_list = [self.work_dq.pick_up_pose]
    #     self.work_dq.str = "" #"<@"
        
    #     # with open('grid.csv', 'wt', newline='', encoding='utf-8') as file:
    #     #     writer = csv.writer(file)
    #     #     writer.writerows(self.work_dq.grid)
    
    # def client_start(self, commend, num, host= "localhost", port= 8888):
    #     self.initWorkDq()
        
    #     if commend == "pic":
    #         log = self.pickWorkDq(num)
    #     elif commend == "plc":
    #         log = self.placeWorkDq(num)
        
    #     # self.resetWorkDq()
    #     super().client_start(host, port, log= log)
    
    def __init__(self):
        super().__init__()
        self.is_long = True


