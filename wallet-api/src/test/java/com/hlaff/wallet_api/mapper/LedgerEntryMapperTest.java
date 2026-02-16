package com.hlaff.wallet_api.mapper;

import com.hlaff.wallet_api.dto.LedgerEntryResponse;
import com.hlaff.wallet_api.enums.OperationType;
import com.hlaff.wallet_api.model.LedgerEntry;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import java.time.Instant;
import java.util.Map;

import static org.assertj.core.api.Assertions.*;

@DisplayName("LedgerEntryMapper Tests")
class LedgerEntryMapperTest {

    private final LedgerEntryMapper ledgerEntryMapper = new LedgerEntryMapper();

    @Test
    @DisplayName("Deve mapear LedgerEntry para LedgerEntryResponse")
    void shouldMapLedgerEntryToResponse() {
        // Given
        LedgerEntry ledgerEntry = new LedgerEntry();
        ledgerEntry.setId("entry-123");
        ledgerEntry.setWalletId("wallet-456");
        ledgerEntry.setTransferId("transfer-789");
        ledgerEntry.setOperation(OperationType.DEPOSIT);
        ledgerEntry.setAmount(10000L);
        ledgerEntry.setOccurredAt(Instant.parse("2024-01-15T10:30:00Z"));
        ledgerEntry.setResultingBalance(25000L);
        ledgerEntry.setMetadata(Map.of("source", "PIX", "description", "Depósito via PIX"));

        // When
        LedgerEntryResponse response = ledgerEntryMapper.toResponse(ledgerEntry);

        // Then
        assertThat(response).isNotNull();
        assertThat(response.id()).isEqualTo("entry-123");
        assertThat(response.walletId()).isEqualTo("wallet-456");
        assertThat(response.operation()).isEqualTo(OperationType.DEPOSIT);
        assertThat(response.amount()).isEqualTo(10000L);
        assertThat(response.occurredAt()).isEqualTo(Instant.parse("2024-01-15T10:30:00Z"));
        assertThat(response.resultingBalance()).isEqualTo(25000L);
    }

    @Test
    @DisplayName("Deve mapear LedgerEntry de saque")
    void shouldMapWithdrawLedgerEntry() {
        // Given
        LedgerEntry ledgerEntry = new LedgerEntry();
        ledgerEntry.setId("entry-withdraw");
        ledgerEntry.setWalletId("wallet-789");
        ledgerEntry.setOperation(OperationType.WITHDRAW);
        ledgerEntry.setAmount(5000L);
        ledgerEntry.setOccurredAt(Instant.parse("2024-01-15T11:00:00Z"));
        ledgerEntry.setResultingBalance(15000L);
        ledgerEntry.setMetadata(Map.of("method", "TED"));

        // When
        LedgerEntryResponse response = ledgerEntryMapper.toResponse(ledgerEntry);

        // Then
        assertThat(response).isNotNull();
        assertThat(response.id()).isEqualTo("entry-withdraw");
        assertThat(response.walletId()).isEqualTo("wallet-789");
        assertThat(response.operation()).isEqualTo(OperationType.WITHDRAW);
        assertThat(response.amount()).isEqualTo(5000L);
        assertThat(response.resultingBalance()).isEqualTo(15000L);
    }

    @Test
    @DisplayName("Deve mapear LedgerEntry de transferência débito")
    void shouldMapTransferDebitLedgerEntry() {
        // Given
        LedgerEntry ledgerEntry = new LedgerEntry();
        ledgerEntry.setId("entry-debit");
        ledgerEntry.setWalletId("wallet-from");
        ledgerEntry.setTransferId("transfer-123");
        ledgerEntry.setOperation(OperationType.TRANSFER_DEBIT);
        ledgerEntry.setAmount(3000L);
        ledgerEntry.setOccurredAt(Instant.parse("2024-01-15T12:00:00Z"));
        ledgerEntry.setResultingBalance(7000L);
        ledgerEntry.setMetadata(Map.of("type", "payment", "recipient", "user-456"));

        // When
        LedgerEntryResponse response = ledgerEntryMapper.toResponse(ledgerEntry);

        // Then
        assertThat(response).isNotNull();
        assertThat(response.operation()).isEqualTo(OperationType.TRANSFER_DEBIT);
        assertThat(response.amount()).isEqualTo(3000L);
        assertThat(response.resultingBalance()).isEqualTo(7000L);
    }

    @Test
    @DisplayName("Deve mapear LedgerEntry de transferência crédito")
    void shouldMapTransferCreditLedgerEntry() {
        // Given
        LedgerEntry ledgerEntry = new LedgerEntry();
        ledgerEntry.setId("entry-credit");
        ledgerEntry.setWalletId("wallet-to");
        ledgerEntry.setTransferId("transfer-123");
        ledgerEntry.setOperation(OperationType.TRANSFER_CREDIT);
        ledgerEntry.setAmount(3000L);
        ledgerEntry.setOccurredAt(Instant.parse("2024-01-15T12:00:00Z"));
        ledgerEntry.setResultingBalance(13000L);
        ledgerEntry.setMetadata(Map.of("type", "received", "sender", "user-123"));

        // When
        LedgerEntryResponse response = ledgerEntryMapper.toResponse(ledgerEntry);

        // Then
        assertThat(response).isNotNull();
        assertThat(response.operation()).isEqualTo(OperationType.TRANSFER_CREDIT);
        assertThat(response.amount()).isEqualTo(3000L);
        assertThat(response.resultingBalance()).isEqualTo(13000L);
    }

    @Test
    @DisplayName("Deve mapear LedgerEntry com valores mínimos")
    void shouldMapLedgerEntryWithMinimalValues() {
        // Given
        LedgerEntry ledgerEntry = new LedgerEntry();
        ledgerEntry.setId("entry-minimal");
        ledgerEntry.setWalletId("wallet-minimal");
        ledgerEntry.setOperation(OperationType.DEPOSIT);
        ledgerEntry.setAmount(1L);
        ledgerEntry.setOccurredAt(Instant.parse("2024-01-01T00:00:00Z"));
        ledgerEntry.setResultingBalance(1L);

        // When
        LedgerEntryResponse response = ledgerEntryMapper.toResponse(ledgerEntry);

        // Then
        assertThat(response).isNotNull();
        assertThat(response.id()).isEqualTo("entry-minimal");
        assertThat(response.walletId()).isEqualTo("wallet-minimal");
        assertThat(response.operation()).isEqualTo(OperationType.DEPOSIT);
        assertThat(response.amount()).isEqualTo(1L);
        assertThat(response.resultingBalance()).isEqualTo(1L);
    }

    @Test
    @DisplayName("Deve preservar todas as operações na conversão")
    void shouldPreserveAllOperationTypesInConversion() {
        // Given & When & Then
        for (OperationType operation : OperationType.values()) {
            LedgerEntry ledgerEntry = new LedgerEntry();
            ledgerEntry.setId("entry-" + operation.name());
            ledgerEntry.setWalletId("wallet-test");
            ledgerEntry.setOperation(operation);
            ledgerEntry.setAmount(1000L);
            ledgerEntry.setOccurredAt(Instant.now());
            ledgerEntry.setResultingBalance(5000L);
            
            LedgerEntryResponse response = ledgerEntryMapper.toResponse(ledgerEntry);
            
            assertThat(response.operation()).isEqualTo(operation);
        }
    }
}
