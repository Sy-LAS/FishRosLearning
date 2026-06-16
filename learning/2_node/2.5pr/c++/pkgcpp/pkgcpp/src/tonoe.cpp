#include <iostream>
#include <functional>
void FreeFunction(std::string str)
{
    std::cout << "自由函数：" << str << std::endl;
}

class MyClass
{
public:
    void MemberFunction(std::string str)
    {
        std::cout << "成员函数" << str << std::endl;
    }
};

int main()
{
    auto lambda = [](std::string str) -> void { std::cout << "lambda函数：" << str << std::endl; };
    std::function<void(std::string)> free = FreeFunction;
    std::function<void(std::string)> member = std::bind(&MyClass::MemberFunction, MyClass(), std::placeholders::_1);
    std::function<void(std::string)> lambda_func = lambda;
    free("hello");
    member("world");
    lambda_func("test");
    return 0;
}
