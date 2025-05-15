package com.riveo.minio.api.controller;

import com.riveo.minio.errorHandler.UnauthorizedException;
import com.riveo.minio.service.JwtUtil;
import com.riveo.minio.service.MinioService;
import io.swagger.v3.oas.annotations.enums.SecuritySchemeType;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.security.SecurityScheme;
import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletRequest;
import org.checkerframework.checker.units.qual.C;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.InputStreamResource;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;

import java.util.Collections;
import java.util.Map;

@Tag(name = "Files", description = "Image management")
@RestController
@RequestMapping("/files")
@SecurityScheme(
        name = "bearerAuth",
        type = SecuritySchemeType.HTTP,
        scheme = "bearer",
        bearerFormat = "JWT"
)
@SecurityRequirement(name = "bearerAuth")
public class FileController {

    private final MinioService minioService;
    private final JwtUtil jwtUtil;

    @Autowired
    public FileController(MinioService minioService, JwtUtil jwtUtil) {
        this.minioService = minioService;
        this.jwtUtil = jwtUtil;
    }

    private String extractToken(String authHeader, String accessTokenCookie, HttpServletRequest request) {
        if (authHeader != null && authHeader.startsWith("Bearer "))
            return authHeader.substring(7);


        if (accessTokenCookie != null && !accessTokenCookie.isEmpty())
            return accessTokenCookie;


        Cookie[] cookies = request.getCookies();
        if (cookies != null)
            for (Cookie cookie : cookies)
                if ("access_token".equals(cookie.getName()))
                    return cookie.getValue();

        return null;
    }

    @Operation(
            summary = "File upload",
            description = "Uploads a file to the specified bucket and returns the generated filename. Requires JWT authentication.",
            responses = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "File successfully uploaded",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(
                                            type = "object",
                                            example = "{\\"filename\\": \\"f97fbd57-7224-4342-9c48-c04536067ade.png\\"}"
                                    )
                            )
                    ),
                    @ApiResponse(
                            responseCode = "400",
                            description = "Invalid bucket name",
                            content = @Content(mediaType = "text/plain")
                    ),
                    @ApiResponse(
                            responseCode = "401",
                            description = "Authentication token is missing.",
                            content = @Content(mediaType = "text/plain")
                    ),
                    @ApiResponse(
                            responseCode = "500",
                            description = "Internal Server Error",
                            content = @Content(mediaType = "text/plain")
                    )
            }
    )
    @PostMapping(value = "/{bucket}", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<Map<String, String>> upload(
            @Parameter(
                    description = "Bucket name (avatars, backgrounds)",
                    example = "avatars",
                    required = true
            )
            @PathVariable
            String bucket,
            @Parameter(
                    description = "File to upload",
                    content = @Content(
                            mediaType = "multipart/form-data",
                            schema = @Schema(
                                    type = "string",
                                    format = "binary"
                            )
                    )
            )
            @RequestParam("file")
            MultipartFile file,
            @Parameter(
                    description = "Authorization header with Bearer JWT token",
                    example = "Bearer eyJhbGciOiJIU...",
                    schema = @Schema(type = "string")
            )
            @RequestHeader(value = "Authorization", required = false)
            String authHeader,
            @Parameter(
                    description = "JWT token from Cookie",
                    example = "eyJhbGciOiJIU...",
                    schema = @Schema(type = "string")
            )
            @CookieValue(value = "access_token", required = false)
            String accessTokenCookie,
            @Parameter(description = "HTTP request", hidden = true)
            HttpServletRequest request
    ) throws Exception {
        String token = extractToken(authHeader, accessTokenCookie, request);
        if (token == null) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(Collections.singletonMap("error", "Authentication token is missing"));
        }
        String userId = jwtUtil.validateTokenAndGetUserID(token);

        String filename = minioService.uploadFile(bucket, file, userId);
        Map<String, String> responseBody = Collections.singletonMap("filename", filename);
        return ResponseEntity.ok(responseBody);
    }

    @Operation(
            summary = "Get file",
            description = "Returns a file from the specified bucket.",
            responses = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "File found",
                            content = @Content(mediaType = "image/jpeg")
                    ),
                    @ApiResponse(
                            responseCode = "400",
                            description = "Invalid bucket name",
                            content = @Content(mediaType = "text/plain")
                    ),
                    @ApiResponse(
                            responseCode = "401",
                            description = "Authentication token is missing.",
                            content = @Content(mediaType = "text/plain")),
                    @ApiResponse(
                            responseCode = "404",
                            description = "File not found",
                            content = @Content(mediaType = "text/plain")
                    )
            }
    )
    @GetMapping("/{bucket}/{filename}")
    public ResponseEntity<InputStreamResource> getFile(
            @Parameter(
                    description = "Bucket name (avatars, backgrounds)",
                    example = "avatars",
                    required = true
            )
            @PathVariable
            String bucket,
            @Parameter(description = "Name of the file")
            @PathVariable
            String filename,
            @Parameter(
                    description = "Authorization header with Bearer JWT token",
                    example = "Bearer eyJhbGciOiJIU...",
                    schema = @Schema(type = "string")
            )
            @RequestHeader(value = "Authorization", required = false)
            String authHeader,
            @Parameter(
                    description = "JWT token from Cookie",
                    example = "eyJhbGciOiJIU...",
                    schema = @Schema(type = "string")
            )
            @CookieValue(value = "access_token", required = false)
            String accessTokenCookie,
            @Parameter(description = "HTTP request", hidden = true)
            HttpServletRequest request
    ) throws Exception {
        String token = extractToken(authHeader, accessTokenCookie, request);
        if (token == null) {
            throw new UnauthorizedException("Authentication token is missing");
        }
        String userId = jwtUtil.validateTokenAndGetUserID(token);
        return ResponseEntity.ok()
                .contentType(MediaType.IMAGE_JPEG)
                .body(new InputStreamResource(minioService.getFile(bucket, filename, userId)));
    }

    @Operation(
            summary = "Delete file",
            description = "Deletes a file from the specified bucket. " +
                    "User can delete only his own files. Default files cannot be deleted.",
            responses = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "File deleted",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(
                                            type = "object",
                                            example = "{\\"message\\": \\"File example.jpg deleted from bucket avatars!\\"}"
                                    )
                            )
                    ),
                    @ApiResponse(
                            responseCode = "400",
                            description = "Invalid bucket name",
                            content = @Content(mediaType = "text/plain")
                    ),
                    @ApiResponse(responseCode = "401",
                            description = "Authentication token is missing.",
                            content = @Content(mediaType = "text/plain")),
                    @ApiResponse(responseCode = "403",
                            description = "Access denied - the file belongs to another user or it is a default file",
                            content = @Content(mediaType = "text/plain")),
                    @ApiResponse(
                            responseCode = "404",
                            description = "File not found",
                            content = @Content(mediaType = "text/plain")
                    )
            }
    )
    @DeleteMapping("/{bucket}/{filename}")
    public ResponseEntity<Map<String, String>> delete(
            @Parameter(
                    description = "Bucket name (avatars, backgrounds)",
                    example = "avatars",
                    required = true
            )
            @PathVariable
            String bucket,
            @Parameter(description = "Name of the file")
            @PathVariable
            String filename,
            @Parameter(
                    description = "Authorization header with Bearer JWT token",
                    example = "Bearer eyJhbGciOiJIU...",
                    schema = @Schema(type = "string")
            )
            @RequestHeader(value = "Authorization", required = false)
            String authHeader,
            @Parameter(
                    description = "JWT token from Cookie",
                    example = "eyJhbGciOiJIU...",
                    schema = @Schema(type = "string")
            )
            @CookieValue(value = "access_token", required = false)
            String accessTokenCookie,
            @Parameter(description = "HTTP request", hidden = true)
            HttpServletRequest request
    ) throws Exception {
        String token = extractToken(authHeader, accessTokenCookie, request);
        if (token == null) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(Collections.singletonMap("error", "Authentication token is missing"));
        }
        String userId = jwtUtil.validateTokenAndGetUserID(token);
        minioService.deleteFile(bucket, filename, userId);
        String message = "File " + filename + " deleted from bucket " + bucket + "!";
        Map<String, String> responseBody = Collections.singletonMap("message", message);
        return ResponseEntity.ok(responseBody);
    }
}