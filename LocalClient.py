#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 17:18:07 2024

@author: won
"""
import socket
import threading
import queue
import time

class LocalClient:
    def recv(self, local_socket, addr):
        print(f"(thread_start)_recv: {addr}")
        
        while True:
            try:
                data = local_socket.recv(1024).decode('utf-8')
                if not data:
                    continue
                print(f"(message)_recv: {data}")
                self.send_message_queue.put(data)
                # client_socket.send("메시지를 받았습니다.".encode('utf-8'))
            except Exception as e:
                print(f"(error)_local_to_core: {e}")
                break
        print(f"(thread_end)_recv: {addr}")  
        local_socket.close()
    
    def send(self, local_socket, addr):
        print(f"(thread_start)_send: {addr}")
        
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
        
    def __init__(self):
        self.send_queue = queue.Queue()
           