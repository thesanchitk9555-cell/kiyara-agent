import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Dashboard({ apiUrl }) {
  const [phone, setPhone] = useState('');
  const [message, setMessage] = useState('');
  const [stats, setStats] = useState({ calls: 0, messages: 0 });
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const wsUrl = apiUrl.replace('http', 'ws').replace('https', 'wss');
    const ws = new WebSocket(`${wsUrl}/ws`);
    ws.onmessage = (e) => {
      try {
        const data = JSON.parse(e.data);
        setLogs(prev => [...prev, data]);
      } catch (err) {
        console.log('WebSocket message:', e.data);
      }
    };
    return () => ws.close();
  }, [apiUrl]);

  const makeCall = async () => {
    try {
      await axios.post(`${apiUrl}/calls/outgoing`, { to_number: phone });
      alert('📞 Call initiated');
    } catch (err) {
      alert('❌ Call failed: ' + err.message);
    }
  };

  const sendWhatsApp = async () => {
    try {
      await axios.post(`${apiUrl}/whatsapp/send`, { to: phone, body: message });
      alert('💬 WhatsApp sent');
    } catch (err) {
      alert('❌ WhatsApp failed: ' + err.message);
    }
  };

  return (
    <div className="dashboard">
      <div className="stats">
        <div className="stat-card">📞 Total Calls: {stats.calls}</div>
        <div className="stat-card">💬 Messages: {stats.messages}</div>
      </div>
      <div className="actions">
        <input value={phone} onChange={e => setPhone(e.target.value)} placeholder="+91 98765 43210" />
        <input value={message} onChange={e => setMessage(e.target.value)} placeholder="Type your message..." />
        <button onClick={makeCall}>📞 Call</button>
        <button onClick={sendWhatsApp}>💬 WhatsApp</button>
      </div>
      <div style={{ marginTop: 20 }}>
        <h3>🔄 Live Activity Feed</h3>
        <div style={{ maxHeight: 300, overflowY: 'auto', background: '#00000044', padding: 20, borderRadius: 20 }}>
          {logs.map((log, i) => (
            <div key={i} style={{ borderBottom: '1px solid #00ffff33', padding: 10 }}>
              <span style={{ color: '#00ffff' }}>[{log.type}]</span> {log.text}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
export default Dashboard;