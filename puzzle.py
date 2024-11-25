#puzzle code
import hashlib
import time

def compute_md5(s):
    return hashlib.md5(s.encode()).hexdigest()

# Load English words into a set
def load_english_words(file_path):
    with open(file_path, 'r') as f:
        return [word.strip().lower() for word in f]

def load_md5_hashes(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f]

def brute_force(md5_file, word_file):
    hashes = load_md5_hashes(md5_file)
    words = word_file
    numbers = range(1, 1000000000)  # All n-digit numbers

    results = {}
    
    # Brute force each hash
    for word in words:
        for number in numbers:
            number_str = f"{number:09d}"
            candidate = number_str + word
            hash_candidate = compute_md5(candidate)
            if number_str == '050000000':
                print('at 50 mill')
            if hash_candidate in hashes:
                print(f"Number found: {candidate} -> {hash_candidate}")
                results[hash_candidate] = (number_str, word)
                break 
    return results

test_dict = ['and', 'a', 'the', 'The', 'be', 'to'] #first word works! 
PUZZLE_FILE = 'PUZZLE.txt'  

# results = brute_force(PUZZLE_FILE, test_dict)
# print(results)

WORD_FILE = load_english_words('words.txt')
def add_commas(WORD_FILE):
    new_words = []
    for word in WORD_FILE:
        new_word = word + ','
        new_words.append(new_word)
    return new_words
new_words = add_commas(WORD_FILE)
first_word = ['I', 'You', 'The', 'It', 'We', 'He', 'She', 'They', 'This', 'That', 
    'There', 'In', 'On', 'A', 'An', 'What', 'Where', 'How', 'Which', 'Why', 
    'Let', 'Do', 'Did', 'Can', 'Will', 'Would', 'Could', 'Must', 'Should', 'May']
WORD_FILE.extend(first_word)
WORD_FILE.extend(new_words)
missing_words = ["over.", "Toward", "the", "part", "upper", "was", "full", "side", "the", "rabbit",
                 "holes."]
WORD_FILE.extend(missing_words)
# print(len(WORD_FILE))

def create_hashes(word_file, number_str):
    guess_hashes = []
    for word in word_file:
        hash = number_str + word
        guess_hashes.append(hash)
    return guess_hashes

def guess_words(md5_file, WORD_FILE, number_str):
    guess_hashes = create_hashes(WORD_FILE, number_str)
    hashes = load_md5_hashes(md5_file)
    indexed_hashes = {h: i for i, h in enumerate(hashes)} 
    results = []
    for word in guess_hashes:
        computed_hash = compute_md5(word)
        if computed_hash in indexed_hashes:
            original_index = indexed_hashes[computed_hash]  # Find the original hash index
            results.append((original_index, word[9:]))  # Append index and word
            
    # Sort results by the original index
    results.sort(key=lambda x: x[0])  
    return results

# results = guess_words(PUZZLE_FILE, WORD_FILE, '294644421')
# print(results)

#patches is the word that is misspelled 
def edit1(word):
    letters = "abcdefghijklmnopqrstuvwxyz"
    #edit1:
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    edit1_words = set(deletes + transposes + replaces + inserts)
    return edit1_words

def generate_2edits(word):
    result = set()
    for e1 in edit1(word):
        for e2 in edit1(e1):
            result.add(e2)
    return list(result)

patches = list(generate_2edits('patches'))
quotation = [ "The", "primroses", "were", "over.", "Toward", "the", "edge", "of", "the", 
    "wood,", "where", "the", "ground", "became", "open", "and", "sloped", 
    "down", "to", "an", "old", "fence", "and", "a", "brambly", "ditch", 
    "beyond,", "only", "a", "few", "fading", "patches", "of", "pale", "yellow", 
    "still", "showed", "among", "the", "dog's", "mercury", "and", "oak-tree", 
    "roots.", "On", "the", "other", "side", "of", "the", "fence,", "the", 
    "upper", "part", "of", "the", "field", "was", "full", "of", "rabbit", 
    "holes."]

word_file = patches + quotation

results = guess_words(PUZZLE_FILE, word_file, '294644421')
print(results)

#misspelling: pacthes
