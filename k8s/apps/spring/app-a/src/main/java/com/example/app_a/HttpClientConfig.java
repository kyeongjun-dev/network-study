package com.example.app_a;

import org.apache.hc.client5.http.impl.io.PoolingHttpClientConnectionManager;
import org.apache.hc.core5.util.TimeValue;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class HttpClientConfig {

    @Value("${appb.client.keep-alive.validate-after-inactivity}")
    private int validateAfterInactivityMs;

    /**
     * 애플리케이션 전역에서 공유할 단 하나의 커넥션 풀을 생성합니다.
     */
    @Bean
    public PoolingHttpClientConnectionManager poolingHttpClientConnectionManager() {
        PoolingHttpClientConnectionManager connManager = new PoolingHttpClientConnectionManager();

        // YAML 파일에서 읽어온 값으로 유휴 검사 시간 설정
        connManager.setValidateAfterInactivity(TimeValue.ofMilliseconds(validateAfterInactivityMs));
        
        // (선택) 최대 연결 수 등 다른 옵션도 여기서 설정 가능
        // connManager.setMaxTotal(200);
        // connManager.setDefaultMaxPerRoute(20);

        return connManager;
    }
}