# Stock Tickers API

A simple Python Websocket API built with FastAPI to demonstrate:

- Schema-first model generation with Pydantic v2
- In-memory WS operations
- Modern Python packaging and dependency management

This project is intended as an **introductory Python upskilling task**.

---

## Requirements

- Python **3.14**
- pip
- Virtual environment support

---

## Setup

### 1. Create and activate a virtual environment

**Windows**

python -m venv .venv
.venv\Scripts\activate

**macOS/Linux**

python3 -m venv .venv
source .venv/bin/activate

### 2. Install dependencies

pip install -r requirements.txt

### 3. Generate Pydantic models form JSON Schema

Do not create or edit stock_model.py or any other models manually.
Use: **python scripts/generate_models.py** to (re)generate them.

### 4. Run the API

uvicorn stock_ticker_api.main:app --reload

---

## Authentication

All endpoints are protected using HTTP Basic authentication.

Default credentials:

- Username: admin
- Password: changeme

---

### How to test it
#### Through DevConsole

1. Open: Developer Tools in Browser
2. Go to Console and paste:
```javascript
const ws = new WebSocket(
    "ws://127.0.0.1:8000/ws/ticker?username=admin&password=changeme"
    );

    ws.onmessage = (event) => {
    console.log("UPDATE:", event.data);
    };
    
    ws.onopen = () => {
    console.log("CONNECTED");
    };

    ws.onclose = () => {
        console.log("DISCONNECTED");
    };
```

4. The WebSocket connection is now open and streaming updates.
5. Press **Ctrl+C** in the terminal to stop the server. The WebSocket will automatically disconnect.


