//#define XERR
#include "main.ih"

int main(int argc, char **argv)
{
    // ifstream inFile{ "../ubuntu_data/1.txt" };
    // ofstream outFile{ "output.txt" };
    // Scanner scanner(inFile, outFile);
    // while (scanner.lex())
    //     ;


    Scanner scanner;
    vector<int> fileNumbers{1};
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
