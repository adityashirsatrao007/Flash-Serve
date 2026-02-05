from engine.llm_engine import LLMEngine
import time

def main():
    # 1. Init Engine
    engine = LLMEngine(model_name="gpt2", max_num_seqs=4)
    
    # 2. Add Requests
    prompts = [
        "The best programming language is",
        "Artificial Intelligence will",
        "The quick brown fox"
    ]
    
    for p in prompts:
        req_id = engine.add_request(p)
        print(f"Added request {req_id}: {p}")
        
    # 3. Run Loop
    print("\n--- Starting Inference Engine Loop ---")
    step = 0
    active = True
    
    while active:
        step += 1
        outputs = engine.step()
        
        if not outputs:
            print("No more work to do.")
            break
            
        # Print stream (simplified)
        print(f"\n[Step {step}]")
        for out in outputs:
            status = "[Finished]" if out["finished"] else ""
            print(f"Req {out['req_id']}: {out['text']} {status}")
            
    print("Done!")

if __name__ == "__main__":
    main()
