import socket
import time

# --- 설정 ---
HOST = 'my-nlb-host.com' # 1. NLB의 DNS 주소
PORT = 8000                                  # 2. NLB 리스너 포트
YOUR_HOST_HEADER = 'my-nlb-host.com'         # 3. (Gunicorn/Nginx가 인지하는) Host 헤더
NLB_TIMEOUT = 300                            # 4. NLB 고정 타임아웃 (350초)
WAIT_TIME = NLB_TIMEOUT + 10                 # 5. NLB 타임아웃보다 길게 대기 (예: 360초)
# -----------

# Gunicorn/Nginx로 보낼 HTTP 요청 메시지
# (NLB는 L4라 HTTP를 모르지만, Gunicorn은 HTTP를 받아야 하므로)
REQUEST = (
    f"GET / HTTP/1.1\r\n"
    f"Host: {YOUR_HOST_HEADER}\r\n"
    f"Connection: keep-alive\r\n"
    f"\r\n"
).encode('utf-8')

print(f"--- NLB Idle Timeout Test (350s) ---")
print(f"Target: {HOST}:{PORT}")
print(f"Server Keep-Alive must be > 350s for this test to be valid.")

try:
    # 1. 소켓 생성 및 NLB에 연결
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"\nConnecting to {HOST}:{PORT}...")
    s.connect((HOST, PORT))
    print("Connected!")

    # 2. 첫 번째 요청 전송 (연결 확인용)
    print("\n--- Sending first request ---")
    s.sendall(REQUEST)
    
    # 3. 첫 번째 응답 수신
    response = s.recv(4096)
    print("--- Received first response ---")
    # 응답의 첫 줄만 출력 (예: HTTP/1.1 200 OK)
    print(response.decode('utf-8', errors='ignore').split('\r\n')[0])

    # 4. NLB가 연결을 끊도록 'WAIT_TIME' (360초) 만큼 대기
    print(f"\n--- Waiting for {WAIT_TIME} seconds to trigger NLB idle timeout ---")
    for i in range(WAIT_TIME):
        time.sleep(1)
        # 진행 상황 표시 (6분은 깁니다)
        print(f"Waiting... {i+1}/{WAIT_TIME} seconds passed", end='\r')
    print("\n--- Wait finished ---")

    # 5. 두 번째 요청 전송 (!! 여기서 오류 발생 예상 !!)
    # 이 시점에 NLB는 350초가 지나 이미 클라이언트(이 스크립트)와 
    # 서버(Gunicorn) 양쪽에 RST 패킷을 보낸 상태입니다.
    print("\n--- Sending second request (on the *same* socket) ---")
    s.sendall(REQUEST) # 이미 끊어진 소켓(RST를 받은)에 쓰기 시도

    # (만약 오류가 안 나고 여기까지 오면 테스트 실패)
    print("--- Second request sent successfully (UNEXPECTED) ---")
    response = s.recv(4096)
    print("--- Received second response ---")
    print(response.decode('utf-8', errors='ignore'))

except socket.error as e:
    # 6. 'Connection reset by peer' (RST 수신) 
    # 또는 'Broken pipe' (RST 수신 후 write 시도) 오류 발생 (테스트 성공)
    print(f"\n*** TEST SUCCESSFUL: Caught expected error! ***")
    print(f"Error: {e}")
    print("This confirms the NLB idle timeout (350s) was triggered.")

finally:
    s.close()
    print("\nSocket closed.")