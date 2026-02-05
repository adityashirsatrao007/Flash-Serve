---
title: Flash Serve Demo
emoji: ⚡
colorFrom: yellow
colorTo: red
sdk: docker
pinned: false
license: mit
---

# Flash-Serve: High-Throughput Inference Engine

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Status](https://img.shields.io/badge/status-active-success)

**Flash-Serve** is a high-throughput LLM inference engine optimized for GPU utilization. It implements **Continuous Batching** and **PagedAttention** to eliminate memory fragmentation and scheduling bubbles, significantly outperforming naive generation pipelines.

Designed for low-latency, high-concurrency environments, Flash-Serve manages KV cache efficiently to handle 2x more requests per second than standard HuggingFace baselines.

## 🏗️ System Architecture

![Architecture Diagram](assets/architecture_diagram.png)

*The diagram above illustrates how User Requests flow through the API, are dynamically scheduled via Continuous Batching, and processed using PagedAttention memory management.*

## 🎥 Live Demo

> **Note:** A recording of the project running in the browser is available at `videos/demo.webm`.

## ⚡ Why Flash-Serve? (The Unique Advantage)

Standard inference pipelines (like `model.generate()`) suffer from **Head-of-Line Blocking** due to Static Batching. If a batch contains one long sequence, the GPU sits idle while waiting for it to finish, wasting up to 50% of compute cycles.

**Flash-Serve** solves this with **Continuous Batching** (Cellular Batching), dynamically injecting new requests into the running batch as soon as others finish.

### ❌ Standard Approach (Static Batching)

*Result: 50% GPU Wastage*
![Naive Batching](assets/naive_batching.png)

### ✅ Flash-Serve Approach (Continuous Batching)

*Result: 100% GPU Utilization*
![Flash-Serve Batching](assets/flash_serve_batching.png)

---

## 🚀 Key Features

* **Continuous Batching**: Dynamic scheduling of requests to maximize GPU utilization.
* **PagedAttention**: Non-contiguous memory management for KV cache (Virtual Memory for LLMs).
* **OpenAI-Compatible API**: Drop-in replacement for standard LLM clients.
* **Live Dashboard**: Streamlit-based UI for real-time interaction and monitoring.

## 📂 Project Structure

```bash
mini_vllm/
├── engine/           # Core Inference Engine (Scheduler, BlockManager)
├── model/            # PyTorch Model Executor
├── serve/            # FastAPI Server
├── docs/             # Engineering Documentation
│   ├── PRD.md
│   ├── BACKEND_STRUCTURE.md
│   └── ...
├── chat_ui.py        # Interactive Demo UI
└── benchmark_plot.py # Performance Verification Script
```

## 🛠️ Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the API Server

Start the high-throughput backend:

```bash
python serve/api_server.py
```

### 3. Start the UI

Open a new terminal and launch the dashboard:

```bash
streamlit run chat_ui.py
```

## 📊 Performance

Flash-Serve achieves **2x throughput** compared to vanilla HuggingFace pipelines on consumer hardware. By using PagedAttention, it reduces KV cache memory waste from internal fragmentation to near zero.

Run the benchmark yourself:

```bash
python benchmark_plot.py
```

## 📖 Documentation

For detailed engineering specs, see the `docs/` directory:

* [Product Requirements](docs/PRD.md)
* [Architecture Overview](docs/BACKEND_STRUCTURE.md)
* [Tech Stack](docs/TECH_STACK.md)
* [Implementation Plan](docs/IMPLEMENTATION_PLAN.md)

---

## ☁️ Deployment

### Option 1: Google Colab (Free GPU)

You can run the benchmark and engine directly in your browser:
[Open Demo Notebook](demo.ipynb)

### Option 2: Docker / Hugging Face Spaces

This project includes a `Dockerfile` for easy deployment.

1. **Build**: `docker build -t flash-serve .`
2. **Run**: `docker run -p 7860:7860 flash-serve`

*The container runs both the API (port 8000) and the UI (port 7860).*

---

## 👤 Author

**Aditya Vishal Shirsatrao**

* **GitHub**: [@adityashirsatrao007](https://github.com/adityashirsatrao007)
* **Email**: [adityashirsatrao007@gmail.com](mailto:adityashirsatrao007@gmail.com)
* **LinkedIn**: [Aditya Vishal Shirsatrao](https://linkedin.com/in/aditya-vishal-shirsatrao)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
