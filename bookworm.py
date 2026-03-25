import requests
import re
import math
import argparse
import spacy
from collections import Counter, defaultdict
from cache_manager import load_cache, save_cache


#url = "https://www.gutenberg.org/"
#response = requests.get(url)

BASE_URL = "https://www.gutenberg.org/files/{id}/{id}-0.txt"


def download_book(book_id):
    url = BASE_URL.format(id=book_id)
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Error downloading book {book_id}")

    return response.text

# Cleans the downloaded text
def clean_gutenberg_text(text):
    """
    Permet de nettoyer le texte téléchargé en enlevant les textes inutiles (licence Gutenberg)
    
    """
    
    #on stock l'index, la position ou commence le texte
    start = text.find("*** START OF")
    #on stopck l'index, la position ou termine le texte
    end = text.find("*** END OF")
    
    #si find() trouve -1, donc na pas trouves start of, end of ,alors on garde tout le texte (avec licence...) et on retourne le text
    if start == -1 or end == -1:
        return text

    #on garde uniquement le texte entre l'index start et l'index end
    #on crée une liste ou chaque élément est une ligne du livre
    #on retire la balise (ligne 0)    
    clean_text = text[start:end].splitlines()[1:]
    #on ajoute des sauts de lignes 
    return "\n".join(clean_text)


def fetch_book(book_id):
    """
    Télécharge un livre grace à son ID ou le lit depuis le cache
    
    """
    
    #on vérifie dans le catch
    cached_text = load_cache("raw_text", book_id)
    if cached_text:
        print(f"Livre {book_id} récupéré depuis le cache!")
        return cached_text

    #si le cache a pas trouvé, on telecharge le livre
    print(f"Téléchargement du livre {book_id} depuis Internet")

    #url pour avoir le format .txt du livre
    url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"
    
    response = requests.get(url)
    
    #si le site repond code 200, on stock le text dans raw_text
    if response.status_code == 200:
        raw_text = response.text
        
        #nettoyage du texte 
        clean_text = clean_gutenberg_text(raw_text)
        
        #sauvegarde dans le cache
        save_cache("raw_text", book_id, clean_text)
        
        return clean_text
    else:
        print(f"Erreur : Impossible de trouver le livre avec l'ID {book_id}")

        return None

def main():
    """
    Mise en place du CLI :
    -lit les arguments utilisateur
    -appelle les fonctions correspondantes
    -affiche les résultats
    """


def tokenize(text):
    text = text.lower()
    words = re.findall(r"\b[a-z']+\b", text)
    return words


# Lexical diversity

def lexical_diversity(book_id, text):
    cached = load_cache("lexdiv", book_id)
    if cached:
        return cached

    tokens = tokenize(text)
    tok = len(tokens)

    counts = Counter(tokens)
    typ = len(counts)
    hap = sum(1 for w in counts if counts[w] == 1)

    ttr = typ / tok if tok else 0
    mwl = sum(len(w) for w in tokens) / tok if tok else 0
    mwf = tok / typ if typ else 0

    result = {
        "tok": tok,
        "typ": typ,
        "hap": hap,
        "ttr": ttr,
        "mwl": mwl,
        "mwf": mwf
    }

    save_cache("lexdiv", book_id, result)
    return result


def summarize_book(book_id, text, n_sentences=5):
    """
    Returns a short extractive summary of the book.
    Uses sentence scoring based on word frequency.
    """
    cached = load_cache("summary", book_id)
    if cached:
        return cached
    #Sentence segmentation
    sentences = re.split(r'(?<=[.!?]) +', text)

    #Avoid extremely long texts (performance)
    sentences = sentences[:2000]

    words = tokenize(text)

    #Compute word frequencies
    freq = Counter(words)

    # Normalize frequencies
    max_freq = max(freq.values()) if freq else 1
    for word in freq:
        freq[word] /= max_freq

    #Score sentences
    sentence_scores = defaultdict(float)

    for sent in sentences:
        sent_words = tokenize(sent)
        # Ignore very short or very long sentences
        if len(sent_words) < 5 or len(sent_words) > 40:
            continue
        for word in sent_words:
            if word in freq:
                sentence_scores[sent] += freq[word]

    #Select top sentences
    best_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:n_sentences]

    # Keep original order
    best_sentences = sorted(best_sentences, key=lambda s: sentences.index(s))

    summary = " ".join(best_sentences)

    save_cache("summary", book_id, summary)

    return summary


def extract_entities(book_id, text):
    """
    Recupere les noms de personnages et lieux du livre
    
    """
    #id en string pour pouvoir appeler
    book_id = str(book_id)


    cached = load_cache("entities", book_id)
    if cached:
        return cached

    print("Chargement de spaCy en cours...")
    
    #chargement de l'ia small spacy + desactivation des truc inutiles 
    try:
        nlp = spacy.load("en_core_web_sm", disable=["tagger", "parser", "lemmatizer"])

    #gestion des erreurs
    except OSError:
        print("Erreur : Modele pas trouvé ")
        return {"characters": [], "locations": []}

    #ajoute a spacy un rajout de 100k caractere en + de la longueur du texte
    nlp.max_length = len(text) + 100000

    print("Analyse du texte...")

    #traite par morceaux de 50 000 caractères et le stock dans docs
    docs = list(nlp.pipe([text[i:i+50000] for i in range(0, len(text), 50000)]))

    
    #création de compteur
    compteur_personnages = Counter()
    compteur_lieux = Counter()
    
    #parcours les entité trouvé de spacy
    for doc in docs:
        for ent in doc.ents:
            mot_propre = ent.text.replace('\n', ' ').strip()
            if ent.label_ == "PERSON":
                compteur_personnages[mot_propre] += 1
            elif ent.label_ in ["GPE", "LOC", "FAC"]:
                compteur_lieux[mot_propre] += 1

    #stock les 20 mots les plus fréquents  dans characters et locations
    characters = [mot for mot, freq in compteur_personnages.most_common(20)]
    locations = [mot for mot, freq in compteur_lieux.most_common(20)]

    #stock les mots les plus fréquent dans le dictionnaire resultats
    resultats = {
        "characters": characters,
        "locations": locations 
    }

    #Sauvegarde dans le cache
    save_cache("entities", book_id, resultats)

    return resultats

def main():
    """
    Mise en place du CLI :
    -lit les arguments utilisateur
    -appelle les fonctions correspondantes
    -affiche les résultats
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("--lexdiv", type=int)
    parser.add_argument("--entities", type=str)

    args = parser.parse_args()

    if args.lexdiv:
        book_id = args.lexdiv
        text = fetch_book(book_id)
        if text:
            stats = lexical_diversity(book_id, text)
            print(f"\n Résultat: {book_id} :")
        print(stats)

    if args.entities:   
        book_id = args.entities
        text = fetch_book(book_id)
        if text:
            entities_dict = extract_entities(book_id, text)
            print(f"\n entités trouvées pour le livre: {book_id} :") 
            print(entities_dict)

        
#permet d'exécuter la fonction main() uniquement si le fichier est lancé directement
if __name__ == "__main__":
    main()
