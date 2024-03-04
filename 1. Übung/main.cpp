#include <iostream>

enum options{
    ADD = 1,
    DEL,
    IMPORT,
    SEARCH,
    PLOT,
    SAVE,
    LOAD,
    QUIT
};

class stock{
    public:
        std::string date;
        std::string name;
        std::string abbr;
        std::string wkn;
        float open;
        float high;
        float low;
        float close;
        float adj_close;
        int volume;
};

int main(){

    int input;

}