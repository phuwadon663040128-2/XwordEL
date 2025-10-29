import os

def run():
    file_folder  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_name = file_folder + '/scripts/1000-most-common-words.txt'
    file_path = os.path.join(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))), file_name)
    blacklist= ['heard', 'instrument', 'temperature', 'dictionary', 'experiment', 'particular', 'especially', 'experience']
 
    #get the words from the file
    wordlist = [   ]
    with open(file_path, 'r') as f:
        for line in f:
            word = line.strip()
            wordlist.append(word)

    #delete the word in file if it is in the blacklist
    wordlist = [x for x in wordlist if x not in blacklist]
    #remove the duplicates and words with less than 3 characters
    wordlist = list(set(wordlist))
    wordlist = [x for x in wordlist if len(x) > 2 and x.isalpha()]
    wordlist.sort()
    #save the words to the file
    with open(file_path, 'w') as f:
        for word in wordlist:
            f.write(word + '\n')
            print(word)

if __name__ == '__main__':
    run()