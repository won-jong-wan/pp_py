#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 15:46:18 2024

@author: won
"""

from collections import deque as dq
import networkx as nx
import csv

class WorkDq:
    def calcMonoTime(self, target_s):
        t_acc = self.max_v/self.max_a
        t_static = self.target_s/self.max_v - t_acc

        t_total = t_acc*2 + t_static
        return t_total
    
    ######## BFS
    def create2dGrid(self,rows, cols):
        G = nx.grid_2d_graph(rows, cols)
        return G

    def customBfs(self, G, start, targetCondition):
        queue = dq([(start, 0)])  # (node, distance)
        visited = set([start])

        while queue:
            current, dist = queue.popleft()
            
            if targetCondition(current, dist) and current not in self.black_list:
                self.black_list.append(current)
                return current, dist

            for neighbor in G.neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        
        return None, -1  # 조건을 만족하는 노드를 찾지 못한 경우

    def findEmptyGrid(self, nx_grid, target_pose):
        # important part # fix needed
        targetCondition = lambda node, dist: len(self.grid[node[0]][node[1]]) < self.grid_level and node != target_pose
        
        result_node, distance =self.customBfs(self.nx_grid, target_pose, targetCondition)
        
        if result_node:
            print(f"    fine near node: {result_node}") 
            print(f"    distance from target_pose: {distance}")
            return result_node, distance
        else:
            print("can't find near node")
            
        return None, -1
    
    ######## check
    def checkPick(self, suspect):
        # 물품을 집고 있을 때
        if self.robot_load[0] != "none":
            self.work_dq.append(suspect) # stack처럼 사용
            
            ### 가장 가까운 빈 공간 찾음 ex: (1, 0)
            near_pose, distance = self.findEmptyGrid(self.nx_grid, suspect[1])
            ### 해당 선정 방법이 성능에 영향을 많이 줄 것임
            
            # 가장 가까운 빈 공간으로 이동
            move_order = ("move", self.robot_pose, near_pose)
            # 내려놓기
            place_order = ("place", near_pose, -1) # 기존 층 위에 쌓는 -1
            
            # 역순으로 stack에 쌓기
            sub_dq = dq()
            sub_dq.extendleft([move_order, place_order])
            
            self.work_dq.extend(sub_dq)
            # work_dq.append(place_order)
            # work_dq.append(move_order)
            
            return False
        
        # 해당 위치 위에 었지 않을 때
        elif suspect[1] is not self.robot_pose:
            self.work_dq.append(suspect)
            
            move_order = ("move", self.robot_pose, suspect[1]) # move 명령 구조 ("move", 현재 로봇 위치, 목표 위치)
            self.work_dq.append(move_order)
            return False
        
        # pick 위치를 타 기물이 막고 있을 때
        elif len(self.grid[suspect[1][0]][suspect[1][1]]) > suspect[2] and suspect[2] != -1:
            self.work_dq.append(suspect)
            
            pick_order = ("pick", suspect[1], -1)
            self.work_dq.append(pick_order)
            return False
        
        # scatter_dq와 연계 필요
        else:
            return True

    # place시 다운 파트에 물품이 존재함을 인지하여 설계    
    def checkPlace(self,suspect):
        # place 위치를 타 기물이 막고 있을 때 
        ## 들고 있던 화물 내려놓기
        ## 막고 있는 화물 치우기
        ## 내려놓은 화물 집기
        stack_high = len(self.grid[suspect[1][0]][suspect[1][1]])
        target_level = suspect[2]
        on = stack_high >= target_level and target_level != -1 
        # load = robot_load[0] != "none"
        
        # if on and len(scatter_dq) == 0:
        #     work_dq.append(suspect)
            
        #     near_pose, distance = findEmptyGrid(nx_grid, suspect[1])
        #     place_order = ("place", near_pose, -1)
        #     work_dq.append(place_order)
            
        #     scatter_place_order = ("place", suspect[1], -1)
        #     scatter_pick_order = ("pick", near_pose, -1)
        #     scatter_dq.appendleft(scatter_pick_order)
        #     scatter_dq.appendleft(scatter_place_order)

        #     return False
        # if on:
        #     tmp = len(grid[suspect[1][0]][suspect[1][1]]) - suspect[2]
        #     sub_dq = dq()
        #     for _ in range(tmp):
        #         near_pose, distance = findEmptyGrid(nx_grid, suspect[1])
        #         # 가장 가까운 빈 공간으로 이동
        #         move_order = ("move", robot_pose, near_pose)
        #         # 내려놓기
        #         place_order = ("place", near_pose, -1) # 기존 층 위에 쌓는 -1
                
        #         sub_dq.extendleft([])
        
        if on:
            self.work_dq.append(suspect)
            
            sub_dq = dq()
            near0, dis0 = self.findEmptyGrid(self.nx_grid, suspect[1])
            
            place0 = ("place", near0, -1)
            
            sub_dq.appendleft(place0)
            
            for i in range(stack_high - target_level + 1):
                pick = ("pick", suspect[1], -1)
                near, dis = self.findEmptyGrid(self.nx_grid, suspect[1])
                place = ("place", near, -1)
                
                sub_dq.extendleft([pick, place])
            
            pick1 = ("pick", near0, -1)
            
            sub_dq.extendleft([pick1])
            
            self.work_dq.extend(sub_dq)
        
        # 해당 위치 위에 있지 않을 때
        elif suspect[1] is not self.robot_pose:        
            self.work_dq.append(suspect) # stack처럼 사용
            
            move_order = ("move", self.robot_pose, suspect[1])
            self.work_dq.append(move_order)
            return False
        
        # elif on and load:
        #     work_dq.append(suspect)
            
        #     near_pose, distance = findEmptyGrid(nx_grid, suspect[1])
        #     place_order = ("place", near_pose, -1)
        #     work_dq.append(place_order)
        #     return False
        
        # elif on:
        #     work_dq.append(suspect)
            
        #     pick_order = ("pick", suspect[1], -1)
        #     work_dq.append(pick_order)
        #     return False
        else:
            return True
        
    ######## comu
    def comuPick(self,suspect):
        ### 집는 함수 구현
        self.robot_load = self.grid[suspect[1][0]][suspect[1][1]].pop()
        
        print("pick: "+str(self.robot_load))
        level = len(self.grid[suspect[1][0]][suspect[1][1]])+1
        
        str_slice = f"pik {level}"
        print("        "+str_slice)
        
        self.str = self.str+str_slice+self.pas_icon
        
        return
        
    def comuPlace(self):
        ### 내려놓는 함수 구현
        print("place: "+str(self.robot_load))
        level = len(self.grid[self.suspect[1][0]][self.suspect[1][1]])+1

        str_slice = f"plc {level}"
        print("        "+str_slice)
        
        self.str = self.str+str_slice+self.pas_icon
        
        self.grid[self.suspect[1][0]][self.suspect[1][1]].append(self.robot_load)
        self.robot_load = ("none", 0, 0)
        # place 끝난 이후 scatter_dq를 이용한 정리 필요
        return

    def comuMove(self, suspect):
        ### 움직이는 함수 구현
        print("move from "+str(suspect[1])+" to "+str(suspect[2]))
        
        self.move(suspect[1], suspect[2])
        
        self.robot_pose = suspect[2]
        return
    
    #### move # fix needed
    def move(self,robot_pose, target_pose):
        diffx = target_pose[0] - robot_pose[0]
        diffy = target_pose[1] - robot_pose[1]
        
        diff = (diffx, diffy)
        
        print(f"    ori: {self.robot_orientation}")
        
        if self.robot_orientation == "row":
            if diff[1] > 0: 
                print(f"        pov {abs(diff[1])}")
                self.str = self.str+f"pov {abs(diff[1])}"+self.pas_icon
            elif diff[1] < 0: 
                print(f"        mov {abs(diff[1])}")
                self.str = self.str+f"mov {abs(diff[1])}"+self.pas_icon
            if diff[0] > 0:
                # row to col: rol 1
                print("        rol 1")
                self.str = self.str+"rol 1"+self.pas_icon
                
                self.robot_orientation = "col"
                print(f"        pov {abs(diff[0])}")
                self.str = self.str+f"pov {abs(diff[0])}"+self.pas_icon
            elif diff[0] < 0:
                print("        rol 1")
                self.str = self.str+"rol 1"+self.pas_icon
                
                self.robot_orientation = "col"
                print(f"        mov {abs(diff[0])}")
                self.str = self.str+f"mov {abs(diff[0])}"+self.pas_icon
        elif self.robot_orientation == "col":
            if diff[0] > 0:
                print(f"        pov {abs(diff[0])}")
                self.str = self.str+f"pov {abs(diff[0])}"+self.pas_icon
            elif diff[0] < 0:
                print(f"        mov {abs(diff[0])}")
                self.str = self.str+f"mov {abs(diff[0])}"+self.pas_icon
            if diff[1] > 0: 
                # col to row: rol 0
                print("        rol 0")
                self.str = self.str+"rol 0"+self.pas_icon
                
                self.robot_orientation = "row"
                print(f"        pov {abs(diff[1])}")
                self.str = self.str+f"pov {abs(diff[1])}"+self.pas_icon
            elif diff[1] < 0: 
                print("        rol 0")
                self.str = self.str+"rol 0"+self.pas_icon
                
                self.robot_orientation = "row"
                print(f"        mov {abs(diff[1])}")
                self.str = self.str+f"mov {abs(diff[1])}"+self.pas_icon
        print("")
        
        return
    
    ######## Run
    def run(self):
        
        while len(self.work_dq) != 0:
            # print(work_dq)
            self.suspect = self.work_dq.pop()
            if self.suspect[0] == "pick":
                sign = self.checkPick(self.suspect)
                if sign:
                    self.comuPick(self.suspect)
            elif self.suspect[0] == "place":
                sign = self.checkPlace(self.suspect)
                if sign:
                    self.comuPlace()
            elif self.suspect[0] == "move":
                self.comuMove(self.suspect)
            
            
        self.str = self.str[:len(self.str)-1]+"!>"
        return self.str

    def vals(self, cols, rows, start_pose, start_orientation):
        self.max_v = 0.3 # 0.3m/s
        self.max_a = 0.4 # 1m/s^2
        self.rotate_delay = 2 # 2초
        
        self.cols = cols
        self.rows = rows
        self.grid_level = 3
        
        self.pick_up_pose = (0, 0)
        self.robot_pose = start_pose # 몇 번째 열인지, 몇 번째 행인지
        self.robot_orientation = start_orientation # row or col
        self.robot_load = ("none", 0, 0) # (이름, id, priority)
        # 이름이 none이면 비어있는 것
        
        self.grid = [[[]for col in range(self.cols)]for row in range(self.rows)]
        self.black_list = [(0, 0)] # pick up place
        self.nx_grid = self.create2dGrid(rows, cols)
        
        # with open('grid.csv', 'w', newline='', encoding='utf-8') as file:
        #     writer = csv.writer(file)
        #     writer.writerows(self.grid)
        
        self.work_dq = dq()
        self.scatter_dq = dq()
        
        self.str = "<@"
        self.pas_icon = "#"
        
    def __init__(self, cols=2, rows=3, start_pose=(0, 0), start_orientation="col"):
        self.vals(cols, rows, start_pose, start_orientation)
