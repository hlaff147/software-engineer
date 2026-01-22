package com.openfinance.consent.domain.entity;

import com.openfinance.common.domain.enums.EnumAuthorisationStatusType;
import com.openfinance.common.domain.valueobject.*;
import lombok.Builder;
import lombok.Data;

import java.time.Instant;

@Data
@Builder
public class Consent {
    private String consentId;
    private Instant creationDateTime;
    private Instant expirationDateTime;
    private Instant statusUpdateDateTime;
    private EnumAuthorisationStatusType status;
    private LoggedUser loggedUser;
    private BusinessEntity businessEntity;
    private Creditor creditor;
    private PaymentInfo payment;
    private DebtorAccount debtorAccount;
    private ConsentRejectionReason rejectionReason;

    public boolean isExpired() {
        return Instant.now().isAfter(expirationDateTime);
    }

    public boolean canBeConsumed() {
        return status == EnumAuthorisationStatusType.AUTHORISED && !isExpired();
    }

    public void authorize() {
        this.status = EnumAuthorisationStatusType.AUTHORISED;
        this.statusUpdateDateTime = Instant.now();
        this.expirationDateTime = Instant.now().plusSeconds(60 * 60); // 60 minutes
    }

    public void consume() {
        this.status = EnumAuthorisationStatusType.CONSUMED;
        this.statusUpdateDateTime = Instant.now();
    }

    public void reject(ConsentRejectionReason reason) {
        this.status = EnumAuthorisationStatusType.REJECTED;
        this.statusUpdateDateTime = Instant.now();
        this.rejectionReason = reason;
    }
}
