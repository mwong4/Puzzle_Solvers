import time
import pandas as pd 
import json
import tkinter as tk
from tkinter import ttk

# Must be non empty
# INITIAL_GUESSES = ["hates", "round", "climb"]
INITIAL_GUESSES = ["soare", "clint", "bumpy"]
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
        
def list_cleaner_helper(word_list, eliminated_list, silent):
    for word in eliminated_list:
        word_list.pop(word)
    if not silent: 
        temp = list(word_list)
        print(temp[:5])
        print("number of words left in the pool: " + str(len(temp)))
    return word_list

def solve_case(inp, silent, tries, true_word, word_list, guess):
    clues = list(inp)

    for i in range(len(clues)):
        eliminated_list = []
        if clues[i] == '_':
            if not silent: print("-"+guess[i].lower(), end =" ")
            for word in word_list:
                # Remove the word if letter is grey in exact position, or if letter in word that is not also yellow or green
                if guess[i] == word[i] or (guess[i] in word and not (guess[i].upper() in inp or guess[i] in inp)):
                    eliminated_list.append(word) # Queue eliminations
        elif clues[i].isupper(): # green
            if not silent: print("G", end =" ")
            for word in word_list:
                if guess[i] != word[i]:
                    eliminated_list.append(word) # Queue eliminations
        else: # lowercase, yellow
            yellow_letter_count = clues.count(clues[i])
            if not silent: print("Y", end =" ")
            for word in word_list:
                if guess[i] == word[i] or word.count(clues[i]) < yellow_letter_count:
                    eliminated_list.append(word) # Queue eliminations
        word_list = list_cleaner_helper(word_list, eliminated_list, silent) # Eliminate queued eliminations
    if not silent: print("")
        
    # Get most likely result
    if not silent: print("Try: " + list(word_list)[0].upper())
    guess = list(word_list)[0].upper()
    inp = ""
    tries += 1    
    return [tries, guess.lower(), word_list]

def wordle_output(word, guess):
    word_copy = list(word)
    guess_copy = list(guess)
    output = ['_', '_', '_', '_', '_']
    # First label greens
    for i in range(5):
        if word[i] == guess[i]:
            output[i] = word[i].upper()
            word_copy[i] = '_'
            guess_copy[i] = '_'
    # Next label yellow
    ## For each letter that is not green in actual word
    for i in range(5):
        if word_copy[i] != '_': 
            # if it is in copy, label copy with yellow and pop from guess
            if word_copy[i] in guess_copy:
                idx = guess_copy.index(word_copy[i])
                output[idx] = guess_copy[idx]
                guess_copy[idx] = '_'

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
    # GUI
    root = tk.Tk()
    root.title("Wordle Solver")

    def add_to_list(event=None):
        text = entry.get()
        if text:
            text_list.insert(tk.END, text)
            entry.delete(0, tk.END)

    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=3)
    root.rowconfigure(0, weight=1)

    ## Frame
    frame = ttk.Frame(root)
    frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)

    entry = ttk.Entry(frame)
    entry.grid(row=0, column=0, sticky="ew")

    # entry.bind("<Return>", lambda event: add_to_list())
    entry.bind("<Return>", add_to_list)

    entry_btn = ttk.Button(frame, text="Add", command=add_to_list)
    entry_btn.grid(row=0, column=1)

    text_list = tk.Listbox(frame)
    text_list.grid(row=1, column=0, columnspan=2, sticky="nsew")
    ## Frame end

    ## Frame 2
    frame2 = tk.Frame(root)
    frame2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    frame2.columnconfigure(0, weight=1)
    frame2.rowconfigure(1, weight=1)

    entry = tk.Entry(frame2)
    entry.grid(row=0, column=0, sticky="ew")

    # entry.bind("<Return>", lambda event: add_to_list())
    entry.bind("<Return>", add_to_list)

    entry_btn = tk.Button(frame2, text="Add", command=add_to_list)
    entry_btn.grid(row=0, column=1)

    text_list = tk.Listbox(frame2)
    text_list.grid(row=1, column=0, columnspan=2, sticky="nsew")
    ## Frame end

    root.mainloop()


    # words = pre_solver(False)
    # solver("testinggg", False, False, words, INITIAL_GUESSES) # Normal 
    # testing_runner() # Tester