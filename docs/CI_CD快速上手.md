# CI/CD 快速上手指南（本地模型版）

## 🎯 你的情况

- ✅ 模型安装在本地
- ✅ 代码只在本地运行
- ✅ 需要实现 CI/CD

## ✅ 好消息：已经配置好了！

你的项目已经配置好了 CI/CD，**不需要修改任何代码**！

---

## 🚀 三步实现 CI/CD

### 步骤 1：推送代码到 GitHub

```bash
# 1. 添加所有文件
git add .

# 2. 提交代码
git commit -m "添加 CI/CD 配置"

# 3. 推送到 GitHub
git push origin main
```

### 步骤 2：自动运行 CI/CD

推送后，GitHub Actions 会自动运行：

1. ✅ 代码质量检查（ruff, black, isort）
2. ✅ 运行测试（使用 Mock，不加载真实模型）
3. ✅ 前端检查（ESLint + 构建）
4. ✅ Docker 构建

### 步骤 3：查看结果

1. 打开 GitHub 仓库
2. 点击 **"Actions"** 标签
3. 查看运行结果

---

## 🔑 关键配置说明

### 1. CI/CD 自动跳过模型加载

`.github/workflows/ci.yml` 中已经设置：

```yaml
env:
  SKIP_MODEL_LOAD: "true"  # ← 关键配置
```

**作用：** 告诉测试环境不要加载真实模型。

### 2. 测试自动使用 Mock

`tests/conftest.py` 中已经配置：

```python
if os.getenv("SKIP_MODEL_LOAD", "false").lower() == "true":
    # 自动使用 Mock 对象，不加载真实模型
```

**作用：** 当 `SKIP_MODEL_LOAD=true` 时，自动使用 Mock。

---

## 🧪 本地测试 vs CI 测试

### 本地测试（有模型）

```bash
# 正常运行，使用真实模型
pytest
```

### CI 测试（无模型）

```bash
# CI 自动设置，使用 Mock
SKIP_MODEL_LOAD=true pytest
```

---

## 📊 工作流说明

```
你的代码
    ↓
推送到 GitHub
    ↓
自动触发 CI/CD
    ↓
┌─────────────────────┐
│ 1. 代码质量检查      │ ← 不依赖模型 ✅
│ 2. 运行测试 (Mock)   │ ← 使用 Mock ✅
│ 3. 前端检查         │ ← 不依赖模型 ✅
│ 4. Docker 构建      │ ← 不依赖模型 ✅
└─────────────────────┘
    ↓
所有检查通过 ✅
```

---

## ❓ 常见问题

### Q: CI/CD 会下载模型吗？

**A:** 不会！CI/CD 使用 Mock 对象，不下载真实模型。

### Q: 测试会失败吗？

**A:** 不会！测试已经配置好 Mock，可以在没有模型的情况下运行。

### Q: 如何查看 CI/CD 结果？

**A:** 
1. 打开 GitHub 仓库
2. 点击 "Actions" 标签
3. 查看运行记录

### Q: 本地测试和 CI 测试有什么区别？

**A:**
- **本地测试**：使用真实模型，完整功能测试
- **CI 测试**：使用 Mock，快速验证代码逻辑

---

## ✅ 检查清单

确保以下文件存在：

- [x] `.github/workflows/ci.yml` - CI/CD 配置
- [x] `tests/conftest.py` - Mock 配置
- [x] `tests/test_server.py` - 测试文件
- [x] `tests/test_models.py` - 测试文件

**所有文件都已经创建好了！**

---

## 🎓 总结

**你只需要：**

1. ✅ 推送代码到 GitHub
2. ✅ CI/CD 自动运行
3. ✅ 查看结果

**不需要：**
- ❌ 修改代码
- ❌ 配置模型路径
- ❌ 下载模型到 CI

**一切都已经配置好了！** 🎉

---

## 📚 详细文档

- `docs/本地模型_CI_CD实现指南.md` - 详细说明
- `docs/CI_CD_入门指南.md` - 入门教程
- `.github/workflows/ci.yml` - CI/CD 配置文件

