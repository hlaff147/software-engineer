package com.openfinance.payment.adapter.output.persistence.document;

import com.openfinance.common.domain.enums.*;
import lombok.Builder;
import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

import java.math.BigDecimal;
import java.time.Instant;

@Data
@Builder
@Document(collection = "payments")
public class PaymentDocument {
    @Id
    private String paymentId;

    @Indexed
    private String consentId;

    @Indexed(unique = true)
    private String idempotencyKey;

    private String endToEndId;
    private Instant creationDateTime;
    private Instant statusUpdateDateTime;
    private String proxy;
    private EnumPaymentStatusType status;
    private EnumLocalInstrument localInstrument;
    private String cnpjInitiator;
    private BigDecimal amount;
    private String currency;
    private String transactionIdentification;
    private String remittanceInformation;
    private String authorisationFlow;

    // Creditor Account
    private String creditorAccountIspb;
    private String creditorAccountIssuer;
    private String creditorAccountNumber;
    private EnumAccountPaymentsType creditorAccountType;

    // Debtor Account
    private String debtorAccountIspb;
    private String debtorAccountIssuer;
    private String debtorAccountNumber;
    private EnumAccountPaymentsType debtorAccountType;

    // Rejection Reason
    private EnumPaymentRejectionReasonType rejectionReasonCode;
    private String rejectionReasonDetail;

    // Cancellation
    private EnumCancellationReason cancellationReason;
    private EnumCancellationFrom cancellationFrom;
    private Instant cancellationAt;
    private String cancellationByIdentification;
    private String cancellationByRel;
}
