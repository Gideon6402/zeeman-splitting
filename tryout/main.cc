//#define XERR
#include "main.ih"

int main(int argc, char **argv)
{
    vector<int> fileNumbers{1, 2, 3, 5, 6, 9, 11};
    ifstream inFile{ "input.txt" };
    ofstream outFile{ "output.txt" };
    Scanner scanner(inFile, outFile);
    while (scanner.lex())
        ;

    // for (int number: fileNumbers)
    // {
    //     string strNumber = to_string(number);
    //     ifstream inFile{ strNumber + ".txt" };
    //     ofstream outFile{ "processed" + strNumber + ".txt" };
    //     scanner.switchStreams(inFile, outFile);
    //     while (scanner.lex())
    //         ;  
    // }
}
