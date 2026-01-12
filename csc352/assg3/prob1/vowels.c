#include <stdio.h>
#include <ctype.h>

/*
 * File: vowels.c
 * Author: Elton Ho
 * Purpose: Repeatedly read in words until no more words can be read in. For 
 * each word read in, it prints 1 if the vowels in the word occur in 
 * alphabetical order and 0 if they don't.
*/

int isVowel(char letter){
	/*
	 *Checks if a char is a vowel and returns 1 (true) if it is and 0 
	 *(false) if it isn't. We assume that the char is a lowercase letter.
	 *Parameters: letter is a char that is the letter we are testing for if
	 *its a vowel or not.
	 *Returns: 0 (false) if the letter is not a vowel and 1 (true) if the 
	 *letter is a vowel.
	*/
	char vowels[]= {'a','e','i','o','u'};
	for (int i = 0; i < 5; i ++){
		if (vowels[i] == letter)
			return 1; 
	}
	return 0; // not a vowel 
}

int checkVowelsInOrder(char inputString[]){
	/*
	 *Checks if an inputed word has its vowels in alphabetical order and 
	 *returns -1 if the word isn't all alphabet letters, 0 (false) if the 
	 *vowels are not in alphabetical order, and 1 (true) if they are. It 
	 *assumes that inputString represents one word.
	 *Parameters: inputString is a string that is the word we are testing 
	 *for if its vowels are in order or not.
	 *Returns: -1 if the word isn't all alphabet letters, 0 (false) if the
	 *vowels are not in alphabetical order, and 1 (true) if they are.
	*/
	char smallestVowelSoFar = 'a';
	int isInOrder = 1;
	for (int i = 0; inputString[i] != '\0'; i ++){
		char lowerCaseChar = tolower(inputString[i]);

		// check if it's an invalid input
		if (lowerCaseChar < 'a' || lowerCaseChar > 'z') 
			return -1;
		
		// check if its a vowel that is before the last vowel we've seen
		int isVowelResult = isVowel(lowerCaseChar);
		if (lowerCaseChar < smallestVowelSoFar && isVowelResult) {

			// doesn't return yet in case of invalid char later
			isInOrder = 0; 
		}
		else if (isVowelResult){
			smallestVowelSoFar = lowerCaseChar;	
		}
	}
	return isInOrder;
}

int main(){
	char inputString[65];
	int errSeen = 0;
	int retVal = scanf("%64s", inputString);

	// keep trying to get valid words to test their vowels 
	while (retVal > 0){
		int resultOfCheck = checkVowelsInOrder(inputString);		
		if (resultOfCheck >= 0){
			printf("%d\n", resultOfCheck);	
		}
		else {
			fprintf(stderr, "Non alpha input: %s\n", inputString);
			errSeen = 1;	
		}
		retVal = scanf("%64s", inputString);	
	}
	return errSeen;
}
