---
layout: default
title: "Step 0: Data Collection"
---

In this step, I focused on collecting a comprehensive list of websites for the categorization project. The data collection process involved the following:

## 1. Extracting URL Logs from Internal Sources

We leveraged URL logs from two colleges, **GNDEC Ludhiana** and **Thapar University**, to extract domain names visited over the past 3 years. 

### Developer Actions:
- **Log Extraction**: I extracted URL logs from the firewall/network monitoring system of both colleges.
- **Data Parsing**: Using Python, I parsed these logs to isolate the domain names from the URLs.
  
Example:
```python
from urllib.parse import urlparse

url = 'https://sub.example.com/page'
domain = urlparse(url).netloc  # Outputs: 'sub.example.com'
```

## 2. Domain Name Extraction

The logs contained full URLs, but only domain names were necessary for the project. Subdomains were removed to ensure focus on primary domains.

### Developer Actions:
- **Parsing and Cleaning**: I used Python's `urlparse` module to extract domain names and cleaned the list to remove subdomains.
  
Example:
```python
domain = urlparse(url).netloc.split('.')[-2:]  # Reduces 'sub.example.com' to 'example.com'
```

## 3. Filtering and Cleaning Data

The raw list of domains was further filtered to remove irrelevant entries such as hosting services and CDN domains. Duplicate domains were also eliminated.

### Developer Actions:
- **Filtering**: I implemented custom filters to exclude domains related to hosting or CDNs.
- **Duplicate Removal**: A simple Python script removed duplicates from the dataset.
  
Example:
```python
unique_domains = list(set(domain_list))
```

## 4. Handling Expired Domains

A significant portion of domains from the logs were expired or unreachable.

### Developer Actions:
- **Availability Check**: I developed a script to check the reachability of each domain.
- **Filtering**: Expired domains were automatically removed from the list.
  
Example:
```python
import requests

def check_domain_availability(domain):
    try:
        response = requests.get(f"http://{domain}", timeout=5)
        return response.status_code == 200
    except requests.ConnectionError:
        return False
```

## 5. Augmenting Data with the Top 10 Million Domains

To enhance the dataset, I downloaded a list of the top 10 million domains from Domcop.

### Developer Actions:
- **Data Integration**: I merged the cleaned internal domain list with the top 10 million domains from Domcop, ensuring proper formatting for scraping.

## 6. Issues with Alternative Data Sources

While considering other sources like Kaggle and GitHub, we encountered formatting issues, such as missing protocols and data inconsistencies.

### Developer Actions:
- **Formatting Issues**: I discarded inconsistent or incomplete lists from Kaggle and GitHub and focused on reliable sources like Domcop.

## 7. Final Domain List

After these processes, I had a refined and structured list of domains ready for scraping and categorization.

### Developer Actions:
- **Combining and Preprocessing**: I combined multiple sources and ensured the domains had proper "http" or "https" prefixes for smooth scraping.
  
---
