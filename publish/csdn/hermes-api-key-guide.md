# Hermes 模型 API Key 配置完全指南：从千问到全模型

> **摘要：** 以千问 API Key 为切入点，手把手教你申请、配置到 Hermes、让 Skill 调用。横向扩展到 OpenAI、DeepSeek、Anthropic 等 7 个主流模型，对比配置的相同与不同之处。附带 OpenRouter 一 Key 通吃方案。

---

## 一、申请千问（DashScope）API Key

### 三步拿到 Key

1. 打开 **dashscope.aliyun.com**，阿里云账号登录
2. 右上角 → **API-KEY 管理**
3. **创建 API-KEY** → 立即复制（只显示一次）

> 千问文本模型（qwen-turbo/plus/max）很便宜，画图稍贵，新用户有免费额度。

### 千问特殊：还需要工作空间

1. 打开 **dashscope.console.aliyun.com**
2. 创建/选择**工作空间**
3. 记下 **Workspace ID**（页面左上角）

千问是少数需要三个环境变量的模型（详见下文对比）。

---

## 二、Hermes 配置千问 API Key

### 所有 Key 统一放一个地方

```bash
# 编辑 ~/.hermes/.env
```

添加：

```bash
DASHSCOPE_API_KEY=***           # 你的 API Key
DASHSCOPE_WORKSPACE_ID=你的ID    # Workspace ID
DASHSCOPE_REGION=cn-beijing      # 或 singapore
```

### 为什么放 .env 而不是 config.yaml？

| 文件 | 用途 | 安全 |
|------|------|------|
| `config.yaml` | 设置项（模型名、工具等） | 可提交 Git |
| **`.env`** | 秘钥 | 绝不能提交 Git，Hermes 防 AI 读取 |

> Hermes 启动时自动读取 .env，运行时可用 `/reload` 热更新。

---

## 三、Skill 如何使用 API Key

### Skill 不直接读 .env

Skill 本身只是 Markdown 文档。真正调用 API 的是 Skill 里的 **Python 脚本**：

```bash
python3 scripts/generate_image.py --preflight
# 脚本内部: os.environ.get("DASHSCOPE_API_KEY")
# 退出码 0 = 已配置
# 退出码 5 = 缺少 Key
```

### 以手绘幻灯片 Skill 为例

三步安全流程：

```bash
# 1. 预检（只检查依赖和Key，不联网不收费）
python3 scripts/generate_image.py --preflight

# 2. 试跑（验证请求格式，不联网）
python3 scripts/generate_image.py --request page.json --dry-run

# 3. 正式生成（计费API调用）
python3 scripts/generate_image.py --request page.json --output page.png
```

**关键设计：** Skill 脚本从环境变量读 Key，不写死在 Skill 目录里。这样 Skill 可以公开分享，绝不泄露秘钥。

---

## 四、横向对比：7 个主流模型配置

### 共同点

| 规则 | 说明 |
|------|------|
| 统一 `.env` | 所有 Key 都在 `~/.hermes/.env` |
| 大写变量名 | 全大写，下划线分隔 |
| 启动加载 | 启动时读取，/reload 热更新 |
| Skill 不存 Key | os.environ 读取，不硬编码 |
| 自动打码 | 终端输出自动 `***` 隐藏 |

### 差异对比

| 模型 | 环境变量 | 需要几个？ | 申请地址 |
|------|------|:--:|------|
| OpenAI | `OPENAI_API_KEY` | 1 | platform.openai.com |
| Anthropic | `ANTHROPIC_API_KEY` | 1 | console.anthropic.com |
| DeepSeek | `DEEPSEEK_API_KEY` | 1 | platform.deepseek.com |
| Google | `GOOGLE_API_KEY` | 1 | aistudio.google.com |
| xAI | `XAI_API_KEY` | 1 | console.x.ai |
| 月之暗面 | `MOONSHOT_API_KEY` | 1 | platform.moonshot.cn |
| **千问** | `DASHSCOPE_API_KEY` + `WORKSPACE_ID` + `REGION` | **3** 🔴 | dashscope.aliyun.com |

### 千问为什么需要 3 个？

- `DASHSCOPE_API_KEY` — 认证（所有模型都需要）
- `DASHSCOPE_WORKSPACE_ID` — 阿里云的工作空间架构，类似 OpenAI 的 Organization ID
- `DASHSCOPE_REGION` — 数据节点选择（beijing / singapore）

大部分模型只需要一个 Key。千问多两个是因为阿里云的企业架构设计。

---

## 五、进阶：OpenRouter 一 Key 通吃

不想每个模型都申请 Key？用 [OpenRouter](https://openrouter.ai)：

```bash
# .env 一行搞定
OPENROUTER_API_KEY=***   # 一个 Key

# 调用 200+ 模型
hermes chat -m anthropic/claude-sonnet-4
hermes chat -m google/gemini-2.5-pro
hermes chat -m qwen/qwen-max
```

---

## 六、总结

| 问题 | 答案 |
|------|------|
| Key 放哪？ | `~/.hermes/.env` |
| 为什么不是 config.yaml？ | config 可提交 Git，.env 不能 |
| Skill 怎么读 Key？ | Python 脚本用 `os.environ` |
| 不同模型配置差异大吗？ | 不大，核心都是填 .env，只是变量名和数量不同 |
| 最省事方案？ | OpenRouter 一个 Key 通吃 |

> **核心原则：** Key 绝不写死在代码或 Skill 目录里。统一 .env 管理，Hermes 自动加载、自动防泄漏。换模型只需改一行环境变量。

---

> 原创不易，转载请注明出处。
> 作者：Yang Huyue · 2026-07-23
