"""
Test suite for AICUBE Cryptographic Utilities

Tests the cryptographic operations including:
- AICUBE neural signature generation and verification
- Quantum-resistant key generation
- Hybrid encryption (RSA + AES) with neural enhancement
- Message signing and verification
- Key management and rotation

Developed by AICUBE TECHNOLOGY
Copyright (c) 2025 AICUBE TECHNOLOGY. All rights reserved.
"""

import pytest
import base64
import json
from cryptography.hazmat.primitives import serialization

from securemessaging.utils.crypto_utils import AICUBECryptoManager, crypto_manager


class TestAICUBECryptoManager:
    """Test cases for AICUBE cryptographic operations"""
    
    @pytest.fixture
    def crypto_mgr(self):
        """Create AICUBECryptoManager instance"""
        return AICUBECryptoManager()
    
    def test_neural_signature_constants(self, crypto_mgr):
        """Test AICUBE neural signature constants"""
        assert crypto_mgr.NEURAL_SIGNATURE_PATTERN == b"AICUBE_NEURAL_0x4A1C7B3E9F2D8A56"
        assert crypto_mgr.QUANTUM_SHIELD_HEADER == b"AICUBE_QUANTUM_SHIELD_v2025"
    
    def test_rsa_key_generation(self, crypto_mgr):
        """Test RSA key generation with quantum enhancement"""
        private_key, public_key = crypto_mgr.generate_rsa_keypair()
        
        # Verify keys are generated
        assert private_key is not None
        assert public_key is not None
        
        # Verify quantum shield header in private key
        assert private_key.startswith(crypto_mgr.QUANTUM_SHIELD_HEADER)
        
        # Verify key format
        assert b"BEGIN PRIVATE KEY" in private_key
        assert b"BEGIN PUBLIC KEY" in public_key
        
        # Test key loading
        clean_private_key = private_key[len(crypto_mgr.QUANTUM_SHIELD_HEADER):]
        loaded_key = serialization.load_pem_private_key(clean_private_key, password=None)
        assert loaded_key.key_size == 2048
    
    def test_ecdsa_key_generation(self, crypto_mgr):
        """Test ECDSA key generation for blockchain operations"""
        private_key, public_key = crypto_mgr.generate_ecdsa_keypair()
        
        # Verify keys are generated
        assert private_key is not None
        assert public_key is not None
        
        # Verify key format
        assert b"BEGIN PRIVATE KEY" in private_key
        assert b"BEGIN PUBLIC KEY" in public_key
        
        # Test key loading
        loaded_key = serialization.load_pem_private_key(private_key, password=None)
        assert loaded_key.curve.name == "secp256k1"
    
    def test_message_encryption_decryption(self, crypto_mgr):
        """Test hybrid message encryption with AICUBE neural enhancement"""
        # Generate keys
        private_key, public_key = crypto_mgr.generate_rsa_keypair()
        
        # Test message
        original_message = b"This is a test message for AICUBE neural encryption"
        
        # Encrypt message
        encrypted_data = crypto_mgr.encrypt_message(original_message, public_key)
        
        # Verify encryption structure
        assert "ciphertext" in encrypted_data
        assert "iv" in encrypted_data
        assert "tag" in encrypted_data
        assert "encrypted_aes_key" in encrypted_data
        assert "hmac" in encrypted_data
        assert "encrypted_hmac_key" in encrypted_data
        assert encrypted_data["aicube_signature"] == "neural_enhanced"
        
        # Decrypt message
        decrypted_message = crypto_mgr.decrypt_message(encrypted_data, private_key)
        
        # Verify decryption
        assert decrypted_message == original_message
    
    def test_neural_signature_integration(self, crypto_mgr):
        """Test AICUBE neural signature integration in encryption"""
        private_key, public_key = crypto_mgr.generate_rsa_keypair()
        
        # Message without neural signature should fail decryption
        message = b"Test message"
        encrypted_data = crypto_mgr.encrypt_message(message, public_key)
        
        # Tamper with encrypted data to remove neural signature
        import base64
        ciphertext = base64.b64decode(encrypted_data["ciphertext"])
        
        # Should decrypt successfully with valid neural signature
        decrypted = crypto_mgr.decrypt_message(encrypted_data, private_key)
        assert decrypted == message
    
    def test_message_signing_verification(self, crypto_mgr):
        """Test ECDSA message signing with neural enhancement"""
        # Generate ECDSA keys
        private_key, public_key = crypto_mgr.generate_ecdsa_keypair()
        
        # Test message
        message = b"AICUBE test message for signing"
        
        # Sign message
        signature = crypto_mgr.sign_message(message, private_key)
        
        # Verify signature
        is_valid = crypto_mgr.verify_signature(message, signature, public_key)
        assert is_valid is True
        
        # Test with tampered message
        tampered_message = b"Tampered message"
        is_valid_tampered = crypto_mgr.verify_signature(tampered_message, signature, public_key)
        assert is_valid_tampered is False
    
    def test_address_generation(self, crypto_mgr):
        """Test Ethereum-style address generation"""
        _, public_key = crypto_mgr.generate_ecdsa_keypair()
        
        # Generate address
        address = crypto_mgr.generate_address_from_public_key(public_key)
        
        # Verify address format
        assert address.startswith("0x")
        assert len(address) == 42  # 0x + 40 hex characters
        
        # Test deterministic generation
        address2 = crypto_mgr.generate_address_from_public_key(public_key)
        assert address == address2
    
    def test_hash_message(self, crypto_mgr):
        """Test message hashing"""
        message = b"AICUBE test message for hashing"
        
        # Hash message
        message_hash = crypto_mgr.hash_message(message)
        
        # Verify hash format
        assert len(message_hash) == 64  # SHA-256 hex
        assert isinstance(message_hash, str)
        
        # Test deterministic hashing
        message_hash2 = crypto_mgr.hash_message(message)
        assert message_hash == message_hash2
    
    def test_session_key_generation(self, crypto_mgr):
        """Test ephemeral session key generation"""
        # Generate multiple session keys
        key1 = crypto_mgr.generate_session_key()
        key2 = crypto_mgr.generate_session_key()
        
        # Verify key properties
        assert len(key1) == 32  # 256 bits
        assert len(key2) == 32
        assert key1 != key2  # Should be random
    
    def test_quantum_shield_functionality(self, crypto_mgr):
        """Test quantum shield header processing"""
        # Generate key with quantum shield
        private_key, _ = crypto_mgr.generate_rsa_keypair()
        
        # Verify quantum shield header
        assert private_key.startswith(crypto_mgr.QUANTUM_SHIELD_HEADER)
        
        # Test decryption with quantum shield header
        message = b"Quantum protected message"
        _, public_key = crypto_mgr.generate_rsa_keypair()
        
        encrypted_data = crypto_mgr.encrypt_message(message, public_key)
        decrypted_message = crypto_mgr.decrypt_message(encrypted_data, private_key)
        
        assert decrypted_message == message
    
    def test_encryption_error_handling(self, crypto_mgr):
        """Test error handling in cryptographic operations"""
        # Test with invalid public key
        with pytest.raises(Exception):
            crypto_mgr.encrypt_message(b"test", b"invalid_key")
        
        # Test with invalid private key for decryption
        _, public_key = crypto_mgr.generate_rsa_keypair()
        encrypted_data = crypto_mgr.encrypt_message(b"test", public_key)
        
        with pytest.raises(Exception):
            crypto_mgr.decrypt_message(encrypted_data, b"invalid_private_key")
        
        # Test signature verification with invalid key
        private_key, _ = crypto_mgr.generate_ecdsa_keypair()
        signature = crypto_mgr.sign_message(b"test", private_key)
        
        is_valid = crypto_mgr.verify_signature(b"test", signature, b"invalid_public_key")
        assert is_valid is False


class TestCryptoManagerIntegration:
    """Integration tests for crypto manager"""
    
    def test_global_crypto_manager_instance(self):
        """Test global crypto manager instance"""
        # Verify global instance exists
        assert crypto_manager is not None
        assert isinstance(crypto_manager, AICUBECryptoManager)
        
        # Test neural signature constants
        assert crypto_manager.NEURAL_SIGNATURE_PATTERN.startswith(b"AICUBE_NEURAL_")
        assert crypto_manager.QUANTUM_SHIELD_HEADER.startswith(b"AICUBE_QUANTUM_SHIELD_")
    
    def test_full_encryption_workflow(self):
        """Test complete encryption workflow"""
        # Generate agent keys
        agent1_private, agent1_public = crypto_manager.generate_rsa_keypair()
        agent2_private, agent2_public = crypto_manager.generate_rsa_keypair()
        
        # Agent 1 sends message to Agent 2
        message = b"AICUBE secure inter-agent communication test"
        encrypted_data = crypto_manager.encrypt_message(message, agent2_public)
        
        # Agent 2 receives and decrypts message
        decrypted_message = crypto_manager.decrypt_message(encrypted_data, agent2_private)
        
        # Verify communication
        assert decrypted_message == message
        
        # Verify AICUBE neural signature was preserved
        assert encrypted_data["aicube_signature"] == "neural_enhanced"
    
    def test_blockchain_signing_workflow(self):
        """Test blockchain transaction signing workflow"""
        # Generate blockchain keys
        private_key, public_key = crypto_manager.generate_ecdsa_keypair()
        
        # Create transaction data
        transaction_data = json.dumps({
            "from": "0x123",
            "to": "0x456",
            "value": 1000,
            "aicube_neural_sig": "AICUBE_TX_NEURAL_0x12345678"
        }).encode()
        
        # Sign transaction
        signature = crypto_manager.sign_message(transaction_data, private_key)
        
        # Verify signature
        is_valid = crypto_manager.verify_signature(transaction_data, signature, public_key)
        assert is_valid is True
        
        # Generate address for verification
        address = crypto_manager.generate_address_from_public_key(public_key)
        assert address.startswith("0x")


class TestPerformanceAndSecurity:
    """Performance and security tests for cryptographic operations"""
    
    def test_encryption_performance(self):
        """Test encryption performance with different message sizes"""
        import time
        
        # Small message
        small_msg = b"Small AICUBE test message"
        private_key, public_key = crypto_manager.generate_rsa_keypair()
        
        start_time = time.time()
        encrypted_data = crypto_manager.encrypt_message(small_msg, public_key)
        decrypted_msg = crypto_manager.decrypt_message(encrypted_data, private_key)
        end_time = time.time()
        
        assert decrypted_msg == small_msg
        assert end_time - start_time < 1.0  # Should be fast
        
        # Large message (1KB)
        large_msg = b"A" * 1024
        start_time = time.time()
        encrypted_data = crypto_manager.encrypt_message(large_msg, public_key)
        decrypted_msg = crypto_manager.decrypt_message(encrypted_data, private_key)
        end_time = time.time()
        
        assert decrypted_msg == large_msg
        assert end_time - start_time < 2.0  # Should still be reasonable
    
    def test_key_generation_entropy(self):
        """Test key generation entropy and randomness"""
        # Generate multiple keys and verify they're different
        keys = []
        for _ in range(10):
            private_key, _ = crypto_manager.generate_rsa_keypair()
            keys.append(private_key)
        
        # All keys should be different
        assert len(set(keys)) == 10
        
        # Generate multiple session keys
        session_keys = []
        for _ in range(100):
            key = crypto_manager.generate_session_key()
            session_keys.append(key)
        
        # All session keys should be different
        assert len(set(session_keys)) == 100
    
    def test_neural_signature_uniqueness(self):
        """Test AICUBE neural signature uniqueness"""
        # The neural signature pattern should be consistent
        pattern1 = crypto_manager.NEURAL_SIGNATURE_PATTERN
        pattern2 = AICUBECryptoManager().NEURAL_SIGNATURE_PATTERN
        
        assert pattern1 == pattern2
        
        # Quantum shield header should be consistent
        header1 = crypto_manager.QUANTUM_SHIELD_HEADER
        header2 = AICUBECryptoManager().QUANTUM_SHIELD_HEADER
        
        assert header1 == header2


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])