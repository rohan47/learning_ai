import React, { useState, useRef, useEffect } from 'react';
import { Send, X } from 'lucide-react';
import { ChatService } from '../services';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'ai';
  timestamp: Date;
  agentType?: string;
  consultation?: {
    specialists_involved?: string[];
    individual_insights?: { [key: string]: string };
    consultation_summary?: string;
    consultation_quality?: string;
  };
}

interface AIChatProps {
  isOpen: boolean;
  onClose: () => void;
}

const AIChat: React.FC<AIChatProps> = ({ isOpen, onClose }) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: "Hi! I'm your ADHD Focus Assistant. I can help you with task management, focus sessions, mood tracking, and productivity strategies. What would you like to work on today?",
      sender: 'ai',
      timestamp: new Date(),
      agentType: 'Focus Assistant'
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [comprehensiveMode, setComprehensiveMode] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (useFresh = false) => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      let chatMethod;
      if (useFresh) {
        chatMethod = ChatService.sendFreshMessage;
      } else if (comprehensiveMode) {
        chatMethod = ChatService.sendComprehensiveMessage;
      } else {
        chatMethod = ChatService.sendMessage;
      }

      const response = await chatMethod({
        message: inputMessage,
        context: {
          current_energy: 7,
          current_mood: 'focused',
          active_tasks: [],
          session_context: {
            previousMessages: messages.slice(-5).map(m => ({
              role: m.sender === 'user' ? 'user' : 'assistant',
              content: m.text
            }))
          }
        }
      });

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: response.response,
        sender: 'ai',
        timestamp: new Date(),
        agentType: response.agent_used || 'AI Assistant',
        consultation: comprehensiveMode ? {
          specialists_involved: response.specialists_involved,
          individual_insights: response.individual_insights,
          consultation_summary: response.consultation_summary,
          consultation_quality: response.consultation_quality
        } : undefined
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: "I'm sorry, I'm having trouble connecting right now. Please check if the backend server is running and try again.",
        sender: 'ai',
        timestamp: new Date(),
        agentType: 'System'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([{
      id: '1',
      text: "Hi! I'm your ADHD Focus Assistant. I can help you with task management, focus sessions, mood tracking, and productivity strategies. What would you like to work on today?",
      sender: 'ai',
      timestamp: new Date(),
      agentType: 'Focus Assistant'
    }]);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="w-full max-w-2xl h-[80vh] bg-white rounded-lg shadow-xl flex flex-col">
        {/* Header */}
        <div className="p-4 border-b border-gray-200 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-t-lg">
          <div className="flex justify-between items-center mb-2">
            <div>
              <h2 className="text-xl font-semibold text-gray-800">AI Chat Assistant</h2>
              <p className="text-sm text-gray-600">Powered by CrewAI with specialized ADHD agents</p>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={clearChat}
                className="px-3 py-1 text-sm bg-yellow-100 text-yellow-700 rounded hover:bg-yellow-200 transition-colors"
              >
                Clear
              </button>
              <button
                onClick={onClose}
                className="p-2 hover:bg-white hover:bg-opacity-50 rounded-lg transition-colors"
              >
                <X size={20} className="text-gray-600" />
              </button>
            </div>
          </div>
          
          {/* Comprehensive Mode Toggle */}
          <div className="flex items-center gap-2 text-sm">
            <label className="flex items-center gap-1 cursor-pointer">
              <input
                type="checkbox"
                checked={comprehensiveMode}
                onChange={(e) => setComprehensiveMode(e.target.checked)}
                className="rounded"
              />
              <span className="text-gray-700">
                {comprehensiveMode ? '🧠 Multi-Agent Consultation' : '🤖 Single Agent Response'}
              </span>
            </label>
            <span className="text-gray-500">
              {comprehensiveMode ? '(Consults all specialists)' : '(Routes to best specialist)'}
            </span>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`${
                  message.sender === 'user' 
                    ? 'max-w-xs lg:max-w-md' 
                    : message.consultation ? 'max-w-md lg:max-w-lg' : 'max-w-xs lg:max-w-md'
                } px-4 py-2 rounded-lg ${
                  message.sender === 'user'
                    ? 'bg-blue-500 text-white rounded-br-none'
                    : 'bg-gray-100 text-gray-800 rounded-bl-none'
                }`}
              >
                {message.sender === 'ai' && message.agentType && (
                  <div className="text-xs font-medium text-blue-600 mb-1">
                    {message.agentType}
                  </div>
                )}
                
                {/* Consultation details for comprehensive responses */}
                {message.sender === 'ai' && message.consultation && (
                  <div className="mb-3 p-2 bg-blue-50 rounded border-l-4 border-blue-300">
                    <div className="text-xs font-semibold text-blue-800 mb-1">
                      📋 Consultation Process
                    </div>
                    
                    {/* Specialists involved */}
                    {message.consultation.specialists_involved && message.consultation.specialists_involved.length > 0 && (
                      <div className="text-xs text-blue-700 mb-2">
                        <span className="font-medium">Specialists consulted:</span> {message.consultation.specialists_involved.join(', ')}
                      </div>
                    )}
                    
                    {/* Individual insights preview */}
                    {message.consultation.individual_insights && Object.keys(message.consultation.individual_insights).length > 0 && (
                      <div className="text-xs text-blue-700 mb-2">
                        <div className="font-medium mb-1">Specialist insights:</div>
                        {Object.entries(message.consultation.individual_insights).map(([specialist, insight]) => (
                          <div key={specialist} className="ml-2 mb-1">
                            <span className="font-medium">{specialist}:</span> {insight.length > 80 ? `${insight.substring(0, 80)}...` : insight}
                          </div>
                        ))}
                      </div>
                    )}
                    
                    {/* Consultation quality */}
                    {message.consultation.consultation_quality && (
                      <div className="text-xs text-blue-600">
                        <span className="font-medium">Quality:</span> {message.consultation.consultation_quality}
                      </div>
                    )}
                  </div>
                )}
                
                <div className="whitespace-pre-wrap break-words">{message.text}</div>
                <div
                  className={`text-xs mt-1 ${
                    message.sender === 'user' ? 'text-blue-100' : 'text-gray-500'
                  }`}
                >
                  {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="flex justify-start">
              <div className="max-w-xs lg:max-w-md px-4 py-2 rounded-lg bg-gray-100 text-gray-800 rounded-bl-none">
                <div className="flex items-center space-x-2">
                  <div className="animate-pulse flex space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                  <span className="text-sm text-gray-600">AI is thinking...</span>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="p-4 border-t border-gray-200 bg-gray-50 rounded-b-lg">
          <div className="flex space-x-2">
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask about focus techniques, task management, mood tracking..."
              className="flex-1 resize-none border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              rows={1}
              disabled={isLoading}
            />
            <button
              onClick={() => handleSendMessage()}
              disabled={!inputMessage.trim() || isLoading}
              className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Send size={20} />
            </button>
            <button
              onClick={() => handleSendMessage(true)}
              disabled={!inputMessage.trim() || isLoading}
              className="px-3 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm"
              title="Send fresh message (bypasses cache)"
            >
              Fresh
            </button>
          </div>
          <div className="mt-2 text-xs text-gray-500">
            Press Enter to send • Shift+Enter for new line • Fresh bypasses response cache
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIChat;
