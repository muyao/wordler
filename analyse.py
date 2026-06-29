import json
from pathlib import Path
from itertools import combinations

with open(Path(__file__).resolve().parent / "english-words.json") as f:
	data = json.load(f)
words = data["words"]
wordCount = data["word_count"]

TARG_LEN = 5

# 1. Filter by length
words = [word for word in words if len(word) == TARG_LEN and word.isalpha()]

# Helper function to convert a word like "cab" to binary: 
# c=1, b=1, a=1 -> ...0000111
def word_to_bitmask(word):
	mask = 0
	for char in word:
		# Shift the bit by the letter's alphabetical index (a=0, b=1, etc.)
		mask |= (1 << (ord(char) - ord('a')))
	return mask

# 2. Convert words to masks and eliminate anagrams
mask_to_word = {}
for w in words:
	mask = word_to_bitmask(w)
	# If we already have a word with this exact letter combo, skip it
	if mask not in mask_to_word:
		mask_to_word[mask] = w

# Now we only iterate over unique letter combinations
unique_masks = list(mask_to_word.keys())

max_unique_letters = 0
best_pair = ()
all_best_pairs = []

# 3. Use itertools.combinations to avoid checking A+B and B+A
for mask1, mask2 in combinations(unique_masks, 2):
	# Combine the two words using Bitwise OR
	combined_mask = mask1 | mask2
	
	# Count the 1s in the binary number (Python 3.10+)
	unique_letters = combined_mask.bit_count()
	
	if unique_letters >= max_unique_letters:
		if unique_letters > max_unique_letters:
			max_unique_letters = unique_letters
			best_pair = (mask_to_word[mask1], mask_to_word[mask2])
			all_best_pairs = []
		
		# Filter out pairs with rare letters
		p = mask_to_word[mask1] + mask_to_word[mask2]
		if "q" not in p and "z" not in p and "w" not in p and "x" not in p and "v" not in p and "j" not in p:
			# Remember the best pairs
			all_best_pairs.append((mask_to_word[mask1], mask_to_word[mask2]))
		
		#if max_unique_letters == 10:
		#	break

print("Best Wordle opener pairs:")
print(all_best_pairs)
print("Maximum unique letters:")
print(max_unique_letters)