package com.riveo.minio.config;

import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Contact;
import io.swagger.v3.oas.annotations.info.Info;

@OpenAPIDefinition(
        info = @Info(
                title = "Image Storage API",
                version = "1.0",
                description = "API for image management in MinIO",
                contact = @Contact(
                        name = "Dmitry Dolzhikov",
                        email = "dmdolzhikov@gmail.com"
                )
        )
)
public class OpenApiConfig {
}