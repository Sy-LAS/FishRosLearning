import threading
class MyThread:
    def func_1(self,p1,p2):
        """ thread function """
        print(f"p1: {p1}, p2: {p2}")
    def func_2(self,p1,p2):
        thread=threading.Thread(target=self.func_1,args=(p1,p2))#创建线程（最核心）
        thread.start()#启动线程
        return thread#为了join准备
def main():
    pa=MyThread()
    ts=[]
    ts.append(pa.func_2(1,2))#使用线程（并行）
    ts.append(pa.func_2(3,4))
    ts.append(pa.func_2(5,6))
    #join阻塞，确保子线程执行完整
    for t in ts:  
        t.join()  
if __name__=="__main__":
    main()

