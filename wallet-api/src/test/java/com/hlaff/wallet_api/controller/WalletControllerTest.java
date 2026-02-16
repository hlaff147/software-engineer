package com.hlaff.wallet_api.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.hlaff.wallet_api.dto.BalanceResponse;
import com.hlaff.wallet_api.dto.CreateWalletRequest;
import com.hlaff.wallet_api.dto.WalletResponse;
import com.hlaff.wallet_api.enums.Currency;
import com.hlaff.wallet_api.enums.WalletStatus;
import com.hlaff.wallet_api.exception.BusinessException;
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

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(WalletController.class)
@DisplayName("WalletController Tests")
class WalletControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockitoBean
    private WalletService walletService;

    @Test
    @DisplayName("Deve criar carteira com sucesso")
    void shouldCreateWalletSuccessfully() throws Exception {
        // Given
        CreateWalletRequest request = new CreateWalletRequest("user-123", Currency.BRL);
        WalletResponse response = new WalletResponse(
            "wallet-123", "user-123", Currency.BRL, WalletStatus.ACTIVE, 0L
        );

        when(walletService.createWallet(any(CreateWalletRequest.class)))
            .thenReturn(response);

        // When & Then
        mockMvc.perform(post("/api/v1/wallets")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").value("wallet-123"))
                .andExpect(jsonPath("$.userId").value("user-123"))
                .andExpect(jsonPath("$.currency").value("BRL"))
                .andExpect(jsonPath("$.status").value("ACTIVE"))
                .andExpect(jsonPath("$.balance").value(0));
    }

    @Test
    @DisplayName("Deve retornar erro 400 ao criar carteira com dados inválidos")
    void shouldReturn400WhenCreatingWalletWithInvalidData() throws Exception {
        // Given
        CreateWalletRequest invalidRequest = new CreateWalletRequest("", null);

        // When & Then
        mockMvc.perform(post("/api/v1/wallets")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(invalidRequest)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.title").value("Validation error"));
    }

    @Test
    @DisplayName("Deve retornar erro 400 ao criar carteira duplicada")
    void shouldReturn400WhenCreatingDuplicateWallet() throws Exception {
        // Given
        CreateWalletRequest request = new CreateWalletRequest("user-123", Currency.BRL);
        
        when(walletService.createWallet(any(CreateWalletRequest.class)))
            .thenThrow(new BusinessException("Carteira já existe para este usuário e moeda"));

        // When & Then
        mockMvc.perform(post("/api/v1/wallets")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.title").value("Business Error"))
                .andExpect(jsonPath("$.detail").value("Carteira já existe para este usuário e moeda"));
    }

    @Test
    @DisplayName("Deve consultar saldo atual com sucesso")
    void shouldGetCurrentBalanceSuccessfully() throws Exception {
        // Given
        BalanceResponse response = new BalanceResponse(
            "wallet-123", Currency.BRL, 15000L, Instant.parse("2024-01-15T10:30:00Z")
        );

        when(walletService.getCurrentBalance("wallet-123"))
            .thenReturn(response);

        // When & Then
        mockMvc.perform(get("/api/v1/wallets/wallet-123/balance"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value("wallet-123"))
                .andExpect(jsonPath("$.currency").value("BRL"))
                .andExpect(jsonPath("$.balance").value(15000))
                .andExpect(jsonPath("$.asOf").value("2024-01-15T10:30:00Z"));
    }

    @Test
    @DisplayName("Deve retornar erro 404 ao consultar carteira inexistente")
    void shouldReturn404WhenWalletNotFound() throws Exception {
        // Given
        when(walletService.getCurrentBalance("non-existent"))
            .thenThrow(new NotFoundException("Carteira não encontrada"));

        // When & Then
        mockMvc.perform(get("/api/v1/wallets/non-existent/balance"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.title").value("Not Found"))
                .andExpect(jsonPath("$.detail").value("Carteira não encontrada"));
    }

    @Test
    @DisplayName("Deve consultar saldo histórico com sucesso")
    void shouldGetHistoricalBalanceSuccessfully() throws Exception {
        // Given
        Instant timestamp = Instant.parse("2024-01-10T12:00:00Z");
        BalanceResponse response = new BalanceResponse(
            "wallet-123", Currency.BRL, 8000L, timestamp
        );

        when(walletService.getHistoricalBalance(eq("wallet-123"), any(Instant.class)))
            .thenReturn(response);

        // When & Then
        mockMvc.perform(get("/api/v1/wallets/wallet-123/balance/history")
                .param("at", "2024-01-10T12:00:00Z"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value("wallet-123"))
                .andExpect(jsonPath("$.currency").value("BRL"))
                .andExpect(jsonPath("$.balance").value(8000))
                .andExpect(jsonPath("$.asOf").value("2024-01-10T12:00:00Z"));
    }
}
