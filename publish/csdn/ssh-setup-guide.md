# Git SSH 配置终极指南：3 分钟搞定，告别 TLS 报错和 Token 过期

> **摘要：** 本文是一份极简实操指南，涵盖 Ed25519 密钥生成、公钥上传 GitHub、SSH 连接测试、远程地址切换。附带多密钥管理、常见报错解决。读完就能永久告别 HTTPS 的 TLS 报错和 Token 过期问题。

---

## 一、为什么要用 SSH？

HTTPS 推 GitHub 有三大痛点：

- ⚠️ **TLS 握手经常失败**（尤其 WSL 环境，`GnuTLS recv error -110` 反复出现）
- ⚠️ **Token 会过期**，忘了更新就 push 不了
- ⚠️ **每次操作都要输密码**（或者配 credential helper，麻烦）

SSH 的优势：

- ✅ 密钥永不过期
- ✅ 不需要密码
- ✅ TLS 不稳定的环境也能稳定推送
- ✅ 私钥永不离开本地，安全等级最高

---

## 二、第一步：生成 Ed25519 密钥

```bash
ssh-keygen -t ed25519 -C "your@email.com"
```

一路回车即可。生成两个文件：

| 文件 | 说明 |
|------|------|
| `~/.ssh/id_ed25519` | 私钥（保密！不要发给任何人） |
| `~/.ssh/id_ed25519.pub` | 公钥（可以公开，上传到 GitHub） |

> **为什么是 Ed25519？** 比 RSA 更短（256bit vs 4096bit）、更快（毫秒级 vs 秒级）、更安全（抗侧信道攻击）。GitHub、GitLab、Bitbucket 三家现在都推荐 Ed25519。

---

## 三、第二步：公钥上传到 GitHub

```bash
cat ~/.ssh/id_ed25519.pub
```

复制输出内容 → 打开 https://github.com/settings/keys → **New SSH Key** → 粘贴 → 保存。

---

## 四、第三步：测试连接

```bash
ssh -T git@github.com
```

看到这行就成功了：

```
Hi yourname! You've successfully authenticated, but GitHub does not provide shell access.
```

第一次连会提示确认主机指纹，输入 `yes` 回车。

---

## 五、第四步：切换仓库到 SSH

```bash
cd 你的仓库

# HTTPS 改成 SSH
git remote set-url origin git@github.com:用户名/仓库名.git

# 还是原来的 push，但走的是 SSH 了
git push
```

---

## 六、进阶：多密钥管理

如果你有 GitHub、GitLab、Gitee 多个账号：

```bash
# 分别生成密钥
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_github -C "github@email"
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_gitlab -C "gitlab@email"
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_gitee -C "gitee@email"

# 编辑 ~/.ssh/config
Host github.com
  HostName github.com
  IdentityFile ~/.ssh/id_ed25519_github

Host gitlab.com
  HostName gitlab.com
  IdentityFile ~/.ssh/id_ed25519_gitlab

Host gitee.com
  HostName gitee.com
  IdentityFile ~/.ssh/id_ed25519_gitee
```

Git 会自动根据远程地址匹配对应密钥。

---

## 七、常见问题速查

### Q1: Permission denied (publickey)

**原因：** 公钥没上传，或 ssh-agent 没加载私钥。

**解决：**
```bash
ssh-add ~/.ssh/id_ed25519
```

### Q2: 端口 22 被防火墙封了

**解决：** 用 HTTPS 端口 443 走 SSH：
```bash
ssh -T -p 443 git@ssh.github.com
```

永久配置 `~/.ssh/config`：
```
Host github.com
  HostName ssh.github.com
  Port 443
```

### Q3: 换了电脑怎么办

**正确做法：** 新电脑重新生成密钥上传。**不要复制私钥**，每台机器独立密钥更安全。

### Q4: 怎么撤销旧密钥

去 https://github.com/settings/keys → 找到旧的 → Delete。万一私钥泄露了第一时间删。

---

## 八、总结

```bash
# 四行命令，永久生效
ssh-keygen -t ed25519 -C "your@email.com"    # 1. 生成密钥
cat ~/.ssh/id_ed25519.pub                     # 2. 复制公钥（贴到 GitHub）
ssh -T git@github.com                         # 3. 测试连接
git remote set-url origin git@github.com:用户/仓库.git  # 4. 切 SSH
```

从此 `git push` 再也不会报 TLS 错误。一次配置，终身受益。

> 原创不易，转载请注明出处。
> 作者：Yang Huyue · 2026-07-16
