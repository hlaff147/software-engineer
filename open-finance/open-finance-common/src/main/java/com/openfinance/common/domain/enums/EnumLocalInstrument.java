package com.openfinance.common.domain.enums;

public enum EnumLocalInstrument {
    MANU, // Manual account data entry
    DICT, // Manual Pix key entry
    QRDN, // Dynamic QR Code reading (except NFC)
    QRES, // Static QR Code reading (except NFC)
    INIC, // Initiator-contracted creditor
    APES, // Static QR Code via NFC
    APDN // Dynamic QR Code via NFC
}
