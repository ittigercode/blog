# Windows 安装 GitHub CLI 完全指南：四种方式横评 + gh 到底有什么用？

> **摘要：** 本文横向对比 Windows 安装 GitHub CLI 的四种方式（winget/Scoop/Chocolatey/手动），分析 winget 管理员与普通用户的区别，并回答一个根本问题：gh CLI 到底能做什么？附带 SSH vs HTTPS+PAT vs gh CLI 三方认证对比。

---

## 一、横向对比：四种安装方式

| 方式 | 命令 | 难度 | 推荐 |
|------|------|:--:|:--:|
| 🟢 winget | `winget install --id GitHub.cli` | ⭐ | ★★★★★ |
| 🔵 Scoop | `scoop install gh` | ⭐⭐ | ★★★★ |
| 🟡 Chocolatey | `choco install gh` | ⭐⭐ | ★★★ |
| 🔴 手动解压 | 下载 zip → 解压 → 加 PATH | ⭐⭐⭐ | ★★ |

### 方式一：winget（最推荐）

Windows 10/11 自带，不需要装任何东西：

```powershell
winget install --id GitHub.cli
```

装完关掉重开 PowerShell，`gh --version` 验证。

### 方式二：Scoop

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex
scoop install gh
```

Scoop 的好处是装到用户目录，不需要管理员权限，更新方便。

### 方式三：Chocolatey

```powershell
choco install gh
```

### 方式四：手动解压

有些人的 Windows 打不开 .msi 文件（权限问题），那就用 zip 版：

1. 打开 https://github.com/cli/cli/releases/latest
2. 下载 `gh_X.X.X_windows_amd64.zip`
3. 解压到 `C:\gh\`
4. 把 `C:\gh\bin` 加到系统 PATH

---

## 二、winget 管理员 vs 普通用户，有什么区别？

| 维度 | 普通用户 | 管理员 |
|------|----------|--------|
| 安装位置 | `%LOCALAPPDATA%` | `C:\Program Files\` |
| 影响范围 | 只装给自己 | 这台电脑所有人 |
| UAC 弹窗 | 不需要 | 需要点「是」 |
| PATH | 自动加 | 自动加，全局生效 |

> **建议普通用户跑就行。** 省事，不弹窗，效果完全一样。只有公司需要给多人装同一个工具时才用管理员。

---

## 三、gh CLI 到底有什么用？

很多人以为 gh 只是「另一个 Git 工具」。完全不是——它把你平时在 GitHub 网页上点的所有操作，搬到了终端：

### 3.1 认证管理

```bash
gh auth login          # 浏览器授权，比 SSH 和 Token 都简单
gh auth status         # 查看登录状态
```

### 3.2 仓库操作

```bash
gh repo create my-project --public   # 创建仓库
gh repo clone owner/repo             # 克隆
gh repo view owner/repo --web        # 浏览器打开
```

### 3.3 Issue 和 PR

```bash
gh issue create --title "Bug: xxx" --body "..."
gh issue list
gh pr create --title "Feature" --body "..."
gh pr review --approve
gh pr merge
```

### 3.4 CI/CD 监控

```bash
gh run watch           # 实时看 Actions 日志
gh run list            # 查看工作流历史
```

### 3.5 Release 发布

```bash
gh release create v1.0 --title "正式版" --notes "更新内容"
```

---

## 四、gh 和 git 的关系

| | git | gh |
|------|-----|----|
| 定位 | 分布式版本控制 | GitHub 平台操作 |
| 范围 | 任何 Git 仓库 | 仅 GitHub |
| 典型命令 | `commit, push, merge` | `issue, pr, release` |
| 互替？ | 不替代，是互补 |

> git 管代码版本，gh 管 GitHub 平台。各司其职，配合使用。

---

## 五、三种认证方式终极对比

| | SSH | HTTPS + PAT | gh CLI |
|------|:--:|:--:|:--:|
| 设置难度 | ⭐⭐⭐ | ⭐⭐ | ⭐ |
| 安全性 | ★★★★★ | ★★★ | ★★★★ |
| WSL 稳定性 | ★★★★★ | ★★ | ★★★★ |
| Issue/PR | ❌ | ❌ | ✅ |

### 最佳实践

- **日常 push/pull** → SSH（最稳定，尤其 WSL 环境）
- **Issue/PR/Release** → gh CLI（最方便）
- **临时操作** → HTTPS + PAT（最快上手）

三者不是竞争关系，是互补关系。

---

## 六、总结

gh CLI 的价值不在于「替代 SSH 或 HTTPS」，而在于把你从浏览器中解放出来。当你可以在终端里完成 Issue 管理、PR Review、Release 发布、CI 监控，你就再也不需要在 IDE 和浏览器之间来回切换了。

> 原创不易，转载请注明出处。
> 作者：Yang Huyue · 2026-07-17
