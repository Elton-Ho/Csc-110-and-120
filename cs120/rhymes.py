"""
    File: rhymes.py
    Author: Elton Ho
    Course: CSC 120, Spring 2024
    Purpose: This program has 3 functions that return a dictionary of the 
    pronunciation of words based on a text file, find the phoneme around the 
    stressed syllable of an inputted word and another passed-in word, and check 
    if two words are a perfect rhyme based on the phoneme. These three 
    functions work together to find all words in a file that are a perfect 
    rhyme of the inputted word.
"""

def convert_to_dic():
    """Takes the input for the name of a file and sets up the file into a 
    dictionary of words as the keys and its pronunciations as the values. 
  
    Parameters: None.
  
    Returns: A dictionary of strings where the key is the word and the value 
    is the pronunciation of the word. 
    """

    file_name = input()
    file = open(file_name)
    word_dic = {}
    for line in file:
        line_list = line.strip().split()
        if line_list[0] not in word_dic:
            word_dic[line_list[0]] = []  # line_list[0] refers to the word

        # line_list[1:] refers to the word's pronunciation 
        word_dic[line_list[0]].append(line_list[1:])
    file.close()
    return (word_dic)

def find_stressed(word_dic, inputted, other):
    """Centers around the stressed syllable of the inputted word and another
    passed in word.  
  
    Parameters: word_dic is a dictionary of strings with the words as the keys 
    and pronunciations as the values.
    inputted is a string that is the word that gets inputted.
    other is a string that is another word that gets passed in.
  
    Returns: A dictionary with strings as the key representing whether it is 
    the inputted word or the passed-in word and the values are a 2D list of the
    strings that are the phenome around the stressed syllable of the word for 
    each pronunciation.
    """

    inputed_upper = inputted.upper()  # makes it case-insensitive
    stressed = {"inputed_word":[],"other_word":[]}
    for pronunciation in word_dic[inputed_upper]:
        for phoneme in range(len(pronunciation)):
            if pronunciation[phoneme][-1] == "1":  # it's a stressed syllable 
                if phoneme != 0:  # if the stressed syllable isn't in front 

                    # start from the phoneme before the stressed syllable
                    stressed["inputed_word"].append(pronunciation[phoneme -1:])
                else:  # if the stressed syllable is in front

                    # put a space in front of the stressed syllable
                    stressed["inputed_word"].append([" "])
                    stressed["inputed_word"][-1] += (pronunciation[0:])

    # same as the inputed_word version, just working on the other_word                
    for pronunciation in word_dic[other]:
        for phoneme in range(len(pronunciation)):
            if pronunciation[phoneme][-1] == "1":
                if phoneme != 0:
                    stressed["other_word"].append(pronunciation[phoneme -1:])
                else:
                    stressed["other_word"].append([" "])
                    stressed["other_word"][-1] += (pronunciation[0:])
    return stressed

def rhyme(word_dic):
    """Finds the perfect rhymes of the inputted word based on the passed in 
    dictionary of word's pronunciation.  
  
    Parameters: word_dic is a dictionary of strings with the words as the keys 
    and pronunciations as the values.
  
    Returns: A list of strings that are a perfect rhyme of the inputted string. 
    """

    inputed_word = input()
    rhymes = []
    for word in word_dic:
        if word != inputed_word:
            stress_dic = find_stressed(word_dic, inputed_word, word)

            # go through each pronunciation of the inputted word 
            for index in range(len(stress_dic["inputed_word"])):

                # compares them to every other word's pronunciations 
                for pronunciation in stress_dic["other_word"]:

                    # preceding phoneme is different 
                    if stress_dic['inputed_word'][index][0] \
                    != pronunciation[0]:
                        
                        # every phoneme that isn't the preceding is the same 
                        if stress_dic['inputed_word'][index][1:] \
                        == pronunciation[1:]:
                            rhymes.append(word)                        
    return rhymes

def main():
    
    # input for a word comes from the rhyme function 
    sorted_rhyme = sorted(rhyme(convert_to_dic()))
    for word in sorted_rhyme:
        print(word)
main()
