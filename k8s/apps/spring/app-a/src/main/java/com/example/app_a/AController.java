package com.example.app_a; // ❗️ 본인 패키지명 확인

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
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
    private final String appBUrl;

    @Autowired
    public AController(
            RestTemplateFactory restTemplateFactory,
            @Value("${appb.client.base-url}") String appBBaseUrl,
            @Value("${appb.client.port}") int appBPort
    ) {
        this.restTemplateFactory = restTemplateFactory;
        this.appBUrl = String.format("%s:%d/api/b/hello", appBBaseUrl, appBPort);
    }
    
    @GetMapping("/api/a/call-b")
    public ResponseEntity<String> callB(
            @RequestParam(name = "delay", defaultValue = "0") int delay,
            @RequestParam(name = "connectTimeout", defaultValue = "${appb.client.default-timeout.connect}") int connectTimeout,
            @RequestParam(name = "readTimeout", defaultValue = "${appb.client.default-timeout.read}") int readTimeout
            // ❗️ validateAfterInactivity 파라미터가 제거되었습니다.
    ) {
        log.info("Calling B (URL: {}) with delay={}, connectTimeout={}, readTimeout={}",
                appBUrl, delay, connectTimeout, readTimeout);

        try {
            // ❗️ 파라미터가 2개만 전달되는지 확인
            RestTemplate restTemplate = restTemplateFactory.create(connectTimeout, readTimeout);

            String urlWithDelay = appBUrl + "?delay=" + delay;
            String response = restTemplate.getForObject(urlWithDelay, String.class);
            return ResponseEntity.ok("Success: " + response);

        } catch (ResourceAccessException e) {
            log.error("ResourceAccessException (Timeout or Connection Reset)", e);
            StringWriter sw = new StringWriter();
            e.printStackTrace(new PrintWriter(sw));
            String stackTrace = sw.toString();
            return ResponseEntity.status(502).body(stackTrace);
        } catch (Exception e) {
            log.error("Other error", e);
            StringWriter sw = new StringWriter();
            e.printStackTrace(new PrintWriter(sw));
            String stackTrace = sw.toString();
            return ResponseEntity.status(500).body(stackTrace);
        }
    }
}