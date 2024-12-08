//#include <cstring>
//#include <iostream>
//#include <netinet/in.h>
//#include <sys/socket.h>
//#include <unistd.h>

//write a c++ hello world program

// ports 59101 - 59999

#include <iostream>
#include <vector>
#include <string>

using namespace std;

int main()
{
    vector<string> msg {"Hello", "C++", "World", "from", "VS Code", "and the C++ extension!"};
    
    for (const string& word : msg)
    {
        cout << word << " ";
    }
    cout << endl;

    return 0;
}



