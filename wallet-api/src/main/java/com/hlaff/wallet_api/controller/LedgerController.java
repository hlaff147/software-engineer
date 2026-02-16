package com.hlaff.wallet_api.controller;

import com.hlaff.wallet_api.dto.LedgerEntryResponse;
import com.hlaff.wallet_api.service.WalletService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.data.web.PageableDefault;
import org.springframework.web.bind.annotation.*;

import java.time.Instant;

@RestController
@RequestMapping("/api/v1/wallets/{id}/ledger")
@RequiredArgsConstructor
@Tag(name = "Ledger", description = "Operações de extrato e histórico")
public class LedgerController {

    private final WalletService walletService;

    @GetMapping
    @Operation(summary = "Consultar extrato", description = "Retorna o histórico de movimentações da carteira")
    public Page<LedgerEntryResponse> ledger(
            @PathVariable String id,
            @RequestParam(required = false) Instant from,
            @RequestParam(required = false) Instant to,
            @PageableDefault(size = 50, sort = "occurredAt", direction = Sort.Direction.DESC) Pageable pageable) {
        return walletService.listLedger(id, from, to, pageable);
    }
}
