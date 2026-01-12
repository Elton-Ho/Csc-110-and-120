#include <stdio.h>
#include <ctype.h>

/*
 * File: cipher.c
 * Author: Elton Ho
 * Purpose: Takes in a number from stdin followed by alphanumeric strings. For 
 * each of those alphanumeric strings, rotate its alphabetial letters by the 
 * number taken as the first input. Rotating it by a positive number means to 
 * move towards z/Z for that number of times and wrap around to A if we pass Z 
 * and the opposite for rotating it by a negative number.
*/

int rotateLetters(char inputString[], int rotateBy){
	/*
	 *Rotates the alphabetical letters of inputString by rotateBy number of 
	 *times. Rotating by a negative rotateBy means moving towards a/A for 
	 *rotateBy number of times and vice versa for positive. This is 
	 *possible through the ability of mod to wrap around back to the 
	 *beginning and we can treat going backwards as rotating forwards, back 
	 *around to behind the number we are at. We assume inputString is a 
	 *valid string, so it has the null character at the end of the string 
	 *and is at most a length of 64.
	 *Parameters: inputString is a string that is the word we rotating.
	 *rotateBy is an int representing what direction and by how much we are 
	 *rotating the input by.
	 *Returns: 1 if the inputString is not a valid word (not only 
	 *alphanumeric char) and 0 if it is valid.
	*/
	for (int i = 0; inputString[i] != '\0'; i ++){
		if (!isalnum(inputString[i])){ // not a valid word
			return 1;	
		}
		
		// wraps rotateBy around 25 so it will be >= 0 and <= 25
		rotateBy %= 26;	

		// as 'a' rotated 25 times = 'a' rotated -1 times = z and 
		// (26 + 25) % 26 = (26 - 1) % 26 = 25 we have the general form 
		rotateBy = (26 + rotateBy) % 26;	
		if (inputString[i] >= 'a' && inputString[i] <= 'z'){
			
			// subtracting by 'a' lets 0 pretend to be 'a' so that 
			// mod lets us wrap around the alphabet back to 'a'
			inputString[i] = (inputString[i] - 'a' + rotateBy) % 26;

			// adding 'a' back after lets it actually be the ASCII 
			inputString[i] += 'a';
		}

		// same logic for lower case applies with upper case
		if (inputString[i] >= 'A' && inputString[i] <= 'Z'){
			inputString[i] = (inputString[i] - 'A' + rotateBy) % 26;
			inputString[i] += 'A';
		}
	}
	return 0;
}

int main(){
	int errSeen = 0;
	char inputString[65];
	
	// try to get a valid integer for rotateBY
	int rotateBy;
	int retVal = scanf("%d", &rotateBy);
	if (retVal < 1){
		fprintf(stderr, "No rotation value input\n"); 
		return 1;	
	}

	// try get get valid words that we are going to rotate
	retVal = scanf("%64s", inputString);
	while (retVal > 0 ){
		if(rotateLetters(inputString, rotateBy) == 1){
			errSeen = 1;

			// revert back for the err message
			rotateLetters(inputString, -rotateBy); 
			char errMessage[] = "Not alpha-numeric string: %s\n";
			fprintf(stderr, errMessage, inputString);	
		}
		else // is valid so print it rotated
			printf("%s\n", inputString);	
		retVal = scanf("%64s", inputString);
	}
	return errSeen;
}
