# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 01:10:10 2024

@author: jonwo
"""

from WorkDq import WorkDq
import csv

import sys
import threading
import socket
import time
import queue as que

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
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
            
            message = input("Act: ").split()
            # print(message)
            
            if message[0] == "quit":
                self.running = False
            elif message[0] == "pick":
                detail = input("Pose: ").split()
                self.message_queue.put(("pick", detail))
            elif message[0] == "place":
                detail = input("Pose: ").split()
                self.message_queue.put(("place", detail))
            else:
                #input_num = [int(i) for i in message]
                continue

        self.server_socket.close()
        print("서버를 종료합니다.")

    def acceptConnections(self):
        while self.running:
            try:
                self.server_socket.settimeout(1.0)  # 1초 타임아웃 설정
                client_socket, addr = self.server_socket.accept()
                print(f"\n클라이언트가 {addr}에서 연결되었습니다.\n : ", end="")
                
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
                    order = self.message_queue.get(timeout=1.0)   
                    
                    message = "empty"
                    
                    if order[0] == "pick":
                        order_num = [int(i) for i in order[1]]
                        message = self.pickWorkDq(order_num)
                    elif order[0] == "place":
                        order_num = [int(i) for i in order[1]]
                        message = self.placeWorkDq(order_num)
                    # message = self.pickWorkDq(input_num)
                    # message = "<@pik 1#plc 1!>"
                    # message = "<@pov 1#rol 0#pov 1#pik 1#mov 1!>"
                    client_socket.send(message.encode('utf-8'))
                    # print(f"메시지를 전송했습니다: {message}")
                    self.resetWorkDq()
                except que.Empty:
                    continue
        finally:
            client_socket.close()
            
    def initWorkDq(self):
        self.work_dq = WorkDq()
        
        # with open('grid.csv', 'r', encoding='utf-8') as file:
        #     csv_reader = csv.reader(file)
        #     for row in csv_reader:
        #         self.work_dq.grid.append(row)
            
        # self.work_dq.grid[0][0].append(("001", 0))
        self.work_dq.grid[0][0].append(("001", 0))
        self.work_dq.grid[0][1].append(("011", 1))
        self.work_dq.grid[0][1].append(("012", 1.5))
        self.work_dq.grid[1][0].append(("101", 2))
        self.work_dq.grid[1][0].append(("102", 3))
        self.work_dq.grid[2][0].append(("201", 4))
        self.work_dq.grid[2][0].append(("202", 5))
        self.work_dq.grid[1][1].append(("111", 6))
        self.work_dq.grid[1][1].append(("112", 7))
        self.work_dq.grid[2][1].append(("211", 8))
        # self.work_dq.grid[2][1].append(("212", 9))
        
        # self.work_dq.grid[2][1].append(("test3", 2, 1))
        # self.work_dq.grid[2][1].append(("test3", 2, 1))
        # grid[2][1].append(("test3", 2, 1))
        
        self.work_dq.str = "<@"
    
    def pickWorkDq(self, input_num):
        pick_order = ("pick", (input_num[0], input_num[1]), input_num[2]) # (2, 2)의 1층을 집음
        place_order = ("place", self.work_dq.pick_up_pose, -1) # level이 -1인 경우 기존 층 위에 쌓음

        self.work_dq.work_dq.appendleft(pick_order) # que처럼 사용
        self.work_dq.work_dq.appendleft(place_order)
        
        print("log: ")
        
        message = self.work_dq.run()+"!>"
        
        print("send message: "+message)
        
        return message
    
    def placeWorkDq(self, input_num):
        pick_order = ("pick", self.work_dq.pick_up_pose, -1) # (2, 2)의 1층을 집음
        place_order = ("place", (input_num[0], input_num[1]), input_num[2]) # level이 -1인 경우 기존 층 위에 쌓음

        self.work_dq.work_dq.appendleft(pick_order) # que처럼 사용
        self.work_dq.work_dq.appendleft(place_order)
        
        print("log: ")
        
        message = self.work_dq.run()+"!>"
        
        print("\nsend message: "+message)
        
        return message
    
    def resetWorkDq(self):
        self.work_dq.black_list = [self.work_dq.pick_up_pose]
        self.work_dq.str = "<@"
        
        with open('grid.csv', 'wt', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(self.work_dq.grid)

if __name__ == "__main__":
    host = '192.168.0.8'
    port = 12345
    if len(sys.argv) == 3:
        host = sys.argv[1]
        port = int(sys.argv[2])

    server = Server(host, port)
    server.start()

# if __name__ == "__main__":
#     workDq = WorkDq()
    
#     workDq.grid[1][1].append(("test", 0))
#     workDq.grid[1][1].append(("test2", 1))
#     workDq.grid[0][0].append(("test3", 2))
#     workDq.grid[0][0].append(("test3", 3))

#     pick_order = ("pick", (1, 1), 1) # (2, 2)의 1층을 집음
#     place_order = ("place", (0, 0), 1) # level이 -1인 경우 기존 층 위에 쌓음

#     workDq.work_dq.appendleft(pick_order) # que처럼 사용
#     workDq.work_dq.appendleft(place_order)
    
#     workDq.run()
    
#     print(workDq.str)
