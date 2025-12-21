# Package importation
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse
import time
import random
import pandas as pd
import re


# Useful Fonctions

# get the url
def fetch_verify_url(url) :
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}  
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch the url: {url} with status code {response.status_code}")
            return None
        return response  
    except requests.RequestException:
        return None


# Transforme the html into a beautifulsoup object
def to_soup(url):
    response = fetch_verify_url(url)
    if response:
        return BeautifulSoup(response.text, 'html.parser') 
    else:
        return None




# Filter the urls added to the list
def filter_links(links, required_keywords=None, domain=None, already_seen=None):
    if required_keywords is None:  # If no list of required keywords is fournished then we create an empty one
        required_keywords = []
    if already_seen is None:  # If no list of already seen links is fournished then we create an empty one
        already_seen = set()
    
    filtered = []
    for l in links:
        l_lower = l.lower()  # Transformation of capital letter into lower case letter
        if required_keywords and not any(keyword.lower() in l_lower for keyword in required_keywords):  # If no required keywords are in the url, then we skip it
            continue
        if domain and urlparse(l).netloc != domain:  # We ignore the urls that are not in the domain
            continue
        if l in already_seen:  # To avoid having multiple times the same url, we skip the ones that are already in the list
            continue
        filtered.append(l)
    return filtered




# Collection of the corpus 
# Collecting the raw corpus
def get_html_corpus(links):
    corpus = []

    for link in links:
        response = fetch_verify_url(link)
        if response:
            corpus.append({'url': link, 'html': response.text}) # A dictionary with the url (as the key) and the corpus is created
        time.sleep(random.uniform(1,4))

    return corpus



# Stocking the corpus in a csv file
import csv

def save_to_csv(data, filename):
    if not data:
        print("Error : There is no data to save")
        return

    fieldnames = data[0].keys()  # Detection of the existing colons in the data file

    with open(filename, 'w', newline='', encoding='utf-8') as f:  # Opens the csv file as utf-8
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)  # Initialising a writer to write the dictionary into the csv file
        writer.writeheader()  # writes the colons headers
        writer.writerows(data)  # writes the rows

    print(f"CSV saved : {filename}")





# This function will clean any html page 
import re

def clean_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    for tag in soup(['script', 'style', 'noscript']):  # Supress any unessecary tags
        tag.decompose()

    text = soup.get_text(separator=' ', strip=True)  # Collect all visible text
    text = re.sub(r'\s+', ' ', text)  # Supress any unecessary spaces

    return text




# Cleans the csv file created previously
def clean_csv_file(input_csv, output_csv):
    df = pd.read_csv(input_csv)  # Take the csv file with the raw html as the input

    if 'html' not in df.columns:  # Verify that the html colon exists
        raise ValueError(f"The html colon is missing in: {input_csv}")

    df['cleaned_text'] = df['html'].apply(clean_html)  # cleans the html colon
    df = df[['url', 'cleaned_text']]  # keep the url and text colon (not the raw html)

    df.to_csv(output_csv, index=False, encoding='utf-8')  # creats a new csv file as the output of the function




# This function normalize any htmlpage
def normalize_html(text):
    text = text.lower()  # convert all letters to lowercase
    text = re.sub(r'\[\d+\]', ' ', text)  # remove reference numbers like [1], [2], etc.
    text = re.sub(r'[^a-z0-9\s]', ' ', text)  # keep only English letters, numbers, and spaces
    text = re.sub(r'\s+', ' ', text)  # replace multiple spaces with a single space
    return text.strip()  # remove leading and trailing spaces




# Normalizes the csv file created previously
def normalize_csv_file(input_csv, output_csv):
    df = pd.read_csv(input_csv)  # Take the csv file with the cleaned text as the input

    if 'cleaned_text' not in df.columns:  # Verify that the cleaned text colon exists
        raise ValueError(f"The cleaned text is missing in: {input_csv}")

    df['normalized_text'] = df['cleaned_text'].apply(normalize_html)  # normalize the cleaned text
    df = df[['url', 'normalized_text']]  # keep the url and normalized text 

    df.to_csv(output_csv, index=False, encoding='utf-8')  # creats a new csv file as the output of the function




# This function tokenize the normalized html
import nltk
from nltk.corpus import stopwords
import string
#nltk.download('punkt_tab') #: to uncomment if not already downloaded
#nltk.download('stopwords') #: to uncomment if not already downloaded

stop_words = list(set(stopwords.words('english'))) + ["'s"]
stem = nltk.stem.SnowballStemmer("english")

def tokenize_html(text):
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    tokens = [token for token in tokens if token not in string.punctuation]  # remove punctuation
    tokens = [token for token in tokens if token not in stop_words]  # remove stopwords
    # tokens = [stem.stem(token) for token in tokens]  # apply stemming (racinisation)
    return tokens



# Tokenizes the csv file created previously
def tokenize_csv_file(input_csv, output_csv):
    df = pd.read_csv(input_csv)  # Take the csv file with the normalized text as the input

    if 'normalized_text' not in df.columns:  # Verify that the normalized text colon exists
        raise ValueError(f"The normalized text is missing in: {input_csv}")

    df['tokenized_text'] = df['normalized_text'].apply(tokenize_html)  # cleans the html colon
    df = df[['url', 'tokenized_text']]  # keep the url and text colon (not the raw html)

    df.to_csv(output_csv, index=False, encoding='utf-8')  # creats a new csv file as the output of the function






#########################################################################################################################################################################




#Scrapping of the lifestyle page of Wikipedia

url_wiki = "https://en.wikipedia.org/wiki/Lifestyle"

soup = to_soup (url_wiki)

if not soup:
    print("Error: Could not fetch Wikipedia page:", url_wiki)
    exit()

links_wiki = []

wiki = soup.find_all('div', class_="mw-content-ltr mw-parser-output")  # Make sure that only the links related to the page lifestyle is scrapped

for div in wiki:
    for p in div.find_all('p'):
        for item in p.find_all('a', href = True):
            href = item.get('href')
            if href.startswith("/wiki/") and ":" not in href:
                links_wiki.append(urljoin(url_wiki, href))

see_also = soup.find_all('div', class_='div-col')  # Collection of links that are in the "see also" section of the page

for div in see_also :
    for li in div.find_all('li'):
        for item in li.find_all('a', href = True):
                href = item.get('href')
                full_url = urljoin(url_wiki, href)
                if href.startswith("/wiki/") and ":" not in href and full_url not in links_wiki and 'Market_segmentation' not in full_url:
                    links_wiki.append(full_url)

print(len(links_wiki), "wikipedia pages has been found")
print("Pages founded:", links_wiki[:1])





# Collection of the corpus of the Wikipedia pages

# Creates a csv file with the Wikipedia pages found previsously (raw html)
corpus = get_html_corpus(links_wiki[:1])
save_to_csv(corpus, "wikipedia_lifestyle_corpus.csv")


# The csv file is transform into a dataframe pandas to help us manipulate the table
import pandas as pd
df = pd.read_csv('wikipedia_lifestyle_corpus.csv')  # df is now a table 



links_wiki_total = ["https://en.wikipedia.org/wiki/Lifestyle"]  # start with the main wikipedia page

# add links
for link in links_wiki.values():
    links_wiki_total.extend(links)



cleaned_wiki_csv = clean_csv_file("wikipedia_lifestyle_corpus.csv", "cleaned_wikipedia_lifestyle_corpus.csv")

normalized_wiki_csv = normalize_csv_file("cleaned_wikipedia_lifestyle_corpus.csv", "normalized_wikipedia_lifestyle_corpus.csv")

tokenized_wiki_csv = tokenize_csv_file("normalized_wikipedia_lifestyle_corpus.csv", "tokenized_wikipedia_lifestyle_corpus.csv")








#########################################################################################################################################################################








# Scrapping of Feedspots

# Collection of the 100 blogs (and not just 95 : 5 were not foundable since there were not in the <a> part of the html)
url_blogs = "https://bloggers.feedspot.com/lifestyle_blogs/"

soup = to_soup(url_blogs)

if not soup:
    print("Error: Could not fetch main blogs page:", url_blogs)

blogs = soup.find_all(lambda tag: tag.name in ['a', 'span'] and tag.get('class') and 'wb-ba' in tag.get('class') and any('ext' in c for c in tag.get('class')))

links_blogs = []
for item in blogs:
    href = item.get('href') if item.name == 'a' else item.text.strip()
    if href and "http" in href and "bloggers.feedspot.com" not in href:  #Cela exclut les liens internes 
        links_blogs.append(href)

print(len(links_blogs), "blogs has been found")
print("Blogs founded:", links_blogs[:1])



# Collection of urls that are in the 100 blogs

def get_links_from_blog(url):
    soup = to_soup(url)
    if not soup:
        return None
    
    links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if not href:
            continue
        # gérer les liens relatifs (/about → https://blog.com/about)
        full_url = urljoin(url, href)
        if full_url.startswith("http") and full_url not in links:
            links.append(full_url)

    return links





# ATTENTION en fassant comme ça on se retrouve avec beacoup trop de liens, il faut absolument filtré plus donc une idée : filtrer en mettant les mots trouvés avec wikipedia comme mot à retrouver dans l'url :))

required_keywords = [
    "lifestyle"
]




links_in_blogs_1 = {}

total_new_urls_1 = 0

for url in links_blogs[:2]:
    print("\nLinks from the blog (first round):", url)

    links = get_links_from_blog(url)
    if links is None:
        print("→ 0 links found (scraping failed or blocked)")
        links_in_blogs_1[url] = []
        continue

    domain = urlparse(url).netloc
    filtered_links = filter_links(links, required_keywords=required_keywords, domain=domain, already_seen=set())

    links_in_blogs_1[url] = filtered_links

    total_new_urls_1 += len(filtered_links)

    print("→", len(filtered_links), "links found:", filtered_links[:1])

    time.sleep(random.uniform(1,4))

print("Total new URLs found in this first round iteration:", total_new_urls_1)



links_in_blogs_2 = {}
already_seen = set()

# URLs déjà vues au round 1
for url, links in links_in_blogs_1.items():
    already_seen.update(links)

total_new_urls_2 = 0

for blog_url, first_round_links in list(links_in_blogs_1.items())[:1]: #Limits the scrapping to the first blog
    print("\nBlog source:", blog_url)
    domain = urlparse(blog_url).netloc

    for page_url in first_round_links [:10]: #Limits the number of pages scraped within a blog page
        print("Links from page:", page_url)
        
        links = get_links_from_blog(page_url)

        if links is None:
            continue

        filtered_links = filter_links(links, required_keywords=required_keywords, domain=domain, already_seen=set())

        links_in_blogs_2[page_url] = filtered_links
        already_seen.update(filtered_links)
        total_new_urls_2 += len(filtered_links)

        if filtered_links:
            print("→", len(filtered_links), "links found:", filtered_links[:10])
        else:
            print("→ 0 links found")

        time.sleep(random.uniform(1,4))

print("\nTotal new URLs found in second round iteration:", total_new_urls_2)




# Creation of a single list composed of all the links collected (100 blogs + first round + second round)
links_blogs_total = links_blogs.copy()  # start with the main blogs list

# add first round links
for links in links_in_blogs_1.values():
    links_blogs_total.extend(links)

# add second round links
for links in links_in_blogs_2.values():
    links_blogs_total.extend(links)

print("Total unique links collected:", len(links_blogs_total))




# Check if a csv file is already created, if no, it creates one otherwise it doesn't
import os

if os.path.exists("blogs_corpus.csv"):
    df = pd.read_csv("blogs_corpus.csv")  # The csv file already exists
else:
    corpus = get_html_corpus(links_blogs_total[:10])  # The csv file doesn't exist yet
    save_to_csv(corpus, "blogs_corpus.csv")




# The csv file is transform into a dataframe pandas to help us manipulate the table
import pandas as pd
df = pd.read_csv('wikipedia_lifestyle_corpus.csv')  # df is now a table 


cleaned_blogs_csv = clean_csv_file("blogs_corpus.csv", "cleaned_blogs_corpus.csv")

normalized_blogs_csv = normalize_csv_file("cleaned_blogs_corpus.csv", "normalized_blogs_corpus.csv")

tokenized_blogs_csv = tokenize_csv_file("normalized_blogs_corpus.csv", "tokenized_blogs_corpus.csv")




