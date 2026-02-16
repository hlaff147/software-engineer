package com.hlaff.wallet_api.mapper;

import com.hlaff.wallet_api.dto.BalanceResponse;
import com.hlaff.wallet_api.model.Wallet;
import org.springframework.stereotype.Component;

import java.time.Instant;

@Component
public class BalanceMapper {
    
    /**
     * Wallet + timestamp -> BalanceResponse
     */
    public BalanceResponse toCurrentBalance(Wallet wallet, Instant asOf) {
        if (wallet == null) {
            return null;
        }
        
        return new BalanceResponse(
            wallet.getId(),
            wallet.getCurrency(),
            wallet.getBalance(),
            asOf
        );
    }
    
    /**
     * Wallet -> BalanceResponse com timestamp atual
     */
    public BalanceResponse toCurrentBalance(Wallet wallet) {
        return toCurrentBalance(wallet, Instant.now());
    }
}
