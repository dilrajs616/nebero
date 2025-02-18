---
layout: default
title: "Introduction"
---

## Problem Statement

With the ever-increasing number of websites online, it has become important to organize and categorize websites based on their content. This categorization helps in enhancing security systems as well.

The problem statement for this project is that we are intending to implement a website blocking feature in our firewall. To block websites effectively, the firewall must first be able to identify the category of each website. Automated categorization will be essential, as it will allow for quick and reliable classification of websites based on their content, ensuring that harmful or unwanted websites can be blocked proactively. The final goal will be to build a model capable of predicting the category of any new website that it encounters.

## Project Overview

In this project, we are aiming to create an automated pipeline that can scrape websites, extract keywords, and categorize them based on their content. Since we do not have any labeled dataset for training the model, we plan to produce a labeled dataset by clustering websites with similar content together and manually labeling these clusters with meaningful category names. The final goal will be to build a model capable of predicting the category of any new website that it encounters.

Our approach will consist of three main tasks:

1. **Scraping Website Content**: Automatically visiting a website, retrieving its content, and cleaning it by removing irrelevant parts (e.g., ads, scripts).

2. **Keyword Extraction**: Extracting relevant keywords from the scraped content using techniques like Term Frequency-Inverse Document Frequency (TF-IDF).

3. **Website Clustering**: Grouping websites with similar keywords using clustering algorithms like K-Means, and then manually labeling the clusters to create a labeled dataset.

This labeled dataset will later be used to train a model capable of categorizing new websites.

## Approach

### 1. Scraping Website Content

To begin with, we will develop an automated web scraping script using Playwright to navigate websites, extract content, and clean the data. The process will be designed to extract only the main textual content by ignoring irrelevant parts of the HTML, such as JavaScript, CSS, and ads.

#### Key Steps in Scraping:

- **Browser Automation**: We will use Playwright to programmatically navigate to websites. A timeout will be implemented to handle slow-loading pages, and we will also capture redirected URLs.
- **Content Extraction**: We will use BeautifulSoup to parse the HTML content and remove unwanted elements such as ads, banners, and scripts to focus on the main body content.
- **Error Handling**: Errors such as timeouts and page load issues will be logged for later analysis, and any failures will be handled gracefully without crashing the entire scraping pipeline.
- **Language Detection**: After extracting content, we will implement a language detection step to identify the language of the text, ensuring that the websites are in the expected language before moving to the next stage.

### 2. Keyword Extraction

Once the content is scraped, we will move on to extracting relevant keywords from the textual data. This will be crucial, as keywords will serve as the main features for categorizing websites.

#### Approach to Keyword Extraction:

- **Content Cleaning**: The text will be cleaned by removing non-alphabetic characters, punctuation, and extra spaces. This will allow us to focus only on meaningful words in the content.
- **TF-IDF Vectorizer**: We will use the Term Frequency-Inverse Document Frequency (TF-IDF) technique to extract important keywords from the content. The TF-IDF vectorizer will assign higher weights to words that are more important within the context of the text, and we will cap the number of features at 1,000 to limit the dimensionality.
- **Keyword Ranking**: After vectorizing the content, we will rank keywords by their TF-IDF scores and select the top-ranked keywords to represent each website.

### 3. Clustering Websites

The next step will be to group websites into categories based on their extracted keywords. We will use K-Means clustering for this purpose.

#### Clustering Process:

- **TF-IDF Matrix**: The TF-IDF vectors for all websites will be assembled into a matrix, which will serve as the input for the clustering algorithm.
- **K-Means Clustering**: We will use the K-Means algorithm to group websites with similar keyword distributions into clusters. The number of clusters (`k`) will be chosen experimentally, and we will aim to arrive at a value of `k=90` based on our dataset.
- **Cluster Labeling**: After running the K-Means algorithm, we will manually inspect the websites in each cluster and assign meaningful category names to the clusters. This step will be crucial for creating a labeled dataset.

#### Evaluating Clusters:

- **Silhouette Score**: To evaluate the quality of the clustering, we will calculate the silhouette score, which measures how well-separated the clusters are. A higher score will indicate that the clusters are more distinct.
- **PCA Visualization**: We will use Principal Component Analysis (PCA) to reduce the dimensionality of the keyword vectors and visualize the clusters in a two-dimensional space. This will allow us to visually inspect the clusters and ensure that they are reasonably well-separated.

### 4. Category Prediction for New Websites

With the labeled dataset created in the clustering step, we will proceed to build a prediction model that can categorize new websites.

#### Prediction Pipeline:

- **Scraping and Keyword Extraction**: The process for new websites will start with scraping the website's content and extracting keywords using the same steps as before.
- **TF-IDF Transformation**: The extracted keywords from new websites will be transformed into TF-IDF vectors using the same vectorizer that was used during the clustering step.
- **Cluster Prediction**: Using the pre-trained K-Means model, we will predict the cluster that the new website belongs to based on its keyword vector.
- **Category Mapping**: Finally, the predicted cluster will be mapped to the corresponding category name based on our manual labeling.

This approach will allow us to categorize any new website by simply running it through the scraping, keyword extraction, and prediction pipeline, making the entire process automated and scalable.
