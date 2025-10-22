package com.example.app_a;

import org.apache.hc.client5.http.config.RequestConfig;
import org.apache.hc.client5.http.impl.classic.CloseableHttpClient;
import org.apache.hc.client5.http.impl.classic.HttpClientBuilder;
import org.springframework.http.client.HttpComponentsClientHttpRequestFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.util.concurrent.TimeUnit;

@Component
public class RestTemplateFactory {

    /**
     * 동적 타임아웃이 적용된 RestTemplate을 생성합니다.
     *
     * @param connectTimeoutMs Connection Timeout (ms)
     * @param readTimeoutMs    Read/Socket Timeout (ms)
     * @return 타임아웃이 적용된 RestTemplate 인스턴스
     */
    public RestTemplate create(int connectTimeoutMs, int readTimeoutMs) {
        
        RequestConfig config = RequestConfig.custom()
                // 1. Connection Timeout: 원격 호스트와 연결을 맺는 데 걸리는 최대 시간
                .setConnectTimeout(connectTimeoutMs, TimeUnit.MILLISECONDS)
                
                // 2. Read/Socket Timeout: 연결 후 데이터를 읽어오는 데 걸리는 최대 시간
                // (HttpClient 5에서는 .setResponseTimeout 사용)
                .setResponseTimeout(readTimeoutMs, TimeUnit.MILLISECONDS)
                .build();

        CloseableHttpClient httpClient = HttpClientBuilder.create()
                .setDefaultRequestConfig(config)
                .build();

        HttpComponentsClientHttpRequestFactory factory = new HttpComponentsClientHttpRequestFactory(httpClient);

        return new RestTemplate(factory);
    }
}