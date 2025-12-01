# 本地模型 CI/CD 实现指南

## 📋 场景说明

**你的情况：**
- ✅ 模型安装在本地（不在 GitHub 上）
- ✅ 代码只在本地运行
- ✅ 需要实现 CI/CD 工作流

**关键点：**
- CI/CD 环境（GitHub Actions）**没有**你的本地模型
- 测试需要使用 **Mock（模拟对象）** 替代真实模型
- 代码质量检查不依赖模型

---

## 🎯 CI/CD 工作流设计

### 核心策略

```
本地环境（有模型）          CI/CD 环境（无模型）
├── 运行真实测试            ├── 运行 Mock 测试
├── 加载真实模型            ├── 使用 Mock 对象
└── 完整功能验证            └── 代码逻辑验证
```

### 工作流步骤

1. **代码质量检查** - 不依赖模型 ✅
2. **单元测试（Mock）** - 使用模拟对象 ✅
3. **前端检查** - 不依赖模型 ✅
4. **Docker 构建** - 不依赖模型 ✅

---

## 🔧 配置说明

### 1. CI/CD 配置文件（已配置）

`.github/workflows/ci.yml` 已经设置了：

```yaml
test:
  name: Unit Tests (pytest)
  steps:
    - name: Run pytest
      run: pytest tests/ -v --cov=engine --cov-report=xml
      env:
        SKIP_MODEL_LOAD: "true"  # ← 关键：跳过模型加载
```

**作用：** 告诉测试环境不要加载真实模型。

---

### 2. 测试配置（已配置）

`tests/conftest.py` 已经配置了 Mock：

```python
@pytest.fixture(autouse=True)
def mock_model_loading():
    """在 CI 环境中自动 mock 模型加载"""
    if os.getenv("SKIP_MODEL_LOAD", "false").lower() == "true":
        # 使用 Mock 对象替代真实模型
        with patch("engine.models.AutoModelForCausalLM.from_pretrained"):
            yield
```

**作用：** 当 `SKIP_MODEL_LOAD=true` 时，自动使用 Mock 对象。

---

## 🚀 如何使用

### 步骤 1：推送代码到 GitHub

```bash
# 1. 添加所有文件
git add .

# 2. 提交代码
git commit -m "添加 CI/CD 配置"

# 3. 推送到 GitHub
git push origin main
```

### 步骤 2：自动触发 CI/CD

当你推送代码后，GitHub Actions 会自动：

1. ✅ **代码质量检查** - ruff, black, isort
2. ✅ **运行测试** - 使用 Mock，不加载真实模型
3. ✅ **前端检查** - ESLint + 构建
4. ✅ **Docker 构建** - 构建镜像

### 步骤 3：查看结果

1. 打开 GitHub 仓库
2. 点击 **"Actions"** 标签
3. 查看运行结果：
   - ✅ 绿色 = 通过
   - ❌ 红色 = 失败

---

## 🧪 本地测试 vs CI 测试

### 本地测试（有模型）

```bash
# 不设置环境变量，使用真实模型
pytest

# 或者明确使用真实模型
SKIP_MODEL_LOAD=false pytest
```

**特点：**
- 加载真实模型
- 测试完整功能
- 运行时间较长

### CI 测试（无模型）

```bash
# 设置环境变量，使用 Mock
SKIP_MODEL_LOAD=true pytest
```

**特点：**
- 使用 Mock 对象
- 测试代码逻辑
- 运行速度快

---

## 📝 测试文件说明

### 当前测试文件

#### `tests/test_server.py` - 服务器测试

```python
@pytest.mark.unit
def test_health_endpoint():
    """测试健康检查端点"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

**说明：** 这个测试不依赖模型，可以在 CI 中正常运行。

#### `tests/test_models.py` - 模型测试

```python
@pytest.mark.unit
def test_model_manager_singleton():
    """测试 ModelManager 单例模式"""
    manager1 = ModelManager()
    manager2 = ModelManager()
    assert manager1 is manager2
```

**说明：** 这个测试也不依赖模型加载，可以在 CI 中运行。

---

## 🔍 验证 CI/CD 是否正常工作

### 方法 1：查看 GitHub Actions

1. 打开你的 GitHub 仓库
2. 点击 **"Actions"** 标签
3. 查看最新的运行记录

**应该看到：**
```
✓ Code Quality Check (通过)
✓ Unit Tests (通过)
✓ Frontend Lint & Build (通过)
✓ Docker Image Build (通过)
```

### 方法 2：本地模拟 CI 环境

```bash
# 设置环境变量，模拟 CI 环境
export SKIP_MODEL_LOAD=true

# 运行测试
pytest tests/ -v

# 应该看到所有测试通过
```

---

## 🛠️ 常见问题解决

### 问题 1：测试在 CI 中失败，但在本地通过

**原因：** 测试可能依赖真实模型

**解决：**
1. 检查测试是否使用了 `@pytest.mark.skipif` 跳过模型测试
2. 确保 `conftest.py` 中的 Mock 配置正确
3. 查看 CI 日志，找到具体错误

### 问题 2：覆盖率报告显示模型代码未测试

**原因：** 这是正常的，因为使用了 Mock

**解决：**
- 这是预期行为
- Mock 测试主要验证代码逻辑，不测试模型加载
- 真实模型测试在本地进行

### 问题 3：Docker 构建失败

**原因：** Dockerfile 可能尝试下载模型

**解决：**
1. 检查 `docker/Dockerfile` 是否在构建时下载模型
2. 确保 Dockerfile 只构建环境，不下载模型
3. 模型应该在运行时挂载

---

## 📊 CI/CD 工作流完整流程

```
你推送代码 (git push)
    ↓
GitHub 收到代码
    ↓
┌─────────────────────────────────┐
│ 步骤 1: 代码质量检查             │
│  ✓ Ruff (语法检查)              │
│  ✓ Black (格式检查)             │
│  ✓ isort (导入排序)             │
│  → 不依赖模型 ✅                 │
└───────────┬─────────────────────┘
            ↓ (通过)
┌─────────────────────────────────┐
│ 步骤 2: 运行测试                 │
│  ✓ pytest (单元测试)            │
│  ✓ 使用 Mock 对象               │
│  ✓ SKIP_MODEL_LOAD=true         │
│  → 不加载真实模型 ✅             │
└───────────┬─────────────────────┘
            ↓ (通过)
┌─────────────────────────────────┐
│ 步骤 3: 前端检查                 │
│  ✓ ESLint (代码检查)            │
│  ✓ Build (构建测试)             │
│  → 不依赖模型 ✅                 │
└───────────┬─────────────────────┘
            ↓ (通过)
┌─────────────────────────────────┐
│ 步骤 4: Docker 构建              │
│  ✓ 构建镜像                      │
│  ✓ 不下载模型                   │
│  → 只构建环境 ✅                 │
└───────────┬─────────────────────┘
            ↓ (通过)
┌─────────────────────────────────┐
│ ✅ 所有检查通过！                │
│ 代码可以合并                     │
└─────────────────────────────────┘
```

---

## 🎯 最佳实践

### 1. 本地测试使用真实模型

```bash
# 本地开发时，使用真实模型测试
pytest  # 不设置 SKIP_MODEL_LOAD，使用真实模型
```

### 2. CI 测试使用 Mock

```bash
# CI 环境中，自动使用 Mock
SKIP_MODEL_LOAD=true pytest
```

### 3. 分离测试类型

- **单元测试** (`@pytest.mark.unit`) - 不依赖模型，CI 中运行
- **集成测试** (`@pytest.mark.integration`) - 可能需要模型，本地运行

### 4. 代码提交前检查

```bash
# 提交前，先本地检查
ruff check .
black --check .
pytest -m unit  # 只运行单元测试
```

---

## 📚 相关文件

- `.github/workflows/ci.yml` - CI/CD 配置
- `tests/conftest.py` - Mock 配置
- `tests/test_server.py` - 服务器测试
- `tests/test_models.py` - 模型测试
- `pyproject.toml` - pytest 配置

---

## ✅ 检查清单

在实现 CI/CD 前，确保：

- [ ] `.github/workflows/ci.yml` 存在
- [ ] `tests/conftest.py` 配置了 Mock
- [ ] 测试设置了 `SKIP_MODEL_LOAD=true`
- [ ] 测试不依赖真实模型加载
- [ ] Dockerfile 不下载模型

---

## 🎓 总结

**关键点：**

1. ✅ **CI/CD 环境没有模型** - 使用 Mock 替代
2. ✅ **测试分为两类** - 单元测试（CI）和集成测试（本地）
3. ✅ **环境变量控制** - `SKIP_MODEL_LOAD=true` 启用 Mock
4. ✅ **代码质量检查** - 不依赖模型，可以在 CI 中运行

**工作流：**
- 本地：使用真实模型，完整测试
- CI：使用 Mock，快速验证代码逻辑

---

**现在你的 CI/CD 已经配置好了！** 推送代码到 GitHub，就会自动运行检查。

