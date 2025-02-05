import json
import numpy as np
from mathematics_dataset import generate
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
import torch
from torch.utils.data import Dataset

# Function to generate math problems
def generate_math_problems(category="arithmetic", num_samples=1000):
    problems = []
    for _ in range(num_samples):
        instance = generate.math_problem(category)
        problem_text = instance.question
        solution_text = instance.answer
        problems.append({"question": problem_text, "answer": solution_text})
    return problems

# Generate dataset
math_data = generate_math_problems(category="arithmetic", num_samples=1000)

# Save to JSON
with open("math_dataset.json", "w") as f:
    json.dump(math_data, f, indent=4)

# Load tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token

# Define PyTorch Dataset
class MathDataset(Dataset):
    def __init__(self, json_file, tokenizer, max_length=128):
        with open(json_file, "r") as f:
            self.data = json.load(f)
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        item = self.data[idx]
        input_text = f"Q: {item['question']} A:"
        target_text = item["answer"]
        
        encoding = self.tokenizer(
            input_text, target_text,
            truncation=True, padding="max_length",
            max_length=self.max_length,
            return_tensors="pt"
        )
        
        input_ids = encoding["input_ids"].squeeze()
        attention_mask = encoding["attention_mask"].squeeze()
        labels = encoding["input_ids"].squeeze()
        
        return {"input_ids": input_ids, "attention_mask": attention_mask, "labels": labels}

# Load dataset
dataset = MathDataset("math_dataset.json", tokenizer)

# Load model
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Define training arguments
training_args = TrainingArguments(
    output_dir="./math_model",
    per_device_train_batch_size=8,
    num_train_epochs=3,
    save_strategy="epoch",
    logging_dir="./logs",
    logging_steps=500,
    evaluation_strategy="epoch"
)

# Trainer API
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    tokenizer=tokenizer
)

# Train the model
trainer.train()

# Save model
model.save_pretrained("./math_trained_model")
tokenizer.save_pretrained("./math_trained_model")

print("Training complete! Model saved.")

