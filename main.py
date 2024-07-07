# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 01:10:10 2024

@author: jonwo
"""

from collections import deque as dq
import numpy as np
import networkx as nx

def calcMonoTime(target_s):
    t_acc = max_v/max_a
    t_static = target_s/max_v - t_acc

    t_total = t_acc*2 + t_static
    return t_total

def findEmptyGrid(target_pose):
    
    # bfs 
    return

def checkPick(suspect):
    # 물품을 집고 있을 때
    if robot_load[0] != "none":
        work_dq.append(suspect) # stack처럼 사용
        
        ### 가장 가까운 빈 공간 찾음 ex: (1, 0)
        ### 해당 선정 방법이 성능에 영향을 많이 줄 것임
        near_place = (1, 0)
        
        # 가장 가까운 빈 공간으로 이동
        move_order = ("move", robot_pose, near_place)
        # 내려놓기
        place_order = ("place", near_place, -1) # 기존 층 위에 쌓는 -1
        
        # 역순으로 stack에 쌓기
        work_dq.append(place_order)
        work_dq.append(move_order)
        
        return False
    
    # 해당 위치 위에 었지 않을 때
    elif suspect[1] is not robot_pose:
        work_dq.append(suspect)
        
        move_order = ("move", robot_pose, suspect[1]) # move 명령 구조 ("move", 현재 로봇 위치, 목표 위치)
        work_dq.append(move_order)
        return False
    
    # pick 위치를 타 기물이 막고 있을 때
    elif len(grid[suspect[1][0]][suspect[1][1]]) > suspect[2] and suspect[2] != -1:
        work_dq.append(suspect)
        
        pick_order = ("pick", suspect[1], -1)
        work_dq.append(pick_order)
        return False
    
    # scatter_dq와 연계 필요
    else:
        return True

#place시 다운 파트에 물품이 존재함을 인지하여 설계    
def checkPlace(suspect):
    # place 위치를 타 기물이 막고 있을 때 
    ## 들고 있던 화물 내려놓기
    ## 막고 있는 화물 치우기
    ## 내려놓은 화물 집기

    
    # 해당 위치 위에 있지 않을 때
    if suspect[1] is not robot_pose:        
        work_dq.append(suspect) # stack처럼 사용
        
        move_order = ("move", robot_pose, suspect[1])
        work_dq.append(move_order)
        return False
    else:
        return True

def comuPick(suspect):
    ### 집는 함수 구현
    global robot_load, grid
    
    robot_load = grid[suspect[1][0]][suspect[1][1]].pop()
    
    print("pick: "+str(robot_load))
    return
    
def comuPlace():
    ### 내려놓는 함수 구현
    global robot_load, grid
    print("place: "+str(robot_load))
    
    grid[suspect[1][0]][suspect[1][1]].append(robot_load)
    robot_load = ("none", 0, 0)
    # place 끝난 이후 scatter_dq를 이용한 정리 필요
    return

def comuMove(suspect):
    ### 움직이는 함수 구현
    print("move from "+str(suspect[1])+" to "+str(suspect[2]))
    
    global robot_pose
    robot_pose = suspect[2]
    return

max_v = 0.3 # 0.3m/s
max_a = 0.4 # 1m/s^2

rotate_delay = 2 # 2초

grid_column_num = 3
grid_row_num = 2
grid_level = 3

robot_pose = (0, 0) # 몇 번째 열인지, 몇 번째 행인지
robot_orientation = "row" # row or col
robot_load = ("none", 0, 0) # (이름, id, priority)
# 이름이 none이면 비어있는 것

grid = [[[]for row in range(grid_row_num)]for col in range(grid_column_num)]

work_dq = dq()
scatter_dq = dq()

grid[1][1].append(("test", 0, 1))

pick_order = ("pick", (1, 1), 1) # (2, 2)의 1층을 집음
place_order = ("place", (2, 1), -1) # level이 -1인 경우 기존 층 위에 쌓음

work_dq.appendleft(pick_order) # que처럼 사용
work_dq.appendleft(place_order)

while len(work_dq) != 0:
    suspect = work_dq.pop()
    if suspect[0] == "pick":
        sign = checkPick(suspect)
        if sign:
            comuPick(suspect)
    elif suspect[0] == "place":
        sign = checkPlace(suspect)
        if sign:
            comuPlace()
    elif suspect[0] == "move":
        comuMove(suspect)

print(work_dq)


