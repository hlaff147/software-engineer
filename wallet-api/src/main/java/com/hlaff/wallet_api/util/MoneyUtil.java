package com.hlaff.wallet_api.util;

import java.math.BigDecimal;
import java.math.RoundingMode;

public class MoneyUtil {
    
    private static final int CENTS_SCALE = 2;
    private static final int CENTS_MULTIPLIER = 100;
    
    /**
     * Converte valor em centavos para BigDecimal
     */
    public static BigDecimal centsToBigDecimal(long cents) {
        return BigDecimal.valueOf(cents)
                .divide(BigDecimal.valueOf(CENTS_MULTIPLIER), CENTS_SCALE, RoundingMode.HALF_EVEN);
    }
    
    /**
     * Converte BigDecimal para centavos
     */
    public static long bigDecimalToCents(BigDecimal amount) {
        if (amount == null) {
            return 0L;
        }
        return amount.multiply(BigDecimal.valueOf(CENTS_MULTIPLIER))
                .setScale(0, RoundingMode.HALF_EVEN)
                .longValue();
    }
    
    /**
     * Valida se o valor em centavos é positivo
     */
    public static boolean isPositive(long cents) {
        return cents > 0;
    }
    
    /**
     * Valida se o valor em centavos não é negativo
     */
    public static boolean isNonNegative(long cents) {
        return cents >= 0;
    }
}
