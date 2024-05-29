#include "scanner.ih"

enum {
    BEGIN = 7,
};


void Scanner::print_column_name()
{
    std::string matchedStr = matched();
    size_t lengthOfName = matchedStr.length() - BEGIN - 1;
    out() << matched().substr(BEGIN, lengthOfName) << '\n';
}

// 123456789
// nom = "column name"

// Begin of name starts at index 7
