#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>

/*
 * File: lineSum.c
 * Author: Elton Ho
 * Purpose: Takes in positive numbers seperated by white space in stdin and 
 * report the sum of the numbers in each line.
 */

int nextNumber(char* line){
	/*
	 *It finds the index of the next number in a line of input string. It 
	 *assumes that the line only has numbers seperated by white space. Note
	 *line param is a copy of the pointer due to pass by value so we it
	 *doesn't interfere with getline freeing memory.
	 *Parameters: line is a string that is an line from the input. 
	 *Returns: None.
	*/
	int index = 0; 

	// go past numbers and the spaces after it to try to go to the next num
	while (isdigit(*line)){
		index ++;
		line ++;	
	}
	while (isspace(*line)){
		index ++;
		line ++;	
	}
	if (index == 0){
		fprintf(stderr, "Bad line input\n");
		exit(1);	
	}
	return index;
}

int addCount(char* line){
	/*
	 *Returns the sum of numbers separated by white space in a line of 
	 *input string. Note that the line param is a copy of the pointer due to
	 *pass by value so we it doesn't interfere with getline freeing memory.
	 *We assume that negative numbers are also invalid as input. If the 
	 *input is invalid, it returns -1. The numbers and the sum are assumed
	 *to be no larger than an int.
	 *Parameters: line is a string that is an line from the input. 
	 *Returns: An int representing the sum of the numbers seperated by white 
	 *space in a line of input string. If the input was invalid it returns 
	 -1.
	*/
	int sum = 0;
	int currNumber;
	int retVal = sscanf(line, "%d", &currNumber);

	// trim leading white spaces
	while (isspace(*line)){
		line ++;	
	}

	if (*line == '\0'){
		fprintf(stderr, "Empty line\n");
		return -1;	
	}
	while (retVal > 0){
		if (currNumber < 0){
			fprintf(stderr, "No negative numbers allowed\n");
			return -1;	
		}
		sum += currNumber;
		// move line local var to the next number and scan starting there
		retVal = sscanf(line += nextNumber(line), "%d", &currNumber);
	}
	if (retVal == 0){ // a non number as input is invalid
		fprintf(stderr, "Bad line input\n");
		return -1;	
	}
	return sum;
}

int main(){
	int errSeen = 0;
	size_t size = 0;
	char* line = NULL;
	int result;

	while (getline(&line, &size, stdin) != EOF){
		result = addCount(line);
		if (result < 0){
			errSeen = 1;	
		}
		else // we got a valid result
			printf("%d\n", result); 
	}
	return errSeen;
}
