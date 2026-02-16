package com.hlaff.wallet_api.model;

import com.hlaff.wallet_api.enums.OperationType;
import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.CompoundIndex;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.Instant;
import java.util.Map;

@Data
@Document("ledger_entries")
@CompoundIndex(def = "{'walletId': 1, 'occurredAt': -1}")
public class LedgerEntry {
    
    @Id
    private String id;
    
    private String walletId;
    
    private String transferId;        // opcional
    
    private OperationType operation;
    
    private Long amount;              // centavos (>=0)
    
    private Instant occurredAt;
    
    private Long resultingBalance;    // saldo após a operação
    
    private Map<String, String> metadata;
}
