---
layout: default  
title: "Introduction to Clustering"
---

## Overview

In the **website categorization pipeline**, clustering is used to organize websites into distinct categories based on textual content. The chosen algorithm for this task is **K-Means**, which groups websites into 90 clusters, evaluated using silhouette scores and PCA visualization. The clustering results are manually labeled to create a labeled dataset for model training.

## Clustering Algorithm Selection

### K-Means
For partitioning the dataset into distinct categories, I implemented **K-Means** clustering. The algorithm groups websites into clusters based on the textual content scraped from each website, with each cluster representing a unique category.

- **Example**: Websites offering news content formed a distinct cluster due to shared terms like "headline," "article," and "news."

### DBSCAN
I experimented with **DBSCAN** for its outlier detection capability but found that **K-Means** performed better for well-separated clusters in our dataset. **DBSCAN** was less efficient for large datasets and clusters with varying densities.

- **Example**: For clusters with arbitrary shapes (e.g., blogs with less structured content), DBSCAN identified some outliers but misclassified many websites.

## Key Considerations

### Feature Extraction
Before clustering, the textual content of each website was converted into numerical vectors using **TF-IDF**. This method was effective in identifying important terms for categorization.

- **Example**: For an e-commerce website, terms like "checkout," "cart," and "product" were assigned higher weights, which helped distinguish it from other categories.

### Dimensionality Reduction
Due to the high-dimensional nature of the TF-IDF vectors, **PCA** was applied to reduce the number of dimensions while preserving the data structure. This step was crucial in improving clustering performance.

- **Example**: After applying PCA, we reduced the dimensionality from 500 to 50 features, leading to faster K-Means convergence without losing significant information.

## Preprocessing for Clustering

- **Stop-Words Removal**: I removed common stop-words (e.g., "the," "is," "in") using **spaCy**, which improved the quality of clusters by reducing noise in the textual data.
- **Scaling**: The features were standardized using **StandardScaler** to ensure that different features (e.g., word frequencies) contributed equally during clustering.

## Examples

- **Cluster Analysis**: The resulting clusters were analyzed using silhouette scores, and PCA visualization was applied to validate the separation of clusters. For example, a distinct cluster of educational websites formed based on terms like "student," "course," and "university."
  
- **Manual Labeling**: After clustering, I manually labeled each cluster based on the dominant terms within it. These labeled clusters were then used as training data for the final categorization model.

