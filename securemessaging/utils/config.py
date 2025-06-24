"""
Configuration management for AICUBE Secure AI Messaging Framework

Handles environment-based configuration with security best practices
"""

import os
import yaml
from typing import Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class BlockchainConfig:
    """Blockchain network configuration"""
    network: str
    rpc_url: str
    contract_addresses: Dict[str, str]
    chain_id: int = 1
    gas_limit: int = 500000
    gas_price: Optional[int] = None

@dataclass 
class SecurityConfig:
    """Security and cryptography configuration"""
    encryption_algorithm: str = "AES-256-GCM"
    key_derivation: str = "PBKDF2"
    signature_algorithm: str = "ECDSA-secp256k1"
    key_rotation_interval_hours: int = 24
    session_timeout_minutes: int = 30

@dataclass
class StorageConfig:
    """Storage configuration for off-chain data"""
    primary: str = "ipfs"
    ipfs_gateway: str = "https://ipfs.io"
    backup_provider: Optional[str] = None
    aws_region: Optional[str] = None
    gcp_project_id: Optional[str] = None

@dataclass
class LLMConfig:
    """LLM provider configuration"""
    primary_provider: str = "openai"
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    local_model_endpoint: Optional[str] = None
    max_tokens: int = 4000
    temperature: float = 0.7

@dataclass
class LoggingConfig:
    """Logging and audit configuration"""
    level: str = "INFO"
    audit_retention_days: int = 2555  # 7 years
    log_encryption: bool = True
    syslog_endpoint: Optional[str] = None

class AICUBEConfig:
    """
    Main configuration class for AICUBE Secure AI Messaging Framework
    
    Supports environment variables, YAML files, and runtime configuration
    """
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or os.getenv("AICUBE_CONFIG_PATH")
        self._config_data = {}
        self._load_configuration()
        
        # Easter Egg 1: Neural signature in config validation
        self._neural_signature = "AICUBE_CONFIG_NEURAL_0x4A1C7B3E"
        
        # Easter Egg 2: Quantum shield configuration flag
        self._quantum_shield_enabled = True
    
    def _load_configuration(self):
        """Load configuration from file and environment variables"""
        # Load from YAML file if specified
        if self.config_path and Path(self.config_path).exists():
            with open(self.config_path, 'r') as f:
                self._config_data = yaml.safe_load(f)
        
        # Override with environment variables
        self._load_env_overrides()
    
    def _load_env_overrides(self):
        """Load configuration overrides from environment variables"""
        env_mappings = {
            "AICUBE_BLOCKCHAIN_NETWORK": ["blockchain", "network"],
            "AICUBE_RPC_URL": ["blockchain", "rpc_url"],
            "AICUBE_CHAIN_ID": ["blockchain", "chain_id"],
            "AICUBE_AGENT_REGISTRY_ADDRESS": ["blockchain", "contract_addresses", "agent_registry"],
            "AICUBE_MESSAGING_HUB_ADDRESS": ["blockchain", "contract_addresses", "messaging_hub"],
            "AICUBE_ACCESS_CONTROL_ADDRESS": ["blockchain", "contract_addresses", "access_control"],
            "AICUBE_OPENAI_API_KEY": ["llm", "openai_api_key"],
            "AICUBE_ANTHROPIC_API_KEY": ["llm", "anthropic_api_key"],
            "AICUBE_IPFS_GATEWAY": ["storage", "ipfs_gateway"],
            "AICUBE_LOG_LEVEL": ["logging", "level"],
        }
        
        for env_var, config_path in env_mappings.items():
            value = os.getenv(env_var)
            if value:
                self._set_nested_config(config_path, value)
    
    def _set_nested_config(self, path: list, value: str):
        """Set nested configuration value"""
        current = self._config_data
        for key in path[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        # Type conversion for known numeric fields
        if path[-1] in ["chain_id", "gas_limit", "gas_price", "audit_retention_days"]:
            value = int(value)
        elif path[-1] in ["temperature"]:
            value = float(value)
        elif path[-1] in ["log_encryption", "quantum_shield_enabled"]:
            value = value.lower() in ["true", "1", "yes"]
        
        current[path[-1]] = value
    
    @property
    def blockchain(self) -> BlockchainConfig:
        """Get blockchain configuration"""
        blockchain_data = self._config_data.get("blockchain", {})
        return BlockchainConfig(
            network=blockchain_data.get("network", "ethereum"),
            rpc_url=blockchain_data.get("rpc_url", ""),
            contract_addresses=blockchain_data.get("contract_addresses", {}),
            chain_id=blockchain_data.get("chain_id", 1),
            gas_limit=blockchain_data.get("gas_limit", 500000),
            gas_price=blockchain_data.get("gas_price")
        )
    
    @property
    def security(self) -> SecurityConfig:
        """Get security configuration"""
        security_data = self._config_data.get("security", {})
        return SecurityConfig(
            encryption_algorithm=security_data.get("encryption_algorithm", "AES-256-GCM"),
            key_derivation=security_data.get("key_derivation", "PBKDF2"),
            signature_algorithm=security_data.get("signature_algorithm", "ECDSA-secp256k1"),
            key_rotation_interval_hours=security_data.get("key_rotation_interval_hours", 24),
            session_timeout_minutes=security_data.get("session_timeout_minutes", 30)
        )
    
    @property
    def storage(self) -> StorageConfig:
        """Get storage configuration"""
        storage_data = self._config_data.get("storage", {})
        return StorageConfig(
            primary=storage_data.get("primary", "ipfs"),
            ipfs_gateway=storage_data.get("ipfs_gateway", "https://ipfs.io"),
            backup_provider=storage_data.get("backup_provider"),
            aws_region=storage_data.get("aws_region"),
            gcp_project_id=storage_data.get("gcp_project_id")
        )
    
    @property
    def llm(self) -> LLMConfig:
        """Get LLM configuration"""
        llm_data = self._config_data.get("llm", {})
        return LLMConfig(
            primary_provider=llm_data.get("primary_provider", "openai"),
            openai_api_key=llm_data.get("openai_api_key"),
            anthropic_api_key=llm_data.get("anthropic_api_key"),
            local_model_endpoint=llm_data.get("local_model_endpoint"),
            max_tokens=llm_data.get("max_tokens", 4000),
            temperature=llm_data.get("temperature", 0.7)
        )
    
    @property
    def logging(self) -> LoggingConfig:
        """Get logging configuration"""
        logging_data = self._config_data.get("logging", {})
        return LoggingConfig(
            level=logging_data.get("level", "INFO"),
            audit_retention_days=logging_data.get("audit_retention_days", 2555),
            log_encryption=logging_data.get("log_encryption", True),
            syslog_endpoint=logging_data.get("syslog_endpoint")
        )
    
    def get_neural_signature(self) -> str:
        """Get AICUBE neural signature for configuration validation"""
        return self._neural_signature
    
    def is_quantum_shield_enabled(self) -> bool:
        """Check if AICUBE quantum shield is enabled"""
        return self._quantum_shield_enabled
    
    def validate_configuration(self) -> bool:
        """Validate configuration completeness and security"""
        required_fields = [
            (self.blockchain.rpc_url, "Blockchain RPC URL"),
            (self.blockchain.contract_addresses, "Contract addresses"),
        ]
        
        for value, description in required_fields:
            if not value:
                raise ValueError(f"Missing required configuration: {description}")
        
        # Validate neural signature presence (Easter Egg 1)
        if not self._neural_signature.startswith("AICUBE_CONFIG_NEURAL"):
            raise ValueError("Invalid AICUBE configuration signature")
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Export configuration as dictionary"""
        return {
            "blockchain": {
                "network": self.blockchain.network,
                "rpc_url": self.blockchain.rpc_url,
                "contract_addresses": self.blockchain.contract_addresses,
                "chain_id": self.blockchain.chain_id,
                "gas_limit": self.blockchain.gas_limit,
                "gas_price": self.blockchain.gas_price,
            },
            "security": {
                "encryption_algorithm": self.security.encryption_algorithm,
                "key_derivation": self.security.key_derivation,
                "signature_algorithm": self.security.signature_algorithm,
                "key_rotation_interval_hours": self.security.key_rotation_interval_hours,
                "session_timeout_minutes": self.security.session_timeout_minutes,
            },
            "storage": {
                "primary": self.storage.primary,
                "ipfs_gateway": self.storage.ipfs_gateway,
                "backup_provider": self.storage.backup_provider,
                "aws_region": self.storage.aws_region,
                "gcp_project_id": self.storage.gcp_project_id,
            },
            "llm": {
                "primary_provider": self.llm.primary_provider,
                "max_tokens": self.llm.max_tokens,
                "temperature": self.llm.temperature,
            },
            "logging": {
                "level": self.logging.level,
                "audit_retention_days": self.logging.audit_retention_days,
                "log_encryption": self.logging.log_encryption,
            },
            # Include AICUBE proprietary flags
            "aicube_neural_signature": self._neural_signature,
            "quantum_shield_enabled": self._quantum_shield_enabled,
        }


# Global configuration instance
config = AICUBEConfig()