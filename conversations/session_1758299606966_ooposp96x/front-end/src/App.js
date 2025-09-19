import React, { useState, useEffect, useRef } from 'react';
import { Home, Coffee, BrainCircuit, ChevronDown, Send, BookOpen, ClipboardCheck, UserCheck } from 'lucide-react';

const brandColors = {
  primary: '#007bff', // Using a generic blue as Starbucks green is a trademark
  secondary: '#6c757d',
  accent: '#28a745',
  background: '#f8f9fa',
  text: '#212529',
  light: '#ffffff',
  border: '#dee2e6',
  userBubble: '#007bff',
  aiBubble: '#ffffff',
  reasoningPanel: '#f1f3f5',
};

const styles = {
  appContainer: {
        display: 'flex',
    height: '100vh',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    backgroundColor: brandColors.background,
    color: brandColors.text},
  sidebar: {
        width: '240px',
    backgroundColor: brandColors.light,
    borderRight: `1px solid ${brandColors.border}`,
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
    color: brandColors.secondary,
    transition: 'background-color 0.2s, color 0.2s'},
  navItemActive: {
        backgroundColor: brandColors.primary,
    color: brandColors.light},
  navIcon: {
    marginRight: '12px'},
  mainContent: {
        flex: 1,
    display: 'flex',
    flexDirection: 'column',
    height: '100vh',
    overflow: 'hidden'},
  chatContainer: {
        flex: 1,
    display: 'flex',
    flexDirection: 'column',
    padding: '20px',
    overflowY: 'auto'},
  messageList: {
        flex: 1,
    display: 'flex',
    flexDirection: 'column',
    gap: '20px',
    paddingRight: '10px'},
  inputArea: {
        padding: '20px',
    borderTop: `1px solid ${brandColors.border}`,
    backgroundColor: brandColors.light},
  inputForm: {
        display: 'flex',
    alignItems: 'center',
    backgroundColor: brandColors.background,
    borderRadius: '12px',
    padding: '5px',
    border: `1px solid ${brandColors.border}`},
  textInput: {
        flex: 1,
    border: 'none',
    outline: 'none',
    padding: '12px 15px',
    fontSize: '16px',
    backgroundColor: 'transparent'},
  sendButton: {
        backgroundColor: brandColors.primary,
    color: brandColors.light,
    border: 'none',
    borderRadius: '8px',
    padding: '10px',
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    margin: '5px',
    transition: 'background-color 0.2s'},
  messageBubble: {
        maxWidth: '75%',
    padding: '15px 20px',
    borderRadius: '20px',
    wordWrap: 'break-word',
    boxShadow: '0 4px 6px rgba(0,0,0,0.05)'},
  userMessage: {
        alignSelf: 'flex-end',
    backgroundColor: brandColors.userBubble,
    color: brandColors.light,
    borderBottomRightRadius: '5px'},
  aiMessageContainer: {
        alignSelf: 'flex-start',
    width: '75%'},
  aiMessage: {
        backgroundColor: brandColors.aiBubble,
    color: brandColors.text,
    borderBottomLeftRadius: '5px'},
  agentAttribution: {
        display: 'flex',
    alignItems: 'center',
    fontSize: '12px',
    color: brandColors.secondary,
    marginBottom: '8px',
    paddingLeft: '10px'},
  agentIcon: {
        marginRight: '8px',
    padding: '4px',
    borderRadius: '50%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'},
  reasoningToggle: {
        display: 'flex',
    alignItems: 'center',
    cursor: 'pointer',
    marginTop: '15px',
    padding: '8px 12px',
    borderRadius: '8px',
    backgroundColor: brandColors.reasoningPanel,
    color: brandColors.secondary,
    fontSize: '13px',
    fontWeight: '500',
    transition: 'background-color 0.2s'},
  reasoningPanel: {
        backgroundColor: brandColors.reasoningPanel,
    borderRadius: '8px',
    marginTop: '10px',
    padding: '15px',
    overflow: 'hidden',
    transition: 'max-height 0.4s ease-in-out, padding 0.4s ease-in-out'},
  reasoningStep: {
        marginBottom: '10px',
    fontSize: '13px'},
  reasoningTitle: {
        fontWeight: 'bold',
    color: brandColors.text},
  typingIndicator: {
        display: 'flex',
    alignItems: 'center',
    padding: '10px 20px'},
  typingDot: {
        height: '8px',
    width: '8px',
    backgroundColor: brandColors.secondary,
    borderRadius: '50%',
    margin: '0 3px',
    animation: 'typing-bounce 1.4s infinite ease-in-out both'},
};

const agents = {
  RECIPE_GURU: {
        name: "Recipe Guru",
    icon: Coffee,
    color: '#d69f7e',
    specialty: "Drink recipes and preparation steps."},
  PROCEDURE_PRO: {
        name: "Procedure Pro",
    icon: ClipboardCheck,
    color: '#60a5fa',
    specialty: "Store operations and checklists."},
  POLICY_PAL: {
        name: "Policy Pal",
    icon: UserCheck,
    color: '#34d399',
    specialty: "Company policies and HR questions."},
  GENERAL_ASSISTANT: {
        name: "General Assistant",
    icon: BrainCircuit,
    color: '#9ca3af',
    specialty: "General inquiries and routing."},
};

const getAgentForQuery = (query) => {
  const q = query.toLowerCase();
  if (q.includes('recipe') || q.includes('make') || q.includes('latte') || q.includes('frappuccino') || q.includes('cappuccino')) {
    return agents.RECIPE_GURU;
  }
  if (q.includes('opening') || q.includes('closing') || q.includes('checklist') || q.includes('procedure') || q.includes('clean')) {
    return agents.PROCEDURE_PRO;
  }
  if (q.includes('policy') || q.includes('dress code') || q.includes('sick') || q.includes('time off')) {
    return agents.POLICY_PAL;
  }
  return agents.GENERAL_ASSISTANT;
};

const getAIResponse = (query, agent) => {
  const q = query.toLowerCase();
  const reasoning = {
    analysis: `User query detected: "${query}". The query seems to be about ${agent.specialty.toLowerCase()}`,
    selection: `Routing to ${agent.name} due to keywords related to its specialty.`,
    knowledge: `Consulting internal knowledge base for ${agent.specialty.toLowerCase()}`,
  };

  let responseText = "";

  switch (agent) {
    case agents.RECIPE_GURU:
      if (q.includes('caramel macchiato')) {
        responseText = "To make a grande Iced Caramel Macchiato: \n1. Pump 3 pumps of vanilla syrup into the cup. \n2. Add milk to the third black line. \n3. Add ice, leaving about 1/2 inch of room. \n4. Queue 2 shots of espresso. \n5. Pour shots over the top of the ice. \n6. Finish with caramel drizzle in a crosshatch pattern.";
      } else {
        responseText = "I can help with that! Which specific drink recipe are you looking for?";
      }
      break;
    case agents.PROCEDURE_PRO:
      if (q.includes('closing')) {
        responseText = "The standard closing procedure involves: \n1. Cleaning the espresso machines. \n2. Wiping down all counters and condiment bars. \n3. Sweeping and mopping all floors. \n4. Taking out the trash and recycling. \n5. Counting the cash drawer. \nAlways refer to the Daily Records Book for the full checklist.";
      } else {
        responseText = "I can guide you through store procedures. What specific task do you need help with?";
      }
      break;
    case agents.POLICY_PAL:
      if (q.includes('dress code')) {
        responseText = "The 'Look Book' outlines the dress code. Key points include: \n- Solid-colored shirts (black, gray, navy, white). \n- Black, gray, navy, brown, or khaki pants, shorts, or skirts. \n- No jeans with rips or tears. \n- Non-slip shoes are required for safety. \n- An apron must always be worn on the floor.";
      } else {
        responseText = "I can answer questions about company policies. What do you need to know?";
      }
      break;
    default:
      responseText = "Hello! I'm your Barista Buddy. How can I assist you today with recipes, procedures, or policies?";
  }
  
  reasoning.generation = `Formulating a clear, step-by-step response based on the retrieved information.`;
  return { text: responseText, reasoning };
};


const App = () => {
  const [activePage, setActivePage] = useState('AI Assistant');

  const Sidebar = () => (
    <div style={styles.sidebar}>
      <div style={styles.logo}>
        <Coffee size={28} style={{ marginRight: '10px' }} />
        Default
      </div>
      <nav style={styles.nav}>
        <a 
          href="#" 
          style={{...(activePage === 'Home' ? styles.navItemActive : {})}}
          onClick={() => setActivePage('Home')}
        >
          <Home size={20} style={styles.navIcon} /> Home
        </a>
        <a 
          href="#" 
          style={{...(activePage === 'AI Assistant' ? styles.navItemActive : {})}}
          onClick={() => setActivePage('AI Assistant')}
        >
          <BrainCircuit size={20} style={styles.navIcon} /> AI Assistant
        </a>
      </nav>
    </div>
  );

  const ChatMessage = ({ message }) => {
    const [isReasoningOpen, setIsReasoningOpen] = useState(false);
    const AgentIcon = message.agent?.icon || (() => null);

    if (message.type === 'user') {
      return (
        <div style={{ animation: 'fadeIn 0.5s' }}>
          {message.text}
        </div>
      );
    }
    
    if (message.type === 'thinking') {
      return (
          <div style={{ alignSelf: 'flex-start' }}>
              <span style={{animationDelay: '0s'}}></span>
              <span style={{animationDelay: '0.2s'}}></span>
              <span style={{animationDelay: '0.4s'}}></span>
          </div>
      );
    }

    return (
      <div style={{animation: 'fadeIn 0.5s'}}>
        <div style={styles.agentAttribution}>
          <div style={{backgroundColor: `${message.agent.color}20`, color: message.agent.color}}>
            <AgentIcon size={16} />
          </div>
          <strong>{message.agent.name}</strong>
        </div>
        <div style={{ }}>
          <div style={{ whiteSpace: 'pre-wrap' }}>{message.text}</div>
          {message.reasoning && (
            <>
              <div 
                style={styles.reasoningToggle} 
                onClick={() => setIsReasoningOpen(!isReasoningOpen)}
              >
                <BookOpen size={16} style={{ marginRight: '8px' }} />
                Show Reasoning
                <ChevronDown size={16} style={{ marginLeft: 'auto', transform: isReasoningOpen ? 'rotate(180deg)' : 'rotate(0deg)', transition: 'transform 0.3s' }}/>
              </div>
              <div style={{maxHeight: isReasoningOpen ? '500px' : '0px', padding: isReasoningOpen ? '15px' : '0 15px'}}>
                <div style={styles.reasoningStep}><span style={styles.reasoningTitle}>1. Analysis:</span> {message.reasoning.analysis}</div>
                <div style={styles.reasoningStep}><span style={styles.reasoningTitle}>2. Agent Selection:</span> {message.reasoning.selection}</div>
                <div style={styles.reasoningStep}><span style={styles.reasoningTitle}>3. Knowledge Base:</span> {message.reasoning.knowledge}</div>
                <div style={styles.reasoningStep}><span style={styles.reasoningTitle}>4. Generation:</span> {message.reasoning.generation}</div>
              </div>
            </>
          )}
        </div>
      </div>
    );
  };
  
  const ChatInterface = () => {
    const [messages, setMessages] = useState([
      {
        id: 1,
        type: 'ai',
        text: "Welcome to Barista Buddy! I'm here to help with drink recipes, store procedures, and company policies. How can I assist you?",
        agent: agents.GENERAL_ASSISTANT,
        reasoning: {
        analysis: "Initial greeting triggered.",
          selection: "Defaulting to General Assistant for initial contact.",
          knowledge: "Loaded standard greeting protocols.",
          generation: "Composed a welcoming and informative initial message."
        }
      }
    ]);
    const [inputValue, setInputValue] = useState('');
    const [isThinking, setIsThinking] = useState(false);
    const messagesEndRef = useRef(null);
  
    const scrollToBottom = () => {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };
  
    useEffect(scrollToBottom, [messages]);
  
    const handleSendMessage = (e) => {
      e.preventDefault();
      if (inputValue.trim() === '' || isThinking) return;
  
      const userMessage = {
        id: Date.now(),
        type: 'user',
        text: inputValue,
      };
      setMessages(prev => [...prev, userMessage]);
      setInputValue('');
      setIsThinking(true);
  
      setTimeout(() => {
        const agent = getAgentForQuery(inputValue);
        const aiResponse = getAIResponse(inputValue, agent);
        const newAiMessage = {
          id: Date.now() + 1,
          type: 'ai',
          ...aiResponse,
          agent,
        };
        setIsThinking(false);
        setMessages(prev => [...prev, newAiMessage]);
      }, 2500);
    };
  
    return (
      <div style={styles.mainContent}>
        <style>
          {`
            @keyframes fadeIn {
              from { opacity: 0; transform: translateY(10px); }
              to { opacity: 1; transform: translateY(0); }
            }
            @keyframes typing-bounce {
              0%, 80%, 100% { transform: scale(0); }
              40% { transform: scale(1.0); }
            }
            .chat-container::-webkit-scrollbar { width: 8px; }
            .chat-container::-webkit-scrollbar-track { background: ${brandColors.background}; }
            .chat-container::-webkit-scrollbar-thumb { background: ${brandColors.border}; border-radius: 4px; }
            .chat-container::-webkit-scrollbar-thumb:hover { background: ${brandColors.secondary}; }
          `}
        </style>
        <div style={styles.chatContainer} className="chat-container">
          <div style={styles.messageList}>
            {messages.map(msg => <ChatMessage key={msg.id} message={msg} />)}
            {isThinking && <ChatMessage message={{type: 'thinking'}} />}
            <div ref={messagesEndRef} />
          </div>
        </div>
        <div style={styles.inputArea}>
          <form style={styles.inputForm} onSubmit={handleSendMessage}>
            <input
              type="text"
              style={styles.textInput}
              placeholder="Ask about a recipe, procedure, or policy..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              disabled={isThinking}
            />
            <button type="submit" style={{opacity: isThinking ? 0.5 : 1}} disabled={isThinking}>
              <Send size={20} />
            </button>
          </form>
        </div>
      </div>
    );
  };
  
  return (
    <div style={styles.appContainer}>
      <Sidebar />
      <ChatInterface />
    </div>
  );
};

export default App;