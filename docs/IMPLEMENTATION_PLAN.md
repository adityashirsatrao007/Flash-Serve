# Implementation Plan & Build Sequence

## Overview
**Project**: Mini-vLLM
**Objective**: Build a high-throughput LLM inference engine from scratch.
**Approach**: Iterative (Baseline -> Memory -> Engine -> API).

---

## Phase 1: Foundation
### Step 1.1: Project Setup & Baseline
**Goal**: Establish ground truth performance.
**Tasks**:
1. Initialize Project Structure (`engine/`, `model/`, `serve/`).
2. Create `baseline_inference.py` using standard HuggingFace pipeline.
3. Measure throughput (tokens/sec) for comparison.
**Success Criteria**: Baseline script runs and outputs metrics.

---

## Phase 2: Core Optimization Components
### Step 2.1: Key-Value (KV) Cache Manager
**Goal**: Manage memory efficiently.
**Tasks**:
1. Implement `PhysicalTokenBlock` class.
2. Implement `BlockManager` to track free/used blocks.
3. Unit test block allocation/freeing.

### Step 2.2: PagedAttention Logic
**Goal**: The "Virtual Memory" of LLMs.
**Tasks**:
1. Design `BlockTable` mapping (Logical -> Physical).
2. (Simplified) Implement logic to prepare inputs for PagedAttention kernels.

---

## Phase 3: The Engine
### Step 3.1: Scheduler (Continuous Batching)
**Goal**: Maximize GPU utilization.
**Tasks**:
1. Create `LLMEngine` class.
2. Implement `add_request()` and `step()`.
3. Implement `_schedule()` to merge Waiting and Running queues dynamically.

### Step 3.2: Model Executor
**Goal**: Run the Neural Network.
**Tasks**:
1. Wrap PyTorch model (`GPT2LMHeadModel`).
2. Implement `forward` method that accepts batched inputs.
3. Extract generated logits and sample new tokens.

---

## Phase 4: Serving & Demo
### Step 4.1: API Server
**Goal**: Expose engine to the world.
**Tasks**:
1. Create `api_server.py` (FastAPI).
2. Run `inference_loop` in background task.
3. Implement `/v1/completions` endpoint to bridge HTTP to Engine.

### Step 4.2: Chat UI
**Goal**: Visual Proof.
**Tasks**:
1. Build `chat_ui.py` with Streamlit.
2. Connect UI to API.
3. Verify end-to-end chat flow.

### Step 4.3: Benchmark
**Goal**: The "Money Shot".
**Tasks**:
1. Create `benchmark_plot.py`.
2. Compare Baseline vs Mini-vLLM.
3. Generate chart.
