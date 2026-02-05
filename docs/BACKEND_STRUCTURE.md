# Backend Architecture & Data Structure

## 1. Architecture Overview
### System Architecture
- **Pattern**: Asynchronous Inference Engine wrapped in REST API.
- **Components**:
  1. **API Layer** (FastAPI): Handles HTTP requests.
  2. **Scheduler**: Manages Request Queue and Batching.
  3. **BlockManager**: Handles PagedAttention Memory (KV Cache).
  4. **ModelExecutor**: Runs the PyTorch Neural Network.

---

## 2. Data Structures (The "Schema")
Since this is an in-memory system (no SQL DB), our "Tables" are Python Class Structures.

### Class: `Sequence`
**Purpose**: Represents a single user request/prompt.

| Attribute | Type | Description |
|-----------|------|-------------|
| `req_id` | `str` (UUID) | Unique identifier |
| `prompt` | `str` | Input text |
| `token_ids`| `List[int]` | Tokenized prompt + generated tokens |
| `status` | `Enum` | WAITING, RUNNING, FINISHED |

### Class: `PhysicalTokenBlock`
**Purpose**: A unit of GPU memory for PagedAttention.

| Attribute | Type | Description |
|-----------|------|-------------|
| `block_number` | `int` | Physical slot index in KV Cache |
| `ref_count` | `int` | Number of sequences using this block (for beam search/sharing) |
| `is_free` | `bool` | Whether it is available for allocation |

---

## 3. API Endpoints
### POST `/v1/completions`
**Purpose**: Generate text from a prompt.

**Request Body**:
```json
{
  "prompt": "Hello world",
  "max_tokens": 50
}
```

**Response**:
```json
{
  "id": "req-1234",
  "object": "text_completion",
  "model": "gpt2",
  "choices": [
    {
      "text": "Hello world, how are you?",
      "finish_reason": "length"
    }
  ]
}
```

**Internal Logic**:
1. Create `Sequence` object.
2. Add to `Scheduler` waiting queue.
3. Wait for `inference_loop` to process.
4. Return result.

---

## 4. Scheduling Logic
### Continuous Batching
Instead of waiting for a batch to finish, we re-evaluate every step:
1. **Filter**: Remove FINISHED sequences.
2. **Inject**: Add WAITING sequences if there is space (BlockManager check).
3. **Execute**: Run model forward pass on new set.

---

## 5. Memory Management (PagedAttention)
- **KV Cache**: Key/Value tensors for Attention mechanism.
- **Problem**: Pre-allocating max length wastes 60-80% memory.
- **Solution**: Allocate "Blocks" (e.g., size 16 tokens) on demand.
- **Mapping**: Using a Block Table to map `Logical Block -> Physical Block`.
