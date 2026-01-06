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

## Structure du projet
''' bash
├── data/                               # Données brutes et nettoyées
├── Data_Collection_Jupyter_Lab/        # Jupyter Notebooks
│   ├── 1_Data_Collection.ipynb         # Scraping (Wikipedia, Blogs, Feedspot)
│   ├── 2_Text_Mining.ipynb             # Prétraitement + analyse textuelle
│   ├── 3_Link_Analysis.ipynb           # Construction des graphes + analyse des liens
│   └── 4_Centrality_PageRank.ipynb     # PageRank, centralités, homophilie
├── src/                                # Scripts Python modularisés
├── requirements.txt                    # Dépendances
└── README.md                           # Documentation du projet
'''


## Auteur.es
**Violaine GUILLAUME** — **Eurydice HANOT** — **Arshik MEHMETAJ**   
Louvain School of Management - Master in Business Analytics

---

> Ce dépôt est privé et destiné à un usage pédagogique. Toute reproduction ou diffusion non autorisée est interdite.
