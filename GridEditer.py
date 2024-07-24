#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 16:12:42 2024

@author: won
"""

from WorkDq import WorkDq
import csv
import json
from collections import OrderedDict
import os

class GridEditer:
    def __init__(self, csv_path="./csv", config_path="./config" ,size=(3, 2, 3), base=(0, 0)):
        self.grid = []
        self.base = base
        self.size = size
        
        self.goods = OrderedDict()
        self.config = OrderedDict()
        
        self.goods_file = os.path.join(csv_path, "item.json")
        self.config_file = os.path.join(config_path, "config.json")
        with open(self.config_file) as file:
            self.config = json.load(file)
            self.id_max = self.config_data["id_max"]
        
        self.csv_file = os.path.join(csv_path, "grid.csv")
        if not os.path.isfile(self.csv_file):
            self.createGrid(size[0], size[1])

        with open(self.csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                self.grid.append(row)
        return
    
    def setBase(self, base):
        self.base = base
        return
    
    def getGrid(self):
        return self.grid
    
    def saveGrid(self):
        with open(self.csv_file, 'wt', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(self.grid)
        return
    
    def createGrid(self, rows, cols):
        self.grid = [[[]for col in range(self.cols)]for row in range(self.rows)]
        
        self.saveGrid()
        return
    
    def insertToBase(self, name, priority):
        id = self.id_max
        self.id_max = self.id_max+1
        
        goods = (name, id, priority)
        if len(self.grid[self.base[0]][self.base[1]]) < self.size[2]:
           self.grid[self.base[0]][self.base[1]].append(goods)
           
           self.saveGrid()
        else: 
            print("base was full")
        return
    
    def switchGoods(self, target1, target2):
        t1_data = self.grid[target1[0]][target1[1]][target1[2]+1]
        t2_data = self.grid[target2[0]][target2[1]][target2[2]+1]

        self.grid[target1[0]][target1[1]][target1[2]+1] = t2_data
        self.grid[target2[0]][target2[1]][target2[2]+1] = t1_data
        
        self.saveGrid()
        
        return
    
    def insertGoods(self, name, priority, pose):
        id = self.id_max
        
        return
        
    def saveConfig(self):
        self.config_data["id_max"] = self.id_max
        with open(self.config_file, 'wt', encoding='utf-8') as file:
            json.dump(self.config_data, file, ensure_ascii=False, indent="\t")
            
        return
    
        