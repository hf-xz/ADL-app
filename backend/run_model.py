import os

import torch
import torch.nn as nn
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "qwen.pth")

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"device = {device}")

# Load the pre-trained Qwen model and tokenizer
qwen_model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-0.5B")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B")
tokenizer.pad_token = tokenizer.eos_token

# Delete the lm_head to avoid using it for regression
del qwen_model.lm_head


# Define a custom regression model using the Qwen base
class QwenRegressor(nn.Module):
    def __init__(self, base_model):
        super().__init__()
        self.qwen = base_model.model
        self.regressor = nn.Sequential(
            nn.Linear(896, 128),
            nn.GELU(),
            nn.Linear(128, 1),
        )

    def forward(self, input_ids, attention_mask=None):
        outputs = self.qwen(input_ids)
        pooled = outputs.last_hidden_state.mean(dim=1)
        return self.regressor(pooled)


# Create an instance of the regression model
model = QwenRegressor(qwen_model)
model = model.to(device)

# Load the saved model weights
print(f"Loading model from {MODEL_PATH}...")
model.load_state_dict(torch.load(MODEL_PATH))
model.eval()
print(f"Model loaded from {MODEL_PATH}")


# Function to predict scores for reviews
def predict_review_scores(reviews):
    scores = []
    for review in reviews:
        # Tokenize the review text
        encoding = tokenizer(
            review,
            max_length=1280,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )
        input_ids = encoding["input_ids"].to(device)

        # Use the model to predict score (in normalized [0, 1] scale)
        with torch.no_grad():
            prediction = model(input_ids).squeeze().item()
        print(f"Review: {review}\nPredicted score: {prediction}\n")
        scores.append(prediction)

    return scores


if __name__ == "__main__":
    # Example reviews
    reviews = [
        "This movie was terrible. The acting was bad and the plot made no sense. I would not recommend it to anyone.",
        "An average movie with some good moments but overall not very memorable.",
        "A masterpiece! The cinematography and direction were top-notch. A must-watch for any film lover.",
    ]

    # Predict scores for the example reviews
    predict_review_scores(reviews)
