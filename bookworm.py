import requests
#nos fonctions:
from cache_manager import load_cache, save_cache 

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

    #on garde uniquement le texte entre lindex start et lindex end
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