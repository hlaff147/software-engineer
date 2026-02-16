package corabank.controller;

import corabank.dto.AccountRequest;
import corabank.dto.AccountResponse;
import corabank.service.AccountCreateService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class AccountController {
    private final AccountCreateService service;

    @PostMapping("/corabank")
    public AccountResponse get(@Valid @RequestBody AccountRequest accountRequest) {

        return service.execute(accountRequest);
    }
}
