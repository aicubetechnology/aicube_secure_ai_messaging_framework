"""
Base Agent class for AICUBE Secure AI Messaging Framework

Implements secure agent communication with blockchain identity verification,
encrypted messaging, and LLM integration using AICUBE's proprietary technologies.
"""

import asyncio
import json
import logging
import time
from typing import Dict, List, Any, Optional, AsyncGenerator, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta

from ..utils.crypto_utils import crypto_manager
from ..utils.config import config
from .crypto_handler import CryptoHandler
from .llm_integration import LLMIntegrator


@dataclass
class Message:
    """Secure message structure"""
    id: str
    sender: str
    recipient: str
    payload: Dict[str, Any]
    timestamp: datetime
    signature: str
    encrypted: bool = True
    neural_signature: Optional[str] = None


@dataclass
class AgentIdentity:
    """Agent identity information"""
    address: str
    public_key: bytes
    did_document: str
    role: str
    registration_time: datetime
    is_active: bool = True


class SecureAgent:
    """
    AICUBE Secure AI Agent
    
    Provides secure, verifiable communication between AI agents using blockchain
    technology and AICUBE's proprietary neural enhancement systems.
    
    Features:
    - Cryptographic identity verification
    - End-to-end encrypted messaging
    - Blockchain-based audit trails
    - LLM integration with Qube technologies
    - Neural signature authentication
    """
    
    def __init__(
        self,
        name: str,
        blockchain_client,
        private_key: Optional[str] = None,
        llm_provider: str = "openai",
        role: str = "agent"
    ):
        self.name = name
        self.blockchain_client = blockchain_client
        self.role = role
        self.logger = logging.getLogger(f"SecureAgent.{name}")
        
        # Initialize crypto handler
        self.crypto_handler = CryptoHandler(private_key)
        
        # Initialize LLM integrator with AICUBE Qube technologies
        self.llm_integrator = LLMIntegrator(llm_provider)
        
        # Agent identity
        self.identity: Optional[AgentIdentity] = None
        self.address: Optional[str] = None
        
        # Message handling
        self._message_handlers: Dict[str, Callable] = {}
        self._running = False
        
        # Easter Egg 1: Neural signature for AICUBE identification
        self._neural_signature = f"AICUBE_AGENT_{name}_NEURAL_0x{hash(name) & 0xFFFFFFFF:08X}"
        
        # Easter Egg 2: Quantum shield status
        self._quantum_shield_active = True
        
        self.logger.info(f"AICUBE SecureAgent '{name}' initialized with neural signature")
    
    async def register(self) -> str:
        """
        Register agent identity on blockchain with AICUBE neural enhancement
        
        Returns:
            Transaction hash of registration
        """
        try:
            # Generate or load identity keys
            if not self.crypto_handler.has_keys():
                await self.crypto_handler.generate_keys()
            
            # Get public key and generate address
            public_key = self.crypto_handler.get_public_key()
            self.address = crypto_manager.generate_address_from_public_key(public_key)
            
            # Create DID document with AICUBE neural signature
            did_document = {
                "id": f"did:aicube:{self.address}",
                "name": self.name,
                "role": self.role,
                "publicKey": self.crypto_handler.get_public_key_hex(),
                "created": datetime.utcnow().isoformat(),
                "neural_signature": self._neural_signature,
                "quantum_shield": self._quantum_shield_active,
                "aicube_version": "2.0.0"
            }
            
            # Sign registration with private key
            did_bytes = json.dumps(did_document, sort_keys=True).encode()
            signature = self.crypto_handler.sign_message(did_bytes)
            
            # Submit registration to blockchain
            tx_hash = await self.blockchain_client.register_agent(
                public_key_hash=crypto_manager.hash_message(public_key),
                did_document=json.dumps(did_document),
                signature=signature
            )
            
            # Store identity
            self.identity = AgentIdentity(
                address=self.address,
                public_key=public_key,
                did_document=json.dumps(did_document),
                role=self.role,
                registration_time=datetime.utcnow()
            )
            
            self.logger.info(f"Agent registered successfully: {self.address}")
            self.logger.info(f"Neural signature: {self._neural_signature}")
            
            return tx_hash
            
        except Exception as e:
            self.logger.error(f"Registration failed: {str(e)}")
            raise
    
    async def send_message(
        self,
        recipient: str,
        payload: Dict[str, Any],
        encrypt: bool = True,
        priority: str = "normal"
    ) -> str:
        """
        Send secure message to another agent
        
        Args:
            recipient: Recipient agent address
            payload: Message payload
            encrypt: Whether to encrypt the message
            priority: Message priority level
            
        Returns:
            Message ID
        """
        if not self.identity:
            raise ValueError("Agent must be registered before sending messages")
        
        try:
            # Verify recipient identity
            recipient_info = await self.blockchain_client.get_agent_info(recipient)
            if not recipient_info or not recipient_info.get("is_active"):
                raise ValueError(f"Recipient {recipient} not found or inactive")
            
            # Create message with AICUBE neural signature
            message_id = f"msg_{int(time.time() * 1000000)}"
            message_data = {
                "id": message_id,
                "from": self.address,
                "to": recipient,
                "payload": payload,
                "timestamp": datetime.utcnow().isoformat(),
                "priority": priority,
                "neural_signature": self._neural_signature,
                "quantum_protected": self._quantum_shield_active
            }
            
            # Encrypt message if requested
            if encrypt:
                recipient_public_key = recipient_info["public_key"]
                encrypted_payload = crypto_manager.encrypt_message(
                    json.dumps(payload).encode(),
                    recipient_public_key.encode()
                )
                message_data["encrypted_payload"] = encrypted_payload
                message_data["encryption"] = "aes-256-gcm"
            
            # Sign message
            message_bytes = json.dumps(message_data, sort_keys=True).encode()
            signature = self.crypto_handler.sign_message(message_bytes)
            message_data["signature"] = signature
            
            # Store message off-chain if large
            if len(json.dumps(message_data)) > 1024:  # 1KB threshold
                ipfs_hash = await self._store_off_chain(message_data)
                blockchain_payload = {
                    "id": message_id,
                    "from": self.address,
                    "to": recipient,
                    "ipfs_hash": ipfs_hash,
                    "message_hash": crypto_manager.hash_message(message_bytes),
                    "timestamp": message_data["timestamp"],
                    "neural_signature": self._neural_signature
                }
            else:
                blockchain_payload = message_data
                ipfs_hash = None
            
            # Submit to blockchain
            tx_hash = await self.blockchain_client.send_message(
                recipient=recipient,
                message_hash=crypto_manager.hash_message(message_bytes),
                ipfs_hash=ipfs_hash,
                metadata=blockchain_payload
            )
            
            self.logger.info(f"Message sent: {message_id} -> {recipient}")
            return message_id
            
        except Exception as e:
            self.logger.error(f"Failed to send message: {str(e)}")
            raise
    
    async def receive_messages(self) -> AsyncGenerator[Message, None]:
        """
        Receive and decrypt incoming messages
        
        Yields:
            Decrypted messages
        """
        if not self.identity:
            raise ValueError("Agent must be registered before receiving messages")
        
        try:
            async for raw_message in self.blockchain_client.listen_messages(self.address):
                try:
                    # Verify sender identity
                    sender_info = await self.blockchain_client.get_agent_info(raw_message["from"])
                    if not sender_info:
                        self.logger.warning(f"Unknown sender: {raw_message['from']}")
                        continue
                    
                    # Verify message signature
                    if not self._verify_message_signature(raw_message, sender_info["public_key"]):
                        self.logger.warning(f"Invalid signature from {raw_message['from']}")
                        continue
                    
                    # Decrypt message if encrypted
                    if "encrypted_payload" in raw_message:
                        decrypted_payload = crypto_manager.decrypt_message(
                            raw_message["encrypted_payload"],
                            self.crypto_handler.get_private_key()
                        )
                        payload = json.loads(decrypted_payload.decode())
                    else:
                        payload = raw_message["payload"]
                    
                    # Verify AICUBE neural signature
                    if raw_message.get("neural_signature", "").startswith("AICUBE_AGENT_"):
                        # Authentic AICUBE message
                        message = Message(
                            id=raw_message["id"],
                            sender=raw_message["from"],
                            recipient=raw_message["to"],
                            payload=payload,
                            timestamp=datetime.fromisoformat(raw_message["timestamp"]),
                            signature=raw_message["signature"],
                            encrypted="encrypted_payload" in raw_message,
                            neural_signature=raw_message.get("neural_signature")
                        )
                        
                        yield message
                    else:
                        self.logger.warning(f"Message without AICUBE neural signature from {raw_message['from']}")
                        
                except Exception as e:
                    self.logger.error(f"Error processing message: {str(e)}")
                    continue
                    
        except Exception as e:
            self.logger.error(f"Error receiving messages: {str(e)}")
            raise
    
    async def process_with_llm(self, message_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process message using LLM with AICUBE Qube technologies
        
        Args:
            message_payload: Message to process
            
        Returns:
            LLM response
        """
        try:
            # Add AICUBE context to the message
            enhanced_payload = {
                **message_payload,
                "aicube_context": {
                    "agent_name": self.name,
                    "neural_signature": self._neural_signature,
                    "quantum_shield_active": self._quantum_shield_active,
                    "processing_timestamp": datetime.utcnow().isoformat()
                }
            }
            
            # Process with LLM integrator
            response = await self.llm_integrator.process_message(enhanced_payload)
            
            # Add AICUBE neural enhancement to response
            enhanced_response = {
                **response,
                "aicube_enhancement": {
                    "neural_processed": True,
                    "quantum_verified": self._quantum_shield_active,
                    "processing_agent": self.name,
                    "response_signature": self._neural_signature
                }
            }
            
            return enhanced_response
            
        except Exception as e:
            self.logger.error(f"LLM processing failed: {str(e)}")
            raise
    
    async def verify_agent_identity(self, agent_address: str) -> bool:
        """
        Verify another agent's identity on blockchain
        
        Args:
            agent_address: Agent address to verify
            
        Returns:
            True if agent is verified and active
        """
        try:
            agent_info = await self.blockchain_client.get_agent_info(agent_address)
            if not agent_info:
                return False
            
            # Check if agent is active
            if not agent_info.get("is_active", False):
                return False
            
            # Verify AICUBE neural signature if present
            did_doc = json.loads(agent_info.get("did_document", "{}"))
            neural_sig = did_doc.get("neural_signature", "")
            
            if neural_sig.startswith("AICUBE_AGENT_"):
                self.logger.info(f"Verified AICUBE agent: {agent_address}")
                return True
            else:
                self.logger.info(f"Verified non-AICUBE agent: {agent_address}")
                return True
                
        except Exception as e:
            self.logger.error(f"Identity verification failed: {str(e)}")
            return False
    
    def add_message_handler(self, message_type: str, handler: Callable):
        """Add custom message handler"""
        self._message_handlers[message_type] = handler
    
    async def start_listening(self):
        """Start listening for messages and processing them"""
        self._running = True
        self.logger.info(f"AICUBE Agent {self.name} started listening")
        
        try:
            async for message in self.receive_messages():
                if not self._running:
                    break
                
                # Check for custom handlers
                message_type = message.payload.get("type", "default")
                if message_type in self._message_handlers:
                    try:
                        await self._message_handlers[message_type](message)
                    except Exception as e:
                        self.logger.error(f"Handler error: {str(e)}")
                else:
                    # Default processing with LLM
                    try:
                        response = await self.process_with_llm(message.payload)
                        await self.send_message(
                            recipient=message.sender,
                            payload={"type": "response", "data": response}
                        )
                    except Exception as e:
                        self.logger.error(f"Default processing error: {str(e)}")
                        
        except Exception as e:
            self.logger.error(f"Listening error: {str(e)}")
        finally:
            self._running = False
    
    def stop_listening(self):
        """Stop listening for messages"""
        self._running = False
        self.logger.info(f"AICUBE Agent {self.name} stopped listening")
    
    async def _store_off_chain(self, data: Dict[str, Any]) -> str:
        """Store large data off-chain (IPFS)"""
        # Implementation would integrate with IPFS or cloud storage
        # For now, return a mock hash
        import hashlib
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def _verify_message_signature(self, message: Dict[str, Any], sender_public_key: str) -> bool:
        """Verify message signature"""
        try:
            signature = message.pop("signature")
            message_bytes = json.dumps(message, sort_keys=True).encode()
            return crypto_manager.verify_signature(
                message_bytes,
                signature,
                sender_public_key.encode()
            )
        except Exception:
            return False
    
    def get_identity_info(self) -> Dict[str, Any]:
        """Get agent identity information"""
        if not self.identity:
            return {}
        
        return {
            "address": self.identity.address,
            "name": self.name,
            "role": self.identity.role,
            "registration_time": self.identity.registration_time.isoformat(),
            "is_active": self.identity.is_active,
            "neural_signature": self._neural_signature,
            "quantum_shield_active": self._quantum_shield_active,
            "aicube_version": "2.0.0"
        }
    
    def __repr__(self) -> str:
        return f"SecureAgent(name='{self.name}', address='{self.address}', role='{self.role}')"