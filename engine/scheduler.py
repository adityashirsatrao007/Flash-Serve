from typing import List, Dict, Optional, Deque
from collections import deque
import enum
import time

class RequestStatus(enum.Enum):
    WAITING = "WAITING"
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"

class Sequence:
    """Represents a single sequence (prompt + generated tokens)."""
    def __init__(self, seq_id: int, prompt: str, prompt_token_ids: List[int]):
        self.seq_id = seq_id
        self.prompt = prompt
        self.prompt_token_ids = prompt_token_ids
        self.output_token_ids: List[int] = []
        self.status = RequestStatus.WAITING

    def get_len(self) -> int:
        return len(self.prompt_token_ids) + len(self.output_token_ids)

    def append_token_id(self, token_id: int):
        self.output_token_ids.append(token_id)

class SequenceGroup:
    """A group of sequences from a single request (for beam search, usually size=1 for greedy)."""
    def __init__(self, request_id: str, seqs: List[Sequence], arrival_time: float):
        self.request_id = request_id
        self.seqs = seqs
        self.arrival_time = arrival_time
        # For simplicity in MVP, we assume 1 seq per group
        
    def get_seqs(self, status: Optional[RequestStatus] = None) -> List[Sequence]:
        if status is None:
            return self.seqs
        return [s for s in self.seqs if s.status == status]

class Scheduler:
    """
    Implements Continuous Batching.
    Decides which sequences to run in the next step.
    """
    def __init__(self, max_num_seqs: int, max_total_tokens: int):
        self.waiting: Deque[SequenceGroup] = deque()
        self.running: List[SequenceGroup] = []
        
        self.max_num_seqs = max_num_seqs # Max batch size (N)
        self.max_total_tokens = max_total_tokens # Max tokens in KV cache context
        
    def add_request(self, request_id: str, prompt: str, prompt_token_ids: List[int]):
        seq = Sequence(seq_id=int(time.time()*1000), prompt=prompt, prompt_token_ids=prompt_token_ids)
        group = SequenceGroup(request_id, [seq], time.time())
        self.waiting.append(group)
        
    def schedule(self) -> List[SequenceGroup]:
        """
        Naive scheduling policy: FCFS.
        Move waiting -> running as long as we have slots.
        """
        # 1. Update running status check (remove finished)
        # (In a real system, the Engine tells Scheduler who finished. 
        # Here we assume Scheduler decides based on external feedback or simple loop)
        
        # 2. Add new requests
        while self.waiting:
            # Check constraints
            if len(self.running) >= self.max_num_seqs:
                break
                
            # Current naive check: Only checks sequence count, not token memory availability
            # In Phase 3, we connect this to BlockManager to check memory
            group = self.waiting.popleft()
            for seq in group.seqs:
                seq.status = RequestStatus.RUNNING
            self.running.append(group)
            
        return self.running

    def free_finished_request(self, request_id: str):
        self.running = [g for g in self.running if g.request_id != request_id]
