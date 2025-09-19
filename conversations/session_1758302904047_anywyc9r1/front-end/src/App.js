import React, { useState, useEffect, useRef } from 'react';
import { Home, MessageSquare, Send, ChevronDown, ChevronUp, Bot, User, BrainCircuit, Search, FileText, Coffee, Briefcase, Boxes } from 'lucide-react';

const brandColors = {
  primary: '#00704A', // Starbucks Green
  secondary: '#333333', // Dark Gray
  accent: '#00704A',
  background: '#F9F9F9',
  contentBg: '#FFFFFF',
  text: '#212529',
  lightText: '#6c757d',
  userBubble: '#00704A',
  userText: '#FFFFFF',
  aiBubble: '#F2F2F2',
  reasoningBg: '#FAFAFA',
  borderColor: '#EAEAEA',
};

const styles = {
  appContainer: {
        display: 'flex',
    height: '100vh',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    backgroundColor: brandColors.background},
  sidebar: {
        width: '240px',
    backgroundColor: brandColors.contentBg,
    borderRight: `1px solid ${brandColors.borderColor}`,
    display: 'flex',
    flexDirection: 'column',
    padding: '20px'},
  logo: {
        display: 'flex',
    alignItems: 'center',
    fontSize: '24px',
    fontWeight: 'bold',
    color: brandColors.primary,
    marginBottom: '40px'},
  logoIcon: {
    marginRight: '10px'},
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
    color: brandColors.secondary,
    textDecoration: 'none',
    transition: 'background-color 0.2s, color 0.2s'},
  navItemActive: {
        backgroundColor: brandColors.primary,
    color: 'white'},
  navIcon: {
    marginRight: '12px'},
  mainContent: {
        flex: 1,
    display: 'flex',
    flexDirection: 'column',
    overflow: 'hidden'},
  chatContainer: {
        display: 'flex',
    flexDirection: 'column',
    height: '100%',
    backgroundColor: brandColors.contentBg,
    boxShadow: '0 4px 12px rgba(0,0,0,0.05)'},
  messageList: {
        flex: 1,
    padding: '20px',
    overflowY: 'auto',
    display: 'flex',
    flexDirection: 'column',
    gap: '20px'},
  messageWrapper: {
        display: 'flex',
    flexDirection: 'column',
    maxWidth: '75%'},
  userMessageWrapper: {
        alignSelf: 'flex-end',
    alignItems: 'flex-end'},
  aiMessageWrapper: {
        alignSelf: 'flex-start',
    alignItems: 'flex-start'},
  messageBubble: {
        padding: '12px 18px',
    borderRadius: '20px',
    fontSize: '15px',
    lineHeight: '1.5',
    boxShadow: '0 2px 5px rgba(0,0,0,0.08)'},
  userMessageBubble: {
        backgroundColor: brandColors.userBubble,
    color: brandColors.userText,
    borderBottomRightRadius: '5px'},
  aiMessageBubble: {
        backgroundColor: brandColors.aiBubble,
    color: brandColors.text,
    borderBottomLeftRadius: '5px'},
  avatar: {
        width: '32px',
    height: '32px',
    borderRadius: '50%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: brandColors.primary,
    color: 'white',
    marginRight: '12px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)'},
  userAvatar: {
        backgroundColor: brandColors.secondary,
    alignSelf: 'flex-end',
    marginLeft: '12px'},
  messageHeader: {
        display: 'flex',
    alignItems: 'center',
    marginBottom: '8px'},
  agentName: {
        fontWeight: 'bold',
    fontSize: '14px',
    color: brandColors.secondary},
  inputArea: {
        padding: '20px',
    borderTop: `1px solid ${brandColors.borderColor}`,
    backgroundColor: brandColors.background},
  inputForm: {
        display: 'flex',
    alignItems: 'center',
    backgroundColor: brandColors.contentBg,
    borderRadius: '12px',
    padding: '5px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.07)'},
  textInput: {
        flex: 1,
    border: 'none',
    outline: 'none',
    padding: '12px 15px',
    fontSize: '15px',
    backgroundColor: 'transparent'},
  sendButton: {
        backgroundColor: brandColors.primary,
    border: 'none',
    borderRadius: '8px',
    padding: '10px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    cursor: 'pointer',
    color: 'white',
    transition: 'background-color 0.2s',
    margin: '3px'},
  typingIndicator: {
        display: 'flex',
    alignItems: 'center',
    gap: '5px',
    padding: '10px 20px',
    alignSelf: 'flex-start'},
  typingDot: {
        width: '8px',
    height: '8px',
    borderRadius: '50%',
    backgroundColor: brandColors.lightText,
    animation: 'typing-bounce 1.2s infinite ease-in-out'},
  reasoningPanel: {
        marginTop: '12px',
    backgroundColor: brandColors.reasoningBg,
    border: `1px solid ${brandColors.borderColor}`,
    borderRadius: '12px',
    overflow: 'hidden'},
  reasoningToggle: {
        display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    width: '100%',
    padding: '10px 15px',
    border: 'none',
    background: 'none',
    cursor: 'pointer',
    textAlign: 'left',
    color: brandColors.secondary,
    fontWeight: '600',
    fontSize: '13px'},
  reasoningContent: {
        maxHeight: '0',
    overflow: 'hidden',
    transition: 'max-height 0.4s ease-out'},
  reasoningContentVisible: {
        maxHeight: '500px',
    transition: 'max-height 0.5s ease-in'},
  reasoningSteps: {
        padding: '0 15px 15px 15px',
    display: 'flex',
    flexDirection: 'column',
    gap: '12px'},
  reasoningStep: {
        display: 'flex',
    alignItems: 'center',
    fontSize: '13px',
    color: brandColors.text},
  reasoningIcon: {
        marginRight: '10px',
    color: brandColors.primary},
};

const AGENTS = {
  SHIFT_MANAGER: {
        name: 'Shift Manager AI',
    icon: <Briefcase size={18} />,
    color: '#007bff',
    keywords: ['shift', 'schedule', 'late', 'swap', 'clock in', 'clock out']},
  INVENTORY_SPECIALIST: {
        name: 'Inventory Specialist',
    icon: <Boxes size={18} />,
    color: '#fd7e14',
    keywords: ['stock', 'inventory', 'order', 'supplies', 'cups', 'milk', 'syrup', 'out of']},
  RECIPE_GURU: {
        name: 'Recipe Guru',
    icon: <Coffee size={18} />,
    color: '#6f4e37',
    keywords: ['recipe', 'make', 'how to', 'drink', 'latte', 'frappuccino', 'custom']},
  HR_POLICY_BOT: {
        name: 'HR Policy Bot',
    icon: <FileText size={18} />,
    color: '#dc3545',
    keywords: ['policy', 'dress code', 'sick leave', 'pay', 'benefits']},
  GENERAL_ASSISTANT: {
        name: 'General Assistant',
    icon: <Bot size={18} />,
    color: '#6c757d',
    keywords: []},
};

const initialMessages = [
  {
    id: 1,
    sender: 'ai',
    agent: AGENTS.GENERAL_ASSISTANT,
    text: "Welcome to the Barista Buddy AI Assistant! I can help with recipes, inventory, scheduling, and HR policies. How can I assist you today?",
    reasoning: null},
  {
    id: 2,
    sender: 'user',
    text: "I'm running low on oat milk, what's the current stock level?"},
];

const App = () => {
  const [activePage, setActivePage] = useState('AI Assistant');
  const [messages, setMessages] = useState(initialMessages);
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

  const analyzeAndRoute = (text) => {
    const lowercasedText = text.toLowerCase();
    for (const key in AGENTS) {
      const agent = AGENTS[key];
      if (agent.keywords.some(keyword => lowercasedText.includes(keyword))) {
        return agent;
      }
    }
    return AGENTS.GENERAL_ASSISTANT;
  };

  const generateResponse = (agent, query) => {
    let responseText = "I'm sorry, I couldn't find information on that.";
    const lowercasedQuery = query.toLowerCase();

    if (agent === AGENTS.INVENTORY_SPECIALIST) {
      if (lowercasedQuery.includes('oat milk')) {
        responseText = "We currently have 12 cartons of oat milk in stock. I've also noted that we are running low and added it to the next delivery order.";
      } else if (lowercasedQuery.includes('vanilla syrup')) {
        responseText = "There are 5 bottles of vanilla syrup remaining. This should last about 2 days based on average usage.";
      } else {
        responseText = "I can check inventory levels for you. What specific item are you looking for?";
      }
    } else if (agent === AGENTS.RECIPE_GURU) {
       if (lowercasedQuery.includes('caramel macchiato')) {
        responseText = "For a grande Caramel Macchiato: 2 shots of espresso, 3 pumps of vanilla syrup, steamed milk, and a caramel drizzle topping in a crosshatch pattern.";
       } else {
        responseText = "I can provide recipes for any standard Starbucks drink. Which one would you like to know about?";
       }
    } else if (agent === AGENTS.SHIFT_MANAGER) {
      if (lowercasedQuery.includes('my schedule')) {
        responseText = "You are scheduled to work Wednesday 8am-4pm, Friday 12pm-8pm, and Saturday 7am-3pm this week.";
      } else {
        responseText = "I can help with schedules, shift swaps, and clocking in/out. What do you need assistance with?";
      }
    } else if (agent === AGENTS.HR_POLICY_BOT) {
        if (lowercasedQuery.includes('dress code')) {
            responseText = "The dress code includes a black, gray, or white collared shirt, dark-wash jeans or black pants, and non-slip black shoes. Your green apron must be worn at all times on the floor.";
        } else {
            responseText = "I can answer questions about HR policies like dress code, time off, and benefits.";
        }
    }

    return {
      text: responseText,
      reasoning: {
        analysis: `Detected keywords related to "${agent.keywords.find(k => lowercasedQuery.includes(k)) || 'general inquiry'}".`,
        selection: `Routing to ${agent.name} due to expertise in this area.`,
        knowledgeBase: `Consulting inventory database and ordering system.`,
        generation: `Formulating a response with current stock levels and order status.`},
    };
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
      const selectedAgent = analyzeAndRoute(userMessage.text);
      const aiResponseData = generateResponse(selectedAgent, userMessage.text);

      const aiMessage = {
        id: Date.now() + 1,
        sender: 'ai',
        agent: selectedAgent,
        text: aiResponseData.text,
        reasoning: aiResponseData.reasoning,
      };
      setIsTyping(false);
      setMessages(prev => [...prev, aiMessage]);
    }, 2000 + Math.random() * 1000);
  };

  const Sidebar = () => (
    <div style={styles.sidebar}>
      <div style={styles.logo}>
        <Coffee style={styles.logoIcon} size={30} />
        <span>Barista Buddy</span>
      </div>
      <nav style={styles.nav}>
        <a href="#" style={{ ...(activePage === 'Home' ? styles.navItemActive : {}) }} onClick={() => setActivePage('Home')}>
          <Home style={styles.navIcon} size={20} /> Home
        </a>
        <a href="#" style={{ ...(activePage === 'AI Assistant' ? styles.navItemActive : {}) }} onClick={() => setActivePage('AI Assistant')}>
          <MessageSquare style={styles.navIcon} size={20} /> AI Assistant
        </a>
      </nav>
    </div>
  );

  const ReasoningPanel = ({ reasoning, id }) => {
    if (!reasoning) return null;
    const isExpanded = !!expandedReasoning[id];
    return (
      <div style={styles.reasoningPanel}>
        <button style={styles.reasoningToggle} onClick={() => toggleReasoning(id)}>
          <span style={{display: 'flex', alignItems: 'center'}}><BrainCircuit size={16} style={{marginRight: '8px'}}/> Agent Reasoning</span>
          {isExpanded ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
        </button>
        <div style={{ ...(isExpanded ? styles.reasoningContentVisible : {}) }}>
          <div style={styles.reasoningSteps}>
            <div style={styles.reasoningStep}><Search size={14} style={styles.reasoningIcon} /><div><strong>Analysis:</strong> {reasoning.analysis}</div></div>
            <div style={styles.reasoningStep}><Bot size={14} style={styles.reasoningIcon} /><div><strong>Selection:</strong> {reasoning.selection}</div></div>
            <div style={styles.reasoningStep}><FileText size={14} style={styles.reasoningIcon} /><div><strong>Knowledge:</strong> {reasoning.knowledgeBase}</div></div>
            <div style={styles.reasoningStep}><BrainCircuit size={14} style={styles.reasoningIcon} /><div><strong>Generation:</strong> {reasoning.generation}</div></div>
          </div>
        </div>
      </div>
    );
  };

  const ChatMessage = ({ msg }) => {
    const isUser = msg.sender === 'user';
    return (
      <div style={{ ...(isUser ? styles.userMessageWrapper : styles.aiMessageWrapper) }}>
        {!isUser && (
          <div style={styles.messageHeader}>
            <div style={{ backgroundColor: msg.agent.color }}>{msg.agent.icon}</div>
            <span style={styles.agentName}>{msg.agent.name}</span>
          </div>
        )}
        <div style={{display: 'flex', alignItems: 'flex-end', width: '100%', flexDirection: isUser ? 'row-reverse' : 'row'}}>
            <div style={{...(isUser ? styles.userMessageBubble : styles.aiMessageBubble)}}>
                {msg.text}
            </div>
        </div>
        {!isUser && <ReasoningPanel reasoning={msg.reasoning} id={msg.id} />}
      </div>
    );
  };
  
  const TypingIndicator = () => (
    <div style={styles.aiMessageWrapper}>
        <div style={styles.messageHeader}>
            <div style={{ backgroundColor: brandColors.secondary }}><BrainCircuit size={18} /></div>
            <span style={styles.agentName}>Assistant is thinking...</span>
        </div>
        <div style={{}}>
            <div style={styles.typingIndicator}>
                <div style={{ animationDelay: '0s' }}></div>
                <div style={{ animationDelay: '0.2s' }}></div>
                <div style={{ animationDelay: '0.4s' }}></div>
            </div>
        </div>
    </div>
  );

  return (
    <div style={styles.appContainer}>
      <style>{`
        @keyframes typing-bounce {
          0%, 80%, 100% { transform: scale(0); }
          40% { transform: scale(1.0); }
        }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #f1f1f1; }
        ::-webkit-scrollbar-thumb { background: #ccc; border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: #aaa; }
      `}</style>
      <Sidebar />
      <main style={styles.mainContent}>
        {activePage === 'AI Assistant' ? (
          <div style={styles.chatContainer}>
            <div style={styles.messageList}>
              {messages.map(msg => <ChatMessage key={msg.id} msg={msg} />)}
              {isTyping && <TypingIndicator />}
              <div ref={messagesEndRef} />
            </div>
            <div style={styles.inputArea}>
              <form style={styles.inputForm} onSubmit={handleSendMessage}>
                <input
                  type="text"
                  style={styles.textInput}
                  placeholder="Ask about recipes, inventory, schedules..."
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                />
                <button type="submit" style={styles.sendButton} aria-label="Send">
                  <Send size={20} />
                </button>
              </form>
            </div>
          </div>
        ) : (
          <div style={{padding: 40}}><h1>Home Page</h1><p>Welcome to the dashboard.</p></div>
        )}
      </main>
    </div>
  );
};

export default App;