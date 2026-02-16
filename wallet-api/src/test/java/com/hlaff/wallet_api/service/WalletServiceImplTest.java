package com.hlaff.wallet_api.service;

import com.hlaff.wallet_api.dto.*;
import com.hlaff.wallet_api.enums.Currency;
import com.hlaff.wallet_api.enums.OperationType;
import com.hlaff.wallet_api.enums.WalletStatus;
import com.hlaff.wallet_api.exception.BusinessException;
import com.hlaff.wallet_api.exception.InsufficientFundsException;
import com.hlaff.wallet_api.exception.NotFoundException;
import com.hlaff.wallet_api.mapper.BalanceMapper;
import com.hlaff.wallet_api.mapper.LedgerEntryMapper;
import com.hlaff.wallet_api.mapper.WalletMapper;
import com.hlaff.wallet_api.model.LedgerEntry;
import com.hlaff.wallet_api.model.Wallet;
import com.hlaff.wallet_api.repository.LedgerEntryRepository;
import com.hlaff.wallet_api.repository.WalletRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;

import java.time.Instant;
import java.util.*;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
@DisplayName("WalletService Tests")
class WalletServiceImplTest {

    @Mock
    private WalletRepository walletRepository;
    
    @Mock
    private LedgerEntryRepository ledgerEntryRepository;
    
    @Mock
    private WalletMapper walletMapper;
    
    @Mock
    private LedgerEntryMapper ledgerEntryMapper;
    
    @Mock
    private BalanceMapper balanceMapper;

    @InjectMocks
    private WalletServiceImpl walletService;

    private Wallet wallet;
    private CreateWalletRequest createRequest;
    private WalletResponse walletResponse;
    private AmountRequest amountRequest;

    @BeforeEach
    void setUp() {
        wallet = new Wallet();
        wallet.setId("wallet-123");
        wallet.setUserId("user-123");
        wallet.setCurrency(Currency.BRL);
        wallet.setBalance(10000L);
        wallet.setStatus(WalletStatus.ACTIVE);
        wallet.setCreatedAt(Instant.now());
        wallet.setUpdatedAt(Instant.now());

        createRequest = new CreateWalletRequest("user-123", Currency.BRL);
        
        walletResponse = new WalletResponse(
            "wallet-123", "user-123", Currency.BRL, WalletStatus.ACTIVE, 10000L
        );

        amountRequest = new AmountRequest(5000L, Map.of("source", "test"));
    }

    @Test
    @DisplayName("Deve criar carteira com sucesso")
    void shouldCreateWalletSuccessfully() {
        // Given
        when(walletRepository.findByUserIdAndCurrency("user-123", Currency.BRL))
            .thenReturn(Optional.empty());
        when(walletMapper.toModel(createRequest)).thenReturn(wallet);
        when(walletRepository.save(any(Wallet.class))).thenReturn(wallet);
        when(walletMapper.toResponse(wallet)).thenReturn(walletResponse);

        // When
        WalletResponse result = walletService.createWallet(createRequest);

        // Then
        assertThat(result).isNotNull();
        assertThat(result.id()).isEqualTo("wallet-123");
        assertThat(result.userId()).isEqualTo("user-123");
        assertThat(result.currency()).isEqualTo(Currency.BRL);
        assertThat(result.status()).isEqualTo(WalletStatus.ACTIVE);
        
        verify(walletRepository).findByUserIdAndCurrency("user-123", Currency.BRL);
        verify(walletRepository).save(any(Wallet.class));
        verify(walletMapper).toModel(createRequest);
        verify(walletMapper).toResponse(wallet);
    }

    @Test
    @DisplayName("Deve lançar exceção ao criar carteira duplicada")
    void shouldThrowExceptionWhenCreatingDuplicateWallet() {
        // Given
        when(walletRepository.findByUserIdAndCurrency("user-123", Currency.BRL))
            .thenReturn(Optional.of(wallet));

        // When & Then
        assertThatThrownBy(() -> walletService.createWallet(createRequest))
            .isInstanceOf(BusinessException.class)
            .hasMessage("Carteira já existe para este usuário e moeda");
            
        verify(walletRepository).findByUserIdAndCurrency("user-123", Currency.BRL);
        verify(walletRepository, never()).save(any());
    }

    @Test
    @DisplayName("Deve consultar saldo atual com sucesso")
    void shouldGetCurrentBalanceSuccessfully() {
        // Given
        BalanceResponse balanceResponse = new BalanceResponse(
            "wallet-123", Currency.BRL, 10000L, Instant.now()
        );
        when(walletRepository.findById("wallet-123")).thenReturn(Optional.of(wallet));
        when(balanceMapper.toCurrentBalance(wallet)).thenReturn(balanceResponse);

        // When
        BalanceResponse result = walletService.getCurrentBalance("wallet-123");

        // Then
        assertThat(result).isNotNull();
        assertThat(result.id()).isEqualTo("wallet-123");
        assertThat(result.balance()).isEqualTo(10000L);
        
        verify(walletRepository).findById("wallet-123");
        verify(balanceMapper).toCurrentBalance(wallet);
    }

    @Test
    @DisplayName("Deve realizar depósito com sucesso")
    void shouldDepositSuccessfully() {
        // Given
        LedgerEntry ledgerEntry = new LedgerEntry();
        ledgerEntry.setId("ledger-123");
        ledgerEntry.setWalletId("wallet-123");
        ledgerEntry.setOperation(OperationType.DEPOSIT);
        ledgerEntry.setAmount(5000L);
        ledgerEntry.setResultingBalance(15000L);
        
        LedgerEntryResponse ledgerResponse = new LedgerEntryResponse(
            "ledger-123", "wallet-123", OperationType.DEPOSIT, 5000L, Instant.now(), 15000L
        );

        when(walletRepository.findById("wallet-123")).thenReturn(Optional.of(wallet));
        when(ledgerEntryRepository.save(any(LedgerEntry.class))).thenReturn(ledgerEntry);
        when(ledgerEntryMapper.toResponse(ledgerEntry)).thenReturn(ledgerResponse);

        // When
        LedgerEntryResponse result = walletService.deposit("wallet-123", amountRequest);

        // Then
        assertThat(result).isNotNull();
        assertThat(result.operation()).isEqualTo(OperationType.DEPOSIT);
        assertThat(result.amount()).isEqualTo(5000L);
        assertThat(result.resultingBalance()).isEqualTo(15000L);
        
        verify(walletRepository).findById("wallet-123");
        verify(walletRepository).save(wallet);
        verify(ledgerEntryRepository).save(any(LedgerEntry.class));
        
        // Verifica se o saldo foi atualizado
        assertThat(wallet.getBalance()).isEqualTo(15000L);
    }

    @Test
    @DisplayName("Deve realizar saque com sucesso")
    void shouldWithdrawSuccessfully() {
        // Given
        LedgerEntry ledgerEntry = new LedgerEntry();
        ledgerEntry.setId("ledger-456");
        ledgerEntry.setWalletId("wallet-123");
        ledgerEntry.setOperation(OperationType.WITHDRAW);
        ledgerEntry.setAmount(3000L);
        ledgerEntry.setResultingBalance(7000L);
        
        LedgerEntryResponse ledgerResponse = new LedgerEntryResponse(
            "ledger-456", "wallet-123", OperationType.WITHDRAW, 3000L, Instant.now(), 7000L
        );

        when(walletRepository.findById("wallet-123")).thenReturn(Optional.of(wallet));
        when(ledgerEntryRepository.save(any(LedgerEntry.class))).thenReturn(ledgerEntry);
        when(ledgerEntryMapper.toResponse(ledgerEntry)).thenReturn(ledgerResponse);

        AmountRequest withdrawRequest = new AmountRequest(3000L, Map.of("method", "TED"));

        // When
        LedgerEntryResponse result = walletService.withdraw("wallet-123", withdrawRequest);

        // Then
        assertThat(result).isNotNull();
        assertThat(result.operation()).isEqualTo(OperationType.WITHDRAW);
        assertThat(result.amount()).isEqualTo(3000L);
        assertThat(result.resultingBalance()).isEqualTo(7000L);
        
        verify(walletRepository).findById("wallet-123");
        verify(walletRepository).save(wallet);
        verify(ledgerEntryRepository).save(any(LedgerEntry.class));
        
        // Verifica se o saldo foi atualizado
        assertThat(wallet.getBalance()).isEqualTo(7000L);
    }

    @Test
    @DisplayName("Deve lançar exceção ao sacar com saldo insuficiente")
    void shouldThrowExceptionWhenInsufficientFunds() {
        // Given
        when(walletRepository.findById("wallet-123")).thenReturn(Optional.of(wallet));
        AmountRequest largeWithdraw = new AmountRequest(20000L, Map.of());

        // When & Then
        assertThatThrownBy(() -> walletService.withdraw("wallet-123", largeWithdraw))
            .isInstanceOf(InsufficientFundsException.class)
            .hasMessage("Saldo insuficiente para realizar o saque");
            
        verify(walletRepository).findById("wallet-123");
        verify(walletRepository, never()).save(any());
        verify(ledgerEntryRepository, never()).save(any());
    }

    @Test
    @DisplayName("Deve realizar transferência com sucesso")
    void shouldTransferSuccessfully() {
        // Given
        Wallet toWallet = new Wallet();
        toWallet.setId("wallet-456");
        toWallet.setUserId("user-456");
        toWallet.setBalance(5000L);
        toWallet.setStatus(WalletStatus.ACTIVE);

        TransferRequest transferRequest = new TransferRequest(
            "wallet-123", "wallet-456", 3000L, Map.of("type", "payment")
        );

        LedgerEntry debitEntry = new LedgerEntry();
        debitEntry.setId("debit-123");
        debitEntry.setOperation(OperationType.TRANSFER_DEBIT);
        
        LedgerEntry creditEntry = new LedgerEntry();
        creditEntry.setId("credit-123");
        creditEntry.setOperation(OperationType.TRANSFER_CREDIT);

        LedgerEntryResponse debitResponse = new LedgerEntryResponse(
            "debit-123", "wallet-123", OperationType.TRANSFER_DEBIT, 3000L, Instant.now(), 7000L
        );
        
        LedgerEntryResponse creditResponse = new LedgerEntryResponse(
            "credit-123", "wallet-456", OperationType.TRANSFER_CREDIT, 3000L, Instant.now(), 8000L
        );

        when(walletRepository.findById("wallet-123")).thenReturn(Optional.of(wallet));
        when(walletRepository.findById("wallet-456")).thenReturn(Optional.of(toWallet));
        when(ledgerEntryRepository.save(any(LedgerEntry.class)))
            .thenReturn(debitEntry)
            .thenReturn(creditEntry);
        when(ledgerEntryMapper.toResponse(debitEntry)).thenReturn(debitResponse);
        when(ledgerEntryMapper.toResponse(creditEntry)).thenReturn(creditResponse);

        // When
        Map<String, Object> result = walletService.transfer(transferRequest);

        // Then
        assertThat(result).isNotNull();
        assertThat(result).containsKey("transferId");
        assertThat(result).containsKey("fromWallet");
        assertThat(result).containsKey("toWallet");
        assertThat(result).containsKey("debitEntry");
        assertThat(result).containsKey("creditEntry");

        verify(walletRepository).findById("wallet-123");
        verify(walletRepository).findById("wallet-456");
        verify(walletRepository, times(2)).save(any(Wallet.class));
        verify(ledgerEntryRepository, times(2)).save(any(LedgerEntry.class));
        
        // Verifica se os saldos foram atualizados
        assertThat(wallet.getBalance()).isEqualTo(7000L);
        assertThat(toWallet.getBalance()).isEqualTo(8000L);
    }

    @Test
    @DisplayName("Deve lançar exceção ao transferir para a mesma carteira")
    void shouldThrowExceptionWhenTransferringToSameWallet() {
        // Given
        TransferRequest transferRequest = new TransferRequest(
            "wallet-123", "wallet-123", 3000L, Map.of()
        );

        // When & Then
        assertThatThrownBy(() -> walletService.transfer(transferRequest))
            .isInstanceOf(BusinessException.class)
            .hasMessage("Carteira de origem e destino não podem ser iguais");
    }

    @Test
    @DisplayName("Deve lançar exceção ao buscar carteira inexistente")
    void shouldThrowExceptionWhenWalletNotFound() {
        // Given
        when(walletRepository.findById("non-existent")).thenReturn(Optional.empty());

        // When & Then
        assertThatThrownBy(() -> walletService.getCurrentBalance("non-existent"))
            .isInstanceOf(NotFoundException.class)
            .hasMessage("Carteira não encontrada");
            
        verify(walletRepository).findById("non-existent");
    }

    @Test
    @DisplayName("Deve lançar exceção ao operar com carteira inativa")
    void shouldThrowExceptionWhenWalletIsInactive() {
        // Given
        wallet.setStatus(WalletStatus.BLOCKED);
        when(walletRepository.findById("wallet-123")).thenReturn(Optional.of(wallet));

        // When & Then
        assertThatThrownBy(() -> walletService.deposit("wallet-123", amountRequest))
            .isInstanceOf(BusinessException.class)
            .hasMessage("Carteira não está ativa");
            
        verify(walletRepository).findById("wallet-123");
    }

    @Test
    @DisplayName("Deve listar extrato com paginação")
    void shouldListLedgerWithPagination() {
        // Given
        LedgerEntry entry1 = new LedgerEntry();
        entry1.setId("entry-1");
        entry1.setWalletId("wallet-123");
        
        LedgerEntry entry2 = new LedgerEntry();
        entry2.setId("entry-2");
        entry2.setWalletId("wallet-123");
        
        List<LedgerEntry> entries = Arrays.asList(entry1, entry2);
        Page<LedgerEntry> entryPage = new PageImpl<>(entries);
        
        LedgerEntryResponse response1 = new LedgerEntryResponse(
            "entry-1", "wallet-123", OperationType.DEPOSIT, 5000L, Instant.now(), 5000L
        );
        
        LedgerEntryResponse response2 = new LedgerEntryResponse(
            "entry-2", "wallet-123", OperationType.WITHDRAW, 1000L, Instant.now(), 4000L
        );

        when(walletRepository.findById("wallet-123")).thenReturn(Optional.of(wallet));
        when(ledgerEntryRepository.findAll(any(PageRequest.class))).thenReturn(entryPage);
        when(ledgerEntryMapper.toResponse(entry1)).thenReturn(response1);
        when(ledgerEntryMapper.toResponse(entry2)).thenReturn(response2);

        PageRequest pageRequest = PageRequest.of(0, 10);

        // When
        Page<LedgerEntryResponse> result = walletService.listLedger(
            "wallet-123", null, null, pageRequest
        );

        // Then
        assertThat(result).isNotNull();
        assertThat(result.getContent()).hasSize(2);
        assertThat(result.getContent().get(0).id()).isEqualTo("entry-1");
        assertThat(result.getContent().get(1).id()).isEqualTo("entry-2");
        
        verify(walletRepository).findById("wallet-123");
        verify(ledgerEntryRepository).findAll(pageRequest);
    }
}
