# 1
### CMakeLists.txt
```c++
cmake_minimum_required(VERSION 3.10)
project(Learning)
add_executable(learning hello_world.cpp)
```
1. 作用：替代`g`
2. 编译：
	1. 终端
	```bash
	cmake.# 生成 Makefile
	make# 编译
	```
	2. `colcon build`
		1. 在workspace（`src`）内根目录文件夹的终端中，用`--packages-select <pkg_name>`选择编译
			1. 而非换终端
			2. 建包直接在`src`终端中
3. 改环境
	1. 每次打开终端`source`
	2. 改`./bashrc`(~/.bashrc不是 ~./bashrc)

# 2 node
## 2.1 node_py
```python
import rclpy
from rclpy.node import Node
  
def main():
    rclpy.init()
    node=Node("first_python")
    node.get_logger().info("1")
    rclpy.spin(node)
    rclpy.shutdown()
if __name__=="__main__":
    main()
```

## 2.2 node_cpp
```cpp
#include "rclcpp/rclcpp.hpp"
int main(int argc,char** argv)
{
    rclcpp::init(argc,argv);
    auto node = std::make_shared<rclcpp::Node>("node_1");
    RCLCPP_INFO(node->get_logger(),"2");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
```
1. 第 2 行：`char** argc`❌， 为 `char** argv`
2. 第 6 行：`rclcp` ❌，为 `rclcpp`
3. 第 7 行：`rclcpp::shutdown` 别少 `()`
4. 第 8 行：`return 0` 别少 `;`

##### CMakeList.txt
```CMake
find_package(rclcpp REQUIRED)
target_include_directories(node PUBLIC ${rclcpp_INCLUDE_DIRS})
target_link_libraries(node ${rclcpp_LIBRARIES})
```

## 2.2 pkg_py
```bash
ros2 pkg create <pkg_name> --buili-type ament_python --license MIT
```
1. `./pkg1/pkg1/node_2.py`
	 1. init缺括号
	2. get_logger有下划线
2. `setup.py`
```python
entry_points={
    'console_scripts': [
    ],
},
```
加入`'NodeName = PkgName.FileName:FuncName',`
###### 或者创建包时
```
ros2 pkg create my_pkg  --build-type ament_python  --node-name my_node
```

#### 运行
```bash
ros2 run pkg_name node_name
```

## 2.3 pkg_c++
1. 建包在==对应目录==
2. 建`node.cpp`
3. 改`CMakeLists.txt`(加)
	```cmake
	#(<target_name>%%可执行文件名%% <cpp文件名>)
	add_executable(nodecpp src/node2.cpp）
	
	#代替两行依赖（`include,link`）((只)支持ros2原生库，与`include,link`查找方式有异)
	ament_target_dependencies(nodecpp rclcpp)
	
	#cpp需要手动拷贝
	install(TARGETS nodecpp DESTINATION lib/${PROJECT_NAME})
	```

## 2.4 工作空间（src）
设依赖（定顺序）`<depend>pkg_name<\depend>`

## 2.5算法基础
### 2.5.1 py
1. 类：class
2. 方法：类中def
	1. 初始化函数`__init__(self,p,_1,p_2) -> None`自动执行
	2. 定义时，函数内第一个参数为self
3. 继承：`from import +子(父)+super().` 
```python
from pkg1.pyl import pyl
class ppyl(pyl):
    def __init__ (self,p_1_value:str,p_2_value:str,p_s_value:str)->None
        super().__init__(p_1_value, p_2_value)
        self.p_s = p_s_value
def main():
    node=ppyl("value_1", "value_2", "value_s")
    node.func("value_3")
```

### 2.5.2~3 c++
```cpp
#include "rclcpp/rclcpp.hpp"
class func :public rclcpp::Node
{
private:
    std::string p1_;
    int p2_;
public:
    func(const std::string &node_name, const std::string &p1, int p2):Node(node_name)
    {
        this->p1_ = p1;
        this->p2_ = p2;
    }
    void f2(const std::string &p3)
    {
        RCLCPP_INFO(this->get_logger(), "p1: %s, p2: %d, p3: %s", p1_.c_str(), p2_, p3.c_str());
    }
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<func>("func_node", "param1", 123);
    RCLCPP_INFO(node->get_logger(), "infor");
    node->f2("param3");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
```

##### auto和shared
`auto p1=std::make_shared`
```cpp
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
```

##### lambda
```cpp
#include <iostream>
#include <algorithm>
int main
{
    auto lam_1 = [](int a,int b) -> int { return a + b; };
    int op1 = lam_1(3, 4);
    auto lam_2 = [op1]() -> void { std::cout << "The sum is: " << op1 << std::endl; }
    lam_2()
    return 0;
}
```
1. 记得调用`lam_2`
2. 可执行文件名字在`CMakeLists.txt`的`add_executable`被指定
   
##### 函数包装器
```cpp
    std::function<void(std::string)> free = FreeFunction;

    std::function<void(std::string)> member = std::bind(&MyClass::MemberFunction, MyClass(), std::placeholders::_1);

    std::function<void(std::string)> lambda_func = lambda;
```

##### thread并行
###### python:
1. 创建：`t=threading.Thread(target=Func1,args=(p))`
	- **类`ClassName`内** **函数**`Func2`中
2. 启动：`t.start()`
3. 使用：`p.=ClassName()   // p.func(pv1,pv2) //p.func(pv3,pv4)`
```python
import threading
class MyThread:
    def func_1(self,p1,p2):
        """ thread function """
        print(f"p1: {p1}, p2: {p2}")
    def func_2(self,p1,p2):
        thread=threading.Thread(target=self.func_1,args=(p1,p2))#创建线程（最核心）
        thread.start()#启动线程
        return thread#为join准备
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
```

###### c++:
1. 创建：
	1. 函数：`std::thread fun_2(type p1,type p2){}`
	2. 内部：`std::thread t(&ClassName::fun_1,this,p1,p2)`
2. 使用：`ClassName pa; // pa.fun_2(pv1,pv2) //pa.fun_2(pv3,pv4)`
3. c++构造即启动，不需要`start`
```cpp
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
	    // 创建线程（最核心）
        std::thread t(&MyThread::func_1, this, p1, p2); 
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
```

# 3 topic
## 3.1 终端命令

| `ros2 topic list`                           | 列                   |                                                                                                             |     |
| :------------------------------------------ | :------------------ | :---------------------------------------------------------------------------------------------------------- | :-- |
| `ros2 topic echo <topic>`                   | 内容                  |                                                                                                             |     |
| `ros2 topic info <topic>`                   | 看信息<br>type,pub,sus |                                                                                                             |     |
| `ros2 interface show<interfacename>`        | 看定义<br>             |                                                                                                             |     |
| `ros2 topic pub <topic> <interface> <info>` | 发命令                 | `ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 1.0 , y: -1.0} angular: {z: 1.0} }"` |     |

## 3.2 .1 pub.py
`x_`规范，为成员，非函数/为内参，不外用
###### `self.p_ = self.create_publisher(InterfaceName, 'TopicName', qos)`
```python
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from queue import Queue

class TopicNode(Node):
    def __init__(self,node_name):
        super().__init__(node_name)
        self.get_logger().info(f'{node_name}启动')

        self.q = Queue()#放在较前面,防止回调函数出错

        self.p_ = self.create_publisher(String, 'topic', 10) #核心
        
        timer_period = 0.5  # 定义间隔时间
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):#回调函数
        if self.q.qsize() > 0:
            m_ = self.q.get() #从队列中取出数据
            ms = String()
            ms.data = m_
            self.p_.publish(ms) #发布数据
            self.get_logger().info(f'发布数据: {ms.data}')
            
    def func(self):
        #函数功能
        pass
```

### 3.2.2 sub.py
###### `self.s_ = self.create_subscription(InterfaceName, 'TopicName',self.sub_callback, qos)`
```python
import espeakng
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from queue import Queue
import threading
import time

class SubscriberNode(Node):
    def __init__(self,node_name):
        super().__init__(node_name)
        self.get_logger().info(f'{node_name}启动')
        self.q = Queue()

        self.s_ = self.create_subscription(String, 'topic',self.sub_callback, 10)#核心

        self.t_ = threading.Thread(target=self.speak_thread)
        self.t_.start()

        def sub_callback(self, msg):
            self.q.put(msg.data)
        def speak_thread(self):
            speaker = espeakng.Speaker()
            speaker.set_voice('zh-CN')
            while rclpy.ok():
                if not self.q.empty():
                    t_=self.q.get()
                    self.get_logger().info(f'开始: {t_}')
                    speaker.say(t_)
                    speaker.wait()
                else:#降CPU
                    time.sleep(1)
```

### 3.3.1 pub.cpp
1. 创建：
	1. private指针：`rclcpp::Publisher<InterfaceName>SharedPtr p_;`
	2. 实现：`p_ =this->create_publisher <InterfaceName>::("TopicName",qos)`
2. 使用：`p_:publish(MessageName)`
```cpp
#include "rclcpp"
#include "geometry_msgs/msg/twist.hpp"
#include <chrono>
using namespace std::chrono_literals;//重载ms

class PublisherNode : public rclcpp::Node
{
private://指针
    rclcpp::TimerBase::SharedPtr t_;
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr p_;
public:
    explicit PublisherNode(const std::string & node_name) : Node(node_name)
    {
        p_ = this->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel", 10);  //核心
        t_ = this->create_wall_timer(100ms, std::bind(&PublisherNode::timer_callback, this));
    }

    void timer_callback()
    {
        auto msg = geometry_msgs::msg::Twist();
        msg.linear.x = 0.5;
        msg.angular.z = 0.2;
        p_->publish(msg);//发布
    };
}
```

### 3.3 sub.cpp
`s_=this->create_subscription<InterfaceName>("TopicName",qos,std::bind(&ClassName::FuncName,this,std::placesholders::1))`

## 3.4 实例
### interface
###### 只支持c++定义
*传输用二进制流，通过接口的定义解析*
1. src下建包
	1. （`ros2 pkg create status_interface --build-type ament_cmake --dependencies builtin_interface rosidl_default_generators --license MIT`）
2. 包下创`msg`文件夹、`SystemStatus.msg`文件
	1. `ros2 interface list |grep Time`
	2. 看到`buildin_interfaces/msg/Time`（包名/类型/接口名）
		1. 规定：对于依赖其他包的消息接口-->去除`msg`（变为`buildin_interfaces/Time`）%%因为`.msg`文件本身表示msg,ROS2会补上%%
	3. `CMakeList.txt`
		1. **转化** 消息接口定义文件为库/头文件类
		```cmake
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/SystemStatus.msg" #"相对路径（src）"
  DEPENDENCIES builtin_interface #消息接口的依赖
)
		```
	4. `package.xml`
		1. **声明** 包含消息接口`<member_of_group>rosidl_interface_packages</member_of_group>`
	5. 在src上一级`colcon build`
	6. 查看：`ros2 interface show status_interface/msg/SystemStatus`
### pub.py创建
```python
import rclpy
from status_interfaces.msg import SystemStatus
from rclpy.node import Node
import psutil
import platform

class pub(Node):
    def __init__(self):
        super().__init__('pub')
        self.p_ = self.create_publisher(SystemStatus, 'system_status', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
    def timer_callback(self):
        msg = SystemStatus()
        msg.stamp = self.get_clock().now().to_msg()
        msg.hostname = platform.node()
        msg.cpu_percent = psutil.cpu_percent()
        msg.memory_percent = psutil.virtual_memory().percent
        msg.memory_total = psutil.virtual_memory().total/1024/1024
        msg.memory_available = psutil.virtual_memory().available/1024/1024
        msg.net_sent = psutil.net_io_counters().bytes_sent/1024/1024
        msg.net_recv = psutil.net_io_counters().bytes_recv/1024/1024
        self.get_logger().info('Publishing: "%s"' % msg)
        self.p_.publish(msg)
```

### 错误
1. `builtin_interface` → `builtin_interfaces`
2. 文件名`SystemSatus.msg`->`SystemStatus.msg`
3. 包名`status_interface->status_interfaces`
4. main中，`node=pub("pub")`->`node=pub()`（class中init硬编码，不接受参数）
5. `l_，app`为声明
6. `std::stringstream show_str;`的`;  <<`错用

# 4 service、param、launch
## 4.1 bash
| ==survice==                                                   |              |                                                                       |                                                            |
| :------------------------------------------------------------ | :----------- | :-------------------------------------------------------------------- | :--------------------------------------------------------- |
| `ros2 service list -t`                                        | 列<br>服务 【接口】 |                                                                       |                                                            |
| `ros2 service call <topic> <interface> <yaml>`                | 指令           | `ros2 service call /spawn turtlesim/srv/Spawn "{x: 5.0, y: 5.0}"`<br> | **rqt-plugin-service-Service Call-可视化选service、调参数**        |
| ==parameters==                                                |              |                                                                       |                                                            |
| `ros2 param list`                                             | 列出当前系统中所有参数  | ROS 2 List Parameters                                                 | ROS 2 列出参数                                                 |
| `ros2 param describe <topic> <paramer>`                       | 描述           |                                                                       |                                                            |
| `ros2 param get <topic> <paramer>`                            | 获值           |                                                                       |                                                            |
| `ros2 param set <topic> <paramer> <value>`                    | 设值           |                                                                       |                                                            |
| `ros2 param dump <\topic> <file.yaml>`                        | 获全参文件        |                                                                       |                                                            |
| `ros2 run <pkg> <node> --ros-args --params-files <file.yaml>` | 以参数文件建node   | 传入`argc,argv`<br>                                                     | `rqt-plugins-configuration-Dynamic Recogfigure--可视化栏选中，拉条` |
| `ros2 run <pkg> <node> --ros-args -p <param>=<param_value>`   | 以值run        | `-p`：单参数                                                              |                                                            |



### 4.2.1 interfaces
1. `ros2 pkg create interfaces --dependencies rosidl_default_generators sensor_msgs `
2. srv/Name.srv:
```srv
sensor_msgs/Image image
---
int16 num
float32 use_name
int32 right
int32 top
int32 left
int32 bottom
```
3. `CM...txt,pkg.xml`

### 资源载入
1. （图片）放入`4_service_launch/src/face_srv/resource`文件夹
2. `setup.py`中`setup（data_files=[]），`内，加入`('share/' + package_name + "/resource", [ 'resource/top.png']),`
	1. 放入`4_service_launch/install/face_srv/share/face_srv/resource/top.png`


## service
1. python:`self.s_:self.create_service(InterfaceName,"SrvName",self.CallbackFuncName)`%%SrvName自己定%%
2. cpp:`s_=this->create_service<SrvType>("SrvName",FunctionCallback)`
## client:
1. python:`self.c_:self.create_client(SrvType,"SrvName")`%%同上是%%
	- requist:`r_=InterfaceName.Requist()`
		- **承接**参数`：r_.parameters =p1`
	- 异步：
		1. `f_=self.client.call_async(r_)`
		2. `rclpy.spin_until_future_complete(self,future)`
		3. `r_=f_.result()`
2. cpp:`c_=this->create_client<SrvType> ("CrcName")`
	1. 请求：
		1. 指针：`auto r_=std::make_shared<SetP::Request>()`
		2. 加参：`r_->arameters.push_back(p_)`
		3. 异步：`auto f_=c_->async_send_request(r_)`
		4. 等待：`rclcpp::spin_until_future_complete(this->get_node_base_interface(),f_)`
		5. 结果：`auto r_=f_.get()`
### client示例
```python
def call_set_parameters(self, parameters):
        # 1. 创建一个客户端，并等待服务上线
        client = self.create_client(
            SetParameters, '/face_detection_node/set_parameters')
        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('等待参数设置服务端上线....')
        # 2. 创建请求对象
        request = SetParameters.Request()
        request.parameters = parameters
        # 3. 异步调用、等待并返回响应结果
        future = client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        response = future.result()
        return response

    def update_detect_model(self,model):
        # 1.创建一个参数对象
        param = Parameter()
        param.name = "face_locations_model"
        # 2.创建参数值对象并赋值
        new_model_value = ParameterValue()
        new_model_value.type = ParameterType.PARAMETER_STRING
        new_model_value.string_value = model
        param.value = new_model_value
        # 3.请求更新参数并处理
        response = self.call_set_parameters([param])
        for result in response.results:
            if result.successful:
                self.get_logger().info(f'参数 {param.name} 设置为{model}')
            else:
                self.get_logger().info(f'参数设置失败，原因为：{result.reason}')
```

## param:
1. 声明：
	1. `self.declare_parameter('ParamName','ParamValue')`
	2. `this->declare_parameter("ParamName",ValueName)`
2. 获取：
	1. `self.v_=self.get_parameter("ParamName").value`
	2. `this->get_parameter("ParamName",p_)`%%传给指针`p_`%%
	- e.g.`self.set_parameters([rclpy.Parameter('face_locations_model', rclpy.Parameter.Type.STRING, 'cnn')])` 
3. 承接：`r_.parameter =p1`
4. 设/改值：
	1. python:
	2. `self.set_parameter(rclpy.Parameter('ParamName',rclpy.Parameter.Type.ParamType,ParamValue))`
		1. `self.set_parameters([rclpy.Parameter(...),rclpy.Parameter(...)])`
	3. c++:
		1. `this->set_parameter(rclcpp.Parameter("ParamName",ParamValue))`
		2. 
		-  `rclcpp.Parameter`是唯一参数，可重载进set_parameter
		- type可省，让ros2自推断
5. **注册回调**：
	1. `add_on_set_parameters_callback(self.p_callback)`
	2. `b_=this->add_on_set_param_callback(p_cb)`
## launch
`def generate_launch_description():`%%固定参数名%%
- PkgName：终端所取
- Exeable：CMakeLiats.txt中add_exe所取
- name：现取（覆盖NodeName）
1. 声明：`a_d_=launch.actions.DeclareLaunchArgument('Launch_ParamName',default_value='ParamValue')`
2. 动作
	1. 替换：（参数：launch->node）
	- `parameters=[{'Node_ParamName':launch.substitutions.LaunchConfiguration('Launch_ParamName',default_value='ParamValue')}]`
	1. 嵌套：
		1. `n_=launch.action.IncludeLaunchDescription(launch.launch_description_source.PythonLaunchDescriptionSource(p_))`
		2. `p_=[get_package_share_dictionary('PkgName'),\launch\,FileName.launch.py]`
	2. 日志：`l_=launch.acion.LogInfo(msg=[str(Msg)])`
	3. 执行：`e_=launch.action.ExecuteProcess(cmd=['Command']，condition=launch.conditions.IfCondition(Bool))`
		- 条件判断⬆️
	4. 组织：`g_=launch.action.GroupAction([t1_,t2_])`
	5. 定时：`t_=launch.action.TimerAction(period=PeriodTimmeName ,action=[ActionName])`
	6. 事件（注册，激发，定先后）：`launch.actions.RegisterEventHandle(event_handle=launch.event_handers.OnProcessExit(target_action=Target_ActionName,on_exit=[Dependencies_ActionNode],)`

##### 基础示例：
```python
import launch
import launch_ros
def generate_launch_description():
	action_declare_arg_bg_g = launch.actions.DeclareLaunchArgument('background_g', default_value='0.0')
    turcrl_=launch_ros.actions.Node(
        package='tur_control',
        executable='turtle',
        parameters=[{'background_g': launch.substitutions.LaunchConfiguration('background_g',default_value='0.0')}],
        name='tur_control'
    )

    trusim_=launch_ros.actions.Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='turtlesim_node'
    )
  
    return launch.LaunchDescription([
        turcrl_,
        trusim_
    ])
```
##### 函数展示
```python
import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
def generate_launch_description():
    a_d_start_rqt_ = launch.actions.DeclareLaunchArgument('start_rqt', default_value='False')
    #替换
    start_rqt = launch.substitutions.LaunchConfiguration('start_rqt')
    #动作1-嵌套
    launch_path_ = [get_package_share_directory('tur_control'), '/launch', '/tur.launch.py']
    action_nested = launch.actions.IncludeLaunchDescription(        launch.launch_description_sources.PythonLaunchDescriptionSource(
            launch_path_
        )
    )
    #动作2-日志
    action_print = launch.actions.LogInfo(
        msg=[str(launch_path_)]
    )
    #动作3-执行
    action_execute = launch.actions.ExecuteProcess(
        cmd=['rqt'],
    #条件判断
        condition=launch.conditions.IfCondition(start_rqt)
    )
    #动作4-组织
    action_group = launch.actions.GroupAction([
    #动作5-定时
        launch.actions.TimerAction(period=2.0,actions=[action_nested]),
        launch.actions.TimerAction(period=5.0,actions=[action_execute]),
    ])
    return launch.LaunchDescription([
        a_d_start_rqt_,
        action_print,
        action_group
    ]) 
```

```python
#动作六 注册事件（激发，定先后）
launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=spawn_entity,
                on_exit=[load_joint_state_controller],)
        ),

```
## 错误
1. `setup（），`->`setup（），`
2. 接口名为`from FolderName.srv import FileName`的`FileName`
3. `rcl_interfaces/srv/patrol.hpp`->`interfaces/srv/patrol.hpp`
4. `return false/true`->`return`      `void`函数      
5. `launch_ros.action.Node`->`launch_ros.actions.Node`

# 5 tools
## tf
| ==tf==                                                                                                                                                |           |
| :---------------------------------------------------------------------------------------------------------------------------------------------------- | :-------- |
| `ros2 run tf2_ros static_transform_publisher --x <X> --y <> --z <> --roll <> --pitch <> --yaw <> --frame-id <father_frame_name> --child-frame-id <~>` | 发布<br>变换  |
| `ros2 run tf2_ros_tf2_echo <father_frame_name> <son_frame_name>`                                                                                      | 查看<br>关系  |
| `3d -rotation-converter`                                                                                                                              | 3d可视化坐标工具 |
| `ros2 topic echo /th_static`                                                                                                                          | 静态        |
| `ros2 topic echo /tf`                                                                                                                                 | 动态        |
### python
1. 创建：
	1. `b_=TransformBroadcaster(self)`
	2. `t_=TransformStampt()`
2. 入参：
	1. 父坐标：`t_.header.frame_id=''`
	2. 子坐标：`t_child_frame_id=''`
	3. 平移：`t_.transform.translation.x=XValue`
	4. 旋转：`t_.transform.rotation.x=q_[1]`
3. 发送：`self.b_.sendTransform(t_)`
4. 暂存：`self.b=Buffer()`
5. 监听：`self.lis_=TransformListener(self.buf_,self)`
6. 获取：`r_=self.b_.lookup_transform('father_FrameName','son_FrameName',rclpy.time.Time(look_TimaName),rclpy.time.Time(Outtime_Name))`
#### 静态
动态：`self.pub_FuncName()->self.t_=self.create_timer(1.0,self.pub_FuncName)`

```python
import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
from tf_transformations import quaternion_from_euler
import math
  
class STFBroadcaster(Node):
    def __init__(self):
        super().__init__('stf_broadcaster')
        self.stfb_=TransformBroadcaster(self)
        self.publish_tf_()
  
    def publish_tf_(self):
        t_=TransformStamped()
        t_.header.stamp=self.get_clock().now().to_msg()
        t_.header.frame_id='base_link'
        t_.child_frame_id='camera_link'
        t_.transform.translation.x=0.5
        t_.transform.translation.y=0.0
        t_.transform.translation.z=0.0
        q_=quaternion_from_euler(math.radians(180),0,0)
        t_.transform.rotation.x=q_[0]
        t_.transform.rotation.y=q_[1]
        t_.transform.rotation.z=q_[2]
        t_.transform.rotation.w=q_[3]
        self.stfb_.sendTransform(t_)
        self.get_logger().info(f'发布静态tf:{t_}')
```

#### 监听
```python
import rclpy
from rclpy.node import Node
from tf2_ros import TransformListener, Buffer#改
from tf_transformations import euler_from_quaternion
import math
class TFB(Node):
    def __init__(self):
        super().__init__('tf_broadcaster')
        self.buf_=Buffer()
        self.lis_=TransformListener(self.buf_,self)
        self.t_=self.create_timer(1.0,self.get_tf)
    def get_tf(self):
        try:
           r_=self.buf_.lookup_transform('base_link','camera_link',rclpy.time.Time(0),rclpy.time.Duration(1.0))//核心
            tf_=r_.transform
            self.get_logger().info(f'平移:{tf_}')
            self.get_logger().info(f'旋转:{tf_.rotation}')
           rot_eul=euler_from_quaternion([tf_.rotation.x,tf_.rotation.y,tf_.rotation.z,tf_.rotation.w])
            self.get_logger().info(f'旋转RPY:{rot_eul}')
            self.get_logger().info(f'平移:{tf_.translation.y}')
        except Exception as e:
            pass
            self.get_logger().info(f'未找到tf:{e}')
```

# 6 sim
## urdf
### xacro创建宏
##### e.g.urdf
```python
<?xml version="1.0">
<robot name="rob">
  <!-- 身体 -->
  <link name="base">
    <visual>
      <origin rpy="0 0 0" xyz="0 0 0"/>
      <geometry>
        <cylinder radius="0.5" length="1"/>
      </geometry>
      <!-- 材料、颜色 -->
      <material name="white">
        <color rgba="1.0 1.0 1.0 0.5"/>
      </material>
    </visual>
    <!-- 碰撞 -->
    <collision>
        <origin rpy="0 0 0" xyz="0 0 0"/>
        <geometry>
            <cylinder radius="${radius}" length="${length}"/>
        </geometry>
        <material name="white">
            <color rgba="1.0 1.0 1.0 0.5"/>
        </material>
    </collision>
    <!-- 质量(惯性) -->
    <xacro:cylinder_inertia m="1.0" r="${radius}" h="${length}"/>
       
  </link>
  <!-- imu -->
  ...
  
  <!-- 连接-->
  </link>
  <!-- joint -->
  <joint name="base_imu" type="fixed">
    <parent link="base"/>
    <child link="imu"/>
    <!-- 子对父偏移/偏转 -->
    <origin rpy="0 0 0" xyz="0 0 0.05"/>
    <!-- 旋转轴 -->
    <axis xyz="0 0 0"/>
    <!-- 限制 -->
    <limit lower="0" upper="0" effort="0" velocity="0"/>
  </joint>
</robot>
```
##### e.g.定义xacro
```xacro
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro">
    <xacro:macro name="wheel_xacro" params="wheel_name xyz">
        <link name="${wheel_name}_link">
            <visual>
                <origin rpy="1.5708 0 0" xyz="${xyz}"/>
                <geometry>
                    <cylinder radius="0.05" length="0.02" />
                </geometry>
                <material name="green">
                    <color rgba="0.0 1.0 0.0 0.8"/>
                </material>
            </visual>
        </link>
  
        <joint name="${wheel_name}_joint" type="continuous">
            <parent link="base_link"/>
            <child link="${wheel_name}_link"/>
            <origin rpy="0 0 0" xyz="${xyz}"/>
            <axis xyz="0 1 0"/>
        </joint>
        
        <!-- gazebo标签 -->
        <gazebo reference="${wheel_name}_link">
            <material>Gazebo/green</material>
            <!-- 摩擦系数（1：切向；2：法向） -->
            <mu1 value="20"/>
            <mu2 value="20"/>
            <!-- 刚度 -->
            <kp value="1000000000"/>
            <!-- 阻尼 -->
            <kd value="20"/>
        </gazebo>
    </xacro:macro>
</robot>
```
### 调用xacro
- 声明：`<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="RobotName">`
- 依赖：`<xacro:include filename="$(find PackageName)/RestPath"/>`
- 调用：`<cacro:XacroName (ParamName="Argument")/>`
```xacro
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="bot">

<xacro:include filename="$(find description)/urdf/bot/base.urdf.xacro"/>

<xacro:include filename=...
...
  
<xacro:base_xacro length="0.12" radius="0.10"/>
<xacro:gazebo_control_plugin/>
</robot>
```