package com.riveo.minio.service;

import com.riveo.minio.errorHandler.UnauthorizedException;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.io.Decoders;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;

@Service
public class JwtUtil {
    @Value("${SECRET_KEY}")
    private String secretKey;

    private SecretKey getKey() {
//        byte[] keyBytes = Decoders.BASE64.decode(secretKey);
        byte[] keybytes = secretKey.getBytes(StandardCharsets.UTF_8);
        // System.out.println(Keys.hmacShaKeyFor(keybytes).getAlgorithm()); // Removed debug print
        // System.out.println(Keys.hmacShaKeyFor(keybytes)); // Removed debug print
        return Keys.hmacShaKeyFor(keybytes);
    }

    public String validateTokenAndGetUserID(String token){
        // System.out.println(secretKey);
        // System.out.println(getKey().toString());
        try{
            Claims claims = Jwts.parser()
                    .verifyWith(getKey())
                    .build()
                    .parseSignedClaims(token)
                    .getPayload();
                    
            Integer userId = claims.get("id", Integer.class);
            if (userId == null) {
                throw new UnauthorizedException("Invalid token: User ID (id) claim is missing.");
            }
            return userId.toString();
        } catch (Exception e){
            throw new UnauthorizedException("Invalid token. " + e.getMessage());
        }
    }
}
