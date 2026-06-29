# english-words.json from https://downloadwordlists.com/english/5-letter-words/
import json
from pathlib import Path

def safeInput(datType, prompt):
    try:
        return datType(input(prompt))
    except:
        safeInput(datType, prompt)

with open(Path(__file__).resolve().parent / "english-words.json") as f:
    data = json.load(f)

wordsAll = data["words"]
wordCount = data["word_count"]

targLen = safeInput(int, "Word length?\n> ")
words = [word for word in wordsAll if len(word) == targLen]
print(words)
# TODO: Ask for green, yellow and grey characters