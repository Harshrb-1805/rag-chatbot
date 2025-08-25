import React, { useState, useEffect, useRef } from 'react';
import { Send, Trash2, RotateCcw, Bot, User, FileText, Loader2 } from 'lucide-react';
import { chatAPI } from '../services/api.ts';

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  created_at: string;
  tokens_used?: number;
}

interface ChatResponse {
  message: string;
  chat_id: string;
  sources: string[];
  tokens_used: number;
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentChatId, setCurrentChatId] = useState<string | null>(null);
  const [sources, setSources] = useState<string[]>([]);
  const [totalTokens, setTotalTokens] = useState(0);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Focus input on mount
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    
    // Add user message to chat
    const userMsg: Message = {
      id: Date.now().toString(),
      content: userMessage,
      role: 'user',
      created_at: new Date().toISOString(),
    };
    
    setMessages(prev => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const response: ChatResponse = await chatAPI.sendMessage(userMessage, currentChatId || undefined);
      
      // Update chat ID if this is a new chat
      if (!currentChatId) {
        setCurrentChatId(response.chat_id);
      }
      
      // Add assistant message
      const assistantMsg: Message = {
        id: (Date.now() + 1).toString(),
        content: response.message,
        role: 'assistant',
        created_at: new Date().toISOString(),
        tokens_used: response.tokens_used,
      };
      
      setMessages(prev => [...prev, assistantMsg]);
      setSources(response.sources);
      setTotalTokens(prev => prev + response.tokens_used);
      
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Add error message
      const errorMsg: Message = {
        id: (Date.now() + 1).toString(),
        content: 'Sorry, I encountered an error. Please try again.',
        role: 'assistant',
        created_at: new Date().toISOString(),
      };
      
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const clearChat = () => {
    if (window.confirm('Are you sure you want to clear the chat history?')) {
      setMessages([]);
      setSources([]);
      setTotalTokens(0);
      setCurrentChatId(null);
    }
  };

  const formatTime = (dateString: string) => {
    return new Date(dateString).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="flex flex-col h-[calc(100vh-120px)] bg-white rounded-lg shadow-sm border border-gray-200">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200">
        <div>
          <h1 className="text-xl font-semibold text-gray-900">Chat with Documents</h1>
          <p className="text-sm text-gray-600">
            Ask questions about your uploaded documents
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={clearChat}
            className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            <RotateCcw className="h-4 w-4 mr-2" />
            Clear Chat
          </button>
        </div>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="text-center py-12">
            <Bot className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">No messages yet</h3>
            <p className="mt-1 text-sm text-gray-500">
              Start a conversation by asking a question about your documents.
            </p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`flex max-w-xs lg:max-w-md xl:max-w-lg ${
                  message.role === 'user' ? 'flex-row-reverse' : 'flex-row'
                }`}
              >
                <div
                  className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                    message.role === 'user'
                      ? 'bg-primary-600 text-white'
                      : 'bg-gray-200 text-gray-600'
                  }`}
                >
                  {message.role === 'user' ? (
                    <User className="h-4 w-4" />
                  ) : (
                    <Bot className="h-4 w-4" />
                  )}
                </div>
                
                <div
                  className={`mx-2 px-4 py-2 rounded-lg ${
                    message.role === 'user'
                      ? 'bg-primary-600 text-white'
                      : 'bg-gray-100 text-gray-900'
                  }`}
                >
                  <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                  <div className={`mt-1 text-xs ${
                    message.role === 'user' ? 'text-primary-200' : 'text-gray-500'
                  }`}>
                    {formatTime(message.created_at)}
                    {message.tokens_used && (
                      <span className="ml-2">• {message.tokens_used} tokens</span>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
        
        {isLoading && (
          <div className="flex justify-start">
            <div className="flex max-w-xs lg:max-w-md xl:max-w-lg">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-200 text-gray-600 flex items-center justify-center">
                <Bot className="h-4 w-4" />
              </div>
              <div className="mx-2 px-4 py-2 rounded-lg bg-gray-100">
                <div className="flex items-center space-x-2">
                  <Loader2 className="h-4 w-4 animate-spin text-gray-500" />
                  <span className="text-sm text-gray-600">Thinking...</span>
                </div>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Sources (if available) */}
      {sources.length > 0 && (
        <div className="border-t border-gray-200 p-4 bg-gray-50">
          <h3 className="text-sm font-medium text-gray-900 mb-2">Sources:</h3>
          <div className="space-y-1">
            {sources.map((source, index) => (
              <div key={index} className="flex items-center text-sm text-gray-600">
                <FileText className="h-3 w-3 mr-2 text-gray-400" />
                {source}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="border-t border-gray-200 p-4">
        <div className="flex space-x-4">
          <div className="flex-1">
            <textarea
              ref={inputRef}
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask a question about your documents..."
              rows={1}
              className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 resize-none"
              disabled={isLoading}
            />
          </div>
          <button
            onClick={handleSendMessage}
            disabled={!inputMessage.trim() || isLoading}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="h-4 w-4" />
          </button>
        </div>
        
        {/* Chat Info */}
        <div className="mt-2 flex items-center justify-between text-xs text-gray-500">
          <span>
            {messages.length > 0 && `Chat ID: ${currentChatId}`}
          </span>
          <span>
            {totalTokens > 0 && `Total tokens: ${totalTokens}`}
          </span>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
