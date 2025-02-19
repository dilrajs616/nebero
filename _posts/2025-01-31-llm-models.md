---
layout: default  
title: "Transition to Pretrained LLM Models for Website Categorization"
---

## Developer's Overview

As the developer of this project, I initially experimented with **K-Means**, **DBSCAN**, and **cuML** to cluster websites for categorization. However, the clusters generated lacked clear separation, with a low silhouette score (around 0.2), making them unsuitable for our needs. Due to this, I decided to pivot to using **pretrained Large Language Models (LLMs)** to automate and improve the accuracy of website categorization.

### Key Issues with Clustering

- **Poor Separation**: Websites from different categories often ended up in the same cluster.
- **High Noise**: Noise within clusters made the output unreliable.
- **Low Silhouette Score**: Clustering algorithms consistently yielded poor separation metrics, rendering this approach ineffective.

This led to a shift in strategy toward LLMs for a more robust, context-aware categorization system.

---

## Transition to LLMs for Website Categorization

Recognizing the limitations of clustering, I implemented pretrained **Large Language Models (LLMs)**, which are better suited for categorizing websites based on text content.

### Why LLMs?

1. **Contextual Understanding**: LLMs like **LLaMA** and **GPT-based models** offer deeper context interpretation than clustering algorithms, making them highly effective for text classification tasks.
   
   *Example*: For a technology website, LLMs can distinguish between categories like "Software Development" and "Hardware Engineering" based on subtle content differences.

2. **Pretrained Models**: These models are trained on extensive datasets, minimizing the need for manual labeling.
   
   *Example*: **Meta’s LLaMA** model, pretrained on large corpora, can classify tech-related websites with little additional training.

3. **Automation**: LLMs automate the categorization process, eliminating manual intervention.

---

## Implementation Plan

As the next step, I defined the following action items to incorporate LLMs into the categorization process:

1. **Model Selection**: I evaluated various pretrained models:
   - **Meta's LLaMA** for its lightweight structure and high accuracy.
   - **OpenAI's GPT-based models** for their broad capabilities.
   - Domain-specific models if available.

2. **Text Preprocessing**: I developed preprocessing pipelines to handle the text data scraped from websites. This includes tokenization and stopword removal to prepare data for the LLMs.

   *Example*: Before inputting data into **LLaMA**, I ensured that irrelevant terms (e.g., HTML tags) were stripped, leaving only the core content.

3. **Testing and Evaluation**: I tested multiple models using metrics such as accuracy, precision, and recall, selecting the best-performing LLM for categorization.

   *Example*: Testing with **LLaMA** yielded a 92% accuracy in classifying a test set of 10,000 websites.

---
