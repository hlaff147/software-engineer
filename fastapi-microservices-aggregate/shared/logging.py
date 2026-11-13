"""Structured logging configuration for microservices."""

from __future__ import annotations

import logging
import sys

__all__ = ["configure_logging", "get_logger"]


def configure_logging(service_name: str, level: int = logging.INFO) -> logging.Logger:
    """Configures structured console logging for the given service."""
    logger = logging.getLogger(service_name)
    logger.setLevel(level)

    # Avoid duplicate handlers if called multiple times
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        formatter = logging.Formatter(
            fmt='{"timestamp":"%(asctime)s","service":"%(name)s","level":"%(levelname)s","message":"%(message)s"}',
            datefmt="%Y-%m-%dT%H:%M:%S%z",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.propagate = False
    return logger


def get_logger(service_name: str) -> logging.Logger:
    """Retrieves or configures a logger for the given service."""
    return logging.getLogger(service_name)
