import React, { useState, useEffect, useRef } from 'react';
import { Home, MessageCircle, Bot, User, ChevronDown, ChevronUp, UserPlus, TrendingUp, HeartHandshake, BookOpen } from 'lucide-react';

const brandColors = {
  primary: '#E50914',
  secondary: '#221F1F',
  accent: '#F5F5F1',
  background: '#000000',
  text: '#FFFFFF',
  textSecondary: '#B3B3B3',
  bubbleUser: '#333333',
  bubbleAi: '#221F1F',
};

const styles = {
  app: {
        display: 'flex',
    height: '100vh',
    backgroundColor: brandColors.background,
    color: brandColors.text,
    fontFamily: '"Netflix Sans", Helvetica, Arial, sans-serif'},
  sidebar: {
        width: '240px',
    backgroundColor: brandColors.secondary,
    padding: '2rem 1rem',
    display: 'flex',
    flexDirection: 'column',
    borderRight: '1px solid #222'},
  logo: {
        fontSize: '2rem',
    fontWeight: 'bold',
    color: brandColors.primary,
    marginBottom: '3rem',
    textAlign: 'center',
    letterSpacing: '2px'},
  nav: {
        display: 'flex',
    flexDirection: 'column',
    gap: '0.5rem'},
  navItem: {
        display: 'flex',
    alignItems: 'center',
    padding: '0.75rem 1rem',
    borderRadius: '6px',
    cursor: 'pointer',
    transition: 'background-color 0.2s ease',
    fontSize: '1rem'},
  navItemActive: {
        backgroundColor: brandColors.primary,
    color: brandColors.text},
  navItemInactive: {
    color: brandColors.textSecondary},
  navIcon: {
    marginRight: '0.75rem'},
  mainContent: {
        flex: 1,
    display: 'flex',
    flexDirection: 'column',
    overflow: 'hidden'},
  chatContainer: {
        flex: 1,
    display: 'flex',
    flexDirection: 'column',
    padding: '1.5rem',
    overflowY: 'auto'},
  messageList: {
        flex: 1,
    display: 'flex',
    flexDirection: 'column',
    gap: '1.5rem',
    paddingRight: '1rem',
    overflowY: 'auto'},
  inputArea: {
        padding: '1.5rem',
    borderTop: `1px solid ${brandColors.secondary}`,
    display: 'flex',
    alignItems: 'center',
    backgroundColor: brandColors.background},
  inputWrapper: {
        display: 'flex',
    alignItems: 'center',
    width: '100%',
    backgroundColor: brandColors.secondary,
    borderRadius: '8px',
    padding: '0.5rem 1rem'},
  textInput: {
        flex: 1,
    backgroundColor: 'transparent',
    border: 'none',
    color: brandColors.text,
    fontSize: '1rem',
    padding: '0.5rem',
    outline: 'none'},
  sendButton: {
        backgroundColor: brandColors.primary,
    color: brandColors.text,
    border: 'none',
    borderRadius: '6px',
    padding: '0.75rem 1.5rem',
    fontSize: '1rem',
    cursor: 'pointer',
    transition: 'opacity 0.2s ease'},
  messageBubble: {
        maxWidth: '75%',
    padding: '1rem',
    borderRadius: '12px',
    display: 'flex',
    flexDirection: 'column',
    position: 'relative',
    boxShadow: '0 4px 12px rgba(0,0,0,0.3)'},
  userMessage: {
        alignSelf: 'flex-end',
    backgroundColor: brandColors.bubbleUser,
    borderBottomRightRadius: '2px'},
  aiMessage: {
        alignSelf: 'flex-start',
    backgroundColor: brandColors.bubbleAi,
    borderBottomLeftRadius: '2px'},
  messageContent: {
        whiteSpace: 'pre-wrap',
    lineHeight: '1.5'},
  agentAttribution: {
        display: 'flex',
    alignItems: 'center',
    marginTop: '1rem',
    paddingTop: '0.75rem',
    borderTop: `1px solid ${brandColors.bubbleUser}`},
  agentIcon: {
        width: '32px',
    height: '32px',
    borderRadius: '50%',
    backgroundColor: brandColors.primary,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: '0.75rem'},
  agentInfo: {
        display: 'flex',
    flexDirection: 'column'},
  agentName: {
        fontWeight: 'bold',
    fontSize: '0.9rem'},
  agentTitle: {
        fontSize: '0.8rem',
    color: brandColors.textSecondary},
  reasoningToggle: {
        display: 'flex',
    alignItems: 'center',
    cursor: 'pointer',
    color: brandColors.textSecondary,
    fontSize: '0.8rem',
    marginTop: '1rem',
    userSelect: 'none'},
  reasoningPanel: {
        backgroundColor: 'rgba(0,0,0,0.3)',
    borderRadius: '8px',
    padding: '0.75rem',
    marginTop: '0.75rem',
    overflow: 'hidden',
    transition: 'max-height 0.4s ease-in-out, opacity 0.4s ease-in-out'},
  reasoningStep: {
        fontSize: '0.8rem',
    marginBottom: '0.5rem',
    lineHeight: '1.4'},
  thinkingIndicator: {
        display: 'flex',
    alignItems: 'center',
    gap: '5px',
    padding: '1rem',
    backgroundColor: brandColors.bubbleAi,
    borderRadius: '12px',
    alignSelf: 'flex-start'},
};

const agents = {
  ONBOARDING_SPECIALIST: {
        name: "Onboarding Specialist",
    title: "AI Agent",
    icon: <UserPlus size={18} />},
  PERFORMANCE_COACH: {
        name: "Performance Coach",
    title: "AI Agent",
    icon: <TrendingUp size={18} />},
  BENEFITS_ADVISOR: {
        name: "Benefits Advisor",
    title: "AI Agent",
    icon: <HeartHandshake size={18} />},
  POLICY_EXPERT: {
        name: "Policy Expert",
    title: "AI Agent",
    icon: <BookOpen size={18} />},
  GENERAL_ASSISTANT: {
        name: "General Assistant",
    title: "AI Agent",
    icon: <Bot size={18} />},
};

const initialMessages = [
  {
    id: 1,
    sender: 'ai',
    text: "Welcome to Netflix! I'm your intelligent HR assistant. I can help with onboarding, performance reviews, benefits, and more. How can I assist you today?",
    agent: agents.GENERAL_ASSISTANT,
    reasoning: {
        analysis: "Initiating conversation as the primary point of contact.",
      selection: "Selected General Assistant for a broad, welcoming introduction.",
      knowledge: "Loaded general HR knowledge base and company-wide information.",
      generation: "Crafted a friendly and informative welcome message."},
  },
  {
    id: 2,
    sender: 'user',
    text: "Hi, I'm a new hire. I need to find my onboarding checklist and I also have a question about how performance reviews work here."},
];

const getAgentForQuery = (query) => {
  const q = query.toLowerCase();
  if (q.includes('performance') || q.includes('review') || q.includes('feedback')) {
    return { 
        agent: agents.PERFORMANCE_COACH, 
        response: "Of course. At Netflix, we have a unique approach to performance focused on continuous feedback and impact. For new hires, your first formal check-in is after 90 days. We use a 360-degree feedback model where you'll receive input from your manager, peers, and direct reports if applicable. The key is to 'seek to understand' and focus on growth. Would you like me to detail the process?",
        reasoning: {
        analysis: "User query contains keywords 'performance reviews'. This is a specialized topic.",
            selection: "Routing to Performance Coach AI, which is trained on Netflix's culture of freedom and responsibility and performance management systems.",
            knowledge: "Accessed internal documents on performance cycles, 360-feedback tools, and new hire integration.",
            generation: "Formulated a concise overview of the performance review philosophy, mentioning the 90-day check-in relevant to a new hire."
        }
    };
  }
  if (q.includes('onboarding') || q.includes('new hire') || q.includes('checklist')) {
    return {
        agent: agents.ONBOARDING_SPECIALIST,
        response: "Welcome to the team! You can find your personalized onboarding checklist on our internal portal, 'Streamline'. It will guide you through everything from setting up your tech to essential first-week meetings. Here is a direct link: [link to Streamline Onboarding].",
        reasoning: {
        analysis: "User identified as a 'new hire' and asked for the 'onboarding checklist'.",
            selection: "Routing to the Onboarding Specialist AI, which has direct access to new hire resources and timelines.",
            knowledge: "Queried the Streamline portal database for the standard new hire checklist.",
            generation: "Provided a direct answer with a helpful link to the resource."
        }
    };
  }
  if (q.includes('benefits') || q.includes('health') || q.includes('dental') || q.includes('401k')) {
      return {
          agent: agents.BENEFITS_ADVISOR,
          response: "I can certainly help with benefits. Netflix offers a comprehensive benefits package designed to support our employees' well-being. What specific area are you interested in? (e.g., health insurance, retirement plans, parental leave)",
          reasoning: {
        analysis: "Detected keywords related to employee benefits.",
            selection: "Routing to the Benefits Advisor AI, which is trained on all compensation and benefits documentation.",
            knowledge: "Accessed the complete benefits summary document.",
            generation: "Crafted a helpful starting point and asked a clarifying question to provide more specific information."
          }
      }
  }
  return {
    agent: agents.GENERAL_ASSISTANT,
    response: "I'm not sure I have the specific information for that, but I can try to find someone who does. Could you please rephrase your question?",
    reasoning: {
        analysis: "Query did not match specific keywords for specialized agents.",
        selection: "Defaulting to General Assistant to handle the query or escalate.",
        knowledge: "Performed a broad search across general knowledge bases.",
        generation: "Generated a polite response indicating a lack of specific knowledge and asking for clarification."
    }
  };
};

const ThinkingIndicator = () => (
  <div style={styles.thinkingIndicator}>
    <div style={{ animation: 'bounce 1.4s infinite ease-in-out both' }}></div>
    <div style={{ animation: 'bounce 1.4s infinite ease-in-out both', animationDelay: '0.16s' }}></div>
    <div style={{ animation: 'bounce 1.4s infinite ease-in-out both', animationDelay: '0.32s' }}></div>
    <style>{`
      @keyframes bounce {
        0%, 80%, 100% { transform: scale(0); }
        40% { transform: scale(1.0); }
      }
      .dot {
        width: 8px;
        height: 8px;
        background-color: ${brandColors.textSecondary};
        border-radius: 50%;
        display: inline-block;
      }
    `}</style>
  </div>
);

const ChatMessage = ({ message }) => {
  const [isReasoningOpen, setIsReasoningOpen] = useState(false);
  const isUser = message.sender === 'user';

  return (
    <div style={{ ...(isUser ? styles.userMessage : styles.aiMessage) }}>
      <div style={styles.messageContent}>{message.text}</div>
      {!isUser && message.agent && (
        <>
          <div style={styles.agentAttribution}>
            <div style={styles.agentIcon}>{message.agent.icon}</div>
            <div style={styles.agentInfo}>
              <span style={styles.agentName}>{message.agent.name}</span>
              <span style={styles.agentTitle}>{message.agent.title}</span>
            </div>
          </div>
          {message.reasoning && (
            <>
              <div style={styles.reasoningToggle} onClick={() => setIsReasoningOpen(!isReasoningOpen)}>
                {isReasoningOpen ? <ChevronUp size={14} style={{ marginRight: '0.25rem' }} /> : <ChevronDown size={14} style={{ marginRight: '0.25rem' }} />}
                Show Agent Reasoning
              </div>
              <div style={{ maxHeight: isReasoningOpen ? '200px' : '0', opacity: isReasoningOpen ? 1 : 0 }}>
                <div style={styles.reasoningStep}><strong>Analysis:</strong> {message.reasoning.analysis}</div>
                <div style={styles.reasoningStep}><strong>Agent Selection:</strong> {message.reasoning.selection}</div>
                <div style={styles.reasoningStep}><strong>Knowledge Base:</strong> {message.reasoning.knowledge}</div>
                <div style={styles.reasoningStep}><strong>Response Generation:</strong> {message.reasoning.generation}</div>
              </div>
            </>
          )}
        </>
      )}
    </div>
  );
};

const HRChatbot = () => {
  const [messages, setMessages] = useState(initialMessages);
  const [inputValue, setInputValue] = useState('');
  const [isThinking, setIsThinking] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isThinking]);
  
  useEffect(() => {
     if (messages.length === 2) {
       handleAutomatedResponse(messages[1].text);
     }
  }, []);

  const handleAutomatedResponse = (query) => {
    setIsThinking(true);
    setTimeout(() => {
      const { agent, response, reasoning } = getAgentForQuery(query);
      const aiMessage = {
        id: Date.now(),
        sender: 'ai',
        text: response,
        agent,
        reasoning,
      };
      setMessages(prev => [...prev, aiMessage]);
      setIsThinking(false);
    }, 2500);
  };

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (inputValue.trim() === '') return;

    const userMessage = {
      id: Date.now(),
      sender: 'user',
      text: inputValue.trim(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    handleAutomatedResponse(inputValue.trim());
  };

  return (
    <div style={styles.mainContent}>
      <div style={styles.chatContainer}>
        <div style={styles.messageList}>
          {messages.map(msg => <ChatMessage key={msg.id} message={msg} />)}
          {isThinking && <ThinkingIndicator />}
          <div ref={messagesEndRef} />
        </div>
      </div>
      <form style={styles.inputArea} onSubmit={handleSendMessage}>
        <div style={styles.inputWrapper}>
          <input
            type="text"
            style={styles.textInput}
            placeholder="Ask about onboarding, performance, benefits..."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            disabled={isThinking}
          />
          <button type="submit" style={{opacity: isThinking ? 0.5 : 1}} disabled={isThinking}>
            Send
          </button>
        </div>
      </form>
    </div>
  );
};

export default function App() {
  const [activePage, setActivePage] = useState('HR Chatbot');

  const navItems = [
    { name: 'Home', icon: <Home size={20} /> },
    { name: 'HR Chatbot', icon: <MessageCircle size={20} /> },
  ];

  return (
    <div style={styles.app}>
      <style>{`
        * {
          box-sizing: border-box;
          margin: 0;
          padding: 0;
        }
        body {
          overflow: hidden;
        }
        /* Custom scrollbar for webkit browsers */
        ::-webkit-scrollbar {
          width: 8px;
        }
        ::-webkit-scrollbar-track {
          background: ${brandColors.secondary};
        }
        ::-webkit-scrollbar-thumb {
          background: #444;
          border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
          background: #555;
        }
      `}</style>
      <div style={styles.sidebar}>
        <div style={styles.logo}>NETFLIX</div>
        <nav style={styles.nav}>
          {navItems.map(item => (
            <div
              key={item.name}
              style={{
                ...(activePage === item.name ? styles.navItemActive : styles.navItemInactive)
              }}
              onMouseEnter={(e) => {
                if (activePage !== item.name) {
                  e.currentTarget.style.backgroundColor = brandColors.bubbleUser;
                }
              }}
              onMouseLeave={(e) => {
                if (activePage !== item.name) {
                  e.currentTarget.style.backgroundColor = 'transparent';
                }
              }}
              onClick={() => setActivePage(item.name)}
            >
              <span style={styles.navIcon}>{item.icon}</span>
              {item.name}
            </div>
          ))}
        </nav>
      </div>
      {activePage === 'HR Chatbot' ? <HRChatbot /> : 
        <div style={{flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
          <h1>Welcome to the Netflix HR Portal</h1>
        </div>
      }
    </div>
  );
}