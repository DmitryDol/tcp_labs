plugins {
	java
	id("org.springframework.boot") version "3.4.2"
	id("io.spring.dependency-management") version "1.1.7"
}

group = "com.riveo"
version = "0.0.1-SNAPSHOT"

java {
	toolchain {
		languageVersion = JavaLanguageVersion.of(17)
	}
}

repositories {
	mavenCentral()
}

dependencies {
	implementation("org.springframework.boot:spring-boot-starter-web")
	//implementation("org.springframework.boot:spring-boot-starter-security")
	//implementation("org.springframework.boot:spring-boot-starter-validation")

	implementation("io.jsonwebtoken:jjwt-api:0.12.3")
	runtimeOnly("io.jsonwebtoken:jjwt-impl:0.12.3")
	runtimeOnly("io.jsonwebtoken:jjwt-jackson:0.12.3")

	//runtimeOnly("org.postgresql:postgresql")
	//implementation("org.springframework.boot:spring-boot-starter-data-jpa")

	developmentOnly("org.springframework.boot:spring-boot-devtools")
	//testImplementation("org.springframework.boot:spring-boot-starter-test")
	testRuntimeOnly("org.junit.platform:junit-platform-launcher")
	implementation("io.minio:minio:8.5.17")
	implementation("org.springdoc:springdoc-openapi-starter-webmvc-ui:2.8.4")
	testImplementation("org.springframework.boot:spring-boot-starter-test") {
        exclude(group = "org.junit.vintage", module = "junit-vintage-engine")
    }
    testImplementation("org.mockito:mockito-core:5.3.1")
}

tasks.withType<Test> {
	useJUnitPlatform()
}
