 # ./pkg1/pkg1/node_2.py
 init缺括号
 get_logger有下划线
 
 # echo "source ~/Desktop/fishros/learning/2_node/2.2colcon/install/setup.bash" >> ~/.bashrc
 应该是：~/.bashrc不是 ~./bashrc
代替每次打开终端source



# setup.py
创建包时确定包名否则
### 手动
entry_points={
    'console_scripts': [
    ],
},
加入`'my_node = my_pkg.my_node:main',`



### 创建包时
```
ros2 pkg create my_pkg \
    --build-type ament_python \
    --node-name my_node
```

这样生成的 `setup.py` 里会自动有：
```python
entry_points={
    'console_scripts': [
        'my_node = my_pkg.my_node:main',
    ],
},
```

同时还会自动在 `my_pkg/` 目录下生成 `my_node.py` 模板文件，省去手动配置的麻烦。
