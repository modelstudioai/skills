# 快速开始

三步完成 Token Plan 个人版订阅和接入：选择套餐、获取 API Key、配置 AI 工具。

## 步骤一：订阅 Token Plan 个人版

访问 [Token Plan 个人版购买页面](https://bailian.console.aliyun.com/cn-beijing/subscription/overview)，选择套餐档位和订阅周期，完成订阅。

购买须知：

-   **RAM 用户授权**：RAM 用户使用 Token Plan 前，需由主账号完成以下授权：
    
    1.  在 [RAM 控制台](https://ram.console.aliyun.com/)为该 RAM 用户授予 `AliyunTokenPlanReadOnlyAccess`（只读）或 `AliyunTokenPlanFullAccess`（管理）系统策略，同时授予 `AliyunBSSReadOnlyAccess` 系统策略。
    2.  在百炼控制台[账号管理](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list)页面，为该 RAM 用户分配管理员或订阅套餐权限。

## 步骤二：获取 Token Plan 个人版 API Key 和 Base URL

-   **API Key**：订阅完成后，在 Token Plan 控制台的**我的订阅**页面生成 API Key。API Key 仅在生成时完整显示一次，请立即复制并妥善保存。此 API Key 以 `sk-sp-` 开头，用于模型调用、按 Credits 抵扣；Harness 权益工具（联网搜索增强版等）使用百炼 API Key（以 `sk-` 开头），详见[接入 Harness 工具](raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-harness-tool.md)。
-   **Base URL**：根据 AI 工具支持的协议，选择对应的 Base URL。

**协议**

**Base URL**

OpenAI 兼容

`[https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1](https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1)`

Anthropic 兼容

`[https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic](https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic)`

## 步骤三：接入模型

将 API Key 和 Base URL 配置到 AI 工具，即可调用 Token Plan 支持的模型进行对话。

![](https://unpkg.com/@lobehub/icons-static-svg@latest/icons/openclaw-color.svg)**[OpenClaw](raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)**

开源、自托管个人 AI 助手

![](https://unpkg.com/@lobehub/icons-static-svg@latest/icons/nousresearch.svg)**[Hermes Agent](raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)**

开源 AI 代理框架，内置自学习循环

![](https://unpkg.com/@lobehub/icons-static-svg@latest/icons/claude-color.svg)**[Claude Code](raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)**

AI 终端编码助手，支持自然语言编程

![](https://unpkg.com/@lobehub/icons-static-svg@latest/icons/opencode.svg)**[OpenCode](raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)**

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

![](https://unpkg.com/@lobehub/icons-static-svg@latest/icons/qwen-color.svg)**[千问办公助理](https://help.aliyun.com/zh/model-studio/qwen-office-assistant)**

千问 APP 办公助理，处理文档、表格等办公任务

**[更多工具](raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)**

其他编程工具

## 步骤四：接入 Harness 权益工具

Standard 与 Pro 套餐附赠的 Harness 权益工具（联网搜索增强版、图像生成等 AgentStudio 工具，不占 Credits）。在百炼控制台[**我的订阅**](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)页面切换到**Harness 权益**页签，常用接入方式：

-   **一键接入**：点击**一键接入**，选择需要的工具并复制配置指令，发给本地 Agent（支持 Qoder、QwenWork、Claude Code、Codex）。首次使用需安装[百炼 CLI](https://bailian.aliyun.com/cli/install.md) 并执行 `bl auth login --console` 登录，再通过 `bl config show` 获取 api\_key。
-   **参考文档**：在工具卡片点击**说明文档**或**AI Native 接入**，按该工具的指引接入。

完整接入流程详见[接入 Harness 工具](raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-harness-tool.md)。

## 可选：接入多模态生成模型

多模态生成模型（wan2.7-image、happyhorse-1.1-t2v 等）需使用专用端点，通过 AI 工具的 Skill 或扩展机制接入，详见[接入多模态生成模型](raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)。
