package com.hlaff.wallet_api.mapper;

import com.hlaff.wallet_api.dto.CreateWalletRequest;
import com.hlaff.wallet_api.dto.WalletResponse;
import com.hlaff.wallet_api.model.Wallet;
import org.springframework.stereotype.Component;

@Component
public class WalletMapper {

    /**
     * DTO Request -> Model (campos calculados definidos no service)
     */
    public Wallet toModel(CreateWalletRequest req) {
        if (req == null) {
            return null;
        }
        
        Wallet wallet = new Wallet();
        wallet.setUserId(req.userId());
        wallet.setCurrency(req.currency());
        // id, status, balance, createdAt, updatedAt serão definidos no service
        
        return wallet;
    }

    /**
     * Model -> DTO Response (mapeamento manual)
     */
    public WalletResponse toResponse(Wallet wallet) {
        if (wallet == null) {
            return null;
        }
        
        return new WalletResponse(
            wallet.getId(),
            wallet.getUserId(),
            wallet.getCurrency(),
            wallet.getStatus(),
            wallet.getBalance()
        );
    }
}
