# 快速开始

三步完成 Token Plan 团队版订阅和接入：选择套餐、获取 API Key、配置 AI 工具。

## 步骤一：订阅 Token Plan 团队版

访问 [Token Plan 团队版购买页面](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/overview)，选择套餐档位和订阅周期并完成订阅，主账号和 RAM 账号均可订阅。

-   **RAM 用户授权**：RAM 用户使用 Token Plan 前，需由主账号完成以下授权：
    
    1.  在 [RAM 控制台](https://ram.console.aliyun.com/)为该 RAM 用户授予 `AliyunTokenPlanReadOnlyAccess`（只读）或 `AliyunTokenPlanFullAccess`（管理）系统策略，同时授予 `AliyunBSSReadOnlyAccess` 系统策略。
    2.  在百炼控制台[账号管理](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/uac-admin/organization/members/list)页面，为该 RAM 用户分配管理员或订阅套餐权限。

## 步骤二：获取 API Key 和 Base URL

-   **API Key**：在 Token Plan 控制台的成员管理页面或管理平台创建成员账号，分配席位后，为成员生成 API Key。详见团队管理。
    
    API Key 使用须知：
    
    -   生成 API Key 前，需在**成员管理**页面为对应账号分配席位。
    -   Token Plan API Key 仅在创建或重置时完整显示一次，之后控制台仅显示脱敏信息（如 `sk-sp-****`），无法再次查看完整内容。请在生成时立即复制并妥善保存。
    -   Token Plan API Key 以 `sk-sp-` 开头，与百炼通用 API Key（`sk-` 开头）格式不同，两者不可混用。
-   **Base URL**：根据 AI 工具支持的协议，选择对应的 Base URL。
    

**协议**

**Base URL**

OpenAI 兼容

`[https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1](https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1)`

Anthropic 兼容

`[https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic](https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic)`

**重要**Token Plan、Coding Plan 和按量付费的 API Key 与 Base URL 完全隔离，必须配套使用，不可混用。

-   **Token Plan 团队版**：使用 `sk-sp-` 开头的套餐 API Key + 上方表格中的 Base URL。
-   **Coding Plan**：使用 Coding Plan API Key + `https://coding.dashscope.aliyuncs.com/v1`。
-   **按量付费**：使用通用 API Key（`sk-` 开头）+ `https://dashscope.aliyuncs.com/compatible-mode/v1`。

如果购买了 Token Plan 但使用了通用 API Key 或其他计费模式的 Base URL，会导致调用走按量计费通道产生意外扣费，或返回 401/403 鉴权失败错误。

## 步骤三：接入 AI 工具

将 API Key 和 Base URL 配置到 AI 工具中，即可开始使用。

![](https://unpkg.com/@lobehub/icons-static-svg@latest/icons/openclaw-color.svg)**[OpenClaw](raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)**

开源、自托管个人 AI 助手

![](https://unpkg.com/@lobehub/icons-static-svg@latest/icons/nousresearch.svg)**[Hermes Agent](raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)**

开源 AI 代理框架，内置自学习循环

![](https://unpkg.com/@lobehub/icons-static-svg@latest/icons/claude-color.svg)**[Claude Code](raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)**

AI 终端编码助手，支持自然语言编程

![](https://unpkg.com/@lobehub/icons-static-svg@latest/icons/opencode.svg)**[OpenCode](https://help.aliyun.com/zh/model-studio/opencode)**

开源 AI 编程代理工具

![](https://unpkg.com/@lobehub/icons-static-svg@latest/icons/cursor.svg)**[Cursor](raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)**

AI 原生代码编辑器

![](https://unpkg.com/@lobehub/icons-static-svg@latest/icons/codex.svg)**[Codex](raw/model-user-guide/use-chat-client-or-development-tool/codex.md)**

OpenAI 推出的命令行编程工具

![](https://unpkg.com/@lobehub/icons-static-svg@latest/icons/qwen-color.svg)**[Qwen Code](raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)**

开源命令行 AI 编码工具

![](https://cdn.jsdelivr.net/gh/agentscope-ai/QwenPaw@main/website/public/qwenpaw-symbol.png)**[QwenPaw](raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)**

开源个人 AI 助手，支持本地与云端部署

![](https://unpkg.com/@lobehub/icons-static-svg@latest/icons/cherrystudio-color.svg)**[Cherry Studio](raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)**

多模型桌面客户端

![](https://cdn.jsdelivr.net/gh/chatboxai/chatbox@main/assets/icon.png)**[Chatbox](https://help.aliyun.com/zh/model-studio/cline-tool)**

跨平台 AI 桌面客户端

![](https://unpkg.com/@lobehub/icons-static-svg@latest/icons/cline.svg)**[Cline](raw/model-user-guide/use-chat-client-or-development-tool/cline.md)**

VS Code 扩展，智能代码补全和调试

![](https://unpkg.com/@lobehub/icons-static-svg@latest/icons/qoder-color.svg)**[Qoder](raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)**

面向真实软件开发的 Agentic 编码平台

![](https://unpkg.com/@lobehub/icons-static-svg@latest/icons/bailian-color.svg)**[Lingma](raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)**

阿里云智能编码助手，提供独立 IDE

![](https://unpkg.com/@lobehub/icons-static-svg@latest/icons/kilocode.svg)**[Kilo CLI](raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)**

轻量高性能命令行编程工具

![](https://unpkg.com/@lobehub/icons-static-svg@latest/icons/deepseek-color.svg)**[DeepSeek Harness](raw/model-user-guide/use-chat-client-or-development-tool/deepseek-harness.md)**

DeepSeek 开源 AI Agent 框架

![](https://unpkg.com/@lobehub/icons-static-svg@latest/icons/qwen-color.svg)**[千问办公助理](raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)**

千问 APP 办公助理，处理文档、表格等办公任务

**[更多工具](raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)**

其他编程工具

## 可选：接入多模态生成模型

Token Plan 团队版支持多模态生成模型（wan2.7-image、happyhorse-1.1-t2v 等）。多模态生成模型使用独立的接口，需要通过 AI 工具的 Skill 或扩展机制接入，详见[接入多模态生成模型](raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。

## 可选：接入 Harness 工具

通过 Harness 工具调用，模型可以在对话中调用联网搜索、文搜图、图搜图、网页抓取、代码解释器等扩展能力。当前仅 qwen3.7、qwen3.8 支持原生工具调用，通过 Responses API 直接调用，Harness 工具按抵扣系数消耗 Credits。详见[接入 Harness 工具](raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)。
