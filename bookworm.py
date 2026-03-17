with open("pg84.txt", "r", encoding="utf-8") as f:
    text = f.read()

start = text.find("*** START OF")
end = text.find("*** END OF")

clean_text = text[start:end].splitlines()[1:]  

print("\n".join(clean_text))