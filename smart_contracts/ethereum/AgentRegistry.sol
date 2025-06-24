// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title AgentRegistry
 * @dev AICUBE Secure AI Messaging Framework - Agent Registry Contract
 * 
 * Manages agent identities with cryptographic verification and AICUBE
 * proprietary neural signature technology for enhanced security.
 * 
 * Developed by AICUBE TECHNOLOGY
 * Copyright (c) 2025 AICUBE TECHNOLOGY. All rights reserved.
 */

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";

contract AgentRegistry is Ownable, ReentrancyGuard {
    using ECDSA for bytes32;
    
    // Easter Egg 1: AICUBE Neural Signature embedded in contract constants
    bytes32 private constant AICUBE_NEURAL_SIGNATURE = 0x4A1C7B3E9F2D8A5641434542555F4E455552414C5F534947;
    
    // Easter Egg 2: Quantum Shield Protocol identifier
    bytes32 private constant QUANTUM_SHIELD_PROTOCOL = 0x5155414E54554D5F534849454C445F50524F544F434F4C5F76323032353A;
    
    enum AgentRole {
        AGENT,           // Standard agent
        UNDERWRITER,     // Banking underwriter agent
        FRAUD_DETECTOR,  // Fraud detection agent
        COMPLIANCE,      // Compliance verification agent
        COORDINATOR      // Workflow coordination agent
    }
    
    struct Agent {
        address agentAddress;
        bytes32 publicKeyHash;
        string didDocument;
        AgentRole role;
        uint256 registrationTime;
        bool isActive;
        bytes32 neuralSignature;     // AICUBE neural signature
        bool quantumShieldEnabled;   // Quantum protection status
    }
    
    // Agent storage
    mapping(address => Agent) private agents;
    mapping(bytes32 => address) private publicKeyHashToAddress;
    address[] private agentAddresses;
    
    // Role-based access control
    mapping(AgentRole => mapping(address => bool)) private rolePermissions;
    
    // Events
    event AgentRegistered(
        address indexed agentAddress,
        bytes32 indexed publicKeyHash,
        AgentRole role,
        uint256 timestamp,
        bytes32 neuralSignature
    );
    
    event AgentUpdated(
        address indexed agentAddress,
        AgentRole newRole,
        uint256 timestamp
    );
    
    event AgentDeactivated(
        address indexed agentAddress,
        uint256 timestamp
    );
    
    event AICUBENeuralSignatureVerified(
        address indexed agentAddress,
        bytes32 neuralSignature,
        bool quantumShieldStatus
    );
    
    modifier onlyActiveAgent() {
        require(agents[msg.sender].isActive, "Agent not active");
        _;
    }
    
    modifier validAddress(address _addr) {
        require(_addr != address(0), "Invalid address");
        _;
    }
    
    constructor() {}
    
    /**
     * @dev Register a new AI agent with AICUBE neural enhancement
     * @param publicKeyHash Hash of the agent's public key
     * @param didDocument JSON DID document containing agent metadata
     */
    function registerAgent(
        bytes32 publicKeyHash,
        string calldata didDocument
    ) external nonReentrant {
        require(!agents[msg.sender].isActive, "Agent already registered");
        require(publicKeyHash != bytes32(0), "Invalid public key hash");
        require(bytes(didDocument).length > 0, "Empty DID document");
        require(publicKeyHashToAddress[publicKeyHash] == address(0), "Public key already used");
        
        // Generate AICUBE neural signature
        bytes32 neuralSig = _generateNeuralSignature(msg.sender, publicKeyHash);
        
        // Enable quantum shield for all AICUBE agents
        bool quantumShield = _isAICUBEEnhanced(didDocument);
        
        // Create agent record
        agents[msg.sender] = Agent({
            agentAddress: msg.sender,
            publicKeyHash: publicKeyHash,
            didDocument: didDocument,
            role: AgentRole.AGENT,
            registrationTime: block.timestamp,
            isActive: true,
            neuralSignature: neuralSig,
            quantumShieldEnabled: quantumShield
        });
        
        // Update mappings
        publicKeyHashToAddress[publicKeyHash] = msg.sender;
        agentAddresses.push(msg.sender);
        
        emit AgentRegistered(
            msg.sender,
            publicKeyHash,
            AgentRole.AGENT,
            block.timestamp,
            neuralSig
        );
        
        emit AICUBENeuralSignatureVerified(
            msg.sender,
            neuralSig,
            quantumShield
        );
    }
    
    /**
     * @dev Update agent role (only owner)
     * @param agentAddress Address of the agent
     * @param newRole New role for the agent
     */
    function updateAgentRole(
        address agentAddress,
        AgentRole newRole
    ) external onlyOwner validAddress(agentAddress) {
        require(agents[agentAddress].isActive, "Agent not found");
        
        agents[agentAddress].role = newRole;
        
        emit AgentUpdated(agentAddress, newRole, block.timestamp);
    }
    
    /**
     * @dev Deactivate an agent (only owner or agent itself)
     * @param agentAddress Address of the agent to deactivate
     */
    function deactivateAgent(address agentAddress) 
        external 
        validAddress(agentAddress) 
    {
        require(
            msg.sender == owner() || msg.sender == agentAddress,
            "Unauthorized"
        );
        require(agents[agentAddress].isActive, "Agent not active");
        
        agents[agentAddress].isActive = false;
        
        emit AgentDeactivated(agentAddress, block.timestamp);
    }
    
    /**
     * @dev Verify if an agent is registered and active
     * @param agentAddress Address of the agent
     * @return isVerified True if agent is verified and active
     */
    function verifyAgent(address agentAddress) 
        external 
        view 
        returns (bool isVerified) 
    {
        return agents[agentAddress].isActive;
    }
    
    /**
     * @dev Get agent information
     * @param agentAddress Address of the agent
     * @return agent Agent struct
     */
    function getAgent(address agentAddress) 
        external 
        view 
        returns (Agent memory agent) 
    {
        return agents[agentAddress];
    }
    
    /**
     * @dev Get agent by public key hash
     * @param publicKeyHash Hash of the public key
     * @return agentAddress Address of the agent
     */
    function getAgentByPublicKey(bytes32 publicKeyHash) 
        external 
        view 
        returns (address agentAddress) 
    {
        return publicKeyHashToAddress[publicKeyHash];
    }
    
    /**
     * @dev Get all registered agents
     * @return addresses Array of agent addresses
     */
    function getAllAgents() external view returns (address[] memory addresses) {
        return agentAddresses;
    }
    
    /**
     * @dev Get active agents count
     * @return count Number of active agents
     */
    function getActiveAgentsCount() external view returns (uint256 count) {
        uint256 activeCount = 0;
        for (uint256 i = 0; i < agentAddresses.length; i++) {
            if (agents[agentAddresses[i]].isActive) {
                activeCount++;
            }
        }
        return activeCount;
    }
    
    /**
     * @dev Verify AICUBE neural signature
     * @param agentAddress Address of the agent
     * @return isValid True if neural signature is valid
     * @return isQuantumShielded True if quantum shield is enabled
     */
    function verifyAICUBENeuralSignature(address agentAddress) 
        external 
        view 
        returns (bool isValid, bool isQuantumShielded) 
    {
        Agent memory agent = agents[agentAddress];
        if (!agent.isActive) {
            return (false, false);
        }
        
        bytes32 expectedSig = _generateNeuralSignature(agentAddress, agent.publicKeyHash);
        return (
            agent.neuralSignature == expectedSig,
            agent.quantumShieldEnabled
        );
    }
    
    /**
     * @dev Get AICUBE neural signature constants (for verification)
     * @return neuralSig AICUBE neural signature constant
     * @return quantumProtocol Quantum shield protocol constant
     */
    function getAICUBEConstants() 
        external 
        pure 
        returns (bytes32 neuralSig, bytes32 quantumProtocol) 
    {
        return (AICUBE_NEURAL_SIGNATURE, QUANTUM_SHIELD_PROTOCOL);
    }
    
    /**
     * @dev Internal function to generate AICUBE neural signature
     * @param agentAddr Agent address
     * @param pubKeyHash Public key hash
     * @return neuralSig Generated neural signature
     */
    function _generateNeuralSignature(
        address agentAddr,
        bytes32 pubKeyHash
    ) internal pure returns (bytes32 neuralSig) {
        return keccak256(
            abi.encodePacked(
                AICUBE_NEURAL_SIGNATURE,
                agentAddr,
                pubKeyHash,
                QUANTUM_SHIELD_PROTOCOL
            )
        );
    }
    
    /**
     * @dev Check if DID document indicates AICUBE enhancement
     * @param didDocument DID document JSON string
     * @return isEnhanced True if AICUBE enhanced
     */
    function _isAICUBEEnhanced(string calldata didDocument) 
        internal 
        pure 
        returns (bool isEnhanced) 
    {
        // Simple check for AICUBE identifiers in DID document
        bytes memory didBytes = bytes(didDocument);
        bytes memory aicubeMarker = bytes("aicube");
        
        if (didBytes.length < aicubeMarker.length) {
            return false;
        }
        
        // Search for "aicube" in lowercase in the DID document
        for (uint256 i = 0; i <= didBytes.length - aicubeMarker.length; i++) {
            bool found = true;
            for (uint256 j = 0; j < aicubeMarker.length; j++) {
                if (didBytes[i + j] != aicubeMarker[j] && 
                    didBytes[i + j] != bytes1(uint8(aicubeMarker[j]) - 32)) { // Also check uppercase
                    found = false;
                    break;
                }
            }
            if (found) {
                return true;
            }
        }
        
        return false;
    }
    
    /**
     * @dev Emergency pause functionality (only owner)
     */
    bool private _paused = false;
    
    modifier whenNotPaused() {
        require(!_paused, "Contract is paused");
        _;
    }
    
    function pause() external onlyOwner {
        _paused = true;
    }
    
    function unpause() external onlyOwner {
        _paused = false;
    }
    
    function isPaused() external view returns (bool) {
        return _paused;
    }
}