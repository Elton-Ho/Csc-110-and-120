#include <stdio.h>
#include <stdlib.h>

/*
 * File: count2.c
 * Author: Elton Ho
 * Purpose: Takes in integers from stdin and report the count of those integers 
 * read in in ascending order.
 */

// represents a node in a linked list
typedef struct node{
	int val;
	struct node* next;
} node;

void sortLinkedList(node* head){
	/*
	 *Takes in an head pointer to an linked list of integers and sorts its
	 *linked list in ascending order based on val. We assume each node only 
	 *holds 1 value which is an int. We are swapping the val of each node 
	 *and not swapping the nodes themselves such that the node we are at 
	 *will have the smallest value when compared to the rest of the nodes 
	 *after it.
	 *Parameters: head is a pointer to the head of an linked list of int's.
	 *Returns: None. 
	*/
	if (head==NULL || head->next == NULL){ 
		return;	// an empty or a list of only 1 node is already sorted
	}
	int temp;
	for (node* currI = head; currI; currI = currI->next){
		// make currI have the smallest val of everything after it
		for (node* currJ = currI->next; currJ; currJ = currJ->next){
			// swap currI's val if we found a smaller val after it
			if (currJ->val < currI->val){ 
				temp = currI->val;
				currI->val = currJ->val; 
				currJ->val = temp;
			}
		}	
	}
}

void printCount(node* head){
	/*
	 *Takes in an head pointer to an linked list of integers and prints
	 *that linked list's values in ascending order with its count for each 
	 *unqiue numbers in the linked list. We assume val is an int.
	 *Parameters: head is a pointer to the head of an linked list of int's.
	 *Returns: None.
	*/	
	if (head==NULL){
		return;	
	}
	int count = 0;
	int seen = head->val;
	node* currI;
	for (currI = head; currI; currI = currI->next){
		if (currI->val == seen){
			count++;	
		}
		// print the count we got so far as we are at a new number
		else {
			printf("%d %d\n", seen, count);

			// set up for the new number with a count of 1
			count = 1;	
			seen = currI->val;		
		}
	}
	printf("%d %d\n", seen, count); // print the last number
}
int main(){
	node* linkedListHead = NULL;
	node* newNode;
	int currNum;
	int retVal = scanf("%d", &currNum);
	
	while (retVal > 0){
		// add a new node based on the inputted number
		newNode = malloc(sizeof(node));	
		if (newNode == NULL){
			fprintf(stderr, "Out of memory!\n");
			return 1;	
		}
		newNode->val = currNum;
		newNode->next = linkedListHead;
		linkedListHead = newNode;

		retVal = scanf("%d", &currNum);	
	}
	if (retVal == 0){
		fprintf(stderr, "Error: Non-integer characters in input\n");
		return 1;
	}
	sortLinkedList(linkedListHead);
	printCount(linkedListHead);
}
