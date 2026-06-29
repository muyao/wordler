# english-words.json from https://downloadwordlists.com/english/5-letter-words/
import json
import re
from pathlib import Path

def safeInput(datType, prompt):
    try:
        return datType(input(prompt))
    except:
        return safeInput(datType, prompt)

with open(Path(__file__).resolve().parent / "english-words.json") as f:
    data = json.load(f)

words = data["words"]
wordCount = data["word_count"]

targLen = safeInput(int, "Word length?\n> ")
words = [word for word in words if len(word) == targLen]

regex = ["."] * targLen

usedWords = safeInput(str, "Which words were used? Separate with a comma (,)\n> ")
usedWords = usedWords.lower().replace(" ", "").split(",")
usedWords = [word for word in usedWords if word != "" and len(word) == targLen]

for word in usedWords:
    greens = safeInput(
        str,
        f"{word}: Which letters are green? Use this format:\n" +
        "[<letter1>:<index1>], [<letter2>:<index2>],...\n" +
        "Note: Indexing begins with 1\n> "
    )
    greens = greens.lower().replace(" ", "").split(",")
    greens = [(green.split(":")[0], int(green.split(":")[1])) for green in greens if green != ""]
    for ltr, idx in greens:
        regex[idx - 1] = ltr

regex = "".join(regex)
print(regex)