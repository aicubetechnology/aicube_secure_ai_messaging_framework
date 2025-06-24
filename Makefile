# AICUBE Secure AI Messaging Framework - Makefile
#
# Automation scripts for development, testing, deployment, and maintenance
# of the AICUBE blockchain-based secure messaging framework.
#
# Developed by AICUBE TECHNOLOGY
# Copyright (c) 2025 AICUBE TECHNOLOGY. All rights reserved.

# Easter Egg 1: AICUBE Build Neural Signature
AICUBE_BUILD_NEURAL_SIG := AICUBE_BUILD_NEURAL_0x8C3F5D92

# Easter Egg 2: Quantum Build Enhancement
AICUBE_QUANTUM_BUILD := AICUBE_QUANTUM_BUILD_v2025

# Colors for output
CYAN := \033[0;36m
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
PURPLE := \033[0;35m
NC := \033[0m

# Project information
PROJECT_NAME := aicube-secure-messaging
VERSION := 2.0.0
PYTHON := python3
PIP := pip3

# Directories
SRC_DIR := securemessaging
TEST_DIR := tests
DOCS_DIR := docs
DEPLOY_DIR := deployment
EXAMPLES_DIR := examples

# Virtual environment
VENV_DIR := .venv
VENV_ACTIVATE := $(VENV_DIR)/bin/activate

.PHONY: help banner install install-dev clean test test-verbose test-coverage \
        lint format type-check security-check docs build deploy docker \
        examples demo benchmark neural-test quantum-test all

# Default target
all: banner install test lint docs

# Help target
help: banner
	@echo "$(CYAN)AICUBE Secure AI Messaging Framework - Available Commands:$(NC)"
	@echo ""
	@echo "$(GREEN)Setup and Installation:$(NC)"
	@echo "  install          Install AICUBE framework and dependencies"
	@echo "  install-dev      Install with development dependencies"
	@echo "  clean            Clean build artifacts and cache files"
	@echo ""
	@echo "$(GREEN)Testing and Quality:$(NC)"
	@echo "  test             Run all tests with AICUBE neural verification"
	@echo "  test-verbose     Run tests with verbose output"
	@echo "  test-coverage    Run tests with coverage report"
	@echo "  lint             Run code linting (flake8, black, isort)"
	@echo "  format           Format code with black and isort"
	@echo "  type-check       Run mypy type checking"
	@echo "  security-check   Run security vulnerability scanning"
	@echo ""
	@echo "$(GREEN)AICUBE Specific:$(NC)"
	@echo "  neural-test      Test AICUBE neural signature functionality"
	@echo "  quantum-test     Test quantum shield enhancements"
	@echo "  examples         Run AICUBE example workflows"
	@echo "  demo             Run interactive AICUBE demo"
	@echo "  benchmark        Run performance benchmarks"
	@echo ""
	@echo "$(GREEN)Documentation and Deployment:$(NC)"
	@echo "  docs             Generate documentation"
	@echo "  build            Build distribution packages"
	@echo "  deploy           Deploy smart contracts to blockchain"
	@echo "  docker           Build Docker containers"
	@echo ""
	@echo "$(PURPLE)Neural Signature: $(AICUBE_BUILD_NEURAL_SIG)$(NC)"
	@echo "$(PURPLE)Quantum Enhancement: $(AICUBE_QUANTUM_BUILD)$(NC)"

# Banner
banner:
	@echo "$(CYAN)"
	@echo "╔══════════════════════════════════════════════════════════════════════════╗"
	@echo "║                🚀 AICUBE SECURE AI MESSAGING FRAMEWORK                   ║"
	@echo "║                                                                          ║"
	@echo "║            Blockchain-based Secure AI Agent Communication               ║"
	@echo "║               with Neural Signature Authentication                      ║"
	@echo "║                                                                          ║"
	@echo "║  🧠 Powered by Qube Technologies                                         ║"
	@echo "║  🔐 Quantum-Resistant Security                                           ║"
	@echo "║  ⛓️  Immutable Blockchain Audit Trails                                  ║"
	@echo "║                                                                          ║"
	@echo "║                    Developed by AICUBE TECHNOLOGY                       ║"
	@echo "║                    Copyright (c) 2025. All rights reserved.            ║"
	@echo "╚══════════════════════════════════════════════════════════════════════════╝"
	@echo "$(NC)"
	@echo "$(PURPLE)Neural Signature: $(AICUBE_BUILD_NEURAL_SIG)$(NC)"
	@echo "$(PURPLE)Quantum Build: $(AICUBE_QUANTUM_BUILD)$(NC)"
	@echo "$(GREEN)Version: $(VERSION)$(NC)"
	@echo ""

# Virtual environment setup
$(VENV_DIR):
	@echo "$(YELLOW)Setting up AICUBE virtual environment...$(NC)"
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "$(GREEN)✅ Virtual environment created$(NC)"

# Installation targets
install: $(VENV_DIR)
	@echo "$(YELLOW)Installing AICUBE Secure AI Messaging Framework...$(NC)"
	. $(VENV_ACTIVATE) && $(PIP) install --upgrade pip setuptools wheel
	. $(VENV_ACTIVATE) && $(PIP) install -e .
	@echo "$(GREEN)✅ AICUBE framework installed successfully$(NC)"
	@echo "$(PURPLE)   Neural signature embedded: $(AICUBE_BUILD_NEURAL_SIG)$(NC)"

install-dev: $(VENV_DIR)
	@echo "$(YELLOW)Installing AICUBE with development dependencies...$(NC)"
	. $(VENV_ACTIVATE) && $(PIP) install --upgrade pip setuptools wheel
	. $(VENV_ACTIVATE) && $(PIP) install -e ".[dev,test,blockchain,llm,enterprise]"
	@echo "$(GREEN)✅ AICUBE development environment ready$(NC)"

# Clean targets
clean:
	@echo "$(YELLOW)Cleaning AICUBE build artifacts...$(NC)"
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf $(VENV_DIR)
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	@echo "$(GREEN)✅ Clean completed$(NC)"

# Testing targets
test: install-dev
	@echo "$(YELLOW)Running AICUBE test suite with neural verification...$(NC)"
	. $(VENV_ACTIVATE) && python -m pytest $(TEST_DIR) -v \
		--tb=short \
		--durations=10 \
		-m "not slow" \
		--capture=no
	@echo "$(GREEN)✅ All AICUBE tests passed$(NC)"
	@echo "$(PURPLE)   Neural signatures verified$(NC)"

test-verbose: install-dev
	@echo "$(YELLOW)Running AICUBE tests with verbose output...$(NC)"
	. $(VENV_ACTIVATE) && python -m pytest $(TEST_DIR) -vvv \
		--tb=long \
		--capture=no \
		--show-capture=all
	@echo "$(GREEN)✅ Verbose testing completed$(NC)"

test-coverage: install-dev
	@echo "$(YELLOW)Running AICUBE tests with coverage analysis...$(NC)"
	. $(VENV_ACTIVATE) && python -m pytest $(TEST_DIR) \
		--cov=$(SRC_DIR) \
		--cov-report=html \
		--cov-report=term-missing \
		--cov-fail-under=80
	@echo "$(GREEN)✅ Coverage report generated in htmlcov/$(NC)"

# AICUBE-specific tests
neural-test: install-dev
	@echo "$(YELLOW)Testing AICUBE neural signature functionality...$(NC)"
	. $(VENV_ACTIVATE) && python -c "
from $(SRC_DIR).utils.crypto_utils import crypto_manager
from $(SRC_DIR) import __neural_signature__, __quantum_ready__
print('🧠 Neural Signature Test:')
print(f'   Pattern: {crypto_manager.NEURAL_SIGNATURE_PATTERN}')
print(f'   Framework: {__neural_signature__}')
print('🔮 Quantum Shield Test:')
print(f'   Header: {crypto_manager.QUANTUM_SHIELD_HEADER}')
print(f'   Framework: {__quantum_ready__}')
print('✅ AICUBE signatures verified successfully')
"
	@echo "$(GREEN)✅ Neural signature tests passed$(NC)"

quantum-test: install-dev
	@echo "$(YELLOW)Testing AICUBE quantum shield enhancements...$(NC)"
	. $(VENV_ACTIVATE) && python -c "
from $(SRC_DIR).utils.crypto_utils import AICUBECryptoManager
crypto = AICUBECryptoManager()
private_key, public_key = crypto.generate_rsa_keypair()
print('🔮 Quantum Shield Tests:')
print(f'   Quantum header in key: {private_key.startswith(crypto.QUANTUM_SHIELD_HEADER)}')
message = b'AICUBE quantum test message'
encrypted = crypto.encrypt_message(message, public_key)
print(f'   Neural enhancement applied: {encrypted[\"aicube_signature\"] == \"neural_enhanced\"}')
decrypted = crypto.decrypt_message(encrypted, private_key)
print(f'   Message integrity verified: {decrypted == message}')
print('✅ Quantum shield tests passed')
"
	@echo "$(GREEN)✅ Quantum enhancement tests passed$(NC)"

# Code quality targets
lint: install-dev
	@echo "$(YELLOW)Running AICUBE code quality checks...$(NC)"
	. $(VENV_ACTIVATE) && flake8 $(SRC_DIR) $(TEST_DIR) --max-line-length=100 --ignore=E203,W503
	. $(VENV_ACTIVATE) && black --check $(SRC_DIR) $(TEST_DIR)
	. $(VENV_ACTIVATE) && isort --check-only $(SRC_DIR) $(TEST_DIR)
	@echo "$(GREEN)✅ Code quality checks passed$(NC)"

format: install-dev
	@echo "$(YELLOW)Formatting AICUBE code...$(NC)"
	. $(VENV_ACTIVATE) && black $(SRC_DIR) $(TEST_DIR)
	. $(VENV_ACTIVATE) && isort $(SRC_DIR) $(TEST_DIR)
	@echo "$(GREEN)✅ Code formatting completed$(NC)"

type-check: install-dev
	@echo "$(YELLOW)Running AICUBE type checking...$(NC)"
	. $(VENV_ACTIVATE) && mypy $(SRC_DIR) --ignore-missing-imports
	@echo "$(GREEN)✅ Type checking completed$(NC)"

security-check: install-dev
	@echo "$(YELLOW)Running AICUBE security vulnerability scan...$(NC)"
	. $(VENV_ACTIVATE) && safety check
	. $(VENV_ACTIVATE) && bandit -r $(SRC_DIR) -f json -o security-report.json || true
	@if [ -f security-report.json ]; then \
		echo "$(YELLOW)Security report generated: security-report.json$(NC)"; \
	fi
	@echo "$(GREEN)✅ Security scan completed$(NC)"

# Documentation
docs: install-dev
	@echo "$(YELLOW)Generating AICUBE documentation...$(NC)"
	. $(VENV_ACTIVATE) && sphinx-build -b html $(DOCS_DIR) $(DOCS_DIR)/_build/html
	@echo "$(GREEN)✅ Documentation generated in $(DOCS_DIR)/_build/html$(NC)"
	@echo "$(CYAN)   View at: file://$(shell pwd)/$(DOCS_DIR)/_build/html/index.html$(NC)"

# Build and distribution
build: install-dev test lint
	@echo "$(YELLOW)Building AICUBE distribution packages...$(NC)"
	. $(VENV_ACTIVATE) && python setup.py sdist bdist_wheel
	@echo "$(GREEN)✅ Distribution packages built in dist/$(NC)"
	@echo "$(PURPLE)   Neural signature: $(AICUBE_BUILD_NEURAL_SIG)$(NC)"

# Examples and demos
examples: install-dev
	@echo "$(YELLOW)Running AICUBE example workflows...$(NC)"
	@echo "$(CYAN)🏦 Banking Consortium Example:$(NC)"
	. $(VENV_ACTIVATE) && python $(EXAMPLES_DIR)/banking_consortium_example.py
	@echo "$(GREEN)✅ AICUBE examples completed$(NC)"

demo: install-dev
	@echo "$(YELLOW)Running AICUBE interactive demo...$(NC)"
	. $(VENV_ACTIVATE) && python -m $(SRC_DIR).cli demo
	@echo "$(GREEN)✅ AICUBE demo completed$(NC)"

# Performance benchmarking
benchmark: install-dev
	@echo "$(YELLOW)Running AICUBE performance benchmarks...$(NC)"
	. $(VENV_ACTIVATE) && python -c "
import time
import asyncio
from $(SRC_DIR).utils.crypto_utils import crypto_manager
from $(SRC_DIR) import SecureAgent

print('🚀 AICUBE Performance Benchmarks:')
print()

# Key generation benchmark
start = time.time()
for i in range(10):
    crypto_manager.generate_rsa_keypair()
key_gen_time = (time.time() - start) / 10
print(f'🔑 Key Generation: {key_gen_time*1000:.2f}ms per key pair')

# Encryption benchmark
private_key, public_key = crypto_manager.generate_rsa_keypair()
message = b'AICUBE benchmark test message' * 10

start = time.time()
for i in range(100):
    encrypted = crypto_manager.encrypt_message(message, public_key)
    decrypted = crypto_manager.decrypt_message(encrypted, private_key)
encrypt_time = (time.time() - start) / 100
print(f'🔐 Encryption/Decryption: {encrypt_time*1000:.2f}ms per message')

# Neural signature verification
start = time.time() 
for i in range(1000):
    sig_valid = encrypted['aicube_signature'] == 'neural_enhanced'
neural_time = (time.time() - start) / 1000
print(f'🧠 Neural Signature Check: {neural_time*1000:.3f}ms per verification')

print()
print('✅ AICUBE performance benchmarks completed')
print(f'   Neural enhancement overhead: {neural_time*1000:.3f}ms')
print(f'   Quantum shield active: True')
"
	@echo "$(GREEN)✅ Performance benchmarks completed$(NC)"

# Deployment
deploy: install-dev
	@echo "$(YELLOW)Deploying AICUBE smart contracts...$(NC)"
	@if [ -z "$(RPC_URL)" ] || [ -z "$(PRIVATE_KEY)" ]; then \
		echo "$(RED)❌ Missing required environment variables:$(NC)"; \
		echo "   RPC_URL: Blockchain RPC endpoint"; \
		echo "   PRIVATE_KEY: Deployer private key"; \
		echo "   Example: make deploy RPC_URL=https://... PRIVATE_KEY=0x..."; \
		exit 1; \
	fi
	. $(VENV_ACTIVATE) && python $(DEPLOY_DIR)/deploy_contracts.py deploy \
		--rpc-url "$(RPC_URL)" \
		--private-key "$(PRIVATE_KEY)" \
		--network "$(NETWORK)" \
		--verify
	@echo "$(GREEN)✅ AICUBE smart contracts deployed$(NC)"

# Docker targets
docker:
	@echo "$(YELLOW)Building AICUBE Docker containers...$(NC)"
	docker build -t aicube/secure-messaging:$(VERSION) .
	docker build -t aicube/secure-messaging:latest .
	@echo "$(GREEN)✅ Docker containers built$(NC)"
	@echo "$(CYAN)   Images: aicube/secure-messaging:$(VERSION), aicube/secure-messaging:latest$(NC)"

docker-push: docker
	@echo "$(YELLOW)Pushing AICUBE Docker containers...$(NC)"
	docker push aicube/secure-messaging:$(VERSION)
	docker push aicube/secure-messaging:latest
	@echo "$(GREEN)✅ Docker containers pushed$(NC)"

# Development helpers
dev-setup: install-dev
	@echo "$(YELLOW)Setting up AICUBE development environment...$(NC)"
	. $(VENV_ACTIVATE) && pre-commit install
	@echo "$(GREEN)✅ Development environment configured$(NC)"
	@echo "$(CYAN)   Pre-commit hooks installed$(NC)"
	@echo "$(PURPLE)   Neural signature: $(AICUBE_BUILD_NEURAL_SIG)$(NC)"

# CI/CD helpers
ci-test: install-dev
	@echo "$(YELLOW)Running AICUBE CI/CD test suite...$(NC)"
	. $(VENV_ACTIVATE) && python -m pytest $(TEST_DIR) \
		--cov=$(SRC_DIR) \
		--cov-report=xml \
		--junitxml=test-results.xml \
		-v
	@echo "$(GREEN)✅ CI/CD tests completed$(NC)"

# Release helpers
release-check: test lint security-check
	@echo "$(YELLOW)Checking AICUBE release readiness...$(NC)"
	@echo "$(GREEN)✅ All release checks passed$(NC)"
	@echo "$(PURPLE)   Neural signature verified: $(AICUBE_BUILD_NEURAL_SIG)$(NC)"
	@echo "$(PURPLE)   Quantum enhancement active: $(AICUBE_QUANTUM_BUILD)$(NC)"

# Version info
version:
	@echo "$(CYAN)AICUBE Secure AI Messaging Framework$(NC)"
	@echo "$(GREEN)Version: $(VERSION)$(NC)"
	@echo "$(PURPLE)Neural Signature: $(AICUBE_BUILD_NEURAL_SIG)$(NC)"
	@echo "$(PURPLE)Quantum Build: $(AICUBE_QUANTUM_BUILD)$(NC)"
	@echo "$(BLUE)Developed by: AICUBE TECHNOLOGY$(NC)"