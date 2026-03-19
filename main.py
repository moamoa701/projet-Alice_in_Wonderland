from bookworm import fetch_book
from analyzer import compute_lexical_stats

#choix du livre
book_id = int(input("veuillez entrer un id de livre : "))

#recupération du livre
print("\n Récupération du texte...")
texte_du_livre = fetch_book(book_id)

if texte_du_livre:

    print("\n Analyse de stats")
    stats = compute_lexical_stats(texte_du_livre, book_id)
    
    #affichage resultat
    print(f"\n Résultat du livre id : {book_id}")
    print(f"Tokens : {stats['tok']}")
    print(f"Types  : {stats['typ']}")
    print(f"Hapax  : {stats['hap']}")
else:
    print("impossible de récupérer le texte")
