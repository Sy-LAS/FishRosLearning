#include <iostream>
#include <memory>

int main()
{
    auto p1 = std::make_shared<std::string>("存的东西");
    std::cout << "p1的引用计数：" << p1.use_count() << " 指向内存 " << p1.get() << std::endl;
    auto p2=p1;
    std::cout << "p1的引用计数：" << p1.use_count() << " 指向内存 " << p1.get() << std::endl;
    std::cout << "p2的引用计数：" << p2.use_count() << " 指向内存 " << p2.get() << std::endl;
    p1.reset();
    std::cout << "p1的引用计数：" << p1.use_count() << " 指向内存 " << p1.get() << std::endl;
    std::cout << "p2的引用计数：" << p2.use_count() << " 指向内存 " << p2.get() << std::endl;
    return 0;
}
//结果：1,2,2,0,1