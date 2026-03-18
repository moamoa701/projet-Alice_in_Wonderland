import requests

url = "https://www.gutenberg.org/"

response = requests.get(url)


def download_books()
    


def clean_gutenberg_text(text):
    "permet de nettoyer le text téléchargé"


    start = text.find("*** START OF")
    end = text.find("*** END OF")
    
    clean_text = text[start:end].splitlines()[1:]
    
    return "\n".join(clean_text)