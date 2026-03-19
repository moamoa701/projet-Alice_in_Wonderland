#importation de nos fonctions
from cache_manager import load_cache, save_cache

def compute_lexical_stats(text, book_id):
    """
    Calcule tok(nb total de mot), typ(nb de mot compté qu'une fois), hap(nb de mot qui apparait uniquement une fois) d'un texte
    
    """
    
    #vérification si le calcul n'a pas déja était réalisé une fois 
    cached_stats = load_cache("stats", book_id)
    if cached_stats:
        print(f"Statistiques du livre {book_id} disponible dans le cache")
        return cached_stats

    print(f"Calcul des statistiques pour le livre {book_id} en cours...")
    
    #Cleaning pour le comptage
    #tout en minuscule pour compté les mots
    text_minuscule = text.lower()
    
    #coupage du texte a chaque espace et création de la liste stoclé dans mots
    mots = text_minuscule.split()
    
    #supprimation des ponctuations aux extremité collées aux mots 
    mots_propres = [mot.strip(".,!?;:()\"'") for mot in mots]

    #on retire les mots vides    
    mots_propres = [mot for mot in mots_propres if mot != ""]

    
    #comptage
    #tok: nb total de mots
    tok = len(mots_propres) 
    
    #dictionnaire pour le comptage
    compteur_mots = {}

    #on vérifie si le mot est déja dans le dictionnaire 
    for mot in mots_propres:
        if mot in compteur_mots:
            #si oui, on incrémente de 1
            compteur_mots[mot] += 1
        else:
            #si non, on lui donne la valeur 1
            compteur_mots[mot] = 1
            
    #typ: nombre de mot compté une fois (dict clean tout seul)      
    typ = len(compteur_mots) 
    
    #hap: compteur de mot uniquement égal a 1
    #initialise hap a 0
    hap = 0

    #on retourne les paires du dict
    for mot, frequence in compteur_mots.items():
        #si la frequence est egale a 1, on incrémente hap, sinon on compte pas
        if frequence == 1:
            hap += 1


    #on prend tous les resultat dans resultats
    resultats = {
        "tok": tok,
        "typ": typ,
        "hap": hap
    }

    #sauvegarde du resultat dans le cache
    save_cache("stats", book_id, resultats)

    return resultats