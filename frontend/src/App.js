import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function App() {
  const [health, setHealth] = useState(null);
  const [message, setMessage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({ name: '', message: '' });
  const [submitResult, setSubmitResult] = useState(null);

  useEffect(() => {
    // Check API health
    axios.get(`${API_URL}/api/health`)
      .then(response => setHealth(response.data))
      .catch(error => console.error('Health check failed:', error));

    // Get message from API
    axios.get(`${API_URL}/api/message`)
      .then(response => setMessage(response.data))
      .catch(error => console.error('Failed to fetch message:', error));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setSubmitResult(null);

    try {
      const response = await axios.post(`${API_URL}/api/data`, formData);
      setSubmitResult(response.data);
      setFormData({ name: '', message: '' });
    } catch (error) {
      setSubmitResult({ success: false, error: error.message });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="container">
        <header className="header">
          <h1>🚀 GROKLORD Fullstack Application</h1>
          <p>Deployed with Jenkins CI/CD & Render.com</p>
        </header>

        <div className="content">
          <section className="card">
            <h2>API Health Status</h2>
            {health ? (
              <div className="status success">
                <p>✅ {health.status}</p>
                <p className="small">{health.message}</p>
                <p className="small">Time: {new Date(health.timestamp).toLocaleString()}</p>
              </div>
            ) : (
              <div className="status loading">Checking...</div>
            )}
          </section>

          <section className="card">
            <h2>Backend Message</h2>
            {message ? (
              <div className="message">
                <p>{message.message}</p>
                <p className="small">Environment: {message.environment}</p>
              </div>
            ) : (
              <div className="status loading">Loading...</div>
            )}
          </section>

          <section className="card">
            <h2>Send Data to Backend</h2>
            <form onSubmit={handleSubmit} className="form">
              <div className="form-group">
                <label htmlFor="name">Name:</label>
                <input
                  type="text"
                  id="name"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  placeholder="Enter your name"
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="message">Message:</label>
                <textarea
                  id="message"
                  value={formData.message}
                  onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                  placeholder="Enter your message"
                  rows="4"
                  required
                />
              </div>
              <button type="submit" disabled={loading} className="submit-btn">
                {loading ? 'Sending...' : 'Submit'}
              </button>
            </form>

            {submitResult && (
              <div className={`result ${submitResult.success ? 'success' : 'error'}`}>
                {submitResult.success ? (
                  <div>
                    <p>✅ Success!</p>
                    <p className="small">Name: {submitResult.received.name}</p>
                    <p className="small">Message: {submitResult.received.message}</p>
                    <p className="small">Time: {new Date(submitResult.received.timestamp).toLocaleString()}</p>
                  </div>
                ) : (
                  <p>❌ Error: {submitResult.error}</p>
                )}
              </div>
            )}
          </section>
        </div>
      </div>
    </div>
  );
}

export default App;

