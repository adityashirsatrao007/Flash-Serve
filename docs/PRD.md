# Product Requirements Document (PRD)

## 1. Product Overview
- **Project Title**: Mini-vLLM (High-Throughput Inference Engine)
- **Version**: 1.0
- **Last Updated**: 2024-02-05
- **Owner**: AI Engineering Team

## 2. Problem Statement
Running Large Language Models (LLMs) with naive HuggingFace pipelines is inefficient. Processing requests sequentially leads to low GPU utilization and high latency for concurrent users. We need a system that maximizes throughput.

## 3. Goals & Objectives
### Business Goals
- Demonstrate "Systems for AI" engineering capability to recruiters.
- Achieve >2x throughput compared to baseline PyTorch inference.

### User Goals
- **End-User**: Chat with a model with minimal latency.
- **Developer**: Integrate LLM inference via a standard API (OpenAI-compatible).

## 4. Success Metrics
- **Throughput**: >100 tokens/sec (vs ~50 tokens/sec baseline) on consumer hardware.
- **Concurrency**: Handle 16+ simultaneous requests without OOM (Out of Memory).
- **Latency**: Time-To-First-Token (TTFT) < 500ms.

## 5. Target Users & Personas
### Primary Persona: AI Engineer (Recruiter/Interviewer)
- **Goals**: Verify the candidate understands PagedAttention, Continuous Batching, and CUDA interaction.
- **Technical Proficiency**: High.

### Secondary Persona: Application Developer
- **Goals**: Use the engine to power a chatbot app via API.
- **Technical Proficiency**: Medium.

## 6. Features & Requirements
### Must-Have Features (P0)
1. **Continuous Batching**
   - **Description**: Schedule new requests immediately when others finish generative phases.
   - **Success Metric**: Zero idle time on GPU between batch items.

2. **PagedAttention Memory Management**
   - **Description**: Manage KV cache in non-contiguous memory blocks to eliminate fragmentation.
   - **Success Metric**: Support 4x larger batch sizes than naive allocation.

3. **OpenAI-Compatible API**
   - **Description**: Expose `/v1/completions` endpoint.
   - **Success Metric**: Compatible with existing OpenAI client libraries.

### Should-Have Features (P1)
1. **Interactive Chat UI**
   - **Description**: Streamlit-based web interface for testing.
   - **Success Metric**: Usable by non-technical users.

## 7. Explicitly OUT OF SCOPE
- **Distributed Inference**: No multi-GPU tensor parallelism (keeping it simple for single device).
- **Kernels**: No custom CUDA kernels (simulated/Python-based for educational clarity).
- **Quantization**: No FP8/INT8 support (FP16/FP32 only).

## 8. User Scenarios
### Scenario 1: High Load Chat
- **Context**: 5 users send prompts simultaneously.
- **Steps**:
  1. Users submit prompts via UI/API.
  2. Engine batches them together.
  3. One user finishes generation early.
  4. Engine immediately inserts a new request in that slot.
- **Expected Outcome**: All users receive tokens continuously; throughput remains high.

## 9. Dependencies & Constraints
- **Hardware**: CPU or NVIDIA GPU (CUDA).
- **Software**: Python 3.10+, PyTorch, FastAPI.

## 10. Timeline & Milestones
- **MVP**: Completed (Engine + API + UI).
- **V1.0**: Optimization & Benchmarking (Completed).
