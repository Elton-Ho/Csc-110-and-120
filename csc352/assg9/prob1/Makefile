mymake : dependencyGraph.o mymake.o
	gcc dependencyGraph.o mymake.o -o mymake 
dependencyGraph.o : dependencyGraph.c dependencyGraph.h
	gcc -Wall dependencyGraph.c -c
mymake.o : mymake.c dependencyGraph.h
	gcc -Wall mymake.c -c 
