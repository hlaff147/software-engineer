package com.hlaff.wallet_api.mapper;

import com.hlaff.wallet_api.dto.LedgerEntryResponse;
import com.hlaff.wallet_api.model.LedgerEntry;
import org.springframework.stereotype.Component;

@Component
public class LedgerEntryMapper {

    /**
     * Model -> DTO Response (mapeamento manual)
     */
    public LedgerEntryResponse toResponse(LedgerEntry ledgerEntry) {
        if (ledgerEntry == null) {
            return null;
        }
        
        return new LedgerEntryResponse(
            ledgerEntry.getId(),
            ledgerEntry.getWalletId(),
            ledgerEntry.getOperation(),
            ledgerEntry.getAmount(),
            ledgerEntry.getOccurredAt(),
            ledgerEntry.getResultingBalance()
        );
    }
}
