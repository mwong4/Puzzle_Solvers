import time
import pandas as pd 

## Soare, Clint : 4.513
## Clint, Soare : 4.518
## Coals, Niter : 4.537
## Slate, Orcin : 4.54

##### TODO #####
# Sort by position over just letter rank
# Find best starter words

FIRST_GUESS = "crane"
SECOND_GUESS = "moist"

def pred(ele):
    return ele.key()


def pre_solver(silent):
    if not silent: print("Loading...")

    # Load rankings of letters, for later sorting
    f = open('letter_rank.txt', 'r')
    rank_content = f.read()
    temp = rank_content.split()
    ranks = {1:{}, 2:{}, 3:{}, 4:{}, 5:{}}
    f.close()

    counter = 1
    for i in temp:
        for j in range(0,26):
            ranks[counter][i[j]] = 26 - j
        counter += 1

    # Load words from list
    f = open('words.txt', 'r')
    content = f.read()
    temp = content.split()
    words = dict()
    f.close()
    
    # using loop to reform dictionary with splits
    for idx, ele in enumerate(temp):
        score = 0
        ele_copy = ele
        ele_copy = "".join(set(ele_copy))
        for i in range(0, len(ele_copy)):
            score += ranks[i+1][ele_copy[i]]
        words[ele] = score

    words = dict(sorted(words.items(), key=lambda item: item[1], reverse=True))
    if not silent: print("Done!")
    #### Done Pre-Parsing
    return words

def solver(word, silent, automated, words):
    # Interface starts here
    tries = 1
    if not silent: print("\n == (_ for fail, caps for green, lowercase for yellow) ==")
    if not silent: print("Start: " + FIRST_GUESS.upper())
    guess = FIRST_GUESS
    words.pop(FIRST_GUESS)

    while True:
        # Check exit condition
        if guess.lower() == word or word == SECOND_GUESS:
            return tries
        if tries > 6:
            return 7
        
        # 2 guess init, run if not guessed on 2nd try
        if (tries == 2):
            guess = SECOND_GUESS
            if (SECOND_GUESS in words):
                words.pop(SECOND_GUESS)
            if not silent: print("2nd Guess Override: " + guess.upper())

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
    curr_char = 0
    output = ""
    occurances = dict()
    for char in guess:
        if char == word[curr_char]:
            # Green
            output = output + char.upper()
        elif (char in word):
            # Yellow
            # Tracks number of occurances
            if (char in occurances):
                occurances[char] += 1
            else:
                occurances[char] = 1
            # If occurance not too many
            if occurances[char] <= word.count(char):
                output = output + char.lower()
            else:
                output = output + "_"
        else:
            output = output + "_"
        curr_char += 1

    return output

def testing_runner():
    pre_parsed_words = pre_solver(True)
    result = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}

    start_time = time.time()
    # Load words from list
    f = open('words.txt', 'r')
    content = f.read()
    words = content.split()
    f.close()

    sum = 0
    counter = 0
    for w in words:
        counter += 1
        if (counter % 300 == 0):
            status = round(100*(counter / len(words)))
            print("Status: " + str(status) + "%") # Status
        try:
            copy = dict(pre_parsed_words)
            attemps = solver(w, True, True, copy)
            result[attemps].append(w)
            sum += attemps
        except:
            print("ERROR occurred on word: " + w)

    avg = sum/len(words)
    print("Average Attempt Count: " + str(avg))
    print("Number of 7+'s: " + str(len(result[7])))
    print("--- %s seconds ---" % (time.time() - start_time))

    # Write to csv
    for i in range(1, 8):
        df = pd.DataFrame(result[i])
        df.to_csv('results/result_' + str(i) + '.csv', index=False, header=False)


if __name__ == '__main__':
    words = pre_solver(False)
    solver("testinggg", False, False, words) # Normal 

    # testing_runner()