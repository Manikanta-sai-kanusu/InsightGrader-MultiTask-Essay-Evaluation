from fastapi import FastAPI
from pydantic import BaseModel
import torch
from transformers import BertTokenizer, pipeline
from your_model_file import CustomGRU
import textstat  # New import


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
vocab_size = tokenizer.vocab_size
embed_dim = 300
model_path = "BERT_best.pth"

model = CustomGRU(vocab_size=vocab_size, embed_dim=embed_dim, num_bio_labels=2)
model.load_state_dict(torch.load(model_path, map_location=device))
model.to(device)
model.eval()

# Initialize grammar correction pipeline once
grammar_corrector = pipeline("text2text-generation", model="prithivida/grammar_error_correcter_v1")

app = FastAPI()


class EssayText(BaseModel):
    essay: str
    domain: str


def estimate_cognitive_load(text: str) -> str:
    """
    Use Textstat's Flesch Reading Ease score to estimate cognitive load.
    Returns one of: "easy", "medium", "difficult"
    """
    score = textstat.flesch_reading_ease(text)
    if score >= 80:
        return "easy"
    elif score >= 60:
        return "medium"
    else:
        return "difficult"


@app.post("/predict")
async def assess_essay(data: EssayText):
    essay_text = data.essay
    domain = data.domain

    encoded = tokenizer(
        essay_text, padding="max_length", truncation=True, max_length=256, return_tensors="pt"
    )
    input_ids = encoded["input_ids"].to(device)

    with torch.no_grad():
        bio_logits, reg_logits = model(input_ids)

    bio_preds = torch.argmax(bio_logits, dim=-1).cpu().tolist()[0]
    tokens = tokenizer.tokenize(essay_text)
    bio_tags = bio_preds[: len(tokens)]

    # Dummy scores: replace with your model's scoring logic
    coherence_score = 7.0
    vocabulary_score = 6.5
    grammar_score = reg_logits.cpu().item()

    # Generate corrected essay using grammar corrector pipeline
    correction_result = grammar_corrector(essay_text)
    corrected_essay = correction_result[0]["generated_text"] if correction_result else "No correction available."

    feedback = "Your essay analysis is complete. See the improved essay below."

    cognitive_load = estimate_cognitive_load(essay_text)  # Use new function

    return {
        "coherence_score": coherence_score,
        "vocabulary_score": vocabulary_score,
        "grammar_score": grammar_score,
        "feedback": feedback,
        "corrected_essay": corrected_essay,
        "bio_tags": bio_tags,
        "cognitive_load": cognitive_load,
    }
