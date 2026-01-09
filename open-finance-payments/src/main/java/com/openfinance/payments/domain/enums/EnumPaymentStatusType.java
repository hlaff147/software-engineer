package com.openfinance.payments.domain.enums;

public enum EnumPaymentStatusType {
    RCVD, // Received
    CANC, // Cancelled
    ACCP, // Accepted Customer Profile
    ACPD, // Accepted Clearing Processed
    RJCT, // Rejected
    ACSC, // Accepted Settlement Completed
    PDNG, // Pending
    SCHD // Scheduled
}
