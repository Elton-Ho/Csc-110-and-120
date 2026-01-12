import csv
import string
import sys

class Word:
    def __init__(self, word):
        self._word = word
        self._count = 1

    def word(self):
        return self._word
    
    def count(self):
        return self._count
    
    def incr(self):
        self._count += 1

    def __lt__(self,other):
        return self._word < other._word

    def __str__(self):
        return self._word + " : " + str(self._count) + " " 
    
def update_count(list, word):
    change = False
    for element in list:
        if word == element.word():
            element.incr()
            change = True
    if not change:
        list.append(Word(word))   

def merge(L1, L2, merged):
    if L1 == [] or L2 == []:
        return merged + L1 + L2
    else:
        if L1[0].count() > L2[0].count():
            new_merged = merged + [ L1[0] ]
            new_L1 = L1[1: ]
            new_L2 = L2
        if L1[0].count() < L2[0].count():
            new_merged = merged + [ L2[0] ]
            new_L1 = L1
            new_L2 = L2[1: ]
        if L1[0].count() == L2[0].count():
            if L1[0] < L2[0]:
                new_merged = merged + [ L1[0] ]
                new_L1 = L1[1: ]
                new_L2 = L2
            else:
                new_merged = merged + [ L2[0] ]
                new_L1 = L1
                new_L2 = L2[1: ]

        return merge(new_L1, new_L2, new_merged)

def msort(L):
    if len(L) <= 1:
        return L
    else:
        split_pt = len(L)//2
        L1 = L[ :split_pt]
        L2 = L[split_pt: ]
        sortedL1 = msort(L1)
        sortedL2 = msort(L2)
        return merge(sortedL1, sortedL2,[])

def process_and_print():
    file_name = input("File: ")
    file = open(file_name)
    word_list = []
    csvreader = csv.reader(file)  # spits at the proper commas of a csv
    for line in csvreader:
        if "#" not in line[0]:

            # gets rid of the punctuation
            new_list = []
            for char in line[4]:
                if char not in string.punctuation:
                    new_list.append(char.lower())
                else:
                    new_list.append(" ")

            # gets rid of the spaces and characters with lengths > 2 
            no_spaces = "".join(new_list).split()
            for char in no_spaces:
                if len(char) > 2:
                    update_count(word_list, char)
    word_list = msort(word_list)
    integer_n = int(input("N: "))  # n is a word's linked list inputed position 
    for words in word_list:
        if words.count() >= word_list[integer_n].count():
            print(words)
    file.close

def main():
    sys.setrecursionlimit(4000)
    process_and_print()

main()