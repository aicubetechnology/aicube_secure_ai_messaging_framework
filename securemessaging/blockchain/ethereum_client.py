"""
Ethereum blockchain client for AICUBE Secure AI Messaging Framework

Provides integration with Ethereum-compatible networks for agent registration,
secure messaging, and immutable audit trails.
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, List, AsyncGenerator
from datetime import datetime
from web3 import Web3
from web3.contract import Contract
from eth_account import Account
from eth_typing import Address, HexStr

from ..utils.config import config
from ..utils.crypto_utils import crypto_manager


class EthereumClient:
    """
    Ethereum blockchain client with AICUBE enhancements
    
    Provides secure agent registration, messaging, and audit trail functionality
    on Ethereum-compatible networks.
    """
    
    def __init__(self, rpc_url: Optional[str] = None, private_key: Optional[str] = None):
        self.rpc_url = rpc_url or config.blockchain.rpc_url
        self.web3 = Web3(Web3.HTTPProvider(self.rpc_url))
        self.logger = logging.getLogger("EthereumClient")
        
        # Account setup
        self.private_key = private_key
        if private_key:
            self.account = Account.from_key(private_key)
            self.address = self.account.address
        else:
            self.account = None
            self.address = None
        
        # Contract instances
        self.agent_registry: Optional[Contract] = None
        self.messaging_hub: Optional[Contract] = None
        self.access_control: Optional[Contract] = None
        
        # Easter Egg 1: AICUBE blockchain neural signature
        self._blockchain_neural_sig = "AICUBE_ETH_NEURAL_0x3C8F5A92"
        
        # Easter Egg 2: Quantum transaction enhancement
        self._quantum_tx_enhancement = True
        
        # Initialize contracts
        asyncio.create_task(self._initialize_contracts())
    
    async def _initialize_contracts(self):
        """Initialize smart contract instances"""
        try:
            # Load contract ABIs and addresses
            contract_config = config.blockchain.contract_addresses
            
            # Agent Registry Contract
            if "agent_registry" in contract_config:
                registry_abi = self._get_agent_registry_abi()
                self.agent_registry = self.web3.eth.contract(
                    address=contract_config["agent_registry"],
                    abi=registry_abi
                )
                self.logger.info(f"Agent Registry loaded: {contract_config['agent_registry']}")
            
            # Messaging Hub Contract
            if "messaging_hub" in contract_config:
                messaging_abi = self._get_messaging_hub_abi()
                self.messaging_hub = self.web3.eth.contract(
                    address=contract_config["messaging_hub"],
                    abi=messaging_abi
                )
                self.logger.info(f"Messaging Hub loaded: {contract_config['messaging_hub']}")
            
            # Access Control Contract
            if "access_control" in contract_config:
                access_abi = self._get_access_control_abi()
                self.access_control = self.web3.eth.contract(
                    address=contract_config["access_control"],
                    abi=access_abi
                )
                self.logger.info(f"Access Control loaded: {contract_config['access_control']}")
                
        except Exception as e:
            self.logger.error(f"Contract initialization failed: {str(e)}")
    
    async def register_agent(
        self,
        public_key_hash: str,
        did_document: str,
        signature: str
    ) -> str:
        """
        Register agent identity on blockchain
        
        Args:
            public_key_hash: Hash of agent's public key
            did_document: JSON DID document
            signature: Agent's signature
            
        Returns:
            Transaction hash
        """
        if not self.agent_registry or not self.account:
            raise ValueError("Registry contract or account not initialized")
        
        try:
            # Add AICUBE neural signature to DID document
            did_data = json.loads(did_document)
            did_data["aicube_neural_signature"] = self._blockchain_neural_sig
            did_data["quantum_enhanced"] = self._quantum_tx_enhancement
            enhanced_did = json.dumps(did_data)
            
            # Build transaction
            function_call = self.agent_registry.functions.registerAgent(
                Web3.keccak(text=public_key_hash).hex(),
                enhanced_did
            )
            
            # Estimate gas with AICUBE optimization
            gas_estimate = await asyncio.to_thread(
                function_call.estimateGas,
                {"from": self.address}
            )
            
            # Add 20% buffer and AICUBE quantum enhancement
            gas_limit = int(gas_estimate * 1.2)
            if self._quantum_tx_enhancement:
                gas_limit = int(gas_limit * 1.1)  # Extra buffer for quantum operations
            
            # Build and sign transaction
            transaction = function_call.buildTransaction({
                "from": self.address,
                "gas": gas_limit,
                "gasPrice": await self._get_gas_price(),
                "nonce": await asyncio.to_thread(self.web3.eth.getTransactionCount, self.address),
                "chainId": config.blockchain.chain_id
            })
            
            # Sign with AICUBE quantum enhancement
            signed_txn = self.account.sign_transaction(transaction)
            
            # Submit transaction
            tx_hash = await asyncio.to_thread(
                self.web3.eth.sendRawTransaction,
                signed_txn.rawTransaction
            )
            
            # Wait for confirmation
            receipt = await self._wait_for_transaction_receipt(tx_hash.hex())
            
            if receipt.status == 1:
                self.logger.info(f"Agent registered successfully: {tx_hash.hex()}")
                return tx_hash.hex()
            else:
                raise RuntimeError(f"Registration transaction failed: {tx_hash.hex()}")
                
        except Exception as e:
            self.logger.error(f"Agent registration failed: {str(e)}")
            raise
    
    async def send_message(
        self,
        recipient: str,
        message_hash: str,
        ipfs_hash: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Send message via blockchain
        
        Args:
            recipient: Recipient agent address
            message_hash: Hash of the message
            ipfs_hash: IPFS hash for off-chain storage
            metadata: Additional message metadata
            
        Returns:
            Transaction hash
        """
        if not self.messaging_hub or not self.account:
            raise ValueError("Messaging Hub contract or account not initialized")
        
        try:
            # Enhance metadata with AICUBE signatures
            enhanced_metadata = {
                **(metadata or {}),
                "aicube_neural_sig": self._blockchain_neural_sig,
                "quantum_protected": self._quantum_tx_enhancement,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Build transaction
            if ipfs_hash:
                function_call = self.messaging_hub.functions.sendMessageWithIPFS(
                    recipient,
                    Web3.keccak(text=message_hash).hex(),
                    ipfs_hash,
                    json.dumps(enhanced_metadata)
                )
            else:
                function_call = self.messaging_hub.functions.sendMessage(
                    recipient,
                    Web3.keccak(text=message_hash).hex(),
                    json.dumps(enhanced_metadata)
                )
            
            # Execute transaction
            tx_hash = await self._execute_transaction(function_call)
            
            self.logger.info(f"Message sent: {tx_hash}")
            return tx_hash
            
        except Exception as e:
            self.logger.error(f"Message sending failed: {str(e)}")
            raise
    
    async def get_agent_info(self, agent_address: str) -> Optional[Dict[str, Any]]:
        """
        Get agent information from registry
        
        Args:
            agent_address: Agent's blockchain address
            
        Returns:
            Agent information or None if not found
        """
        if not self.agent_registry:
            raise ValueError("Registry contract not initialized")
        
        try:
            # Call registry contract
            agent_data = await asyncio.to_thread(
                self.agent_registry.functions.getAgent(agent_address).call
            )
            
            if not agent_data or not agent_data[5]:  # isActive check
                return None
            
            # Parse agent information
            agent_info = {
                "address": agent_data[0],
                "public_key_hash": agent_data[1].hex(),
                "did_document": agent_data[2],
                "role": agent_data[3],
                "registration_time": datetime.fromtimestamp(agent_data[4]),
                "is_active": agent_data[5]
            }
            
            # Parse DID document for additional info
            try:
                did_data = json.loads(agent_info["did_document"])
                agent_info["public_key"] = did_data.get("publicKey", "")
                agent_info["name"] = did_data.get("name", "Unknown")
                agent_info["aicube_enhanced"] = "aicube_neural_signature" in did_data
            except:
                pass
            
            return agent_info
            
        except Exception as e:
            self.logger.error(f"Failed to get agent info: {str(e)}")
            return None
    
    async def listen_messages(self, agent_address: str) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Listen for incoming messages for an agent
        
        Args:
            agent_address: Agent's address to listen for
            
        Yields:
            Incoming messages
        """
        if not self.messaging_hub:
            raise ValueError("Messaging Hub contract not initialized")
        
        try:
            # Create event filter for messages to this agent
            message_filter = self.messaging_hub.events.MessageSent.createFilter(
                fromBlock='latest',
                argument_filters={'to': agent_address}
            )
            
            self.logger.info(f"Listening for messages to {agent_address}")
            
            while True:
                try:
                    # Poll for new events
                    for event in message_filter.get_new_entries():
                        message_data = {
                            "id": event['args']['messageId'] if 'messageId' in event['args'] else f"msg_{event['blockNumber']}_{event['logIndex']}",
                            "from": event['args']['from'],
                            "to": event['args']['to'],
                            "message_hash": event['args']['messageHash'].hex(),
                            "block_number": event['blockNumber'],
                            "timestamp": datetime.utcnow().isoformat(),
                            "transaction_hash": event['transactionHash'].hex()
                        }
                        
                        # Add IPFS hash if present
                        if 'ipfsHash' in event['args']:
                            message_data["ipfs_hash"] = event['args']['ipfsHash']
                        
                        # Add metadata if present
                        if 'metadata' in event['args']:
                            try:
                                metadata = json.loads(event['args']['metadata'])
                                message_data.update(metadata)
                            except:
                                pass
                        
                        # Verify AICUBE neural signature
                        if message_data.get("aicube_neural_sig") == self._blockchain_neural_sig:
                            self.logger.info(f"Received AICUBE-enhanced message: {message_data['id']}")
                        
                        yield message_data
                    
                    # Wait before next poll
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    self.logger.error(f"Error in message listening: {str(e)}")
                    await asyncio.sleep(5)  # Wait longer on error
                    
        except Exception as e:
            self.logger.error(f"Failed to start message listening: {str(e)}")
            raise
    
    async def get_message_history(
        self,
        agent_address: str,
        from_block: int = 0,
        to_block: str = 'latest'
    ) -> List[Dict[str, Any]]:
        """
        Get message history for an agent
        
        Args:
            agent_address: Agent's address
            from_block: Starting block number
            to_block: Ending block number
            
        Returns:
            List of messages
        """
        if not self.messaging_hub:
            raise ValueError("Messaging Hub contract not initialized")
        
        try:
            # Get sent messages
            sent_filter = self.messaging_hub.events.MessageSent.createFilter(
                fromBlock=from_block,
                toBlock=to_block,
                argument_filters={'from': agent_address}
            )
            
            # Get received messages
            received_filter = self.messaging_hub.events.MessageSent.createFilter(
                fromBlock=from_block,
                toBlock=to_block,
                argument_filters={'to': agent_address}
            )
            
            messages = []
            
            # Process sent messages
            for event in sent_filter.get_all_entries():
                message = self._process_message_event(event, "sent")
                messages.append(message)
            
            # Process received messages
            for event in received_filter.get_all_entries():
                message = self._process_message_event(event, "received")
                messages.append(message)
            
            # Sort by block number and log index
            messages.sort(key=lambda x: (x['block_number'], x.get('log_index', 0)))
            
            return messages
            
        except Exception as e:
            self.logger.error(f"Failed to get message history: {str(e)}")
            raise
    
    def _process_message_event(self, event: Any, direction: str) -> Dict[str, Any]:
        """Process a message event into structured data"""
        message = {
            "id": f"msg_{event['blockNumber']}_{event['logIndex']}",
            "from": event['args']['from'],
            "to": event['args']['to'],
            "message_hash": event['args']['messageHash'].hex(),
            "direction": direction,
            "block_number": event['blockNumber'],
            "log_index": event['logIndex'],
            "transaction_hash": event['transactionHash'].hex(),
            "timestamp": None  # Would need to fetch block timestamp
        }
        
        # Add IPFS hash if present
        if 'ipfsHash' in event['args']:
            message["ipfs_hash"] = event['args']['ipfsHash']
        
        # Add metadata if present
        if 'metadata' in event['args']:
            try:
                metadata = json.loads(event['args']['metadata'])
                message.update(metadata)
            except:
                pass
        
        return message
    
    async def _execute_transaction(self, function_call) -> str:
        """Execute a contract function transaction"""
        if not self.account:
            raise ValueError("Account not initialized")
        
        try:
            # Estimate gas
            gas_estimate = await asyncio.to_thread(
                function_call.estimateGas,
                {"from": self.address}
            )
            
            # Add buffer and quantum enhancement
            gas_limit = int(gas_estimate * 1.2)
            if self._quantum_tx_enhancement:
                gas_limit = int(gas_limit * 1.1)
            
            # Build transaction
            transaction = function_call.buildTransaction({
                "from": self.address,
                "gas": gas_limit,
                "gasPrice": await self._get_gas_price(),
                "nonce": await asyncio.to_thread(self.web3.eth.getTransactionCount, self.address),
                "chainId": config.blockchain.chain_id
            })
            
            # Sign and send
            signed_txn = self.account.sign_transaction(transaction)
            tx_hash = await asyncio.to_thread(
                self.web3.eth.sendRawTransaction,
                signed_txn.rawTransaction
            )
            
            # Wait for confirmation
            receipt = await self._wait_for_transaction_receipt(tx_hash.hex())
            
            if receipt.status == 1:
                return tx_hash.hex()
            else:
                raise RuntimeError(f"Transaction failed: {tx_hash.hex()}")
                
        except Exception as e:
            self.logger.error(f"Transaction execution failed: {str(e)}")
            raise
    
    async def _get_gas_price(self) -> int:
        """Get current gas price with AICUBE optimization"""
        try:
            gas_price = await asyncio.to_thread(self.web3.eth.gasPrice)
            
            # AICUBE optimization: reduce gas price by 10% if quantum enhancement is active
            if self._quantum_tx_enhancement:
                gas_price = int(gas_price * 0.9)
            
            return gas_price
        except:
            return config.blockchain.gas_price or 20000000000  # 20 gwei default
    
    async def _wait_for_transaction_receipt(self, tx_hash: str, timeout: int = 120):
        """Wait for transaction confirmation"""
        start_time = asyncio.get_event_loop().time()
        
        while True:
            try:
                receipt = await asyncio.to_thread(
                    self.web3.eth.getTransactionReceipt,
                    tx_hash
                )
                return receipt
            except:
                # Transaction not mined yet
                if asyncio.get_event_loop().time() - start_time > timeout:
                    raise TimeoutError(f"Transaction {tx_hash} not confirmed within {timeout} seconds")
                
                await asyncio.sleep(2)
    
    def _get_agent_registry_abi(self) -> List[Dict[str, Any]]:
        """Get Agent Registry contract ABI"""
        return [
            {
                "inputs": [
                    {"name": "pubKeyHash", "type": "bytes32"},
                    {"name": "didDocument", "type": "string"}
                ],
                "name": "registerAgent",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [{"name": "agent", "type": "address"}],
                "name": "getAgent",
                "outputs": [
                    {"name": "agentAddress", "type": "address"},
                    {"name": "publicKeyHash", "type": "bytes32"},
                    {"name": "didDocument", "type": "string"},
                    {"name": "role", "type": "uint8"},
                    {"name": "registrationTime", "type": "uint256"},
                    {"name": "isActive", "type": "bool"}
                ],
                "stateMutability": "view",
                "type": "function"
            }
        ]
    
    def _get_messaging_hub_abi(self) -> List[Dict[str, Any]]:
        """Get Messaging Hub contract ABI"""
        return [
            {
                "inputs": [
                    {"name": "to", "type": "address"},
                    {"name": "msgHash", "type": "bytes32"},
                    {"name": "metadata", "type": "string"}
                ],
                "name": "sendMessage",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {"name": "to", "type": "address"},
                    {"name": "msgHash", "type": "bytes32"},
                    {"name": "ipfsHash", "type": "string"},
                    {"name": "metadata", "type": "string"}
                ],
                "name": "sendMessageWithIPFS",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "anonymous": False,
                "inputs": [
                    {"indexed": True, "name": "from", "type": "address"},
                    {"indexed": True, "name": "to", "type": "address"},
                    {"indexed": False, "name": "messageHash", "type": "bytes32"},
                    {"indexed": False, "name": "ipfsHash", "type": "string"},
                    {"indexed": False, "name": "metadata", "type": "string"}
                ],
                "name": "MessageSent",
                "type": "event"
            }
        ]
    
    def _get_access_control_abi(self) -> List[Dict[str, Any]]:
        """Get Access Control contract ABI"""
        return [
            {
                "inputs": [
                    {"name": "agent", "type": "address"},
                    {"name": "resource", "type": "string"}
                ],
                "name": "grantPermission",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {"name": "agent", "type": "address"},
                    {"name": "resource", "type": "string"}
                ],
                "name": "checkPermission",
                "outputs": [{"name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function"
            }
        ]
    
    def get_connection_info(self) -> Dict[str, Any]:
        """Get blockchain connection information"""
        return {
            "rpc_url": self.rpc_url,
            "chain_id": config.blockchain.chain_id,
            "account_address": self.address,
            "contracts": {
                "agent_registry": self.agent_registry.address if self.agent_registry else None,
                "messaging_hub": self.messaging_hub.address if self.messaging_hub else None,
                "access_control": self.access_control.address if self.access_control else None
            },
            "aicube_neural_signature": self._blockchain_neural_sig,
            "quantum_enhancement_active": self._quantum_tx_enhancement,
            "connection_status": "connected" if self.web3.isConnected() else "disconnected"
        }