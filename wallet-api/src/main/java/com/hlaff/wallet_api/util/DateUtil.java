package com.hlaff.wallet_api.util;

import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;

public class DateUtil {
    
    private static final DateTimeFormatter DEFAULT_FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
    private static final ZoneId DEFAULT_ZONE = ZoneId.of("America/Sao_Paulo");
    
    public static String formatInstant(Instant instant) {
        if (instant == null) {
            return null;
        }
        return LocalDateTime.ofInstant(instant, DEFAULT_ZONE)
                .format(DEFAULT_FORMATTER);
    }
    
    public static Instant parseToInstant(String dateTime) {
        if (dateTime == null || dateTime.trim().isEmpty()) {
            return null;
        }
        return LocalDateTime.parse(dateTime, DEFAULT_FORMATTER)
                .atZone(DEFAULT_ZONE)
                .toInstant();
    }
    
    public static Instant now() {
        return Instant.now();
    }
}
