import requests
import re
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import csv
import yake
import os
from typing import Optional, Tuple, Set, List

def is_downloadable(url: str) -> bool:
    """
    Checks if the URL points to a downloadable resource (e.g., a file) by inspecting the headers.
    
    Args:
        url (str): The URL to check.

    Returns:
        bool: True if the URL points to a downloadable file, False otherwise.
    """
    try:
        response = requests.head(url, allow_redirects=True)
        content_type = response.headers.get('Content-Type', '')
        
        if 'application' in content_type or 'octet-stream' in content_type:
            return True
        return False
    except requests.RequestException as e:
        return False

def extract_internal_links(site: str, soup: BeautifulSoup) -> Set[str]:
    """
    Extracts internal links from a BeautifulSoup object and returns them as a set.
    
    Args:
        site (str): The base URL of the website.
        soup (BeautifulSoup): The parsed HTML of the website.

    Returns:
        set: A set of internal links that belong to the same domain as the base URL.
    """
    links = soup.find_all("a", href=True)
    internal_links = set()

    domain = urlparse(site).netloc

    for link in links:
        href = link['href']
        full_url = urljoin(site, href)  
        parsed_url = urlparse(full_url)

        if parsed_url.netloc == domain:
            internal_links.add(full_url)
    
    return internal_links

def clean_text(text: str) -> str:
    """
    Cleans up the scraped text by removing numbers and extra whitespace.
    
    Args:
        text (str): The raw text extracted from the website.

    Returns:
        str: The cleaned text.
    """
    cleaned_text = re.sub(r'\d+', '', text)

    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    return cleaned_text

def extract_html(site):
    """
    Extracts the main content from the given website by rendering it using Selenium and cleaning it using BeautifulSoup.
    
    Args:
        site (str): The URL of the website to scrape.

    Returns:
        tuple: A tuple containing the cleaned text content and internal links, or (None, None) if an error occurs.
    """


    if is_downloadable(site):
        return None, None  


    gecko_driver_path = "/usr/local/bin/geckodriver"
    service = Service(executable_path=gecko_driver_path)
    os.environ["MOZ_HEADLESS"] = "1"

    driver = webdriver.Firefox(service=service)
    driver.set_page_load_timeout(30)

    try:
        driver.get(site)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')


        for script in soup(["script", "style"]):
            script.decompose()

        for div in soup.find_all("div", class_=["ad", "ads", "popup", "banner", "modal"]):
            div.decompose()

        for header in soup.find_all("header"):
            header.decompose()

        for footer in soup.find_all("footer"):
            footer.decompose()


        main_content = soup.find_all(["article", "section", "main", "div"])
        text_content = ""


        for element in main_content:
            text_content += element.get_text(separator=" ", strip=True) + " "

        clean_content = clean_text(text_content)
        

        internal_links = extract_internal_links(site, soup)


    except TimeoutException:
            return None, None
    
    except Exception as e:
        return None, None
    finally:
        driver.quit()

    return clean_content, internal_links


def scrape_website(site):
    """
    Scrapes the main text and internal links of a given website. Scrapes a limited number of internal links as well.
    
    Args:
        site (str): The base URL of the website.

    Returns:
        str: The combined scraped text content from the main site and some internal links.
    """
    all_text = []
    main_text, internal_links = extract_html(site)
    if main_text==None or internal_links==None:
        return None
    all_text.append(main_text)

    max_links_to_scrape = 5

    for index, link in enumerate(internal_links):
        if index >= max_links_to_scrape:  
            break
        link_text, _ = extract_html(link)
        all_text.append(link_text)

    # Filter out None values and join only valid string elements
    paragraph = ' '.join([str(item) for item in all_text if item is not None])

    
    return paragraph


def get_keywords_yake(document, num_keywords=20, dedupLim=0.9):
    """
    Extracts the top keywords from a document using the YAKE keyword extraction algorithm.
    
    Args:
        document (str): The text content from which to extract keywords.
        num_keywords (int, optional): The number of top keywords to extract. Default is 20.
        dedupLim (float, optional): Deduplication threshold for similar keywords. Default is 0.9.

    Returns:
        list: A list of extracted keywords.
    """
    kw_extractor = yake.KeywordExtractor(       
        top=num_keywords,         
        dedupLim=dedupLim,        
        windowsSize=2,            
        features=None             
    )
    
    keywords = kw_extractor.extract_keywords(document)
    
    # Extract just the keyword text
    return [kw[0] for kw in keywords]

with open('counter.txt', 'r') as f:
    i = int(f.readline())

with open("testDomains.txt", 'r') as f:
    total_sites = f.readlines()

sites = total_sites[i:]

with open('keywords.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)

    for index, site in enumerate(sites, start=i+1):  
        site = site.strip()
        site_content = scrape_website(site)

        if not site_content or all(item == '' for item in site_content):
            keywords = ["NA"]
        else:
            keywords = get_keywords_yake(site_content)

        keywords_str = ", ".join(keywords)

        writer.writerow([index, site, keywords_str])

        with open('counter.txt', 'w') as f:
            f.write(str(index + 1)) 

