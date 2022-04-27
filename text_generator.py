# Write your code here
import os
from nltk.tokenize import word_tokenize, regexp_tokenize, WhitespaceTokenizer
import numpy as np
from nltk.util import ngrams
from collections import defaultdict
import random
import regex
from nltk import trigrams


def load_corpus():
    filename = input()
    while not os.path.exists(filename):
        print("File not found.")
        filename = input()

    corpus = ""
    with open(filename, 'r', encoding='"utf-8"') as f:
        corpus = f.read()

    tk = WhitespaceTokenizer()
    words = tk.tokenize(corpus)

    return words


def get_query_int(len_words):
    """
    :param len_words: int
    :return: Boolean if exit, Boolean if error, query (int)
    """

    query = input()

    if query == 'exit':
        exit_statue = True
        return True, False, 0

    try:
        query = int(query)
    except ValueError:
        print("Type Error. Please input an integer.")
        return False, True, 0

    query = int(query)
    if query >= len_words:
        print("Index Error. Please input an integer that is in the range of the corpus.")
        return False, True, 0

    return False, False, query


def describe_corpus():
    words = load_corpus()

    print("Corpus statistics")
    print("All tokens: " + str(len(words)))
    print("Unique tokens: " + str(len(np.unique(words))))
    print("")

    exit_statue, error_statue = False, False
    while not exit_statue:
        exit_statue, error_statue, query = get_query_int(len(words))
        if not exit_statue and not error_statue:
            print(words[query])


def query_grams():
    words = load_corpus()

    bigrams = list(ngrams(words, 2))
    print("Number of bigrams: " + str(len(bigrams)))
    print("")

    exit_statue, error_statue = False, False
    while not exit_statue:
        exit_statue, error_statue, query = get_query_int(len(bigrams))
        if not exit_statue and not error_statue:
            print("Head: " + bigrams[query][0] + "\t" + "Tail: " + bigrams[query][1])


def form_grams():

    words = load_corpus()
    bigrams = list(ngrams(words, 2))
    freq = defaultdict(dict)

    for head, tail in bigrams:
        if tail in freq[head].keys():
            freq[head][tail] += 1
        else:
            freq[head][tail] = 1

    while True:
        head = input()
        if head == "exit":
            break

        print("Head: " + head)
        if head in freq.keys():
            for tail in freq[head].keys():
                print("Tail: " + tail + "\t" + "Count: " + str(freq[head][tail]))

        else:
            print("Key Error. The requested word is not in the model."
                  " Please input another word.")
        print("")


def gen_sentences():

    words = load_corpus()
    trigrams_list = list(trigrams(words))

    freq = defaultdict(dict)

    for head, head2, tail in trigrams_list:
        if tail in freq[(head, head2)].keys():
            freq[(head, head2)][tail] += 1
        else:
            freq[(head, head2)][tail] = 1

    i = 0
    while i < 10:

        while True:
            iter_word = random.choice(list(freq.keys()))
            if regex.match(r"^[A-Z]{1}[^\.\!\?]*?$", iter_word[0]):
                break

        seq = [iter_word[0], iter_word[1]]
        iter_word = iter_word[1]
        j = 1

        while True:
            if len(freq[(seq[-2], seq[-1])]) == 0:
                break
            iter_word = random.choice(list(freq[(seq[-2], seq[-1])].keys()))
            discard = False
            seq.append(iter_word)
            check_end = seq[-1][-1] in ".!?"
            if check_end and len(seq) < 4:
                while True:
                    # iter_word = random.choice(list(freq.keys()))
                    if len(freq[(seq[-2], seq[-1])]) == 0:
                        discard = True
                        break
                    iter_word = random.choice(list(freq[(seq[-2], seq[-1])].keys()))
                    # print(iter_word)
                    if regex.match(r"^[A-Z]{1}[^\.\!\?]*?$", iter_word):
                        # seq.append(iter_word[0])
                        seq.append(iter_word)
                        break
                if discard:
                    continue
                if seq[-1][-1] in ".!?" and len(seq) > 4:
                    break
            elif len(seq) > 4 and check_end:
                break
            else:
                iter_word = seq[-1]

            j += 1

        print(" ".join(seq))
        i += 1


gen_sentences()

