COMPILER = g++
CFLAGS = -std=c++20 -O3

INCLUDES = src/grid.cpp src/cell.cpp src/application.cpp

INFILE = src/main.cpp
OUTFILE = bin/wfc-test

test: build
	cd bin; ../$(OUTFILE); cd ..

build: $(INFILE) $(INCLUDES)
	$(COMPILER) $(CFLAGS) -o $(OUTFILE) $(INFILE)

clean:
	rm -rf bin/
	mkdir bin

.PHONY: build, test, clean
