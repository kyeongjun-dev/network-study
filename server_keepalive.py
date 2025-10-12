# server_keepalive.py
import socket

# 서버 소켓 설정
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 30000))
server_socket.listen()
print("클라이언트 접속을 기다립니다...")

client_socket, addr = server_socket.accept()
print(f"{addr} 에서 접속했습니다.")

# --- Keepalive 옵션 설정 ---
# 1. Keepalive 활성화
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

# 아래 옵션들은 리눅스/macOS에서 좀 더 세부적인 설정이 필요할 때 사용합니다.
# (윈도우에서는 SIO_KEEPALIVE_VALS ioctl을 사용해야 해서 더 복잡합니다)
if hasattr(socket, "TCP_KEEPIDLE"):
    # 2. 마지막 데이터 교환 후 Keepalive 메시지를 처음 보낼 때까지 대기 시간 (초)
    client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)

if hasattr(socket, "TCP_KEEPINTVL"):
    # 3. Keepalive 메시지를 보내는 주기 (초)
    client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)

if hasattr(socket, "TCP_KEEPCNT"):
    # 4. 응답이 없을 경우 Keepalive 메시지를 보내는 최대 횟수
    client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)
# -----------------------------

print("Keepalive 설정을 완료했습니다. 연결은 유지되지만, 비정상 종료 시 감지됩니다.")

try:
    # 데이터 수신 대기 (여기서는 간단히 유지하는 것만 보여줌)
    while True:
        data = client_socket.recv(1024)
        if not data:
            print("클라이언트가 정상적으로 연결을 종료했습니다.")
            break
except Exception as e:
    print(f"오류가 발생하며 연결이 끊어졌습니다: {e}")
finally:
    client_socket.close()
    server_socket.close()