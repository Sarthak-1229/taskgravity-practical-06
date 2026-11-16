/**
 * Practical 06: RESTful API using Node.js and Express
 * Implements CRUD operations, database persistence, and Postman testing suite.
 */

require('dotenv').config();
const express = require('express');
const path = require('path');
const cors = require('cors');
const taskRoutes = require('./routes/taskRoutes');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve API documentation & dashboard UI
app.use(express.static(path.join(__dirname, 'public')));

// Request logging middleware
app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log(`[REST API] ${req.method} ${req.originalUrl} -> ${res.statusCode} (${duration}ms)`);
  });
  next();
});

// Health Check Endpoint
app.get('/api/health', (req, res) => {
  res.status(200).json({
    status: 'online',
    system: 'TaskGravity REST API',
    version: '1.0.0',
    timestamp: new Date().toISOString()
  });
});

// Mount Resource Routes
app.use('/api/tasks', taskRoutes);

// Fallback 404 Handler
app.use((req, res) => {
  res.status(404).json({
    success: false,
    message: `Resource endpoint '${req.method} ${req.originalUrl}' does not exist.`
  });
});

// Central Error Handler
app.use((err, req, res, next) => {
  console.error('[Unhandled API Error]', err);
  res.status(500).json({
    success: false,
    message: 'Internal server error occurred.',
    error: err.message
  });
});

if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`[TaskGravity REST API] Running on http://localhost:${PORT}`);
    console.log(`[Postman Suite] Ready for endpoint automated verification.`);
  });
}

module.exports = app;
