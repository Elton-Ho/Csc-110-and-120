#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

/*
 * File: anagrams2.c
 * Author: Elton Ho
 * Purpose: Takes in strings from stdin and prints out on each line the inputs 
 * grouped based on them being anagrams of each other. This is possible through 
 * our special linked list where a word can be an anagramHead if there is no 
 * anagram of this word yet or an anagramNode inside an inner list started by 
 * an anagramHead of its anagrams otherwise. 
*/

struct anagramHead { // start of a anagram linked list
	int* count; // to identify if other nodes belong in this linked list
	char* word;
	struct anagramNode* firstNode;
	struct anagramNode* lastNode;
	struct anagramHead* next; 
};

struct anagramNode{
	char* word;
	struct anagramNode* next;
};

int* createCharCount(char* word){
	/*
	 *Counts the number of occurrance of letters in the word and stores 
	 *the counts in a block of dynamic memory where *(count + 0) would give
	 *the number of a's in the word and *(count + 25) would give the number
	 *of z's in the word. Note that the count is case-insensitive. We are 
	 *assuming that we are only allowing words to be considered valid if 
	 *the word is made up of only alphabetical letters and only counting
	 *those letters.
	 *Parameters: word is the string we want to count for occurrance of
	 *letters. 
	 *Returns: a int pointer that have the occurrance of letters in the 
	 *word where *(count + 0) gives the number of a's in the word and NULL
	 *when the word has an invalid character.
	*/
	int* count = calloc(26, sizeof(int)); // calloc initializes with all 0's
	if (count == NULL){
		fprintf(stderr, "Unable to allocate memory\n");
		exit(1);	
	}
	while (*word != '\0'){
		if (!isalpha(*word))
			return NULL;
		(*(count + (tolower(*word) - 'a'))) ++; // increase the count
		word ++;	
	} 
	return count;
}

int isAnagram(char* word, int* count){
	/*
	 *It tests if a word is an anagram of a word with a particular count of
	 *of letters. We are assumming the count correctly tells the count of 
	 *letters. It is based on the idea that a word is an anagram of another
	 *word if their count of letters are the same and returns based on that.
	 *Parameters: word is the string we want to test if it is an anagram of
	 *the word that have the particular count (of letters). 
	 *count is the int pointer that have the count of letters in the word we
	 *want to use for testing for anagrams.
	 *Returns: a int of -1 if the word is invalid, 0 if the word is not an 
	 *anagram of the word that have the count, 1 if the word is.
	*/
	int* thisWordCount = createCharCount(word);
	if (thisWordCount == NULL)
		return -1;
	for (int i = 0; i < 26; i ++){
		// counts for this letter is not the same so not an anagram
		if (*(thisWordCount + i) != *(count + i)){
			return 0;
		}
	}
	return 1;
}

int addToLinkedList(char* word, struct anagramHead** firstAnaLoc){
	/*
	 *It puts in the word in our special linked list where a word can be an 
	 *anagramHead if there is no anagram of this word yet or an anagramNode 
	 *inside an inner list of its anagrams otherwise. Each anagramHead is 
	 *connected to both its inner list of its anagrams and the next seperate 
	 *anagramHead. We are inserting by appending to the end as we assume the 
	 *'next' node/head is also the next word in occurrence in the input. We
	 *also return -1 if the word is invalid and 0 otherwise.
	 *Parameters: word is the string we want to put into our linked list. 
	 *firstAnaLoc is the memory location of the pointer to the actual head 
	 *of the linked list representing the first anagram to appear in the 
	 *input.
	 *Returns: a int of -1 if the word is invalid and 0 otherwise. 
	*/
	struct anagramHead* currAna;
	struct anagramHead* prevAna; // incase we want to append a new head
	char* errMessage = "Unable to allocate memory\n";
	int isAnaResult;
	if (*firstAnaLoc != NULL){
		for (currAna = *firstAnaLoc; currAna; currAna = currAna->next){
			isAnaResult = isAnagram(word, currAna->count);
			// it is an anagram already in the linked list
			if (isAnaResult == 1){ 				
				// so be a node of an inner list of its anagrams
				struct anagramNode* newNode;
				newNode = malloc(sizeof(struct anagramNode));
				if (newNode == NULL){
					fprintf(stderr, errMessage);
					exit(1);	
				}
				newNode->word = strdup(word);
				newNode->next = NULL;
				// inner list is empty so the first node of it
				if (currAna->firstNode == NULL){
					currAna->firstNode = newNode;
					currAna->lastNode = newNode;
				}
				else{ // append it to the not empty inner list
					currAna->lastNode->next = newNode;
					currAna->lastNode = newNode;
				}
				return 0;
			}
			// found out its an invalid word
			if (isAnaResult == -1){
				return -1;
			}
			prevAna = currAna;
		}
	}
	// test if its a valid word and get its count for a new anagramHead
	int* wordCount = createCharCount(word);
	if (wordCount == NULL){
		return -1;	
	}
	// append a new head to the outer list as its the first of its anagram 
	struct anagramHead* newHead = malloc(sizeof(struct anagramHead));
	if (newHead == NULL){
		fprintf(stderr, errMessage);
		exit(1);	
	}
	newHead->count = wordCount;
	newHead->word = strdup(word);	
	newHead->firstNode = NULL;
	newHead->lastNode = NULL;
	newHead->next = NULL;
	if (*firstAnaLoc == NULL){ // list is empty
		*firstAnaLoc = newHead;	
	}
	else{
		prevAna->next = newHead;
	}
	return 0;
	
}

void printAnagrams(struct anagramHead* head){
	/*
	 *Takes advantage of the structure of the linked list to print out each 
	 *group of anagrams on each line as they occur in the input. That is 
	 *assumming we do want their order to be based on how they occur in the
	 *input and that we allow duplicates. We also assume that any invalid
	 *input has been handled by now and we are safe to print.
	 *Parameters: head is a pointer to the actual head of the linked list
	 *representing the first anagram to appear in the input.
	 *Returns: None.
	*/
	struct anagramHead* currAna;
	struct anagramNode* currNode;
	for (currAna = head; currAna; currAna = currAna->next){
		// print all the anagrams of currAna on 1 line
		if (currAna->firstNode != NULL){
			printf("%s ", currAna->word); // show head first

			// print its other anagrams seperated by spaces
			currNode = currAna->firstNode;
			while (currNode->next){
				printf("%s ", currNode->word);	
				currNode = currNode->next;
			}
			// print the last node as the last one of its anagrams 
			printf("%s\n", currNode->word); 
		}	
		else { // only the head so show it as the last of its anagrams 
			printf("%s\n", currAna->word);	
		}
	}	
}

int main(){
	int errSeen = 0;
	struct anagramHead* head = NULL;
	char inputStr[65];
	int retVal = scanf("%64s", inputStr);
	while (retVal != EOF){
		if (addToLinkedList(inputStr, &head) == -1){
			fprintf(stderr, "Bad word %s\n", inputStr);
			errSeen = 1;
		}
		retVal = scanf("%64s", inputStr);	
	}
	printAnagrams(head);
	return errSeen;
}
