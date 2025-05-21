package com.riveo.minio.service;

import com.riveo.minio.errorHandler.AccessDeniedException;
import com.riveo.minio.errorHandler.FileNotFoundException;
import io.minio.*;
import io.minio.errors.ErrorResponseException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.InputStream;
import java.util.*;

@Service
public class MinioService {

    @Autowired
    private MinioClient minioClient;

    @Value("${DEFAULT_BACKGROUND}")
    private String defaultBackground;
    @Value("${DEFAULT_AVATAR}")
    private String defaultAvatar;
    private static final Set<String> ALLOWED_BUCKETS = new HashSet<>(Arrays.asList("avatars", "backgrounds"));

    public String generateFileName(String originalName) {
        String extension = "";

        if (originalName != null && originalName.contains(".")) {
            extension = originalName.substring(originalName.lastIndexOf("."));
        }

        return UUID.randomUUID().toString() + extension;
    }

    public String uploadFile(String bucket, MultipartFile file, String userId) throws Exception {
        return uploadFile(bucket, file, userId, null);
    }

    public String uploadFile(String bucket, MultipartFile file, String userId, String roadmap_id) throws Exception {
        validateBucket(bucket);
        
        boolean found = minioClient.bucketExists(BucketExistsArgs.builder()
                .bucket(bucket).build());
        
        if (!found) {
            minioClient.makeBucket(MakeBucketArgs.builder()
                    .bucket(bucket).build());
        }
        
        String originalName = file.getOriginalFilename();
        String generatedName = generateFileName(originalName);

        Map<String, String> imageTags = new HashMap<String, String>();
        imageTags.put("user_id", userId);
        if ("backgrounds".equals(bucket) && roadmap_id != null){
            imageTags.put("roadmap_id", roadmap_id);
        }

        minioClient.putObject(
                PutObjectArgs.builder()
                        .bucket(bucket)
                        .object(generatedName)
                        .stream(file.getInputStream(), file.getSize(), -1)
                        .contentType(file.getContentType())
                        .tags(imageTags)
                        .build()
        );
        return generatedName;
    }

    public boolean isFileOwnedByUser(String bucket, String filename, String userId) throws Exception {
        try {
            Map<String, String> tags = minioClient.getObjectTags(
                    GetObjectTagsArgs.builder()
                            .bucket(bucket)
                            .object(filename)
                            .build()
            ).get();

            return userId.equals(tags.get("user_id"));
        } catch (ErrorResponseException e) {
            if (e.errorResponse().code().equals("NoSuchKey")) {
                throw new FileNotFoundException("File '" + filename + "' not found in bucket '" + bucket + "'");
            }
            throw e;
        }
    }

    public InputStream getFile(String bucket, String filename, String userId) throws Exception {
        validateBucket(bucket);

        if (!isFileOwnedByUser(bucket, filename, userId) && "backgrounds".equals(bucket) && !filename.equals(defaultBackground)) {
            throw new AccessDeniedException("Access denied to file '" + filename + "' in bucket '" + bucket + "'");
        }

        try {
            return minioClient.getObject(
                    GetObjectArgs.builder()
                            .bucket(bucket)
                            .object(filename)
                            .build()
            );
        } catch (ErrorResponseException e) {
            if (e.errorResponse().code().equals("NoSuchKey")) {
                throw new FileNotFoundException("File '" + filename + "' not found in bucket '" + bucket + "'");
            }
            throw e;
        }
    }

    public void  deleteFile(String bucket, String filename, String userId) throws Exception {
        validateBucket(bucket);

        if (("avatars".equals(bucket) && defaultAvatar.equals(filename)) || ("backgrounds".equals(bucket) && defaultBackground.equals(filename))){
            return;
        }

        if (!isFileOwnedByUser(bucket, filename, userId)) {
            throw new AccessDeniedException("Access denied to file '" + filename + "' in bucket '" + bucket + "'");
        }

        try {
            minioClient.statObject(
                    StatObjectArgs.builder()
                            .bucket(bucket)
                            .object(filename)
                            .build()
            );

            minioClient.removeObject(
                    RemoveObjectArgs.builder()
                            .bucket(bucket)
                            .object(filename)
                            .build()
            );
        } catch (ErrorResponseException e) {
            if (e.errorResponse().code().equals("NoSuchKey")) {
                throw new FileNotFoundException("File '" + filename + "' not found in bucket '" + bucket + "'");
            }
            throw new RuntimeException("Error deleting file", e);
        }
    }

    private void validateBucket(String bucket) {
        if (!ALLOWED_BUCKETS.contains(bucket)) {
            throw new IllegalArgumentException("Invalid bucket name. Allowed buckets are: " + ALLOWED_BUCKETS);
        }
    }
}