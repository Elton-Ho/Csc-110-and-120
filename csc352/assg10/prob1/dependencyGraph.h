/*
 * File: denpendencyGraph.h
 * Author: Elton Ho
 * Purpose: This contains the typedef for the dependency graph and a global 
 * pointer to the head of the graph declaration to make it easier to free the
 * graph. It also has the prototypes for methods that source files may need.
 */

#ifndef DEPENDENCYGRAPH_H
#define DEPENDENCYGRAPH_H
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

typedef struct edge{
	struct node* dependsOn;
	struct edge* next;
} edge; 

typedef struct command{
	char* name;
	struct command* next;
} command;

typedef struct node {
	char* name;
	int visited;
	int target; // make sure a target is not repeated
	edge* dependencies;
	edge* lastDependency; // for easy appending to follow order of input
	command* commands;
	command* lastCommand; // for easy appending to follow order of input
	struct node* next;
} node;

extern node* head; // global head of the linked list of nodes

// prototypes
node* addNode (char* nodeName);
void addEdge (node* target, node* dependency);
void setCommand (node* target, char* commandName);
void useGraph (node* target); 
void freeGraph();
#endif
