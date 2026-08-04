# 🌸 Skincare AI E-Commerce, Voice & Vision Platform API

AI-powered Skincare E-Commerce Platform featuring **Multimodal Vision AI (Skin & Product Analysis)**, **Bengali Voice Assistance (Free Google Speech TTS & MP3 Audio)**, **Direct Chatbot Order Placement (No Add-To-Cart Required)**, **Dynamic Delivery Fee Rules (Inside/Outside Dhaka)**, **RAG Product Matching**, and **AI Sales Growth Engines** built with FastAPI, OpenAI (`gpt-4o-mini`), and MongoDB.

---

## 📁 Project Structure

```
skincare-ai/
├── main.py                        ← FastAPI entry point & Router registration
├── requirements.txt
├── .env
├── README.md                      ← Documentation
└── app/
    ├── api/
    │   └── routes/
    │       ├── skincare_products.py ← GET/POST /api/products/ (Catalog, Safety, Comparison, Sales)
    │       ├── chat.py              ← POST /api/chat/ (Voice, Text, Vision AI Advisor)
    │       └── orders.py            ← POST/GET /api/orders/ (Direct Chatbot COD Orders)
    ├── core/
    │   ├── config.py              ← Environment Settings
    │   └── database.py            ← MongoDB Motor Async Connection
    ├── models/
    │   ├── skincare.py            ← Product, Safety, Comparison, Order schemas
    │   └── chat.py                ← ChatRequest & ChatResponse schemas
    └── services/
        ├── skincare_seed.py       ← MongoDB product auto-seeding
        └── skincare_ai_service.py  ← RAG Engine, Vision AI, Voice TTS & Sales Logics
```

---

## ⚡ Core Features & Capabilities

### 1. 📷 Multimodal Vision AI (Skin & Product Recognition)
- **Skin/Face Photo Analysis**: Analyzes facial skin condition (*acne, redness, dark spots, dryness, pores, dark circles*) and outputs a comprehensive analysis & description in **Bengali** (`reply` and `voice_text`).
- **Product Bottle Recognition**: Identifies skincare product bottles/boxes, brand, active ingredients, usage instructions in **Bengali**, and checks store availability.

### 2. 🗣️ Free Voice Speech & TTS (`voice_audio_url`)
- **100% Free Voice Output**: Outputs voice scripts tailored for browser `window.speechSynthesis` (Google Bangla Voice).
- **Free Direct MP3 Audio Link (`voice_audio_url`)**: Generates direct Google Translate TTS audio links for frontend audio players without incurring API costs.

### 3. 🛒 Direct Chatbot Order Confirmation (No Add-To-Cart Page Needed)
- Allows users to order recommended products directly inside the chat conversation.
- Flexible selection: choose 1, 2, or all recommended items (e.g., *"only 1st product"* or *"CeraVe cleanser only"*).
- **Dynamic Delivery Fee Calculation**:
  - **Inside Dhaka**: `$2.00` (60 BDT)
  - **Outside Dhaka**: `$4.00` (120 BDT)
- **Auto Order Extraction**: AI prompts for Name, Phone, Address, Email, extracts details, saves order to MongoDB `orders` collection with status `"Pending Admin Confirmation"`, and returns an order receipt.

### 4. 📈 4 AI Sales Growth Engines
- **Smart Routine Bundle Builder** (`POST /api/products/bundle-recommendation`): Complete 3-step routine bundle with 15% discount for up-selling.
- **Restock & Replenishment Calculator** (`POST /api/products/restock-calculator`): Calculates bottle depletion days and suggests restock date.
- **Gift Finder Quiz** (`POST /api/products/gift-finder`): Curated luxury skincare gift box sets based on budget and skin type.
- **Social Proof Confidence Stats** (`GET /api/products/{id}/confidence-stats`): Verified customer skin improvement ratings.

### 5. 🛡️ AI Skincare Safety & Routine Tools
- **Ingredient Safety & Conflict Checker** (`POST /api/products/check-safety`): Identifies chemical conflict risks (e.g. *Retinol + Vitamin C*) and provides morning/night separation rules.
- **Side-by-Side Product Comparison** (`POST /api/products/compare`): Compares 2 products side-by-side and declares winners for Dry, Oily, and Sensitive skin.
- **Weekly Routine Scheduler** (`POST /api/products/routine-schedule`): Monday-Sunday AM/PM routine grid.

### 6. 💸 Ultra Low-Cost RAG Engine (`gpt-4o-mini`)
- **RAG Keyword Retriever**: Filters catalog down to top 3-5 relevant products before prompting the LLM, reducing token costs by **~95%**.
- **Zero-Token Pre-Indexed Rule Engines**: Safety checks, comparisons, routine scheduling, and order calculations run on fast zero-cost local Python logic.

---

## 📑 API Endpoints Reference

| Category | Method | Endpoint | Description |
|----------|--------|----------|-------------|
| **AI Chat & Vision** | `POST` | `/api/chat/` | Voice, Text & Vision AI Advisor (Symptom analysis, products, Bengali voice TTS script) |
| | `POST` | `/api/chat/analyze-image` | Multimodal Vision AI for Skin Photo Analysis & Product Recognition in Bengali |
| | `POST` | `/api/chat/analyze-symptoms` | Dedicated skin symptom analysis & product match endpoint |
| | `GET`  | `/api/chat/charts/concerns` | Common skin concern distribution chart |
| **Catalog & Products** | `GET`  | `/api/products/` | List all skincare products with concern/skin-type filters |
| | `GET`  | `/api/products/{id}` | Get single skincare product details |
| | `POST` | `/api/products/seed` | Manually trigger product database auto-seeding |
| **Safety & Tools** | `POST` | `/api/products/check-safety` | AI Ingredient Safety & Chemical Conflict Checker |
| | `POST` | `/api/products/compare` | AI Side-by-Side Product Comparison & Winner Verdict |
| | `POST` | `/api/products/routine-schedule` | AI Weekly Routine Scheduler (Monday-Sunday AM/PM Grid) |
| **Sales Growth** | `POST` | `/api/products/bundle-recommendation` | AI Smart Routine Bundle Builder (15% Up-Sell Discount) |
| | `POST` | `/api/products/restock-calculator` | AI Restock & Volume Depletion Calculator |
| | `POST` | `/api/products/gift-finder` | AI Skincare Gift Finder Quiz & Box Builder |
| | `GET`  | `/api/products/{id}/confidence-stats` | AI Social Proof & Verified Results Stats |
| **Chatbot Orders** | `POST` | `/api/orders/` | Place direct Cash-on-Delivery order (Inside/Outside Dhaka delivery fee) |
| | `GET`  | `/api/orders/` | Admin list customer orders with status filter |
| | `GET`  | `/api/orders/{id}` | Get single order details |
| | `PATCH`| `/api/orders/{id}/status` | Admin update order status (*Pending -> Confirmed by Call -> Shipped*) |

---

## 🚀 Setup & Execution Guide

```bash
# 1. Activate Python environment
venv\Scripts\activate  # On Linux/macOS: source venv/bin/activate

# 2. Install required packages
pip install -r requirements.txt

# 3. Environment configuration (.env)
# Create or update .env file:
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=skincare_db
OPENAI_API_KEY=your_openai_api_key_here

# 4. Start the server
uvicorn main:app --reload --port 8000
```

---

## 🌐 Interactive OpenAPI Documentation

Access interactive Swagger documentation and test endpoints directly at:
**`http://localhost:8000/docs`**