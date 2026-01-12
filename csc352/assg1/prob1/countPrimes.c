#include <stdio.h>
#include <math.h>

/*
 * File: countPrimes.c
 * Author: Elton Ho
 * Purpose: Counts the number of prime numbers between (not inclusive) two 
 * positive integers m and n from stdin.
*/
int checkPrime(int number){
	/*
	 *Checks if a number is prime. We assume that the number is an valid integer.
	 *Parameters: number is a int that is the number we are testing if its prime
	 *or not.
	 *Returns: 0 (false) if the number is not prime and 1 (true) if the number is
	 *prime.
	*/

	// 2 is the first prime number
	if (number <= 1) 
		return 0;
	if (number == 2) 
		return 1;

	// +1 to be careful of truncated part of the sqrt
	int sqrtNum = sqrt(number) + 1;

	// if we found found a factor of the number when looking at numbers from 2 to 
	// the square root of the number (inclusive), then it is not prime
	for (int i = 2; i <= sqrtNum; i++){
		if (number%i == 0)
			return 0;
	}	
	return 1;
}

int countPrime(int m, int n){
	/*
	 *Counts the number of prime numbers between two positive integers.
	 *Parameters: m is an int that is a positive number we are searching for primes
	 *greater than.
	 *n is an int that is a positive number we are searching for primes less than.
	 *Returns: a int representing the number of prime numbers between m and n.
	*/
	int count = 0;

	for (int i = m+1; i < n; i++){
		if (checkPrime(i))
			count++;
	}
	return count;
}

int main(){
	int m;
	int n;
	
	// check for invalid inputs (negative numbers, not numbers, missing input)
	if((scanf("%d%d", &m, &n) != 2) || m <= 0 || n <= 0){
		fprintf(stderr, "Two positive integers not entered\n");
		return 1;
	}

	printf("%d\n", countPrime(m, n));
	return 0;
}

