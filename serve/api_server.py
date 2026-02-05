from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import uuid
import uvicorn
from contextlib import asynccontextmanager
from typing import Dict, AsyncGenerator

import sys
import os

# Add parent directory to path to allow importing 'engine' and 'model'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from engine.llm_engine import LLMEngine

# Global Engine Instance
engine: LLMEngine = None
request_queues: Dict[str, asyncio.Queue] = {}

class CompletionRequest(BaseModel):
    prompt: str
    max_tokens: int = 50

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize Engine
    global engine
    # Use a small model for the demo to run on consumer hardware
    # Use a medium model for better intelligence (requires more RAM)
    engine = LLMEngine(model_name="gpt2-medium", max_num_seqs=16) 
    
    # Start the background inference loop
    asyncio.create_task(inference_loop())
    yield
    # Shutdown logic (if any)

app = FastAPI(lifespan=lifespan)

async def inference_loop():
    """
    Background Task: Ticks the engine every few milliseconds.
    """
    print("[Server] Inference loop started.")
    while True:
        # Run one step of the engine
        outputs = engine.step()
        
        # Distribute results to waiting requests
        for out in outputs:
            req_id = out["req_id"]
            if req_id in request_queues:
                # Put the output into the specific request's queue
                request_queues[req_id].put_nowait(out)
                
        # Yield control to allow other async tasks (like receiving requests) to run
        # A small sleep to prevent CPU spinning if idle, 
        # but in tight loop we want 0.
        if not outputs:
            await asyncio.sleep(0.01)
        else:
            await asyncio.sleep(0)

@app.post("/v1/completions")
async def generate(request: CompletionRequest):
    """
    OpenAI-compatible completion endpoint (simplified).
    """
    # 1. Add request to engine
    # We ignore the engine's internal req_id and use our own to map back
    # Actually, LLMEngine.add_request returns the req_id it assigned.
    # We should wrap add_request to be thread-safe if needed, 
    # practically for this MVP, Python GIL + Asyncio single thread is fine.
    
    req_id = engine.add_request(request.prompt)
    
    # 2. Setup a queue to receive tokens
    queue = asyncio.Queue()
    request_queues[req_id] = queue
    
    generated_text = ""
    
    try:
        while True:
            # Wait for next token
            output = await queue.get()
            
            token_text = output["text"]
            generated_text += token_text
            
            if output["finished"]:
                break
                
    finally:
        # Cleanup
        del request_queues[req_id]
        
    return {
        "id": req_id,
        "object": "text_completion",
        "created": int(uuid.uuid4().time_low),
        "model": "gpt2",
        "choices": [
            {
                "text": generated_text,
                "index": 0,
                "logprobs": None,
                "finish_reason": "length"
            }
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
