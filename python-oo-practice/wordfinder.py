"""Word Finder: finds random words from a dictionary."""
from random import choice
# import random
class WordFinder:

    def __init__(self, path):
        text = open(path)
        self.words = self.parse(text)
        print(f'{len(self.words)} words read')
 
    def  parse(self, text):
        return [word.strip() for word in text]

    def random(self):
        return choice(self.words)   

class RandomWordFinder(WordFinder):
    def parse(self, text):
        return [word.strip() for word in text 
                if word.strip()and not word.startswith('#')]
