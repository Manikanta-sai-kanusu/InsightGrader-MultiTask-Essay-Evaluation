from transformers import RobertaModel, RobertaConfig

class CustomRobertaMTL(nn.Module):
    def __init__(self, pretrained=True, num_bio_labels=2):
        super().__init__()
        config = RobertaConfig()
        self.encoder = RobertaModel(config) if not pretrained else RobertaModel.from_pretrained('roberta-base')
        hidden_size = self.encoder.config.hidden_size
        self.bio_classifier = nn.Linear(hidden_size, num_bio_labels)
        self.reg_head = nn.Linear(hidden_size, 1)
    def forward(self, input_ids, attention_mask):
        outputs = self.encoder(input_ids=input_ids, attention_mask=attention_mask)
        seq_out = outputs.last_hidden_state
        pooled = seq_out[:, 0, :]
        bio_logits = self.bio_classifier(seq_out)
        reg_logits = self.reg_head(pooled).squeeze(-1)
        return bio_logits, reg_logits
print("done")