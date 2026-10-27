# use chat client or development tool

本文档面向开发者，说明如何将阿里云百炼平台的模型能力接入主流 AI 编程工具、桌面客户端及开发框架。支持的接入方式包括 Token Plan 个人版/团队版、Coding Plan 和按量计费四种方案，绝大多数工具通过 OpenAI 兼容协议（`/compatible-mode/v1`）或 Anthropic 兼容协议（`/apps/anthropic`）对接，无需修改业务逻辑即可复用现有 SDK 或配置习惯。

## 支持的模型/功能

百炼支持的模型能力因接入方案而异，**并非所有模型在所有套餐下均可用**：

- **Token Plan 个人版与团队版**：仅支持文本生成类模型（如 `qwen3.8-max`、`qwen3.7-plus`、`glm-5.3`、`deepseek-v4.1-flash`），不支持图像、视频、语音或多模态理解类模型（如 `wan2.6-t2i`、`qwen-omni`、`qwen-audio`）。[更多细节见 Token Plan 个人版概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)。
- **Coding Plan**：支持 `qwen3.7-plus` 及其向下兼容模型（如 `qwen3.6-flash`），但不支持 `qwen3.8-*` 系列及 `glm-5.*` 系列。[Coding Plan 支持模型清单详见此处](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)。
- **按量计费**：覆盖最全模型集，包括文生图（`wan2.6-t2i`）、文生视频（`wan2.6-v2v`）、多模态理解（`qwen-vl-plus`）、语音（`qwen-audio`）等，且支持 OpenAI、Anthropic、DashScope 原生三套协议。[完整模型列表参见 OpenAI 兼容接口文档](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。

> **注意**：千问 APP 的工作助理功能**仅支持 Token Plan（个人版和团队版）**，明确不支持按量计费或 Coding Plan [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)。此限制与其他工具（如 Cursor、Qwen Code）不同，需特别注意。

## 关键参数

所有接入均依赖三个核心参数：**API Key**、**Base URL** 和 **Model ID**，必须严格匹配同一计费方案与地域：

| 计费方案       | OpenAI 兼容 Base URL（华北2·北京）                            | Anthropic 兼容 Base URL（华北2·北京）                         | API Key 来源                                                                 |
|----------------|---------------------------------------------------------------|----------------------------------------------------------------|------------------------------------------------------------------------------|
| Token Plan 个人版 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` | [Token Plan 个人版控制台](https://bailian.console.aliyun.com/cn-beijing/subscription/overview) |
| Token Plan 团队版 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` | [Token Plan 团队版管理页](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list) |
| Coding Plan      | `https://coding.dashscope.aliyuncs.com/v1`                     | `https://coding.dashscope.aliyuncs.com/apps/anthropic`          | [Coding Plan 控制台](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan)     |
| 按量计费         | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic` | [API Key 获取指南](../../raw/model-api-reference/preparations/get-api-key.md) |

- **Model ID** 必须与百炼官方模型名**完全一致**（区分大小写，无额外前缀/后缀），例如 `qwen3.8-max` 不可写作 `Qwen38Max` 或 `qwen38max`。部分工具（如 Cursor）要求将 `.` 替换为 `-`（即 `glm-5.3` → `glm-5-3`），详见各工具文档。
- **思考模式（Thinking Mode）**：`qwen3.*` 系列中带 `-max`、`-flash` 后缀的模型默认启用思考，调用时需在请求体中显式传入 `"enable_thinking": true`（如 Qwen Code、Cline）或通过 `effort` 参数控制（如 OpenClaw、Codex）。[OpenClaw 配置示例](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md) 中已体现该参数。

## 使用方式

接入流程高度统一，分为三步：安装工具 → 配置凭证 → 验证调用。

1. **安装**：各工具提供脚本（`curl`/`bash`）、包管理器（`npm`/`pip`）或 GUI 安装包。例如：
   - OpenClaw：`curl -fsSL https://openclaw.ai/install.sh | bash`
   - Hermes Agent：`curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash`
   - QwenPaw：`curl -fsSL https://qwenpaw.agentscope.io/install.sh | bash`

2. **配置凭证**：根据工具类型选择配置方式：
   - **命令行工具（Hermes、Claude Code、Kilo CLI）**：通过 CLI 命令（`hermes config set`）或编辑配置文件（`~/.hermes/config.yaml`、`~/.claude/settings.json`）。
   - **桌面客户端（Cursor、WorkBuddy、Cherry Studio）**：通过图形界面设置 → 模型 → 添加自定义模型，填入 Base URL、API Key 和 Model ID。
   - **IDE 插件（Cline、Qoder）**：在 VS Code 或 JetBrains 设置面板中选择 OpenAI 兼容协议，输入对应参数。
   - **开发平台（Dify）**：**仅支持按量计费 API Key**，且必须使用 `OpenAI-API-compatible` 插件配置端点，Token Plan/Coding Plan 套餐在此场景下**明确不被支持** [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。

3. **验证调用**：启动工具后，发送简单请求（如“你好”）并检查响应。若返回 `401` 错误，优先检查 API Key 与 Base URL 是否来自同一方案；若返回 `400` 或模型不存在错误，核对 Model ID 拼写及套餐支持范围。

## 限制和注意事项

- **协议与端点强绑定**：OpenAI 兼容端点（`/compatible-mode/v1`）**仅接受 `/chat/completions` 路径**，不可直接访问 `/v1` 根路径；Anthropic 兼容端点（`/apps/anthropic`）**仅接受 `/messages` 路径**，不可混用。WorkBuddy 明确声明“仅支持 OpenAI 兼容的 Chat Completions 协议，不支持 Responses API 与 Anthropic 协议” [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/workbuddy.md)。
- **地域一致性**：按量计费的 API Key、Base URL 中的 `{WorkspaceId}`、控制台查看的免费额度三者必须同属一个地域（如华北2·北京）。跨地域使用（如北京 Key + 新加坡 URL）将导致认证失败或费用异常 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。
- **禁止滥用场景**：Token Plan 个人版、团队版及 Coding Plan **严禁用于工作流平台（Dify、n8n）、API 测试工具（Postman、cURL）或自定义后端应用**。此类调用视为违规，可能导致订阅暂停或 API Key 封禁 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。
- **模型名称转换规则**：Cursor、Chatbox 等工具要求模型名中的 `.` 替换为 `-`（如 `glm-5.3` → `glm-5-3`），而 OpenClaw、Hermes 等则保持原名。务必查阅目标工具文档确认格式。
- **免费额度限制**：新人免费额度**仅适用于华北2（北京）地域的按量计费模型**，且各模型额度独立计算，不可跨模型共享。Token Plan/Coding Plan 无免费额度概念。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [千问](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [接入 WorkBuddy](../../raw/model-user-guide/use-chat-client-or-development-tool/workbuddy.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [DeepSeek Harness](../../raw/model-user-guide/use-chat-client-or-development-tool/deepseek-harness.md)


