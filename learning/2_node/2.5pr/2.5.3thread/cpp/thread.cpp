#include <thread>
#include <vector>
#include <iostream>

class MyThread {
public:
    void func_1(int p1, int p2) {
        /* 线程执行函数 */
        std::cout << "p1: " << p1 << ", p2: " << p2 << std::endl;
    }
    std::thread func_2(int p1, int p2) {
        std::thread t(&MyThread::func_1, this, p1, p2); // 创建线程（最核心）
        return t; // 返回线程对象，为了join准备
    }
};

int main() {
    MyThread pa;
    std::vector<std::thread> ts;
    ts.push_back(pa.func_2(1, 2)); // 使用线程（并行）
    ts.push_back(pa.func_2(3, 4));
    ts.push_back(pa.func_2(5, 6));
    // join阻塞，确保子线程执行完整
    for (auto& t : ts) {
        t.join();
    }
    return 0;
}
