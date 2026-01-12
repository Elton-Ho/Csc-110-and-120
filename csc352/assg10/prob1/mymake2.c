#include "dependencyGraph.h"
#include <ctype.h>
/*
 * File: mymake2.c
 * Author: Elton Ho
 * Purpose: Process the input in order to call the proper functions to build
 * and use the dependency graph. Note the usage is 'mymake2 [-f aMakeFile ] 
 * [aTarget]' such that the graph is created using the aMakeFile and the aTarget
 * is the src node for the traversal to execute the commands of the nodes we 
 * reached along the way. The arguments are optional and the order doesn't 
 * matter. If no arguments are given the defaults are 'myMakefile' as the 
 * makefile and the first target as the target. The makefile should follow 
 * target : dependency1 dependency2 ...
 * /t command1
 * ...
 * where /t represents a tab.
 */

/*
 *Deals with the colons in the inputStr that contains the target name before
 *the colon and the list of dependencies after the collon. It assumes it's an
 *error if the inputStr contains more than 1 colon.
 *Parameters: inputStr is the string containing the name of the target and its
 *dependencies.
 *dependenciesStr is the pointer to the str representing the list of the 
 *target's dependencies.
 *makeFile is the pointer to the FILE that represents the makefile we might 
 *need to close.
 *Returns: an int representing how many colons we saw in inputStr.
 */
int handleCollon (char* inputStr, char** dependenciesStr, FILE* makeFile){
	int colonCount = 0;
	char* currChar = inputStr;
	while (*currChar) { // look for colons as dependencies are after them 
		if (*currChar == ':') {
			colonCount++;
			if (colonCount > 1) {
				fprintf(stderr, 
					"Too many ':' on definition line: %s:%s"
					, inputStr
					, *dependenciesStr);
				freeGraph(); free(inputStr); fclose(makeFile);
				exit(1);
			}
			*currChar = '\0'; // targetStr stops before the colon
			// everything after the colon is for dependencies
			*dependenciesStr = currChar + 1;
		}
		currChar++;
	}
	return colonCount;
}

/*
 *Calls the proper commands to add a target and its dependencies into the graph
 *based on the inputStr. We assume we want to follow the format of a makefile
 *that only allows 1 target to be declared before the colon and that a target
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
	int newI;
	int colonCount = handleCollon(inputStr, &dependenciesStr, makeFile);
	// trim leading and trailing spaces
	int retValTar = sscanf(targetStr, "%64s%1s", trimmedTargetStr, errStr); 
	if (retValTar < 1 && colonCount == 0) return; // blank line
	if (colonCount == 0) {
		fprintf(stderr, "No ':' on definition line: %s", targetStr);
		freeGraph(); free(targetStr); fclose(makeFile);
		exit(1);
	}
	if (retValTar != 1) {
		fprintf(stderr, "Not exactly 1 target %s\n", targetStr);
		freeGraph(); free(targetStr); fclose(makeFile);
		exit(1);
	}
	*targetNode = addNode(trimmedTargetStr); // finds node, otherwise create
	if ((*targetNode)->target) { // node was found and was marked a target
		fprintf(stderr, "Target, %s, declared more than once\n", 
			trimmedTargetStr);
		freeGraph(); free(targetStr); fclose(makeFile);
		exit(1);
	}
	(*targetNode)->target = 1; // mark it a target for next time
	// add dependencies
	while (sscanf(dependenciesStr, "%64s%n", dependencyName, &newI) > 0) {
		node* dependencyNode = addNode(dependencyName);
		addEdge (*targetNode, dependencyNode);
		dependenciesStr += newI;
	}
}

/*
 *Look through the lines of the makeFile to create the target and its 
 *dependencies and add the commands to the target. We assume that the beginning 
 *of the makefile must not be a command (ignoring empty lines).
 *Parameters: makeFile is the pointer to the FILE that we want to process the 
 *lines of.
 *Returns: A pointer to the node representing the first target for the default
 *behavior when no target is specified.
 */
node* processMakeFile(FILE* makeFile) {
	char* inputStr = NULL, test[2];
	size_t size = 0;
	node* targetNode = NULL, * firstTarget = NULL;
	int retVal = getline(&inputStr, &size, makeFile), seenFirstTarget = 0; 
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
		if (!seenFirstTarget) {
			seenFirstTarget = 1;
			firstTarget = targetNode;
		}
		retVal = getline(&inputStr, &size, makeFile);
		// put commands into the graph if there are any for the target
		while (retVal != EOF && *inputStr == '\t' && targetNode) {
			int spaceCount = 0;
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
	return firstTarget;
}

/*
 *Looks for a target in our linked list of nodes with a certain name and 
 *traverses the graph and execute its commands as desired if we found that 
 *target. We assume that it can't be a dependency and must exist in the graph.
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

/*
 *Looks for the file we need to open based on what is after the -f argument and
 *handles invalid arguments. If no -f are provided, it is defaulted to 
 *opening myMakefile.
 *Parameters: fileOption is a pointer to an int representing which argument 
 *number is the -f, defaulting to 0 and is needed later for determining where 
 *target declaration is.
 *argc is the length of the argv array.
 *argv is the array of the arguments of the program.
 *Returns: A node representing the first target for when there is no declared
 *target as a argument.
 */
node* openProperFile (int* fileOption, int argc, char* argv[]) {
	FILE* makeFile;
	char* fileName = "";
	for (int i = 1; i < argc; i ++) 
		if (!strcmp(argv[i], "-f"))
			*fileOption = i;
	if (*fileOption) { 
		// too long of a commmand or no makefile after -f
		if (argc > 4 || *fileOption == argc-1) { 
			fprintf(stderr, "Usage: exMymake2 [-f makefile] [target]\n");
			exit(1);
		}
		makeFile = fopen(argv[*fileOption + 1], "r");
		fileName = argv[*fileOption + 1];
	}
	else if (argc > 2) {
		fprintf(stderr, "Usage: exMymake2 [-f makefile] [target]\n");
		exit(1);
	}
	else
		makeFile = fopen("myMakefile", "r");
	if (makeFile == NULL) { // problem opening the makefile
		perror(fileName);
		fclose(makeFile);
		exit(1);
	}
	node* firstTarget = processMakeFile(makeFile);
	fclose(makeFile);
	return firstTarget;
}

int main(int argc, char* argv[]) {
	int errSeen = 0, fileOption = 0; // flag for if we are using the -f option
	node* firstTarget = openProperFile(&fileOption, argc, argv); 
	// look for target name and use graph accordingly
	if (fileOption && fileOption - 1 != 0) // target name before the -f
		processTargetInput(argv[fileOption - 1]); 
	else if (fileOption && fileOption + 2 == argc - 1) // target name after -f file
		processTargetInput(argv[fileOption + 2]); 
	else if (!fileOption && argc == 2) 
		processTargetInput(argv[1]);
	else {
		if (firstTarget)
			processTargetInput(firstTarget->name); // default behavior is the first target 
		else {
			fprintf(stderr, "No targets defined\n");
			return 1;
		}
	}
	freeGraph();
	return errSeen;	
}
