package com.hlaff.wallet_api.controller;

import com.hlaff.wallet_api.dto.LedgerEntryResponse;
import com.hlaff.wallet_api.enums.OperationType;
import com.hlaff.wallet_api.exception.NotFoundException;
import com.hlaff.wallet_api.service.WalletService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.test.web.servlet.MockMvc;

import java.time.Instant;
import java.util.Arrays;
import java.util.List;

import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(LedgerController.class)
@DisplayName("LedgerController Tests")
class LedgerControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockitoBean
    private WalletService walletService;

    @Test
    @DisplayName("Deve listar extrato com sucesso")
    void shouldListLedgerSuccessfully() throws Exception {
        // Given
        List<LedgerEntryResponse> entries = Arrays.asList(
            new LedgerEntryResponse(
                "entry-1", "wallet-123", OperationType.DEPOSIT, 10000L,
                Instant.parse("2024-01-15T10:00:00Z"), 10000L
            ),
            new LedgerEntryResponse(
                "entry-2", "wallet-123", OperationType.WITHDRAW, 3000L,
                Instant.parse("2024-01-15T11:00:00Z"), 7000L
            )
        );

        Page<LedgerEntryResponse> page = new PageImpl<>(entries);

        when(walletService.listLedger(eq("wallet-123"), isNull(), isNull(), any()))
            .thenReturn(page);

        // When & Then
        mockMvc.perform(get("/api/v1/wallets/wallet-123/ledger"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content").isArray())
                .andExpect(jsonPath("$.content.length()").value(2))
                .andExpect(jsonPath("$.content[0].id").value("entry-1"))
                .andExpect(jsonPath("$.content[0].operation").value("DEPOSIT"))
                .andExpect(jsonPath("$.content[0].amount").value(10000))
                .andExpect(jsonPath("$.content[1].id").value("entry-2"))
                .andExpect(jsonPath("$.content[1].operation").value("WITHDRAW"))
                .andExpect(jsonPath("$.content[1].amount").value(3000));
    }

    @Test
    @DisplayName("Deve listar extrato com filtro de período")
    void shouldListLedgerWithDateFilter() throws Exception {
        // Given
        List<LedgerEntryResponse> entries = Arrays.asList(
            new LedgerEntryResponse(
                "entry-filtered", "wallet-123", OperationType.TRANSFER_CREDIT, 5000L,
                Instant.parse("2024-01-15T12:00:00Z"), 12000L
            )
        );

        Page<LedgerEntryResponse> page = new PageImpl<>(entries);

        when(walletService.listLedger(eq("wallet-123"), any(Instant.class), any(Instant.class), any()))
            .thenReturn(page);

        // When & Then
        mockMvc.perform(get("/api/v1/wallets/wallet-123/ledger")
                .param("from", "2024-01-15T00:00:00Z")
                .param("to", "2024-01-15T23:59:59Z"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content").isArray())
                .andExpect(jsonPath("$.content.length()").value(1))
                .andExpect(jsonPath("$.content[0].id").value("entry-filtered"))
                .andExpect(jsonPath("$.content[0].operation").value("TRANSFER_CREDIT"));
    }

    @Test
    @DisplayName("Deve listar extrato com paginação customizada")
    void shouldListLedgerWithCustomPagination() throws Exception {
        // Given
        List<LedgerEntryResponse> entries = Arrays.asList(
            new LedgerEntryResponse(
                "entry-page", "wallet-123", OperationType.DEPOSIT, 2000L,
                Instant.parse("2024-01-15T13:00:00Z"), 14000L
            )
        );

        Page<LedgerEntryResponse> page = new PageImpl<>(entries);

        when(walletService.listLedger(eq("wallet-123"), isNull(), isNull(), any()))
            .thenReturn(page);

        // When & Then
        mockMvc.perform(get("/api/v1/wallets/wallet-123/ledger")
                .param("page", "1")
                .param("size", "5")
                .param("sort", "occurredAt,desc"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content").isArray())
                .andExpect(jsonPath("$.content.length()").value(1))
                .andExpect(jsonPath("$.content[0].id").value("entry-page"));
    }

    @Test
    @DisplayName("Deve retornar erro 404 para carteira inexistente")
    void shouldReturn404WhenWalletNotFoundForLedger() throws Exception {
        // Given
        when(walletService.listLedger(eq("non-existent"), isNull(), isNull(), any()))
            .thenThrow(new NotFoundException("Carteira não encontrada"));

        // When & Then
        mockMvc.perform(get("/api/v1/wallets/non-existent/ledger"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.title").value("Not Found"))
                .andExpect(jsonPath("$.detail").value("Carteira não encontrada"));
    }

    @Test
    @DisplayName("Deve retornar lista vazia quando não há movimentações")
    void shouldReturnEmptyListWhenNoEntries() throws Exception {
        // Given
        Page<LedgerEntryResponse> emptyPage = new PageImpl<>(Arrays.asList());

        when(walletService.listLedger(eq("wallet-123"), isNull(), isNull(), any()))
            .thenReturn(emptyPage);

        // When & Then
        mockMvc.perform(get("/api/v1/wallets/wallet-123/ledger"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content").isArray())
                .andExpect(jsonPath("$.content.length()").value(0))
                .andExpect(jsonPath("$.totalElements").value(0));
    }
}
