import os
import json
import hashlib
from functools import wraps

#stock .cache 
CACHE_DIR = ".cache"

def setup_cache():
    """
    Création du dossier de cache s'il n'existe pas

    """

    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

def cache_result(func):
    """
    Sauvegarde les resultats sur le disque, si une fonction a besoin de lire
    certains resultats deja calculée alors il check direct dans le cache sans faire recalculer

    """

    @wraps(func) #conservation de l'identité de la fonction
    def wrapper(*args, **kwargs): #adaptation a toutes les fonctions 
        setup_cache() #verification de l'éxistence du dossier cache et le crée si il nexiste pas
        
        #gestions des sauvegardes dans le .cache
        #key_string stock la fonction qui est utilisé et sur quel livre
        key_string = f"{func.__name__}_{args}_{kwargs}"
        #cache_key = utilise le resultat de keystring hashé pour nommé le fichier 
        cache_key = hashlib.md5(key_string.encode('utf-8')).hexdigest()
        #range les fichiers convertis en .json dans le .cache
        cache_file = os.path.join(CACHE_DIR, f"{cache_key}.json")

        #vérification de l'existence du fichier
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)

            #gestion des erreurs        
            except (json.JSONDecodeError, IOError):
                pass

        #si cache nexiste pas, on lance la fonction de l'user
        result = func(*args, **kwargs)

        #on sauvegarde et converti le résultat en .json pour la prochaine fois
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                #converti en .json 
                json.dump(result, f, ensure_ascii=False, indent=4)
        #gestion des erreurs        
        except IOError as e:
            print(f"Erreur lors de la sauvegarde du cache : {e}")

        return result
    return wrapper