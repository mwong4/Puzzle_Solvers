from test import *

def runner(silent):
    # Load words from list
    f = open('words.txt', 'r')
    content = f.read()
    words = content.split()
    f.close()

    word = "dairy"
    if not silent: print(word)

    # Game loop
    while True:
        # Input
        good = False
        while not good:
            inp = input("Guess: ")
            if (len(inp) == 5):
                good = True

        curr_char = 0
        output = ""
        for char in inp:
            if char == word[curr_char]:
                # Green
                output = output + char.upper()
            elif (char in word) and inp.count(char) <= word.count(char):
                # Yellow
                output = output + char.lower()
            else:
                output = output + "_"
            curr_char += 1

        if word == output.lower():
            return

        if not silent: print(output)


if __name__ == '__main__':
    runner(False)