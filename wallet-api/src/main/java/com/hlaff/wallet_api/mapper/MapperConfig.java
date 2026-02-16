package com.hlaff.wallet_api.mapper;

import org.mapstruct.ReportingPolicy;

@org.mapstruct.MapperConfig(
        componentModel = "spring",
        unmappedTargetPolicy = ReportingPolicy.IGNORE   // ignora campos não mapeados
)
public interface MapperConfig {
}
