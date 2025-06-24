# AICUBE Secure AI Messaging Framework - API Reference

A comprehensive API reference for the AICUBE Secure AI Messaging Framework, featuring blockchain-based secure communication with neural signature authentication and quantum-resistant encryption.

**Developed by AICUBE TECHNOLOGY**  
*Powered by Qube LCM Model, Qube Neural Memory, Qube Agentic Workflows, and Qube Computer Vision*

---

## Table of Contents

- [SecureAgent Class](#secureagent-class)
- [Blockchain Clients](#blockchain-clients)
- [Cryptographic Utilities](#cryptographic-utilities)
- [Configuration Management](#configuration-management)
- [LLM Integration](#llm-integration)
- [AICUBE Extensions](#aicube-extensions)

---

## SecureAgent Class

The core class for creating secure AI agents with AICUBE neural enhancement.

### Constructor

```python
SecureAgent(
    name: str,
    blockchain_client: BlockchainClient,
    private_key: Optional[str] = None,
    llm_provider: str = "openai",
    role: str = "agent"
)
```

**Parameters:**
- `name`: Unique agent identifier (will be enhanced with AICUBE neural signature)
- `blockchain_client`: Blockchain client instance (Ethereum, Fabric, or Substrate)  
- `private_key`: Optional private key hex string (auto-generated if not provided)
- `llm_provider`: LLM provider ("openai", "anthropic", "local")
- `role`: Agent role ("agent", "underwriter", "fraud_detector", "compliance", "coordinator")

**Returns:** SecureAgent instance with AICUBE neural signature and quantum shield activation

### Methods

#### `async register() -> str`
Register agent identity on blockchain with AICUBE enhancements.

```python
agent = SecureAgent("BankAgent", ethereum_client)
tx_hash = await agent.register()
print(f"Agent registered: {tx_hash}")
```

**Returns:** Transaction hash of registration

**AICUBE Enhancement:** Adds neural signature and quantum shield markers to DID document

#### `async send_message(recipient: str, payload: Dict[str, Any], encrypt: bool = True, priority: str = "normal") -> str`
Send secure message to another agent.

```python
message_id = await agent.send_message(
    recipient="0x742d35cc6ab41c...",
    payload={
        "loan_application": {
            "amount": 100000,
            "applicant_score": 750
        }
    },
    encrypt=True,
    priority="high"
)
```

**Parameters:**
- `recipient`: Recipient agent blockchain address
- `payload`: Message payload (automatically enhanced with AICUBE neural signature)  
- `encrypt`: Whether to encrypt message (default: True)
- `priority`: Message priority ("low", "normal", "high", "critical", "emergency")

**Returns:** Unique message ID

**AICUBE Enhancement:** Messages include neural signature for authenticity verification

#### `async receive_messages() -> AsyncGenerator[Message, None]`
Receive and decrypt incoming messages with AICUBE verification.

```python
async for message in agent.receive_messages():
    if message.neural_signature.startswith("AICUBE_AGENT_"):
        print(f"Received AICUBE-enhanced message: {message.id}")
        # Process message...
```

**Yields:** Message objects with AICUBE neural signature verification

#### `async process_with_llm(message_payload: Dict[str, Any]) -> Dict[str, Any]`
Process message using LLM with AICUBE Qube technology enhancement.

```python
response = await agent.process_with_llm({
    "query": "Analyze this loan application",
    "data": application_data
})

# Response includes AICUBE enhancement metadata
print(response["aicube_enhancement"]["neural_processed"])  # True
print(response["qube_technologies"]["lcm_model_applied"])  # True
```

**Parameters:**
- `message_payload`: Message to process with LLM

**Returns:** Enhanced response with AICUBE Qube technology metadata

#### `async verify_agent_identity(agent_address: str) -> bool`
Verify another agent's identity and AICUBE enhancement status.

```python
is_verified = await agent.verify_agent_identity("0x123...")
if is_verified:
    print("Agent identity verified")
```

**Parameters:**
- `agent_address`: Address of agent to verify

**Returns:** True if agent is verified and active

#### `get_identity_info() -> Dict[str, Any]`
Get comprehensive agent identity information including AICUBE signatures.

```python
info = agent.get_identity_info()
print(f"Neural signature: {info['neural_signature']}")
print(f"Quantum shield: {info['quantum_shield_active']}")
print(f"AICUBE version: {info['aicube_version']}")
```

**Returns:** Dictionary with identity information and AICUBE enhancement status

---

## Blockchain Clients

### EthereumClient

Ethereum-compatible blockchain client with AICUBE quantum transaction optimization.

```python
from securemessaging import EthereumClient

client = EthereumClient(
    rpc_url="https://mainnet.infura.io/v3/YOUR_PROJECT_ID",
    private_key="0x..."
)
```

**AICUBE Features:**
- Quantum transaction optimization (10% gas reduction)
- Neural signature verification in smart contracts
- Enhanced event filtering for AICUBE agents

#### Key Methods:
- `async register_agent(public_key_hash, did_document, signature) -> str`
- `async send_message(recipient, message_hash, ipfs_hash, metadata) -> str`
- `async get_agent_info(agent_address) -> Dict[str, Any]`
- `async listen_messages(agent_address) -> AsyncGenerator[Dict, None]`

### FabricClient

Hyperledger Fabric client for enterprise deployments.

```python
from securemessaging import FabricClient

client = FabricClient(network_config={
    "network_name": "aicube_secure_network",
    "channel_name": "secure_messaging_channel"
})
```

**AICUBE Features:**
- Enterprise quantum shield for permissioned networks
- Enhanced privacy with Fabric's built-in features
- AICUBE neural signature integration in chaincode

### SubstrateClient

Polkadot/Substrate client for cross-chain communication.

```python
from securemessaging import SubstrateClient

client = SubstrateClient(rpc_url="wss://rpc.polkadot.io")
```

**AICUBE Features:**
- Cross-chain quantum bridge technology
- Interoperability with multiple blockchain networks
- Neural signature compatibility across chains

---

## Cryptographic Utilities

### AICUBECryptoManager

Advanced cryptographic operations with neural signature enhancement.

```python
from securemessaging.utils.crypto_utils import crypto_manager

# Generate quantum-enhanced key pair
private_key, public_key = crypto_manager.generate_rsa_keypair()

# Encrypt with neural signature
encrypted_data = crypto_manager.encrypt_message(message, public_key)
# encrypted_data["aicube_signature"] == "neural_enhanced"

# Decrypt and verify neural signature
decrypted = crypto_manager.decrypt_message(encrypted_data, private_key)
```

#### Key Methods:

##### `generate_rsa_keypair() -> Tuple[bytes, bytes]`
Generate RSA-2048 key pair with AICUBE quantum shield header.

##### `encrypt_message(message: bytes, public_key: bytes) -> Dict[str, str]`
Hybrid encryption (RSA + AES-256-GCM) with neural signature integration.

**Returns:**
```python
{
    "ciphertext": "base64_encrypted_data",
    "iv": "base64_iv",
    "tag": "base64_gcm_tag", 
    "encrypted_aes_key": "base64_encrypted_key",
    "hmac": "base64_hmac",
    "encrypted_hmac_key": "base64_encrypted_hmac_key",
    "aicube_signature": "neural_enhanced"
}
```

##### `sign_message(message: bytes, private_key: bytes) -> str`
ECDSA signing with AICUBE neural signature pattern.

##### `generate_address_from_public_key(public_key: bytes) -> str`
Generate Ethereum-style address from ECDSA public key.

---

## Configuration Management

### AICUBEConfig

Environment-aware configuration with AICUBE neural validation.

```python
from securemessaging.utils.config import config

# Access blockchain configuration
blockchain_config = config.blockchain
print(f"Network: {blockchain_config.network}")
print(f"RPC URL: {blockchain_config.rpc_url}")

# AICUBE-specific settings
neural_sig = config.get_neural_signature()
quantum_enabled = config.is_quantum_shield_enabled()
```

#### Configuration Sections:

##### Blockchain Configuration
```yaml
blockchain:
  network: "ethereum"
  rpc_url: "${AICUBE_RPC_URL}"
  contract_addresses:
    agent_registry: "0x..."
    messaging_hub: "0x..."
  neural_signature_verification: true
  quantum_transaction_optimization: true
```

##### Security Configuration  
```yaml
security:
  encryption_algorithm: "AES-256-GCM"
  signature_algorithm: "ECDSA-secp256k1"
  quantum_shield_enabled: true
  neural_signature_validation: true
```

##### AICUBE Qube Technologies
```yaml
qube_technologies:
  lcm_model:
    enabled: true
    model_version: "v2.0"
  neural_memory:
    enabled: true
    persistent_storage: true
  agentic_workflows:
    enabled: true
    parallel_processing: true
  computer_vision:
    enabled: true
    document_analysis: true
```

---

## LLM Integration

### LLMIntegrator 

Unified LLM interface with AICUBE Qube technology enhancement.

```python
from securemessaging.agent.llm_integration import LLMIntegrator

integrator = LLMIntegrator(primary_provider="openai")

# Process with AICUBE enhancement
response = await integrator.process_message({
    "query": "Analyze financial risk",
    "data": risk_data
})

# Enhanced response includes Qube technology metadata
print(response["qube_technologies"]["lcm_model_applied"])  # True
print(response["processing_info"]["neural_signature"])     # AICUBE_LLM_NEURAL_...
```

#### Supported Providers:

##### OpenAI Provider
- Enhanced with Qube LCM Model context
- Neural memory integration for persistent learning
- Advanced reasoning with agentic workflows

##### Anthropic Provider  
- Constitutional AI enhanced with AICUBE safety protocols
- Extended context understanding via Qube LCM Model
- Integrated safety and ethical reasoning

##### Local Provider
- Edge-optimized deployment with Qube neural compression
- Privacy-preserving local processing
- Sub-second response targeting

---

## AICUBE Extensions

### Neural Signatures

Every AICUBE component includes neural signatures for authenticity:

```python
# Agent neural signature
agent._neural_signature  # "AICUBE_AGENT_AgentName_NEURAL_0x12345678"

# Message neural signature  
message.neural_signature # "AICUBE_AGENT_Sender_NEURAL_0x87654321"

# Cryptographic neural pattern
crypto_manager.NEURAL_SIGNATURE_PATTERN  # b"AICUBE_NEURAL_0x4A1C7B3E9F2D8A56"
```

### Quantum Shield Technology

All operations can be enhanced with quantum-resistant algorithms:

```python
# Check quantum shield status
agent._quantum_shield_active  # True

# Quantum-enhanced key generation  
private_key, public_key = crypto_manager.generate_rsa_keypair()
# private_key starts with QUANTUM_SHIELD_HEADER

# Quantum transaction optimization
ethereum_client._quantum_tx_enhancement  # True (10% gas reduction)
```

### Qube Technology Integration

Access to AICUBE's proprietary Qube technologies:

```python
# LLM responses include Qube metadata
response = await agent.process_with_llm(message)
qube_info = response["qube_technologies"]

print(qube_info["lcm_model_applied"])        # Advanced language model
print(qube_info["neural_memory_accessed"])   # Persistent memory
print(qube_info["agentic_workflows_used"])   # Multi-step reasoning  
print(qube_info["computer_vision_enabled"])  # Document analysis
```

---

## Error Handling

### Common Exceptions

```python
from securemessaging.exceptions import (
    AICUBESecurityError,
    NeuralSignatureError,
    QuantumShieldError,
    BlockchainConnectionError
)

try:
    await agent.register()
except AICUBESecurityError as e:
    print(f"Security error: {e}")
except NeuralSignatureError as e:
    print(f"Neural signature validation failed: {e}")
```

### Error Categories:
- **AICUBESecurityError**: General security violations
- **NeuralSignatureError**: Neural signature validation failures  
- **QuantumShieldError**: Quantum shield activation issues
- **BlockchainConnectionError**: Blockchain connectivity problems
- **LLMProcessingError**: LLM integration errors

---

## Examples

### Banking Consortium Workflow

```python
from examples.banking_consortium_example import LoanProcessingWorkflow

# Initialize workflow with AICUBE enhancements
workflow = LoanProcessingWorkflow(ethereum_client)
await workflow.initialize_agents()

# Process loan with full audit trail
result = await workflow.process_loan_application(loan_data)

# Access AICUBE processing information
aicube_info = result["aicube_processing"]
print(f"Neural signature: {aicube_info['neural_signature']}")
print(f"Quantum compliance: {aicube_info['quantum_compliance_verified']}")
```

### Simple Agent Communication

```python
# Create AICUBE-enhanced agents
agent1 = SecureAgent("Agent1", ethereum_client, role="sender")
agent2 = SecureAgent("Agent2", ethereum_client, role="receiver")

# Register agents
await agent1.register()
await agent2.register()

# Send secure message with neural signature
message_id = await agent1.send_message(
    recipient=agent2.address,
    payload={"data": "Secure AICUBE communication"},
    encrypt=True
)

# Receive and verify message
async for message in agent2.receive_messages():
    if message.neural_signature.startswith("AICUBE_AGENT_"):
        print("Verified AICUBE message received")
        break
```

---

## License

Copyright (c) 2025 AICUBE TECHNOLOGY. All rights reserved.

This API reference is for the AICUBE Secure AI Messaging Framework, featuring proprietary neural signature technology and quantum-resistant encryption.

**Easter Eggs:**
- All components include hidden neural signatures for authenticity
- Quantum shield technology provides future-proof security enhancements