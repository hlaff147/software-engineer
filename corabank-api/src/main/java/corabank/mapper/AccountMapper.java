package corabank.mapper;

import corabank.dto.AccountRequest;
import corabank.dto.AccountResponse;
import corabank.model.Account;
import org.springframework.stereotype.Component;

@Component
public class AccountMapper {

    public Account toEntity(AccountRequest request) {
        if (request == null) {
            return null;
        }

        Account account = new Account();
        account.setName(request.getName());
        account.setCpf(request.getCpf());

        return account;
    }

    public AccountResponse toResponse(Account account) {
        if (account == null) {
            return null;
        }

        return new AccountResponse(
                account.getId(),
                account.getName(),
                account.getCpf(),
                account.getBalance(),
                account.getActive()
        );
    }
}