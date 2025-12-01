# Docker 镜像自动推送配置指南

## 📋 配置说明

CI/CD 已配置为自动构建并推送 Docker 镜像到：
1. **Docker Hub** - 公开镜像仓库
2. **GitHub Container Registry (ghcr.io)** - GitHub 的容器仓库

---

## 🔧 配置步骤

### 步骤 1：配置 Docker Hub 密钥（可选）

如果你想推送到 Docker Hub：

1. **登录 Docker Hub**
   - 访问 https://hub.docker.com
   - 如果没有账号，先注册

2. **创建访问令牌**
   - 登录后，点击右上角头像 → Account Settings
   - 选择 Security → New Access Token
   - 创建令牌并复制

3. **在 GitHub 添加密钥**
   - 打开你的 GitHub 仓库
   - Settings → Secrets and variables → Actions
   - 点击 "New repository secret"
   - 添加以下密钥：
     - `DOCKER_USERNAME` - 你的 Docker Hub 用户名
     - `DOCKER_PASSWORD` - 你的 Docker Hub 访问令牌

### 步骤 2：GitHub Container Registry（自动配置）

GitHub Container Registry 使用 GitHub Token，**无需额外配置**！

- ✅ 自动使用 `GITHUB_TOKEN`（GitHub 自动提供）
- ✅ 镜像会推送到 `ghcr.io/你的用户名/仓库名`

---

## 🚀 工作流程

### 推送代码到主分支

```bash
git push origin main
```

**CI/CD 会：**
1. ✅ 运行代码检查
2. ✅ 运行测试
3. ✅ 检查前端
4. ✅ **构建并推送 Docker 镜像**

**镜像标签：**
- `latest` - 主分支的最新版本
- `main-<commit-sha>` - 基于 commit SHA
- `main` - 分支名

### 创建 Pull Request

**CI/CD 会：**
1. ✅ 运行代码检查
2. ✅ 运行测试
3. ✅ 检查前端
4. ✅ **只构建镜像，不推送**（`push: false`）

**原因：** PR 的代码可能不完整，不推送镜像

---

## 📦 镜像位置

### Docker Hub（如果配置了）

```
docker pull <你的用户名>/neurobreak:latest
```

### GitHub Container Registry

```
docker pull ghcr.io/<你的用户名>/neurobreak:latest
```

---

## 🔍 查看推送的镜像

### Docker Hub

1. 访问 https://hub.docker.com
2. 登录后查看你的仓库
3. 找到 `neurobreak` 仓库

### GitHub Container Registry

1. 打开你的 GitHub 仓库
2. 点击右侧 "Packages"
3. 找到 `neurobreak` 包

---

## ⚙️ 配置说明

### CI/CD 配置详解

```yaml
- name: Log in to Docker Hub
  if: github.event_name != 'pull_request'
  uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKER_USERNAME }}
    password: ${{ secrets.DOCKER_PASSWORD }}
```

**作用：**
- 登录 Docker Hub
- 只在非 PR 时登录（PR 不推送）

```yaml
- name: Log in to GitHub Container Registry
  if: github.event_name != 'pull_request'
  uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}
```

**作用：**
- 登录 GitHub Container Registry
- 使用 GitHub 自动提供的 token

```yaml
- name: Extract metadata
  id: meta
  uses: docker/metadata-action@v5
  with:
    images: |
      ${{ secrets.DOCKER_USERNAME }}/neurobreak
      ghcr.io/${{ github.repository }}
    tags: |
      type=ref,event=branch
      type=ref,event=pr
      type=sha,prefix={{branch}}-
      type=raw,value=latest,enable={{is_default_branch}}
```

**作用：**
- 自动生成镜像标签
- 支持多种标签格式

```yaml
- name: Build and push Docker image
  uses: docker/build-push-action@v5
  with:
    push: ${{ github.event_name != 'pull_request' }}
```

**作用：**
- 构建镜像
- 只在非 PR 时推送（`push: true`）
- PR 时只构建不推送（`push: false`）

---

## 🎯 使用场景

### 场景 1：推送到主分支

```bash
git push origin main
```

**结果：**
- ✅ 构建镜像
- ✅ 推送到 Docker Hub（如果配置了）
- ✅ 推送到 GitHub Container Registry
- ✅ 标签：`latest`, `main-<sha>`, `main`

### 场景 2：创建 Pull Request

```bash
git checkout -b feature/new-feature
git push origin feature/new-feature
# 创建 PR
```

**结果：**
- ✅ 构建镜像（验证能否构建）
- ❌ 不推送镜像（PR 代码可能不完整）

### 场景 3：打标签发布

```bash
git tag v1.0.0
git push origin v1.0.0
```

**结果：**
- ✅ 构建镜像
- ✅ 推送到两个仓库
- ✅ 标签：`v1.0.0`, `1.0.0`, `1.0`, `latest`

---

## 🔒 安全说明

### Docker Hub

- ✅ 使用访问令牌，不使用密码
- ✅ 令牌存储在 GitHub Secrets 中
- ✅ 只有仓库管理员可以访问

### GitHub Container Registry

- ✅ 使用 GitHub Token（自动提供）
- ✅ 权限由 GitHub 管理
- ✅ 默认私有，可以设置为公开

---

## 📝 本地使用推送的镜像

### 从 Docker Hub 拉取

```bash
docker pull <你的用户名>/neurobreak:latest
docker run -it --gpus all \
  -p 8000:8000 \
  -v /path/to/models:/cache \
  -e HF_TOKEN=your_token \
  <你的用户名>/neurobreak:latest
```

### 从 GitHub Container Registry 拉取

```bash
# 先登录（如果需要拉取私有镜像）
echo $GITHUB_TOKEN | docker login ghcr.io -u <你的用户名> --password-stdin

# 拉取镜像
docker pull ghcr.io/<你的用户名>/neurobreak:latest

# 运行容器
docker run -it --gpus all \
  -p 8000:8000 \
  -v /path/to/models:/cache \
  -e HF_TOKEN=your_token \
  ghcr.io/<你的用户名>/neurobreak:latest
```

---

## ❓ 常见问题

### Q1: 如何只推送到 GitHub Container Registry？

**A:** 删除 Docker Hub 登录步骤，只保留 GitHub Container Registry 登录。

### Q2: 如何只推送到 Docker Hub？

**A:** 删除 GitHub Container Registry 登录步骤，只保留 Docker Hub 登录。

### Q3: PR 时为什么不推送镜像？

**A:** 因为 PR 的代码可能不完整，推送不完整的镜像没有意义。只有合并到主分支后才推送。

### Q4: 如何查看推送的镜像？

**A:**
- Docker Hub: https://hub.docker.com → 你的仓库
- GitHub: 仓库页面 → Packages

### Q5: 镜像标签有哪些？

**A:**
- `latest` - 主分支最新版本
- `<branch>-<sha>` - 分支名和 commit SHA
- `<branch>` - 分支名
- `<tag>` - Git 标签（如 v1.0.0）

---

## ✅ 检查清单

配置完成后，确保：

- [ ] Docker Hub 密钥已配置（可选）
- [ ] GitHub Container Registry 自动可用
- [ ] CI/CD 配置已更新
- [ ] 推送代码后镜像自动构建和推送

---

## 🎓 总结

**配置完成后的工作流程：**

1. ✅ 推送代码到主分支
2. ✅ CI/CD 自动运行检查
3. ✅ 自动构建 Docker 镜像
4. ✅ 自动推送到 Docker Hub 和 GitHub Container Registry
5. ✅ 可以在任何地方拉取镜像使用

**现在你的 Docker 镜像会自动构建和推送了！** 🎉

