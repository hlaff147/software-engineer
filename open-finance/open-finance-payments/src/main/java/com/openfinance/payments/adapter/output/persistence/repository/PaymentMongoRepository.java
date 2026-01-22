package com.openfinance.payments.adapter.output.persistence.repository;

import com.openfinance.payments.adapter.output.persistence.mapper.DocumentMapper;
import com.openfinance.payments.domain.entity.PixPayment;
import com.openfinance.payments.domain.port.output.PaymentRepositoryPort;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.time.ZoneOffset;
import java.util.List;
import java.util.Optional;

@Repository
@RequiredArgsConstructor
public class PaymentMongoRepository implements PaymentRepositoryPort {

    private final SpringDataPaymentRepository springDataRepository;
    private final DocumentMapper mapper;

    private String currentIdempotencyKey;

    public void setIdempotencyKey(String idempotencyKey) {
        this.currentIdempotencyKey = idempotencyKey;
    }

    @Override
    public PixPayment save(PixPayment payment) {
        var document = mapper.toDocument(payment, currentIdempotencyKey);
        var saved = springDataRepository.save(document);
        return mapper.toDomain(saved);
    }

    @Override
    public Optional<PixPayment> findById(String paymentId) {
        return springDataRepository.findById(paymentId)
                .map(mapper::toDomain);
    }

    @Override
    public List<PixPayment> findByConsentId(String consentId) {
        return springDataRepository.findByConsentId(consentId).stream()
                .map(mapper::toDomain)
                .toList();
    }

    @Override
    public List<PixPayment> findByConsentIdAndDateRange(String consentId, LocalDate startDate, LocalDate endDate) {
        var start = startDate.atStartOfDay().toInstant(ZoneOffset.UTC);
        var end = endDate.plusDays(1).atStartOfDay().toInstant(ZoneOffset.UTC);

        return springDataRepository.findByConsentIdAndCreationDateTimeBetween(consentId, start, end).stream()
                .map(mapper::toDomain)
                .toList();
    }

    @Override
    public boolean existsByIdempotencyKey(String idempotencyKey) {
        return springDataRepository.existsByIdempotencyKey(idempotencyKey);
    }

    @Override
    public Optional<PixPayment> findByIdempotencyKey(String idempotencyKey) {
        return springDataRepository.findByIdempotencyKey(idempotencyKey)
                .map(mapper::toDomain);
    }
}
