# CI/CD 实施方案

本文档说明如何为 NeuroBreak 项目设置完整的 CI/CD 流程。

## 📋 方案概述

### 1. 单元测试框架 (pytest)

- ✅ 已配置 `pytest` 作为测试框架
- ✅ 支持单元测试和集成测试标记
- ✅ 自动生成代码覆盖率报告
- ✅ 在 CI 环境中跳过模型加载（使用 mock）

### 2. 代码质量工具

- ✅ **ruff**: 快速 Python linter（替代 flake8）
- ✅ **black**: 代码格式化工具
- ✅ **isort**: 导入语句排序工具

## 🚀 快速开始

### 步骤 1: 安装依赖

确保 `requirements.txt` 包含测试和代码质量工具：

```bash
pip install -r requirements.txt
```

### 步骤 2: 运行代码检查

```bash
# 检查代码风格（ruff）
ruff check .

# 检查格式化（black）
black --check .

# 检查导入排序（isort）
isort --check-only .
```

### 步骤 3: 自动修复

```bash
# 自动修复可修复的问题
ruff check --fix .

# 自动格式化代码
black .

# 自动排序导入
isort .
```

### 步骤 4: 运行测试

```bash
# 运行所有测试
pytest

# 运行并生成覆盖率报告
pytest --cov=engine --cov-report=html

# 只运行单元测试
pytest -m unit

# 跳过集成测试
pytest -m "not integration"
```

## 📁 文件结构

```
.
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI/CD 配置
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # pytest 配置和 fixtures
│   ├── test_server.py          # FastAPI 服务器测试
│   └── test_models.py          # 模型管理模块测试
├── pyproject.toml              # 工具配置（black, isort, ruff, pytest）
└── requirements.txt            # 包含 pytest, ruff, black, isort
```

## 🔧 配置说明

### pytest 配置 (`pyproject.toml`)

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
]
```

### ruff 配置

- 检查规则：E (errors), W (warnings), F (pyflakes), B (bugbear), C4 (comprehensions), UP (pyupgrade)
- 行长度：100 字符
- 排除目录：`frontend`, `notebooks`, `build`, `dist`

### black 配置

- 行长度：100 字符
- 目标 Python 版本：3.10, 3.11
- 自动排除：`frontend`, `notebooks`, `venv`

### isort 配置

- 与 black 兼容
- 行长度：100 字符
- 自动识别 `engine` 为第一方包

## 🔄 CI/CD 流程

GitHub Actions 会在以下情况自动运行：

1. **Push 到主分支** (`main`, `master`, `develop`)
2. **创建 Pull Request** 到主分支

### CI 任务流程

```
┌─────────────────────┐
│  Code Quality Check  │  ← ruff, black, isort
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│   Unit Tests        │  ← pytest with coverage
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  Frontend Check     │  ← ESLint + Build
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  Docker Build       │  ← 构建 Docker 镜像
└─────────────────────┘
```

## 📝 编写测试

### 单元测试示例

```python
# tests/test_example.py
import pytest
from engine.example import example_function

@pytest.mark.unit
def test_example_function():
    """测试示例函数"""
    result = example_function("input")
    assert result == "expected_output"
```

### 集成测试示例

```python
@pytest.mark.integration
def test_api_integration():
    """测试 API 集成"""
    # 测试完整的 API 流程
    pass
```

## 🐛 故障排查

### CI 失败常见原因

1. **Lint 失败**
   ```bash
   # 本地运行修复
   ruff check --fix .
   black .
   isort .
   ```

2. **测试失败**
   - 检查测试是否依赖外部资源
   - 确保使用 `SKIP_MODEL_LOAD=true` 环境变量

3. **格式化检查失败**
   ```bash
   # 自动修复
   black .
   isort .
   ```

### 本地验证 CI

在提交前运行：

```bash
# 1. 代码质量检查
ruff check . && black --check . && isort --check-only .

# 2. 运行测试
pytest

# 3. 前端检查
cd frontend && npm run lint && npm run build
```

## 📊 代码覆盖率

查看覆盖率报告：

```bash
# 生成 HTML 报告
pytest --cov=engine --cov-report=html

# 查看报告
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
```

## 🔗 相关文档

- [Pytest 文档](https://docs.pytest.org/)
- [Ruff 文档](https://docs.astral.sh/ruff/)
- [Black 文档](https://black.readthedocs.io/)
- [GitHub Actions 文档](https://docs.github.com/en/actions)

## ✅ 检查清单

在提交代码前，确保：

- [ ] 所有测试通过 (`pytest`)
- [ ] 代码格式正确 (`black --check .`)
- [ ] 导入已排序 (`isort --check-only .`)
- [ ] 没有 lint 错误 (`ruff check .`)
- [ ] 前端代码检查通过 (`cd frontend && npm run lint`)
- [ ] 前端构建成功 (`cd frontend && npm run build`)

