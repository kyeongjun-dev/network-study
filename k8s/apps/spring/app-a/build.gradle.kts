plugins {
	java
	id("org.springframework.boot") version "3.5.6"
	id("io.spring.dependency-management") version "1.1.7"
}

group = "com.example"
version = "0.0.1-SNAPSHOT"
description = "Demo project for Spring Boot"

java {
	toolchain {
		languageVersion = JavaLanguageVersion.of(17)
	}
}

tasks.apply {
    bootJar {
    	// 실행 가능한 JAR 생성 설정
        enabled = true
    }
    jar {
        // 일반 JAR 파일 생성 비활성화
        enabled = false
    }
}

repositories {
	mavenCentral()
}

dependencies {
	implementation("org.springframework.boot:spring-boot-starter-web")
	testImplementation("org.springframework.boot:spring-boot-starter-test")
	testRuntimeOnly("org.junit.platform:junit-platform-launcher")
	// add for timeout test
	implementation("org.apache.httpcomponents.client5:httpclient5")
}

tasks.withType<Test> {
	useJUnitPlatform()
}
