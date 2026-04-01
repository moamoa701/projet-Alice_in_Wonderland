# Project Bookworm - NLP Engine



## À propos du projet
Développé dans le cadre d'un projet Epitech, **Bookworm** est un moteur de traitement automatique du langage naturel (NLP) léger en ligne de commande. Il a été conçu pour la startup fictive "Through the Looking-Glass" afin d'aider les éditeurs à analyser rapidement le vaste catalogue littéraire de Project Gutenberg.

Le script `bookworm.py` transforme du texte brut en données structurées, générant des "fiches de lecture" automatiques sans avoir besoin de lire les œuvres entières. Il est optimisé pour utiliser des modèles légers et sauvegarder les calculs coûteux pour une exécution rapide.

## Fonctionnalités (CLI)
Le programme propose plusieurs commandes d'analyse sur une sélection de livres (Alice au Pays des Merveilles, Sherlock Holmes, Frankenstein, etc.):

* **`--lexdiv <ID>` (Diversité Lexicale) :** Calcule la richesse du vocabulaire d'un livre (nombre de mots, mots uniques, hapax, ratio TTR, longueur moyenne des mots) pour analyser le style linguistique.
* **`--topics <ID>` (Modélisation de thématiques) :** Extrait les 10 mots principaux par section pour identifier les thèmes majeurs de l'œuvre.
* **`--entities <ID>` (Reconnaissance d'Entités Nommées - NER) :** Identifie automatiquement les personnages et les lieux mentionnés pour faciliter la création de cartes de personnages.
* **`--summarize <ID>` (Résumé) :** Condense le livre en un court résumé de quelques phrases.
* **`--similar <ID>` (Recommandation) :** Compare les livres (via similarité cosinus) pour identifier les ressemblances thématiques ou stylistiques, et retourne les 5 livres les plus proches.
* **`--card <ID>` (Fiche complète) :** Compile toutes les analyses précédentes (métadonnées, entités, sujets, résumé, similarité) dans un dictionnaire global structuré.

## Installation & Utilisation

1. **Cloner le dépôt :**
   ```bash
   git clone git@github.com:moamoa701/projet-Alice_in_Wonderland.git
   cd Projet-Bookworm

2. **Générer la fiche de l'id 11**
python3 bookworm.py --card 11
