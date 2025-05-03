import React, { useState } from 'react';
import axios from 'axios';
import '../styles/chatbot.css';

function Chatbot() {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Bonjour ! Comment puis-je vous aider ?' }
  ]);
  const [input, setInput] = useState('');

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);

    try {
      const response = await axios.post('http://localhost:5000/predict', {
        message: input
      });

      console.log('Réponse du serveur:', response.data); // Pour debug

      const botMessage = {
        sender: 'bot',
        text: response.data.response // ← Utilise "response", pas "answer"
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Erreur lors de la requête:', error);
      setMessages(prev => [...prev, {
        sender: 'bot',
        text: "Erreur de communication avec le serveur."
      }]);
    }

    setInput('');
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') sendMessage();
  };

  return (
    <div className="chat-container">
      <div className="chat-box">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            {msg.text}
          </div>
        ))}
      </div>
      <div className="input-container">
        <input
          type="text"
          placeholder="Écrivez un message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
        />
        <button onClick={sendMessage}>Envoyer</button>
      </div>
    </div>
  );
}

export default Chatbot;
