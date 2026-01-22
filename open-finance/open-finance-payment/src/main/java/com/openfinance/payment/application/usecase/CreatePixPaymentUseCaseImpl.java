package com.openfinance.payment.application.usecase;

import com.openfinance.payment.adapter.output.persistence.repository.PaymentMongoRepository;
import com.openfinance.payment.adapter.output.external.dto.ConsentResponse;
import com.openfinance.common.application.exception.ConsentInvalidException;
import com.openfinance.common.application.exception.ConsentNotFoundException;
import com.openfinance.common.domain.valueobject.DebtorAccount;
import com.openfinance.common.domain.enums.EnumAccountPaymentsType;
import com.openfinance.payment.domain.entity.PixPayment;
import com.openfinance.payment.domain.port.input.CreatePixPaymentUseCase;
import com.openfinance.payment.domain.port.output.ConsentServicePort;
import com.openfinance.payment.domain.port.output.DictServicePort;
import com.openfinance.payment.domain.port.output.PaymentRepositoryPort;
import com.openfinance.payment.domain.port.output.SpiServicePort;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Slf4j
@Service
@RequiredArgsConstructor
public class CreatePixPaymentUseCaseImpl implements CreatePixPaymentUseCase {

    private final PaymentRepositoryPort paymentRepository;
    private final ConsentServicePort consentService;
    private final DictServicePort dictService;
    private final SpiServicePort spiService;

    @Override
    public List<PixPayment> execute(CreatePixPaymentCommand command) {
        log.info("Creating {} payment(s)", command.payments().size());

        // Check idempotency
        if (paymentRepository.existsByIdempotencyKey(command.idempotencyKey())) {
            log.info("Payment already exists for idempotency key: {}", command.idempotencyKey());
            return paymentRepository.findByIdempotencyKey(command.idempotencyKey())
                    .map(List::of)
                    .orElse(List.of());
        }

        // Set idempotency key for repository
        if (paymentRepository instanceof PaymentMongoRepository mongoRepo) {
            mongoRepo.setIdempotencyKey(command.idempotencyKey());
        }

        List<PixPayment> createdPayments = new ArrayList<>();

        for (var paymentItem : command.payments()) {
            // Get and validate consent via Feign client
            var consentResponse = validateConsent(paymentItem.consentId());

            // Validate Pix key if present
            if (paymentItem.proxy() != null) {
                dictService.validatePixKey(paymentItem.proxy());
            }

            var now = Instant.now();
            var payment = PixPayment.builder()
                    .paymentId(generatePaymentId())
                    .endToEndId(paymentItem.endToEndId())
                    .consentId(paymentItem.consentId())
                    .creationDateTime(now)
                    .statusUpdateDateTime(now)
                    .proxy(paymentItem.proxy())
                    .localInstrument(paymentItem.localInstrument())
                    .cnpjInitiator(paymentItem.cnpjInitiator())
                    .amount(paymentItem.amount())
                    .currency(paymentItem.currency())
                    .transactionIdentification(paymentItem.transactionIdentification())
                    .remittanceInformation(paymentItem.remittanceInformation())
                    .creditorAccount(paymentItem.creditorAccount())
                    .debtorAccount(mapDebtorAccount(consentResponse.getData().getDebtorAccount()))
                    .authorisationFlow(paymentItem.authorisationFlow())
                    .build();

            // Process payment synchronously
            payment.receive();
            payment.accept();

            // Send to SPI (mocked)
            var spiResult = spiService.sendPayment(payment);
            if (spiResult.isSuccess()) {
                payment.process();
                payment.complete();
            }

            var saved = paymentRepository.save(payment);
            createdPayments.add(saved);

            log.info("Payment created: {}", saved.getPaymentId());
        }

        return createdPayments;
    }

    private ConsentResponse validateConsent(String consentId) {
        ConsentResponse consent;
        try {
            consent = consentService.getConsent(consentId);
        } catch (Exception e) {
            log.error("Failed to fetch consent: {}", consentId, e);
            throw new ConsentNotFoundException(consentId);
        }

        if (consent == null || consent.getData() == null) {
            throw new ConsentNotFoundException(consentId);
        }

        var status = consent.getData().getStatus();
        if ("CONSUMED".equals(status)) {
            throw new ConsentInvalidException("Consent already consumed: " + consentId, "CONSENTIMENTO_INVALIDO");
        }

        if ("REJECTED".equals(status)) {
            throw new ConsentInvalidException("Consent rejected: " + consentId, "CONSENTIMENTO_INVALIDO");
        }

        if (!"AUTHORISED".equals(status)) {
            throw new ConsentInvalidException(
                    "Consent cannot be consumed. Status: " + status,
                    "CONSENTIMENTO_INVALIDO");
        }

        return consent;
    }

    private DebtorAccount mapDebtorAccount(ConsentResponse.DebtorAccount debtorAccount) {
        if (debtorAccount == null)
            return null;

        return DebtorAccount.builder()
                .ispb(debtorAccount.getIspb())
                .issuer(debtorAccount.getIssuer())
                .number(debtorAccount.getNumber())
                .accountType(EnumAccountPaymentsType.valueOf(debtorAccount.getAccountType()))
                .build();
    }

    private String generatePaymentId() {
        return UUID.randomUUID().toString().replace("-", "").substring(0, 32);
    }
}
