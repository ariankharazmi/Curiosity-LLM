import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import load_dataset
import transformers
transformers.logging.set_verbosity_info()
# Load the fine-tuning dataset
fine_tune_ds = load_dataset('json', data_files='seed_tasks_5MB.jsonl', split='train')

# Load the pre-trained model and tokenizer from the checkpoint, training results @ /Users/kharazmimac/PycharmProjects/Curiosity-Test14/results/checkpoint-1500
checkpoint_dir = '/Users/kharazmimac/PycharmProjects/Curiosity-Test14/results/checkpoint-1500'  # Adjust the path as necessary
model_name = 'gpt2'
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(checkpoint_dir)

# Set padding token for consistency
tokenizer.pad_token = tokenizer.eos_token

# Preprocess function for fine-tuning
def preprocess_function(dataset_column_examples):
    # Adjust this list based on your dataset columns
    text_fields = ['text', 'prompt', 'response', 'chosen', 'rejected', 'content',
        'sentence', 'concept_name', 'context',
        'column', 'id', 'name', 'instruction', 'instances',
        'input', 'noinput', 'output']
    for field in text_fields:
        if field in dataset_column_examples:
            texts = dataset_column_examples[field]
            break
    else:
        raise ValueError(f"No available text fields were found: {dataset_column_examples.keys()}")

    texts = [str(text) if text is not None else "" for text in texts]
    return tokenizer(texts, truncation=True, padding='max_length', max_length=256)

# Tokenize the fine-tuning dataset
tokenized_datasets = fine_tune_ds.map(preprocess_function, batched=True, remove_columns=fine_tune_ds.column_names)
tokenized_datasets.set_format('torch', columns=['input_ids', 'attention_mask'])

dataset_size = len(tokenized_datasets)

# Define the size of the subsets, for training sets and eval sets, good for setting sizes later
eval_size = min(200, dataset_size)

# Shuffle and split the dataset
shuffled_dataset = tokenized_datasets.shuffle(seed=42)
small_eval_dataset = shuffled_dataset.select(range(eval_size))

# Fine-tuning arguments
training_args = TrainingArguments(
    output_dir='./fine_tuned_results',
    num_train_epochs=3, 
    per_device_train_batch_size=2,
    save_total_limit=2,
    learning_rate=2e-5,
    weight_decay=0.01,
    eval_strategy='epoch', 
    logging_dir='./logs',
    logging_steps=10,
    save_steps=500, 
)

# Data collator for language modeling (not using MLM)
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,
)

# Trainer setup
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets,
    data_collator=data_collator,
    tokenizer=tokenizer,
    eval_dataset=small_eval_dataset
)

# Resume from checkpoint during training if needed to run fine-tuning in different intervals
#Add this snippet into train.train() if needed --> (resume_from_checkpoint="/Users/kharazmimac/PycharmProjects/Curiosity-Test14/fine_tuned_results/checkpoint-9500")
trainer.train(resume_from_checkpoint="/Users/kharazmimac/PycharmProjects/Curiosity-Test14/fine_tuned_results/checkpoint-21000")

# Save the model
trainer.save_model('./fine_tuned_model')

# Evaluate the model
eval_results = trainer.evaluate()
print("Evaluation results:", eval_results)