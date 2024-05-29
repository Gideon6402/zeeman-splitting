//#define XERR
#include "main.ih"

int main(int argc, char **argv)
{
    Scanner scanner;
    vector<int> fileNumbers{1, 2, 3, 5, 6, 9, 11};
    for (int number: fileNumbers)
    {
        string strNumber = to_string(number);
        ifstream inFile{ "../ubuntu-data/" + strNumber + ".txt" };
        ofstream outFile{ "../processed-data/" + strNumber + ".txt" };
        scanner.switchStreams(inFile, outFile);
        while (scanner.lex())
            ;
    }
}
