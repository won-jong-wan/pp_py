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


def create2dGrid(rows, cols):
    G = nx.grid_2d_graph(rows, cols)
    return G

def customBfs(G, start, targetCondition):
    queue = dq([(start, 0)])  # (node, distance)
    visited = set([start])

    while queue:
        current, dist = queue.popleft()
        
        if targetCondition(current, dist):
            global black_list
            black_list.append(current)
            return current, dist

        for neighbor in G.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    
    return None, -1  # 조건을 만족하는 노드를 찾지 못한 경우

def findEmptyGrid(nx_grid, target_pose):
    
    # most important part
    targetCondition = lambda node, dist: len(grid[node[0]][node[1]]) < grid_level and node != target_pose and node != black_list
    
    result_node, distance =customBfs(nx_grid, target_pose, targetCondition)
    
    if result_node:
        print(f"    fine near node: {result_node}") 
        print(f"        distance from target_pose: {distance}")
        return result_node, distance
    else:
        print("can't find near node")
        
    return None, -1

def checkPick(suspect):
    # 물품을 집고 있을 때
    if robot_load[0] != "none":
        work_dq.append(suspect) # stack처럼 사용
        
        ### 가장 가까운 빈 공간 찾음 ex: (1, 0)
        near_pose, distance = findEmptyGrid(nx_grid, suspect[1])
        ### 해당 선정 방법이 성능에 영향을 많이 줄 것임
        
        # 가장 가까운 빈 공간으로 이동
        move_order = ("move", robot_pose, near_pose)
        # 내려놓기
        place_order = ("place", near_pose, -1) # 기존 층 위에 쌓는 -1
        
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
    on = len(grid[suspect[1][0]][suspect[1][1]]) >= suspect[2] and suspect[2] != -1 
    load = robot_load[0] != "none"
    
    if on and len(scatter_dq) == 0:
        work_dq.append(suspect)
        
        near_pose, distance = findEmptyGrid(nx_grid, suspect[1])
        place_order = ("place", near_pose, -1)
        work_dq.append(place_order)
        
        scatter_place_order = ("place", suspect[1], -1)
        scatter_pick_order = ("pick", near_pose, -1)
        scatter_dq.appendleft(scatter_pick_order)
        scatter_dq.appendleft(scatter_place_order)

        return False
    
    # 해당 위치 위에 있지 않을 때
    elif suspect[1] is not robot_pose:        
        work_dq.append(suspect) # stack처럼 사용
        
        move_order = ("move", robot_pose, suspect[1])
        work_dq.append(move_order)
        return False
    
    elif on and load:
        work_dq.append(suspect)
        
        near_pose, distance = findEmptyGrid(nx_grid, suspect[1])
        place_order = ("place", near_pose, -1)
        work_dq.append(place_order)
        return False
    
    elif on:
        work_dq.append(suspect)
        
        pick_order = ("pick", suspect[1], -1)
        work_dq.append(pick_order)
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
    
    move(suspect[1], suspect[2])
    
    global robot_pose
    robot_pose = suspect[2]
    return

def move(robot_pose, target_pose):
    diffx = target_pose[0] - robot_pose[0]
    diffy = target_pose[1] - robot_pose[1]
    
    diff = (diffx, diffy)
    
    global robot_orientation
    
    print(f"    ori: {robot_orientation}")
    
    if robot_orientation == "row":
        print(f"        move row {diff[1]}")
        robot_orientation = "col"
        print(f"        move col {diff[0]}")
    elif robot_orientation == "col":
        print(f"        move col {diff[0]}")
        robot_orientation = "row"
        print(f"        move row {diff[1]}")
        
    

max_v = 0.3 # 0.3m/s
max_a = 0.4 # 1m/s^2

rotate_delay = 2 # 2초

cols = 2
rows = 3
grid_level = 3

robot_pose = (0, 0) # 몇 번째 열인지, 몇 번째 행인지
robot_orientation = "row" # row or col
robot_load = ("none", 0, 0) # (이름, id, priority)
# 이름이 none이면 비어있는 것

grid = [[[]for col in range(cols)]for row in range(rows)]
black_list = [(0, 0)] # pick up place
nx_grid = create2dGrid(rows, cols)

work_dq = dq()
scatter_dq = dq()

grid[1][1].append(("test", 0, 1))
grid[1][1].append(("test2", 1, 1))
# grid[2][1].append(("test3", 2, 1))

pick_order = ("pick", (1, 1), 1) # (2, 2)의 1층을 집음
place_order = ("place", (2, 1), 1) # level이 -1인 경우 기존 층 위에 쌓음

work_dq.appendleft(pick_order) # que처럼 사용
work_dq.appendleft(place_order)

while len(work_dq) != 0:
    # print(work_dq)
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

while len(scatter_dq) != 0:
    print(scatter_dq)
    suspect = scatter_dq.pop()
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
