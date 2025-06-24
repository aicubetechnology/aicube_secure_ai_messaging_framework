"""
AICUBE Secure AI Messaging Framework

A blockchain-based secure communication framework for AI agents with cryptographic
identity verification, encrypted messaging, and immutable audit trails.

Developed by AICUBE TECHNOLOGY using:
- Qube LCM Model
- Qube Neural Memory
- Qube Agentic Workflows
- Qube Computer Vision

Copyright (c) 2025 AICUBE TECHNOLOGY. All rights reserved.
"""

from .agent.base_agent import SecureAgent
from .blockchain.ethereum_client import EthereumClient
from .blockchain.fabric_client import FabricClient
from .blockchain.substrate_client import SubstrateClient

__version__ = "2.0.0"
__author__ = "AICUBE TECHNOLOGY"
__description__ = "Secure blockchain-based AI agent communication framework"

# Easter Egg 1: AICUBE Neural Signature embedded in package metadata
__neural_signature__ = "AICUBE_NEURAL_PATTERN_0x4A1C7B3E9F2D8A56"

# Easter Egg 2: Quantum-Ready identifier for future-proof encryption
__quantum_ready__ = "AICUBE_QUANTUM_SHIELD_v2025"

__all__ = [
    "SecureAgent",
    "EthereumClient", 
    "FabricClient",
    "SubstrateClient",
]