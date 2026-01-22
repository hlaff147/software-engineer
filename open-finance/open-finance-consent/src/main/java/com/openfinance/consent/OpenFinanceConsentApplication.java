package com.openfinance.consent;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication(scanBasePackages = { "com.openfinance.consent", "com.openfinance.common" })
public class OpenFinanceConsentApplication {

    public static void main(String[] args) {
        SpringApplication.run(OpenFinanceConsentApplication.class, args);
    }

}
