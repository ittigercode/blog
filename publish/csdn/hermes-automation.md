# Hermes Agent 自动化原理揭秘：四层架构实现全自动博客发布

> **摘要：** 本文深入解析 Hermes Agent 如何通过四层架构实现从 AI 创作到 GitHub 推送的完全自动化。重点解答一个看似矛盾的问题：为什么 AI 不能直接 git push，却最终能自动推送？

---

## 一、问题的起点

用 Hermes 搭博客时出现了一个矛盾场景：

- ✅ AI 能写文章（write_file 工具）
- ✅ AI 能改首页（patch 工具）
- ❌ AI 不能 git push（网络请求被安全策略拦截）
- ✅ 但最终自动推送了

答案藏在 Hermes 的四层自动化架构中。

---

## 二、四层架构全景

```
你说「发布博客」
       ↓
① 工具层 — AI 直接操控
   write_file() 写文章，patch() 改首页
   ❌ 网络受限，不能 git push
       ↓
② Cron 调度层 — 独立进程执行  
   cronjob(no_agent=true)
   创建一次性定时任务
       ↓
③ 脚本层 — Python 纯脚本
   blog_auto_push.py
   git add → commit → SSH push
   不需要 LLM，不经过安全策略
       ↓
④ 记忆层 — 跨会话持久化
   memory → 博客路径/配置
   skill  → 发布流程 SOP
```

---

## 三、逐层解析

### 3.1 工具层：AI 的手和眼

AI 使用 write_file、patch、read_file 等工具完成本地文件操作。这些只涉及本地磁盘，不触发网络安全策略。

但当尝试 git push 时，Hermes 的安全子系统（Tirith）会扫描所有终端命令——凡是包含 Token 或外部网络请求的都会被拦截，要求用户手动审批。在网络不稳定的 WSL 环境里，审批经常超时，命令被阻止。

### 3.2 Cron 调度层：绕过的关键

这是整个架构最巧妙的一环。Hermes 的 cronjob 支持 **no_agent=True** 模式：

- **no_agent=False**：Cron 启动完整 AI Agent，再次触发安全策略
- **no_agent=True**：Cron 直接执行脚本，零 AI 参与，零安全扫描

Cron 进程是**完全独立的 Python 进程**，不受主会话安全策略约束。这就是「绕过」的秘诀。

### 3.3 脚本层：真正的执行者

```python
import subprocess, os, glob

os.chdir(os.path.expanduser("~/blog"))

# 清理旧文件
for f in glob.glob("posts/old-*.html"):
    os.remove(f)

# Git 操作
subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "自动更新"])
subprocess.run(["git", "push"])  # SSH 不需要 Token
```

脚本做三件事：文件清理、Git 提交、SSH 推送。

**为什么是 SSH 而不是 HTTPS？**

之前用 HTTPS + Personal Access Token 频繁失败：
- Token 会被安全策略自动替换为 `***`
- WSL 的 HTTPS/TLS 连接不稳定（GnuTLS recv error -110）

SSH 的优势：密钥放在 `~/.ssh/id_ed25519`，Git 自动读取，不需要命令行传 Token。而且 TCP 连接比 TLS 握手更稳定。

### 3.4 记忆层：让 AI 不「失忆」

通过 memory 系统和 skill_manage 创建可复用文档，记录完整发布流程。下次新会话自动注入到系统提示词，不需要重新问「博客在哪」。

---

## 四、完整流程复盘

| 步骤 | 操作 | 层级 |
|:--:|------|:--:|
| 1 | 你说「发布博客」 | → |
| 2 | write_file 创建 HTML | 工具层 |
| 3 | patch 更新首页 | 工具层 |
| 4 | cronjob(schedule="1m") | 调度层 |
| 5 | 60秒后 Cron 独立启动 | 调度层 |
| 6 | blog_auto_push.py 执行 | 脚本层 |
| 7 | git add → commit → push | 脚本层 |
| 8 | GitHub 远程同步 🎉 | 完成 |

**全程用户不需要碰任何 Git 命令。**

---

## 五、架构优势与局限

**优势：**
- 职责分离：AI 创作，Cron 执行
- 安全边界清晰：敏感操作在独立脚本中运行
- 失败隔离：推送失败不影响创作

**局限：**
- 60秒最小延迟（Cron 粒度限制）
- 脚本错误不会反馈到 AI 对话
- 依赖 SSH 密钥正确配置

---

## 六、总结

这套架构的本质是 Unix 哲学「小工具组合」思想：每个工具只做一件事并做好，通过简单的接口串联成强大流水线。AI 负责「想」，Cron 负责「跑」——各司其职，简洁高效。

> 原创不易，转载请注明出处。
> 作者：Yang Huyue · 2026-07-17
