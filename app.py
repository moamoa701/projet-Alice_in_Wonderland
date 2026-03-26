from flask import Flask, jsonify, render_template
from bookworm import generate_card, lexical_diversity, topic_modeling, extract_entities, summarize_book, fetch_book

#création de l'app
app = Flask(__name__)

#affichage
@app.route("/")
def index():
    return render_template("index.html")

#recherche des card
@app.route("/card/<int:book_id>")
def card(book_id):
    result = generate_card(book_id)
    if result:
        return jsonify(result)

    #gestion des erreurs    
    return jsonify({"error": "Livre introuvable"}), 404

#lancement du serveur
if __name__ == "__main__":
    app.run(debug=True)