package com.openfinance.payments.adapter.output.persistence.document;

import com.openfinance.payments.domain.enums.*;
import lombok.Builder;
import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

import java.math.BigDecimal;
import java.time.Instant;
import java.time.LocalDate;

@Data
@Builder
@Document(collection = "consents")
public class ConsentDocument {
    @Id
    private String consentId;

    @Indexed(unique = true)
    private String idempotencyKey;

    private Instant creationDateTime;
    private Instant expirationDateTime;
    private Instant statusUpdateDateTime;
    private EnumAuthorisationStatusType status;

    // LoggedUser
    private String loggedUserIdentification;
    private String loggedUserRel;

    // BusinessEntity (optional)
    private String businessEntityIdentification;
    private String businessEntityRel;

    // Creditor
    private EnumPaymentPersonType creditorPersonType;
    private String creditorCpfCnpj;
    private String creditorName;

    // Payment
    private EnumPaymentType paymentType;
    private EnumPaymentPurpose paymentPurpose;
    private LocalDate paymentDate;
    private String currency;
    private BigDecimal amount;
    private String ibgeTownCode;

    // Payment Details
    private EnumLocalInstrument localInstrument;
    private String qrCode;
    private String proxy;

    // Creditor Account
    private String creditorAccountIspb;
    private String creditorAccountIssuer;
    private String creditorAccountNumber;
    private EnumAccountPaymentsType creditorAccountType;

    // Debtor Account (optional)
    private String debtorAccountIspb;
    private String debtorAccountIssuer;
    private String debtorAccountNumber;
    private EnumAccountPaymentsType debtorAccountType;

    // Rejection Reason
    private EnumConsentRejectionReasonType rejectionReasonCode;
    private String rejectionReasonDetail;
}
