#include <iostream>
#include <algorithm>
int main()
{
    auto lam_1 = [](int a,int b) -> int { return a + b; };
    int op1 = lam_1(3, 4);
    auto lam_2 = [op1]() -> void { std::cout << "The sum is: " << op1 << std::endl; };
    lam_2();
    return 0;
}