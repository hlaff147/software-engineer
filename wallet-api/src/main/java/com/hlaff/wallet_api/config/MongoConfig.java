package com.hlaff.wallet_api.config;

import com.hlaff.wallet_api.repository.WalletRepository;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;

@Configuration
@EnableMongoRepositories(basePackageClasses = WalletRepository.class)
public class MongoConfig {
}
