from transformers import GPT2Tokenizer, GPT2LMHeadModel, pipeline

# Loading GPT-2 + GPT-2 Tokenizer + Checkpoint filePATH
model_path = '/Users/kharazmimac/PycharmProjects/Curiosity-Test14/fine_tuned_results/checkpoint-26394'
tokenizer = GPT2Tokenizer.from_pretrained(model_path)
model = GPT2LMHeadModel.from_pretrained(model_path)

# Set up pipeline for text generation (relating to user prompt)
text_generator = pipeline('text-generation', model=model, tokenizer=tokenizer)

# Interactive Prompt for user, generate text based on user's entered prompt
while True:
    user_text = input("Enter Prompt: ")
    if user_text.lower() == 'Exiting Chat...':
        break
    result = text_generator(user_text, num_return_sequences=1, truncation=True, max_length=224)
    print(result[0]['generated_text'])
