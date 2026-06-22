cmake_minimum_required(VERSION 3.8)
project(demo_cpp_tf)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)

add_executable(static_tf_bcast src/static_tf_bcast.cpp)
ament_target_dependencies(static_tf_bcast rclcpp tf2 tf2_ros geometry_msgs tf2_geometry_msgs)

add_executable(dyn_tf_bcast src/dyn_tf_bcast.cpp)
ament_target_dependencies(dyn_tf_bcast rclcpp tf2 tf2_ros geometry_msgs tf2_geometry_msgs)

add_executable(tf_lsnr src/tf_lsnr.cpp)
ament_target_dependencies(tf_lsnr rclcpp tf2 tf2_ros geometry_msgs tf2_geometry_msgs)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

install(TARGETS
  tf_lsnr
  static_tf_bcast
  dyn_tf_bcast
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
