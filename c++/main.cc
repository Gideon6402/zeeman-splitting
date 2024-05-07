//#define XERR
#include "main.ih"

int main(int argc, char **argv)
{
    ifstream input("input.txt");

    string line;
    input >> line;
    cout << line;

    Scanner scanner(input, cout);
    while (scanner.lex())
        ;
}
