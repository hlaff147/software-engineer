package com.hlaff.wallet_api.model;

import com.hlaff.wallet_api.enums.Currency;
import com.hlaff.wallet_api.enums.WalletStatus;
import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.CompoundIndex;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.Instant;

@Data
@Document("wallets")
@CompoundIndex(def = "{'userId': 1, 'currency': 1}", unique = true)
public class Wallet {
    
    @Id
    private String id;
    
    private String userId;
    
    private Currency currency;
    
    private Long balance;             // em centavos
    
    private WalletStatus status;
    
    private Instant createdAt;
    
    private Instant updatedAt;
}
