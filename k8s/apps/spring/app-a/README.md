AWS의 NLB(Network Load Balancer)는 유휴 상태(데이터 전송이 없는) TCP 연결을 일정 시간(기본값 350초)이 지나면 말없이(Silently) 끊어버립니다.

하지만 App A의 커넥션 풀은 그 연결이 끊겼다는 사실을 모르고 "아직 유효한 연결"이라고 착각합니다. 이 상태에서 App A가 350초가 지난 뒤 이 '죽은' 연결을 재사용하여 요청을 보내면, NLB가 TCP RST(Reset) 패킷을 보내고, App A에서는 java.net.SocketException: Connection reset by peer (혹은 Connection reset) 에러가 발생합니다.

## 1. 해결 및 테스트 원리
이 문제를 해결(또는 테스트)하는 방법은 App A의 Apache HttpClient 커넥션 풀 설정, 그중에서도 setValidateAfterInactivity (비활성 후 유효성 검사) 값을 조정하는 것입니다.

NLB Idle Timeout: 350초 (고정)

validateAfterInactivity: 커넥션 풀에서 연결을 꺼내 쓸 때, 이 연결이 지정된 시간(예: 300초) 이상 쉬었으면, 요청을 보내기 전에 "이 연결 아직 살아있나?"라고 테스트(Validation Query)를 먼저 보내는 설정입니다.

이 값을 NLB 타임아웃(350초)보다 짧게 설정하면 에러를 방지할 수 있고, 길게 설정하면 에러를 재현할 수 있습니다.