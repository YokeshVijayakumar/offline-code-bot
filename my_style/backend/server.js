require('dotenv').config(); // Load environment variables from .env
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors'); // For cross-origin requests
const productRoutes = require('./routes/products');
// const userRoutes = require('./routes/users'); // Example for future user routes

const app = express();
const PORT = process.env.PORT || 3000;
const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017/mystyle_db';

// Connect to MongoDB
mongoose.connect(MONGO_URI)
  .then(() => console.log('MongoDB connected successfully'))
  .catch(err => console.error('MongoDB connection error:', err));

// Middleware
app.use(express.json()); // Body parser for JSON
app.use(cors()); // Enable CORS for all origins (adjust for production)

// Routes
app.get('/', (req, res) => {
  res.send('API is running...');
});
app.use('/api/products', productRoutes);
// app.use('/api/users', userRoutes); // Example for future user routes

// Error handling middleware (optional, for more robust error handling)
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('Something broke!');
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});