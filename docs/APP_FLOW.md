# Application Flow Documentation

## 1. Entry Points
### Primary Entry Points
- **API Endpoint**: `POST /v1/completions` (Programmatic access)
- **Streamlit UI**: `http://localhost:8501` (Visual access)

## 2. Core User Flows

### Flow 1: Chat Request (UI)
**Goal**: User generates text from a prompt.
**Entry Point**: Streamlit Chat Input.
**Frequency**: High.

#### Happy Path
1. **Page: Chat Interface**
   - User types prompt: "Explain quantum physics."
   - Clicks "Send".

2. **System Action: API Call**
   - UI sends `POST /v1/completions` to API Server (`localhost:8000`).
   - Payload: `{"prompt": "...", "max_tokens": 50}`.

3. **System Action: Engine Scheduling**
   - API Server pushes request to `LLMEngine` queue.
   - `Scheduler` picks up request and allocates blocks via `BlockManager`.
   - Engine runs `model.forward()` step by step.

4. **System Action: Response Streaming**
   - API Server receives generated tokens.
   - Returns full text to UI (MVP: non-streaming HTTP response).

5. **Page: Chat Interface**
   - UI updates with full response.
   - Adds message to chat history.

#### Error States
- **Server Offline**
  - Display: "Error connecting to engine."
  - Action: User must check if `api_server.py` is running.
- **OOM (Out of Memory - Rare)**
  - Display: "Engine overloaded."
  - Action: Scheduler pre-empts requests (if implemented) or rejects.

### Flow 2: Benchmark Run
**Goal**: User verifies performance.
**Entry Point**: CLI Command.

#### Happy Path
1. **User Action**: Run `python benchmark_plot.py`.
2. **System Action**:
   - Runs Inference on Naive Baseline (simulated/logged data).
   - Runs Inference on Mini-vLLM Engine.
   - Generates `benchmark_result.png`.
3. **Output**: Image file saved to disk.

## 3. Navigation Map (UI)
```
Chat UI (Single Page)
├── Chat History Area
│   └── User/Assistant Messages
├── Sidebar
│   ├── Engine Status Indicator
│   └── Settings (Max Tokens Slider)
└── Input Area
    └── Text Box + Send Button
```

## 4. Interaction Patterns
### API Pattern: Polling/Async
- The Engine runs an infinite background loop (`inference_loop()`).
- The API handler puts request in queue and `await`s result.
- Engine processes queue in batches and notifies waiting handlers.

## 5. Decision Points
### Decision: Scheduling
```
IF current_batch size < max_batch_size AND free_memory_blocks > required_blocks
THEN add_request_to_batch()
ELSE
THEN queue_request() # Wait for next slot
```

## 6. Error Handling
### 500 Server Error (Engine Crash)
- **Display**: Stack trace in terminal, 500 JSON error in API.
- **Recovery**: Restart `api_server.py`.
