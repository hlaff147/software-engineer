package com.hlaff.wallet_api.controller;

import com.hlaff.wallet_api.dto.BalanceResponse;
import com.hlaff.wallet_api.dto.CreateWalletRequest;
import com.hlaff.wallet_api.dto.WalletResponse;
import com.hlaff.wallet_api.service.WalletService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.Instant;

@RestController
@RequestMapping("/api/v1/wallets")
@RequiredArgsConstructor
@Tag(name = "Wallets", description = "Operações relacionadas às carteiras")
public class WalletController {

    private final WalletService walletService;

    @PostMapping
    @Operation(summary = "Criar nova carteira", description = "Cria uma nova carteira para um usuário")
    public ResponseEntity<WalletResponse> create(@Valid @RequestBody CreateWalletRequest req) {
        WalletResponse response = walletService.createWallet(req);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @GetMapping("/{id}/balance")
    @Operation(summary = "Consultar saldo atual", description = "Retorna o saldo atual da carteira")
    public BalanceResponse balance(@PathVariable String id) {
        return walletService.getCurrentBalance(id);
    }

    @GetMapping("/{id}/balance/history")
    @Operation(summary = "Consultar saldo histórico", description = "Retorna o saldo da carteira em uma data específica")
    public BalanceResponse historical(@PathVariable String id, 
                                    @RequestParam Instant at) {
        return walletService.getHistoricalBalance(id, at);
    }
}
