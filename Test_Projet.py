# Package importation
import requests
from bs4 import BeautifulSoup
import os


# Useful Fonctions

# get the url
def fetch_verify_url(url) :
    # ici on met requests.get dans une fonction
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}  
        response = requests.get(url, headers=headers)
        if response.status_code != 200:  # si pas OK
            return None
        return response  # HTML brut
    except requests.RequestException:
        return None

def to_soup(url):
    response = fetch_verify_url(url)
    if response:
        return BeautifulSoup(response.text, 'html.parser')  # correction du parser
    else:
        return None


# Scrapping of Feedspots

# Collection of the 100 blogs (and not just 95 : 5 were not foundable since there were not in the <a> part of the html)
url_blogs = "https://bloggers.feedspot.com/lifestyle_blogs/"

soup = to_soup(url_blogs)

blogs = soup.find_all(lambda tag: tag.name in ['a', 'span'] 
                      and tag.get('class') 
                      and 'wb-ba' in tag.get('class') 
                      and any('ext' in c for c in tag.get('class')))

links_blogs = []
for item in blogs:
    href = item.get('href') if item.name == 'a' else item.text.strip()
    if href and "http" in href and "bloggers.feedspot.com" not in href:  #Cela exclut les liens internes (ce qui est correct si tu veux juste les blogs externes)
        links_blogs.append(href)

print(len(links_blogs), "blogs has been found")
print("Blogs founded:", links_blogs[:1])


# Collection of urls that are in the 100 blogs

def get_links_from_blog(url, headers):
    
    soup = to_soup(url)

    links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if not href:
            continue
        # gérer les liens relatifs (/about → https://blog.com/about)
        full_url = urljoin(blog_url, href)
        if full_url.startswith("http") and full_url not in links:
            links.append(full_url)

    return links


all_links = {}

for url in links_blogs[:2]:  # scrappe les x premiers blogs et retourne le nombre de lien trouvé sur la page d'accueil et les 5 premiers liens
    print("\nLinks from the blog:", url)

    links = get_links_from_blog(url, headers)
    all_links[blog_url] = links

    print("→", len(links), "liens trouvés :", links[:1])

    # ⏱️ pause entre chaque requête (IMPORTANT)
    time.sleep(1)

# Attention on prend les liens de la première page 




"""
import requests

r = requests.get("https://www.poppyloves.co.uk/")

print(r.status_code)
"""

"""
#Si tu veux qu'il donne le status_code d'une manière plus stylé

if r.status_code == 200:
    print("Sucess !")
else:
    print("Error in getting the url, error =", r.status_code)
"""

"""
print(r.encoding) #Détecte l'encodage de la page html (dans l'idéal c'est "utf-8".) Pour forcer l'encodage on ajoute r.encoding = "utf-8". Requests va décoder les octets en texte avec cet encodage.
#.encoding = la clé qui dit à Requests comment lire la page. Cela influence le r.text.
"""

"""
print(r.content)
print(r.headers) #donne des infos sur les metadonnées de la page
"""
"""
print(r.text[:200]) #imprime les 200 premiers charachtéres de la page html
"""
"""
from bs4 import BeautifulSoup
# Open and parse the HTML file
soup = BeautifulSoup(r.text, 'html.parser')
title = soup.find("title")
print(title.text)
"""






#Importation des url des 100 (/96) blogs de la base de données https://bloggers.feedspot.com/lifestyle_blogs/?_src=bloggers_directory_l

import requests
from bs4 import BeautifulSoup
    
url_blogs = "https://bloggers.feedspot.com/lifestyle_blogs/"

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}  # Header pour simuler un navigateur

response_blogs = requests.get(url_blogs, headers=headers)

if response_blogs.status_code == 200:
    print(response_blogs.status_code)
    soup = BeautifulSoup(response_blogs.text, "html.parser")
else:
    print("Erreur lors du téléchargement:", response_blogs.status_code)

blogs = soup.find_all('a', class_='ext text-blue wb-ba')
links_blogs = []
for item in blogs:
    href = item.get("href")
    if "http" in href and "bloggers.feedspot.com" not in href:  #Cela exclut les liens internes (ce qui est correct si tu veux juste les blogs externes)
        links_blogs.append(href)

print(len(links_blogs))
print(links_blogs[:5])




# Importation des urls des blogs trouvés plutôt

import time
from urllib.parse import urljoin


def get_all_links_from_blog(blog_url, headers):
    try:
        response = requests.get(blog_url, headers=headers, timeout=10)
    except requests.exceptions.RequestException:
        print("⛔ Erreur de connexion :", blog_url)
        return []

    if response.status_code != 200:
        print("⛔ Bloqué ou erreur :", blog_url, response.status_code)
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if not href:
            continue
        # 🌐 gérer les liens relatifs (/about → https://blog.com/about)
        full_url = urljoin(blog_url, href)
        if full_url.startswith("http") and full_url not in links:
            links.append(full_url)

    return links


all_links = {}

for blog_url in links_blogs[:20]:  # scrappe les x premiers blogs et retourne le nombre de lien trouvé sur la page d'accueil et les 5 premiers liens
    print("\nLinks from the blog:", blog_url)

    links = get_all_links_from_blog(blog_url, headers)
    all_links[blog_url] = links

    print("→", len(links), "liens trouvés :", links[:1])

    # ⏱️ pause entre chaque requête (IMPORTANT)
    time.sleep(1)

# Attention on prend les liens de la première page 



"""
# Stock les liens dans un fichier csv

import csv

edges = []  # liste des (source, target)

for blog_url in links_blogs[:1]:  # limite pour tester
    print("\nScraping blog:", blog_url)

    links = get_all_links_from_blog(blog_url, headers)

    for link in links:
        edges.append((blog_url, link))  # PRÉDÉCESSEUR → LIEN

    time.sleep(1)  # ⏱️ pause obligatoire

with open("links_graph.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["source", "target"])  # colonnes standard graphes
    writer.writerows(edges)

import os
print("CSV (links_graph.csv) créé ici :", os.getcwd())  # nous dit où est stocké ce fichier
"""



"""
# Obtenir le corpus des blogs
import requests
from bs4 import BeautifulSoup
import time


def get_blog_text(blog_url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(blog_url, headers=headers)
    if response.status_code != 200:
        print("Erreur")
        return ""
    soup = BeautifulSoup(response.text, "html.parser")

    # Récupérer le titre principal (souvent dans <h1>)
    title = soup.find('title')
    if title:
        title_text = title.get_text(strip=True)
    else:
        title_text = blog_url  # fallback si pas de <h1>

    # Récupérer les paragraphes (<p>)
    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p') if p.get_text(strip=True)]
    
    # Structurer l'info dans un dictionnaire
    return {"title": title_text, "paragraphs": paragraphs}

"""
""" 
Sans les prints de tous les paragraphes, ...
corpus_blogs = {}
for blog_url in links_blogs:
    corpus = get_blog_text(blog_url)
    corpus_blogs[blog_url] = corpus
    
    print(f"Nombre de blogs traités : {len(corpus_blogs)}")
"""


"""
blog_text = {}

for blog_url in links_blogs[:1]:  # scrappe les 2 premiers blogs et retourne le nombre de lien trouvé sur la page d'accueil et les 5 premiers liens
    print("\nText from the blog:", blog_url)

    structured = get_blog_text(blog_url)
    blog_text[blog_url] = structured

    print("Titre:", structured["title"])
    print("Nombre de paragraphes:", len(structured["paragraphs"]))
    print("Premier paragraphe:", structured["paragraphs"][0] if structured["paragraphs"] else "Aucun")
    
    # Afficher chaque paragraphe avec son numéro
    for i, para in enumerate(structured["paragraphs"][:5], start=1):
        print(f"Paragraphe n°{i} : {para}")
    
    # pause entre chaque requête (IMPORTANT)
    time.sleep(1)

"""


"""
# Normalisation du texte
import re

def clean_text(text): # Archik a d'autres filtre
 
    text = text.lower()  # tout en minuscules
    text = re.sub(r'[^a-zà-ÿ0-9\s]', ' ', text)  # lettres, chiffres, espaces
    text = re.sub(r'\s+', ' ', text)  # espaces multiples -> 1 espace
    return text.strip()



# Tokenisation filtrée
import nltk
from collections import Counter
nltk.download('stopwords')
from nltk.corpus import stopwords

english_stopwords = set(stopwords.words('english'))

def tokenize_filtered(text, stopwords=None, min_freq=3):

    # Tokenization
    tokens = text.split()
    
    # Filtrage stopwords
    if stopwords:
        tokens = [t for t in tokens if t not in stopwords]

    # Filtrage par fréquence
    counter = Counter(tokens)
    tokens = [t for t in tokens if counter[t] >= min_freq]
    
    return tokens



corpus_tokens = {}

for blog_url in links_blogs[:1]:  # limiter pour tester
    print("\nTraitement du blog :", blog_url)
    
    structured = get_blog_text(blog_url)
    full_text = structured["title"] + " " + " ".join(structured["paragraphs"])
    
    # Normalisation
    cleaned_text = clean_text(full_text)
    
    # Tokenization avec filtres
    tokens = tokenize_filtered(cleaned_text, stopwords=english_stopwords, min_freq=5)
    
    corpus_tokens[blog_url] = tokens
    
    print("Nombre de tokens :", len(tokens))
    print("Exemple de tokens :", tokens[:20])
    
    time.sleep(1)
"""








"""
#Importation liens de la page Lifestyle de Wikipedia

import requests
from bs4 import BeautifulSoup

url_wiki = "https://en.wikipedia.org/wiki/Lifestyle"

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}  # Header pour simuler un navigateur

response_wiki = requests.get(url_wiki, headers=headers)

soup= BeautifulSoup(response_wiki.text, 'html.parser')

if response_wiki.status_code == 200:
    print(response_wiki.status_code)
    soup = BeautifulSoup(response_wiki.text, "html.parser")
else:
    print("Erreur lors du téléchargement:", response_wiki.status_code)

wiki = soup.find_all('a', href = True)
links_wiki = []
for item in wiki:
    href = item.get("href")
    if "http" in href: 
        links_wiki.append(href)

print(len(links_wiki))
print(links_wiki[:5])
"""


"""
# --------------------------------------------------
# Étape 2 : visiter chaque lien et extraire les infos
# --------------------------------------------------
data = []

for i, link in enumerate(wiki_links, 1):
    print(f"\n[{i}/{len(wiki_links)}] Scraping : {link}")
    try:
        time.sleep(1)  # pause pour rester poli
        res = requests.get(link, headers=headers, timeout=10)
        if res.status_code != 200:
            print(f"Erreur {res.status_code} sur {link}")
            continue

        page_soup = BeautifulSoup(res.text, 'html.parser')

        # Récupérer le titre de la page
        title = page_soup.title.string.strip() if page_soup.title else ""

        # Récupérer les 3 premiers paragraphes
        paragraphs = [p.get_text(strip=True) for p in page_soup.find_all('p')[:3]]
        text = "\n".join(paragraphs)

        # Récupérer tous les liens internes et externes
        page_links = [urljoin(link, a['href']) for a in page_soup.find_all('a', href=True)]

        # Ajouter au dataset
        data.append({
            "url": link,
            "title": title,
            "text": text,
            "links": page_links
        })

        print(f"✅ Page scrapée : {title}")

    except Exception as e:
        print(f"❌ Erreur sur {link} : {e}")

"""

"""
# --------------------------------------------------
# Étape 3 : enregistrer les données dans un CSV
# --------------------------------------------------
with open("wikipedia_external_pages.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["url", "title", "text", "links"])
    writer.writeheader()
    for row in data:
        # Les liens sont convertis en chaîne de caractères séparés par ;
        row["links"] = "; ".join(row["links"])
        writer.writerow(row)

print("\n🎉 FIN DU SCRAPING – données enregistrées dans wikipedia_external_pages.csv")
"""




















"""
# Scrap pinterest : recolte les images
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://www.pinterest.com/search/pins/?q=lifestyle&rs=typed")

time.sleep(5)  # laisser charger le JS

pins = driver.find_elements(By.TAG_NAME, "img")

for pin in pins[:1]:
    print(pin.get_attribute("src"))

driver.quit()
"""


"""
❌ Ce pour quoi Selenium n’est PAS fait (mais souvent utilisé)
🚫 Scraper des plateformes fermées

Réseaux sociaux (Pinterest, Instagram, LinkedIn),

Sites avec login obligatoire,

Sites qui bloquent les bots.

👉 Là, Selenium simule un humain pour contourner des protections.

➡️ Techniquement possible
➡️ Méthodologiquement et légalement problématique
"""


"""

# Scrap Pinterest : recolte les url des pins trouvables sur la page lifestyle de pinterest 
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Lancer Chrome (Selenium)
driver = webdriver.Chrome()
driver.get("https://www.pinterest.com/search/pins/?q=lifestyle")

# Attendre le chargement JS
time.sleep(5)

# Collecter les pins visibles (limité à 10)
pins = driver.find_elements(By.CSS_SELECTOR, "div[data-test-id='pin']")[:10]

data = []

for pin in pins:
    try:
        title = pin.get_attribute("aria-label")  # Pinterest stocke souvent le texte dans aria-label
        link = pin.find_element(By.TAG_NAME, "a").get_attribute("href")
        data.append({"title": title, "link": link})
    except:
        continue

driver.quit()

# Sauvegarder dans CSV
df = pd.DataFrame(data)
df.to_csv("pinterest_topics.csv", index=False)
print("Données Pinterest enregistrées :", df)
"""



"""
# Scrap Pinterest : récolte les URL et le texte des pins trouvables sur la page lifestyle
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Lancer Chrome (Selenium)
driver = webdriver.Chrome()
driver.get("https://www.pinterest.com/search/pins/?q=lifestyle")

# Attendre le chargement JS
time.sleep(5)

# Collecter les pins visibles (limité à 10)
pins = driver.find_elements(By.CSS_SELECTOR, "div[data-test-id='pin']")[:5]

data = []

for pin in pins:
    try:
        # Titre principal
        title = pin.get_attribute("aria-label")  

        # Lien vers le pin
        link = pin.find_element(By.TAG_NAME, "a").get_attribute("href")
        
        # Texte / description secondaire (si présent)
        try:
            desc_element = pin.find_element(By.CSS_SELECTOR, "div[data-test-id='pin-description']")
            description = desc_element.text
        except:
            description = ""  # Pas de description disponible

        data.append({
            "title": title,
            "link": link,
            "description": description
        })
    except:
        continue

driver.quit()

# Sauvegarder dans CSV
df = pd.DataFrame(data)
df.to_csv("pinterest_topics.csv", index=False)
print("Données Pinterest enregistrées :", df)
"""





"""
#Scrap Pinterest pour récupérer les liens et descriptions des pins.
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

def scrap_pinterest(search_url, num_pins=5, csv_file="pinterest_topics.csv"):
    
    # Lancer Chrome
    driver = webdriver.Chrome()
    driver.get(search_url)
    
    # Attendre le chargement JS
    time.sleep(5)
    
    # Étape 1 : récupérer les liens des pins visibles
    pins = driver.find_elements(By.CSS_SELECTOR, "div[data-test-id='pin']")[:num_pins]
    links = []
    for pin in pins:
        try:
            link = pin.find_element(By.TAG_NAME, "a").get_attribute("href")
            links.append(link)
        except:
            continue
    
    # Étape 2 : visiter chaque lien et récupérer la description
    data = []
    for link in links:
        driver.get(link)
        time.sleep(3)
        try:
            description = driver.find_element(By.CSS_SELECTOR, "div[data-test-id='pin-description']").text
        except:
            description = ""
        data.append({"link": link, "description": description})
    
    driver.quit()
    
    # Créer DataFrame et sauvegarder CSV
    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)
    print(f"Données Pinterest enregistrées dans {csv_file}")
    
    return df

# Exemple d'utilisation
url = "https://www.pinterest.com/search/pins/?q=lifestyle"
df_pins = scrap_pinterest(url, num_pins=5)
print(df_pins)
"""


"""
#     Scrap Pinterest pour récupérer les liens externes des pins.
    Ne garde que les liens qui ne contiennent pas 'pinterest'.
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

def scrap_pinterest_external_links(search_url, num_pins=5, csv_file="pinterest_external_links.csv"):

    driver = webdriver.Chrome()
    driver.get(search_url)
    time.sleep(5)  # attendre le JS

    # Récupérer les liens des pins visibles
    pins = driver.find_elements(By.CSS_SELECTOR, "div[data-test-id='pin']")[:num_pins]
    pin_links = []
    for pin in pins:
        try:
            link = pin.find_element(By.TAG_NAME, "a").get_attribute("href")
            pin_links.append(link)
        except:
            continue

    data = []
    for link in pin_links:
        driver.get(link)
        time.sleep(3)  # attendre le chargement complet
        
        # Chercher tous les liens de la page
        try:
            a_tags = driver.find_elements(By.TAG_NAME, "a")
            external_link = ""
            for a in a_tags:
                href = a.get_attribute("href")
                if href and "pinterest" not in href:
                    external_link = href
                    break  # prendre le premier lien externe trouvé
        except:
            external_link = ""
        
        data.append({
            "pin_link": link,
            "external_link": external_link
        })
    
    driver.quit()

    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)
    print(f"Données enregistrées dans {csv_file}")
    return df

# Exemple d'utilisation
search_url = "https://www.pinterest.com/search/pins/?q=lifestyle&rs=rs&source_id=rs_RDVlqATG&top_pin_ids=8233211816862608&eq=&etslf=1451"
df = scrap_pinterest_external_links(search_url, num_pins=25)
print(df)
"""





# Scrap Pinterest : récupère les URLs des pins et le texte disponible dans l'attribut 'alt' des images MAIS ne récupère qu'une partie du texte :(())
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import pandas as pd

def scrap_pinterest_pins(search_url, num_pins=5, csv_file="pinterest_pins_alt_text.csv"):
    """
    Scrap Pinterest : récupère les URLs des pins et le texte disponible dans l'attribut 'alt' des images
    """
    driver = webdriver.Chrome()
    driver.get(search_url)
    time.sleep(5)  # attendre le JS

    # Récupérer les pins visibles
    pins = driver.find_elements(By.CSS_SELECTOR, "div[data-test-id='pin']")[:num_pins]

    data = []

    for pin in pins:
        try:
            pin_link = pin.find_element(By.TAG_NAME, "a").get_attribute("href")
            img = pin.find_element(By.TAG_NAME, "img")
            alt_text = img.get_attribute("alt")  # texte disponible (souvent tronqué)
            
            data.append({
                "pin_link": pin_link,
                "alt_text": alt_text
            })
        except Exception as e:
            print(f"Erreur sur un pin :", e)
            continue

    driver.quit()

    # Sauvegarder les résultats
    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)
    print(f"Données enregistrées dans {csv_file}")
    return df

# Exemple d'utilisation
search_url = "https://www.pinterest.com/search/pins/?q=lifestyle"
df = scrap_pinterest_pins(search_url, num_pins=5)
print(df)


