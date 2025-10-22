# app_a.py
from flask import Flask
import requests
import time
import os
import logging

app = Flask(__name__)

# K8s 내부 DNS 이름을 사용
TARGET_HOST = os.environ.get('TARGET_HOST', 'http://my-python-app:8000')
# App B의 keep-alive(10초)보다 길게 설정
IDLE_TIME = int(os.environ.get('IDLE_TIME', '15')) 

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

@app.route('/')
def index():
    return "Hello from App A (Client). Go to /test-reset to start the test."

@app.route('/test-reset')
def test_reset():
    # 세션을 생성하여 Keep-Alive 연결을 사용
    session = requests.Session()
    
    # 1. 최초 호출 (Keep-Alive 연결 수립)
    try:
        log.info(f"Making INITIAL request to {TARGET_HOST}/")
        resp1 = session.get(f"{TARGET_HOST}/")
        log.info(f"INITIAL request successful. Status: {resp1.status_code}, Text: {resp1.text}")
    except Exception as e:
        log.error(f"INITIAL request FAILED: {e}")
        return f"Initial request failed: {e}", 500

    # 2. App B의 Gunicorn keep-alive 타임아웃(10초)보다 길게 대기
    log.info(f"Sleeping for {IDLE_TIME} seconds to let connection go idle...")
    time.sleep(IDLE_TIME)
    log.info("Sleep finished.")

    # 3. 동일 세션(오래된 소켓)으로 두 번째 호출
    try:
        log.info(f"Making SECOND request to {TARGET_HOST}/")
        resp2 = session.get(f"{TARGET_HOST}/")
        log.info(f"SECOND request successful. Status: {resp2.status_code}")
        # 이 응답을 받으면 테스트 실패 (Connection Reset이 발생하지 않음)
        return f"TEST FAILED: Both requests worked. No connection reset. (Status: {resp2.status_code})", 500
    except requests.exceptions.ConnectionError as e:
        # ConnectionResetError는 requests.exceptions.ConnectionError로 래핑됨
        log.warning(f"CAUGHT EXPECTED ERROR: {e}")
        # 이 응답을 받으면 테스트 성공
        return f"TEST PASSED: Caught expected ConnectionError (likely ConnectionResetError): {e}", 200
    except Exception as e:
        log.error(f"UNEXPECTED ERROR on second request: {e}")
        return f"Unexpected error: {e}", 500

if __name__ == '__main__':
    # App A는 8001 포트에서 실행
    app.run(host='0.0.0.0', port=8001)