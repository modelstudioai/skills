# 接入多模态生成模型

图像生成模型需通过工具的扩展机制（Skill、Slash Command 或 Agent）接入。

## **前提：获取套餐专属凭证**

在控制台「我的订阅」打开 Token Plan 套餐详情页，接入信息卡片展示套餐专属 API Key（以 `sk-sp-` 为前缀，掩码显示），支持生成、重置与复制 API Key。

**说明**

套餐详情页「可使用模型」以文本、编程模型为主；图像生成模型不在该列表展示，需通过 `multimodal-generation` API 调用。

## **示例：在 Claude Code 中接入图像生成模型**

以 Claude Code 为例，通过 Slash Command 接入图像生成模型。其他工具的接入方式类似，区别在于扩展机制和配置文件路径不同。

### **步骤一：创建 Slash Command**

将套餐专属 API Key（以 `sk-sp-` 为前缀）配置为环境变量 `$ANTHROPIC_AUTH_TOKEN`，供后续 curl 鉴权使用。

在项目根目录创建 `.claude/commands/text-to-image.md`，写入以下内容：

```
调用 Token Plan 文生图 API，根据描述生成图片。

用户需求：$ARGUMENTS

## 步骤

1. 从用户需求中提取 prompt（图片描述）、model、size（默认 1024*1024）。若用户明确指定了模型（如“模型=wan2.7-image”或“用 wan2.7-image 画”），必须严格使用用户指定的模型名，不要回退到默认模型；仅当用户未指定模型时才使用默认 qwen-image-2.0。常用图像生成模型有 qwen-image-2.0、qwen-image-2.0-pro、wan2.7-image、wan2.7-image-pro、z-image-turbo 等，完整列表以百炼模型列表为准。

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

在 Claude Code 中输入 `/text-to-image 画一只猫`。如需使用默认模型以外的图像生成模型，在指令中写明模型名即可，例如 `/text-to-image 用 wan2.7-image 画一只猫`。

## **其他工具**

控制台套餐详情页「快速接入 AI 编程工具」入口提供 Qwen Code、Qoder、OpenClaw、Claude Code、OpenCode 等工具的接入文档。不同工具的扩展机制和配置文件路径如下表所示，该表为支持扩展机制的主流 AI 编程工具示例。将上述 Claude Code 示例中的配置内容保存到对应路径即可。

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

Qoder

Skill

`~/.qoder/skills/text-to-image/SKILL.md`

**说明**

Skill 类工具（Codex、Qwen Code、OpenClaw、Hermes Agent、Qoder）需要在配置文件开头添加 YAML front matter：

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
