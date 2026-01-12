#include <stdio.h>
#include <limits.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

/*
 * File: minDistance.c
 * Author: Elton Ho
 * Purpose: By using a linked list of nodes where each node in themselves
 * contains a linked list of their edges, we determine for the user the 
 * minimum distance between two nodes in a graph. We create the graph based on
 * the file the user passes in the name of as an argument of this program. The
 * file follows the format of "name1 name2 distBetweenThem". The query taken in
 * from stdin follows the format "name1 name2" and what gets printed in stdout
 * is the minimum distance between those two nodes in the graph.
 */

typedef struct node { // doesn't include mark as we will rep marked via a list 
	char* name;
	int minDist;
	struct edge* edges;
	struct node* prev; // makes it easier to detach from the list
	struct node* next;
} node;

typedef struct edge {
	int dist;
	struct node* goesTo;
	struct edge* next;	
} edge;

/*
 *This creates an edge between two nodes for both nodes in the graph. This 
 *assumes that both nodes exists, and the input file states that there should
 *be an edge between them with a distance given in that input file. We also 
 *assume that the two nodes are not the same. We are also assuming that the 
 *edges go both ways in this graph.
 *Parameters: name1Node is a node pointer to the node that has the new edge to 
 *name2Node with a distance of dist.
 *name2Node is a node pointer to the node that has the new edge to name1Node 
 *with a distance of dist.
 *dist is an int representing the distance between the two nodes that share the
 *new edge.
 *Returns: None.
 */
void createEdgeInGraph (node* name1Node, node* name2Node, int dist) {
	edge* newE1 = malloc(sizeof(edge)); 
	edge* newE2 = malloc(sizeof(edge));
	if (newE1 == NULL || newE2 == NULL) {
		fprintf(stderr, "Unable to allocate enough memory");
		exit(1);
	}
	// set up their fields and add them to their respective node's edges
	newE1->goesTo = name2Node; 
	newE2->goesTo = name1Node;
	newE1->dist = dist; 
	newE2->dist = dist;
	newE1->next = name1Node->edges; 
	newE2->next = name2Node->edges;
	name1Node->edges = newE1; 
	name2Node->edges = newE2;
}

/*
 *This creates at most 2 nodes at once in a graph. It will create 2 nodes if 
 *the names are different but if name1 = name2, we will only make 1 node. This
 *assumes there are no duplicate nodes in the graph. This takes in a pointer to
 *a pointer of a node because we want to check in the caller after if the node 
 *for name2 was made to know if we need to create an edge between the two new
 *nodes. We assume that the nodes are checked for their existance in the graph 
 *by the caller, if it isn't found (the node is NULL), then only then must we 
 *create it.
 *Parameters: headLoc is a pointer to a node pointer to the head of the linked 
 *list of nodes of our graph.
 *name1 is a str that is the name of the first node we want to create.
 *name2 is a str that is the name of the second node we might want to create.
 *name1NodeLoc is a pointer to a node pointer to the node that has the name 
 *name1 that needs to be created.
 *name2NodeLoc is a pointer to a node pointer to the node that has the name 
 *name2 that might need to be created.
 *Returns: None.
 */
void createNodesInGraph(
		node** headLoc, 
		char* name1, 
		char* name2, 
		node** name1NodeLoc, 
		node** name2NodeLoc) 
{
	if (! *name1NodeLoc) { // create the first node and add to the graph
		*name1NodeLoc = malloc(sizeof(node));
		if (*name1NodeLoc == NULL) {
			fprintf(stderr, "Unable to allocate enough memory");
			exit(1);
		}
		(*name1NodeLoc)->minDist = INT_MAX;
		(*name1NodeLoc)->name = strdup(name1);
		if ((*name1NodeLoc)->name == NULL) {
			fprintf(stderr, "Unable to allocate enough memory");
			exit(1);
		}
		(*name1NodeLoc)->edges = NULL;
		(*name1NodeLoc)->next = *headLoc;
		(*name1NodeLoc)->prev = NULL;
		if (*headLoc)
			(*headLoc)->prev = *name1NodeLoc;
		*headLoc = *name1NodeLoc;
	}
	if (!strcmp(name1, name2)) return; // strcmp to prevent duplicates
	if (! *name2NodeLoc)  { // create the second node and add to the graph
		*name2NodeLoc = malloc(sizeof(node));
		if (*name2NodeLoc == NULL) {
			fprintf(stderr, "Unable to allocate enough memory");
			exit(1);
		}
		(*name2NodeLoc)->minDist = INT_MAX;
		(*name2NodeLoc)->name = strdup(name2);
		if ((*name2NodeLoc)->name == NULL) {
			fprintf(stderr, "Unable to allocate enough memory");
			exit(1);
		}
		(*name2NodeLoc)->edges = NULL;
		(*name2NodeLoc)->next = *headLoc;
		(*name2NodeLoc)->prev = NULL;
		(*headLoc)->prev = *name2NodeLoc;
		*headLoc = *name2NodeLoc;
	}
}

/*
 *This checks if the two names in a line of the input file is valid. This 
 *assumes that names of only alphabetical letters are considered valid.
 *Parameters: name1 is a str that is the name of the first node we want to 
 *create and/or add an edge for.
 *name2 is a str that is the name of the second node we might want to create 
 *and/or create an edge for.
 *inputStr is a line from the input file to create the graph.
 *Returns: an int of 1 (true) if the name is valid and 0 (false) otherwise.
 */
int isValidNames (char* name1, char* name2, char* inputStr) {
	// iterate over the char of name1 string
	for (int i = 0; *(name1 + i * sizeof(char)) != '\0'; i ++) {
		if (! isalpha(*(name1 + i * sizeof(char)))) {
			fprintf(stderr, "Illegal node name %s\n", inputStr);
			return 0;	
		}
	}
	// iterate over the char of name2 string
	for (int i = 0; *(name2 + i * sizeof(char)) != '\0'; i ++) {
		if (! isalpha(*(name2 + i * sizeof(char)))) {
			fprintf(stderr, "Illegal node name %s\n", inputStr);
			return 0;	
		}
	}
	return 1;
}

/*
 *This updates the graph based on an line of the input file by calling the 
 *proper methods. We return -1 if any error occured during and 0 otherwise.
 *Parameters: inputStr is a line from the input file to create the graph. We 
 *assume that trying to change the distance between an edge already in the 
 *graph is an invalid operation.
 *headLoc is a pointer to a node pointer to the head of the linked list of 
 *nodes of our graph.
 *Returns: -1 if any error occured when updating our graph and 0 otherwise.
 */
int processFileInputLine(char* inputStr, node** headLoc) {
	char name1[65], name2[65], xtraStr[2];
	node* name1Node = NULL, * name2Node = NULL;
	int dist, retVal;
	retVal = sscanf(inputStr, "%64s%64s%d%1s", name1, name2, &dist, xtraStr);	
	if (!isValidNames(name1, name2, inputStr)) return -1;
	if (retVal != 3) {
		fprintf(stderr, "Illegal edge: %s\n", inputStr);
		return -1;
	}
	// check if the two nodes already exists in the graph
	for (node* currNode = *headLoc; currNode; currNode = currNode->next) {
		if (! strcmp(currNode->name, name1))
			name1Node = currNode;
		// else if so if the names are the same, name2Node stays NULL
		else if (! strcmp(currNode->name, name2))
			name2Node = currNode;	
	}
	createNodesInGraph(headLoc, name1, name2, &name1Node, &name2Node);
	if (name2Node) { // same as if name1 != name2
		// check if an edge between name1 and name2 already exists
		edge* currEdge = name1Node->edges;
		for (; currEdge; currEdge = currEdge->next) {
			if (currEdge->goesTo == name2Node) {
				fprintf(stderr, "Repeat Edge: %s\n", inputStr); 
				return -1;
			}
		}
		createEdgeInGraph (name1Node, name2Node, dist);
	}
	return 0;
}

/*
 *This implments Dijkstra's single source algorithm to find the smallest 
 *distance between the src node and other nodes. We assume that the caller 
 *already initializes the graph for this algorithm by setting the src's minDist
 *as 0 and all other nodes' minDist as INT_MAX (representing infinity). Note 
 *that we don't keep a field for if a node is marked because we represent that 
 *by two list here. I choose to do that because we then can actually represent
 *a set of unmarked nodes and a set of marked nodes, so we don't have to 
 *iterate over the whole linked each time to find the nodes that are unmarked.
 *Parameters: headLoc is a pointer to a node pointer to the head of the linked 
 *list of nodes of our graph.
 *Returns: None. 
 */
static void dijkstraSingleSource(node** headLoc) {
	node* marked = NULL;	
	node* unmarked = *headLoc; // start with whole list as unmarked
	while (unmarked) {
		node* currUnmarked = unmarked;
		node* minUnmarked = unmarked;
		// look for the unmarked node with the smallest minDist
		for (; currUnmarked; currUnmarked = currUnmarked->next) {
			if (currUnmarked->minDist < minUnmarked->minDist)
				minUnmarked = currUnmarked;
		}
		// marks minUnmakred: 1. take it out of unmarked
		if (minUnmarked->prev)
			minUnmarked->prev->next = minUnmarked->next; 
		else // minUnmarked is the head
			unmarked = minUnmarked->next;
		if (minUnmarked->next)
			minUnmarked->next->prev = minUnmarked->prev;
		// 2. puts it into the marked as its new head
		if (marked)
			marked->prev = minUnmarked;
		minUnmarked->prev = NULL; minUnmarked->next = marked;
		marked = minUnmarked;
		// update its neighbors
		for (edge* currE = marked->edges; currE; currE = currE->next) {
			// protect against their sum overflowing to a neg #
			if (INT_MAX - marked->minDist > currE->dist) { 
				int newCalDist = marked->minDist + currE->dist;
				if (newCalDist < currE->goesTo->minDist) 
					currE->goesTo->minDist = newCalDist;
			}
		}
	}
	// cleanup for next query by resetting with the new head of linked list
	*headLoc = marked;
}

/*
 *This returns the min distance between the src node and the end node. To do 
 *so, it initializes the graph for Dijkstra's single source algorithm by setting
 *the srcNode's minDist to 0 and all other nodes' minDist as INT_MAX 
 *(representing infinity). We can then simply represent the shortest distance to
 *the end node as the minDist after we called the Dijkstra helper method.
 *Parameters: headLoc is a pointer to a node pointer to the head of the linked 
 *list of nodes of our graph.
 *Returns: the shortest distance to the end node (the minDist of it).
 */
int shortestDistance (node** headLoc, node* srcNode, node* endNode){
	for (node* currNode = *headLoc; currNode; currNode = currNode->next) {
		currNode->minDist = INT_MAX; // represents infinity
	}	
	srcNode->minDist = 0;
	dijkstraSingleSource(headLoc);
	return endNode->minDist;
}

/*
 *This prints out the minimum distance between the two nodes specified in the 
 *input from stdin. Note that no a query of a node to itself will always print
 *0 no matter how you strcutre the graph via the input file. We assume that the
 *query will be on a connected graph so we don't check for that.
 *Parameters: inputStr is a string representing the query for the minimum 
 *distance between two nodes in the graph.
 *headLoc is a pointer to a node pointer to the head of the linked list of nodes 
 *of our graph.
 *Returns: -1 if any error occured when processing the query and 0 otherwise.
 */
int processQuery (char* inputStr, node** headLoc) {
	char srcName[65], endName[65], xtraStr[2];
	node* srcNode = NULL, *endNode = NULL;
	int retVal = sscanf(inputStr, "%64s%64s%1s", srcName, endName, xtraStr);

	if (retVal != 2) {
		fprintf(stderr, "Illegal query: %s\n", inputStr);
		return -1;
	}
	for (node* currNode = *headLoc; currNode; currNode = currNode->next) {
		if (! strcmp(currNode->name, srcName))
			srcNode = currNode;
		if (! strcmp(currNode->name, endName))
			endNode = currNode;
	}
	if (! srcNode) {
		fprintf(stderr, "No node named %s\n", srcName);
		return -1;
	}
	if (! endNode) {
		fprintf(stderr, "No node named %s\n", endName);
		return -1;
	}
	if (srcNode == endNode) 
		printf("0\n");
	else
		printf("%d\n", shortestDistance(headLoc, srcNode, endNode));
	
	return 0;
} 

/*
 *This frees up the memory of our adjacency list. This assumes we don't need 
 *the graph any more and it follows the structure of an adjacency list.
 *Parameters: headLoc is a pointer to a node pointer to the head of the linked 
 *list of nodes of our graph.
 *Returns: None.
 */
void freeDataStruct (node* headNode) {
	node* nextNode = NULL;
	while (headNode) {
		nextNode = headNode->next;
		free(headNode->name); // made using strdup
		edge* nextEdge = NULL;
		while (headNode->edges) {
			nextEdge = headNode->edges->next;	
			free(headNode->edges);
			headNode->edges = nextEdge;
		}
		free(headNode);
		headNode = nextNode;
	}
}

int main(int argc, char* argv[]) {
	char* inputStr = NULL;
	size_t size = 0;
	node* headNode = NULL;
	int errSeen = 0;

	if (argc < 2) {
		fprintf(stderr, "Too few arguments\n");
		return 1;
	}
	FILE* inputFile = fopen(argv[1], "r");
	if (argc > 2) {
		fprintf(stderr, "Too many arguments\n");
		errSeen = 1;
	}
	if (inputFile == NULL) {
		perror(argv[1]);	
		return 1;
	}
	while (getline(&inputStr, &size, inputFile) != EOF) { // make graph 
		if (processFileInputLine(inputStr, &headNode) == -1) {
			errSeen = 1;
		}
	}
	fclose(inputFile);
	while (getline(&inputStr, &size, stdin) != EOF) { // take stdin query
		if (processQuery(inputStr, &headNode) == -1) {
			errSeen = 1;
		}
	}
	free(inputStr);
	freeDataStruct(headNode);
	return errSeen;
}
