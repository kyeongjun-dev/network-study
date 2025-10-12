import socket
import time

# 31초 대기하여 서버의 타임아웃 유발
print("31초 후 서버에 접속을 시도합니다.")
time.sleep(31)

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 30000))
    print("서버에 연결 시도...") # 이 메시지는 서버가 이미 닫혀서 보이지 않을 것입니다.

except ConnectionRefusedError:
    print("서버에 연결할 수 없습니다. 서버가 이미 종료된 것 같습니다.")
    
finally:
    client_socket.close()