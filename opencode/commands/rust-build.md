---
description: 修复 Rust 构建错误和借用检查器问题
agent: build
subtask: true
---

# Rust 构建命令

修复 Rust 构建、clippy 和依赖错误：$ARGUMENTS

## 你的任务

1. **运行 cargo check**：`cargo check 2>&1`
2. **运行 cargo clippy**：`cargo clippy -- -D warnings 2>&1`
3. **逐个修复错误**
4. **验证修复不引入新错误**

## 常见 Rust 错误

### 借用检查器

```
cannot borrow `x` as mutable because it is also borrowed as immutable
```

**修复**：先结束不可变借用再获取可变借用；仅在有充分理由时 clone

### 类型不匹配

```
mismatched types: expected `T`, found `U`
```

**修复**：添加 `.into()`、`as` 或显式类型转换

### 缺少导入

```
unresolved import `crate::module`
```

**修复**：修正 `use` 路径或声明模块

### 生命周期错误

```
does not live long enough
```

**修复**：使用拥有所有权的类型或添加生命周期标注

## 修复顺序

1. **构建错误** — 代码必须能编绎
2. **Clippy 警告** — 修复可疑结构
3. **格式化** — `cargo fmt` 合规

## 验证

修复后：

```bash
cargo check                  # 应成功
cargo clippy -- -D warnings  # 不允许警告
cargo fmt --check            # 格式化应通过
cargo test                   # 测试应通过
```

---

**重要**：只修复错误，不重构，不改进。用最小变更让构建通过。
