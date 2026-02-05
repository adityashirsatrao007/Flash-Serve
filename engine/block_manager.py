from typing import List, Dict

class PhysicalTokenBlock:
    """Represents a physical block of memory on the GPU."""
    def __init__(self, device: str, block_number: int, block_size: int):
        self.device = device
        self.block_number = block_number
        self.block_size = block_size
        self.ref_count = 0

class BlockAllocator:
    """
    Manages the free list of physical blocks.
    """
    def __init__(self, num_blocks: int, block_size: int, device: str = "cuda"):
        self.num_blocks = num_blocks
        self.block_size = block_size
        self.device = device
        
        # Initialize all blocks as free
        # We perform lazy allocation: we just track indices 0 to N-1
        self.free_blocks: List[int] = list(range(num_blocks))
        
    def allocate(self) -> int:
        if not self.free_blocks:
            raise ValueError("Out of memory! No free blocks available.")
        return self.free_blocks.pop()
    
    def free(self, block_number: int):
        if block_number < 0 or block_number >= self.num_blocks:
            raise ValueError(f"Invalid block number {block_number}")
        self.free_blocks.append(block_number)
        
    def get_num_free_blocks(self) -> int:
        return len(self.free_blocks)

class BlockTable:
    """
    Maps logical blocks to physical blocks for a single sequence.
    Similar to a Virtual Memory Page Table.
    """
    def __init__(self, block_size: int, block_allocator: BlockAllocator):
        self.block_size = block_size
        self.allocator = block_allocator
        self.physical_block_indices: List[int] = []
        
    def allocate_token_slot(self):
        """
        Called when a new token is generated. 
        Ensures there is space in the last block, or optimizes a new block.
        """
        # Calculate current logical length capacity
        current_capacity = len(self.physical_block_indices) * self.block_size
        
        # We rely on external tracker to know how many tokens we actually have.
        # But here, let's assume this method is called *before* adding a token that would overflow.
        # Actually simplest logic: "Do we need a new block?"
        
        # This function is meant to be called by the BlockManager which knows the seq len.
        pass

    def add_block(self):
        new_block = self.allocator.allocate()
        self.physical_block_indices.append(new_block)
        
    def free(self):
        for block_idx in self.physical_block_indices:
            self.allocator.free(block_idx)
        self.physical_block_indices = []

class BlockManager:
    """
    High-level manager for PagedAttention memory.
    Connects requests to their block tables.
    """
    def __init__(self, block_size: int, num_gpu_blocks: int, device: str = "cuda"):
        self.block_size = block_size
        self.allocator = BlockAllocator(num_blocks=num_gpu_blocks, block_size=block_size, device=device)
        self.block_tables: Dict[str, BlockTable] = {}
        
    def allocate(self, request_id: str):
        # Create a new table for this request
        self.block_tables[request_id] = BlockTable(self.block_size, self.allocator)
        
    def free(self, request_id: str):
        if request_id in self.block_tables:
            self.block_tables[request_id].free()
            del self.block_tables[request_id]
            
    def get_block_table(self, request_id: str) -> BlockTable:
        return self.block_tables[request_id]
