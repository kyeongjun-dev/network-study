package com.example.app_a;

import org.apache.hc.client5.http.config.RequestConfig;
import org.apache.hc.client5.http.impl.classic.CloseableHttpClient;
import org.apache.hc.client5.http.impl.classic.HttpClientBuilder;
import org.apache.hc.client5.http.impl.io.PoolingHttpClientConnectionManager; // ⬅️ import
import org.springframework.beans.factory.annotation.Autowired; // ⬅️ import
import org.springframework.http.client.HttpComponentsClientHttpRequestFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.util.concurrent.TimeUnit;

@Component
public class RestTemplateFactory {

    // ⬇️ [수정] Bean으로 등록된 공유 커넥션 풀을 주입받습니다.
    private final PoolingHttpClientConnectionManager sharedConnectionManager;

    @Autowired
    public RestTemplateFactory(PoolingHttpClientConnectionManager sharedConnectionManager) {
        this.sharedConnectionManager = sharedConnectionManager;
    }

    /**
     * [수정] validateAfterInactivity 파라미터 제거
     * (공유 풀의 설정을 따르므로 동적 지정이 불가능)
     */
    public RestTemplate create(int connectTimeoutMs, int readTimeoutMs) {

        // 1. 요청별 타임아웃 설정 (기존과 동일)
        RequestConfig config = RequestConfig.custom()
                .setConnectTimeout(connectTimeoutMs, TimeUnit.MILLISECONDS)
                .setResponseTimeout(readTimeoutMs, TimeUnit.MILLISECONDS)
                .build();

        // 2. HttpClient 생성
        CloseableHttpClient httpClient = HttpClientBuilder.create()
                // ⬇️ [수정] 'new' 대신 주입받은 'sharedConnectionManager' 사용
                .setConnectionManager(sharedConnectionManager) 
                .setDefaultRequestConfig(config)
                .build();

        HttpComponentsClientHttpRequestFactory factory = new HttpComponentsClientHttpRequestFactory(httpClient);

        return new RestTemplate(factory);
    }
}