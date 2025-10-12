import socket

# 서버 소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 30000))
server_socket.listen()

print("서버가 30초 동안 클라이언트 연결을 기다립니다...")

try:
    # 서버 소켓이 클라이언트의 접속을 기다리는 시간을 30초로 설정 ⏰
    server_socket.settimeout(30)
    
    # accept()는 클라이언트가 연결할 때까지 여기서 실행을 멈춤(blocking)
    # 하지만 settimeout(30) 때문에 30초가 지나면 socket.timeout 예외를 발생시킴
    client_socket, addr = server_socket.accept()
    print(f"{addr} 에서 접속했습니다.")
    
    # 연결 성공 후 로직 (여기서는 간단히 연결 종료)
    client_socket.close()

except socket.timeout:
    print("30초 동안 접속이 없어 서버를 종료합니다.")

except Exception as e:
    print(f"오류가 발생했습니다: {e}")

finally:
    # 소켓 정리
    server_socket.close()
    print("서버 소켓을 닫았습니다.")