import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Target, Search, Mail, Send, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import './index.css';

function App() {
  const [formData, setFormData] = useState({ company: '', icp: '', email: '' });
  const [loading, setLoading] = useState(false);
  const [logs, setLogs] = useState([]);
  const [finalOutput, setFinalOutput] = useState('');
  const terminalEndRef = useRef(null);

  const scrollToBottom = () => {
    terminalEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [logs]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const addLog = (msg, type = 'info') => {
    setLogs(prev => [...prev, { text: msg, type }]);
  };

  const runAgent = async (e) => {
    e.preventDefault();
    if (!formData.company || !formData.icp || !formData.email) return;

    setLoading(true);
    setLogs([]);
    setFinalOutput('');
    addLog(`Initializing FireReach agent for target: ${formData.company}...`, 'info');

    try {
      const response = await fetch('/run-agent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      const data = await response.json();
      
      if (data.status === 'success') {
        data.log.forEach((logStr, i) => {
          setTimeout(() => {
            let type = 'info';
            if (logStr.includes('finished')) type = 'success';
            if (logStr.includes('Error')) type = 'error';
            addLog(`[${new Date().toLocaleTimeString()}] ${logStr}`, type);
          }, i * 800);
        });

        setTimeout(() => {
           // Show email status
           if (data.tool_results?.email_result) {
             const emailRes = data.tool_results.email_result;
             if (emailRes.status === 'sent') {
               addLog(`✅ Email successfully sent!`, 'success');
             } else {
               addLog(`⚠️ Email status: ${emailRes.status} — ${emailRes.error_message || 'Check spam folder'}`, 'error');
             }
           }
           setFinalOutput(data.final_response);
           setLoading(false);
        }, data.log.length * 800 + 500);
      } else {
        addLog(`Error: ${data.final_response || data.detail || 'Failed to execute agent'}`, 'error');
        setLoading(false);
      }
    } catch (err) {
      addLog(`Network error: ${err.message}`, 'error');
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="header"
      >
        <h1>FireReach</h1>
        <p>The Autonomous Outreach Engine</p>
      </motion.div>

      <div className="main-content">
        <motion.div 
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.1 }}
          className="glass-card"
        >
          <form onSubmit={runAgent}>
            <div className="form-group">
              <label>Target Company</label>
              <div style={{position: 'relative'}}>
                <Target size={18} style={{position: 'absolute', left: '12px', top: '14px', color: '#94a3b8'}} />
                <input 
                  type="text" 
                  name="company" 
                  value={formData.company} 
                  onChange={handleChange} 
                  placeholder="e.g. OpenAI" 
                  required 
                  style={{paddingLeft: '40px'}}
                />
              </div>
            </div>

            <div className="form-group">
              <label>Ideal Customer Profile (ICP)</label>
              <div style={{position: 'relative'}}>
                <Search size={18} style={{position: 'absolute', left: '12px', top: '14px', color: '#94a3b8'}} />
                <input 
                  type="text" 
                  name="icp" 
                  value={formData.icp} 
                  onChange={handleChange} 
                  placeholder="e.g. Series B startups..." 
                  required 
                  style={{paddingLeft: '40px'}}
                />
              </div>
            </div>

            <div className="form-group">
              <label>Sender Email</label>
              <div style={{position: 'relative'}}>
                <Mail size={18} style={{position: 'absolute', left: '12px', top: '14px', color: '#94a3b8'}} />
                <input 
                  type="email" 
                  name="email" 
                  value={formData.email} 
                  onChange={handleChange} 
                  placeholder="name@company.com" 
                  required 
                  style={{paddingLeft: '40px'}}
                />
              </div>
            </div>

            <button type="submit" disabled={loading} className="btn-primary">
              {loading ? (
                <><Loader2 className="pulse" size={20} /> Deploying Agent...</>
              ) : (
                <><Send size={20} /> Execute Campaign</>
              )}
            </button>
          </form>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
          className="glass-card"
          style={{ display: 'flex', flexDirection: 'column' }}
        >
          <h3 style={{marginTop: 0, marginBottom: '1rem', color: 'var(--text-muted)'}}>Agent Logs & Output</h3>
          
          <div className="terminal">
            {logs.length === 0 && !loading && (
               <div style={{color: '#4B5563', fontStyle: 'italic'}}>Awaiting instructions...</div>
            )}
            <AnimatePresence>
              {logs.map((log, index) => (
                <motion.div 
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  key={index}
                  className={`log-entry log-${log.type}`}
                >
                  <span style={{marginRight: '8px'}}>
                    {log.type === 'success' && <CheckCircle size={14} style={{display:'inline', verticalAlign:'middle'}} />}
                    {log.type === 'error' && <AlertCircle size={14} style={{display:'inline', verticalAlign:'middle'}} />}
                  </span>
                  {log.text}
                </motion.div>
              ))}
            </AnimatePresence>
            <div ref={terminalEndRef} />
          </div>

          <AnimatePresence>
            {finalOutput && (
              <motion.div 
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="final-output"
              >
                <h4 style={{marginTop: 0, color: 'var(--accent-primary)'}}>Mission Accomplished</h4>
                <p style={{whiteSpace: 'pre-wrap', fontSize: '0.95rem'}}>{finalOutput}</p>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      </div>
    </div>
  );
}

export default App;
