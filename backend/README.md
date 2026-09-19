# AI Voice Sales Agent - Backend & Product Database

This folder contains the backend server, SQLite product database, and REST API endpoints for the **AI Voice Sales Agent**.

---

## 🛠️ Tech Stack & Database Architecture

- **Backend Framework**: Python 3 + FastAPI
- **Database**: SQLite 3 (`products.db`)
- **Validation**: Pydantic v2
- **Server Runner**: Uvicorn

---

## 📦 Database Schema (`products.db`)

Each product entry includes:
- `id` (INTEGER, Primary Key)
- `name` (TEXT) — Product name
- `category` (TEXT) — Category (e.g., Laptops, Audio, Wearables, Smartphones)
- `price` (REAL) — Original price
- `description` (TEXT) — Detailed description
- `features` (TEXT/JSON) — Array of key product features
- `availability` (TEXT) — Status string (`In Stock`, `Low Stock`, `Out of Stock`)
- `stock_quantity` (INTEGER) — Total available units
- `discount_percentage` (REAL) — Discount percentage

---

## 🚀 API Endpoints

### 1. Product Search API
- **`GET /api/products/search`**
  - **Query Parameters**:
    - `q` (string): Keyword search (matches name, description, features)
    - `category` (string): Filter by product category
    - `min_price` / `max_price` (float): Filter price range
    - `in_stock_only` (boolean): Show only in-stock products
  - **Example**: `GET /api/products/search?q=laptop`

### 2. Product Details API
- **`GET /api/products/{product_id}`**
  - Fetch product details by ID.
  - **Example**: `GET /api/products/1`
- **`GET /api/products/details/by-name`**
  - Fetch product details by product name.
  - **Example**: `GET /api/products/details/by-name?name=SonicWave`

### 3. Product Availability API
- **`GET /api/products/{product_id}/availability`**
  - Returns stock status and quantity for a product ID.
  - **Example**: `GET /api/products/1/availability`
- **`GET /api/products/availability/search`**
  - Returns stock status and voice-ready message by searching product name.
  - **Example**: `GET /api/products/availability/search?name=SoundBox`

### 4. Integration Endpoint (For Padma's DL Model & Voice Module)
- **`POST /api/intent-query`**
  - Accepts classified intent & entity payload from the AI/Voice system and returns voice-ready response.
  - **Request Body**:
    ```json
    {
      "intent": "price_query",
      "query": "smartwatch"
    }
    ```
  - **Response**:
    ```json
    {
      "intent": "price_query",
      "spoken_response": "The price of FitPulse Smartwatch 4 is $149.50.",
      "products": [...]
    }
    ```

---

## 💻 How to Run the Backend Server

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the server**:
   ```bash
   python app.py
   ```
   Or with uvicorn directly:
   ```bash
   uvicorn app:app --reload --port 8000
   ```

3. **Interactive Swagger API Docs**:
   Open browser at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 Running Tests

Execute the automated test suite:
```bash
python test_backend.py
```
