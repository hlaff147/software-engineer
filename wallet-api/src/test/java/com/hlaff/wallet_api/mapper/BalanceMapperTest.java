package com.hlaff.wallet_api.mapper;

import com.hlaff.wallet_api.dto.BalanceResponse;
import com.hlaff.wallet_api.enums.Currency;
import com.hlaff.wallet_api.enums.WalletStatus;
import com.hlaff.wallet_api.model.Wallet;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import java.time.Instant;

import static org.assertj.core.api.Assertions.*;

@DisplayName("BalanceMapper Tests")
class BalanceMapperTest {

    private final BalanceMapper balanceMapper = new BalanceMapper();

    @Test
    @DisplayName("Deve mapear Wallet para BalanceResponse com timestamp específico")
    void shouldMapWalletToBalanceResponseWithSpecificTimestamp() {
        // Given
        Wallet wallet = new Wallet();
        wallet.setId("wallet-123");
        wallet.setUserId("user-456");
        wallet.setCurrency(Currency.BRL);
        wallet.setStatus(WalletStatus.ACTIVE);
        wallet.setBalance(25000L);
        wallet.setCreatedAt(Instant.parse("2024-01-15T10:00:00Z"));
        wallet.setUpdatedAt(Instant.parse("2024-01-15T11:00:00Z"));

        Instant asOf = Instant.parse("2024-01-15T12:00:00Z");

        // When
        BalanceResponse response = balanceMapper.toCurrentBalance(wallet, asOf);

        // Then
        assertThat(response).isNotNull();
        assertThat(response.id()).isEqualTo("wallet-123");
        assertThat(response.currency()).isEqualTo(Currency.BRL);
        assertThat(response.balance()).isEqualTo(25000L);
        assertThat(response.asOf()).isEqualTo(asOf);
    }

    @Test
    @DisplayName("Deve mapear Wallet para BalanceResponse com timestamp atual")
    void shouldMapWalletToBalanceResponseWithCurrentTimestamp() {
        // Given
        Wallet wallet = new Wallet();
        wallet.setId("wallet-789");
        wallet.setUserId("user-123");
        wallet.setCurrency(Currency.USD);
        wallet.setStatus(WalletStatus.ACTIVE);
        wallet.setBalance(15000L);

        Instant beforeCall = Instant.now();

        // When
        BalanceResponse response = balanceMapper.toCurrentBalance(wallet);

        // Then
        Instant afterCall = Instant.now();
        
        assertThat(response).isNotNull();
        assertThat(response.id()).isEqualTo("wallet-789");
        assertThat(response.currency()).isEqualTo(Currency.USD);
        assertThat(response.balance()).isEqualTo(15000L);
        assertThat(response.asOf()).isBetween(beforeCall, afterCall);
    }

    @Test
    @DisplayName("Deve mapear Wallet com balance zero")
    void shouldMapWalletWithZeroBalance() {
        // Given
        Wallet wallet = new Wallet();
        wallet.setId("wallet-empty");
        wallet.setUserId("user-empty");
        wallet.setCurrency(Currency.EUR);
        wallet.setStatus(WalletStatus.ACTIVE);
        wallet.setBalance(0L);

        Instant asOf = Instant.parse("2024-01-01T00:00:00Z");

        // When
        BalanceResponse response = balanceMapper.toCurrentBalance(wallet, asOf);

        // Then
        assertThat(response).isNotNull();
        assertThat(response.id()).isEqualTo("wallet-empty");
        assertThat(response.currency()).isEqualTo(Currency.EUR);
        assertThat(response.balance()).isEqualTo(0L);
        assertThat(response.asOf()).isEqualTo(asOf);
    }

    @Test
    @DisplayName("Deve mapear Wallet com balance alto")
    void shouldMapWalletWithHighBalance() {
        // Given
        Wallet wallet = new Wallet();
        wallet.setId("wallet-rich");
        wallet.setUserId("user-rich");
        wallet.setCurrency(Currency.BRL);
        wallet.setStatus(WalletStatus.ACTIVE);
        wallet.setBalance(999999999L); // 9.999.999,99 BRL em centavos

        Instant asOf = Instant.parse("2024-12-31T23:59:59Z");

        // When
        BalanceResponse response = balanceMapper.toCurrentBalance(wallet, asOf);

        // Then
        assertThat(response).isNotNull();
        assertThat(response.id()).isEqualTo("wallet-rich");
        assertThat(response.currency()).isEqualTo(Currency.BRL);
        assertThat(response.balance()).isEqualTo(999999999L);
        assertThat(response.asOf()).isEqualTo(asOf);
    }

    @Test
    @DisplayName("Deve preservar todas as currencies na conversão")
    void shouldPreserveAllCurrenciesInConversion() {
        // Given & When & Then
        for (Currency currency : Currency.values()) {
            Wallet wallet = new Wallet();
            wallet.setId("wallet-" + currency.name());
            wallet.setUserId("user-test");
            wallet.setCurrency(currency);
            wallet.setStatus(WalletStatus.ACTIVE);
            wallet.setBalance(10000L);

            Instant asOf = Instant.now();
            BalanceResponse response = balanceMapper.toCurrentBalance(wallet, asOf);
            
            assertThat(response.currency()).isEqualTo(currency);
        }
    }

    @Test
    @DisplayName("Deve manter precisão de timestamp")
    void shouldMaintainTimestampPrecision() {
        // Given
        Wallet wallet = new Wallet();
        wallet.setId("wallet-precision");
        wallet.setUserId("user-precision");
        wallet.setCurrency(Currency.BRL);
        wallet.setStatus(WalletStatus.ACTIVE);
        wallet.setBalance(12345L);

        // Timestamp com nanossegundos
        Instant preciseTiming = Instant.parse("2024-01-15T12:30:45.123456789Z");

        // When
        BalanceResponse response = balanceMapper.toCurrentBalance(wallet, preciseTiming);

        // Then
        assertThat(response.asOf()).isEqualTo(preciseTiming);
        assertThat(response.asOf().getNano()).isEqualTo(123456789);
    }
}
