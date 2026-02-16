package com.hlaff.wallet_api.mapper;

import org.mapstruct.MapperConfig;
import org.mapstruct.ReportingPolicy;

@MapperConfig(
        componentModel = "spring",
        unmappedTargetPolicy = ReportingPolicy.IGNORE   // ignora campos não mapeados
)
public interface BaseMapperConfig {
}
