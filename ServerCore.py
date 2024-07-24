#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 15:00:03 2024

@author: won
"""
import socket
import threading
import queue
import time

class ServerCore:
    def handle_robot_to_core(self, robot_socket, addr):
        print(f"(thread_start)_robot_to_core: {addr}")
        while True:
            try:
                data = robot_socket.recv(1024).decode('utf-8')
                if not data:
                    continue
                print(f"(message)_robot_to_core: {data}")
                self.get_message_queue.put(data)
                # client_socket.send("<get_ok>".encode('utf-8'))
            except Exception as e:
                print(f"(error)_robot_to_core: {e}")
                break
        print(f"(thread_end)_robot_to_core: {addr}")
        robot_socket.close()

    def handle_core_to_robot(self, robot_socket, addr):
        print(f"(thread_start)_core_to_robot: {addr}")
        while True:
            try:
                if not self.send_message_queue.empty():
                    data = self.send_message_queue.get() 
                    print(f"(message)_core_to_robot: {data}")
                    robot_socket.send(data.encode('utf-8'))
                else:
                    time.sleep(0.1)
            except Exception as e: 
                print(f"(error)_core_to_robot: {e}") 
                break
        print(f"(thread_end)_core_to_robot: {addr}")
        robot_socket.close()

    def handle_local_to_core(self, local_socket, addr):
        print(f"(thread_start)_local_to_core: {addr}")
        while True:
            try:
                data = local_socket.recv(1024).decode('utf-8')
                if not data:
                    continue
                print(f"(message)_local_to_core: {data}")
                self.send_message_queue.put(data)
                # client_socket.send("메시지를 받았습니다.".encode('utf-8'))
            except Exception as e:
                print(f"(error)_local_to_core: {e}")
                break
        print(f"(thread_end)_local_to_core: {addr}")  
        local_socket.close()
    
    def handle_core_to_local(self, local_socket, addr):
        print(f"(thread_start)_core_to_local: {addr}")
        while True:
            try:
                if not self.get_message_queue.empty():
                    data = self.get_message_queue.get() 
                    print(f"(message)_core_to_local: {data}")
                    local_socket.send(data.encode('utf-8'))
                else:
                    time.sleep(0.1)
            except Exception as e: 
                print(f"(error)_core_to_local: {e}") 
                break
        print(f"(thread_end)_core_to_local: {addr}")
        local_socket.close()

    def start_robot_server(self, host, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((host, port)) 
            server.listen()
            
            print(f"(server_start)_robot_server_{host}:{port}")
            
            while True:
                try:
                    #server.settimeout(1.0) 
                    robot_sock, addr = server.accept()
                    
                    core_to_robot_thread = threading.Thread(target=self.handle_core_to_robot, 
                                                            args=(robot_sock, addr)) 
                    robot_to_core_thread = threading.Thread(target=self.handle_robot_to_core, 
                                                            args=(robot_sock, addr)) 
                    core_to_robot_thread.start()
                    robot_to_core_thread.start()
                except socket.timeout():
                    continue
                except Exception as e:
                    print(f"(error)_robot_server: {e}")

    def start_local_server(self, host, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((host, port)) 
            server.listen()
            
            print(f"(server_start)_local_server_{host}:{port}")

            while True:
                try:
                    local_sock, addr = server.accept()
                    core_to_local_thread = threading.Thread(target=self.handle_core_to_local, 
                                                            args=(local_sock, addr))
                    local_to_core_thread = threading.Thread(target=self.handle_local_to_core, 
                                                            args=(local_sock, addr))
                
                    core_to_local_thread.start()
                    local_to_core_thread.start()
                except socket.timeout():
                    continue
                except Exception as e:
                    print(f"(error)_robot_server: {e}")

    # def process_messages():
    #     while True:
    #         source, message = message_queue.get()
    #         print(f"처리 중: {source}로부터의 메시지 - {message}")
    #         # 여기에 메시지 처리 로직을 추가하세요
    #         message_queue.task_done()
    def set_robot_host_port(self, host, port):
        self.robot_host = host
        self.robot_port = port
        
    def set_local_host_port(self, host, port):
        self.local_host = host
        self.local_port = port
    
    def start_server(self):
        # robot server
        robot_thread = threading.Thread(target=self.start_robot_server, 
                                        args=(self.robot_host, self.robot_port))
        # local server
        local_thread = threading.Thread(target=self.start_local_server, 
                                        args=(self.local_host, self.local_port))
        
        print("Server Core Start")
        robot_thread.start()
        local_thread.start()

        # message
        # process_thread = threading.Thread(target=process_messages)
        # process_thread.start()

        # 메인 스레드가 종료되지 않도록 대기
        robot_thread.join()
        local_thread.join()
        # process_thread.join()
        
    def __init__(self):
        self.send_message_queue = queue.Queue()
        self.get_message_queue = queue.Queue()

if __name__ == "__main__":
    ROBOT_HOST = '192.168.0.8'  # 모든 인터페이스에서 외부 연결 허용
    ROBOT_PORT = 12345       # 외부에서 접속할 포트
    LOCAL_HOST = 'localhost'   # 로컬 연결만 허용
    LOCAL_PORT = 8888          # 로컬에서 접속할 포트
    
    core = ServerCore()
    
    core.set_robot_host_port(ROBOT_HOST, ROBOT_PORT)
    core.set_local_host_port(LOCAL_HOST, LOCAL_PORT)
    
    core.start_server()
