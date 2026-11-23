# Token Plan 概览

Token Plan 是阿里云百炼的 AI 模型订阅服务，以 Credits 统一计量，支持在兼容的 AI 工具中交互式使用。

## 快速开始

选择套餐并获取 API Key，按使用的工具复制命令完成接入。

[购买套餐](https://bailian.console.aliyun.com/cn-beijing/subscription/overview)[获取 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)

#### Claude Code

```
# 自动安装阿里云百炼 CLI 并为所选 Agent 完成接入；将 sk-sp-xxxx 替换为你的 Token Plan API Key
curl -fsSL https://bailian.aliyun.com/cli/install.sh | bash
export TOKEN_PLAN_API_KEY="sk-sp-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
bl config agent --agent claude-code --region cn-beijing --api-key $TOKEN_PLAN_API_KEY --model auto
```

#### Codex

```
# 自动安装阿里云百炼 CLI 并为所选 Agent 完成接入；将 sk-sp-xxxx 替换为你的 Token Plan API Key
curl -fsSL https://bailian.aliyun.com/cli/install.sh | bash
export TOKEN_PLAN_API_KEY="sk-sp-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
bl config agent --agent codex --region cn-beijing --api-key $TOKEN_PLAN_API_KEY --model auto
```

#### Qwen Code

```
# 自动安装阿里云百炼 CLI 并为所选 Agent 完成接入；将 sk-sp-xxxx 替换为你的 Token Plan API Key
curl -fsSL https://bailian.aliyun.com/cli/install.sh | bash
export TOKEN_PLAN_API_KEY="sk-sp-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
bl config agent --agent qwen-code --region cn-beijing --api-key $TOKEN_PLAN_API_KEY --model auto
```

#### OpenClaw

```
# 自动安装阿里云百炼 CLI 并为所选 Agent 完成接入；将 sk-sp-xxxx 替换为你的 Token Plan API Key
curl -fsSL https://bailian.aliyun.com/cli/install.sh | bash
export TOKEN_PLAN_API_KEY="sk-sp-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
bl config agent --agent openclaw --region cn-beijing --api-key $TOKEN_PLAN_API_KEY --model auto
```

#### Hermes Agent

```
# 自动安装阿里云百炼 CLI 并为所选 Agent 完成接入；将 sk-sp-xxxx 替换为你的 Token Plan API Key
curl -fsSL https://bailian.aliyun.com/cli/install.sh | bash
export TOKEN_PLAN_API_KEY="sk-sp-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
bl config agent --agent hermes --region cn-beijing --api-key $TOKEN_PLAN_API_KEY --model auto
```

## 接入 AI 工具

选择你使用的工具，按对应指南配置 Token Plan 个人版或团队版。

[

**Qoder**

面向真实软件开发的 Agentic 编码平台

](raw/token-plan-user-guide/use-chat-client-or-development-tool/qoder-agent.md)[

**Claude Code**

AI 终端编码助手，支持自然语言编程

](raw/token-plan-user-guide/use-chat-client-or-development-tool/claude-code.md)[

**Codex**

OpenAI 推出的命令行编程工具

](raw/token-plan-user-guide/use-chat-client-or-development-tool/codex.md)[

**Qwen Code**

开源命令行 AI 编码工具

](raw/token-plan-user-guide/use-chat-client-or-development-tool/qwen-code.md)[

**OpenClaw**

开源、自托管个人 AI 助手

](raw/token-plan-user-guide/use-chat-client-or-development-tool/openclaw.md)[

**Hermes Agent**

开源 AI 代理框架，内置自学习循环

](raw/token-plan-user-guide/use-chat-client-or-development-tool/hermes-agent.md)[

**Trae**

自定义模型接入，无需安装插件

](raw/token-plan-user-guide/use-chat-client-or-development-tool/trae-tool-guide.md)[

**DeepSeek Harness**

开源插件化 Agent 框架，Web UI 与命令行双模式

](raw/token-plan-user-guide/use-chat-client-or-development-tool/deepseek-harness.md)[

**WorkBuddy**

桌面 AI Agent 工作台

](raw/token-plan-user-guide/use-chat-client-or-development-tool/workbuddy.md)[

**通用接入指南**

其他编程工具

](raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/more-tools.md)

## 接入其他模型

AI 工具原生只处理文本协议，图像、视频、语音等能力需要通过扩展机制接入，详见[接入概览](raw/token-plan-user-guide/token-plan-best-practice/token-plan-integration-overview.md)。

[

**接入决策模型**

按置信度自动放行、隐藏或转人工。

](raw/token-plan-user-guide/token-plan-best-practice/token-plan-decision-model.md)[

**接入图像生成模型**

根据文字描述生成图片。

](raw/token-plan-user-guide/token-plan-best-practice/token-plan-image-generation.md)[

**接入视频生成模型**

提交异步任务并下载视频。

](raw/token-plan-user-guide/token-plan-best-practice/token-plan-video-generation.md)[

**接入语音合成模型**

将文本转为音频。

](raw/token-plan-user-guide/token-plan-best-practice/token-plan-speech-synthesis.md)[

**接入语音识别模型**

将音频转为转写文本。

](raw/token-plan-user-guide/token-plan-best-practice/token-plan-speech-recognition.md)[

**接入实时语音对话模型**

创建并运行实时语音客户端。

](raw/token-plan-user-guide/token-plan-best-practice/token-plan-realtime-voice.md)

## 用量与问题

[

**用量与额度**

Credits 怎么计算、额度何时重置、用完了怎么办。

](raw/token-plan-user-guide/token-plan-guide/token-plan-usage-quota.md)[

**个人版订阅与权益**

升级、续费、退订，以及 Harness 权益。

](raw/token-plan-user-guide/token-plan-personal/token-plan-personal-overview.md)[

**团队版订阅与权益**

坐席、成员、共享用量包和团队管理。

](raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-overview.md)[

**常见问题**

购买、退订、使用限制和接入报错。

](raw/token-plan-user-guide/token-plan-guide/token-plan-faq.md)

## 接入 Harness

个人版 Standard 与 Pro 套餐附赠 Harness 权益，可调用 AgentStudio 工具，不占用 Credits。复制下方提示词并发送给本地 AI 工具，即可让它完成配置。

Harness 服务本地配置指南

```
## Harness 服务本地配置指南

请按照以下步骤配置 Harness 服务给本地 AI 工具使用。

### 前置依赖安装与检查
1. 检查是否安装百炼 CLI，如没有安装请参照如下文档进行安装：https://bailian.aliyun.com/cli/install.md
2. 使用百炼 CLI 完成登录：bl auth login --console
3. 执行如下命令：bl config show，拿到 config_file 文件路径，并读取文件内部api_key。

### 需要配置的服务 — 自研工具
将以下 MCP 服务器配置写入本地全局配置（请识别准确目录），直接通过 MCP 协议调用，不经 bailian-cli 中转。所有服务的公共信息：
- 类型：HTTP Streamable
- 请求头：Authorization: Bearer ${DASHSCOPE_API_KEY}

需要配置的服务清单：

| 服务名 | URL |
|---|---|
| 图像生成 MCP | `https://dashscope.aliyuncs.com/api/v1/mcps/TextGenerateImage/mcp` |
| 视频生成 MCP | `https://dashscope.aliyuncs.com/api/v1/mcps/VideoGenerate/mcp` |
| 代码解释器 MCP | `https://dashscope.aliyuncs.com/api/v1/mcps/CodeInterpreter/mcp` |
| 联网搜索增强版 MCP | `https://dashscope.aliyuncs.com/api/v1/mcps/EnhancedSearch/mcp` |
| 网页解析 MCP | `https://dashscope.aliyuncs.com/api/v1/mcps/WebFetch/mcp` |
| 垂类搜索 MCP | `https://dashscope.aliyuncs.com/api/v1/mcps/VerticalSearch/mcp` |
| 语音合成 MCP | `https://dashscope.aliyuncs.com/api/v1/mcps/TextGenerateSpeech/mcp` |
| 语音识别 MCP | `https://dashscope.aliyuncs.com/api/v1/mcps/SpeechGenerateText/mcp` |

### 需要配置的服务 — 基础设施
以下服务登录后先询问用户需求，根据需求走不同路径：

- **体验**：通过 bailian-cli 对应命令直接调用，针对不同场景操作。
- **写代码接入**：使用前置步骤中获取的 `api_key`，帮助用户书写代码调用相关 API。

具体服务：

| 服务名 | CLI 命令 | API 文档 |
|---|---|---|
| RAG-知识库服务 | bl knowledge 系列 | https://docs.agent.bailian.aliyun.com/zh/api/rag/overview |
| Memory-记忆库服务 | bl memory 系列 | https://docs.agent.bailian.aliyun.com/zh/api/memory/overview |
| Managed Agent-托管智能体 | bl managed-agent 系列 | https://docs.agent.bailian.aliyun.com/zh/api/managed-agents/introduction |
```

查看配置指南

\## Harness 服务本地配置指南 请按照以下步骤配置 Harness 服务给本地 AI 工具使用。 ### 前置依赖安装与检查 1. 检查是否安装百炼 CLI，如没有安装请参照如下文档进行安装：[https://bailian.aliyun.com/cli/install.md](https://bailian.aliyun.com/cli/install.md) 2. 使用百炼 CLI 完成登录：bl auth login --console 3. 执行如下命令：bl config show，拿到 config\_file 文件路径，并读取文件内部api\_key。 ### 需要配置的服务 — 自研工具 将以下 MCP 服务器配置写入本地全局配置（请识别准确目录），直接通过 MCP 协议调用，不经 bailian-cli 中转。所有服务的公共信息： - 类型：HTTP Streamable - 请求头：Authorization: Bearer ${DASHSCOPE\_API\_KEY} 需要配置的服务清单： | 服务名 | URL | |---|---| | 图像生成 MCP | \`[https://dashscope.aliyuncs.com/api/v1/mcps/TextGenerateImage/mcp\`](https://dashscope.aliyuncs.com/api/v1/mcps/TextGenerateImage/mcp%60) | | 视频生成 MCP | \`[https://dashscope.aliyuncs.com/api/v1/mcps/VideoGenerate/mcp\`](https://dashscope.aliyuncs.com/api/v1/mcps/VideoGenerate/mcp%60) | | 代码解释器 MCP | \`[https://dashscope.aliyuncs.com/api/v1/mcps/CodeInterpreter/mcp\`](https://dashscope.aliyuncs.com/api/v1/mcps/CodeInterpreter/mcp%60) | | 联网搜索增强版 MCP | \`[https://dashscope.aliyuncs.com/api/v1/mcps/EnhancedSearch/mcp\`](https://dashscope.aliyuncs.com/api/v1/mcps/EnhancedSearch/mcp%60) | | 网页解析 MCP | \`[https://dashscope.aliyuncs.com/api/v1/mcps/WebFetch/mcp\`](https://dashscope.aliyuncs.com/api/v1/mcps/WebFetch/mcp%60) | | 垂类搜索 MCP | \`[https://dashscope.aliyuncs.com/api/v1/mcps/VerticalSearch/mcp\`](https://dashscope.aliyuncs.com/api/v1/mcps/VerticalSearch/mcp%60) | | 语音合成 MCP | \`[https://dashscope.aliyuncs.com/api/v1/mcps/TextGenerateSpeech/mcp\`](https://dashscope.aliyuncs.com/api/v1/mcps/TextGenerateSpeech/mcp%60) | | 语音识别 MCP | \`[https://dashscope.aliyuncs.com/api/v1/mcps/SpeechGenerateText/mcp\`](https://dashscope.aliyuncs.com/api/v1/mcps/SpeechGenerateText/mcp%60) | ### 需要配置的服务 — 基础设施 以下服务登录后先询问用户需求，根据需求走不同路径： - \*\*体验\*\*：通过 bailian-cli 对应命令直接调用，针对不同场景操作。 - \*\*写代码接入\*\*：使用前置步骤中获取的 \`api\_key\`，帮助用户书写代码调用相关 API。 具体服务： | 服务名 | CLI 命令 | API 文档 | |---|---|---| | RAG-知识库服务 | bl knowledge 系列 | [https://docs.agent.bailian.aliyun.com/zh/api/rag/overview](https://docs.agent.bailian.aliyun.com/zh/api/rag/overview) | | Memory-记忆库服务 | bl memory 系列 | [https://docs.agent.bailian.aliyun.com/zh/api/memory/overview](https://docs.agent.bailian.aliyun.com/zh/api/memory/overview) | | Managed Agent-托管智能体 | bl managed-agent 系列 | [https://docs.agent.bailian.aliyun.com/zh/api/managed-agents/introduction](https://docs.agent.bailian.aliyun.com/zh/api/managed-agents/introduction) |

## 场景 Playbook

接入完成后，可以按场景开始使用。

[

**AI Coding / 开发**

给现有系统加功能、搭建个人小工具或评审代码。

](raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-coding/token-plan-playbook-ai-coding-feature.md)[

**自媒体 / 内容创作**

制作封面与文案、故事配音或商品展示视频。

](raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-content/token-plan-playbook-cinematic-broll.md)[

**资料与数据处理**

分析表格、提取网页字段或阅读长文并问答。

](raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-data/token-plan-playbook-sheet-analysis.md)[

**生活娱乐**

修复老照片、规划周末出游或排查居家隐患。

](raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-life/token-plan-playbook-brand-spokesperson.md)[

**求职职场**

按岗位要求改写简历、练习面试或制作解题讲解网页。

](raw/token-plan-user-guide/token-plan-playbooks/token-plan-playbook-career/token-plan-playbook-resume-doctor.md)
