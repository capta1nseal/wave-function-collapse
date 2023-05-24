// debugging and command line interface
#include <iostream>


#include "cell.cpp"

#include "grid.cpp"

#include "application.cpp"

int main(int argc, char* argv[])
{
    Application application {};

    application.run();

    return 0;
}
