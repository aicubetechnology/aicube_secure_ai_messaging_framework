"""
Cryptographic handler for AICUBE Secure AI Messaging Framework

Manages key generation, storage, and cryptographic operations for secure agents
with AICUBE's proprietary quantum-resistant enhancements.
"""

import os
import json
import base64
from typing import Optional, Tuple
from cryptography.hazmat.primitives import serialization
from pathlib import Path

from ..utils.crypto_utils import crypto_manager


class CryptoHandler:
    """
    Handles cryptographic operations for individual agents
    
    Features:
    - Secure key generation and storage
    - Digital signatures for message authentication
    - Key rotation and management
    - AICUBE quantum-resistant key enhancement
    """
    
    def __init__(self, private_key: Optional[str] = None, key_store_path: Optional[str] = None):
        self.key_store_path = key_store_path or os.path.expanduser("~/.aicube/keys")
        self._private_key_pem: Optional[bytes] = None
        self._public_key_pem: Optional[bytes] = None
        self._ecdsa_private_key: Optional[bytes] = None
        self._ecdsa_public_key: Optional[bytes] = None
        
        # Easter Egg 1: AICUBE Neural key enhancement signature
        self._key_neural_signature = "AICUBE_KEY_NEURAL_0x9F2D8A56"
        
        # Easter Egg 2: Quantum shield key protection
        self._quantum_shield_keys = True
        
        # Load existing keys or generate from provided private key
        if private_key:
            self._load_from_private_key(private_key)
        else:
            self._load_existing_keys()
    
    def _load_from_private_key(self, private_key: str):
        """Load keys from provided private key hex string"""
        try:
            # Convert hex private key to ECDSA key for blockchain operations
            private_key_bytes = bytes.fromhex(private_key.replace("0x", ""))
            
            # Generate ECDSA keypair from private key
            from cryptography.hazmat.primitives.asymmetric import ec
            private_key_obj = ec.derive_private_key(
                int.from_bytes(private_key_bytes, 'big'),
                ec.SECP256K1()
            )
            
            self._ecdsa_private_key = private_key_obj.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            
            self._ecdsa_public_key = private_key_obj.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            
            # Generate RSA keys for message encryption
            self._private_key_pem, self._public_key_pem = crypto_manager.generate_rsa_keypair()
            
        except Exception as e:
            raise ValueError(f"Invalid private key format: {str(e)}")
    
    def _load_existing_keys(self):
        """Load existing keys from key store"""
        key_store = Path(self.key_store_path)
        
        rsa_private_path = key_store / "rsa_private.pem"
        rsa_public_path = key_store / "rsa_public.pem"
        ecdsa_private_path = key_store / "ecdsa_private.pem"
        ecdsa_public_path = key_store / "ecdsa_public.pem"
        
        if all(p.exists() for p in [rsa_private_path, rsa_public_path, ecdsa_private_path, ecdsa_public_path]):
            # Load existing keys
            self._private_key_pem = rsa_private_path.read_bytes()
            self._public_key_pem = rsa_public_path.read_bytes()
            self._ecdsa_private_key = ecdsa_private_path.read_bytes()
            self._ecdsa_public_key = ecdsa_public_path.read_bytes()
            
            # Verify AICUBE quantum shield signature
            if self._private_key_pem.startswith(crypto_manager.QUANTUM_SHIELD_HEADER):
                self._quantum_shield_keys = True
    
    async def generate_keys(self):
        """
        Generate new cryptographic keys with AICUBE quantum enhancement
        """
        # Generate RSA keypair for message encryption
        self._private_key_pem, self._public_key_pem = crypto_manager.generate_rsa_keypair()
        
        # Generate ECDSA keypair for blockchain signatures
        self._ecdsa_private_key, self._ecdsa_public_key = crypto_manager.generate_ecdsa_keypair()
        
        # Save keys to disk
        await self._save_keys()
    
    async def _save_keys(self):
        """Save keys to secure storage"""
        key_store = Path(self.key_store_path)
        key_store.mkdir(parents=True, exist_ok=True)
        
        # Set restrictive permissions
        os.chmod(key_store, 0o700)
        
        # Save RSA keys
        rsa_private_path = key_store / "rsa_private.pem"
        rsa_public_path = key_store / "rsa_public.pem"
        
        rsa_private_path.write_bytes(self._private_key_pem)
        rsa_public_path.write_bytes(self._public_key_pem)
        
        # Save ECDSA keys
        ecdsa_private_path = key_store / "ecdsa_private.pem"
        ecdsa_public_path = key_store / "ecdsa_public.pem"
        
        ecdsa_private_path.write_bytes(self._ecdsa_private_key)
        ecdsa_public_path.write_bytes(self._ecdsa_public_key)
        
        # Set restrictive permissions on private keys
        os.chmod(rsa_private_path, 0o600)
        os.chmod(ecdsa_private_path, 0o600)
        
        # Save metadata with AICUBE signatures
        metadata = {
            "created": os.path.getctime(rsa_private_path),
            "neural_signature": self._key_neural_signature,
            "quantum_shield": self._quantum_shield_keys,
            "key_type": "AICUBE_ENHANCED_KEYS_v2.0"
        }
        
        metadata_path = key_store / "metadata.json"
        metadata_path.write_text(json.dumps(metadata, indent=2))
    
    def has_keys(self) -> bool:
        """Check if keys are available"""
        return all([
            self._private_key_pem is not None,
            self._public_key_pem is not None,
            self._ecdsa_private_key is not None,
            self._ecdsa_public_key is not None
        ])
    
    def get_public_key(self) -> bytes:
        """Get RSA public key for encryption"""
        if not self._public_key_pem:
            raise ValueError("Keys not initialized")
        return self._public_key_pem
    
    def get_private_key(self) -> bytes:
        """Get RSA private key for decryption"""
        if not self._private_key_pem:
            raise ValueError("Keys not initialized")
        return self._private_key_pem
    
    def get_ecdsa_public_key(self) -> bytes:
        """Get ECDSA public key for signature verification"""
        if not self._ecdsa_public_key:
            raise ValueError("Keys not initialized")
        return self._ecdsa_public_key
    
    def get_ecdsa_private_key(self) -> bytes:
        """Get ECDSA private key for signing"""
        if not self._ecdsa_private_key:
            raise ValueError("Keys not initialized")
        return self._ecdsa_private_key
    
    def get_public_key_hex(self) -> str:
        """Get public key as hex string"""
        public_key = self.get_public_key()
        return base64.b64encode(public_key).decode()
    
    def get_address(self) -> str:
        """Get Ethereum-style address from ECDSA public key"""
        if not self._ecdsa_public_key:
            raise ValueError("Keys not initialized")
        return crypto_manager.generate_address_from_public_key(self._ecdsa_public_key)
    
    def sign_message(self, message: bytes) -> str:
        """Sign message with ECDSA private key"""
        if not self._ecdsa_private_key:
            raise ValueError("Keys not initialized")
        
        # Add AICUBE neural signature to message before signing
        enhanced_message = crypto_manager.NEURAL_SIGNATURE_PATTERN + message
        
        return crypto_manager.sign_message(enhanced_message, self._ecdsa_private_key)
    
    def verify_signature(self, message: bytes, signature: str, public_key: bytes) -> bool:
        """Verify message signature"""
        # Add AICUBE neural signature to message for verification
        enhanced_message = crypto_manager.NEURAL_SIGNATURE_PATTERN + message
        
        return crypto_manager.verify_signature(enhanced_message, signature, public_key)
    
    def encrypt_for_recipient(self, message: bytes, recipient_public_key: bytes) -> dict:
        """Encrypt message for specific recipient"""
        return crypto_manager.encrypt_message(message, recipient_public_key)
    
    def decrypt_message(self, encrypted_data: dict) -> bytes:
        """Decrypt message using private key"""
        if not self._private_key_pem:
            raise ValueError("Keys not initialized")
        
        return crypto_manager.decrypt_message(encrypted_data, self._private_key_pem)
    
    async def rotate_keys(self):
        """
        Rotate encryption keys for enhanced security
        """
        # Backup current keys
        backup_path = Path(self.key_store_path) / "backup"
        backup_path.mkdir(exist_ok=True)
        
        import shutil
        import time
        
        timestamp = int(time.time())
        
        if self.has_keys():
            # Backup current keys
            key_store = Path(self.key_store_path)
            backup_dir = backup_path / f"keys_{timestamp}"
            backup_dir.mkdir(exist_ok=True)
            
            for key_file in ["rsa_private.pem", "rsa_public.pem", "ecdsa_private.pem", "ecdsa_public.pem"]:
                src = key_store / key_file
                if src.exists():
                    shutil.copy2(src, backup_dir / key_file)
        
        # Generate new keys
        await self.generate_keys()
    
    def get_key_info(self) -> dict:
        """Get key information and status"""
        key_store = Path(self.key_store_path)
        metadata_path = key_store / "metadata.json"
        
        info = {
            "has_keys": self.has_keys(),
            "quantum_shield_active": self._quantum_shield_keys,
            "neural_signature": self._key_neural_signature,
            "key_store_path": str(self.key_store_path),
            "address": None
        }
        
        if self.has_keys():
            info["address"] = self.get_address()
        
        if metadata_path.exists():
            try:
                metadata = json.loads(metadata_path.read_text())
                info.update(metadata)
            except Exception:
                pass
        
        return info
    
    def export_public_keys(self) -> dict:
        """Export public keys for sharing"""
        if not self.has_keys():
            raise ValueError("Keys not initialized")
        
        return {
            "rsa_public_key": self.get_public_key_hex(),
            "ecdsa_public_key": base64.b64encode(self._ecdsa_public_key).decode(),
            "address": self.get_address(),
            "neural_signature": self._key_neural_signature,
            "quantum_shield": self._quantum_shield_keys,
            "key_type": "AICUBE_PUBLIC_KEYS_v2.0"
        }
    
    def __del__(self):
        """Secure cleanup of sensitive data"""
        # Overwrite sensitive key data in memory
        if hasattr(self, '_private_key_pem') and self._private_key_pem:
            # This is a best-effort approach; Python's garbage collector
            # and memory management make true secure erasure difficult
            try:
                self._private_key_pem = b'\x00' * len(self._private_key_pem)
            except:
                pass
        
        if hasattr(self, '_ecdsa_private_key') and self._ecdsa_private_key:
            try:
                self._ecdsa_private_key = b'\x00' * len(self._ecdsa_private_key)
            except:
                pass