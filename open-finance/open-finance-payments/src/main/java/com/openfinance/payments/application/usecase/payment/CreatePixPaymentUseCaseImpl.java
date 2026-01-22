package com.openfinance.payments.application.usecase.payment;

import com.openfinance.payments.adapter.output.persistence.repository.PaymentMongoRepository;
import com.openfinance.payments.application.exception.ConsentInvalidException;
import com.openfinance.payments.application.exception.ConsentNotFoundException;
import com.openfinance.payments.domain.entity.Consent;
import com.openfinance.payments.domain.entity.PixPayment;
import com.openfinance.payments.domain.enums.EnumAuthorisationStatusType;
import com.openfinance.payments.domain.port.input.CreatePixPaymentUseCase;
import com.openfinance.payments.domain.port.output.ConsentRepositoryPort;
import com.openfinance.payments.domain.port.output.DictServicePort;
import com.openfinance.payments.domain.port.output.PaymentRepositoryPort;
import com.openfinance.payments.domain.port.output.SpiServicePort;
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
    private final ConsentRepositoryPort consentRepository;
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
            // Get and validate consent
            var consent = validateConsent(paymentItem.consentId());

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
                    .debtorAccount(consent.getDebtorAccount())
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

            // Consume consent
            consent.consume();
            consentRepository.save(consent);

            log.info("Payment created: {}", saved.getPaymentId());
        }

        return createdPayments;
    }

    private Consent validateConsent(String consentId) {
        var consent = consentRepository.findById(consentId)
                .orElseThrow(() -> new ConsentNotFoundException(consentId));

        if (consent.getStatus() == EnumAuthorisationStatusType.CONSUMED) {
            throw new ConsentInvalidException("Consent already consumed: " + consentId, "CONSENTIMENTO_INVALIDO");
        }

        if (consent.getStatus() == EnumAuthorisationStatusType.REJECTED) {
            throw new ConsentInvalidException("Consent rejected: " + consentId, "CONSENTIMENTO_INVALIDO");
        }

        if (!consent.canBeConsumed()) {
            throw new ConsentInvalidException(
                    "Consent cannot be consumed. Status: " + consent.getStatus(),
                    "CONSENTIMENTO_INVALIDO");
        }

        return consent;
    }

    private String generatePaymentId() {
        return UUID.randomUUID().toString().replace("-", "").substring(0, 32);
    }
}
