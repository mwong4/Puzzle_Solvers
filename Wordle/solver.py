import time
import pandas as pd 
import json
import tkinter as tk

INITIAL_GUESSES = ["soare", "clint", "bumpy"] # Must be non empty
MODEL_FILE = "wordcount_output.json"
WORDS_FILE = "words.txt"
WORD_LENGTH = 5

# For GUI
COLORS = [["#7a7b7f", "#414248"], ["#c6b657", "#8e8340"], ["#69aa67", "#518750"]] # Gray, Yellow, Green: [normal, highlighted]

def pred(ele):
    return ele.key()

# This loads in the model pre-parsed from the trainng data, 
# and creates a sorted list of most useful to least useful words
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

# Class for wordle looking letter boxes with encapsulation
class LetterButton:
    # Makes a new object with default values on a given frame
    def __init__(self, frame, interact_on):
        self.state = 0
        self.button = tk.Label(frame, font=("Helvetica", 20, "bold"), fg="#ffffff", width=2, height=1, bg=COLORS[0][0])
        self.hover = False
        if interact_on:
            self.button.bind("<Button-1>", func= lambda e: self.cycle())
            self.button.bind("<Button-2>", func= lambda e: self.reverse_cycle())
            self.button.bind("<Button-3>", func= lambda e: self.reverse_cycle())
            self.button.bind("<Enter>", func= lambda e: self.hover_in())
            self.button.bind("<Leave>", func= lambda e: self.hover_out())
    
    def reset(self):
        self.state = 0
        self.change_colour()
    
    def cycle(self):
        self.state += 1
        self.state %= len(COLORS)
        self.change_colour()
    
    def reverse_cycle(self):
        self.state -= 1
        self.state %= len(COLORS)
        self.change_colour()
    
    def hover_in(self):
        self.hover = True
        self.change_colour()
    
    def hover_out(self):
        self.hover = False
        self.change_colour()
    
    def change_colour(self):
        self.button.config(bg=COLORS[self.state][1 if self.hover else 0])
    
    def change_letter(self, letter):
        self.button.config(text=letter)
        

# This is a wrapper function for solving the wordle, called by both
# for manually solving wordle, and for the automated benchmarking
def solver_wrapper(word, silent, automated, words, init_guesses):
    # Interface starts here
    tries = 1
    init_size = len(init_guesses)
    guess = "temp"

    # For handling first initial guesses
    if not silent: print("\n == (_ for fail, caps for green, lowercase for yellow) ==")
    if len(init_guesses) > 0:
        if not silent: print("Start: " + init_guesses[0].upper())
        guess = init_guesses[0]
        words.pop(init_guesses[0])

    if automated:
        # For benchmark testing
        while True:
            # Check exit condition
            if guess.lower() == word or (tries <= init_size and word == init_guesses[tries-1]):
                return tries
            if tries > 6:
                return 7
            tries, words, guess  = solver(word, silent, automated, words, init_guesses, tries, guess, init_size)
    else:
        # GUI Mode (Manual Input)
        root = tk.Tk()
        root.title("Wordle Solver")

        ## Main Frame
        main = tk.Frame(root)
        main.pack(padx=20, pady=20)
        title = tk.Label(main, text = "WORDLE SOLVER", font = ("Arial", 32, "bold"))
        title.pack(anchor="w")
        subtitle = tk.Label(main, text = "BY MAX WONG", font = ("Arial", 10, "bold"))
        subtitle.pack(anchor="e")
        
        ## Try Frame
        try_frame = tk.Frame(main)
        try_frame.pack(anchor="w", pady=(20, 10))
        guess_label = tk.Label(try_frame, text = "TRY: ", font = ("Arial", 20, "bold"))
        guess_label.pack(side="left")
        guess_txt = [LetterButton(try_frame, False) for i in range(WORD_LENGTH)]
        for i in range(0, WORD_LENGTH):
            guess_txt[i].change_letter(init_guesses[0][i].upper())
            guess_txt[i].button.pack(side="left", padx=4)
        guess_txt[0].button.pack(padx=(74,4))

        
        ## Result Frame
        result_frame = tk.Frame(main)
        result_frame.pack(anchor="w")
        result_label = tk.Label(result_frame, text = "RESULT: ", font = ("Arial", 20, "bold"))
        result_label.pack(side="left", padx=(0, 15))
        btns = [LetterButton(result_frame, True) for i in range(WORD_LENGTH)]
        for i in range(0, WORD_LENGTH):
            btns[i].change_letter(init_guesses[0][i].upper())
            btns[i].button.pack(side="left", padx=4)
        
        def submitResult():
            nonlocal tries, words, guess # Otherwise Python wont use the right scope

            # Parse btn_state and create clue to pass to solver
            temp = []
            for btn_idx in range(WORD_LENGTH):
                if btns[btn_idx].state == 0:
                    temp.append('_')
                elif btns[btn_idx].state == 1:
                    temp.append(guess[btn_idx].lower())
                else:
                    temp.append(guess[btn_idx].upper())
                # Reset State
                btns[btn_idx].reset()

            # Call Solver
            tries, words, guess  = solver(word, silent, automated, words, init_guesses, tries, guess, init_size, "".join(temp))
            # Update Labels
            for idx in range(WORD_LENGTH):
                guess_txt[idx].change_letter(guess[idx].upper())
            for idx in range(len(btns)):
                btns[idx].change_letter(guess[idx].upper())

        btn_submit = tk.Button(result_frame, text="SUBMIT", bg=COLORS[0][0], command=submitResult)
        btn_submit.pack(side="left", padx=(10, 0))
        btn_submit.bind("<Enter>", lambda e: btn_submit.config(bg=COLORS[0][1]))
        btn_submit.bind("<Leave>", lambda e: btn_submit.config(bg=COLORS[0][0]))
        
        root.bind("<Return>", lambda event: submitResult())
        ## Frame end
        root.mainloop()

# This function solves wordle for each iteration
def solver(word, silent, automated, words, init_guesses, tries, guess, init_size, inp=None):
    # Input
    if automated:
        # Automated input
        inp = wordle_output(word, guess)
        if not silent: print("Input from machine: " + inp)
    else:
        if not silent: print("GUI Input was: " + inp)
    
    # Solve case
    tries, guess, words = solve_case(inp, silent, tries, words, guess)
    
    # Keep going through initial guesses
    if (tries <= init_size):
        guess = init_guesses[tries-1]
        if (init_guesses[tries-1] in words):
            words.pop(init_guesses[tries-1])
        if not silent: print("Initial Guess Override #" + str(tries) + ": " + guess.upper())
    else:
        words.pop(guess) # Remove guess from list
    return tries, words, guess
        
# This updates the list of words that are still valid
def list_cleaner_helper(word_list, eliminated_list, silent):
    for word in eliminated_list:
        word_list.pop(word)
    if not silent: 
        temp = list(word_list)
        print(temp[:5])
        print("number of words left in the pool: " + str(len(temp)))
    return word_list

# This takes in the clues from 1 round and updates the list of words that are still valid
def solve_case(inp, silent, tries, word_list, guess):
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

# This is my implementation of Wordle, and simulates the same outputs
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

# This is a function used for benchmarking the current performance.
# It tests the algo on every single possible word and produces stats
# On the overall performance of the algo.
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
            attemps = solver_wrapper(w, True, True, copy, INITIAL_GUESSES)
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

# This is main
if __name__ == '__main__':
    words = pre_solver(False)
    solver_wrapper("testinggg", False, False, words, INITIAL_GUESSES) # Normal 
    # testing_runner() # Tester Benchmark