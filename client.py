# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 00:34:48 2024

@author: jonwo
"""

import socket
import json

def send_request(host, port, graph, start, goal):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        
        # 데이터 준비
        data = {
            "graph": graph,
            "start": start,
            "goal": goal
        }
        
        # JSON으로 인코딩하여 전송
        s.sendall(json.dumps(data).encode('utf-8'))
        
        # 응답 수신
        response = s.recv(4096)
        
        return response.decode('utf-8')

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 65432

    # 예제 그래프
    graph = {
        "A": ["B", "C"],
        "B": ["A", "D", "E"],
        "C": ["A", "F"],
        "D": ["B"],
        "E": ["B", "F"],
        "F": ["C", "E"]
    }
    start = "A"
    goal = "F"

    try:
        result = send_request(HOST, PORT, graph, start, goal)
        print(f"Server response: {result}")
        
        # JSON 응답 파싱
        response_data = json.loads(result)
        if 'path' in response_data:
            path = response_data['path']
            if path:
                print(f"Path found: {' -> '.join(path)}")
            else:
                print("No path found")
        else:
            print("Unexpected response format")
    except json.JSONDecodeError:
        print("Failed to parse server response")
    except ConnectionRefusedError:
        print("Failed to connect to the server. Make sure the server is running.")
    except Exception as e:
        print(f"An error occurred: {e}")