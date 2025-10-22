---
license: apache-2.0
language:
- en
base_model:
- openai-community/gpt2-medium
pipeline_tag: text-generation
tags:
- research
- proof-of-concept
---
## Curiosity-16

Model Summary

- Parameters: 404M Parameters

- Base: GPT-2 Medium (Decoder)

- Tokenizer: AutoTokenizer

- Training: 2-Phase Full SFT

- Purpose: Research Model -- Proof of Concept

- Strengths: Short factual responses, small stories, basic reasoning

- Limitations: Hard-limit at 1-2 Sentences, tends to misunderstand, no safety filter, prone to hallucinate

Description
- Curiosity-16 is a small research model (based on pre-trained GPT-2 Medium) that has 404M Parameters. It uses training samples from 11 diverse HuggingFace datasets.