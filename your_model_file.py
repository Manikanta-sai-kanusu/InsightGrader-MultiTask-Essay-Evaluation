import torch
import torch.nn as nn

class CustomGRU(nn.Module):
    def __init__(self, vocab_size, embed_dim, num_bio_labels=2):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.gru = nn.GRU(embed_dim, 128, batch_first=True, bidirectional=True)
        self.bio_classifier = nn.Linear(128 * 2, num_bio_labels)
        self.reg_head = nn.Linear(128 * 2, 1)

    def forward(self, input_ids):
        emb = self.embedding(input_ids)
        out, _ = self.gru(emb)
        # Pool (take first token's output, or use torch.mean/max for different pooling)
        pooled = out[:, 0, :]  # (batch_size, 256)
        bio_logits = self.bio_classifier(out)       # (batch_size, seq_len, num_bio_labels)
        reg_logits = self.reg_head(pooled).squeeze(-1)  # (batch_size,)
        return bio_logits, reg_logits
