from .scheduler import Scheduler
from .block_manager import BlockManager, BlockAllocator
from model.model_executor import ModelExecutor
from transformers import AutoTokenizer
import torch

class LLMEngine:
    def __init__(self, model_name: str, block_size: int = 16, max_num_seqs: int = 16, max_total_tokens: int = 1024):
        self.model_name = model_name
        self.block_size = block_size
        
        print(f"[Engine] Initializing Scheduler (max_seqs={max_num_seqs})...")
        self.scheduler = Scheduler(max_num_seqs=max_num_seqs, max_total_tokens=max_total_tokens)
        
        print(f"[Engine] Initializing BlockManager (block_size={block_size})...")
        # TODO: Implement proper GPU memory profiling
        num_gpu_blocks = 100 
        self.block_allocator = BlockAllocator(num_blocks=num_gpu_blocks, block_size=block_size)
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_executor = ModelExecutor(model_name, device=self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        self.request_counter = 0

    def add_request(self, prompt: str) -> str:
        req_id = str(self.request_counter)
        self.request_counter += 1
        
        prompt_token_ids = self.tokenizer.encode(prompt)
        self.scheduler.add_request(req_id, prompt, prompt_token_ids)
        return req_id

    def step(self):
        """
        Performs one decoding step.
        1. Schedule sequences
        2. Prepare batch inputs
        3. Run model inference
        4. Update state
        """
        running_groups = self.scheduler.schedule()
        if not running_groups:
            return []

        # Prepare batch
        # TODO: This naive preparation sends the full context every time.
        # Future optimization: Send only new tokens and use KV cache.
        input_ids = []
        for group in running_groups:
            seq = group.get_seqs()[0]
            full_seq = seq.prompt_token_ids + seq.output_token_ids
            input_ids.append(full_seq)

        logits = self.model_executor.forward(input_ids)
        
        # Greedy sampling
        # logits shape: [batch_size, vocab_size]
        next_token_ids = torch.argmax(logits, dim=-1).tolist()
        
        outputs = []
        for i, group in enumerate(running_groups):
            seq = group.get_seqs()[0]
            token_id = next_token_ids[i]
            
            seq.append_token_id(token_id)
            text = self.tokenizer.decode([token_id])
            
            # Simple stop condition for MVP
            is_finished = seq.get_len() > 50
            if is_finished:
                self.scheduler.free_finished_request(group.request_id)
                
            outputs.append({
                "req_id": group.request_id, 
                "text": text, 
                "finished": is_finished
            })
            
        return outputs
