package com.hlaff.wallet_api.repository;

import com.hlaff.wallet_api.enums.Currency;
import com.hlaff.wallet_api.model.Wallet;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface WalletRepository extends MongoRepository<Wallet, String> {
    
    Optional<Wallet> findByUserIdAndCurrency(String userId, Currency currency);
}
