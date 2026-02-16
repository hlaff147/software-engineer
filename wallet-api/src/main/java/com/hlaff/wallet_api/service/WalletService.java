package com.hlaff.wallet_api.service;

import com.hlaff.wallet_api.dto.*;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.time.Instant;
import java.util.Map;

public interface WalletService {
    
    WalletResponse createWallet(CreateWalletRequest req);
    
    BalanceResponse getCurrentBalance(String walletId);
    
    BalanceResponse getHistoricalBalance(String walletId, Instant at);
    
    LedgerEntryResponse deposit(String walletId, AmountRequest req);
    
    LedgerEntryResponse withdraw(String walletId, AmountRequest req);
    
    Map<String, Object> transfer(TransferRequest req);
    
    Page<LedgerEntryResponse> listLedger(String walletId, Instant from, Instant to, Pageable pageable);
}
