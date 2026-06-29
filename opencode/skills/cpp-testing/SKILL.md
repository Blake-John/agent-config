---
name: cpp-testing
description: 仅在编写/更新/修复 C++ 测试、配置 GoogleTest/CTest、诊断失败或脆弱的测试、或添加覆盖率/消毒器时使用。
origin: ECC
---

# C++ 测试（Agent 技能）

面向 agent 的现代 C++（C++17/20）测试工作流，使用 GoogleTest/GoogleMock 配合 CMake/CTest。

## 使用时机

- 编写新的 C++ 测试或修复现有测试
- 为 C++ 组件设计单元/集成测试覆盖
- 添加测试覆盖率、CI 门控或回归防护
- 配置 CMake/CTest 工作流以实现一致的测试执行
- 调查测试失败或不稳定行为
- 启用消毒器进行内存/竞态诊断

### 不使用场景

- 实现新功能但不涉及测试变更
- 与测试覆盖率或失败无关的大规模重构
- 性能调优但没有需要验证的测试回归
- 非 C++ 项目或非测试任务

## 核心概念

- **TDD 循环**：红 → 绿 → 重构（先写测试，最小修复，然后清理）
- **隔离性**：优先使用依赖注入和假实现，而非全局状态
- **测试布局**：`tests/unit`、`tests/integration`、`tests/testdata`
- **Mock 与 Fake**：mock 用于交互验证，fake 用于有状态行为
- **CTest 发现**：使用 `gtest_discover_tests()` 实现稳定的测试发现
- **CI 信号**：先运行子集，然后运行完整套件，配合 `--output-on-failure`

## TDD 工作流

遵循 红 → 绿 → 重构 循环：

1. **RED（红）**：编写一个失败测试，描述新行为
2. **GREEN（绿）**：实现最小改动以通过测试
3. **REFACTOR（重构）**：在测试保持通过的前提下清理代码

```cpp
// tests/add_test.cpp
#include <gtest/gtest.h>

int Add(int a, int b); // Provided by production code.

TEST(AddTest, AddsTwoNumbers) { // RED
  EXPECT_EQ(Add(2, 3), 5);
}

// src/add.cpp
int Add(int a, int b) { // GREEN
  return a + b;
}

// REFACTOR: simplify/rename once tests pass
```

## 代码示例

### 基本单元测试（gtest）

```cpp
// tests/calculator_test.cpp
#include <gtest/gtest.h>

int Add(int a, int b); // Provided by production code.

TEST(CalculatorTest, AddsTwoNumbers) {
    EXPECT_EQ(Add(2, 3), 5);
}
```

### 测试夹具（gtest）

```cpp
// tests/user_store_test.cpp
// Pseudocode stub: replace UserStore/User with project types.
#include <gtest/gtest.h>
#include <memory>
#include <optional>
#include <string>

struct User { std::string name; };
class UserStore {
public:
    explicit UserStore(std::string /*path*/) {}
    void Seed(std::initializer_list<User> /*users*/) {}
    std::optional<User> Find(const std::string &/*name*/) { return User{"alice"}; }
};

class UserStoreTest : public ::testing::Test {
protected:
    void SetUp() override {
        store = std::make_unique<UserStore>(":memory:");
        store->Seed({{"alice"}, {"bob"}});
    }

    std::unique_ptr<UserStore> store;
};

TEST_F(UserStoreTest, FindsExistingUser) {
    auto user = store->Find("alice");
    ASSERT_TRUE(user.has_value());
    EXPECT_EQ(user->name, "alice");
}
```

### Mock（gmock）

```cpp
// tests/notifier_test.cpp
#include <gmock/gmock.h>
#include <gtest/gtest.h>
#include <string>

class Notifier {
public:
    virtual ~Notifier() = default;
    virtual void Send(const std::string &message) = 0;
};

class MockNotifier : public Notifier {
public:
    MOCK_METHOD(void, Send, (const std::string &message), (override));
};

class Service {
public:
    explicit Service(Notifier &notifier) : notifier_(notifier) {}
    void Publish(const std::string &message) { notifier_.Send(message); }

private:
    Notifier &notifier_;
};

TEST(ServiceTest, SendsNotifications) {
    MockNotifier notifier;
    Service service(notifier);

    EXPECT_CALL(notifier, Send("hello")).Times(1);
    service.Publish("hello");
}
```

### CMake/CTest 快速入门

```cmake
# CMakeLists.txt (excerpt)
cmake_minimum_required(VERSION 3.20)
project(example LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(FetchContent)
# Prefer project-locked versions. If using a tag, use a pinned version per project policy.
set(GTEST_VERSION v1.17.0) # Adjust to project policy.
FetchContent_Declare(
  googletest
  # Google Test framework (official repository)
  URL https://github.com/google/googletest/archive/refs/tags/${GTEST_VERSION}.zip
)
FetchContent_MakeAvailable(googletest)

add_executable(example_tests
  tests/calculator_test.cpp
  src/calculator.cpp
)
target_link_libraries(example_tests GTest::gtest GTest::gmock GTest::gtest_main)

enable_testing()
include(GoogleTest)
gtest_discover_tests(example_tests)
```

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build -j
ctest --test-dir build --output-on-failure
```

## 运行测试

```bash
ctest --test-dir build --output-on-failure
ctest --test-dir build -R ClampTest
ctest --test-dir build -R "UserStoreTest.*" --output-on-failure
```

```bash
./build/example_tests --gtest_filter=ClampTest.*
./build/example_tests --gtest_filter=UserStoreTest.FindsExistingUser
```

## 调试失败

1. 使用 gtest filter 重新运行单个失败的测试
2. 在失败的断言周围添加作用域日志
3. 启用消毒器后重新运行
4. 找到根本原因后扩展到完整测试套件

## 覆盖率

优先使用目标级别设置，而非全局标志。

```cmake
option(ENABLE_COVERAGE "Enable coverage flags" OFF)

if(ENABLE_COVERAGE)
  if(CMAKE_CXX_COMPILER_ID MATCHES "GNU")
    target_compile_options(example_tests PRIVATE --coverage)
    target_link_options(example_tests PRIVATE --coverage)
  elseif(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    target_compile_options(example_tests PRIVATE -fprofile-instr-generate -fcoverage-mapping)
    target_link_options(example_tests PRIVATE -fprofile-instr-generate)
  endif()
endif()
```

GCC + gcov + lcov：

```bash
cmake -S . -B build-cov -DENABLE_COVERAGE=ON
cmake --build build-cov -j
ctest --test-dir build-cov
lcov --capture --directory build-cov --output-file coverage.info
lcov --remove coverage.info '/usr/*' --output-file coverage.info
genhtml coverage.info --output-directory coverage
```

Clang + llvm-cov：

```bash
cmake -S . -B build-llvm -DENABLE_COVERAGE=ON -DCMAKE_CXX_COMPILER=clang++
cmake --build build-llvm -j
LLVM_PROFILE_FILE="build-llvm/default.profraw" ctest --test-dir build-llvm
llvm-profdata merge -sparse build-llvm/default.profraw -o build-llvm/default.profdata
llvm-cov report build-llvm/example_tests -instr-profile=build-llvm/default.profdata
```

## 消毒器

```cmake
option(ENABLE_ASAN "Enable AddressSanitizer" OFF)
option(ENABLE_UBSAN "Enable UndefinedBehaviorSanitizer" OFF)
option(ENABLE_TSAN "Enable ThreadSanitizer" OFF)

if(ENABLE_ASAN)
  add_compile_options(-fsanitize=address -fno-omit-frame-pointer)
  add_link_options(-fsanitize=address)
endif()
if(ENABLE_UBSAN)
  add_compile_options(-fsanitize=undefined -fno-omit-frame-pointer)
  add_link_options(-fsanitize=undefined)
endif()
if(ENABLE_TSAN)
  add_compile_options(-fsanitize=thread)
  add_link_options(-fsanitize=thread)
endif()
```

## 脆弱测试防护

- 切勿使用 `sleep` 进行同步；应使用条件变量或 latch
- 为每个测试生成唯一的临时目录并在测试后清理
- 避免在单元测试中依赖真实时间、网络或文件系统
- 对随机输入使用确定性种子

## 最佳实践

### 应该做

- 保持测试确定性且隔离
- 优先使用依赖注入而非全局变量
- 使用 `ASSERT_*` 作为前置条件，`EXPECT_*` 进行多项检查
- 在 CTest 标签或目录中将单元测试与集成测试分开
- 在 CI 中运行消毒器以检测内存和竞态问题

### 不应做

- 不要在单元测试中依赖真实时间或网络
- 不要使用 sleep 进行同步，当条件变量可用时
- 不要过度 mock 简单的值对象
- 不要在非关键日志上使用脆弱的字符串匹配

### 常见陷阱

- **使用固定临时路径** → 为每个测试生成唯一临时目录并清理
- **依赖墙上时钟时间** → 注入时钟或使用伪时间源
- **不稳定的并发测试** → 使用条件变量/latch 和有界等待
- **隐藏的全局状态** → 在夹具中重置全局状态或移除全局变量
- **过度 mock** → 有状态行为优先使用 fake，仅 mock 交互
- **缺少消毒器运行** → 在 CI 中添加 ASan/UBSan/TSan 构建
- **仅在 debug 构建上做覆盖率** → 确保覆盖率目标使用一致的标志

## 可选附录：Fuzzing / 属性测试

仅在项目已支持 LLVM/libFuzzer 或属性测试库时使用。

- **libFuzzer**：最适合纯函数且 I/O 最少的场景
- **RapidCheck**：基于属性的测试，用于验证不变式

最小化 libFuzzer harness（伪代码：替换 ParseConfig）：

```cpp
#include <cstddef>
#include <cstdint>
#include <string>

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    std::string input(reinterpret_cast<const char *>(data), size);
    // ParseConfig(input); // project function
    return 0;
}
```

## GoogleTest 的替代方案

- **Catch2**：header-only，富有表现力的匹配器
- **doctest**：轻量级，最小编译开销
