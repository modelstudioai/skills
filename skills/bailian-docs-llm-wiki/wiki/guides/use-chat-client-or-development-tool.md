# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端及开发平台接入模型服务，覆盖终端 CLI、IDE 插件、Web UI 和工作流系统等场景。开发者可根据使用习惯选择适配的客户端，并按计费方案（Token Plan 个人版/团队版、Coding Plan 或按量计费）配置对应凭证与协议。所有工具均基于 OpenAI 或 Anthropic 兼容 API 协议，无需修改业务逻辑即可快速切换。

## 支持的模型/功能

百炼支持的模型能力取决于所选计费方案和协议类型：

- **Token Plan 个人版/团队版**：仅支持文本生成类模型（如 `qwen3.8-max`、`qwen3.7-plus`、`glm-5.3`、`deepseek-v4-pro`），不支持图像、视频、语音或多模态模型（如 Qwen-VL、Qwen-Omni、万相）。详见 [Token Plan 个人版支持的模型](raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)。
- **Coding Plan**：支持文本生成类模型（如 `qwen3.7-plus`），不支持思考模式（`enable_thinking`）或视觉模型；部分工具（如 Cursor 免费版）强制限制为 `auto` 模式 [Cursor](raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)。
- **按量计费**：支持全量模型，包括文生图（`wan2.6-t2i`）、文生视频（`wan2.1-v2v`）、多模态（`qwen-vl`）、语音（`qwen-audio`）及思考增强模型（`qwen3.8-max` with `enable_thinking=true`）。Dify 等工作流平台**仅允许使用按量计费 API Key**，严禁混用 Token Plan/Coding Plan 凭证 [Dify](raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。
- **协议差异**：
  - OpenAI 兼容协议（`/compatible-mode/v1/chat/completions`）适用于绝大多数客户端（Cursor、WorkBuddy、Cherry Studio、QwenPaw 等）；
  - Anthropic 兼容协议（`/apps/anthropic`）主要用于 Hermes Agent、Claude Code、OpenClaw 等强调 reasoning 流程的工具；
  - 图像/视频生成 API 使用独立路径（如 `/api/v1/services/aigc/text2image/image-synthesis`），不兼容 Chat Completions 协议 [使用Postman或cURL调用图像/视频生成API](raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

> **注意**：千问 APP 工作助理**仅支持 Token Plan（个人版/团队版）**，明确不支持按量计费或 Coding Plan [千问](raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)。

## 关键参数

| 参数 | 说明 | 示例值 | 注意事项 |
|------|------|--------|----------|
| `Base URL` | 必填，决定协议类型与地域 | OpenAI：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>Anthropic：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` | 地域必须与 API Key 匹配；按量计费需替换 `{WorkspaceId}`；Token Plan/Coding Plan 的 Base URL **不可互换** |
| `API Key` | 必填，四类方案凭证完全隔离 | Token Plan 个人版：`sk-xxx`（控制台 Subscription 页面获取）<br>按量计费：`sk-xxx`（控制台 API Key 页面获取） | 错误混用（如用 Token Plan Key 配按量 Base URL）将返回 `401 Incorrect API key provided` |
| `Model ID` | 必填，区分大小写且不可加后缀 | `qwen3.8-max`（正确）<br>`qwen3.8-max-v1`（错误） | Cursor 要求部分模型名转义（`glm-5.3` → `glm-5-3`）；Qoder CN 仅支持文本生成模型，选错将报 `"Unknown Custom model Exception"` |
| `enable_thinking` / `effort` | 可选，启用推理增强 | `{"extra_body": {"enable_thinking": true}}`（Qwen Code）<br>`"effort": "xhigh"`（Codex） | 部分模型（如 `qwen3.8-max`）强制要求开启思考模式，否则报错 `"The value of the enable_thinking parameter is restricted to True"` |

## 使用方式

### 1. 客户端安装与配置通用流程
- **安装**：各工具均提供一键脚本（如 `curl -fsSL https://.../install.sh \| bash`）、npm 全局安装（`npm install -g xxx`）或官网下载安装包（Cursor、WorkBuddy、Qoder CN）。
- **配置入口**：
  - CLI 工具（Hermes、Claude Code、Qwen Code）：运行 `/auth` 或 `xxx config set` 命令；
  - 桌面客户端（Cursor、Cherry Studio、WorkBuddy）：设置 → 模型 → 添加自定义模型；
  - IDE 插件（Cline、Qoder JetBrains）：侧边栏插件面板 → 设置 → 模型配置；
  - Web 平台（Dify）：设置 → 模型供应商 → 通义千问插件 → API Key 配置。

### 2. 四类计费方案配置要点
| 方案 | Base URL（OpenAI） | Base URL（Anthropic） | API Key 来源 | 典型适用工具 |
|------|---------------------|------------------------|--------------|--------------|
| **Token Plan 个人版** | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` | [Subscription → Overview](https://bailian.console.aliyun.com/cn-beijing/subscription/overview) | OpenClaw、Hermes Agent、QwenPaw |
| **Token Plan 团队版** | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` | [UAC Admin → Members](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list) | DeepSeek Harness、Qoder CN |
| **Coding Plan** | `https://coding.dashscope.aliyuncs.com/v1` | `https://coding.dashscope.aliyuncs.com/apps/anthropic` | [Subscription → Coding Plan](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan) | Claude Code、OpenCode |
| **按量计费** | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic` | [API Key 管理](raw/model-api-reference/preparations/get-api-key.md) | Dify、Postman、自定义 SDK |

> **注意**：Dify 明确禁止使用 Token Plan/Coding Plan 凭证，仅接受按量计费 API Key；违规使用将导致订阅暂停或 Key 封禁 [Dify](raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。

### 3. 验证与调试
- **连接测试**：所有客户端均提供“测试连接”按钮（WorkBuddy、Cherry Studio）或命令行验证（`hermes --version`、`qwen --version`）。
- **错误排查**：
  - `401`：检查 API Key 与 Base URL 是否同属一方案且地域一致；
  - `400 InternalError.Algo.InvalidParameter`：Cline/Qoder CLI 需勾选 `Enable R1 messages format`；
  - 模型不存在：确认模型 ID 与文档列表完全一致（如 `qwen3.8-flash` 不可写作 `qwen38flash`）。

## 限制和注意事项

- **方案隔离性**：Token Plan 个人版、Token Plan 团队版、Coding Plan、按量计费的 API Key 和 Base URL **完全不互通**。混用将导致认证失败，且可能触发风控策略 [Qoder CN](raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)。
- **地域绑定**：按量计费的 API Key 与 Workspace ID 强绑定，华北2（北京）Key 无法用于新加坡地域服务；Token Plan/Coding Plan 的 Base URL 已固化地域，无需替换 WorkspaceId。
- **功能限制**：
  - Token Plan/Coding Plan **不支持**图像/视频/语音/OCR 等 AIGC 模型，仅限文本生成；
  - Cursor 免费版仅支持 `auto` 模型，付费版才可指定 `qwen3.8-max` 等具体 ID；
  - Dify、n8n、Coze 等工作流平台**禁止接入** Token Plan/Coding Plan，仅限按量计费 [更多工具](raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。
- **安全实践**：
  - 生产环境避免硬编码 API Key，应使用环境变量（如 `BAILIAN_API_KEY`）或密钥管理服务；
  - 本地调试时，建议禁用网关鉴权（如 OpenClaw 的 `auth.mode: none`），但上线前必须启用 token 鉴权（运行 `openclaw doctor --fix`）；
  - 按量计费用户需关注免费额度地域限制（仅华北2有效），跨地域调用将直接计费 [Cherry Studio](raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [千问](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [DeepSeek Harness](../../raw/model-user-guide/use-chat-client-or-development-tool/deepseek-harness.md)
- [接入 WorkBuddy](../../raw/model-user-guide/use-chat-client-or-development-tool/workbuddy.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)


