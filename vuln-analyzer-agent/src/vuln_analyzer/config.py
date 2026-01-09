"""Configuration management for the vulnerability analyzer."""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml


@dataclass
class MendConfig:
    """Mend.io API configuration."""
    api_key: str = ""
    user_key: str = ""
    org_token: str = ""
    url: str = "https://saas.mend.io"
    
    @property
    def is_configured(self) -> bool:
        return bool(self.api_key and self.user_key and self.org_token)


@dataclass
class NvdConfig:
    """NVD API configuration."""
    api_key: str = ""
    
    @property
    def is_configured(self) -> bool:
        return bool(self.api_key)


@dataclass
class OwaspConfig:
    """OWASP Dependency-Check configuration."""
    path: str = ""
    nvd_api_key: str = ""


@dataclass
class ThresholdsConfig:
    """Analysis thresholds configuration."""
    fail_on_cvss: float = 7.0


@dataclass
class Config:
    """Main configuration class."""
    mend: MendConfig = field(default_factory=MendConfig)
    nvd: NvdConfig = field(default_factory=NvdConfig)
    owasp: OwaspConfig = field(default_factory=OwaspConfig)
    thresholds: ThresholdsConfig = field(default_factory=ThresholdsConfig)
    suppressions: list[str] = field(default_factory=list)
    
    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "Config":
        """Load configuration from file and environment variables."""
        config = cls()
        
        # Try to load from file
        if config_path and config_path.exists():
            config = cls._load_from_file(config_path)
        else:
            # Try default locations
            for path in [
                Path.cwd() / "config.yaml",
                Path.cwd() / "config.yml",
                Path.home() / ".vuln-analyzer" / "config.yaml",
            ]:
                if path.exists():
                    config = cls._load_from_file(path)
                    break
        
        # Override with environment variables
        config._load_from_env()
        
        return config
    
    @classmethod
    def _load_from_file(cls, path: Path) -> "Config":
        """Load configuration from YAML file."""
        with open(path) as f:
            data = yaml.safe_load(f) or {}
        
        mend_data = data.get("mend", {})
        nvd_data = data.get("nvd", {})
        owasp_data = data.get("owasp", {})
        thresholds_data = data.get("thresholds", {})
        
        return cls(
            mend=MendConfig(
                api_key=mend_data.get("api_key", ""),
                user_key=mend_data.get("user_key", ""),
                org_token=mend_data.get("org_token", ""),
                url=mend_data.get("url", "https://saas.mend.io"),
            ),
            nvd=NvdConfig(
                api_key=nvd_data.get("api_key", ""),
            ),
            owasp=OwaspConfig(
                path=owasp_data.get("path", ""),
                nvd_api_key=owasp_data.get("nvd_api_key", ""),
            ),
            thresholds=ThresholdsConfig(
                fail_on_cvss=thresholds_data.get("fail_on_cvss", 7.0),
            ),
            suppressions=data.get("suppressions", []),
        )
    
    def _load_from_env(self) -> None:
        """Override configuration with environment variables."""
        # Mend
        if api_key := os.getenv("MEND_API_KEY"):
            self.mend.api_key = api_key
        if user_key := os.getenv("MEND_USER_KEY"):
            self.mend.user_key = user_key
        if org_token := os.getenv("MEND_ORG_TOKEN"):
            self.mend.org_token = org_token
        if url := os.getenv("MEND_URL"):
            self.mend.url = url
            
        # NVD
        if nvd_key := os.getenv("NVD_API_KEY"):
            self.nvd.api_key = nvd_key
            
        # OWASP
        if owasp_path := os.getenv("DEPENDENCY_CHECK_PATH"):
            self.owasp.path = owasp_path
        if owasp_nvd_key := os.getenv("DEPENDENCY_CHECK_NVD_API_KEY"):
            self.owasp.nvd_api_key = owasp_nvd_key
            
        # Thresholds
        if fail_cvss := os.getenv("VULN_FAIL_ON_CVSS"):
            try:
                self.thresholds.fail_on_cvss = float(fail_cvss)
            except ValueError:
                pass
