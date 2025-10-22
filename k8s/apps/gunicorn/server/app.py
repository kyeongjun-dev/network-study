from flask import Flask
import os
import time

app = Flask(__name__)

wait_time = int(os.environ.get('WAIT_TIME', '10'))

@app.route('/')
def hello():
    return "Hello from Flask App behind NGINX!"

# 로드밸런서 유휴 시간 초과 재현을 위한 엔드포인트
@app.route('/slow-response')
def slow_response():
    print(f"Request received. Waiting for {wait_time} seconds...")
    # 이 시간은 테스트하려는 로드밸런서의 유휴 시간보다 길어야 합니다.
    time.sleep(wait_time)
    start_time = time.time()
    while time.time() - start_time < wait_time:
        pass
    print(f"Waited {wait_time} seconds. Sending response now.")
    return "Finally, here is your slow response!"


if __name__ == '__main__':
    timeout = int(os.environ.get('TIMEOUT', '30'))
    keep_alive = int(os.environ.get('KEEP_ALIVE', '5'))

    # 이 부분은 Docker 이미지에서는 Gunicorn으로 대체되므로 직접 실행되지 않습니다.
    app.run(host='0.0.0.0', port=8000)