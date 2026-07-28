import React, { useState } from 'react';
import Dashboard from './components/Dashboard';
import CallLog from './components/CallLog';
import WhatsAppPanel from './components/WhatsAppPanel';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  return (
    <div className="app-container">
      <header className="glow-header">
        <h1>🌟 Kiyara AI</h1>
        <nav>
          <button onClick={() => setActiveTab('dashboard')}>Dashboard</button>
          <button onClick={() => setActiveTab('calls')}>Call Logs</button>
          <button onClick={() => setActiveTab('whatsapp')}>WhatsApp</button>
        </nav>
      </header>
      <main>
        {activeTab === 'dashboard' && <Dashboard apiUrl={API_URL} />}
        {activeTab === 'calls' && <CallLog apiUrl={API_URL} />}
        {activeTab === 'whatsapp' && <WhatsAppPanel apiUrl={API_URL} />}
      </main>
    </div>
  );
}
export default App;