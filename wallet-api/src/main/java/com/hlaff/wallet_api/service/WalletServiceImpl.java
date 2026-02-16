package com.hlaff.wallet_api.service;

import com.hlaff.wallet_api.dto.*;
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
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@Slf4j
@Service
@RequiredArgsConstructor
public class WalletServiceImpl implements WalletService {

    private final WalletRepository walletRepository;
    private final LedgerEntryRepository ledgerEntryRepository;
    private final WalletMapper walletMapper;
    private final LedgerEntryMapper ledgerEntryMapper;
    private final BalanceMapper balanceMapper;

    @Override
    public WalletResponse createWallet(CreateWalletRequest req) {
        log.info("Criando carteira para usuário: {} com moeda: {}", req.userId(), req.currency());
        
        // Verifica se já existe uma carteira para o usuário com a mesma moeda
        var existingWallet = walletRepository.findByUserIdAndCurrency(req.userId(), req.currency());
        if (existingWallet.isPresent()) {
            throw new BusinessException("Carteira já existe para este usuário e moeda");
        }

        Wallet wallet = walletMapper.toModel(req);
        wallet.setStatus(WalletStatus.ACTIVE);
        wallet.setBalance(0L);
        wallet.setCreatedAt(Instant.now());
        wallet.setUpdatedAt(wallet.getCreatedAt());
        
        wallet = walletRepository.save(wallet);
        log.info("Carteira criada com sucesso: {}", wallet.getId());
        
        return walletMapper.toResponse(wallet);
    }

    @Override
    public BalanceResponse getCurrentBalance(String walletId) {
        log.info("Buscando saldo atual da carteira: {}", walletId);
        
        Wallet wallet = findWalletById(walletId);
        return balanceMapper.toCurrentBalance(wallet);
    }

    @Override
    public BalanceResponse getHistoricalBalance(String walletId, Instant at) {
        log.info("Buscando saldo histórico da carteira: {} em: {}", walletId, at);
        
        Wallet wallet = findWalletById(walletId);
        
        // Busca todas as entradas até a data especificada
        List<LedgerEntry> entries = ledgerEntryRepository.findByWalletIdAndOccurredAtLessThanEqual(walletId, at);
        
        // Calcula o saldo somando todas as movimentações
        Long historicalBalance = entries.stream()
                .mapToLong(entry -> {
                    return switch (entry.getOperation()) {
                        case DEPOSIT, TRANSFER_CREDIT -> entry.getAmount();
                        case WITHDRAW, TRANSFER_DEBIT -> -entry.getAmount();
                    };
                })
                .sum();
        
        return new BalanceResponse(walletId, wallet.getCurrency(), historicalBalance, at);
    }

    @Override
    public LedgerEntryResponse deposit(String walletId, AmountRequest req) {
        log.info("Realizando depósito na carteira: {} valor: {}", walletId, req.amount());
        
        Wallet wallet = findWalletById(walletId);
        validateWalletActive(wallet);
        
        // Atualiza saldo da carteira
        Long newBalance = wallet.getBalance() + req.amount();
        wallet.setBalance(newBalance);
        wallet.setUpdatedAt(Instant.now());
        walletRepository.save(wallet);
        
        // Cria entrada no ledger
        LedgerEntry ledgerEntry = createLedgerEntry(
                walletId, null, OperationType.DEPOSIT, req.amount(), newBalance, req.metadata()
        );
        
        log.info("Depósito realizado com sucesso. Novo saldo: {}", newBalance);
        return ledgerEntryMapper.toResponse(ledgerEntry);
    }

    @Override
    public LedgerEntryResponse withdraw(String walletId, AmountRequest req) {
        log.info("Realizando saque da carteira: {} valor: {}", walletId, req.amount());
        
        Wallet wallet = findWalletById(walletId);
        validateWalletActive(wallet);
        
        // Verifica se há saldo suficiente
        if (wallet.getBalance() < req.amount()) {
            throw new InsufficientFundsException("Saldo insuficiente para realizar o saque");
        }
        
        // Atualiza saldo da carteira
        Long newBalance = wallet.getBalance() - req.amount();
        wallet.setBalance(newBalance);
        wallet.setUpdatedAt(Instant.now());
        walletRepository.save(wallet);
        
        // Cria entrada no ledger
        LedgerEntry ledgerEntry = createLedgerEntry(
                walletId, null, OperationType.WITHDRAW, req.amount(), newBalance, req.metadata()
        );
        
        log.info("Saque realizado com sucesso. Novo saldo: {}", newBalance);
        return ledgerEntryMapper.toResponse(ledgerEntry);
    }

    @Override
    public Map<String, Object> transfer(TransferRequest req) {
        log.info("Realizando transferência de {} para {} valor: {}", 
                req.fromWalletId(), req.toWalletId(), req.amount());
        
        if (req.fromWalletId().equals(req.toWalletId())) {
            throw new BusinessException("Carteira de origem e destino não podem ser iguais");
        }
        
        Wallet fromWallet = findWalletById(req.fromWalletId());
        Wallet toWallet = findWalletById(req.toWalletId());
        
        validateWalletActive(fromWallet);
        validateWalletActive(toWallet);
        
        // Verifica se há saldo suficiente
        if (fromWallet.getBalance() < req.amount()) {
            throw new InsufficientFundsException("Saldo insuficiente para realizar a transferência");
        }
        
        String transferId = UUID.randomUUID().toString();
        
        // Debita da carteira origem
        Long newFromBalance = fromWallet.getBalance() - req.amount();
        fromWallet.setBalance(newFromBalance);
        fromWallet.setUpdatedAt(Instant.now());
        walletRepository.save(fromWallet);
        
        // Credita na carteira destino
        Long newToBalance = toWallet.getBalance() + req.amount();
        toWallet.setBalance(newToBalance);
        toWallet.setUpdatedAt(Instant.now());
        walletRepository.save(toWallet);
        
        // Cria entradas no ledger
        LedgerEntry debitEntry = createLedgerEntry(
                req.fromWalletId(), transferId, OperationType.TRANSFER_DEBIT, req.amount(), newFromBalance, req.metadata()
        );
        
        LedgerEntry creditEntry = createLedgerEntry(
                req.toWalletId(), transferId, OperationType.TRANSFER_CREDIT, req.amount(), newToBalance, req.metadata()
        );
        
        log.info("Transferência realizada com sucesso. Transfer ID: {}", transferId);
        
        return Map.of(
                "transferId", transferId,
                "fromWallet", Map.of(
                        "walletId", req.fromWalletId(),
                        "newBalance", newFromBalance
                ),
                "toWallet", Map.of(
                        "walletId", req.toWalletId(),
                        "newBalance", newToBalance
                ),
                "debitEntry", ledgerEntryMapper.toResponse(debitEntry),
                "creditEntry", ledgerEntryMapper.toResponse(creditEntry)
        );
    }

    @Override
    public Page<LedgerEntryResponse> listLedger(String walletId, Instant from, Instant to, Pageable pageable) {
        log.info("Listando extrato da carteira: {} de {} até {}", walletId, from, to);
        
        // Verifica se a carteira existe
        findWalletById(walletId);
        
        Page<LedgerEntry> entries;
        if (from != null && to != null) {
            entries = ledgerEntryRepository.findByWalletIdAndOccurredAtBetween(walletId, from, to, pageable);
        } else {
            entries = ledgerEntryRepository.findAll(pageable);
        }
        
        return entries.map(ledgerEntryMapper::toResponse);
    }

    private Wallet findWalletById(String walletId) {
        return walletRepository.findById(walletId)
                .orElseThrow(() -> new NotFoundException("Carteira não encontrada"));
    }

    private void validateWalletActive(Wallet wallet) {
        if (wallet.getStatus() != WalletStatus.ACTIVE) {
            throw new BusinessException("Carteira não está ativa");
        }
    }

    private LedgerEntry createLedgerEntry(String walletId, String transferId, OperationType operation, 
                                         Long amount, Long resultingBalance, Map<String, String> metadata) {
        LedgerEntry ledgerEntry = new LedgerEntry();
        ledgerEntry.setWalletId(walletId);
        ledgerEntry.setTransferId(transferId);
        ledgerEntry.setOperation(operation);
        ledgerEntry.setAmount(amount);
        ledgerEntry.setOccurredAt(Instant.now());
        ledgerEntry.setResultingBalance(resultingBalance);
        ledgerEntry.setMetadata(metadata);
        
        return ledgerEntryRepository.save(ledgerEntry);
    }
}
