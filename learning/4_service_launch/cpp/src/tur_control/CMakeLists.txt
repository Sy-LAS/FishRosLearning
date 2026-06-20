cmake_minimum_required(VERSION 3.8)
project(tur_control)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(turtlesim REQUIRED)
find_package(interfaces REQUIRED)
find_package(rcl_interfaces REQUIRED)

add_executable(turtle src/turtle.cpp)
ament_target_dependencies(turtle rclcpp geometry_msgs turtlesim interfaces rcl_interfaces)

install(TARGETS
  turtle
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY
  ../../launch/
  DESTINATION share/${PROJECT_NAME}/launch
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
