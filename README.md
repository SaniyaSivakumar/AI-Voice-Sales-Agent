# AI Voice Sales Agent

An intelligent voice-enabled sales assistant designed to interact with customers, process voice inputs, classify user intents, query product catalogs and pricing, and recommend products seamlessly.

---

## 📁 Project Structure

```text
AI-Voice-Sales-Agent/
│
├── ai-model/        # Intent classification & Natural Language Processing (NLP) models
├── voice-module/    # Speech-to-Text (STT) and Text-to-Speech (TTS) engine integrations
├── dataset/         # Intent datasets and training samples
│   └── intents.json # 8 core customer intents with sample sentences
├── frontend/        # User interface for interacting with the AI Voice Sales Agent
└── backend/         # Server logic, API endpoints, and database connections
```

---

## 👥 Team & Responsibilities

| Team Member | Module & Responsibilities |
| :--- | :--- |
| **padmaapriya** | **AI / Deep Learning**<br>• Intent classification model design and training<br>• NLP preprocessing and entity extraction<br>• Dataset collection and model evaluation |
| **hafil** | **Voice Module**<br>• Speech-to-Text (STT) audio transcription<br>• Text-to-Speech (TTS) voice generation<br>• Audio streaming & speech processing pipeline |
| **saniya** | **Frontend + Backend / Database**<br>• Web user interface development<br>• REST/WebSocket API endpoints<br>• Product database design & query handling |

---

## 🎯 Dataset & Initial Intents

The dataset is maintained under [`dataset/intents.json`](file:///c:/Users/saniya/Desktop/AI-Voice-Sales-Agent/dataset/intents.json) and includes the following 8 core sales intents with 10 customer example sentences each:

1. `greeting`: Initial customer welcomes & salutations.
2. `product_search`: Inquiries searching for specific items or categories.
3. `product_recommendation`: Requests for product suggestions or advice.
4. `price_query`: Questions asking about pricing or product costs.
5. `discount_query`: Inquiries regarding sales, coupons, and discounts.
6. `feature_query`: Queries about specifications, features, or compatibility.
7. `availability`: Stock checks and color/size availability inquiries.
8. `goodbye`: Closing greetings & concluding statements.
