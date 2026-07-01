import json
import re
from pathlib import Path
from helpers import safeInput

# english-words.json from https://downloadwordlists.com/english/5-letter-words/

CONFIG = {
	"5": {
		"openers": "cones,trial,dough"
	}
}

with open(Path(__file__).resolve().parent / "english-words.json") as f:
	data = json.load(f)

words = data["words"]
wordCount = data["word_count"]

targLen = safeInput(int, "\tWord length?\n> ")
words = [word for word in words if len(word) == targLen]
print()

regex = ["."] * targLen

if str(targLen) in CONFIG:
	useConfig = safeInput(str, f"\tUse preconfigured data for word length {targLen}? (y/n)\n> ").lower()
if useConfig == "y":
	usedWords = CONFIG[str(targLen)]["openers"]
else:
	usedWords = safeInput(str, "\tWhich words were used? Separate with a comma (,)\n> ")
usedWords = usedWords.lower().replace(" ", "").split(",")
if useConfig == "y":
	moreUsedWords = safeInput(str, "\tAdditional words that were used? Separate with a comma (,)\n> ")
	moreUsedWords = moreUsedWords.lower().replace(" ", "").split(",")
	usedWords += moreUsedWords
usedWords = [word for word in usedWords if word != "" and len(word) == targLen]
print()

for word in usedWords:
	greens = safeInput(
		str,
		f"\t{word}: Which letters are green? Use this format:\n" +
		"\t[<letter1>:<index1>], [<letter2>:<index2>],...\n" +
		"\tNote: Indexing begins with 1\n> "
	)
	greens = greens.lower().replace(" ", "").split(",")
	greens = [(green.split(":")[0], int(green.split(":")[1])) for green in greens if green != ""]
	print()
	for ltr, idx in greens:
		if regex[idx - 1] != "." and regex[idx - 1] != ltr:
			raise Exception()
		regex[idx - 1] = ltr

pattern = re.compile("".join(regex))
print("< Filtering greens...")
words = [word for word in words if bool(re.fullmatch(pattern, word))]
print("< Done")
if len(words) == 1:
	print()
	print(f"< Word: {words[0]}")
	exit(0)
print(f"< {len(words)} possible words left")
print()

greys = safeInput(str, "\tWhich letters are grey? Separate with a comma (,)\n> ")
greys = greys.lower().replace(" ", "").replace(",", "")
greyYellow = []
for char in regex:
	if char == ".":
		greyYellow.append(f"[^{greys}]")
		continue
	greyYellow.append(char)

regex = greyYellow

pattern = re.compile("".join(regex))
print("< Filtering greys...")
words = [word for word in words if bool(re.fullmatch(pattern, word))]
print("< Done")
if len(words) == 1:
	print()
	print(f"< Word: {words[0]}")
	exit(0)
print(f"< {len(words)} possible words left")
print()

regex = []

for word in usedWords:
	yellows = safeInput(
		str,
		f"\t{word}: Which letters are yellow? Use this format:\n" +
		"\t[<letter1>:<index1>], [<letter2>:<index2>],...\n" +
		"\tNote: Indexing begins with 1\n> "
	)
	yellows = yellows.lower().replace(" ", "").split(",")
	yellows = [(yellow.split(":")[0], int(yellow.split(":")[1])) for yellow in yellows if yellow != ""]
	print()
	for ltr, idx in yellows:
		if f"(?=.*{ltr})" not in regex:
			regex.append(f"(?=.*{ltr})")
		if greyYellow[idx - 1][0] != "[":
			continue
		elif ltr in greyYellow[idx - 1].split("]")[0]:
			continue
		greyYellow[idx - 1] = greyYellow[idx - 1].split("]")[0] + ltr + "]"

regex += greyYellow

pattern = re.compile("".join(regex))
print("< Filtering yellows...")
words = [word for word in words if bool(re.fullmatch(pattern, word))]
print("< Done")
if len(words) == 1:
	print()
	print(f"< Word: {words[0]}")
	exit(0)
print(f"< {len(words)} possible words left")
print()

print()
print("\tPossible words:")
print(f"< {words}")