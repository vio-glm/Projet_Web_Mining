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