import React from 'react';
import Chatbot from './components/Chatbot';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Assistant ISET</h1>
        <p>Votre assistant virtuel pour l'ISET</p>
      </header>
      <div className="chat-container">
        <Chatbot />
      </div>
    </div>
  );
}

export default App;
