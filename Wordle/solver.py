import time
import pandas as pd 
import json

## Soare, Clint : 4.513
## Clint, Soare : 4.518
## Coals, Niter : 4.537
## Slate, Orcin : 4.54

##### TODO #####
# Sort by position over just letter rank
# Find best starter words

# Must be non empty
INITIAL_GUESSES = ["soare", "clint"] # "crane", "moist"
MULTIPLIER = -1000
MODEL_FILE = "wordcount_output.json"
WORDS_FILE = "words.txt"

def pred(ele):
    return ele.key()


def pre_solver(silent):
    result = {}
    if not silent: print("Loading...")

    # Load wordcounts
    with open(MODEL_FILE, 'r') as file:
        count = json.load(file)

    # Load words
    with open(WORDS_FILE, 'r') as file:
        words = file.read().splitlines()

    # Collect scores
    for word in words:
        score = 1
        for i in range(len(word)):
            score *= count[str(i)][word[i]] / len(words)
        result[word] = score
    
    result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))
    return result # Return dictionary of words with their score, sorted

def solver(word, silent, automated, words, init_guesses):
    # Interface starts here
    tries = 1
    init_size = len(init_guesses)
    guess = "temp"

    if not silent: print("\n == (_ for fail, caps for green, lowercase for yellow) ==")
    if len(init_guesses) > 0:
        if not silent: print("Start: " + init_guesses[0].upper())
        guess = init_guesses[0]
        words.pop(init_guesses[0])

    while True:
        # Check exit condition
        if guess.lower() == word or (tries <= init_size and word == init_guesses[tries-1]):
            return tries
        if tries > 6:
            return 7
        
        # Keep going through initial guesses
        if (tries <= init_size):
            guess = init_guesses[tries-1]
            if (init_guesses[tries-1] in words):
                words.pop(init_guesses[tries-1])
            if not silent: print("Initial Guess Override #" + str(tries) + ": " + guess.upper())

        # Input
        if automated:
            inp = wordle_output(word, guess)
            if not silent: print("Input from machine: " + inp)
        else:
            good = False
            while not good:
                inp = input("Input result: ")
                if (len(inp) == 5):
                    good = True
        
        tries, guess, words = solve_case(inp, silent, tries, word, words, guess)
        words.pop(guess)

        # If 4th Guess, Bring back in duplicate cases
        # if tries == 4:
        #     for val, key in enumerate(words):
        #         copy = key
        #         copy = "".join(set(copy))
        #         if val < 0:
        #             val = (val - MULTIPLIER) * -1
        
def solve_case(inp, silent, tries, word, words, guess):
    # Parse result
    curr_char = 0
    for char in inp:
        copy = dict(words)
        if (char != '_'):
            if (char.isupper()):
                if not silent: print("G", end =" ")
                # Green
                for key in words:
                    if key[curr_char] != char.lower():
                        copy.pop(key)
            else:
                if not silent: print("Y", end =" ")
                # Yellow
                for key in words:
                    if char not in key or key[curr_char] == char:
                        copy.pop(key)
        else:
            if not silent: print("-"+guess[curr_char].lower(), end =" ")
            # Ignore This Char
            for key in words:
                if guess[curr_char].lower() in key and (inp.count(guess[curr_char].lower()) + inp.count(guess[curr_char].upper()) == 0):
                    copy.pop(key)
        curr_char += 1
        words = dict(copy)
    if not silent: print("")
    
    # Get most likely result
    if not silent: print("Try: " + list(words)[0].upper())
    guess = list(words)[0].upper()
    inp = ""
    tries += 1    
    return [tries, guess.lower(), words]

def wordle_output(word, guess):
    word_copy = list(word)
    output = ['_', '_', '_', '_', '_']
    # First label greens
    for i in range(5):
        if word[i] == guess[i]:
            output[i] = word[i].upper()
            word_copy[i] = '_'
    # Next label yellow
    for i in range(5):
        if word[i] != guess[i] and guess[i] in word_copy:
            output[i] = guess[i]

    return "".join(output)

def testing_runner():
    pre_parsed_words = pre_solver(True)
    result = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}

    start_time = time.time()
    # Load words from list
    with open(WORDS_FILE, 'r') as f:
        content = f.read()
        words = content.split()

    sum = 0
    counter = 0
    for w in words:
        counter += 1
        if (counter % 300 == 0):
            status = round(100*(counter / len(words)))
            print("Status: " + str(status) + "%") # Status
        try:
            copy = dict(pre_parsed_words)
            attemps = solver(w, True, True, copy, INITIAL_GUESSES)
            result[attemps].append(w)
            sum += attemps
        except:
            print("ERROR occurred on word: " + w)

    avg = sum/len(words)
    print("Average Attempt Count: " + str(avg))
    print("Number of 7+'s: " + str(len(result[7])) + " (" + str(round((len(result[7]) / len(words)) * 100, 2)) + "%)")
    print("7+ Words: ")
    print(result[7])
    print("--- %s seconds ---" % (time.time() - start_time))

    # Write to csv
    for i in range(1, 8):
        df = pd.DataFrame(result[i])
        df.to_csv('results/result_' + str(i) + '.csv', index=False, header=False)


if __name__ == '__main__':
    words = pre_solver(False)
    # solver("testinggg", False, False, words, INITIAL_GUESSES) # Normal 

    testing_runner() # Tester

    # solver("dowdy", False, False, words, INITIAL_GUESSES) # Debug

    # print(wordle_output("dowdy", "daddy"))