cmake_minimum_required(VERSION 3.8)
project(pkgcpp)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

add_executable(nodecpp src/node2.cpp)
add_executable(functioncpp src/function.cpp)
add_executable(auto_shared src/auto_shared.cpp)
add_executable(lambda src/lambda.cpp)
add_executable(tonoe src/tonoe.cpp)

ament_target_dependencies(nodecpp rclcpp)
ament_target_dependencies(functioncpp rclcpp)
install(TARGETS nodecpp functioncpp auto_shared lambda tonoe DESTINATION lib/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  # skip cppcheck (path contains '+' which breaks its regex)
  set(ament_cmake_cppcheck_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
