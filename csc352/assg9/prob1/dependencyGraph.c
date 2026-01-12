#include "dependencyGraph.h"

/*
 * File: denpendencyGraph.c
 * Author: Elton Ho
 * Purpose: By using a linked list of nodes where each node in themselves
 * contains a linked list of their edges and a linked list of their commands, we 
 * can mimic a very premature make that can only print its traversal for 
 * checking if a command has to be executed to update a target and commands 
 * that would have been called during that traversal. The process of input to
 * do so will be done in mymake.c. This is just for creating and traversing the
 * linked list/graph.
 */

node* head = NULL; // head node of the linked list of nodes is defined here

/*
 *This adds a node to the linked list, it can be a dependency or a target. This 
 *assumes that the argument is not NULL and that it doesn't matter what order
 *we add to the linked list of nodes. Note that if the node already exists in 
 *the graph, we just return that found node.
 *Parameters: nodeName is the string of the name of the node being added.
 *Returns: The pointer to the node with the name of the argument whether or not
 *it was created or already existed..
 */
node* addNode (char* nodeName) {
	node* currNode = head;
	for(; currNode; currNode = currNode->next) {
		if (! strcmp(currNode->name, nodeName)) { // alr in the graph
			return currNode;	
		}
	}
	node* newNode = malloc(sizeof(node));	
	if (newNode == NULL) {
		fprintf(stderr, "Unable to allocate memory\n");
		exit(1);
	}
	newNode->name = strdup(nodeName);
	if (newNode->name == NULL) {
		fprintf(stderr, "Unable to allocate memory\n");
		exit(1);
	}
	// initialize its feilds and add it to the front of the linked list
	newNode->visited = 0;
	newNode->target = 0;
	newNode->dependencies = NULL;
	newNode->lastDependency = NULL;
	newNode->commands = NULL;
	newNode->lastCommand = NULL;
	newNode->next = head;	
	head = newNode;
	return newNode;
}

/*
 *This adds a edge to the the target's linked list of edges such that the edge
 *goes to a dependency. This assumes that both arguments are not NULL and 
 *duplicates are not suppose to be created.
 *Parameters: target is the pointer to the node that is the target we are 
 *adding an edge to.
 *dependency is the pointer to the node that is the dependency we want the edge
 *to go to.
 *Returns: None.
 */
void addEdge (node* target, node* dependency) {
	edge* currEdge = target->dependencies;
	// check for duplicate dependency in input
	for(;currEdge; currEdge = currEdge->next) {
		if (currEdge->dependsOn == dependency)
			return;
	} 
	edge* newEdge = malloc(sizeof(edge));
	if (newEdge == NULL) {
		fprintf(stderr, "Unable to allocate memory\n");
		exit(1);
	}
	newEdge->dependsOn = dependency;
	newEdge->next = NULL;
	if (target->lastDependency) // non empty linked list of edges
		target->lastDependency->next = newEdge;
	else // the first dependency
		target->dependencies = newEdge;
	target->lastDependency = newEdge;
}

/*
 *This adds a command to the the target's linked list of commands. This assumes
 *the command can be of any length and the arguments are not NULL.
 *Parameters: target is the pointer to the node that is the target we are 
 *adding a command to.
 *commandName is the string representing the command we want to add to the 
 *target's linked list of commands.
 *Returns: None.
 */
void setCommand (node* target, char* commandName) {
	command* newCommand = malloc(sizeof(command));
	if (newCommand == NULL) {
		fprintf(stderr, "Unable to allocate memory\n");
		exit(1);
	}
	newCommand->name = strdup(commandName);
	if (newCommand->name == NULL) {
		fprintf(stderr, "Unable to allocate memory\n");
		exit(1);
	}
	newCommand->next = NULL;
	if (target->lastCommand) // non empty linked list of commands
		target->lastCommand->next = newCommand;
	else // the first command
		target->commands = newCommand;
	target->lastCommand = newCommand;
}

/*
 *This is the post order traversal so that we can print the traversal and the 
 *commands executed in the order they appear in the inputed makefile as 
 *desired. This assumes the target is not NULL and that we want the commands to
 *start with two spaces.
 *Parameters: target is the pointer to the node that is the target we are 
 *starting the traversal from.
 *Returns: None.
 */
static void postOrderTraversal (node* target) {
	if (target->visited)
		return;
	target->visited = 1;
	edge* currEdge = target->dependencies;
	for (; currEdge; currEdge = currEdge->next) {
		postOrderTraversal(currEdge->dependsOn);	
	}
	printf("%s\n", target->name);
	// print the commands in the order they appear in the make file
	command* currCommand = target->commands;
	for (; currCommand; currCommand = currCommand->next) 
		printf("  %s", currCommand->name);
}

/*
 *This resets the visited flag for all nodes for the dfs traversal of the graph
 *and then actually calls the traversal so that we can print the traversal and
 *the commands executed as desired. This assumes the target is not NULL.
 *Parameters: target is the pointer to the node that is the target we are 
 *starting the traversal from.
 *Returns: None.
 */
void useGraph (node* target) {
	node* currNode = head;
	for(; currNode; currNode = currNode->next) {
		currNode->visited = 0;
	}
	postOrderTraversal(target);
}

/*
 *This frees up the memory of our linked list of nodes. This assumes we don't 
 *need the graph any more, and it follows the structure of our graph.
 *Parameters: None.
 *Returns: None.
 */
void freeGraph() {
	while (head) {
		node* nextNode = head->next;
		edge* currEdge = head->dependencies;
		while (currEdge) {
			edge* nextEdge = currEdge->next;
			free(currEdge);
			currEdge = nextEdge;
		}
		command* currCommand = head->commands;
		while (currCommand) {
			command* nextCommand = currCommand->next;
			free(currCommand->name);
			free(currCommand);
			currCommand = nextCommand;
		}
		free(head->name);
		free(head);
		head = nextNode;
	}
}
