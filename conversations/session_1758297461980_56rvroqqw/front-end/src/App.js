import React, { useState, useEffect, useRef } from 'react';
import { Home, MessageSquare, Briefcase, FileText, LifeBuoy, ChevronDown, ChevronUp, Send, Bot, CheckCircle, Search, BrainCircuit, Share2 } from 'lucide-react';

// Brand Colors
const brandColors = {
  primary: '#007bff',
  secondary: '#6c757d',
  accent: '#28a745',
  background: '#f8f9fa',
  text: '#212529',
  light: '#ffffff',
  border: '#dee2e6',
  userMessageBg: '#007bff',
  userMessageText: '#ffffff',
  aiMessageBg: '#ffffff',
  aiMessageText: '#212529',
  sidebarBg: '#ffffff',
  sidebarText: '#343a40',
  sidebarActiveBg: '#e9ecef',
  sidebarActiveText: '#007bff',
};

// Agent Definitions
const agents = {
  HR_EXPERT: {
        name: 'HR Expert',
    icon: <Briefcase size={18} />,
    color: '#dc3545',
    specialty: 'Handles questions about vacation, leave, and internal policies.'},
  POLICY_SPECIALIST: {
        name: 'Policy Specialist',
    icon: <FileText size={18} />,
    color: '#ffc107',
    specialty: 'Provides detailed information on company documentation and guidelines.'},
  BENEFITS_ADVISOR: {
        name: 'Benefits Advisor',
    icon: <LifeBuoy size={18} />,
    color: '#17a2b8',
    specialty: 'Advises on health insurance, retirement plans, and other benefits.'},
  GENERAL_ASSISTANT: {
        name: 'General Assistant',
    icon: <Bot size={18} />,
    color: '#6c757d',
    specialty: 'Handles general inquiries and directs questions to the right specialist.'},
};

const App = () => {
  const [activePage, setActivePage] = useState('AI Assistant');
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'ai',
      text: "Hello! I'm your AI Assistant. I can automatically connect you with the right expert for your needs. How can I help you today?",
      agent: agents.GENERAL_ASSISTANT,
      reasoning: null},
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [expandedReasoning, setExpandedReasoning] = useState({});
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const toggleReasoning = (id) => {
    setExpandedReasoning(prev => ({ ...prev, [id]: !prev[id] }));
  };

  const getAgentResponse = (userInput) => {
    const lowerInput = userInput.toLowerCase();
    let selectedAgent = agents.GENERAL_ASSISTANT;
    let analysis = "General inquiry detected.";
    let knowledge = "General knowledge base";

    if (lowerInput.includes('vacation') || lowerInput.includes('leave') || lowerInput.includes('time off')) {
      selectedAgent = agents.HR_EXPERT;
      analysis = "Inquiry related to employee time off detected.";
      knowledge = "Employee Handbook, HR Policies";
    } else if (lowerInput.includes('policy') || lowerInput.includes('guideline') || lowerInput.includes('dress code')) {
      selectedAgent = agents.POLICY_SPECIALIST;
      analysis = "Request for specific company policy information detected.";
      knowledge = "Internal Policy Documents v3.4";
    } else if (lowerInput.includes('health insurance') || lowerInput.includes('benefits') || lowerInput.includes('401k')) {
      selectedAgent = agents.BENEFITS_ADVISOR;
      analysis = "Question about employee benefits package identified.";
      knowledge = "Benefits Provider Contracts, Retirement Plan Docs";
    }
    
    const reasoning = {
      steps: [
        { icon: <Search size={16} />, title: "Query Analysis", description: analysis, status: "Completed" },
        { icon: <Share2 size={16} />, title: "Agent Routing", description: `Optimal agent identified as ${selectedAgent.name} due to expertise in the detected subject matter.`, status: "Completed" },
        { icon: <BrainCircuit size={16} />, title: "Knowledge Retrieval", description: `Consulting relevant documents: ${knowledge}.`, status: "Completed" },
        { icon: <CheckCircle size={16} />, title: "Response Generation", description: "Synthesizing information to formulate a clear and concise answer.", status: "Completed" },
      ]
    };
    
    let responseText = `I've connected you with our ${selectedAgent.name}. `;
    switch(selectedAgent.name) {
      case 'HR Expert':
        responseText += "According to our policy, full-time employees are entitled to 20 days of paid vacation per year. Would you like to submit a time-off request?";
        break;
      case 'Policy Specialist':
        responseText += "The company's official dress code policy is 'business casual.' This generally means slacks or skirts with a blouse or collared shirt. Jeans are permitted on Fridays. For full details, I can send you the official document.";
        break;
      case 'Benefits Advisor':
        responseText += "Our company offers three tiers of health insurance plans through BlueCross. Open enrollment begins in November. I can provide a summary of each plan if you'd like.";
        break;
      default:
        responseText += "I can help with general questions. For more specific topics like HR or benefits, I will route you to the correct specialist.";
        break;
    }

    return { agent: selectedAgent, text: responseText, reasoning };
  };

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const userMessage = {
      id: Date.now(),
      sender: 'user',
      text: inputValue,
    };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsTyping(true);

    setTimeout(() => {
      const aiResponse = getAgentResponse(userMessage.text);
      const aiMessage = {
        id: Date.now() + 1,
        sender: 'ai',
        ...aiResponse,
      };
      setMessages(prev => [...prev, aiMessage]);
      setIsTyping(false);
    }, 2000);
  };

  const styles = {
    appContainer: {
        display: 'flex',
      height: '100vh',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      backgroundColor: brandColors.background},
    sidebar: {
        width: '220px',
      backgroundColor: brandColors.sidebarBg,
      borderRight: `1px solid ${brandColors.border}`,
      padding: '20px',
      display: 'flex',
      flexDirection: 'column'},
    logo: {
        display: 'flex',
      alignItems: 'center',
      fontSize: '24px',
      fontWeight: 'bold',
      color: brandColors.primary,
      marginBottom: '40px',
      padding: '10px 0'},
    nav: {
        display: 'flex',
      flexDirection: 'column',
      gap: '10px'},
    navItem: {
        display: 'flex',
      alignItems: 'center',
      padding: '12px 15px',
      borderRadius: '8px',
      cursor: 'pointer',
      textDecoration: 'none',
      color: brandColors.sidebarText,
      transition: 'background-color 0.2s, color 0.2s',
      fontWeight: 500},
    navItemActive: {
        backgroundColor: brandColors.sidebarActiveBg,
      color: brandColors.sidebarActiveText},
    navIcon: {
      marginRight: '12px'},
    mainContent: {
        flex: 1,
      display: 'flex',
      flexDirection: 'column',
      position: 'relative'},
    chatContainer: {
        flex: 1,
      padding: '20px 40px',
      overflowY: 'auto',
      display: 'flex',
      flexDirection: 'column',
      gap: '20px'},
    messageBubble: {
        maxWidth: '75%',
      padding: '15px 20px',
      borderRadius: '20px',
      lineHeight: '1.5',
      boxShadow: '0 4px 6px rgba(0,0,0,0.05)',
      position: 'relative',
      animation: 'fadeIn 0.5s ease-in-out'},
    userMessage: {
        alignSelf: 'flex-end',
      backgroundColor: brandColors.userMessageBg,
      color: brandColors.userMessageText,
      borderBottomRightRadius: '5px'},
    aiMessage: {
        alignSelf: 'flex-start',
      backgroundColor: brandColors.aiMessageBg,
      color: brandColors.aiMessageText,
      border: `1px solid ${brandColors.border}`,
      borderBottomLeftRadius: '5px'},
    agentBadge: {
        display: 'flex',
      alignItems: 'center',
      gap: '8px',
      marginBottom: '10px',
      fontSize: '14px',
      fontWeight: '600'},
    reasoningToggle: {
        display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      cursor: 'pointer',
      padding: '8px 0',
      marginTop: '15px',
      borderTop: `1px solid ${brandColors.border}`,
      fontSize: '13px',
      color: brandColors.secondary,
      fontWeight: 500},
    reasoningPanel: {
        maxHeight: '0',
      overflow: 'hidden',
      transition: 'max-height 0.4s ease-in-out',
      marginTop: '10px'},
    reasoningPanelExpanded: {
      maxHeight: '500px'},
    reasoningStep: {
        display: 'flex',
        alignItems: 'flex-start',
        marginBottom: '12px',
        fontSize: '13px'},
    reasoningStepIcon: {
        marginRight: '12px',
        color: brandColors.accent,
        marginTop: '3px'},
    reasoningStepContent: {
        display: 'flex',
        flexDirection: 'column'},
    reasoningStepTitle: {
        fontWeight: '600',
        color: brandColors.text},
    reasoningStepDesc: {
        color: brandColors.secondary},
    inputArea: {
        padding: '20px 40px',
      backgroundColor: brandColors.light,
      borderTop: `1px solid ${brandColors.border}`},
    inputForm: {
        display: 'flex',
      alignItems: 'center',
      position: 'relative'},
    textInput: {
        flex: 1,
      padding: '15px 20px',
      borderRadius: '12px',
      border: `1px solid ${brandColors.border}`,
      fontSize: '16px',
      outline: 'none',
      transition: 'border-color 0.2s, box-shadow 0.2s'},
    sendButton: {
        position: 'absolute',
      right: '10px',
      top: '50%',
      transform: 'translateY(-50%)',
      background: brandColors.primary,
      color: 'white',
      border: 'none',
      borderRadius: '8px',
      width: '40px',
      height: '40px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      cursor: 'pointer',
      transition: 'background-color 0.2s'},
    typingIndicator: {
        display: 'flex',
      alignItems: 'center',
      gap: '5px',
      padding: '15px 20px',
      backgroundColor: brandColors.aiMessageBg,
      borderRadius: '20px',
      borderBottomLeftRadius: '5px',
      alignSelf: 'flex-start',
      boxShadow: '0 4px 6px rgba(0,0,0,0.05)',
      border: `1px solid ${brandColors.border}`},
    typingDot: {
        width: '8px',
      height: '8px',
      borderRadius: '50%',
      backgroundColor: brandColors.secondary,
      animation: 'bounce 1.4s infinite ease-in-out both'},
  };

  const keyframes = `
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }
    @keyframes bounce {
      0%, 80%, 100% { transform: scale(0); }
      40% { transform: scale(1.0); }
    }
    input:focus {
        border-color: ${brandColors.primary};
        box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.15);
    }
    .send-button:hover {
        background-color: #0056b3;
    }
  `;

  return (
    <div style={styles.appContainer}>
      <style>{keyframes}</style>
      <div style={styles.sidebar}>
        <div style={styles.logo}>
          <MessageSquare size={28} style={{ marginRight: '10px' }}/>
          <span>Default</span>
        </div>
        <nav style={styles.nav}>
          <a href="#" style={{ ...(activePage === 'Home' ? styles.navItemActive : {}) }} onClick={() => setActivePage('Home')}>
            <Home size={20} style={styles.navIcon} />
            <span>Home</span>
          </a>
          <a href="#" style={{ ...(activePage === 'AI Assistant' ? styles.navItemActive : { }) }} onClick={() => setActivePage('AI Assistant')}>
            <Bot size={20} style={styles.navIcon} />
            <span>AI Assistant</span>
          </a>
        </nav>
      </div>
      <div style={styles.mainContent}>
        <div style={styles.chatContainer}>
          {messages.map((msg) => (
            <div
              key={msg.id}
              style={{
                ...(msg.sender === 'user' ? styles.userMessage : styles.aiMessage) }}
            >
              {msg.sender === 'ai' && msg.agent && (
                <div style={{ color: msg.agent.color }}>
                  {msg.agent.icon}
                  <span>{msg.agent.name} responded</span>
                </div>
              )}
              <p style={{ margin: 0 }}>{msg.text}</p>
              {msg.sender === 'ai' && msg.reasoning && (
                <>
                  <div style={styles.reasoningToggle} onClick={() => toggleReasoning(msg.id)}>
                    <span>Show Reasoning</span>
                    {expandedReasoning[msg.id] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                  </div>
                  <div style={{...(expandedReasoning[msg.id] ? styles.reasoningPanelExpanded : {})}}>
                    {msg.reasoning.steps.map((step, index) => (
                      <div key={index} style={styles.reasoningStep}>
                        <div style={styles.reasoningStepIcon}>{step.icon}</div>
                        <div style={styles.reasoningStepContent}>
                          <span style={styles.reasoningStepTitle}>{step.title}</span>
                          <span style={styles.reasoningStepDesc}>{step.description}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </>
              )}
            </div>
          ))}
          {isTyping && (
            <div style={styles.typingIndicator}>
              <div style={{ animationDelay: '0s' }}></div>
              <div style={{ animationDelay: '0.2s' }}></div>
              <div style={{ animationDelay: '0.4s' }}></div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
        <div style={styles.inputArea}>
          <form style={styles.inputForm} onSubmit={handleSendMessage}>
            <input
              type="text"
              style={styles.textInput}
              placeholder="Ask about HR, policies, benefits, and more..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
            />
            <button type="submit" style={styles.sendButton} className="send-button">
              <Send size={20} />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default App;