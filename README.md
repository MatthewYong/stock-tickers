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

- python -m venv .venv
.venv\Scripts\activate

**macOS/Linux**

- python3 -m venv .venv
source .venv/bin/activate

### 2. Install dependencies

- pip install -r requirements.txt

### 3. Generate Pydantic models form JSON Schema

Do not create or edit stock_model.py or any other models manually.
Use: **python scripts/generate_models.py** to (re)generate them.

### 4. Run the API

```javascript
uvicorn stock_ticker_api.main:app --reload 
```
---

## Authentication

All endpoints are protected using HTTP Basic authentication.

Default credentials:

- Username: admin
- Password: changeme

---

## How To Test

1. Open a Terminal
2. Paste:
```javascript
uvicorn stock_ticker_api.main:app --reload 
```

2. Open a another new Terminal 
3. Paste:
```javascript
wscat -c ws://127.0.0.1:8000/ws/ticker -H "Authorization: Basic YWRtaW46Y2hhbmdlbWU="   
```

4. The WebSocket connection is now open and streaming updates.
5. Press **Ctrl+C** in the terminal to stop the server. The WebSocket will automatically disconnect.


Example output:
```javascript
{"symbol":"MSFT","price":250.859,"change":0.1034,"percent_change":0.04124,"last_updated":"2026-01-29T15:43:30.625232Z"}
{"symbol":"TSLA","price":160.01867,"change":0.92022,"percent_change":0.5784,"last_updated":"2026-01-29T15:43:32.631756Z"}
{"symbol":"EURUSD","price":130.8956,"change":0.78899,"percent_change":0.60642,"last_updated":"2026-01-29T15:43:34.639709Z"}
```
