---
layout: default
title: "Step 0: Data Collection"
---

Before starting the scraping process, it was essential to gather a comprehensive list of websites to be categorized. The data collection process involved the following steps:

## 1. Extracting URL Logs from Internal Sources

As the firewall was already implemented in multiple colleges and companies, we were able to access URL logs from two colleges: **GNDEC Ludhiana** and **Thapar University**. These logs contained URLs visited by users over the last 3 years. The objective was to extract domain names from these logs for further processing.

### Key Steps:
- **Log Extraction**: We obtained the URL logs from the colleges’ firewall or network monitoring system. These logs contained data about every website visited by users.
- **Data Range**: The data provided logs of URLs accessed over the last 3 years, which gave us a historical snapshot of website traffic.
  
## 2. Extracting Domain Names

After extracting the logs, the next task was to extract only the domain names from the URLs. This was crucial, as the logs also contained full URLs, but we only needed the domain portion for further processing.

### Key Steps:
- **Parsing URLs**: Using Python’s `urlparse` module or similar tools, we parsed the URLs to extract the domain names.
- **Handling Subdomains**: We removed subdomains from the extracted domain names to ensure we were only left with the primary domain. For example, “sub.example.com” would be reduced to “example.com”.
  
## 3. Filtering and Cleaning the Data

Once we had the domain names, we performed a series of cleaning steps to ensure that only relevant domains were included.

### Key Steps:
- **Removing Useless Domains**: We filtered out domains that were irrelevant to the categorization task, such as domains for hosting services (e.g., “example-hosting.com”) and CDN websites (e.g., “cdn.example.com”).
- **Duplicate Removal**: We removed any duplicate domains to avoid having redundant entries in our final list.
- **Final Cleaned Dataset**: After cleaning, we were left with a list of several hundred thousand unique domain names.

## 4. Dealing with Expired Domains

One of the challenges we encountered was that many of the domain names in the extracted list were no longer reachable, as they had expired. These expired domains could not be scraped, so we had to take steps to gather active domains for our project.

### Key Steps:
- **Domain Availability Check**: We implemented a script to check the availability of domains in the list. This helped identify and remove expired or unreachable domains.
- **Filtering Unreachable Domains**: Domains that were no longer available or had expired were removed from the list, leaving only the active ones.

## 5. Downloading the Top 10 Million Domains

To complement the internal data from the URL logs, we downloaded a list of the top 10 million domains to increase the breadth of our dataset. This list was sourced from [Domcop’s Top 10 Million Websites](https://www.domcop.com/top-10-million-websites).

### Key Steps:
- **Downloading from Domcop**: We obtained a ready-made list of the top 10 million domains. This list contained domains that are among the most popular and widely visited on the web, making it a valuable source for website categorization.
  
## 6. Challenges with Alternative Data Sources

While exploring additional sources, we also attempted to download domain lists from Kaggle and GitHub. However, these sources presented some challenges.

### Key Issues:
- **Missing Protocol**: The lists from Kaggle and GitHub only contained domain names (e.g., "example.com") without the "http" or "https" prefix. For web scraping, it is essential to have the full URLs, including the protocol (i.e., "https://example.com"). Without this information, the domains were not directly usable for scraping.
- **Data Inconsistencies**: Some of the domain lists from Kaggle and GitHub lacked necessary details or had inconsistent formatting, which made them less practical compared to the Domcop list.

## 7. Final Domain List

After performing the data collection and cleaning steps, we were left with a refined list of domains, including the top 10 million domains from Domcop and the active domains from the internal URL logs. This list served as the foundation for the next stages of our website categorization project.

### Key Steps:
- **Combining Sources**: We combined the internal domain list with the top 10 million domains from Domcop to create a comprehensive list.
- **Pre-processing**: We ensured that each domain in the final list had the proper format (including "http" or "https") to ensure smooth scraping and data collection.
