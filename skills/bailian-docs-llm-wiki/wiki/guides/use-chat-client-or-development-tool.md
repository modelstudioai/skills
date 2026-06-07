# use chat client or development tool

百炼平台兼容主流的对话客户端、AI 编码 Agent、IDE 插件和通用调试工具，开发者可以通过这些工具直接接入百炼托管的 Qwen、DeepSeek、Kimi、GLM、MiniMax 等模型，无需自己编写 SDK 调用代码。本主题汇总了 16 个常见客户端的接入方式、所需配置项以及它们与百炼三种计费方式（按量付费、Coding Plan、Token Plan 团队版）的适配关系。

## 工具分类与适用场景

按使用场景，常见接入工具大致分为四类：

| 类别 | 典型工具 | 适用场景 |
| --- | --- | --- |
| 通用对话客户端 | [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)、[Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md) | 桌面端对话、知识库问答、文件分析 |
| AI 编码 Agent（CLI / 桌面） | [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)、[Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)、[Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)、[OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)、[Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)、[Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md) | 在终端中完成代码生成、重构、调试，多步任务自动化 |
| IDE / 编辑器集成 | [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)、[Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)、[Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)、[Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md) | 在 IDE/编辑器内联完成补全、对话、Agent 模式编程 |
| 多渠道平台 / 调试 | [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)、[Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)、[使用 Postman 或 cURL 调用图像/视频生成 API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)、[更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) | 接入钉钉/飞书/微信/QQ 消息渠道、低代码工作流、HTTP 调试 |

## 通用接入要素

无论使用哪个客户端，接入百炼模型本质上只需要配置三个要素：

1. **API Key**：决定计费方式与可用模型集
   - 按量付费：`sk-xxxxx`，在[百炼控制台 API Key 管理](https://help.aliyun.com/zh/model-studio/get-api-key)创建
   - Coding Plan：`sk-sp-xxxxx`，专属编码计划 Key
   - Token Plan 团队版：在团队订阅页面获取，仅限团队成员使用
2. **Base URL**：根据 API 协议和接入计划选择
3. **模型 ID**：填写客户端可见的模型列表，必须是该计费方式下支持的模型

### Base URL 速查

| 计费方式 | OpenAI 兼容协议 | Anthropic 协议 |
| --- | --- | --- |
| 按量付费（华北2 北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `https://dashscope.aliyuncs.com/apps/anthropic` |
| 按量付费（新加坡） | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/apps/anthropic` |
| Coding Plan | `https://coding.dashscope.aliyuncs.com/compatible-mode/v1` | `https://coding.dashscope.aliyuncs.com/apps/anthropic` |
| Token Plan 团队版 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |

> **注意**：Base URL、API Key 和模型必须归属同一地域、同一计费方式。跨地域或跨计费方式混搭会返回 `401 Incorrect API key` 或 `model not found`。新加坡等海外地域的 `{WorkspaceId}` 需在控制台「Workspace 管理」页面获取。

### 协议选择

- **OpenAI 兼容模式**（`/compatible-mode/v1`）：覆盖最广，几乎所有第三方客户端都支持。适用于 Chatbox、Cherry Studio、Cursor、Cline、Dify 等。
- **Anthropic Messages 模式**（`/apps/anthropic`）：面向 Claude Code、OpenClaw、Hermes、Codex 等 Anthropic 协议原生客户端，可以直接复用社区生态。
- **DashScope 原生 API**：用 Postman/cURL 调试图像、视频等多模态生成任务时使用，参见 [使用 Postman 或 cURL 调用图像/视频生成 API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

## 选型建议

- **想要图形化对话、知识库问答**：优先选 Cherry Studio 或 Chatbox，桌面端开箱即用，支持文件附件与多会话。
- **追求编码效率，习惯终端**：Claude Code、Qwen Code、OpenCode、Codex 都是 CLI 形态，配合 Coding Plan 性价比最高，可参考 [Coding Plan 支持模型](https://help.aliyun.com/zh/model-studio/coding-plan)。
- **希望留在 IDE 内**：VS Code 用户可选 Cline 或 Cursor（独立编辑器），JetBrains 用户可选 Qoder/Qoder CN，国内开发者使用 [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md) 体验本土化场景更佳。
- **需要把模型接入聊天群组**：[OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md) 提供钉钉、飞书、企业微信、QQ 渠道插件以及 Cron 定时任务能力，可一站式搭建群机器人。
- **构建低代码工作流或 RAG 应用**：[Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md) 适合配合知识库做企业级应用编排。
- **图像/视频生成 API 调试**：直接用 [Postman 或 cURL](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)，便于查看[异步任务](../concepts/async-task.md)回调与 RequestId。

## 关键配置注意事项

- **配置文件局部修改**：以 OpenClaw 为例，配置文件位于 `~/.openclaw/openclaw.json`，添加新计费方式时应保留已有 `models`、`agents`、`channels`、`plugins` 配置，仅追加新字段，避免直接全量替换导致历史会话或渠道丢失。多数 CLI 形态工具（Claude Code、Codex 等）都遵循类似约定。
- **网关鉴权**：本地单机使用时通常将 `auth.mode` 设为 `none`，如需在团队内共享或远程访问，应启用 token 鉴权（如 `openclaw doctor --fix`）。
- **重启生效**：修改 Base URL、API Key 或模型清单后必须重启网关或重新加载客户端（CLI：`<tool> gateway restart`；桌面端：完全退出后重新启动），否则旧会话仍使用旧配置。
- **思考模式兼容**：部分模型（如 Qwen3、DeepSeek、Kimi、GLM 系列）支持思考模式输出，在 Anthropic 协议下需要在客户端设置 `compat.thinkingFormat = "openai"`，否则可能丢失推理内容。
- **上下文窗口与 maxTokens**：各模型上下文与最大输出差异较大（如 Qwen3.6-Plus 1,000,000 token 上下文 / 65,536 输出；MiniMax-M2.5 204,800 / 131,072）。客户端的 `models` 字段需如实填写，避免裁剪过短导致 Agent 任务被截断。

## 常见问题

- **`HTTP 401: Incorrect API key`**：API Key 与 Base URL 计费方式不匹配，或 Key 已失效；按上文 Base URL 速查表核对地域与计费方式。
- **找不到模型**：模型不在该计费方式的可用列表中。Token Plan、Coding Plan 各有专属模型清单，按量付费走[模型广场](https://bailian.console.aliyun.com/?tab=model#/model-market)。
- **历史缓存导致配置不生效**：删除工具自身的 provider 缓存（如 OpenClaw 的 `~/.openclaw/agents/main/agent/models.json` 中的 `providers` 字段）再重启，或对比 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) 中列出的其它客户端的清缓存方法。
- **多渠道机器人无响应**：检查渠道插件状态（如 `openclaw status` / `openclaw plugins list`），确认渠道凭证有效、网关已重启、Bot 已加入群聊。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)



