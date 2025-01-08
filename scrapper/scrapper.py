import requests
import re
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import csv
import yake

def is_downloadable(url):
    try:
        response = requests.head(url, allow_redirects=True)
        content_type = response.headers.get('Content-Type', '')
        
        if 'application' in content_type or 'octet-stream' in content_type:
            return True
        return False
    except requests.RequestException as e:
        print(f"Error checking URL: {url}. Error: {e}")
        return False

def extract_internal_links(site, soup):
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

def clean_text(text):
    """
    Cleans up the scraped text by removing unwanted patterns, numbers, and extra whitespace.
    """
    cleaned_text = re.sub(r'\d+', '', text)

    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    return cleaned_text

def extract_html(site):

    if is_downloadable(site):
        print(f"Skipping download link: {site}")
        return None, None  

    gecko_driver_path = "/usr/local/bin/geckodriver"
    service = Service(executable_path=gecko_driver_path)
    # os.environ["MOZ_HEADLESS"] = "1"

    driver = webdriver.Firefox(service=service)

    try:
        driver.set_page_load_timeout(30) 
        driver.get(site)
        driver.implicitly_wait(10)
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
            print(f"Timeout: {site} took too long to load. Skipping...")
            return None, None
    
    except Exception as e:
        print(f"An error occurred while scraping {site}: {e}")
        return None, None
    finally:
        driver.quit()

    return clean_content, internal_links


def scrape_website(site):
    all_text = []
    main_text, internal_links = extract_html(site)
    if main_text==None or internal_links==None:
        return None
    all_text.append(main_text)

    max_links_to_scrape = 5
    print(f"Found {len(internal_links)} internal links. Scraping the first {min(max_links_to_scrape, len(internal_links))} links.")

    for index, link in enumerate(internal_links):
        if index >= max_links_to_scrape:  
            break
        print(f"{index + 1}: Scraping internal link: {link}")
        link_text, _ = extract_html(link)
        all_text.append(link_text)

    # Filter out None values and join only valid string elements
    paragraph = ' '.join([str(item) for item in all_text if item is not None])

    
    return paragraph


with open("testDomains.txt", 'r') as f:
    sites = f.readlines()

def get_keywords_yake(document, num_keywords=10):
    kw_extractor = yake.KeywordExtractor(n=1, top=num_keywords)
    keywords = kw_extractor.extract_keywords(document)
    return [kw[0] for kw in keywords]

with open('keywords.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    writer.writerow(['Index', 'Website', 'Keywords'])

    for index, site in enumerate(sites, start=61): 
        site = site.strip()
        site_content = scrape_website(site)
        
        if not site_content or all(item == '' for item in site_content):
            keywords = ["NA"]
        else:
            keywords = get_keywords_yake(site_content)

        keywords_str = ", ".join(keywords)

        writer.writerow([index, site, keywords_str])

        print(f"Writing {site} data done.")