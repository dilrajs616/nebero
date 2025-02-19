---
layout: default
title: "Multilingual Data Translation and Model Evaluation"
---

### Developer Overview

In this project, I addressed the challenge of **processing multilingual data** by evaluating and testing translation models from Hugging Face. My goal was to identify the most efficient models for translating website content in various languages. I focused on two models:

### 1. **Helsinki-NLP/opus-mt-{src_lang}-en** 
I implemented and tested this model to handle language-specific translations, selecting `{src_lang}` for different languages based on the data.

- **Process**: For each language, I downloaded the corresponding model (e.g., `fr-en` for French to English). I managed the loading of models dynamically, ensuring only one model was active at a time to optimize resource usage.
- **Optimization**: Each model required **300-400 MB of VRAM**, which allowed for efficient translation without overloading GPU memory.
  
**Example Usage**:
```python
from transformers import MarianMTModel, MarianTokenizer

# Loading the French to English model
model_name = "Helsinki-NLP/opus-mt-fr-en"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

# Example translation
text = "Bonjour tout le monde"
tokens = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
translation = model.generate(**tokens)
translated_text = tokenizer.decode(translation[0], skip_special_tokens=True)
print(translated_text)  # Output: "Hello everyone"
```

- **Challenges Solved**: By managing separate models for each language pair, I reduced VRAM usage but needed to handle multiple downloads.

### 2. **M2M100 Fine-Tuned by Facebook**
I tested the **M2M100 model**, which supports translations between any language pair.

- **Process**: The single model was used to translate between various language pairs without downloading separate models.
- **Resource Usage**: The model required **4.6 GB of VRAM**, which was manageable with the available GPU resources. It simplified the process by handling any-to-any translation without extra configuration.

**Example Usage**:
```python
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

# Loading the M2M100 model
model_name = "facebook/m2m100_418M"
tokenizer = M2M100Tokenizer.from_pretrained(model_name)
model = M2M100ForConditionalGeneration.from_pretrained(model_name)

# Example translation (French to German)
text = "Bonjour tout le monde"
tokens = tokenizer(text, return_tensors="pt", padding=True)
model_inputs = tokens.to(device)
generated_tokens = model.generate(**model_inputs, forced_bos_token_id=tokenizer.get_lang_id("de"))
translated_text = tokenizer.decode(generated_tokens[0], skip_special_tokens=True)
print(translated_text)  # Output: "Hallo zusammen"
```

### Conclusion

As the developer, I shortlisted these models for translation tasks:

- **Helsinki-NLP/opus-mt-{src_lang}-en** for scenarios with limited language pairs and minimal VRAM consumption.
- **M2M100** for comprehensive multilingual tasks, trading higher VRAM usage for simplicity and flexibility.
