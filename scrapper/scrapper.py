import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup as BS
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import spacy
from nltk.corpus import stopwords
nlp = spacy.load("en_core_web_sm")

# conn = sqlite3.connect('urls_database.db')
# cursor = conn.cursor()
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS urls (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         url TEXT NOT NULL UNIQUE,
#         details TEXT
#     )
# ''')
# conn.commit()

nltk.download('stopwords')

def preprocess_text(text) -> list:
    doc = nlp(text)
    cleaned_tokens = [token.lemma_.lower() for token in doc if token.is_alpha and not token.is_stop]
    return ' '.join(cleaned_tokens)

def extract_keywords(texts, num_keywords=10):
    tfidf = TfidfVectorizer(max_features=num_keywords)
    tfidf_matrix = tfidf.fit_transform(texts)
    feature_names = tfidf.get_feature_names_out()
    scores = tfidf_matrix.sum(axis=0).A1
    top_keywords = sorted(zip(feature_names, scores), key=lambda x: x[1], reverse=True)
    return top_keywords

async def scrape_site(url) -> None:
    browser = None
    try:
        browser = await launch(headless=True)
        page = await browser.newPage()
        
        await page.goto(url, timeout=60000)  
        await page.waitForSelector('body', timeout=10000)  
        
        html_content = await page.content()
        
        soup = BS(html_content, 'html.parser')
        text_content = soup.get_text()
        cleaned_text = preprocess_text(text_content)
        keywords = extract_keywords([cleaned_text], num_keywords=5)
        keywords_str = ", ".join([keyword for keyword, score in keywords])
        print(keywords_str)
        # cursor.execute("INSERT INTO urls(url, details) VALUES (?,?)", (url, keywords_str))
        # conn.commit()

    except asyncio.TimeoutError:
        pass
        # cursor.execute("INSERT INTO urls(url, details) VALUES (?,?)", (url, "did not respond"))
        # conn.commit()

    except Exception as e:
        pass
        # cursor.execute("INSERT INTO urls(url, details) VALUES (?,?)", (url, "invalid url"))
        # conn.commit()

    finally:
        if browser:
            await browser.close()

asyncio.get_event_loop().run_until_complete(scrape_site("https://www.spermbank.com/"))



# def test() -> None:
#     with open("../domains/filterDomains.txt", 'r') as f:
#         urls = f.readlines()

#     urls = [url.strip() for url in urls]
#     i=0
#     for url in urls:
#         print(i)
#         asyncio.get_event_loop().run_until_complete(scrape_site(url,conn))
#         i+=1

# test()
# conn.close()