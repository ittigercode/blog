# 手绘幻灯片 Skill 实战全记录：6 个难点逐个击破

> **摘要：** 记录 handdrawn-slide-skill-pack 从安装到跑通的全过程。Qwen 直连路径因 Pro 模型不兼容而失败，最终用「百炼 CLI 生图 + Skill 脚本收口」的混合路径跑通。含 6 个难点速查表。

---

## 一、Skill 是什么

一个双技能包：

| 技能 | 角色 | 功能 |
|------|------|------|
| `turning-articles-into-handdrawn-decks` | 编排层 | 读文章 → 拆页 → 定义 brief |
| `generating-handdrawn-slide-images` | 原子层 | 根据 brief 生成手绘 PNG |

两条生图路径：
- **Qwen 直连**：脚本直接调 API
- **Host-native 收口**：外部工具画图 → 脚本校验 → 交付

---

## 二、安装

```bash
unzip handdrawn-slide-skill-pack-v1.2.0.zip
cp -r handdrawn-slide-skill-pack/generating-handdrawn-slide-images ~/.hermes/skills/
cp -r handdrawn-slide-skill-pack/turning-articles-into-handdrawn-decks ~/.hermes/skills/
pip install Pillow --break-system-packages
```

> **难点 1：PEP 668 限制。** `--break-system-packages` 解决。

---

## 三、Qwen 路径踩坑

### 需要三个环境变量

```bash
export DASHSCOPE_API_KEY=*** DASHSCOPE_WORKSPACE_ID="***"
export DASHSCOPE_REGION="beijing"
```

> **难点 2：缺一不可。** 其他模型只需一个 Key，千问要三个。

### Workspace ID 获取

> **难点 3：路径变更。** 百炼新平台需在 bailian.console.aliyun.com 创建应用获取。

### Pro 模型不兼容

> **难点 4：核心问题。** 脚本锁定 `qwen-image-2.0-pro`，但 API 调用反复报 exit 8/12。标准版也不行——脚本强校验模型名。**Qwen 直连路径最终失败。**

---

## 四、混合路径：最终可用方案

思路：`bl image generate` 能画 → Skill `--adopt` 收口：

```bash
# Step 1：写页面描述
cat > /tmp/page.json << 'EOF'
{"schema_version":1,"page_id":"page-01",
 "prompt":"技术封面图，标题，白底黑字手绘线条",
 "negative_prompt":"","role":"cover","target_ratio":"16:9"}
EOF

# Step 2：百炼生成图
bl image generate --prompt "技术封面图，标题，手绘线条"

# Step 3：收口
rm -f /tmp/page-01.png /tmp/page-01.manifest.json
python3 scripts/generate_image.py \
  --request /tmp/page.json \
  --adopt /home/yhy/bailian-output/images/图片名.png \
  --output /tmp/page-01.png \
  --accept-ratio-mismatch

# Step 4：验证
python3 scripts/image_delivery.py inspect /tmp/page-01.png --target-ratio 16:9
```

> **难点 5：manifest 冲突。** 重复执行报错，先 `rm -f` 清理。
> **难点 6：比例不匹配。** bl 默认正方形，用 `--accept-ratio-mismatch` 接受。

---

## 五、难点速查表

| # | 问题 | 解决 |
|:--:|------|------|
| 1 | PEP 668 | `--break-system-packages` |
| 2 | 缺环境变量 | export 三个 DASHSCOPE_* |
| 3 | Workspace ID | bailian.console 创建应用 |
| 4 | Pro 模型不兼容 | bl + adopt 混合路径 |
| 5 | manifest 冲突 | rm -f 清理 |
| 6 | 比例不匹配 | --accept-ratio-mismatch |

---

## 六、总结

- Qwen 直连路径在当前环境不可用，混合路径可行
- 三个环境变量每次新终端都要 export，建议写 `~/.bashrc`
- 期待脚本升级支持标准版 `qwen-image-2.0`

> 原创不易，转载请注明出处。
> 作者：Yang Huyue · 2026-07-24
