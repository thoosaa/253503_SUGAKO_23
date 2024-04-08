'''
Task 4.23.
a) determine the number of words consisting of capital letters ;
b) find the longest word that starts with the letter 's';
c) find the repetitive words

Lab: 3
Version: 1.0
Dev: Sugako Tatyana
Date: 24.03.2024
'''

def CapitalLettersCount(str):
    """Count the number of words consisting of capital letters"""
    cap_let = [chr(65 + i) for i in range(0, 27)]
    res = 0
    words = str.split()
    for word in words:
        if word[0] in cap_let:
            res += 1
    return res

def LongestWordStartS(str):
    """Find the longest word that starts with the letter 's'"""
    str = str.split()
    words = [word for word in str if word[0] == 's' or word[0] == 'S']
    words.sort(key=len)
    return words[-1]

def RepetitiveWords(str):
    """Find the repetitive words"""
    words = str.split()
    counts = {}
    # Dictionary, where keys are words and the values is number they occur 
    for word in words:
        if word not in counts:
            counts[word] = 0
        counts[word] += 1
    
    duplicate = []
    for key, value in counts.items():
        if value > 1:
            duplicate.append(key)
    return duplicate


def Task4():
    print("Task 4", '-' * 100, sep='\n')
    given_str = """So she was considering in her own mind, as well as she could, 
                for the hot day made her feel very sleepy and stupid, 
                whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, 
                when suddenly a White Rabbit with pink eyes ran close by her."""
    print(f"Number of words with capital letters: {CapitalLettersCount(given_str)}", f"Longest word which starts with s: {LongestWordStartS(given_str)}", f"Repetitive words: {RepetitiveWords(given_str)}", sep='\n')
    print('-' * 100)