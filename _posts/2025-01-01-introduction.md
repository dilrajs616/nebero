---
layout: default
title: "Introduction"
---

## Problem Statement

In order to block unwanted websites, our firewall requires the ability to categorize websites based on their content. Given the vast number of websites, this categorization must be automated to ensure efficient and reliable blocking of harmful sites. The objective is to build a model capable of predicting the category of any new website.

## Project Overview

This project involves creating an automated pipeline that:

1. Scrapes website content.
2. Extracts keywords using TF-IDF.
3. Clusters websites based on similar keywords for manual labeling, producing a labeled dataset.

The end goal is to build a model that can predict the category of new websites, enabling automated website blocking in the firewall.

## Approach

### 1. Scraping Website Content

We use Playwright for automating browser navigation, extracting textual content while ignoring irrelevant HTML components (e.g., ads, JavaScript). Key implementation details:

- **Browser Automation**: Playwright handles navigation, and timeouts manage slow-loading pages. Redirects are captured automatically.
  
  **Example**:
  ```python
  page.goto("https://example.com", timeout=30000)  # 30s timeout for slow pages
  ```

- **Content Extraction**: BeautifulSoup parses the HTML, and we clean the content by removing scripts, ads, and banners.

  **Example**:
  ```python
  soup = BeautifulSoup(page.content(), "html.parser")
  main_content = soup.find("div", {"class": "main-body"})
  ```

- **Error Handling**: Logs handle errors like timeouts without interrupting the scraping flow.

- **Language Detection**: After scraping, a language detection step ensures we're working with the correct language before proceeding.

### 2. Keyword Extraction

We use the Term Frequency-Inverse Document Frequency (TF-IDF) method to extract keywords. This will be used for clustering.

- **Content Cleaning**: Non-alphabetic characters, punctuation, and extra spaces are removed.

  **Example**:
  ```python
  cleaned_text = re.sub(r'[^a-zA-Z\s]', '', raw_text)
  ```

- **TF-IDF Vectorizer**: This assigns higher weights to important words, capped at 1,000 features to limit dimensionality.

  **Example**:
  ```python
  from sklearn.feature_extraction.text import TfidfVectorizer
  vectorizer = TfidfVectorizer(max_features=1000)
  tfidf_matrix = vectorizer.fit_transform(cleaned_texts)
  ```

### 3. Website Clustering

We use K-Means to group websites with similar keywords.

- **TF-IDF Matrix**: The keyword vectors from the TF-IDF process are assembled into a matrix for clustering.

- **K-Means Clustering**: We aim for 90 clusters, with the number determined experimentally. Post-clustering, manual labeling will assign categories to clusters.

  **Example**:
  ```python
  from sklearn.cluster import KMeans
  kmeans = KMeans(n_clusters=90, random_state=0)
  clusters = kmeans.fit_predict(tfidf_matrix)
  ```

- **Cluster Evaluation**: We evaluate clusters using the silhouette score and PCA for visualization.

  **Example**:
  ```python
  from sklearn.metrics import silhouette_score
  score = silhouette_score(tfidf_matrix, clusters)
  ```

### 4. Category Prediction for New Websites

Once the labeled dataset is prepared, we build a pipeline for predicting categories of new websites.

- **Scraping and Keyword Extraction**: New websites are scraped, and keywords are extracted as before.

- **TF-IDF Transformation**: The same TF-IDF vectorizer is used for transforming new website content.

- **Cluster Prediction**: The pre-trained K-Means model predicts the cluster for new websites, mapping them to categories.

  **Example**:
  ```python
  new_vector = vectorizer.transform(new_website_content)
  predicted_cluster = kmeans.predict(new_vector)
  ```

This pipeline allows for automated, scalable website categorization, enabling effective website blocking in the firewall system.

---
