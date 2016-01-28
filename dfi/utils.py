import re
import string

from collections import Counter

def tokenize(input=None):
    tokens = re.split('\W+|_+', input.lower().strip())
    return filter(None, tokens)

def counter(input=None):
    tokens = re.findall(r'\w+', input.lower())
    return Counter(tokens)
