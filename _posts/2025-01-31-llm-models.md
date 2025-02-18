---

layout: default  
title: "Transition to Pretrained LLM Models for Website Categorization"

---

## Overview

After extensive experimentation with clustering algorithms, including **K-Means**, **DBSCAN**, and even leveraging GPU acceleration using **cuML**, we encountered a major roadblock: the clusters generated were not well-separated. There was too much noise within the clusters, leading to overlapping categories. This lack of clear separation between clusters meant that the results would not be reliable for our use case, and it was clear that using such noisy clusters would not yield satisfactory accuracy.

### Issues with Clustering

- **Poor Separation**: The clusters were not well-defined, and many websites ended up in the same cluster despite being from different categories.
- **High Noise**: There was a significant amount of noise, which made the clusters unusable for categorization purposes.
- **Low Silhouette Score**: Despite all efforts, the highest silhouette score we achieved with K-Means was around 0.2, indicating poor cluster separation.

As a result, we had to abandon this approach since it was clear that the quality of clustering would not be sufficient for our goals.

---

## Transition to Large Language Models (LLMs)

Given the limitations of clustering, we decided to pivot our approach. Instead of manually categorizing the websites using clusters, we turned to **pretrained open-source Large Language Models (LLMs)** to automate the process of website categorization. These models have shown remarkable ability in understanding and classifying text data and can potentially offer much higher accuracy in categorizing websites based on their content.

### Why LLMs for Website Categorization?

1. **Contextual Understanding**: LLMs are trained on vast amounts of text and can understand the context of words and sentences, making them suitable for tasks like categorizing website content based on textual information.
2. **Pretrained Models**: Pretrained LLMs come with the advantage of already being trained on a diverse dataset, which can be fine-tuned or directly applied to our use case.
3. **Automation**: Using LLMs allows us to bypass the need for manual labeling and categorization, automating the process based on the text data scraped from websites.

---

## The New Plan

Our new plan is to test different **pretrained LLM models** for categorizing the websites based on their content. This involves the following steps:

1. **Model Selection**: We will explore various open-source LLMs that have shown good performance in text classification tasks. Some potential models include:
   - **Meta's LLaMA model**: Known for its efficiency and accuracy in NLP tasks.
   - **OpenAI's GPT-based models**: Proven capability in text classification.
   - **Other domain-specific models**: If available, models fine-tuned for specific domains (e.g., technology, finance) could be valuable.

2. **Text Data Preprocessing**: The text data that was scraped from websites needs to be preprocessed for feeding into LLMs. This involves tokenization, stopword removal, and ensuring that the text is in a suitable format for input into the model.

3. **Testing and Evaluation**: We will test multiple LLMs on our dataset and evaluate their performance based on classification accuracy, precision, recall, and other relevant metrics. The best-performing model will be used for final website categorization.

---

## Conclusion

After realizing that traditional clustering methods were insufficient for separating website categories effectively, we decided to transition to a more advanced approach using pretrained Large Language Models (LLMs). These models are expected to provide better accuracy and allow us to automate the website categorization process based on the content we scraped.

The next steps will involve selecting suitable LLMs, preprocessing the data, and evaluating the models for this task.

---