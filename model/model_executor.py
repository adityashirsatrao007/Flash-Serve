import torch
from transformers import AutoModelForCausalLM

class ModelExecutor:
    def __init__(self, model_name: str, device: str = "cuda"):
        self.device = device
        print(f"Loading {model_name} on {device}...")
        self.model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
        # TODO: optimization - enable torch.compile for production
        # self.model = torch.compile(self.model) 

    def forward(self, input_ids: list[list[int]], past_key_values=None):
        """
        Batched forward pass.
        Current implementation uses naive left-padding.
        TODO: Refactor to use PagedAttention with unpadded tensors.
        """
        # Determine max length for padding
        max_len = max(len(ids) for ids in input_ids)
        
        # GPT-2 uses EOS as pad token usually
        PAD_TOKEN_ID = 50256 
        
        padded_inputs = []
        attn_masks = []
        
        for ids in input_ids:
            pad_len = max_len - len(ids)
            # Left padding is required for generation
            padded = [PAD_TOKEN_ID] * pad_len + ids 
            mask = [0] * pad_len + [1] * len(ids)
            
            padded_inputs.append(padded)
            attn_masks.append(mask)
            
        # Move to GPU
        inputs_tensor = torch.tensor(padded_inputs, device=self.device)
        mask_tensor = torch.tensor(attn_masks, device=self.device)
        
        with torch.no_grad():
            outputs = self.model(input_ids=inputs_tensor, attention_mask=mask_tensor, use_cache=True)
            
        # Logits for the last token (next token prediction)
        return outputs.logits[:, -1, :]
