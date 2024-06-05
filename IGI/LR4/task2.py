'''
Task 2.23. Output the source text by replacing spaces with the character entered from the keyboard
Determine whether this string is a GUID with or without parentheses. A GUID is a string of 8, 4, 4, 4, 4, 4, 12 hexadecimal digits separated by a dash. 
An example of a valid expression is: e02fd0e4-00fd-090A-ca30-0d00a0038ba0 An example of an invalid expression is: e02fd0e400fd090Aca300d00a0038ba0.
find the number of words that are 3 characters long;
find the words with the number of vowels equal to the number of consonants and their ordinal numbers;
output the words in descending order of their lengths
⦁ the number of sentences in a text; 
⦁ the number of sentences in a text of each type separately (narrative, interrogative, and imperative); 
⦁ average sentence length in characters (only words count); 
⦁ the average length of a word in the text in characters;
⦁ the number of emoticons in the given text. A smiley is a sequence of characters that satisfies the following conditions: 
 the first character is either ";" (semicolon) or ":" (colon) exactly once; 
 followed by "-" (minus) symbol as many times as you like (including minus symbol can be zero times); 
 at the end there must be some number (not less than one) of identical brackets from the following set: "(", ")", "[", "]"; 
 no other symbols can occur inside the smiley face. For example, this sequence is an emoticon: ";---------[[[[[[[[". These sequences are not emoticons: "]", ";--",":",")".

Lab: 4
Version: 1.0
Dev: Sugako Tatyana
Date: 20.04.2024
'''
import re
import zipfile
from validation import int_input
from mixin import TimeLoggerMixin

class TextAnalizer(TimeLoggerMixin):
    text = ""

    def __init__(self, filename):
        try:
            with open(filename, 'r') as file:
                self.text = file.read()
        except FileNotFoundError:
            print(f"File '{filename}' not found.")

    def count_sentences(self):
        self.log_with_time()
        pattern = r"[.!?](?:\s|$)"
        sentences = re.split(pattern, self.text)
        sentences = [sentence for sentence in sentences if sentence.strip()]
        return len(sentences)

    def categorize_sentences(self):
        self.log_with_time()
        categories = {
            "declarative" : 0, 
            "exclamatory" : 0, 
            "interrogative" : 0
        }

        decl_pattern = r"[.](?:\s|$)"
        decl_sentences = re.split(decl_pattern, self.text)
        decl_sentences = [sentence for sentence in decl_sentences if sentence.strip()]
        categories['declarative'] = len(decl_sentences)

        excl_pattern = r"[!](?:\s|$)"
        excl_sentences = re.split(excl_pattern, self.text)
        excl_sentences = [sentence for sentence in excl_sentences if sentence.strip()]
        categories['exclamatory'] = len(excl_sentences)

        inter_pattern = r"[?](?:\s|$)"
        inter_sentences = re.split(inter_pattern, self.text)
        inter_sentences = [sentence for sentence in inter_sentences if sentence.strip()]
        categories['interrogative'] = len(inter_sentences)

        return categories


    def av_len_sent(self):
        self.log_with_time()
        sentences = re.split(r"[.?!]",self.text)
        sentences_len = [len(s) for s in sentences]
        return sum(sentences_len) / len(sentences_len)


    def av_len_word(self):
        self.log_with_time()
        words = re.split(r"\s+", self.text)
        words_len = [len(w) for w in words]
        return sum(words_len) / len(words_len)
    

    def smileys(self):
        self.log_with_time()
        return re.findall(r'[:;]-*[()\[\]]+', self.text)
    

    def is_guid(self):
        pattern = r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
        if re.match(pattern, self.text):
            return True
        else:
            return False
    

    def words_with_len_3(self):
        pattern = r"\b\w{3}\b"
        words = re.findall(pattern, self.text)
        return words
    

    def find_words_with_equal_vowels_consonants(self):
        words = re.findall(r'\b\w+\b', self.text)
        res = []

        for index, word in enumerate(words, 1):
            vowels = re.findall(r'[aeiou]', word, re.IGNORECASE)
            consonants = re.findall(r'[bcdfghjklmnpqrstvwxyz]', word, re.IGNORECASE)

            vowels_len, consonants_len = len(vowels), len(consonants)

            if vowels_len == consonants_len:
                res.append(index)

        return res
    

    def sort_words_by_length(self):
        words = re.findall(r'\b\w+\b', self.text)
        words = list(set(words))

        sorted_words = sorted(words, key=len, reverse=True)
        return sorted_words

    def main_task(self):
        print(f"Count sentences: {self.count_sentences()}\n" \
              f"Categorize sentences: {self.categorize_sentences()}\n" \
              f"Average sentence length: {self.av_len_sent()}\n"  \
              f"Average word length: {self.av_len_word()}\n" \
              f"Smileys: {self.smileys()}\n")
        
    
    def var_task(self):
        print(f"Is string GUID: {self.is_guid()}\n" \
              f"Words with len 3: {self.words_with_len_3()}\n" \
              f"Vowels == consonants: {self.find_words_with_equal_vowels_consonants()}\n" \
              f"Sort by len: {self.sort_words_by_length()}\n")

    def zip(self):
        info = f"Is string GUID: {self.is_guid()}\n Words with len 3: {self.words_with_len_3()}\n Vowels == consonants: {self.find_words_with_equal_vowels_consonants()}\nSort by len: {self.sort_words_by_length()}"

        with open('analysis.txt', 'w') as file:
            file.write(info)

        with zipfile.ZipFile('analysis.zip', 'w') as zipf:
            zipf.write('analysis.txt')

    def unzip(self):
        with zipfile.ZipFile('analysis.zip', 'r') as zipf:
            for item in zipf.infolist():
                print(f"filename: {item.filename} | date: {item.date_time} | size: {item.file_size}")
                with zipf.open(item) as file:
                    data = file.read()
                    print(data)

def Task2():
    textAnalizer = TextAnalizer("text.txt")

    while True:
        way = int_input("Choose: \n1. Main task \n2. Variant task\n3. Zip\n4. Unzip\n5. Exit\n")
        match way:
            case 1:
                textAnalizer.main_task()
            case 2:
                textAnalizer.var_task()
            case 3:
                textAnalizer.zip()
            case 4:
                textAnalizer.unzip()
            case 5:
                break
            case _:
                continue