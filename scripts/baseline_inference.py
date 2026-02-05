import time
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import psutil

# Configuration
MODEL_NAME = "gpt2" # Small model for baseline
BATCH_SIZE = 4
PROMPTS = [
    "The future of AI is",
    "Once upon a time in a digital world",
    "The key to high performance computing is",
    "Python is a great language because"
] * 2  # Duplicate to hit batch size if needed

def log_memory():
    process = psutil.Process()
    print(f"[Memory] RAM: {process.memory_info().rss / 1024**2:.2f} MB")

def main():
    print(f"Loading {MODEL_NAME}...")
    log_memory()
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    # GPT2 doesn't have a pad token by default
    tokenizer.pad_token = tokenizer.eos_token
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME).to(device)
    log_memory()

    # Encode
    inputs = tokenizer(PROMPTS[:BATCH_SIZE], return_tensors="pt", padding=True, truncation=True).to(device)
    input_tokens = inputs["input_ids"].shape[1]
    
    print("\n--- Starting Warmup ---")
    _ = model.generate(**inputs, max_new_tokens=10)
    torch.cuda.synchronize() if device == "cuda" else None
    
    print("\n--- Starting Baseline Inference ---")
    start_time = time.time()
    
    # Generate
    MAX_NEW_TOKENS = 50
    with torch.no_grad():
        outputs = model.generate(
            **inputs, 
            max_new_tokens=MAX_NEW_TOKENS, 
            pad_token_id=tokenizer.eos_token_id,
            use_cache=True
        )
    
    if device == "cuda":
        torch.cuda.synchronize()
        
    end_time = time.time()
    duration = end_time - start_time
    
    # Metrics
    total_generated_tokens = (outputs.shape[1] - input_tokens) * BATCH_SIZE
    throughput = total_generated_tokens / duration
    
    print(f"\n[Results]")
    print(f"Batch Size: {BATCH_SIZE}")
    print(f"Input Tokens (per seq): {input_tokens}")
    print(f"Generated Tokens (per seq): {MAX_NEW_TOKENS}")
    print(f"Total Latency: {duration:.4f} s")
    print(f"Throughput: {throughput:.2f} tokens/sec")
    
    print("\n[Generated Text Sample]")
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))

if __name__ == "__main__":
    main()
