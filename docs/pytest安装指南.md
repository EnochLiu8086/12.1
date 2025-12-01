# pytest 安装指南

## ✅ 好消息：pytest 已经在 requirements.txt 中！

你的 `requirements.txt` 文件已经包含了 pytest 及其相关依赖：

```txt
pytest==8.3.3
pytest-cov==5.0.0
pytest-mock==3.14.0
httpx==0.27.2
```

---

## 🚀 安装步骤

### 方法 1：安装所有依赖（推荐）

```bash
# 安装项目所有依赖（包括 pytest）
pip install -r requirements.txt
```

**这会安装：**
- ✅ pytest - 测试框架
- ✅ pytest-cov - 覆盖率工具
- ✅ pytest-mock - Mock 工具
- ✅ httpx - HTTP 客户端（用于 FastAPI 测试）
- ✅ 以及其他所有项目依赖

### 方法 2：只安装 pytest

```bash
# 只安装 pytest 相关依赖
pip install pytest pytest-cov pytest-mock httpx
```

---

## 🧪 验证安装

### 检查 pytest 是否安装成功

```bash
# 检查 pytest 版本
pytest --version

# 应该显示：pytest 8.3.3
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行并显示详细信息
pytest -v

# 运行特定文件
pytest tests/test_server.py

# 运行特定测试
pytest tests/test_server.py::test_health_endpoint
```

---

## 🔧 如果安装失败

### 问题 1：pip 版本太旧

```bash
# 升级 pip
python -m pip install --upgrade pip

# 然后重新安装
pip install -r requirements.txt
```

### 问题 2：使用虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 问题 3：使用国内镜像源加速

```bash
# 使用清华镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 📦 依赖说明

### pytest (8.3.3)
- **作用：** 测试框架
- **用途：** 运行所有测试

### pytest-cov (5.0.0)
- **作用：** 代码覆盖率工具
- **用途：** 生成覆盖率报告

### pytest-mock (3.14.0)
- **作用：** Mock 工具
- **用途：** 创建模拟对象（用于测试）

### httpx (0.27.2)
- **作用：** HTTP 客户端
- **用途：** FastAPI 的 TestClient 需要

---

## 🎯 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行测试

```bash
# 运行所有测试
pytest

# 运行并生成覆盖率报告
pytest --cov=engine --cov-report=html
```

### 3. 查看覆盖率报告

```bash
# 打开 HTML 报告
# Windows:
start htmlcov/index.html
# Linux/Mac:
open htmlcov/index.html
```

---

## ✅ 检查清单

安装完成后，确保：

- [ ] `pytest --version` 显示版本号
- [ ] `pytest` 可以运行测试
- [ ] 所有测试通过（或至少能运行）

---

## 🎓 总结

**pytest 已经在 requirements.txt 中，只需要：**

```bash
pip install -r requirements.txt
```

**然后就可以运行测试了：**

```bash
pytest
```

**就这么简单！** 🎉

