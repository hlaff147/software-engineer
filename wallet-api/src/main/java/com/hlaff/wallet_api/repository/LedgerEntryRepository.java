package com.hlaff.wallet_api.repository;

import com.hlaff.wallet_api.model.LedgerEntry;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.time.Instant;
import java.util.List;

@Repository
public interface LedgerEntryRepository extends MongoRepository<LedgerEntry, String> {
    
    Page<LedgerEntry> findByWalletIdAndOccurredAtBetween(
            String walletId, 
            Instant from, 
            Instant to, 
            Pageable pageable
    );
    
    List<LedgerEntry> findByWalletIdAndOccurredAtLessThanEqual(
            String walletId, 
            Instant at
    );
    
    List<LedgerEntry> findByWalletIdOrderByOccurredAtDesc(String walletId);
}
