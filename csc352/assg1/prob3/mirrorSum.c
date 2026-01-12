#include <stdio.h>

/*
 * File: mirrorSum.c
 * Author: Elton Ho
 * Purpose: Takes in a sequence of 0 or more positive integers from stdin and 
 * print out the mirror sum of the input.
*/

int reverseNum (int num){
        /*
	 *Calculates and returns the reversed digits version of a positive integer.
	 *The integer being positive is an asumption we are making.
	 *Parameters: num is an positive int that we want to get the reverse of.
	 *Returns: an int that is num with its digits reversed.
	*/
	int reverse = 0;

	// go through num's digit one by one starting at the one's place 
	while (num > 0){
		
		// build the reverse from the lowest digit place one at a time
		reverse = 10 * reverse + num%10;
		num /= 10;
	}
	return reverse;
}

int main(){
	int num;
	int errSeen = 0;
	int retVal = scanf("%d", &num);

	// keep taking in stdin until no more can be read
	while (retVal > 0){

		// error if stdin gets a non positive number
		if (num <= 0){
			fprintf(stderr, "Error: input value %d is not positive\n", num);
			errSeen = 1;
		}
		else{

			// print out the mirror sum of num (num is the input)
			printf("%d\n", reverseNum(num)+num);
		}

		// keep taking in stdin
		retVal = scanf("%d", &num);
	}

	// error if stdin didn't get an number so it exits
	if (retVal == 0){
		fprintf(stderr, "Error: Non-integer value in input\n");
		return 1;
	}
	return errSeen;
}
