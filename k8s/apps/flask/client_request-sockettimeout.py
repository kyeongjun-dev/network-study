import socket
import time

# --- 설정 ---
HOST = 'nlb-address' # 1. NLB의 DNS 주소
PORT = 8000                            # 2. NLB 리스너 포트
YOUR_HOST_HEADER = 'nlb-address'         # 3. (Gunicorn/Nginx가 인지하는) Host 헤더
READ_TIMEOUT = 10.0 # 10초만 기다린다
# -----------

# Gunicorn/Nginx로 보낼 HTTP 요청 메시지
# (NLB는 L4라 HTTP를 모르지만, Gunicorn은 HTTP를 받아야 하므로)
REQUEST = (
    f"GET /slow-response HTTP/1.1\r\n"
    f"Host: {YOUR_HOST_HEADER}\r\n"
    f"Connection: keep-alive\r\n"
    f"\r\n"
).encode('utf-8')

print(f"--- Read Timeout Test ({READ_TIMEOUT}s) ---")
print(f"Target: {HOST}:{PORT}")
print(f"Server will sleep for 20s, Client will wait for {READ_TIMEOUT}s.")

s = None

try:
    # 1. 소켓 생성 및 연결
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"\nConnecting to {HOST}:{PORT}...")
    s.connect((HOST, PORT))
    print("Connected!")
    
    # 2. !! 읽기 타임아웃 설정 !!
    # connect() 성공 후에 설정해야 함
    s.settimeout(READ_TIMEOUT) 
    print(f"Socket read timeout set to {READ_TIMEOUT} seconds.")

    # 3. 첫 번째 요청 전송
    print("\n--- Sending request (Server will sleep for 20s) ---")
    s.sendall(REQUEST)
    
    # 4. 첫 번째 응답 수신 (!! 여기서 10초 대기 후 타임아웃 발생 예상 !!)
    print(f"--- Waiting for response (max {READ_TIMEOUT}s)... ---")
    response = s.recv(4096) # 10초 동안 응답이 안 오면 예외 발생

    # (여기까지 오면 테스트 실패)
    print("--- Received response (UNEXPECTED) ---")
    print(response.decode('utf-8', errors='ignore'))
    print("*** TEST FAILED: Server responded too quickly. ***")

except socket.timeout:
    # 5. s.recv(4096)에서 10초가 지나 타임아웃 발생 (테스트 성공)
    print(f"\n*** TEST SUCCESSFUL: Caught expected 'socket.timeout'! ***")
    print("The read operation timed out after 10 seconds.")
except socket.error as e:
    print(f"\n*** TEST FAILED: Caught unexpected socket error. ***")
    print(f"Error: {e}")
except Exception as e:
    print(f"\n*** SCRIPT ERROR: {e} ***")
finally:
    if s:
        s.close()
    print("\nSocket closed.")