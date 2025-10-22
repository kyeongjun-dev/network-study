package com.example.app_a; // ❗️ 본인 패키지명 확인

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value; // ⬇️ Import 추가
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestTemplate;

import java.io.PrintWriter;
import java.io.StringWriter;

@RestController
public class AController {

    private static final Logger log = LoggerFactory.getLogger(AController.class);
    private final RestTemplateFactory restTemplateFactory;

    // ⬇️ [수정] YAML에서 주입받은 값으로 최종 URL을 조립
    private final String appBUrl; // 예: "http://app-b:8081/api/b/hello"

    @Autowired
    public AController(
            RestTemplateFactory restTemplateFactory,
            @Value("${appb.client.base-url}") String appBBaseUrl, // ⬇️ YAML 값 주입
            @Value("${appb.client.port}") int appBPort             // ⬇️ YAML 값 주입
    ) {
        this.restTemplateFactory = restTemplateFactory;
        
        // ⬇️ [수정] 생성자에서 URL을 한 번만 조립
        this.appBUrl = String.format("%s:%d/api/b/hello", appBBaseUrl, appBPort);
    }

    @GetMapping("/api/a/call-b")
    public ResponseEntity<String> callB(
            @RequestParam(name = "delay", defaultValue = "0") int delay,

            // ⬇️ [수정] defaultValue에 YAML 값을 직접 지정
            @RequestParam(name = "connectTimeout", defaultValue = "${appb.client.default-timeout.connect}") int connectTimeout,
            @RequestParam(name = "readTimeout", defaultValue = "${appb.client.default-timeout.read}") int readTimeout
    ) {
        log.info("Calling B (URL: {}) with delay={}, connectTimeout={}, readTimeout={}",
                appBUrl, delay, connectTimeout, readTimeout);

        try {
            RestTemplate restTemplate = restTemplateFactory.create(connectTimeout, readTimeout);
            
            // ⬇️ [수정] 조립된 URL 사용
            String urlWithDelay = appBUrl + "?delay=" + delay;
            String response = restTemplate.getForObject(urlWithDelay, String.class);
            
            return ResponseEntity.ok("Success: " + response);

        } catch (ResourceAccessException e) {
            log.error("Timeout occurred", e);
            StringWriter sw = new StringWriter();
            e.printStackTrace(new PrintWriter(sw));
            String stackTrace = sw.toString();
            return ResponseEntity.status(504).body(stackTrace);

        } catch (Exception e) {
            log.error("Other error", e);
            StringWriter sw = new StringWriter();
            e.printStackTrace(new PrintWriter(sw));
            String stackTrace = sw.toString();
            return ResponseEntity.status(500).body(stackTrace);
        }
    }
}