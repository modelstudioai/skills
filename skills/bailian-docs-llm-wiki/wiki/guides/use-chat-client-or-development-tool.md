# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端及开发平台接入模型服务，覆盖终端 CLI、IDE 插件、Web UI 和工作流平台等场景。开发者可根据使用习惯选择适配的客户端，并按计费方案（[Token](../concepts/token.md) Plan 个人版/团队版、Coding Plan 或按量计费）配置对应凭证与协议。所有工具均基于 OpenAI 兼容或 Anthropic 兼容 API 协议，无需修改业务逻辑即可快速切换。

## 支持的模型/功能

百炼支持的模型能力因接入方式和计费方案而异：

- **文本生成模型**：全量支持 `qwen3.8-max`、`qwen3.8-flash`、`qwen3.7-plus`、`qwen3.7-max`、`qwen3.6-flash`、`glm-5.3`、`glm-5.2`、`deepseek-v4.*` 等主流模型；其中 `qwen3.7+` 及更高版本默认启用思考模式（reasoning），需在请求中显式启用 `enable_thinking` 或使用 `effort` 参数控制推理深度。
- **多模态支持**：`qwen3.8-max`、`qwen3.8-flash`、`qwen3.7-plus` 等支持图像输入（`input: ["text", "image"]`），但需客户端协议与配置匹配（如 OpenClaw 的 `compat.thinkingFormat: "openai"`）[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)。
- **非文本模型限制**：Qwen-Omni、Qwen-Audio、Qwen-OCR、万相（文生图/视频）等模型**不支持**在 Dify、Coze、n8n 等工作流平台直接配置，必须通过 HTTP 节点或原生 API 调用 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)；千问 APP 工作助理仅支持 [Token](../concepts/token.md) Plan，**不支持**按量计费或 Coding Plan [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)。
- **协议差异**：
  - OpenAI 兼容协议：Base URL 以 `/compatible-mode/v1` 结尾，使用 `/chat/completions` 端点（如 WorkBuddy 要求完整路径）；
  - Anthropic 兼容协议：Base URL 以 `/apps/anthropic` 结尾，使用 `anthropic-messages` API 模式（如 Hermes Agent、Claude Code）。

> **注意**：部分文档对模型命名规范存在矛盾。例如 Cursor 文档要求将 `glm-5.3` 写为 `glm-5-3`，而 OpenCode、Kilo CLI 等文档中直接使用 `glm-5.3`；Qoder CN 文档明确说明“仅支持文本生成模型”，但 Qoder IDE 配置界面实际允许选择 `qwen3.8-max`（含图像输入能力）。建议以 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md) 中的运行时校验为准，避免依赖静态配置列表。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `base_url` | 必填，模型服务端点地址，**必须与 API Key 方案及地域严格匹配** | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（[Token](../concepts/token.md) Plan 个人版 OpenAI）<br>`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic`（按量计费 Anthropic） |
| `api_key` | 必填，专属凭证，**四类方案互不通用** | `sk-xxx`（Token Plan 个人版）<br>`sk-coding-xxx`（Coding Plan） |
| `model` | 必填，模型 ID，**区分大小写且不可加前后缀**（如 `qwen3.7-plus` ≠ `Qwen3.7-Plus`） | `qwen3.7-plus`, `auto` |
| `enable_thinking` / `effort` | 思考模式开关，Qwen3.7+ 系列必需 | `true`（JSON body）<br>`"effort": "xhigh"`（Codex model-catalog） |
| `workspace_id` | 按量计费必需，URL 中 `{WorkspaceId}` 需替换为真实 ID | `ws-abc123xyz` |

## 使用方式

### 1. 客户端安装
- **CLI 工具**（如 Hermes Agent、Qwen Code、Kilo CLI）：依赖 Node.js ≥18，通过 `npm install -g <pkg>` 安装；
- **桌面应用**（如 Cursor、Cherry Studio、WorkBuddy）：从官网下载安装包，无需本地运行时依赖；
- **IDE 插件**（如 Cline、Qoder JetBrains 插件）：在 VS Code 或 JetBrains 扩展市场安装；
- **Web 平台**（如 Dify、QwenPaw）：部署后通过浏览器访问，Dify 需额外安装「通义千问」插件 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。

### 2. 凭证配置
- **环境变量**：适用于 Codex（`OPENAI_API_KEY`）、DeepSeek Harness（`BAILIAN_API_KEY`）等；
- **配置文件**：OpenClaw（`~/.openclaw/openclaw.json`）、Hermes（`~/.hermes/config.yaml`）、Qwen Code（`~/.qwen/settings.json`）；
- **GUI 设置**：Cursor、Cherry Studio、WorkBuddy 均提供可视化模型配置界面；
- **交互式命令**：Qwen Code 支持 `/auth`、Qoder CLI 支持 `/model` 启动向导。

### 3. 协议与端点选择
- 所有 OpenAI 兼容工具（Cursor、Cherry Studio、WorkBuddy、Cline）**必须使用 `/chat/completions` 端点**，不可省略路径；
- Anthropic 兼容工具（Claude Code、Hermes Agent）需设置 `api_mode: anthropic_messages` 且 Base URL 以 `/apps/anthropic` 结尾；
- 图像/视频生成等 AIGC API **不适用本主题客户端**，需直接调用 `POST /api/v1/services/aigc/text2image/image-synthesis` 等专用接口 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

## 限制和注意事项

- **计费方案适用范围严格受限**：
  - Token Plan 个人版/团队版、Coding Plan **仅限 AI 编程工具与 OpenClaw 类 Agent**（如 OpenClaw、Hermes、Qwen Code、Qoder）；
  - **工作流/自动化平台（Dify、n8n、Coze）严禁使用上述套餐 API Key**，否则可能导致订阅暂停 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)；
  - Postman、cURL、自定义脚本等 **仅用于测试，禁止生产调用**，且不支持 Token Plan/Coding Plan。

- **地域与 Workspace ID 绑定**：
  - 按量计费的 `base_url` 中 `{WorkspaceId}` 必须与 API Key 所属业务空间一致；
  - 免费额度**仅限华北2（北京）地域**，使用新加坡/美国端点将产生费用 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。

- **模型兼容性陷阱**：
  - Cursor 免费版仅支持 `auto` 模型，指定 `qwen3.7-plus` 将报错 `Named models unavailable Free plans can only use Auto`；
  - Qoder CN 企业版**不支持接入百炼**，仅限个人社区版/专业版；
  - 所有工具中模型名称必须与百炼控制台显示的 ID **完全一致**（如 `qwen3.8-flash` 不可写作 `qwen38-flash` 或 `Qwen3.8-Flash`）。

- **安全与调试**：
  - OpenClaw 默认禁用网关鉴权（`auth.mode: none`），**仅限单机使用**，共享环境必须运行 `openclaw doctor --fix` 启用 token 鉴权；
  - 报错 `401 Incorrect API key provided` 90% 原因为 API Key 与 Base URL 方案/地域不匹配，需逐项核对；
  - 报错 `400 InternalError.Algo.InvalidParameter` 多因未启用 R1 messages 格式（Qwen3/QwQ 模型需勾选 `Enable R1 messages format`）。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [千问](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [DeepSeek Harness](../../raw/model-user-guide/use-chat-client-or-development-tool/deepseek-harness.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [接入 WorkBuddy](../../raw/model-user-guide/use-chat-client-or-development-tool/workbuddy.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)


