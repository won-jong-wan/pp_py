#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 16:12:42 2024

@author: won
"""
import csv
import json
import os

class GridEditer:
    def write_json(self, config_dic):
        self.config_dic["id_max"] = self.id_max
        
        with open(self.config_path, "w") as json_file:
            json.dump(config_dic, json_file, indent=4)
        return
    
    def write_grid(self, grid):
        x_len = len(grid)
        y_len = len(grid[0])
        
        goods_list = []
        
        for x in range(x_len):
            for y in range(y_len):
                for level in range(len(grid[x][y])):
                    goods = list(grid[x][y][level])
                    goods.append(x)
                    goods.append(y)
                    goods_list.append(goods)
                
        with open(self.csv_path, "w") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(goods_list)
        return
    
    def read_json(self):
        config_dic = {}
        
        with open(self.config_path, "r") as json_file:
            config_dic = json.load(json_file)
        return config_dic
    
    def read_grid(self, grid_size= (3, 2)):
        grid = [[[]for col in range(grid_size[1])]for row in range(grid_size[0])]
        
        with open(self.csv_path, "r") as csv_file:
            reader = csv.reader(csv_file)
            for line in reader:
                if len(line) == 0:
                    continue
                grid[int(line[2])][int(line[3])].append(line[0:2])
        return grid
    
    def make_default_files(self):
        
        config_dic = {}
        
        # grid information
        config_dic["cols"] = 2
        config_dic["rows"] = 3
        config_dic["grid_level"] = 3
        config_dic["pick_up_pose"] = (0, 0)
        
        # robot information
        config_dic["max_v"] = 0.3 # 0.3m/s
        config_dic["max_a"] = 0.4 # 1m/s^2
        config_dic["rotate_delay"] = 2 # 2초
        
        config_dic["robot_pose"] = (0, 0)
        config_dic["robot_orientation"] = "col"
        config_dic["robot_load"] = ("none", 0, -1)
        
        # message option
        # self.str ="" # "<@"
        config_dic["pas_icon"]  = "#"
        
        grid = [[[]for col in range(2)]for row in range(3)]
        
        # for reset #
        
        grid[0][1].append(("A", 0))
        grid[0][1].append(("B", 1))
        grid[1][0].append(("D", 2))
        grid[1][0].append(("C", 3))
        grid[1][1].append(("H", 4))
        grid[1][1].append(("I", 5))
        grid[2][0].append(("J", 6))
        grid[2][0].append(("G", 7))
        grid[2][1].append(("F", 8))
        grid[2][1].append(("E", 9))
        # grid[0][0].append(("001", 0))
        # # self.work_dq.grid[0][1].append(("011", 1))
        # # self.work_dq.grid[0][1].append(("012", 1.5))
        # grid[1][0].append(("101", 1))
        # grid[1][0].append(("102", 2))
        # grid[2][0].append(("201", 3))
        # grid[2][0].append(("202", 4))
        # grid[1][1].append(("111", 5))
        # grid[1][1].append(("112", 6))
        # grid[2][1].append(("211", 7))
        # grid[2][1].append(("212", 8))
        # grid[2][1].append(("213", 9))
        # grid[2][0].append(("203", 10))
        
        # for reset end #
        
        grid_len = 0
        
        x_len = len(grid)
        y_len = len(grid[0])
        
        for x in range(x_len):
            for y in range(y_len):
                for level in range(len(grid[x][y])):
                    grid_len = grid_len + 1
        
        config_dic["id_max"] = grid_len - 1
        
        self.write_json(config_dic)
        self.write_grid(grid)
        
    def read_files(self):
        self.grid = self.read_grid()
        self.config_dic = self.read_json()
        self.id_max = self.config_dic["id_max"]
        
    def write_files(self):
        self.write_grid(self.grid)
        self.write_json(self.config_dic)
        
    def add_goods(self, name, pose= (0, 0, -1)):
        target_grid= self.grid[pose[0]][pose[1]]
        pose_level = pose[2]
        
        if pose[2] == -1:
            pose_list = list(pose)
            pose_list[2] = len(target_grid)+1
            self.add_goods(name, pose=tuple(pose_list))
        else:
            if name in (level[0] for x in self.grid for y in x for level in y):
                name_ = name+"("+str(self.id_max+1)+")"
            else:
                name_ = name
            
            if pose_level <= len(target_grid):
               target_grid[pose_level-1] = (name_, self.id_max+1)
            elif pose_level > len(target_grid):
                target_grid.append((name_, self.id_max+1))
            self.id_max = self.id_max + 1
    
    def del_goods_as_pose(self, pose = (0, 0, -1)):
        target_grid= self.grid[pose[0]][pose[1]]
        pose_level = pose[2]
        if pose_level == -1 or pose_level > len(target_grid):
            pose_list = list(pose)
            pose_list[2] = len(target_grid)
            return self.del_goods_as_pose(pose=tuple(pose_list))
        else:
            if pose_level == len(target_grid):
                return target_grid.pop()
            elif pose_level < len(target_grid):
                tmp = target_grid[pose_level-1]
                target_grid.remove(target_grid[pose_level-1])
                
                return tmp
    def del_goods_as_name(self, name):
        grid = self.grid
        
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
        self.del_goods_as_pose(num)
        
    
    def __init__(self, csv_path="./csv", config_path="./config"):
        self.grid = []
        self.config_dic = {}
        
        self.csv_path = os.path.join(csv_path, "grid.csv")
        self.config_path = os.path.join(config_path, "config.json")
        self.id_max = 0
        
        self.read_files()
        # print(self.grid[0])
        
        # print(self.grid[1])
        
    
# if __name__== "__main__":
#     ge = GridEditer()
#     # ge.make_default_files()
    
#     ge.read_files()
    
#     ge.add_goods("test", (0, 0, 2))
#     ge.add_goods("test2", )
    
#     print(ge.del_goods_as_pose((0,0,2)))
    
#     global grid
    
#     grid = ge.grid
    
#     ge.write_files()
    
    
    # def __init__(self, csv_path="./csv", config_path="./config" ,size=(3, 2, 3), base=(0, 0)):
    #     self.grid = []
    #     self.base = base
    #     self.size = size
        
    #     self.goods = OrderedDict()
    #     self.config = OrderedDict()
        
    #     self.goods_file = os.path.join(csv_path, "item.json")
    #     self.config_file = os.path.join(config_path, "config.json")
    #     with open(self.config_file) as file:
    #         self.config = json.load(file)
    #         self.id_max = self.config_data["id_max"]
        
    #     self.csv_file = os.path.join(csv_path, "grid.csv")
    #     if not os.path.isfile(self.csv_file):
    #         self.createGrid(size[0], size[1])

    #     with open(self.csv_file, 'r', encoding='utf-8') as file:
    #         csv_reader = csv.reader(file)
    #         for row in csv_reader:
    #             self.grid.append(row)
    #     return
    
    # def setBase(self, base):
    #     self.base = base
    #     return
    
    # def getGrid(self):
    #     return self.grid
    
    # def saveGrid(self):
    #     with open(self.csv_file, 'wt', newline='', encoding='utf-8') as file:
    #         writer = csv.writer(file)
    #         writer.writerows(self.grid)
    #     return
    
    # def createGrid(self, rows, cols):
    #     self.grid = [[[]for col in range(self.cols)]for row in range(self.rows)]
        
    #     self.saveGrid()
    #     return
    
    # def insertToBase(self, name, priority):
    #     id = self.id_max
    #     self.id_max = self.id_max+1
        
    #     goods = (name, id, priority)
    #     if len(self.grid[self.base[0]][self.base[1]]) < self.size[2]:
    #        self.grid[self.base[0]][self.base[1]].append(goods)
           
    #        self.saveGrid()
    #     else: 
    #         print("base was full")
    #     return
    
    # def switchGoods(self, target1, target2):
    #     t1_data = self.grid[target1[0]][target1[1]][target1[2]+1]
    #     t2_data = self.grid[target2[0]][target2[1]][target2[2]+1]

    #     self.grid[target1[0]][target1[1]][target1[2]+1] = t2_data
    #     self.grid[target2[0]][target2[1]][target2[2]+1] = t1_data
        
    #     self.saveGrid()
        
    #     return
    
    # def insertGoods(self, name, priority, pose):
    #     id = self.id_max
        
    #     return
        
    # def saveConfig(self):
    #     self.config_data["id_max"] = self.id_max
    #     with open(self.config_file, 'wt', encoding='utf-8') as file:
    #         json.dump(self.config_data, file, ensure_ascii=False, indent="\t")
            
    #     return
    
        