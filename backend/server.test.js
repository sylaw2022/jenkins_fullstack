const request = require('supertest');
const express = require('express');
const cors = require('cors');

// Create test app (same setup as server.js)
const app = express();
app.use(cors());
app.use(express.json());

// Routes (same as server.js)
app.get('/api/health', (req, res) => {
    res.json({ 
        status: 'ok', 
        message: 'Backend API is running', 
        timestamp: new Date().toISOString() 
    });
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

describe('Backend API Tests', () => {
    describe('GET /api/health', () => {
        test('should return health status', async () => {
            const response = await request(app)
                .get('/api/health')
                .expect(200);
            
            expect(response.body).toHaveProperty('status');
            expect(response.body.status).toBe('ok');
            expect(response.body).toHaveProperty('message');
            expect(response.body).toHaveProperty('timestamp');
        });
    });

    describe('GET /api/message', () => {
        test('should return message', async () => {
            const response = await request(app)
                .get('/api/message')
                .expect(200);
            
            expect(response.body).toHaveProperty('message');
            expect(response.body).toHaveProperty('environment');
            expect(response.body.message).toBe('Hello from the backend API!');
        });
    });

    describe('POST /api/data', () => {
        test('should accept and return data', async () => {
            const testData = {
                name: 'Test User',
                message: 'Test message'
            };
            
            const response = await request(app)
                .post('/api/data')
                .send(testData)
                .expect(200);
            
            expect(response.body).toHaveProperty('success');
            expect(response.body.success).toBe(true);
            expect(response.body).toHaveProperty('received');
            expect(response.body.received.name).toBe(testData.name);
            expect(response.body.received.message).toBe(testData.message);
            expect(response.body.received).toHaveProperty('timestamp');
        });

        test('should handle missing data with defaults', async () => {
            const response = await request(app)
                .post('/api/data')
                .send({})
                .expect(200);
            
            expect(response.body.success).toBe(true);
            expect(response.body.received.name).toBe('Anonymous');
            expect(response.body.received.message).toBe('No message provided');
        });
    });
});

