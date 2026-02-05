# Technology Stack Documentation

## 1. Stack Overview
**Last Updated**: 2024-02-05
**Version**: 1.0

### Architecture Pattern
- **Type**: Backend Service with detached UI
- **Pattern**: Python AsyncIO Service + Stateless API + Client UI
- **Deployment**: Local / Single Node (GPU/CPU)

---

## 2. Infrastructure & Compute
### Core Runtime
- **Language**: Python
- **Version**: 3.10+
- **Reason**: Dominant ecosystem for AI/ML.

### AI/ML Framework
- **Library**: PyTorch (`torch`)
- **Version**: 2.2.0+
- **Reason**: Native tensor operations, widespread adoption, CUDA support.
- **Model Library**: HuggingFace Transformers (`transformers`)
- **Reason**: Access to GPT-2, Llama, and other pre-trained models.

---

## 3. Backend Stack (The Engine)
### API Framework
- **Framework**: FastAPI
- **Version**: 0.109.0
- **Server**: Uvicorn
- **Reason**: High-performance AsyncIO, auto-generated docs, easy to integrate with Engine loop.

### Concurrency
- **Library**: `asyncio` (Standard Lib)
- **Reason**: Handling concurrent API requests while managing the blocking Engine loop.

---

## 4. Frontend Stack (The Demo UI)
### UI Framework
- **Library**: Streamlit
- **Version**: 1.30.0
- **Reason**: Rapid prototyping for data apps. No HTML/CSS required.
- **HTTP Client**: `requests` (Standard synchronous client for Streamlit).

---

## 5. Development Tools
### Visualization
- **Library**: Matplotlib
- **Reason**: Generating benchmark charts.

### Utilities
- **Library**: `psutil`
- **Reason**: Monitoring system memory usage.
- **Library**: `numpy`
- **Reason**: Fast math for memory block calculations.

---

## 6. Environment Variables
No secrets required for local demo (running open weights).
Optional (if using gated models):
```bash
HUGGING_FACE_TOKEN="hf_..."
```

---

## 7. Dependencies Lock
### Requirements (`requirements.txt`)
```text
torch
transformers
fastapi
uvicorn
psutil
numpy
streamlit
matplotlib
requests
```
