"""
Test suite for AICUBE Secure AI Messaging Framework - SecureAgent

Tests the core SecureAgent functionality including:
- Agent registration and identity management
- Secure message sending and receiving
- Cryptographic operations with neural signatures
- LLM integration with Qube technologies
- Blockchain interaction and audit trails

Developed by AICUBE TECHNOLOGY
Copyright (c) 2025 AICUBE TECHNOLOGY. All rights reserved.
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime

from securemessaging import SecureAgent, EthereumClient
from securemessaging.agent.base_agent import AgentIdentity, Message
from securemessaging.utils.crypto_utils import crypto_manager


class TestSecureAgent:
    """Test cases for SecureAgent class with AICUBE enhancements"""
    
    @pytest.fixture
    def mock_ethereum_client(self):
        """Create mock Ethereum client"""
        client = Mock(spec=EthereumClient)
        client.register_agent = AsyncMock(return_value="0x1234567890abcdef")
        client.get_agent_info = AsyncMock(return_value={
            "address": "0xabcdef123456",
            "public_key": "mock_public_key",
            "is_active": True,
            "name": "TestAgent"
        })
        client.send_message = AsyncMock(return_value="0xmessage_tx_hash")
        client.listen_messages = AsyncMock()
        return client
    
    @pytest.fixture
    def secure_agent(self, mock_ethereum_client):
        """Create SecureAgent instance for testing"""
        return SecureAgent(
            name="TestAgent_AICUBE",
            blockchain_client=mock_ethereum_client,
            private_key="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
            llm_provider="openai",
            role="test_agent"
        )
    
    def test_agent_initialization(self, secure_agent):
        """Test agent initialization with AICUBE neural signatures"""
        assert secure_agent.name == "TestAgent_AICUBE"
        assert secure_agent.role == "test_agent"
        assert secure_agent._neural_signature.startswith("AICUBE_AGENT_")
        assert secure_agent._quantum_shield_active is True
        assert secure_agent.identity is None  # Not registered yet
    
    @pytest.mark.asyncio
    async def test_agent_registration(self, secure_agent, mock_ethereum_client):
        """Test agent registration on blockchain with AICUBE enhancements"""
        # Mock crypto handler methods
        with patch.object(secure_agent.crypto_handler, 'has_keys', return_value=False):
            with patch.object(secure_agent.crypto_handler, 'generate_keys', new_callable=AsyncMock):
                with patch.object(secure_agent.crypto_handler, 'get_public_key', return_value=b'mock_public_key'):
                    with patch.object(secure_agent.crypto_handler, 'get_public_key_hex', return_value='mock_hex_key'):
                        with patch.object(secure_agent.crypto_handler, 'sign_message', return_value='mock_signature'):
                            
                            # Register agent
                            tx_hash = await secure_agent.register()
                            
                            # Verify registration
                            assert tx_hash == "0x1234567890abcdef"
                            assert secure_agent.identity is not None
                            assert secure_agent.address is not None
                            
                            # Verify AICUBE neural signature in DID document
                            did_data = json.loads(secure_agent.identity.did_document)
                            assert "neural_signature" in did_data
                            assert did_data["neural_signature"].startswith("AICUBE_AGENT_")
                            assert did_data["quantum_shield"] is True
                            assert did_data["aicube_version"] == "2.0.0"
                            
                            # Verify blockchain client was called correctly  
                            mock_ethereum_client.register_agent.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_send_message_encrypted(self, secure_agent, mock_ethereum_client):
        """Test sending encrypted message with AICUBE neural enhancement"""
        # Setup agent identity
        secure_agent.identity = AgentIdentity(
            address="0x123",
            public_key=b"mock_key",
            did_document="{}",
            role="test",
            registration_time=datetime.utcnow()
        )
        secure_agent.address = "0x123"
        
        # Mock recipient info
        mock_ethereum_client.get_agent_info.return_value = {
            "address": "0x456",
            "public_key": "recipient_public_key",
            "is_active": True,
            "name": "RecipientAgent"
        }
        
        # Mock crypto operations
        with patch.object(crypto_manager, 'encrypt_message') as mock_encrypt:
            mock_encrypt.return_value = {
                "ciphertext": "encrypted_data",
                "aicube_signature": "neural_enhanced"
            }
            
            with patch.object(secure_agent.crypto_handler, 'sign_message', return_value='signature'):
                # Send message
                payload = {"test": "message", "amount": 100}
                message_id = await secure_agent.send_message(
                    recipient="0x456",
                    payload=payload,
                    encrypt=True
                )
                
                # Verify message was sent
                assert message_id.startswith("msg_")
                mock_ethereum_client.send_message.assert_called_once()
                
                # Verify AICUBE neural signature was added
                call_args = mock_ethereum_client.send_message.call_args
                metadata = call_args[1]["metadata"]
                assert "neural_signature" in metadata
                assert metadata["neural_signature"].startswith("AICUBE_AGENT_")
                assert metadata["quantum_protected"] is True
    
    @pytest.mark.asyncio
    async def test_message_verification(self, secure_agent):
        """Test message signature verification with AICUBE neural patterns"""
        # Mock message data
        message_data = {
            "id": "test_msg_001",
            "from": "0x123",
            "to": "0x456", 
            "payload": {"test": "data"},
            "timestamp": datetime.utcnow().isoformat(),
            "neural_signature": "AICUBE_AGENT_TestAgent_NEURAL_0x12345678",
            "signature": "mock_signature"
        }
        
        sender_public_key = "mock_sender_public_key"
        
        # Test signature verification
        with patch.object(crypto_manager, 'verify_signature', return_value=True):
            result = secure_agent._verify_message_signature(message_data.copy(), sender_public_key)
            assert result is True
        
        # Test invalid signature
        with patch.object(crypto_manager, 'verify_signature', return_value=False):
            result = secure_agent._verify_message_signature(message_data.copy(), sender_public_key)
            assert result is False
    
    @pytest.mark.asyncio
    async def test_llm_processing_with_qube_enhancement(self, secure_agent):
        """Test LLM processing with AICUBE Qube technologies"""
        # Mock LLM integrator
        mock_response = {
            "response": "Processed with AICUBE Qube LCM Model",
            "analysis": "Neural enhanced analysis",
            "qube_technologies": {
                "lcm_model_applied": True,
                "neural_memory_accessed": True
            }
        }
        
        with patch.object(secure_agent.llm_integrator, 'process_message', new_callable=AsyncMock) as mock_process:
            mock_process.return_value = mock_response
            
            # Process message
            payload = {"query": "Analyze this transaction", "amount": 50000}
            result = await secure_agent.process_with_llm(payload)
            
            # Verify AICUBE enhancement
            assert "aicube_enhancement" in result
            assert result["aicube_enhancement"]["neural_processed"] is True
            assert result["aicube_enhancement"]["quantum_verified"] is True
            assert result["aicube_enhancement"]["processing_agent"] == "TestAgent_AICUBE"
            
            # Verify original response is preserved
            assert result["response"] == mock_response["response"]
            assert result["qube_technologies"]["lcm_model_applied"] is True
    
    @pytest.mark.asyncio
    async def test_agent_identity_verification(self, secure_agent, mock_ethereum_client):
        """Test agent identity verification with AICUBE neural signatures"""
        # Mock agent info with AICUBE neural signature
        mock_ethereum_client.get_agent_info.return_value = {
            "address": "0x789",
            "is_active": True,
            "did_document": json.dumps({
                "neural_signature": "AICUBE_AGENT_VerifyAgent_NEURAL_0x87654321",
                "quantum_shield": True
            })
        }
        
        # Verify AICUBE agent
        result = await secure_agent.verify_agent_identity("0x789")
        assert result is True
        
        # Mock non-AICUBE agent
        mock_ethereum_client.get_agent_info.return_value = {
            "address": "0x999",
            "is_active": True,
            "did_document": json.dumps({
                "name": "StandardAgent"
            })
        }
        
        # Verify non-AICUBE agent (should still pass)
        result = await secure_agent.verify_agent_identity("0x999")
        assert result is True
        
        # Mock inactive agent
        mock_ethereum_client.get_agent_info.return_value = {
            "address": "0x000",
            "is_active": False
        }
        
        # Verify inactive agent
        result = await secure_agent.verify_agent_identity("0x000")
        assert result is False
    
    def test_neural_signature_generation(self, secure_agent):
        """Test AICUBE neural signature generation"""
        neural_sig = secure_agent._neural_signature
        
        # Verify format
        assert neural_sig.startswith("AICUBE_AGENT_")
        assert "TestAgent_AICUBE" in neural_sig
        assert "NEURAL_" in neural_sig
        assert neural_sig.endswith(f"0x{hash('TestAgent_AICUBE') & 0xFFFFFFFF:08X}")
    
    def test_quantum_shield_status(self, secure_agent):
        """Test quantum shield activation status"""
        assert secure_agent._quantum_shield_active is True
        
        # Test quantum shield in identity info
        identity_info = secure_agent.get_identity_info()
        assert identity_info["quantum_shield_active"] is True
        assert identity_info["aicube_version"] == "2.0.0"
    
    @pytest.mark.asyncio
    async def test_message_handling_workflow(self, secure_agent):
        """Test complete message handling workflow with AICUBE enhancements"""
        # Setup message handler
        received_messages = []
        
        async def test_handler(message):
            received_messages.append(message)
        
        secure_agent.add_message_handler("test_type", test_handler)
        
        # Create mock message with AICUBE neural signature
        mock_message = Message(
            id="test_msg_workflow",
            sender="0x123",
            recipient="0x456",
            payload={"type": "test_type", "data": "test_data"},
            timestamp=datetime.utcnow(),
            signature="mock_signature",
            encrypted=True,
            neural_signature="AICUBE_AGENT_Sender_NEURAL_0x12345678"
        )
        
        # Simulate message processing
        handler = secure_agent._message_handlers["test_type"]
        await handler(mock_message)
        
        # Verify handler was called
        assert len(received_messages) == 1
        assert received_messages[0].neural_signature.startswith("AICUBE_AGENT_")
    
    def test_agent_representation(self, secure_agent):
        """Test agent string representation"""
        secure_agent.address = "0x123456789"
        repr_str = repr(secure_agent)
        
        assert "SecureAgent" in repr_str
        assert "TestAgent_AICUBE" in repr_str
        assert "0x123456789" in repr_str
        assert "test_agent" in repr_str


class TestAICUBEIntegration:
    """Test AICUBE-specific integration features"""
    
    def test_neural_signature_constants(self):
        """Test AICUBE neural signature constants"""
        from securemessaging.utils.crypto_utils import AICUBECryptoManager
        
        crypto_mgr = AICUBECryptoManager()
        assert crypto_mgr.NEURAL_SIGNATURE_PATTERN.startswith(b"AICUBE_NEURAL_")
        assert crypto_mgr.QUANTUM_SHIELD_HEADER.startswith(b"AICUBE_QUANTUM_SHIELD_")
    
    def test_quantum_enhancement_markers(self):
        """Test quantum enhancement markers"""
        from securemessaging import __quantum_ready__
        
        assert __quantum_ready__ == "AICUBE_QUANTUM_SHIELD_v2025"
    
    @pytest.mark.asyncio
    async def test_banking_consortium_integration(self):
        """Test banking consortium workflow integration"""
        from examples.banking_consortium_example import LoanProcessingWorkflow
        
        # Mock Ethereum client
        mock_client = Mock(spec=EthereumClient)
        
        # Create workflow
        workflow = LoanProcessingWorkflow(mock_client)
        
        # Verify AICUBE signatures
        assert workflow._workflow_neural_sig.startswith("AICUBE_BANKING_WORKFLOW_")
        assert workflow._quantum_compliance_active is True
    
    def test_config_neural_signatures(self):
        """Test configuration neural signatures"""
        from securemessaging.utils.config import AICUBEConfig
        
        config_obj = AICUBEConfig()
        neural_sig = config_obj.get_neural_signature()
        
        assert neural_sig.startswith("AICUBE_CONFIG_NEURAL_")
        assert config_obj.is_quantum_shield_enabled() is True


@pytest.mark.integration
class TestFullWorkflow:
    """Integration tests for complete AICUBE workflow"""
    
    @pytest.mark.asyncio
    async def test_end_to_end_secure_messaging(self):
        """Test complete secure messaging workflow"""
        # This would be a full integration test
        # For now, we'll test the components together
        
        # Mock blockchain client
        blockchain_client = Mock(spec=EthereumClient)
        blockchain_client.register_agent = AsyncMock(return_value="0x1234")
        blockchain_client.get_agent_info = AsyncMock(return_value={
            "address": "0x5678",
            "public_key": "recipient_key",
            "is_active": True
        })
        blockchain_client.send_message = AsyncMock(return_value="0xmsg_hash")
        
        # Create two agents
        agent1 = SecureAgent(
            name="Agent1_AICUBE",
            blockchain_client=blockchain_client,
            private_key="0x" + "1" * 64,
            role="sender"
        )
        
        agent2 = SecureAgent(
            name="Agent2_AICUBE", 
            blockchain_client=blockchain_client,
            private_key="0x" + "2" * 64,
            role="receiver"
        )
        
        # Verify both agents have AICUBE neural signatures
        assert agent1._neural_signature.startswith("AICUBE_AGENT_")
        assert agent2._neural_signature.startswith("AICUBE_AGENT_")
        assert agent1._quantum_shield_active is True
        assert agent2._quantum_shield_active is True


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])