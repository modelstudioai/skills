# 接入多模态生成模型

图像生成模型需通过工具的扩展机制（Skill、Slash Command 或 Agent）接入。

## **示例：在 Claude Code 中接入图像生成模型**

以 Claude Code 为例，通过 Slash Command 接入图像生成模型。其他工具的接入方式类似，区别在于扩展机制和配置文件路径不同。

### **步骤一：创建 Slash Command**

在项目根目录创建 `.claude/commands/text-to-image.md`，写入以下内容：

```
调用 Token Plan 文生图 API，根据描述生成图片。

用户需求：$ARGUMENTS

## 步骤

1. 从用户需求中提取 prompt（图片描述）、model（默认 qwen-image-2.0）、size（默认 1024*1024）。

2. 调用 API 生成图片（使用 Bash 工具执行 curl）：

```
curl -s -X POST "https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
  -H "Authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "<model>",
    "input": {
      "messages": [{"role":"user","content":[{"text":"<prompt>"}]}]
    },
    "parameters": {"size":"<size>"}
  }'
```

3. 从返回 JSON 的 output.choices[*].message.content[*].image 中提取图片 URL。

4. 用 curl -s -o "generated_$(date +%Y%m%d_%H%M%S).png" "<URL>" 下载到当前目录。

5. 向用户展示生成的图片文件路径。
```

### **步骤二：生成图片**

在 Claude Code 中输入 `/text-to-image 画一只猫`。

## **其他工具**

不同工具的扩展机制和配置文件路径如下表所示。将上述 Claude Code 示例中的配置内容保存到对应路径即可。

工具

扩展机制

配置文件路径

Claude Code

Slash Command

`.claude/commands/text-to-image.md`

Codex

Skill

`~/.codex/skills/token-plan-image/SKILL.md`

Qwen Code

Skill

`~/.qwen/skills/text-to-image/SKILL.md`

OpenCode

Agent

`.opencode/agents/text-to-image.md`

OpenClaw

Skill

`~/.openclaw/workspace/skills/token-plan-image/SKILL.md`

Hermes Agent

Skill

`~/.hermes/skills/media/text-to-image/SKILL.md`

**说明**

Skill 类工具（Codex、Qwen Code、OpenClaw、Hermes Agent）需要在配置文件开头添加 YAML front matter：

```
---
name: "token-plan-image"
description: "调用 Token Plan 文生图模型，根据文字描述生成图片。当用户要求画图、生成图片时激活。"
---

（... 与上述 Claude Code 示例相同的内容 ...）
```

OpenCode Agent 需要不同的 front matter 格式：

```
---
description: "调用 Token Plan 文生图模型，根据文字描述生成图片。"
mode: subagent
tools:
  bash: true
  write: false
  edit: false
---

（... 与上述 Claude Code 示例相同的内容 ...）
```
