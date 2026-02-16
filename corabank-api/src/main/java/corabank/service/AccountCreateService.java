package corabank.service;

import corabank.dto.AccountRequest;
import corabank.dto.AccountResponse;
import corabank.mapper.AccountMapper;
import corabank.model.Account;
import corabank.repository.ContaRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class AccountCreateService {
    private final ContaRepository contaRepository;
    private final AccountMapper accountMapper;

    public AccountResponse execute(AccountRequest request) {
        Account account = accountMapper.toEntity(request);
        
        account.setActive(true);
        
        if (isValidReferralCode(request.getReferralCode())) {
            account.setBalance(10.0);
        } else {
            account.setBalance(0.0);
        }
        
        Account savedAccount = contaRepository.save(account);
        
        return accountMapper.toResponse(savedAccount);
    }
    
    private boolean isValidReferralCode(String referralCode) {
        return "CORA10".equals(referralCode);
    }
}
