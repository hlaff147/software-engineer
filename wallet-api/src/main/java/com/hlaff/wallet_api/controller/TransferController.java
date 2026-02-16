package com.hlaff.wallet_api.controller;

import com.hlaff.wallet_api.dto.AmountRequest;
import com.hlaff.wallet_api.dto.LedgerEntryResponse;
import com.hlaff.wallet_api.dto.TransferRequest;
import com.hlaff.wallet_api.service.WalletService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/v1")
@RequiredArgsConstructor
@Tag(name = "Transfers", description = "Operações de movimentação financeira")
public class TransferController {

    private final WalletService walletService;

    @PostMapping("/wallets/{id}/deposit")
    @Operation(summary = "Realizar depósito", description = "Adiciona valor à carteira")
    public LedgerEntryResponse deposit(@PathVariable String id, 
                                     @Valid @RequestBody AmountRequest req) {
        return walletService.deposit(id, req);
    }

    @PostMapping("/wallets/{id}/withdraw")
    @Operation(summary = "Realizar saque", description = "Remove valor da carteira")
    public LedgerEntryResponse withdraw(@PathVariable String id, 
                                      @Valid @RequestBody AmountRequest req) {
        return walletService.withdraw(id, req);
    }

    @PostMapping("/transfers")
    @Operation(summary = "Realizar transferência", description = "Transfere valor entre carteiras")
    public ResponseEntity<Map<String, Object>> transfer(@Valid @RequestBody TransferRequest req) {
        Map<String, Object> response = walletService.transfer(req);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }
}
