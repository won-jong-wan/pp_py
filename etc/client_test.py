#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 17:20:04 2024

@author: won
"""

import socket

def start_client(host='localhost', port=12345):
    # 소켓 객체 생성
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # 서버에 연결
        client_socket.connect((host, port))
        print(f"서버 {host}:{port}에 연결되었습니다.")

        while True:
            # 서버로부터 데이터 수신
            data = client_socket.recv(1024)
            if not data:
                print("서버와의 연결이 종료되었습니다.")
                break

            # 수신한 데이터 디코딩 및 출력
            message = data.decode('utf-8')
            print(f"서버로부터 받은 메시지: {message}")

    except ConnectionRefusedError:
        print("서버에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요.")
    except KeyboardInterrupt:
        print("클라이언트를 종료합니다.")
    finally:
        # 소켓 닫기
        client_socket.close()

if __name__ == "__main__":
    start_client()