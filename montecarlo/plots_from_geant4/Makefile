EXE = createTable

ROOTCFLAGS	= $(shell root-config --cflags)
ROOTLIBS	= $(shell root-config --libs)
ROOTGLIBS	= $(shell root-config --glibs)

VPATH    	 = src
INCLUDEDIR		 = -Iinclude



LIBS         = -lm -ldl 
LIBS        += $(ROOTLIBS)
GLIBS        = -L/usr/lib  
GLIBS       += $(ROOTGLIBS)
CC           = g++ 

CFLAGS       =  -O3 -g -Wall -fPIC 
CFLAGS      += $(ROOTCFLAGS)
CFLAGS      += -I/usr/include
CFLAGS		+= $(INCLUDEDIR)



$(EXE): $(EXE).cpp  $(OBJ)
	$(CC) $(CFLAGS) -o $(EXE) $(OBJ)  $(LIBS) $(GLIBS) $(CERNLIBS) $(EXE).cpp 
	@echo "$(EXE) done"	


clean:	
	rm -rf *.o *~ core *.so *.dSYM *Dict* *.dylib $(EXE)

install: 
	cp -f $(EXE) /home/feigao/bin
