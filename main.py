# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 01:10:10 2024

@author: jonwo
"""

from collections import deque as dq
import networkx as nx
import sys
import threading
import socket
import time
import queue as que

class WorkDq:
    def calcMonoTime(self, target_s):
        t_acc = self.max_v/self.max_a
        t_static = self.target_s/self.max_v - t_acc

        t_total = t_acc*2 + t_static
        return t_total

    def create2dGrid(self,rows, cols):
        G = nx.grid_2d_graph(rows, cols)
        return G

    def customBfs(self, G, start, targetCondition):
        queue = dq([(start, 0)])  # (node, distance)
        visited = set([start])

        while queue:
            current, dist = queue.popleft()
            
            if targetCondition(current, dist):
                self.black_list.append(current)
                return current, dist

            for neighbor in G.neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        
        return None, -1  # 조건을 만족하는 노드를 찾지 못한 경우

    def findEmptyGrid(self, nx_grid, target_pose):
        # most important part
        targetCondition = lambda node, dist: len(self.grid[node[0]][node[1]]) < self.grid_level and node != target_pose and node != self.black_list
        
        result_node, distance =self.customBfs(self.nx_grid, target_pose, targetCondition)
        
        if result_node:
            print(f"    fine near node: {result_node}") 
            print(f"    distance from target_pose: {distance}")
            return result_node, distance
        else:
            print("can't find near node")
            
        return None, -1

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

    #place시 다운 파트에 물품이 존재함을 인지하여 설계    
    def checkPlace(self,suspect):
        # place 위치를 타 기물이 막고 있을 때 
        ## 들고 있던 화물 내려놓기
        ## 막고 있는 화물 치우기
        ## 내려놓은 화물 집기
        on = len(self.grid[suspect[1][0]][suspect[1][1]]) >= suspect[2] and suspect[2] != -1 
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
        
        # 해당 위치 위에 있지 않을 때
        if suspect[1] is not self.robot_pose:        
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

    def move(self,robot_pose, target_pose):
        diffx = target_pose[0] - robot_pose[0]
        diffy = target_pose[1] - robot_pose[1]
        
        diff = (diffx, diffy)
        
        print(f"    ori: {self.robot_orientation}")
        
        if self.robot_orientation == "row":
            if diff[1] > 0: 
                print(f"        pmov {abs(diff[1])}")
                self.str = self.str+f"pmov {abs(diff[1])}"+self.pas_icon
            elif diff[1] < 0: 
                print(f"        mmov {abs(diff[1])}")
                self.str = self.str+f"mmov {abs(diff[1])}"+self.pas_icon
            if diff[0] > 0:
                print("        rol")
                self.str = self.str+"rol"+self.pas_icon
                
                self.robot_orientation = "col"
                print(f"        pmov {abs(diff[0])}")
                self.str = self.str+f"pmov {abs(diff[0])}"+self.pas_icon
            elif diff[0] < 0:
                print("        rol")
                self.str = self.str+"rol"+self.pas_icon
                
                self.robot_orientation = "col"
                print(f"        mmov {abs(diff[0])}")
                self.str = self.str+f"mmov {abs(diff[0])}"+self.pas_icon
        elif self.robot_orientation == "col":
            if diff[0] > 0:
                print(f"        pmov {abs(diff[0])}")
                self.str = self.str+f"pmov {abs(diff[0])}"+self.pas_icon
            elif diff[0] < 0:
                print(f"        mmov {abs(diff[0])}")
                self.str = self.str+f"mmov {abs(diff[0])}"+self.pas_icon
            if diff[1] > 0: 
                print("        rol")
                self.str = self.str+"rol"+self.pas_icon
                
                self.robot_orientation = "row"
                print(f"        pmov {abs(diff[1])}")
                self.str = self.str+f"pmov {abs(diff[1])}"+self.pas_icon
            elif diff[1] < 0: 
                print("        rol")
                self.str = self.str+"rol"+self.pas_icon
                
                self.robot_orientation = "row"
                print(f"        mmov {abs(diff[1])}")
                self.str = self.str+f"mmov {abs(diff[1])}"+self.pas_icon
        print("")
        
        return

    def workDqRun(self):
        
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
        return self.str

    def globalVal(self, cols, rows, start_pose, start_orientation):
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
        
        self.work_dq = dq()
        self.scatter_dq = dq()
        
        self.str = ""
        self.pas_icon = "\n"
        
    def __init__(self, cols=2, rows=3, start_pose=(0, 0), start_orientation="row"):
        self.globalVal(cols, rows, start_pose, start_orientation)

################## server

class Server:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message_queue = que.Queue()
        self.running = False
        
        self.initWorkDq()

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print(f"서버가 {self.host}:{self.port}에서 시작되었습니다.")
        self.running = True
        
        # 클라이언트 연결을 처리하는 스레드 시작
        threading.Thread(target=self.acceptConnections, daemon=True).start()
        
        # 메인 스레드에서 사용자 입력 처리
        while self.running:
            while not self.message_queue.empty():
                time.sleep(1)
            
            message = input("target load(ex: 1 1 1): ").split()
            print(message)
            
            if message[0] == "quit":
                self.running = False
            elif len(message) != 3:
                continue
            else:
                input_num = [int(i) for i in message]
                self.message_queue.put(input_num)

        self.server_socket.close()
        print("서버를 종료합니다.")

    def acceptConnections(self):
        while self.running:
            try:
                self.server_socket.settimeout(1.0)  # 1초 타임아웃 설정
                client_socket, addr = self.server_socket.accept()
                print(f"클라이언트가 {addr}에서 연결되었습니다.")
                
                # 클라이언트 처리를 위한 새 스레드 시작
                threading.Thread(target=self.handleClient, args=(client_socket,), daemon=True).start()
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"연결 수락 중 오류 발생: {e}")

    def handleClient(self, client_socket):
        try:
            while self.running:
                try:
                    input_num = self.message_queue.get(timeout=1.0)
                    
                    message = self.setAndRunWorkDq(input_num)
                    
                    client_socket.send(message.encode('utf-8'))
                    # print(f"메시지를 전송했습니다: {message}")
                    self.resetWorkDq()
                except que.Empty:
                    continue
        finally:
            client_socket.close()
            
    def initWorkDq(self):
        self.work_dq = WorkDq()
            
        self.work_dq.grid[1][1].append(("test", 0, 1))
        self.work_dq.grid[1][1].append(("test2", 1, 1))
        # grid[2][1].append(("test3", 2, 1))
    
    def setAndRunWorkDq(self, input_num):
        pick_order = ("pick", (input_num[0], input_num[1]), input_num[2]) # (2, 2)의 1층을 집음
        place_order = ("place", self.work_dq.pick_up_pose, -1) # level이 -1인 경우 기존 층 위에 쌓음

        self.work_dq.work_dq.appendleft(pick_order) # que처럼 사용
        self.work_dq.work_dq.appendleft(place_order)
        
        message = self.work_dq.workDqRun()
        
        print(message)
        
        return message
    
    def resetWorkDq(self):
        self.work_dq.black_list = [self.work_dq.pick_up_pose]
        self.work_dq.str = ""

if __name__ == "__main__":
    host = '192.168.0.7'
    port = 12345
    if len(sys.argv) == 3:
        host = sys.argv[1]
        port = int(sys.argv[2])

    server = Server(host, port)
    server.start()

# if __name__ == "__main__":
#     workDq = WorkDq()
    
#     workDq.grid[1][1].append(("test", 0, 1))
#     workDq.grid[1][1].append(("test2", 1, 1))
#     # grid[2][1].append(("test3", 2, 1))

#     pick_order = ("pick", (1, 1), 1) # (2, 2)의 1층을 집음
#     place_order = ("place", (0, 0), -1) # level이 -1인 경우 기존 층 위에 쌓음

#     workDq.work_dq.appendleft(pick_order) # que처럼 사용
#     workDq.work_dq.appendleft(place_order)
    
#     workDq.workDqRun()
