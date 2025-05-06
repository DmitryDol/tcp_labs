package com.riveo.minio;

import com.riveo.minio.service.JwtUtil;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class MinioApplication {

	public static void main(String[] args) {
		SpringApplication.run(MinioApplication.class, args);
	}

	@Bean
	public JwtUtil jwtUtil() {
		return new JwtUtil();
	}
}