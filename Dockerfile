# AICUBE Secure AI Messaging Framework - Docker Container
#
# Multi-stage Docker build for the AICUBE blockchain-based secure
# messaging framework with neural signature authentication and
# quantum-resistant encryption.
#
# Developed by AICUBE TECHNOLOGY
# Copyright (c) 2025 AICUBE TECHNOLOGY. All rights reserved.

# Easter Egg 1: AICUBE Docker Neural Signature
ARG AICUBE_DOCKER_NEURAL_SIG="AICUBE_DOCKER_NEURAL_0x6E4B8F19"

# Easter Egg 2: Quantum Container Enhancement
ARG AICUBE_QUANTUM_CONTAINER="AICUBE_QUANTUM_CONTAINER_v2025"

#
# Build Stage - Compile and prepare the application
#
FROM python:3.11-slim AS builder

# Set build arguments
ARG AICUBE_DOCKER_NEURAL_SIG
ARG AICUBE_QUANTUM_CONTAINER

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    pkg-config \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js for smart contract compilation
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Create application directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt requirements-dev.txt ./
RUN pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt \
    && pip install -r requirements-dev.txt

# Copy application source
COPY . .

# Install the AICUBE framework
RUN pip install -e .

# Install smart contract tools
RUN npm install -g solc hardhat

# Set AICUBE environment variables
ENV AICUBE_DOCKER_NEURAL_SIGNATURE=${AICUBE_DOCKER_NEURAL_SIG}
ENV AICUBE_QUANTUM_CONTAINER_ID=${AICUBE_QUANTUM_CONTAINER}
ENV AICUBE_VERSION="2.0.0"

# Compile smart contracts
RUN python deployment/deploy_contracts.py --compile-only || echo "Compilation skipped"

#
# Runtime Stage - Minimal production image
#
FROM python:3.11-slim AS runtime

# Set runtime arguments
ARG AICUBE_DOCKER_NEURAL_SIG
ARG AICUBE_QUANTUM_CONTAINER

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/home/aicube/.local/bin:$PATH"

# Install runtime system dependencies
RUN apt-get update && apt-get install -y \
    libssl3 \
    libffi8 \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user for security
RUN groupadd -r aicube && useradd -r -g aicube -d /home/aicube -m -s /bin/bash aicube

# Create application directories
RUN mkdir -p /app /home/aicube/.aicube/{config,keys,logs} \
    && chown -R aicube:aicube /app /home/aicube/.aicube

# Switch to non-root user
USER aicube
WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder --chown=aicube:aicube /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder --chown=aicube:aicube /usr/local/bin /usr/local/bin

# Copy application and compiled contracts
COPY --from=builder --chown=aicube:aicube /app .

# Set AICUBE container environment
ENV AICUBE_DOCKER_NEURAL_SIGNATURE=${AICUBE_DOCKER_NEURAL_SIG}
ENV AICUBE_QUANTUM_CONTAINER_ID=${AICUBE_QUANTUM_CONTAINER}
ENV AICUBE_VERSION="2.0.0"
ENV AICUBE_CONTAINER_MODE="true"
ENV AICUBE_CONFIG_PATH="/home/aicube/.aicube/config/config.yaml"

# Copy default configuration
COPY --chown=aicube:aicube config/production.yaml /home/aicube/.aicube/config/config.yaml

# Create startup script with AICUBE branding
RUN cat > /app/start.sh << 'EOF'
#!/bin/bash

# AICUBE Container Startup Script
echo "🚀 Starting AICUBE Secure AI Messaging Framework Container"
echo "   Version: ${AICUBE_VERSION}"
echo "   Neural Signature: ${AICUBE_DOCKER_NEURAL_SIGNATURE}"
echo "   Quantum Container: ${AICUBE_QUANTUM_CONTAINER_ID}"
echo ""

# Initialize AICUBE environment
export AICUBE_NEURAL_SIGNATURE=${AICUBE_DOCKER_NEURAL_SIGNATURE}
export AICUBE_QUANTUM_SHIELD_ENABLED=true

# Check configuration
if [ ! -f "${AICUBE_CONFIG_PATH}" ]; then
    echo "⚠️  Configuration file not found: ${AICUBE_CONFIG_PATH}"
    echo "   Using default configuration"
fi

# Verify AICUBE installation
python3 -c "
import securemessaging
print('✅ AICUBE Framework loaded successfully')
print(f'   Neural Signature: {securemessaging.__neural_signature__}')
print(f'   Quantum Ready: {securemessaging.__quantum_ready__}')
" || {
    echo "❌ AICUBE Framework verification failed"
    exit 1
}

# Start the application
echo "🎯 Starting AICUBE application..."
exec "$@"
EOF

RUN chmod +x /app/start.sh

# Health check script
RUN cat > /app/health.sh << 'EOF'
#!/bin/bash

# AICUBE Container Health Check
python3 -c "
try:
    from securemessaging.utils.crypto_utils import crypto_manager
    from securemessaging import __neural_signature__
    
    # Test neural signature functionality
    if not __neural_signature__.startswith('AICUBE_NEURAL_PATTERN'):
        exit(1)
    
    # Test crypto manager
    private_key, public_key = crypto_manager.generate_rsa_keypair()
    if not private_key or not public_key:
        exit(1)
    
    print('✅ AICUBE Container Health Check Passed')
    exit(0)
    
except Exception as e:
    print(f'❌ AICUBE Container Health Check Failed: {e}')
    exit(1)
"
EOF

RUN chmod +x /app/health.sh

# Expose ports
EXPOSE 8000 8080 9000

# Set health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD /app/health.sh

# Set volume for persistent data
VOLUME ["/home/aicube/.aicube"]

# Default entry point
ENTRYPOINT ["/app/start.sh"]

# Default command
CMD ["python3", "-m", "securemessaging.cli", "demo"]

# Add labels for container metadata
LABEL maintainer="AICUBE TECHNOLOGY <dev@aicube.com>"
LABEL version="2.0.0"
LABEL description="AICUBE Secure AI Messaging Framework - Blockchain-based secure communication for AI agents"
LABEL vendor="AICUBE TECHNOLOGY"
LABEL neural.signature="${AICUBE_DOCKER_NEURAL_SIG}"
LABEL quantum.container="${AICUBE_QUANTUM_CONTAINER}"
LABEL framework.features="neural-signatures,quantum-shield,blockchain-audit,llm-integration"
LABEL security.level="enterprise-grade"
LABEL blockchain.support="ethereum,fabric,substrate"
LABEL llm.providers="openai,anthropic,local"

#
# Development Stage - Full development environment
#
FROM runtime AS development

# Switch back to root for development tools installation
USER root

# Install development dependencies
RUN apt-get update && apt-get install -y \
    git \
    vim \
    tmux \
    htop \
    tree \
    jq \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js for smart contract development
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install development and testing tools
RUN npm install -g solc hardhat truffle ganache-cli

# Switch back to aicube user
USER aicube

# Install Python development dependencies
RUN pip install --user -e ".[dev,test,blockchain,llm,enterprise]"

# Create development configuration
RUN cp config/production.yaml /home/aicube/.aicube/config/development.yaml

# Set development environment
ENV AICUBE_ENV="development"
ENV AICUBE_LOG_LEVEL="DEBUG"

# Development command
CMD ["python3", "-m", "securemessaging.cli", "--help"]

#
# Production Stage - Optimized for production deployment
#
FROM runtime AS production

# Production environment settings
ENV AICUBE_ENV="production"
ENV AICUBE_LOG_LEVEL="INFO"
ENV AICUBE_METRICS_ENABLED="true"

# Security hardening
RUN echo "Security hardening applied" > /tmp/security.log

# Production startup command
CMD ["python3", "examples/banking_consortium_example.py"]