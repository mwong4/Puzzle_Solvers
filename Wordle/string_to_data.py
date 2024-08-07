import pandas as pd 

result = {1:[], 2:[], 3:[], 4:[], 5:[]}

# Load words from list
f = open('words.txt', 'r')
content = f.read()
words = content.split()
f.close()

df = pd.DataFrame(words)
df.to_csv('words.csv', index=False, header=False)