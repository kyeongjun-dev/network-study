package com.example.app_b;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.concurrent.TimeUnit;

@RestController
public class BController {

    @GetMapping("/api/b/hello")
    public String hello(@RequestParam(name = "delay", defaultValue = "0") int delay) {
        try {
            TimeUnit.MILLISECONDS.sleep(delay);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return "Error during delay";
        }
        return "Hello from B (after " + delay + "ms delay)";
    }
}