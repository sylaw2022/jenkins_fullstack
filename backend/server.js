const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', message: 'Backend API is running', timestamp: new Date().toISOString() });
});

app.get('/api/message', (req, res) => {
  res.json({ 
    message: 'Hello from the backend API!',
    environment: process.env.NODE_ENV || 'development'
  });
});

app.post('/api/data', (req, res) => {
  const { name, message } = req.body;
  res.json({ 
    success: true,
    received: {
      name: name || 'Anonymous',
      message: message || 'No message provided',
      timestamp: new Date().toISOString()
    }
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

