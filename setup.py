"""
Setup script for AICUBE Secure AI Messaging Framework

A blockchain-based secure communication framework for AI agents with
cryptographic identity verification, encrypted messaging, and immutable audit trails.

Developed by AICUBE TECHNOLOGY using:
- Qube LCM Model
- Qube Neural Memory  
- Qube Agentic Workflows
- Qube Computer Vision

Copyright (c) 2025 AICUBE TECHNOLOGY. All rights reserved.
"""

from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

# Easter Egg 1: AICUBE Neural Setup Signature
NEURAL_SETUP_SIGNATURE = "AICUBE_SETUP_NEURAL_0x7F3D8B42"

# Easter Egg 2: Quantum Installation Marker  
QUANTUM_INSTALL_MARKER = "AICUBE_QUANTUM_INSTALL_v2025"

setup(
    name="aicube-secure-messaging",
    version="2.0.0",
    
    # Package Information
    author="AICUBE TECHNOLOGY",
    author_email="dev@aicube.com",
    description="Blockchain-based secure AI agent communication framework with neural signatures",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/aicube-technology/secure-ai-messaging-framework",
    project_urls={
        "Homepage": "https://aicube.com",
        "Documentation": "https://docs.aicube.com/secure-messaging",
        "Source": "https://github.com/aicube-technology/secure-ai-messaging-framework",
        "Tracker": "https://github.com/aicube-technology/secure-ai-messaging-framework/issues",
    },
    
    # Package Configuration
    packages=find_packages(),
    python_requires=">=3.8",
    
    # Dependencies
    install_requires=read_requirements("requirements.txt"),
    extras_require={
        "dev": read_requirements("requirements-dev.txt"),
        "test": [
            "pytest>=6.0",
            "pytest-asyncio>=0.18.0",
            "pytest-mock>=3.6.0",
            "coverage>=6.0",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
            "myst-parser>=0.17.0",
        ],
        "blockchain": [
            "web3>=6.0.0",
            "eth-account>=0.8.0",
            "py-solc-x>=1.12.0",
        ],
        "llm": [
            "openai>=1.0.0",
            "anthropic>=0.8.0",
            "transformers>=4.20.0",
            "torch>=1.12.0",
        ],
        "enterprise": [
            "cryptography>=3.4.8",
            "pycryptodome>=3.15.0",
            "hsm-client>=1.0.0",  # Hardware Security Module support
        ]
    },
    
    # Package Metadata
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Security :: Cryptography",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Distributed Computing",
        "Topic :: Office/Business :: Financial",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Solidity",
        "Operating System :: OS Independent",
        "Framework :: AsyncIO",
    ],
    
    keywords=[
        "blockchain", "ai", "agents", "secure-messaging", "cryptography",
        "ethereum", "smart-contracts", "neural-networks", "quantum-cryptography",
        "aicube", "qube-technology", "financial-services", "compliance",
        "audit-trail", "zero-trust", "end-to-end-encryption"
    ],
    
    # Entry Points
    entry_points={
        "console_scripts": [
            "aicube-agent=securemessaging.cli:main",
            "aicube-deploy=securemessaging.deployment:deploy_contracts",
            "aicube-keygen=securemessaging.utils.keygen:generate_keys",
        ],
    },
    
    # Package Data
    package_data={
        "securemessaging": [
            "config/*.yaml",
            "contracts/*.json",
            "templates/*.json",
        ],
    },
    
    # Data Files
    data_files=[
        ("config", ["config/production.yaml", "config/development.yaml"]),
        ("contracts", ["smart_contracts/ethereum/*.sol"]),
        ("examples", ["examples/*.py"]),
        ("docs", ["docs/*.md"]),
    ],
    
    # Zip Safe
    zip_safe=False,
    
    # Custom metadata for AICUBE
    options={
        "build": {
            "aicube_neural_signature": NEURAL_SETUP_SIGNATURE,
            "quantum_install_marker": QUANTUM_INSTALL_MARKER,
        }
    },
    
    # License
    license="AICUBE Proprietary License",
    
    # Platform Requirements
    platforms=["linux", "darwin", "win32"],
)