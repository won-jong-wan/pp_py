#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 15:46:18 2024

@author: won
"""
from GridEditer import GridEditer
from rich import print

from collections import deque as dq
import networkx as nx

class WorkDq:
    def calcMonoTime(self, target_s):
        t_acc = self.max_v/self.max_a
        t_static = self.target_s/self.max_v - t_acc

        t_total = t_acc*2 + t_static
        return t_total
    
    def findLevel(self, target_pose):
        min_level = 3
        
        max_level = 1
        
        for x in range(self.rows):
            for y in range(self.cols):
                node = tuple([x, y])
                
                is_free = node not in self.black_list and node != target_pose
                
                if min_level > len(self.grid[x][y]) and is_free:
                    min_level = len(self.grid[x][y])
                
                if max_level < len(self.grid[x][y]) and is_free:
                    max_level = len(self.grid[x][y])
        
        return min_level, max_level
    
    ######## BFS
    def create2dGrid(self,rows, cols):
        G = nx.grid_2d_graph(rows, cols)
        return G

    def customBfs(self, G, start, targetCondition):
        queue = dq([(start, 0)])  # (node, distance)
        visited = set([start])

        while queue:
            current, dist = queue.popleft()
            
            if targetCondition(current, dist, start):
                return current, dist

            for neighbor in G.neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        
        return None, -1  # 조건을 만족하는 노드를 찾지 못한 경우

    def findEmptyGrid(self, nx_grid, target_pose, is_temp= False):
        # important part # fix needed
        def targetCondition(node, dist, target_pose):
            
            min_level, max_level = self.findLevel(target_pose)
            
            node_level = len(self.grid[node[0]][node[1]])        
            
            is_over_max_flag = node_level >= self.grid_level
            is_target_flag = node == target_pose
            is_blackL_flag = node in self.black_list
            
            if is_temp:
                is_min_level = node_level != min_level
            else:
                is_min_level = node_level == min_level
            
            is_ok = not is_over_max_flag and not is_target_flag and not is_blackL_flag and is_min_level
            
            if is_ok and is_temp:
                self.black_list.append(node)
            
            return is_ok
        
        result_node, distance =self.customBfs(self.nx_grid, target_pose, targetCondition)
        
        if result_node:
            print(f"    fine near node: {result_node}") 
            print(f"    distance from target_pose: {distance}\n")
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
            near0, dis0 = self.findEmptyGrid(self.nx_grid, suspect[1], is_temp= True)
            
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
    
    ######## sort
    def find_accord_grid(self, robot_pose, accord_condition, blocking = False):
        def targetCondition(node, dist, target_pose):
            
            min_level, max_level = self.findLevel(target_pose)
            
            node_level = len(self.grid[node[0]][node[1]])        
            
            is_over_max_flag = node_level >= self.grid_level
            is_target_flag = node == target_pose
            is_blackL_flag = node in self.black_list
            
            if accord_condition == "high":
                is_accord_level = (node_level == max_level)
                is_over_max_flag = False
            elif accord_condition == "low":
                is_accord_level = (node_level == min_level)
            
            is_ok = not is_over_max_flag and not is_target_flag and not is_blackL_flag and is_accord_level
            
            # print(f"ok: {is_ok} target: {node} node_level: {node_level} max_level: {max_level}")
            
            if is_ok and blocking:
                self.black_list.append(node)
            
            return is_ok
        
        result_node, distance =self.customBfs(self.nx_grid, tuple(robot_pose), targetCondition)
        
        if result_node:
            print(f"    fine accord node: {result_node}") 
            print(f"    distance from robot_pose: {distance}\n")
            return result_node, distance
        else:
            print("can't find near node")
            
        return None, -1
    
    def sort_ord_generator(self):
        min_level, max_level = self.findLevel(self.pick_up_pose)
        
        print(f"min: {min_level}, max: {max_level}")
        
        if max_level - min_level <= 1:
            print("no need to sort")
            return False
        
        # print(self.robot_pose)
        high_node, distance = self.find_accord_grid(self.robot_pose, "high")
        low_node, distance = self.find_accord_grid(high_node, "low")
        
        sub_dq = dq()
        
        pick = ("pick", high_node, -1)
        place = ("place", low_node, -1)
        
        sub_dq.extendleft([place, pick])
        
        self.work_dq.extendleft(sub_dq)
        
        return True
    
    ######## Run
    def run(self):
        
        if len(self.str) !=0:
            self.str = self.str+self.pas_icon
        
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
            
            self.semi_save()
            
            
        self.str = self.str[:len(self.str)-1] # +"!>"
        return self.str
    
    def reset(self):
        self.black_list = [self.work_dq.pick_up_pose]
        self.work_dq.str = "" #"<@"
        
    def semi_save(self):
        self.gridEditer.config_dic["robot_orientation"] = self.robot_orientation
        self.gridEditer.config_dic["robot_load"] = self.robot_load
        self.gridEditer.config_dic["robot_pose"] = self.robot_pose
        
        self.gridEditer.write_files()
    
    # def vals(self, cols, rows, start_pose, start_orientation):
    def vals(self):
        
        self.gridEditer.read_files()
        
        config_dic = self.gridEditer.config_dic
        grid = self.gridEditer.grid
        
        # grid information
        self.cols = config_dic["cols"] # cols
        self.rows = config_dic["rows"] # rows
        self.grid_level = config_dic["grid_level"] # 3
        self.pick_up_pose = tuple(config_dic["pick_up_pose"]) # (0, 0)
        
        # robot information
        self.max_v = config_dic["max_v"] # 0.3 # 0.3m/s
        self.max_a = config_dic["max_a"] # 0.4 # 1m/s^2
        self.rotate_delay = config_dic["rotate_delay"] # 2 # 2초
        
        self.robot_pose = tuple(config_dic["robot_pose"])  # (0, 0)
        self.robot_orientation = config_dic["robot_orientation"] # "col"
        self.robot_load = tuple(config_dic["robot_load"]) # ("none", 0, -1)
        
        # define vals
        self.grid = grid # [[[]for col in range(self.cols)]for row in range(self.rows)]
        self.black_list = [self.pick_up_pose] # pick up place
        self.nx_grid = self.create2dGrid(self.rows, self.cols)
        
        self.work_dq = dq()
        self.scatter_dq = dq()
        
        # message option
        self.str ="" # "<@"
        self.pas_icon = config_dic["pas_icon"] # "#"
        
    # def __init__(self, cols=2, rows=3, start_pose=(0, 0), start_orientation="col"):
    #     self.vals(cols, rows, start_pose, start_orientation)
    def __init__(self, gridEditer = GridEditer()):
        self.gridEditer = gridEditer
        self.vals()
