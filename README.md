# Projet Web Mining — Analyse des blogs d'expertise

## Contexte
Ce projet explore et analyse le contenu des blogs de niche dans le domaine du Lifestyle (bien-être, nutrition, sport ...).  Le secteur du Lifestyle se distingue par la production régulière de contenus textuels longs et par une structure de réseau dense (citations, recommandations).
Ce projet a été réalisé dans le cadre du cours de Web Mining et vise donc à appliquer les techniques d'extraction, de traitement de texte et d'analyse de données vues en classe. L'objectif est d'extraire des tendances, des thématiques dominantes et des indicateurs de crédibilité ou d'influence depuis nos différentes sources.

Notre approche compare deux visions :
  1. **Théorique** : Corpus Wikipédia, définissant les concepts du domaine.
  2. **Pratique** : Corpus de blogs spécialisés (ex: "MindBodyGreen"), représentant l'usage réel, les tendances et le vocabulaire des communautés passionnées.

## Objectifs
L'objectif est de comprendre comment ce micro-univers se structure sémantiquement et techniquement à travers quatre axes :
1. **Data Collection (scraping)** : Collecter un corpus représentatif de blogs d'expertise dans le domaine ciblé en appliquant des techniques d'extraction web contrôlées (crawling, filtrage des pages non-pertinentes, normalisation des données).
2. **Text Mining** : Appliquer des techniques de prétraitement linguistique, d'extraction de texte et d'analyse sémantique pour identifier les patterns récurrents, les mots-clés stratégiques et comparer le vocabulaire théorique vs pratique.
3. **Link Analysis** : Cartographier la structure du réseau hypertextuel entre blogs pour détecter les noeuds d'influence (Hubs), les pages intermédiaires (Bridges) et mesurer la centralité des contenus via des algorithmes de graphes.
4. **Correlation (Structure-sémantique)** : Mettre en relation l'importance sémantique d'un thème (poids TF-IDF, statistiques) avec l'importance structurelle des pages qui le traitent (PageRank, Centralité).

## Environnement
Environnement de développement :
- **Langage** : Python
- **Bibliothèques clés** : BeautifulSoup, pandas, scikit-learn, nltk, spacy
- **Expérimentation** : Jupyter Notebook
- **Éditeur** : Visual Studio Code
- **Versioning** : Git et GitHub

## Technologies et Méthodologie
Le projet suit un pipeline de données complet :
1. **Collecte** (\data) :
  - Scraping : BeautifulSoup, Requests, Regex.
  - Stratégie : Exploration BFS (Breadth-First Search) pour une exploration par couches des blogs avec des filtres pour réduire le bruit. Parsing immédiat des dates (parsing ISO/formats textuels).
2. **Prétraitement (NLP)** : 
  - Outils : NLTK, Spacy
  - Traitement : Nettoyage HTML, Tokenisation, Suppression des Stopwords, Lemmatisation (WordNetLemmatizer) préférée au Stemming pour préserver l'interprétabilité des thèmes.
3. **Modélisation (Text Mining)** :
  - Vectorisation : TF-IDF (scikit-learn)
  - Topic Modeling : LDA (Latent Dirichlet Allocation) pour une modélisation globale et BERTopic pour une analyse fine via embeddings contextuels (Deep Learning).
4. **Analyse de Graphe (Link Analysis)** : 
  - Outils : ???NetworkX???
  - Métriques : PageRank, Centralité de degré (Degree) et d'intermédiarité (Betweenness) et Shortest Path pour l'analyse de la circulation de l'information. 

## Structure du projet
```bash
├── data/                  # Données brutes (HTML) et CSV nettoyés
├── notebooks/             # Jupyter Notebooks d'expérimentation
│   ├── 1_Scraping.ipynb   # Scripts de collecte (Wiki + Blogs)
│   ├── 2_Preprocessing.ipynb # Nettoyage et tokenisation
│   ├── 3_TextMining.ipynb # LDA, BERTopic, Visualisations
│   └── 4_LinkAnalysis.ipynb # PageRank, Centralités
├── src/                   # Scripts Python modularisés
├── requirements.txt       # Dépendances
└── README.md              # Documentation
``` 

## Auteur.es
**Violaine GUILLAUME** — **Eurydice HANOT** — **Arshik MEHMETAJ**   
Louvain School of Management - Master in Business Analytics

---

> Ce dépôt est privé et destiné à un usage pédagogique. Toute reproduction ou diffusion non autorisée est interdite.
