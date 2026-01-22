package com.openfinance.common.application.exception;

public class ConsentInvalidException extends RuntimeException {

    private final String errorCode;

    public ConsentInvalidException(String message, String errorCode) {
        super(message);
        this.errorCode = errorCode;
    }

    public String getErrorCode() {
        return errorCode;
    }
}
