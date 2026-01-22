package com.openfinance.payments.domain.entity;

import com.openfinance.payments.domain.enums.EnumLocalInstrument;
import com.openfinance.payments.domain.enums.EnumPaymentStatusType;
import com.openfinance.payments.domain.valueobject.*;
import lombok.Builder;
import lombok.Data;

import java.math.BigDecimal;
import java.time.Instant;

@Data
@Builder
public class PixPayment {
    private String paymentId;
    private String endToEndId;
    private String consentId;
    private Instant creationDateTime;
    private Instant statusUpdateDateTime;
    private String proxy;
    private EnumPaymentStatusType status;
    private PaymentRejectionReason rejectionReason;
    private EnumLocalInstrument localInstrument;
    private String cnpjInitiator;
    private BigDecimal amount;
    private String currency;
    private String transactionIdentification;
    private String remittanceInformation;
    private CreditorAccount creditorAccount;
    private DebtorAccount debtorAccount;
    private Cancellation cancellation;
    private String authorisationFlow;

    public void receive() {
        this.status = EnumPaymentStatusType.RCVD;
        this.statusUpdateDateTime = Instant.now();
    }

    public void accept() {
        this.status = EnumPaymentStatusType.ACCP;
        this.statusUpdateDateTime = Instant.now();
    }

    public void process() {
        this.status = EnumPaymentStatusType.ACPD;
        this.statusUpdateDateTime = Instant.now();
    }

    public void complete() {
        this.status = EnumPaymentStatusType.ACSC;
        this.statusUpdateDateTime = Instant.now();
    }

    public void schedule() {
        this.status = EnumPaymentStatusType.SCHD;
        this.statusUpdateDateTime = Instant.now();
    }

    public void setPending() {
        this.status = EnumPaymentStatusType.PDNG;
        this.statusUpdateDateTime = Instant.now();
    }

    public void reject(PaymentRejectionReason reason) {
        this.status = EnumPaymentStatusType.RJCT;
        this.statusUpdateDateTime = Instant.now();
        this.rejectionReason = reason;
    }

    public void cancel(Cancellation cancellationInfo) {
        this.status = EnumPaymentStatusType.CANC;
        this.statusUpdateDateTime = Instant.now();
        this.cancellation = cancellationInfo;
    }

    public boolean canBeCancelled() {
        return status == EnumPaymentStatusType.SCHD || status == EnumPaymentStatusType.PDNG;
    }
}
