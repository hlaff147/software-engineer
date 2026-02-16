package com.hlaff.wallet_api.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.hlaff.wallet_api.dto.AmountRequest;
import com.hlaff.wallet_api.dto.LedgerEntryResponse;
import com.hlaff.wallet_api.dto.TransferRequest;
import com.hlaff.wallet_api.enums.OperationType;
import com.hlaff.wallet_api.exception.InsufficientFundsException;
import com.hlaff.wallet_api.exception.NotFoundException;
import com.hlaff.wallet_api.service.WalletService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.time.Instant;
import java.util.Map;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(TransferController.class)
@DisplayName("TransferController Tests")
class TransferControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockitoBean
    private WalletService walletService;

    @Test
    @DisplayName("Deve realizar depósito com sucesso")
    void shouldDepositSuccessfully() throws Exception {
        // Given
        AmountRequest request = new AmountRequest(5000L, Map.of("source", "PIX"));
        LedgerEntryResponse response = new LedgerEntryResponse(
            "ledger-123", "wallet-123", OperationType.DEPOSIT, 5000L, 
            Instant.parse("2024-01-15T10:30:00Z"), 15000L
        );

        when(walletService.deposit(eq("wallet-123"), any(AmountRequest.class)))
            .thenReturn(response);

        // When & Then
        mockMvc.perform(post("/api/v1/wallets/wallet-123/deposit")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value("ledger-123"))
                .andExpect(jsonPath("$.walletId").value("wallet-123"))
                .andExpect(jsonPath("$.operation").value("DEPOSIT"))
                .andExpect(jsonPath("$.amount").value(5000))
                .andExpect(jsonPath("$.resultingBalance").value(15000));
    }

    @Test
    @DisplayName("Deve retornar erro 400 ao depositar valor inválido")
    void shouldReturn400WhenDepositingInvalidAmount() throws Exception {
        // Given
        AmountRequest invalidRequest = new AmountRequest(-1000L, Map.of());

        // When & Then
        mockMvc.perform(post("/api/v1/wallets/wallet-123/deposit")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(invalidRequest)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.title").value("Validation error"));
    }

    @Test
    @DisplayName("Deve realizar saque com sucesso")
    void shouldWithdrawSuccessfully() throws Exception {
        // Given
        AmountRequest request = new AmountRequest(3000L, Map.of("method", "TED"));
        LedgerEntryResponse response = new LedgerEntryResponse(
            "ledger-456", "wallet-123", OperationType.WITHDRAW, 3000L,
            Instant.parse("2024-01-15T10:35:00Z"), 7000L
        );

        when(walletService.withdraw(eq("wallet-123"), any(AmountRequest.class)))
            .thenReturn(response);

        // When & Then
        mockMvc.perform(post("/api/v1/wallets/wallet-123/withdraw")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value("ledger-456"))
                .andExpect(jsonPath("$.walletId").value("wallet-123"))
                .andExpect(jsonPath("$.operation").value("WITHDRAW"))
                .andExpect(jsonPath("$.amount").value(3000))
                .andExpect(jsonPath("$.resultingBalance").value(7000));
    }

    @Test
    @DisplayName("Deve retornar erro 409 ao sacar com saldo insuficiente")
    void shouldReturn409WhenInsufficientFunds() throws Exception {
        // Given
        AmountRequest request = new AmountRequest(20000L, Map.of());

        when(walletService.withdraw(eq("wallet-123"), any(AmountRequest.class)))
            .thenThrow(new InsufficientFundsException("Saldo insuficiente para realizar o saque"));

        // When & Then
        mockMvc.perform(post("/api/v1/wallets/wallet-123/withdraw")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isConflict())
                .andExpect(jsonPath("$.title").value("Insufficient funds"))
                .andExpect(jsonPath("$.detail").value("Saldo insuficiente para realizar o saque"));
    }

    @Test
    @DisplayName("Deve retornar erro 404 ao operar em carteira inexistente")
    void shouldReturn404WhenWalletNotFoundForDeposit() throws Exception {
        // Given
        AmountRequest request = new AmountRequest(5000L, Map.of());

        when(walletService.deposit(eq("non-existent"), any(AmountRequest.class)))
            .thenThrow(new NotFoundException("Carteira não encontrada"));

        // When & Then
        mockMvc.perform(post("/api/v1/wallets/non-existent/deposit")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.title").value("Not Found"))
                .andExpect(jsonPath("$.detail").value("Carteira não encontrada"));
    }

    @Test
    @DisplayName("Deve realizar transferência com sucesso")
    void shouldTransferSuccessfully() throws Exception {
        // Given
        TransferRequest request = new TransferRequest(
            "wallet-123", "wallet-456", 5000L, Map.of("type", "payment")
        );

        Map<String, Object> response = Map.of(
            "transferId", "txn-123",
            "fromWallet", Map.of("id", "wallet-123", "newBalance", 5000L),
            "toWallet", Map.of("id", "wallet-456", "newBalance", 15000L),
            "debitEntry", Map.of("id", "debit-123", "operation", "TRANSFER_DEBIT"),
            "creditEntry", Map.of("id", "credit-123", "operation", "TRANSFER_CREDIT")
        );

        when(walletService.transfer(any(TransferRequest.class)))
            .thenReturn(response);

        // When & Then
        mockMvc.perform(post("/api/v1/transfers")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.transferId").value("txn-123"))
                .andExpect(jsonPath("$.fromWallet.id").value("wallet-123"))
                .andExpect(jsonPath("$.fromWallet.newBalance").value(5000))
                .andExpect(jsonPath("$.toWallet.id").value("wallet-456"))
                .andExpect(jsonPath("$.toWallet.newBalance").value(15000));
    }

    @Test
    @DisplayName("Deve retornar erro 400 ao transferir dados inválidos")
    void shouldReturn400WhenTransferringInvalidData() throws Exception {
        // Given
        TransferRequest invalidRequest = new TransferRequest(
            "", "", -1000L, Map.of()
        );

        // When & Then
        mockMvc.perform(post("/api/v1/transfers")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(invalidRequest)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.title").value("Validation error"));
    }
}
