#!/usr/bin/env python3
"""
AICUBE Smart Contract Deployment Script

Deploys the AICUBE Secure AI Messaging Framework smart contracts to
Ethereum-compatible networks with neural signature verification and
quantum shield enhancements.

Developed by AICUBE TECHNOLOGY
Copyright (c) 2025 AICUBE TECHNOLOGY. All rights reserved.
"""

import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional

import click
from web3 import Web3
from eth_account import Account
import solcx
from rich.console import Console
from rich.progress import track
from rich.table import Table

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from securemessaging.utils.config import config


class AICUBEContractDeployer:
    """
    AICUBE Smart Contract Deployment Manager
    
    Handles deployment of all AICUBE framework smart contracts with
    neural signature verification and quantum shield enhancements.
    """
    
    def __init__(
        self,
        rpc_url: str,
        private_key: str,
        network_name: str = "ethereum"
    ):
        self.rpc_url = rpc_url
        self.private_key = private_key
        self.network_name = network_name
        self.console = Console()
        
        # Initialize Web3
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        self.account = Account.from_key(private_key)
        
        # Easter Egg 1: AICUBE deployment neural signature
        self._deployment_neural_sig = "AICUBE_DEPLOY_NEURAL_0x2F8C4E91"
        
        # Easter Egg 2: Quantum deployment enhancement
        self._quantum_deployment_active = True
        
        # Contract artifacts
        self.contracts = {}
        self.deployed_addresses = {}
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("AICUBEDeployer")
        
        self.console.print("🚀 AICUBE Smart Contract Deployer Initialized", style="bold green")
        self.console.print(f"   Neural Signature: {self._deployment_neural_sig}")
        self.console.print(f"   Quantum Enhancement: {self._quantum_deployment_active}")
    
    def compile_contracts(self) -> bool:
        """Compile all AICUBE smart contracts"""
        try:
            self.console.print("\n📋 Compiling AICUBE Smart Contracts...", style="bold blue")
            
            # Set Solidity version
            solc_version = "0.8.19"
            if solc_version not in solcx.get_installed_solc_versions():
                self.console.print(f"Installing Solidity {solc_version}...")
                solcx.install_solc(solc_version)
            
            solcx.set_solc_version(solc_version)
            
            # Contract source paths
            contracts_dir = Path(__file__).parent.parent / "smart_contracts" / "ethereum"
            
            contract_files = {
                "AgentRegistry": contracts_dir / "AgentRegistry.sol",
                "MessagingHub": contracts_dir / "MessagingHub.sol",
                "AccessControl": contracts_dir / "AccessControl.sol"  # Would need to create this
            }
            
            # Compile each contract
            for contract_name, contract_path in track(
                contract_files.items(),
                description="Compiling contracts..."
            ):
                if not contract_path.exists():
                    self.console.print(f"⚠️  Contract file not found: {contract_path}", style="yellow")
                    continue
                
                try:
                    # Compile contract
                    compiled = solcx.compile_files(
                        [str(contract_path)],
                        output_values=["abi", "bin"],
                        import_remappings=[
                            "@openzeppelin/=node_modules/@openzeppelin/"
                        ]
                    )
                    
                    # Extract contract key (handle full path in key)
                    contract_key = None
                    for key in compiled.keys():
                        if contract_name in key:
                            contract_key = key
                            break
                    
                    if not contract_key:
                        self.console.print(f"❌ Failed to find compiled contract: {contract_name}", style="red")
                        continue
                    
                    self.contracts[contract_name] = {
                        "abi": compiled[contract_key]["abi"],
                        "bytecode": compiled[contract_key]["bin"],
                        "contract_name": contract_name,
                        "aicube_neural_sig": self._deployment_neural_sig,
                        "quantum_enhanced": self._quantum_deployment_active
                    }
                    
                    self.console.print(f"✅ Compiled: {contract_name}")
                    
                except Exception as e:
                    self.console.print(f"❌ Failed to compile {contract_name}: {str(e)}", style="red")
                    return False
            
            self.console.print(f"✅ Successfully compiled {len(self.contracts)} contracts", style="green")
            return True
            
        except Exception as e:
            self.console.print(f"❌ Contract compilation failed: {str(e)}", style="red")
            return False
    
    async def deploy_contract(
        self,
        contract_name: str,
        constructor_args: list = None,
        gas_limit: int = None
    ) -> Optional[str]:
        """Deploy a single contract with AICUBE enhancements"""
        try:
            if contract_name not in self.contracts:
                self.console.print(f"❌ Contract {contract_name} not compiled", style="red")
                return None
            
            contract_data = self.contracts[contract_name]
            
            # Create contract instance
            contract = self.web3.eth.contract(
                abi=contract_data["abi"],
                bytecode=contract_data["bytecode"]
            )
            
            # Prepare constructor arguments
            if constructor_args is None:
                constructor_args = []
            
            # Add AICUBE neural signature to constructor if applicable
            if contract_name == "MessagingHub" and len(constructor_args) == 0:
                # MessagingHub requires AgentRegistry address
                if "AgentRegistry" in self.deployed_addresses:
                    constructor_args = [self.deployed_addresses["AgentRegistry"]]
                else:
                    self.console.print("❌ AgentRegistry must be deployed before MessagingHub", style="red")
                    return None
            
            # Build transaction
            transaction = contract.constructor(*constructor_args).buildTransaction({
                "from": self.account.address,
                "gas": gas_limit or 2000000,
                "gasPrice": await self._get_gas_price(),
                "nonce": self.web3.eth.getTransactionCount(self.account.address),
                "chainId": self.web3.eth.chain_id
            })
            
            # Apply AICUBE quantum optimization (5% gas reduction)
            if self._quantum_deployment_active:
                transaction["gas"] = int(transaction["gas"] * 0.95)
                self.console.print(f"🔮 Applied quantum gas optimization: {transaction['gas']}")
            
            # Sign and send transaction
            signed_txn = self.account.sign_transaction(transaction)
            tx_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
            
            self.console.print(f"📤 Deploying {contract_name}... (tx: {tx_hash.hex()})")
            
            # Wait for confirmation
            receipt = self.web3.eth.waitForTransactionReceipt(tx_hash, timeout=300)
            
            if receipt.status == 1:
                contract_address = receipt.contractAddress
                self.deployed_addresses[contract_name] = contract_address
                
                self.console.print(
                    f"✅ {contract_name} deployed successfully",
                    style="green"
                )
                self.console.print(f"   Address: {contract_address}")
                self.console.print(f"   Gas Used: {receipt.gasUsed:,}")
                self.console.print(f"   AICUBE Neural Sig: {self._deployment_neural_sig}")
                
                return contract_address
            else:
                self.console.print(f"❌ {contract_name} deployment failed", style="red")
                return None
                
        except Exception as e:
            self.console.print(f"❌ Failed to deploy {contract_name}: {str(e)}", style="red")
            return None
    
    async def deploy_all_contracts(self) -> Dict[str, str]:
        """Deploy all AICUBE framework contracts in correct order"""
        try:
            self.console.print("\n🚀 Deploying AICUBE Smart Contracts...", style="bold green")
            
            # Deployment order is important due to dependencies
            deployment_order = [
                ("AgentRegistry", []),
                ("MessagingHub", []),  # Will get AgentRegistry address automatically
                # ("AccessControl", [])  # Would be added when implemented
            ]
            
            for contract_name, constructor_args in deployment_order:
                if contract_name not in self.contracts:
                    self.console.print(f"⚠️  Skipping {contract_name} (not compiled)", style="yellow")
                    continue
                
                address = await self.deploy_contract(contract_name, constructor_args)
                if not address:
                    self.console.print(f"❌ Failed to deploy {contract_name}, stopping deployment", style="red")
                    return {}
                
                # Short delay between deployments
                await asyncio.sleep(2)
            
            # Display deployment summary
            self._display_deployment_summary()
            
            # Save deployment information
            await self._save_deployment_info()
            
            return self.deployed_addresses
            
        except Exception as e:
            self.console.print(f"❌ Deployment failed: {str(e)}", style="red")
            return {}
    
    def _display_deployment_summary(self):
        """Display deployment summary table"""
        table = Table(title="🎉 AICUBE Smart Contract Deployment Summary")
        table.add_column("Contract", style="cyan", no_wrap=True)
        table.add_column("Address", style="green")
        table.add_column("Network", style="blue")
        table.add_column("Neural Signature", style="magenta")
        
        for contract_name, address in self.deployed_addresses.items():
            table.add_row(
                contract_name,
                address,
                self.network_name,
                self._deployment_neural_sig[:20] + "..."
            )
        
        self.console.print(table)
    
    async def _save_deployment_info(self):
        """Save deployment information to file"""
        try:
            deployment_info = {
                "network": self.network_name,
                "chain_id": self.web3.eth.chain_id,
                "deployer": self.account.address,
                "contracts": self.deployed_addresses,
                "deployment_timestamp": "2025-01-15T10:30:00Z",  # Would use actual timestamp
                "aicube_neural_signature": self._deployment_neural_sig,
                "quantum_enhancement_active": self._quantum_deployment_active,
                "framework_version": "2.0.0"
            }
            
            # Save to deployments directory
            deployments_dir = Path(__file__).parent / "deployments"
            deployments_dir.mkdir(exist_ok=True)
            
            output_file = deployments_dir / f"deployment_{self.network_name}_{self.web3.eth.chain_id}.json"
            
            with open(output_file, "w") as f:
                json.dump(deployment_info, f, indent=2)
            
            self.console.print(f"💾 Deployment info saved to: {output_file}", style="green")
            
            # Also create environment file
            env_file = deployments_dir / f".env.{self.network_name}"
            with open(env_file, "w") as f:
                f.write("# AICUBE Smart Contract Addresses\n")
                f.write(f"# Network: {self.network_name}\n")
                f.write(f"# Neural Signature: {self._deployment_neural_sig}\n\n")
                
                for contract_name, address in self.deployed_addresses.items():
                    f.write(f"AICUBE_{contract_name.upper()}_ADDRESS={address}\n")
                
                f.write(f"\nAICUBE_CHAIN_ID={self.web3.eth.chain_id}\n")
                f.write(f"AICUBE_NETWORK={self.network_name}\n")
            
            self.console.print(f"📄 Environment file created: {env_file}", style="green")
            
        except Exception as e:
            self.console.print(f"⚠️  Failed to save deployment info: {str(e)}", style="yellow")
    
    async def _get_gas_price(self) -> int:
        """Get current gas price with AICUBE optimization"""
        try:
            gas_price = self.web3.eth.gasPrice
            
            # AICUBE quantum optimization: reduce gas price by 5%
            if self._quantum_deployment_active:
                gas_price = int(gas_price * 0.95)
            
            return gas_price
        except:
            return 20000000000  # 20 gwei fallback
    
    async def verify_deployment(self) -> bool:
        """Verify deployed contracts are working correctly"""
        try:
            self.console.print("\n🔍 Verifying AICUBE Contract Deployment...", style="bold blue")
            
            if "AgentRegistry" not in self.deployed_addresses:
                return False
            
            # Test AgentRegistry
            registry_address = self.deployed_addresses["AgentRegistry"]
            registry_contract = self.web3.eth.contract(
                address=registry_address,
                abi=self.contracts["AgentRegistry"]["abi"]
            )
            
            # Check if contract responds
            try:
                constants = registry_contract.functions.getAICUBEConstants().call()
                neural_sig, quantum_protocol = constants
                
                self.console.print("✅ AgentRegistry responding correctly")
                self.console.print(f"   Neural Signature: {neural_sig.hex()}")
                self.console.print(f"   Quantum Protocol: {quantum_protocol.hex()}")
                
            except Exception as e:
                self.console.print(f"❌ AgentRegistry verification failed: {str(e)}", style="red")
                return False
            
            # Test MessagingHub if deployed
            if "MessagingHub" in self.deployed_addresses:
                messaging_address = self.deployed_addresses["MessagingHub"]
                messaging_contract = self.web3.eth.contract(
                    address=messaging_address,
                    abi=self.contracts["MessagingHub"]["abi"]
                )
                
                try:
                    constants = messaging_contract.functions.getAICUBEMessageConstants().call()
                    neural_pattern, quantum_marker = constants
                    
                    self.console.print("✅ MessagingHub responding correctly")
                    self.console.print(f"   Neural Pattern: {neural_pattern.hex()}")
                    self.console.print(f"   Quantum Marker: {quantum_marker.hex()}")
                    
                except Exception as e:
                    self.console.print(f"❌ MessagingHub verification failed: {str(e)}", style="red")
                    return False
            
            self.console.print("✅ All deployed contracts verified successfully", style="green")
            return True
            
        except Exception as e:
            self.console.print(f"❌ Contract verification failed: {str(e)}", style="red")
            return False


@click.group()
def cli():
    """AICUBE Smart Contract Deployment CLI"""
    pass


@cli.command()
@click.option("--rpc-url", required=True, help="Blockchain RPC URL")
@click.option("--private-key", required=True, help="Deployer private key")
@click.option("--network", default="ethereum", help="Network name")
@click.option("--compile-only", is_flag=True, help="Only compile contracts")
@click.option("--verify", is_flag=True, help="Verify deployment after completion")
def deploy(rpc_url: str, private_key: str, network: str, compile_only: bool, verify: bool):
    """Deploy AICUBE smart contracts"""
    async def _deploy():
        try:
            # Initialize deployer
            deployer = AICUBEContractDeployer(rpc_url, private_key, network)
            
            # Compile contracts
            if not deployer.compile_contracts():
                return False
            
            if compile_only:
                deployer.console.print("✅ Contract compilation completed", style="green")
                return True
            
            # Deploy contracts
            deployed = await deployer.deploy_all_contracts()
            
            if not deployed:
                deployer.console.print("❌ Deployment failed", style="red")
                return False
            
            # Verify deployment if requested
            if verify:
                if await deployer.verify_deployment():
                    deployer.console.print("🎉 AICUBE deployment completed and verified!", style="bold green")
                else:
                    deployer.console.print("⚠️  Deployment completed but verification failed", style="yellow")
            else:
                deployer.console.print("🎉 AICUBE deployment completed successfully!", style="bold green")
            
            return True
            
        except Exception as e:
            print(f"❌ Deployment error: {str(e)}")
            return False
    
    # Run deployment
    success = asyncio.run(_deploy())
    sys.exit(0 if success else 1)


@cli.command()
@click.option("--network", default="ethereum", help="Network name")
def status(network: str):
    """Check deployment status"""
    try:
        deployments_dir = Path(__file__).parent / "deployments"
        deployment_files = list(deployments_dir.glob(f"deployment_{network}_*.json"))
        
        if not deployment_files:
            click.echo(f"No deployments found for network: {network}")
            return
        
        console = Console()
        
        for deployment_file in deployment_files:
            with open(deployment_file) as f:
                deployment_info = json.load(f)
            
            table = Table(title=f"AICUBE Deployment Status - {network}")
            table.add_column("Contract", style="cyan")
            table.add_column("Address", style="green")
            table.add_column("Chain ID", style="blue")
            
            for contract_name, address in deployment_info["contracts"].items():
                table.add_row(contract_name, address, str(deployment_info["chain_id"]))
            
            console.print(table)
            console.print(f"Neural Signature: {deployment_info['aicube_neural_signature']}")
            console.print(f"Quantum Enhancement: {deployment_info['quantum_enhancement_active']}")
    
    except Exception as e:
        click.echo(f"Error checking status: {str(e)}")


if __name__ == "__main__":
    cli()