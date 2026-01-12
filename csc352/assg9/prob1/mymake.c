#include "dependencyGraph.h"
#include <ctype.h>
/*
 * File: mymake.c
 * Author: Elton Ho
 * Purpose: Process the input in order to call the proper functions to build
 * and use the dependency graph. Note the usage is 'mymake makefile target' 
 * such that the graph is created using the makefile and the target is the src
 * node for the traversal to print the traversal and the commands of the nodes
 * we reached along the way. The makefile should follow 
 * target : dependency1 dependency2 ...
 * /t command1
 * ...
 * where /t represents a tab.
 */

/*
 *Deals with the collons in the inputStr that contains the target name before
 *the collon and the list of dependencies after the collon. It assumes its an
 *error if the inputStr contains more than 1 collon.
 *Parameters: inputStr is the string containing the name of the target and its
 *dependencies.
 *dependenciesStr is the pointer to the str representing the list of the 
 *target's dependencies.
 *makeFile is the pointer to the FILE that represents the makefile we might 
 *need to close.
 *Returns: an int representing how many collons we say in inputStr.
 */
int handleCollon (char* inputStr, char** dependenciesStr, FILE* makeFile){
	int collonCount = 0;
	char* currChar = inputStr;
	while (*currChar) { // look for colons as dependencies are after them 
		if (*currChar == ':') {
			collonCount++;
			if (collonCount > 1) {
				fprintf(stderr, 
					"Too many ':' on definition line: %s", 
					inputStr);
				freeGraph(); free(inputStr); fclose(makeFile);
				exit(1);
			}
			*currChar = '\0'; // targetStr stops before the collon
			// everything after the colon is for dependencies
			*dependenciesStr = currChar + 1;
		}
		currChar++;
	}
	return collonCount;
}

/*
 *Calls the proper commands to add a target and its dependencies into the graph
 *based on the inputStr. We assume we want to follow the format of a makefile
 *that only allows 1 target to be declared before the collon and that a target
 *can only be declared once. Having no dependencies is allowed.
 *Parameters: inputStr is the string containing the name of the target and its
 *dependencies.
 *targetNode is the pointer to the pointer of the node that is the target we 
 *want to create if it doesn't exist already and add dependencies to it.
 *makeFile is the pointer to the FILE that represents the makefile we might 
 *need to close.
 *Returns: None.
 */
void processGraphCreation(char* inputStr, node** targetNode, FILE* makeFile){
	char* targetStr = inputStr, trimmedTargetStr[65];
	char* dependenciesStr, dependencyName[65], errStr[2];
	int newIndex;
	int collonCount = handleCollon(inputStr, &dependenciesStr, makeFile);
	// trim leading and trailing spaces
	int retVal = sscanf(targetStr, "%64s%1s", trimmedTargetStr, errStr); 
	if (retVal < 1) return; // blank line
	if (collonCount == 0) {
		fprintf(stderr, "No ':' on definition line: %s", targetStr);
		freeGraph(); free(targetStr); fclose(makeFile);
		exit(1);
	}
	if (retVal > 1) {
		fprintf(stderr, "Not exactly 1 target %s\n", targetStr);
		freeGraph(); free(targetStr); fclose(makeFile);
		exit(1);

	}
	*targetNode = addNode(trimmedTargetStr); // find node otherwise create 
	if ((*targetNode)->target) { // node was found and was marked a target
		fprintf(stderr, "Target, %s, declared more than once\n", 
			trimmedTargetStr);
		freeGraph(); free(targetStr); fclose(makeFile);
		exit(1);
	}
	(*targetNode)->target = 1; // mark it a target for next time
	// add dependencies
	while (sscanf(dependenciesStr, "%64s%n", dependencyName, &newIndex)>0) {
		node* dependencyNode = addNode(dependencyName);
		addEdge (*targetNode, dependencyNode);
		dependenciesStr += newIndex;
	}
}

/*
 *Look through the lines of the makeFile to create the target and its 
 *dependencies and add the commands to the target. We assume that the beginning 
 *of the make file must not be a command (ignoring empty lines).
 *Parameters: makeFile is the pointer to the FILE that we want to process the 
 *lines of.
 *Returns: None.
 */
void processMakeFile(FILE* makeFile) {
	char* inputStr = NULL, test[2];
	size_t size = 0;
	node* targetNode = NULL;
	int retVal = getline(&inputStr, &size, makeFile), spaceCount = 0; 
	while (retVal != EOF) {
		// we start by defining the target and its dependencies
		if (*inputStr == '\t' && sscanf(inputStr, "%1s", test) > 0)  {
			// non empty line with a tab when there are no targets 
			fprintf(stderr, "command without a target: %s", 
				inputStr);
			freeGraph(); free(inputStr); fclose(makeFile);
			exit(1);
		}
		processGraphCreation(inputStr, &targetNode, makeFile);
		retVal = getline(&inputStr, &size, makeFile);
		// put commands into the graph if there are any for the target
		while (retVal != EOF && *inputStr == '\t' && targetNode) {
			// ignore leading spaces
			while (isspace(*(inputStr + spaceCount))) spaceCount++;
			// remove lagging spaces
			int spaceCountTail = strlen(inputStr) - 1;
			while(isspace(*(inputStr + spaceCountTail)) && 
				spaceCountTail > 0) {
				*(inputStr + spaceCountTail) = '\0';
				spaceCountTail --;
			}
			// add a new line after the last char
			*(inputStr + spaceCountTail + 1) = '\n'; 
			if (spaceCountTail != 0) // if whole thing is not spaces
				setCommand(targetNode, inputStr + spaceCount);
			retVal = getline(&inputStr, &size, makeFile);
		}
	}
	free(inputStr);
}

/*
 *Looks for a target in our linked list of nodes with a certain name and 
 *traverses the graph and print as desired if we found that target. We assume
 *that it can't be a dependency and must exist in the graph.
 *Parameters: targetName is the string representing what should be the name of 
 *a target in our graph for the src of the traversal.
 *Returns: None.
 */
void processTargetInput(char* targetName) {
	node* currNode = head;
	for(; currNode; currNode = currNode->next) {
		if (! strcmp(currNode->name, targetName)){ // found the target
			if (currNode->target) {
				useGraph(currNode);
				return;
			}
			else // error because its a dependency instead
				break;	
		}
	}
	fprintf(stderr, "No target named %s defined\n", targetName);
	freeGraph(); 
	exit(1);
}

int main(int argc, char* argv[]) {
	FILE* makeFile;
	int errSeen = 0;
	if (argc != 3) {
		fprintf(stderr, "Usage: mymake makefile target\n");
		return 1;
	}
	makeFile = fopen(argv[1], "r");
	if (makeFile == NULL) { // problem opening the makefile
		perror(argv[1]);
		return 1;
	}
	processMakeFile(makeFile);
	fclose(makeFile);
	processTargetInput(argv[2]); // 2nd arg is the target name
	freeGraph();
	return errSeen;	
}
