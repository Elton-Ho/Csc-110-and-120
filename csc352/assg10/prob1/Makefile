mymake2 : dependencyGraph.o mymake2.o
	gcc dependencyGraph.o mymake2.o -o mymake2
dependencyGraph.o : dependencyGraph.c dependencyGraph.h
	gcc -Wall dependencyGraph.c -c 
mymake2.o : mymake2.c dependencyGraph.h
	gcc -Wall mymake2.c -c 
.PHONY: clean
clean :
	rm *.o mymake2
