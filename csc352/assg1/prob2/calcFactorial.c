#include <stdio.h>

/*
 * File: calcFactorial.c
 * Author: Elton Ho
 * Purpose: Takes in a sequence of 0 or more integers between 0 and 12 
 * (inclusive) from stdin (until no more can be read in) and prints out their 
 * factorial.
*/
int calFact(int num){
        /*
	 *Calculates the factorial of a number.
	 *Parameters: num is an int that is the positive integer we want the factorial
	 *of. The integer being positive is an asumption we are making.
	 *Returns: an int that is the factorial of num.
	*/
	int currFact = 1;
	for (int i = 1; i <= num; i++)
		currFact*=i;	
	return currFact;
}

int main(){
	int num;
	int retVal = scanf("%d", &num);
	int errSeen = 0;

	// keep taking in stdin until no more can be read in
	while (retVal > 0){

		// check for invalid numbers 
		if (num < 0 || num > 12){
			fprintf(stderr, "Error: input value %d is out of range\n", num);
			errSeen = 1;
		}
		else{
			printf("%d! = %d\n", num, calFact(num));
		}

		// continue taking in stdin 
		retVal = scanf("%d", &num);
	}

	// non integers were found, thus an error so exit
	if (retVal == 0) {
		fprintf(stderr, "Error: input is not a number\n");
		return 1;
	}

	return errSeen;
}
