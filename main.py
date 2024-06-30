# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 01:10:10 2024

@author: jonwo
"""

from collections import deque as dq
import numpy as np

grid_column_num = 3
grid_row_num = 2
grid_level = 3

grid = np.zeros([grid_column_num, grid_row_num, grid_level])

robot_pose = (0, 0) # 몇 번째 열인지, 몇 번째 행인지
robot_orientation = (1, 1) # 음의 열 쪽인지:-1 양의 열 쪽인지:1, 음의 행 쪽인지:-1 양의 행 쪽인지:1
robot_load = ("none", 0, 0) # (이름, id, priority)
# 이름이 none이면 비어있는 것

work_dq = dq()
scatter_dq = dq()

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
    
    # pick 혹은 place 위치를 타 기물이 막고 있을 때 
    
    # scatter_dq와 연계 필요
    else:
        return True

def comuPick():
    ### 집는 함수 구현
    print("pick!")
    
    #robot_load 바뀌어야함
    #suspect 받아와야 할 수도
    return

#place시 다운 파트에 물품이 존재함을 인지하여 설계    
def checkPlace(suspect):
    # pick 혹은 place 위치를 타 기물이 막고 있을 때 

    
    # 해당 위치 위에 었지 않을 때
    if suspect[1] is not robot_pose:        
        work_dq.append(suspect) # stack처럼 사용
        
        move_order = ("move", robot_pose, suspect[1])
        work_dq.append(move_order)
        return False
    else:
        return True
    
def comuPlace():
    ### 내려놓는 함수 구현
    print("place!")
    
    global robot_load
    robot_load = ("none", 0, 0)
    # place 끝난 이후 scatter_dq를 이용한 정리 필요
    return

def comuMove(suspect):
    ### 움직이는 함수 구현
    print("move from "+str(suspect[1])+" to "+str(suspect[2]))
    
    global robot_pose
    robot_pose = suspect[2]
    return

pick_order = ("pick", (2, 2), 1) # (2, 2)의 1층으로 운송 
place_order = ("place", (1, 1), -1) # level이 -1인 경우 기존 층 위에 쌓음

work_dq.appendleft(pick_order) # que처럼 사용
work_dq.appendleft(place_order)

while len(work_dq) != 0:
    suspect = work_dq.pop()
    if suspect[0] == "pick":
        sign = checkPick(suspect)
        if sign:
            comuPick()
    elif suspect[0] == "place":
        sign = checkPlace(suspect)
        if sign:
            comuPlace()
    elif suspect[0] == "move":
        comuMove(suspect)

print(work_dq)


