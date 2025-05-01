package com.riveo.minio;

import com.riveo.minio.service.MinioService;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.bean.override.mockito.MockitoBean;

@SpringBootTest
@ActiveProfiles("test")
class MinioApplicationTests {


	@MockitoBean
    private MinioService minioService;

	@Test
	void contextLoads() {
	}

}
