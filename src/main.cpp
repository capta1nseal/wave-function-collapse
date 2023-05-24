// debugging and command line interface
#include <iostream>

// grid data structure
#include <array>

// logic processing for cell restrictions
#include "cell.cpp"

// data and logic for the grid
#include "grid.cpp"

// user interface for the algorithms
#include "application.cpp"


int main(int argc, char* argv[])
{
    Application application {};

    application.run();

    return 0;
}
