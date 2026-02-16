package com.hlaff.wallet_api.mapper;

import com.hlaff.wallet_api.dto.CreateWalletRequest;
import com.hlaff.wallet_api.dto.WalletResponse;
import com.hlaff.wallet_api.enums.Currency;
import com.hlaff.wallet_api.enums.WalletStatus;
import com.hlaff.wallet_api.model.Wallet;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import java.time.Instant;

import static org.assertj.core.api.Assertions.*;

@DisplayName("WalletMapper Tests")
class WalletMapperTest {

    private final WalletMapper walletMapper = new WalletMapper();

    @Test
    @DisplayName("Deve mapear CreateWalletRequest para Wallet")
    void shouldMapCreateWalletRequestToWallet() {
        // Given
        CreateWalletRequest request = new CreateWalletRequest("user-123", Currency.BRL);

        // When
        Wallet wallet = walletMapper.toModel(request);

        // Then
        assertThat(wallet).isNotNull();
        assertThat(wallet.getUserId()).isEqualTo("user-123");
        assertThat(wallet.getCurrency()).isEqualTo(Currency.BRL);
        
        // Campos ignorados devem ser null
        assertThat(wallet.getId()).isNull();
        assertThat(wallet.getStatus()).isNull();
        assertThat(wallet.getBalance()).isNull();
        assertThat(wallet.getCreatedAt()).isNull();
        assertThat(wallet.getUpdatedAt()).isNull();
    }

    @Test
    @DisplayName("Deve mapear CreateWalletRequest com currency USD")
    void shouldMapCreateWalletRequestWithUSD() {
        // Given
        CreateWalletRequest request = new CreateWalletRequest("user-456", Currency.USD);

        // When
        Wallet wallet = walletMapper.toModel(request);

        // Then
        assertThat(wallet).isNotNull();
        assertThat(wallet.getUserId()).isEqualTo("user-456");
        assertThat(wallet.getCurrency()).isEqualTo(Currency.USD);
    }

    @Test
    @DisplayName("Deve mapear Wallet para WalletResponse")
    void shouldMapWalletToWalletResponse() {
        // Given
        Wallet wallet = new Wallet();
        wallet.setId("wallet-123");
        wallet.setUserId("user-789");
        wallet.setCurrency(Currency.EUR);
        wallet.setStatus(WalletStatus.ACTIVE);
        wallet.setBalance(15000L);
        wallet.setCreatedAt(Instant.parse("2024-01-15T10:00:00Z"));
        wallet.setUpdatedAt(Instant.parse("2024-01-15T11:00:00Z"));

        // When
        WalletResponse response = walletMapper.toResponse(wallet);

        // Then
        assertThat(response).isNotNull();
        assertThat(response.id()).isEqualTo("wallet-123");
        assertThat(response.userId()).isEqualTo("user-789");
        assertThat(response.currency()).isEqualTo(Currency.EUR);
        assertThat(response.status()).isEqualTo(WalletStatus.ACTIVE);
        assertThat(response.balance()).isEqualTo(15000L);
    }

    @Test
    @DisplayName("Deve mapear Wallet com status BLOCKED")
    void shouldMapWalletWithBlockedStatus() {
        // Given
        Wallet wallet = new Wallet();
        wallet.setId("wallet-456");
        wallet.setUserId("user-blocked");
        wallet.setCurrency(Currency.BRL);
        wallet.setStatus(WalletStatus.BLOCKED);
        wallet.setBalance(0L);

        // When
        WalletResponse response = walletMapper.toResponse(wallet);

        // Then
        assertThat(response).isNotNull();
        assertThat(response.id()).isEqualTo("wallet-456");
        assertThat(response.userId()).isEqualTo("user-blocked");
        assertThat(response.status()).isEqualTo(WalletStatus.BLOCKED);
        assertThat(response.balance()).isEqualTo(0L);
    }

    @Test
    @DisplayName("Deve preservar todas as currencies na conversão")
    void shouldPreserveAllCurrenciesInConversion() {
        // Given & When & Then
        for (Currency currency : Currency.values()) {
            CreateWalletRequest request = new CreateWalletRequest("user-test", currency);
            Wallet wallet = walletMapper.toModel(request);
            
            assertThat(wallet.getCurrency()).isEqualTo(currency);
        }
    }

    @Test
    @DisplayName("Deve preservar todos os status na conversão")
    void shouldPreserveAllStatusInConversion() {
        // Given & When & Then
        for (WalletStatus status : WalletStatus.values()) {
            Wallet wallet = new Wallet();
            wallet.setId("wallet-test");
            wallet.setUserId("user-test");
            wallet.setCurrency(Currency.BRL);
            wallet.setStatus(status);
            wallet.setBalance(1000L);
            
            WalletResponse response = walletMapper.toResponse(wallet);
            
            assertThat(response.status()).isEqualTo(status);
        }
    }
}
