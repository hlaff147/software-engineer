package com.openfinance.payment;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.openfeign.EnableFeignClients;

@SpringBootApplication(scanBasePackages = { "com.openfinance.payment", "com.openfinance.common" })
@EnableFeignClients
public class OpenFinancePaymentApplication {

    public static void main(String[] args) {
        SpringApplication.run(OpenFinancePaymentApplication.class, args);
    }

}
