import requests
import re
import math
import argparse
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
    
    start = text.find("*** START OF")
    end = text.find("*** END OF")
    
    clean_text = text[start:end].splitlines()[1:]
    return "\n".join(clean_text)

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

