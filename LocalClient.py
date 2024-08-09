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

from rich import print

class LocalClient:
    def recv(self, local_socket, addr):
        print(f"(thread_start)_recv: {addr}")
        
        while True:
            try:
                data = local_socket.recv(1024).decode('utf-8')
                if not data:
                    continue
                print(f"\n[orange](message)[/orange]_recv: {data}")
                self.get_queue.put(data)
                # client_socket.send("메시지를 받았습니다.".encode('utf-8'))
            except Exception as e:
                print(f"[red](error)[/red]_recv: {e}")
                break
        print(f"[orange](thread_end)[/orange]_recv: {addr}")  
        local_socket.close()
    
    def send(self, local_socket, addr):
        print(f"(thread_start)_send: {addr}")
        
        while True:
            try:
                if not self.send_queue.empty():
                    data = self.send_queue.get() 
                    print(f"\n(message)_local_to_core: {data}")
                    local_socket.send(data.encode('utf-8'))
                else:
                    time.sleep(0.1)
            except Exception as e: 
                print(f"(error)_send: {e}") 
                break
        print(f"(thread_end)_send: {addr}")
        local_socket.close()
    
    def client_start(self, host= "localhost", port= 8888, commend= "", num= "", log= ""):
        print("\n\n[pink]Local Client Start[/pink]")
        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            #server.settimeout(1.0) 
            client.connect((host, port))
            print(f"[orange](client_start)[/orange]_client_connect_{host}:{port}")
            
            recv_thread = threading.Thread(target=self.recv, 
                                                    args=(client, host)) 
            send_thread = threading.Thread(target=self.send, 
                                                    args=(client, host)) 
            
            recv_thread.daemon = True
            send_thread.daemon = True
            
            recv_thread.start()
            send_thread.start()
        except Exception as e:
            print(f"[red](error)[/red]_client: {e}")
            
        if self.is_typer:
            self.typer_queue(commend, num)
            
            recv_thread.join(0.5)
            send_thread.join(0.5)
        elif self.is_long:
            self.long_fill_queue(log)
            
            recv_thread.join(0.5)
            send_thread.join(0.5)
        else:
            self.fill_queue()
        # self.fill_queue()

        # recv_thread.join()
        # send_thread.join()
        
    def fill_queue(self):
        
        self.running = True
        while self.running:
            while not self.send_queue.empty():
                time.sleep(1)
                
            message = "empty"
            message = input("\nmessage: ")
            # print(message)
            
            if message == "quit":
                self.running = False
            else:
                # input_num = [int(i) for i in message]
                self.send_queue.put("<@{message}!>")
                continue
                
        print("(stop)_fill_queue")
    
    def typer_queue(self, commend, num):
        self.send_queue.put(f"<@{commend} {num}!>")
        
    def long_fill_queue(self, log):
        self.send_queue.put(f"<@{log}!>")
        
    # def long_raw_queue(self, log):
    #     self.send_queue.put(f"<@{log}!>")
        
    def __init__(self):
        self.send_queue = queue.Queue()
        self.get_queue = queue.Queue()
        self.running = False
        self.is_typer = False
        self.is_long = False

# if __name__ == "__main__":
#     HOST = "localhost"
#     PORT = 8888
    
#     client = LocalClient()
    
#     client.client_start(HOST, PORT)
        
#     print("(stop)_main_thread")
