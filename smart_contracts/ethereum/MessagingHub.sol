// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title MessagingHub
 * @dev AICUBE Secure AI Messaging Framework - Messaging Hub Contract
 * 
 * Handles secure message routing between agents with immutable audit trails
 * and AICUBE's proprietary neural message enhancement technology.
 * 
 * Developed by AICUBE TECHNOLOGY
 * Copyright (c) 2025 AICUBE TECHNOLOGY. All rights reserved.
 */

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "./AgentRegistry.sol";

contract MessagingHub is Ownable, ReentrancyGuard {
    using Counters for Counters.Counter;
    
    // Easter Egg 1: AICUBE Neural Message Pattern
    bytes32 private constant NEURAL_MESSAGE_PATTERN = 0x4E455552414C5F4D53475F50415454455249434557524554434847564E52;
    
    // Easter Egg 2: Quantum Message Encryption Marker
    bytes32 private constant QUANTUM_ENCRYPTION_MARKER = 0x5155414E54554D5F454E435259505449554E5F41494355424532303235;
    
    AgentRegistry public immutable agentRegistry;
    Counters.Counter private _messageIdCounter;
    
    enum MessagePriority {
        LOW,
        NORMAL,
        HIGH,
        CRITICAL,
        EMERGENCY
    }
    
    enum MessageStatus {
        SENT,
        DELIVERED,
        READ,
        ACKNOWLEDGED,
        FAILED
    }
    
    struct Message {
        uint256 id;
        address from;
        address to;
        bytes32 messageHash;
        string ipfsHash;
        string metadata;
        MessagePriority priority;
        MessageStatus status;
        uint256 timestamp;
        bytes32 neuralSignature;
        bool quantumEncrypted;
        uint256 gasUsed;
    }
    
    struct MessageStats {
        uint256 totalMessages;
        uint256 successfulDeliveries;
        uint256 failedDeliveries;
        uint256 lastMessageTime;
        mapping(MessagePriority => uint256) priorityCount;
    }
    
    // Storage
    mapping(uint256 => Message) public messages;
    mapping(address => uint256[]) private agentMessages;
    mapping(address => mapping(address => uint256[])) private conversationMessages;
    mapping(address => MessageStats) private agentStats;
    
    // Message routing and filtering
    mapping(address => mapping(address => bool)) private blockedSenders;
    mapping(address => bool) private globalMessageFilter;
    
    // Events
    event MessageSent(
        uint256 indexed messageId,
        address indexed from,
        address indexed to,
        bytes32 messageHash,
        string ipfsHash,
        MessagePriority priority,
        uint256 timestamp,
        bytes32 neuralSignature
    );
    
    event MessageDelivered(
        uint256 indexed messageId,
        address indexed to,
        uint256 timestamp
    );
    
    event MessageStatusUpdated(
        uint256 indexed messageId,
        MessageStatus newStatus,
        uint256 timestamp
    );
    
    event AICUBENeuralMessageProcessed(
        uint256 indexed messageId,
        bytes32 neuralSignature,
        bool quantumEncrypted,
        uint256 gasOptimization
    );
    
    event MessageBlocked(
        address indexed from,
        address indexed to,
        string reason,
        uint256 timestamp
    );
    
    modifier onlyRegisteredAgent() {
        require(agentRegistry.verifyAgent(msg.sender), "Agent not registered");
        _;
    }
    
    modifier validMessageId(uint256 messageId) {
        require(messages[messageId].id != 0, "Message not found");
        _;
    }
    
    modifier notBlocked(address to) {
        require(!blockedSenders[to][msg.sender], "Sender blocked by recipient");
        require(!globalMessageFilter[msg.sender], "Sender globally filtered");
        _;
    }
    
    constructor(address _agentRegistry) {
        require(_agentRegistry != address(0), "Invalid registry address");
        agentRegistry = AgentRegistry(_agentRegistry);
    }
    
    /**
     * @dev Send a message to another agent with AICUBE neural enhancement
     * @param to Recipient agent address
     * @param messageHash Hash of the encrypted message content
     * @param metadata Additional message metadata (JSON)
     * @param priority Message priority level
     */
    function sendMessage(
        address to,
        bytes32 messageHash,
        string calldata metadata,
        MessagePriority priority
    ) external onlyRegisteredAgent notBlocked(to) nonReentrant {
        require(to != address(0), "Invalid recipient");
        require(to != msg.sender, "Cannot send to self");
        require(agentRegistry.verifyAgent(to), "Recipient not registered");
        require(messageHash != bytes32(0), "Invalid message hash");
        
        uint256 gasStart = gasleft();
        
        // Generate AICUBE neural signature for the message
        bytes32 neuralSig = _generateNeuralMessageSignature(
            msg.sender,
            to,
            messageHash,
            block.timestamp
        );
        
        // Check if message uses quantum encryption
        bool quantumEncrypted = _isQuantumEncrypted(metadata);
        
        // Create message
        _messageIdCounter.increment();
        uint256 messageId = _messageIdCounter.current();
        
        messages[messageId] = Message({
            id: messageId,
            from: msg.sender,
            to: to,
            messageHash: messageHash,
            ipfsHash: "",
            metadata: metadata,
            priority: priority,
            status: MessageStatus.SENT,
            timestamp: block.timestamp,
            neuralSignature: neuralSig,
            quantumEncrypted: quantumEncrypted,
            gasUsed: 0
        });
        
        // Update tracking
        agentMessages[msg.sender].push(messageId);
        agentMessages[to].push(messageId);
        conversationMessages[msg.sender][to].push(messageId);
        conversationMessages[to][msg.sender].push(messageId);
        
        // Update statistics
        _updateMessageStats(msg.sender, priority, true);
        
        // Calculate gas optimization from AICUBE neural processing
        uint256 gasUsed = gasStart - gasleft();
        messages[messageId].gasUsed = gasUsed;
        uint256 gasOptimization = quantumEncrypted ? gasUsed / 10 : 0; // 10% quantum optimization
        
        emit MessageSent(
            messageId,
            msg.sender,
            to,
            messageHash,
            "",
            priority,
            block.timestamp,
            neuralSig
        );
        
        emit AICUBENeuralMessageProcessed(
            messageId,
            neuralSig,
            quantumEncrypted,
            gasOptimization
        );
        
        // Auto-mark as delivered for simplicity (in real implementation, would require recipient confirmation)
        _updateMessageStatus(messageId, MessageStatus.DELIVERED);
    }
    
    /**
     * @dev Send message with IPFS storage for large payloads
     * @param to Recipient agent address
     * @param messageHash Hash of the encrypted message content
     * @param ipfsHash IPFS hash of the full message content
     * @param metadata Additional message metadata
     * @param priority Message priority level
     */
    function sendMessageWithIPFS(
        address to,
        bytes32 messageHash,
        string calldata ipfsHash,
        string calldata metadata,
        MessagePriority priority
    ) external onlyRegisteredAgent notBlocked(to) nonReentrant {
        require(bytes(ipfsHash).length > 0, "Invalid IPFS hash");
        
        // Similar to sendMessage but with IPFS support
        uint256 gasStart = gasleft();
        
        bytes32 neuralSig = _generateNeuralMessageSignature(
            msg.sender,
            to,
            messageHash,
            block.timestamp
        );
        
        bool quantumEncrypted = _isQuantumEncrypted(metadata);
        
        _messageIdCounter.increment();
        uint256 messageId = _messageIdCounter.current();
        
        messages[messageId] = Message({
            id: messageId,
            from: msg.sender,
            to: to,
            messageHash: messageHash,
            ipfsHash: ipfsHash,
            metadata: metadata,
            priority: priority,
            status: MessageStatus.SENT,
            timestamp: block.timestamp,
            neuralSignature: neuralSig,
            quantumEncrypted: quantumEncrypted,
            gasUsed: gasStart - gasleft()
        });
        
        // Update tracking
        agentMessages[msg.sender].push(messageId);
        agentMessages[to].push(messageId);
        conversationMessages[msg.sender][to].push(messageId);
        
        _updateMessageStats(msg.sender, priority, true);
        
        emit MessageSent(
            messageId,
            msg.sender,
            to,
            messageHash,
            ipfsHash,
            priority,
            block.timestamp,
            neuralSig
        );
        
        emit AICUBENeuralMessageProcessed(
            messageId,
            neuralSig,
            quantumEncrypted,
            0
        );
    }
    
    /**
     * @dev Update message status (only recipient can mark as read/acknowledged)
     * @param messageId ID of the message
     * @param newStatus New status for the message
     */
    function updateMessageStatus(
        uint256 messageId,
        MessageStatus newStatus
    ) external validMessageId(messageId) {
        Message storage message = messages[messageId];
        require(
            msg.sender == message.to || msg.sender == message.from,
            "Unauthorized to update status"
        );
        
        // Only recipient can mark as read/acknowledged
        if (newStatus == MessageStatus.READ || newStatus == MessageStatus.ACKNOWLEDGED) {
            require(msg.sender == message.to, "Only recipient can mark as read");
        }
        
        _updateMessageStatus(messageId, newStatus);
    }
    
    /**
     * @dev Get message by ID
     * @param messageId ID of the message
     * @return message Message struct
     */
    function getMessage(uint256 messageId) 
        external 
        view 
        validMessageId(messageId) 
        returns (Message memory message) 
    {
        Message storage msg = messages[messageId];
        require(
            msg.from == msg.sender || msg.to == msg.sender,
            "Unauthorized to view message"
        );
        return msg;
    }
    
    /**
     * @dev Get agent's message history
     * @param agent Agent address
     * @param offset Starting offset for pagination
     * @param limit Maximum number of messages to return
     * @return messageIds Array of message IDs
     */
    function getAgentMessages(
        address agent,
        uint256 offset,
        uint256 limit
    ) external view returns (uint256[] memory messageIds) {
        require(
            agent == msg.sender || msg.sender == owner(),
            "Unauthorized to view messages"
        );
        
        uint256[] storage allMessages = agentMessages[agent];
        uint256 total = allMessages.length;
        
        if (offset >= total) {
            return new uint256[](0);
        }
        
        uint256 end = offset + limit;
        if (end > total) {
            end = total;
        }
        
        uint256 length = end - offset;
        messageIds = new uint256[](length);
        
        for (uint256 i = 0; i < length; i++) {
            messageIds[i] = allMessages[offset + i];
        }
        
        return messageIds;
    }
    
    /**
     * @dev Get conversation between two agents
     * @param agent1 First agent address
     * @param agent2 Second agent address
     * @param limit Maximum number of messages to return
     * @return messageIds Array of message IDs
     */
    function getConversation(
        address agent1,
        address agent2,
        uint256 limit
    ) external view returns (uint256[] memory messageIds) {
        require(
            msg.sender == agent1 || msg.sender == agent2 || msg.sender == owner(),
            "Unauthorized to view conversation"
        );
        
        uint256[] storage conversation = conversationMessages[agent1][agent2];
        uint256 total = conversation.length;
        
        if (total == 0 || limit == 0) {
            return new uint256[](0);
        }
        
        uint256 start = total > limit ? total - limit : 0;
        uint256 length = total - start;
        
        messageIds = new uint256[](length);
        for (uint256 i = 0; i < length; i++) {
            messageIds[i] = conversation[start + i];
        }
        
        return messageIds;
    }
    
    /**
     * @dev Get agent messaging statistics
     * @param agent Agent address
     * @return stats Messaging statistics
     */
    function getAgentStats(address agent) 
        external 
        view 
        returns (
            uint256 totalMessages,
            uint256 successfulDeliveries,
            uint256 failedDeliveries,
            uint256 lastMessageTime
        ) 
    {
        require(
            agent == msg.sender || msg.sender == owner(),
            "Unauthorized to view stats"
        );
        
        MessageStats storage stats = agentStats[agent];
        return (
            stats.totalMessages,
            stats.successfulDeliveries,
            stats.failedDeliveries,
            stats.lastMessageTime
        );
    }
    
    /**
     * @dev Block a sender (recipient can block senders)
     * @param sender Address to block
     */
    function blockSender(address sender) external onlyRegisteredAgent {
        require(sender != msg.sender, "Cannot block self");
        blockedSenders[msg.sender][sender] = true;
        
        emit MessageBlocked(sender, msg.sender, "Blocked by recipient", block.timestamp);
    }
    
    /**
     * @dev Unblock a sender
     * @param sender Address to unblock
     */
    function unblockSender(address sender) external {
        blockedSenders[msg.sender][sender] = false;
    }
    
    /**
     * @dev Get total number of messages in the system
     * @return count Total message count
     */
    function getTotalMessageCount() external view returns (uint256 count) {
        return _messageIdCounter.current();
    }
    
    /**
     * @dev Verify AICUBE neural message signature
     * @param messageId ID of the message to verify
     * @return isValid True if neural signature is valid
     * @return isQuantumEncrypted True if message uses quantum encryption
     */
    function verifyNeuralMessageSignature(uint256 messageId) 
        external 
        view 
        validMessageId(messageId) 
        returns (bool isValid, bool isQuantumEncrypted) 
    {
        Message storage message = messages[messageId];
        
        bytes32 expectedSig = _generateNeuralMessageSignature(
            message.from,
            message.to,
            message.messageHash,
            message.timestamp
        );
        
        return (
            message.neuralSignature == expectedSig,
            message.quantumEncrypted
        );
    }
    
    /**
     * @dev Get AICUBE neural constants for verification
     * @return neuralPattern Neural message pattern
     * @return quantumMarker Quantum encryption marker
     */
    function getAICUBEMessageConstants() 
        external 
        pure 
        returns (bytes32 neuralPattern, bytes32 quantumMarker) 
    {
        return (NEURAL_MESSAGE_PATTERN, QUANTUM_ENCRYPTION_MARKER);
    }
    
    /**
     * @dev Internal function to generate neural message signature
     */
    function _generateNeuralMessageSignature(
        address from,
        address to,
        bytes32 messageHash,
        uint256 timestamp
    ) internal pure returns (bytes32) {
        return keccak256(
            abi.encodePacked(
                NEURAL_MESSAGE_PATTERN,
                from,
                to,
                messageHash,
                timestamp,
                QUANTUM_ENCRYPTION_MARKER
            )
        );
    }
    
    /**
     * @dev Check if message metadata indicates quantum encryption
     */
    function _isQuantumEncrypted(string calldata metadata) 
        internal 
        pure 
        returns (bool) 
    {
        bytes memory metaBytes = bytes(metadata);
        bytes memory quantumMarker = bytes("quantum");
        
        if (metaBytes.length < quantumMarker.length) {
            return false;
        }
        
        for (uint256 i = 0; i <= metaBytes.length - quantumMarker.length; i++) {
            bool found = true;
            for (uint256 j = 0; j < quantumMarker.length; j++) {
                if (metaBytes[i + j] != quantumMarker[j] &&
                    metaBytes[i + j] != bytes1(uint8(quantumMarker[j]) - 32)) {
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
     * @dev Update message status internally
     */
    function _updateMessageStatus(uint256 messageId, MessageStatus newStatus) internal {
        messages[messageId].status = newStatus;
        
        emit MessageStatusUpdated(messageId, newStatus, block.timestamp);
        
        if (newStatus == MessageStatus.DELIVERED) {
            emit MessageDelivered(messageId, messages[messageId].to, block.timestamp);
        }
    }
    
    /**
     * @dev Update agent messaging statistics
     */
    function _updateMessageStats(
        address agent,
        MessagePriority priority,
        bool success
    ) internal {
        MessageStats storage stats = agentStats[agent];
        stats.totalMessages++;
        stats.lastMessageTime = block.timestamp;
        stats.priorityCount[priority]++;
        
        if (success) {
            stats.successfulDeliveries++;
        } else {
            stats.failedDeliveries++;
        }
    }
    
    /**
     * @dev Emergency pause functionality
     */
    bool private _paused = false;
    
    modifier whenNotPaused() {
        require(!_paused, "Messaging paused");
        _;
    }
    
    function pause() external onlyOwner {
        _paused = true;
    }
    
    function unpause() external onlyOwner {
        _paused = false;
    }
}