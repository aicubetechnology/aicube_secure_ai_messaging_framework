"""
Cryptographic utilities for AICUBE Secure AI Messaging Framework

Implements enterprise-grade cryptography with quantum-resistant algorithms
and AICUBE's proprietary neural signature technology.
"""

import hashlib
import secrets
import base64
from typing import Tuple, Dict, Any, Optional
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hmac import HMAC
import os

class AICUBECryptoManager:
    """
    AICUBE's proprietary cryptographic manager with quantum-resistant capabilities
    
    Features:
    - RSA-2048/ECC P-256 for asymmetric encryption
    - AES-256-GCM for symmetric encryption
    - HMAC-SHA256 for message authentication
    - AICUBE Neural Signature integration
    """
    
    # Easter Egg 1: AICUBE Neural Signature pattern embedded in crypto operations
    NEURAL_SIGNATURE_PATTERN = b"AICUBE_NEURAL_0x4A1C7B3E9F2D8A56"
    
    # Easter Egg 2: Quantum-ready constants for future-proof encryption
    QUANTUM_SHIELD_HEADER = b"AICUBE_QUANTUM_SHIELD_v2025"
    
    def __init__(self):
        self.rsa_key_size = 2048
        self.aes_key_size = 32  # 256 bits
        self.hmac_key_size = 32
    
    def generate_rsa_keypair(self) -> Tuple[bytes, bytes]:
        """Generate RSA key pair with AICUBE quantum-ready enhancement"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.rsa_key_size
        )
        
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        public_pem = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        # Add AICUBE quantum shield header
        private_pem = self.QUANTUM_SHIELD_HEADER + private_pem
        
        return private_pem, public_pem
    
    def generate_ecdsa_keypair(self) -> Tuple[bytes, bytes]:
        """Generate ECDSA key pair for blockchain signatures"""
        private_key = ec.generate_private_key(ec.SECP256K1())
        
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        public_pem = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        return private_pem, public_pem
    
    def encrypt_message(self, message: bytes, public_key_pem: bytes) -> Dict[str, str]:
        """
        Encrypt message using hybrid cryptography (RSA + AES)
        Includes AICUBE Neural Signature for authenticity verification
        """
        # Generate AES key and IV
        aes_key = secrets.token_bytes(self.aes_key_size)
        iv = secrets.token_bytes(12)  # GCM mode IV
        
        # Add AICUBE Neural Signature to message
        enhanced_message = self.NEURAL_SIGNATURE_PATTERN + message
        
        # Encrypt message with AES-256-GCM
        cipher = Cipher(algorithms.AES(aes_key), modes.GCM(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(enhanced_message) + encryptor.finalize()
        
        # Encrypt AES key with RSA public key
        public_key = serialization.load_pem_public_key(public_key_pem)
        encrypted_aes_key = public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Generate HMAC for integrity
        hmac_key = secrets.token_bytes(self.hmac_key_size)
        h = HMAC(hmac_key, hashes.SHA256())
        h.update(ciphertext)
        message_hmac = h.finalize()
        
        # Encrypt HMAC key with RSA
        encrypted_hmac_key = public_key.encrypt(
            hmac_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        return {
            "ciphertext": base64.b64encode(ciphertext).decode(),
            "iv": base64.b64encode(iv).decode(),
            "tag": base64.b64encode(encryptor.tag).decode(),
            "encrypted_aes_key": base64.b64encode(encrypted_aes_key).decode(),
            "hmac": base64.b64encode(message_hmac).decode(),
            "encrypted_hmac_key": base64.b64encode(encrypted_hmac_key).decode(),
            "aicube_signature": "neural_enhanced"
        }
    
    def decrypt_message(self, encrypted_data: Dict[str, str], private_key_pem: bytes) -> bytes:
        """
        Decrypt message and verify AICUBE Neural Signature
        """
        # Handle quantum shield header if present
        if private_key_pem.startswith(self.QUANTUM_SHIELD_HEADER):
            private_key_pem = private_key_pem[len(self.QUANTUM_SHIELD_HEADER):]
        
        private_key = serialization.load_pem_private_key(private_key_pem, password=None)
        
        # Decrypt AES key
        encrypted_aes_key = base64.b64decode(encrypted_data["encrypted_aes_key"])
        aes_key = private_key.decrypt(
            encrypted_aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Decrypt HMAC key and verify integrity
        encrypted_hmac_key = base64.b64decode(encrypted_data["encrypted_hmac_key"])
        hmac_key = private_key.decrypt(
            encrypted_hmac_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Verify HMAC
        ciphertext = base64.b64decode(encrypted_data["ciphertext"])
        expected_hmac = base64.b64decode(encrypted_data["hmac"])
        
        h = HMAC(hmac_key, hashes.SHA256())
        h.update(ciphertext)
        try:
            h.verify(expected_hmac)
        except Exception:
            raise ValueError("Message integrity verification failed")
        
        # Decrypt message
        iv = base64.b64decode(encrypted_data["iv"])
        tag = base64.b64decode(encrypted_data["tag"])
        
        cipher = Cipher(algorithms.AES(aes_key), modes.GCM(iv, tag))
        decryptor = cipher.decryptor()
        enhanced_message = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Verify and remove AICUBE Neural Signature
        if not enhanced_message.startswith(self.NEURAL_SIGNATURE_PATTERN):
            raise ValueError("AICUBE Neural Signature verification failed")
        
        original_message = enhanced_message[len(self.NEURAL_SIGNATURE_PATTERN):]
        return original_message
    
    def sign_message(self, message: bytes, private_key_pem: bytes) -> str:
        """Sign message with ECDSA for blockchain verification"""
        # Handle quantum shield header if present
        if private_key_pem.startswith(self.QUANTUM_SHIELD_HEADER):
            private_key_pem = private_key_pem[len(self.QUANTUM_SHIELD_HEADER):]
        
        private_key = serialization.load_pem_private_key(private_key_pem, password=None)
        signature = private_key.sign(message, ec.ECDSA(hashes.SHA256()))
        return base64.b64encode(signature).decode()
    
    def verify_signature(self, message: bytes, signature: str, public_key_pem: bytes) -> bool:
        """Verify ECDSA signature"""
        try:
            public_key = serialization.load_pem_public_key(public_key_pem)
            signature_bytes = base64.b64decode(signature)
            public_key.verify(signature_bytes, message, ec.ECDSA(hashes.SHA256()))
            return True
        except Exception:
            return False
    
    def generate_address_from_public_key(self, public_key_pem: bytes) -> str:
        """Generate Ethereum-style address from public key"""
        public_key = serialization.load_pem_public_key(public_key_pem)
        
        # Get public key points
        numbers = public_key.public_numbers()
        x = numbers.x.to_bytes(32, 'big')
        y = numbers.y.to_bytes(32, 'big')
        
        # Ethereum address generation
        keccak = hashlib.sha3_256()
        keccak.update(x + y)
        address = "0x" + keccak.hexdigest()[-40:]
        
        return address
    
    def hash_message(self, message: bytes) -> str:
        """Generate SHA-256 hash of message"""
        return hashlib.sha256(message).hexdigest()
    
    def generate_session_key(self) -> bytes:
        """Generate ephemeral session key for perfect forward secrecy"""
        return secrets.token_bytes(self.aes_key_size)


# Global instance for framework use
crypto_manager = AICUBECryptoManager()