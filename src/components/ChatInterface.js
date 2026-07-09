import React, { useState, useRef, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { addChatMessage, fetchInteractions } from '../store/interactionSlice';
import api from '../services/api';

function ChatInterface() {
  const dispatch = useDispatch();
  const { chatMessages } = useSelector(state => state.interactions);
  const [input, setInput] = useState('');
  const [mode, setMode] = useState('log');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatMessages]);

  const handleSend = async () => {
  if (!input.trim()) return;

  const userMessage = { role: 'user', content: input };
  dispatch(addChatMessage(userMessage));
  setInput('');

  try {
    const response = await api.sendChatMessage([...chatMessages, userMessage], mode);
    
    console.log('Chat response:', response.data);
    
    if (response.data.data) {
      const data = response.data.data;
      let formattedContent = '';
      
      if (response.data.message) {
        formattedContent += response.data.message + '\n\n';
      }
      
      if (typeof data === 'object') {
        formattedContent += JSON.stringify(data, null, 2);
      } else {
        formattedContent += data;
      }
      
      const botResponse = {
        role: 'assistant',
        content: formattedContent
      };
      dispatch(addChatMessage(botResponse));
      
      // Refresh interactions if new one created
      dispatch(fetchInteractions());
    }
  } catch (error) {
    console.error('Chat error:', error);
    dispatch(addChatMessage({
      role: 'assistant',
      content: 'Error: ' + (error.response?.data?.detail || error.message || 'Something went wrong')
    }));
  }
};

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h2>AI Chat Assistant</h2>
        <div className="mode-selector">
          <label>Mode:</label>
          <select value={mode} onChange={(e) => setMode(e.target.value)}>
            <option value="log">Log Interaction</option>
            <option value="edit">Edit Interaction</option>
            <option value="suggest">Suggest Follow-up</option>
            <option value="compliance">Compliance Check</option>
            <option value="summarize">Summarize</option>
          </select>
        </div>
      </div>

      <div className="chat-messages">
        {chatMessages.length === 0 && (
          <div className="chat-welcome">
            <p>👋 Hi! I'm your AI assistant for managing HCP interactions.</p>
            <p>Tell me about your interaction, and I'll help you log it.</p>
            <p className="examples">
              <strong>Examples:</strong><br/>
              • "Log interaction with Dr. Smith about Product X"<br/>
              • "I had a 30-minute call with Dr. Johnson discussing diabetes treatment"
            </p>
          </div>
        )}
        
        {chatMessages.map((msg, index) => (
          <div key={index} className={`chat-message ${msg.role}`}>
            <div className="message-content">
              {msg.role === 'assistant' ? (
                <pre>{msg.content}</pre>
              ) : (
                <p>{msg.content}</p>
              )}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Describe your interaction or ask me to perform an action..."
          rows="3"
        />
        <button onClick={handleSend} className="btn btn-primary">Send</button>
      </div>
    </div>
  );
}

export default ChatInterface;
