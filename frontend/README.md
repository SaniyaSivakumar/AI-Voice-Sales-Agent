# AI Voice Sales Agent - Frontend Web Application

A modern, responsive web application for the **AI Voice Sales Agent**, built with HTML5, CSS3 (Vanilla Glassmorphism design system), and JavaScript ES Modules (Vite).

---

## ✨ Features

1. **AI Voice Assistant Section**:
   - Interactive microphone button with animated pulse rings and status indicators.
   - Start / Stop listening controls via Web Speech API (`webkitSpeechRecognition`).
   - Live real-time speech transcript box.
   - Text input fallback for typing commands directly.
   - AI Agent speech response card with audio wave visualizer and SpeechSynthesis voice output.
   - Dynamic conversation history feed.

2. **Product Catalog & Recommendations**:
   - Product search bar matching product names, categories, and feature descriptions.
   - Category filter chips (Laptops, Audio, Wearables, Smartphones, Tablets, Cameras, Accessories, Footwear, Bags).
   - In-Stock filter toggle.
   - Responsive product cards displaying:
     - Product Name & Category badge
     - Original price & Discounted price tag
     - Availability pill (`In Stock`, `Low Stock`, `Out of Stock`)
     - Features list & product description
     - Quick "Ask Agent" & "Details Modal" buttons.
   - Handpicked "Recommended Products" carousel.

3. **Backend Integration**:
   - Connects live to FastAPI backend at `http://localhost:8000`.
   - Real-time status pill (`🟢 Backend Online` / `🟡 Backend Offline - Local Fallback Mode`).
   - Prepared for future integration with Padma's Deep Learning intent model and Hafil's voice module.

---

## 🛠️ How to Run the Frontend

1. **Install Dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Start Development Server**:
   ```bash
   npm run dev
   ```
   The application will start at: [http://localhost:3000](http://localhost:3000)

3. **Build for Production**:
   ```bash
   npm run build
   ```

---

## 🔗 Connecting with Backend

Ensure the Python FastAPI backend server is running:
```bash
cd backend
python app.py
```
The frontend will automatically connect to `http://localhost:8000` and display `Backend Online (localhost:8000)` in the top navigation header.
