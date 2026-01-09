package com.openfinance.payments.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import io.swagger.v3.oas.models.servers.Server;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.List;

@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI openFinanceOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("API Payment Initiation - Open Finance Brasil")
                        .description(
                                "API de Iniciação de Pagamentos, responsável por viabilizar as operações de iniciação de pagamentos para o Open Finance Brasil.")
                        .version("5.0.0-beta.1")
                        .contact(new Contact()
                                .name("Open Finance Brasil")
                                .email("gt-interfaces@openbankingbr.org")
                                .url("https://openbanking-brasil.github.io/areadesenvolvedor/"))
                        .license(new License()
                                .name("Apache 2.0")
                                .url("https://www.apache.org/licenses/LICENSE-2.0")))
                .servers(List.of(
                        new Server()
                                .url("http://localhost:8080/open-banking/payments/v5")
                                .description("Local Development Server")));
    }
}
