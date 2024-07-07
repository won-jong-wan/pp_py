# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 00:34:31 2024

@author: jonwo
"""

import socket
import json
from collections import deque

def bfs(graph, start, goal):
    queue = deque([[start]])
    visited = set([start])

    while queue:
        path = queue.popleft()
        vertex = path[-1]

        if vertex == goal:
            return path

        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

    return None

def handle_client(client_socket):
    # 클라이언트로부터 데이터 수신
    data = client_socket.recv(4096).decode('utf-8')
    
    try:
        # JSON 형식의 데이터 파싱
        request = json.loads(data)
        graph = request['graph']
        start = request['start']
        goal = request['goal']

        # BFS 수행
        result = bfs(graph, start, goal)

        # 결과를 JSON 형식으로 변환
        response = json.dumps({'path': result})

        # 결과 전송
        client_socket.send(response.encode('utf-8'))
    except json.JSONDecodeError:
        client_socket.send("Invalid JSON format".encode('utf-8'))
    except KeyError:
        client_socket.send("Missing required data".encode('utf-8'))
    finally:
        client_socket.close()

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 65432

    start_server(HOST, PORT)