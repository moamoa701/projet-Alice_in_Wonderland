import os
import json
import hashlib

#attribution de .cache 
CACHE_DIR = ".cache"

def setup_cache():
    """
    Création du dossier .cache s'il n'existe pas.

    """
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

def get_cache_path(action, book_id):
    """
    Fabrication du chemin du fichier de sauvegarde.

    """

    #création du nom (action + livre) 
    tag = f"{action}_{book_id}"
    
    #hashage de l'étiquette pour avoir un nom de fichier propre (pas de '/')
    safe_name = hashlib.md5(tag.encode('utf-8')).hexdigest()
    
    #on retourne le chemin complet 
    return os.path.join(CACHE_DIR, f"{safe_name}.json")

def load_cache(action, book_id):
    """
    Vérifie si le calcul a déjà été réalisé et le renvoie, et renvoie rien si il n'a rien trouvée
  
    """

    filepath = get_cache_path(action, book_id)
    
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                #on retourne le fichier trouvé
                return json.load(f) 
        #gestion des erreurs        
        except (json.JSONDecodeError, IOError):
            pass 
    #on retourne rien si on a pas trouvé le fichier        
    return None

def save_cache(action, book_id, data):
    """
    Sauvegarde le résultat dans un fichier JSON pour la prochaine fois.
    """
    #on crée le fichier .cache si il existe pas 
    setup_cache() 
    filepath = get_cache_path(action, book_id)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            #gestion des erreurs
    except IOError as e:
        print(f"Erreur lors de la sauvegarde du cache : {e}")