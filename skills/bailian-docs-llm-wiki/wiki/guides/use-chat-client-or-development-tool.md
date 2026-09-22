# use chat client or development tool

阿里云百炼支持多种主流 AI 编程客户端与开发工具（如 Hermes Agent、Claude Code、Cursor 等）及通用开发工具（如 Postman、cURL、Dify），通过 OpenAI 或 Anthropic 兼容协议接入。开发者可根据使用场景选择预置客户端（面向终端/IDE/桌面）或低代码/代码级工具（面向工作流、测试或自定义集成）。所有工具均需按计费方案配置对应 API Key 与 Base URL，且不同方案凭证不互通。

## 支持的模型/功能

百炼支持的模型能力因接入方案而异：

- **[Token](../concepts/token.md) Plan（个人版/团队版）**：仅支持文本生成类模型（如 `qwen3.8-max`、`qwen3.7-plus`、`glm-5.3`、`deepseek-v4-pro`），不支持多模态、Embedding、Rerank 或 AIGC（图像/视频）模型；[Token Plan 个人版支持的模型](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md) 和 [Token Plan 团队版支持的模型](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 均明确限定为文本生成类。
- **Coding Plan**：支持指定文本模型（如 `qwen3.7-plus`），详见 [Coding Plan 支持的模型](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)；不支持 [Token](../concepts/token.md) Plan 中的全部模型变体（如 `qwen3.8-flash`）。
- **按量计费**：覆盖最全模型谱系，包括文本（`qwen3`, `glm`, `deepseek`）、视觉（`qwen-vl`, `qvq`）、语音（`qwen-audio`）、OCR（`qwen-ocr`）、多模态（`qwen-omni`）、文生图（`wan2.6-t2i`）等；具体支持列表见 [兼容 OpenAI 协议的模型](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope#7f9c78ae99pwz) 及 [Anthropic 兼容 API](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。
- **特殊限制**：千问 APP 工作助理仅支持 [Token](../concepts/token.md) Plan，不支持按量计费或 Coding Plan；Dify 等工作流平台**不支持** Token Plan 和 Coding Plan，仅允许使用按量计费 API Key —— 此限制在 [不支持的工具类型](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) 文档中明确说明。

> **注意**：文档 17（Dify）与文档 19（更多工具）存在直接矛盾：前者强调“Dify 不支持 Token Plan/Coding Plan”，后者在“不支持的工具类型”中将 Dify 列为典型示例，但未说明其唯一例外是“仅允许按量计费”。该表述一致，无实质冲突；但需注意 Dify 的插件机制（如通义千问插件）对 API Key 权限有额外校验（例如要求 `qwen-turbo` 调用权限），此细节在 [Dify 常见问题](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md) 中补充说明。

## 关键参数

所有工具配置均围绕以下核心参数展开，必须严格匹配所选计费方案：

| 参数 | Token Plan 个人版 | Token Plan 团队版 | Coding Plan | 按量计费 |
|------|------------------|-------------------|-------------|-----------|
| **API Key** | 专属 Token Plan 个人版 Key（控制台获取） | 专属 Token Plan 团队版 Key（控制台获取） | Coding Plan 专属 Key | 百炼通用 API Key（`sk-` 开头） |
| **Base URL（OpenAI 协议）** | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | 同上 | `https://coding.dashscope.aliyuncs.com/v1` | `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`（需替换 `{WorkspaceId}`） |
| **Base URL（Anthropic 协议）** | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` | 同上 | `https://coding.dashscope.aliyuncs.com/apps/anthropic` | `https://{WorkspaceId}.{region}.maas.aliyuncs.com/apps/anthropic`（需替换 `{WorkspaceId}`） |
| **模型 ID 格式** | 多数工具要求原样填写（如 `qwen3.8-max`），但 Cursor 等需将 `.` 替换为 `-`（如 `glm-5.3` → `glm-5-3`） | 同 Token Plan 个人版 | 同上，且部分模型名需调整（如 `kimi-k2.5` → `kimi-k2-5`） | 同上，且需确保[模型部署](../concepts/model-deployment.md)地域与 Workspace ID 所属地域一致 |

> **注意**：文档 1（Hermes Agent）中提及 Anthropic 协议 Base URL 以 `/apps/anthropic` 结尾，而文档 19（更多工具）表格中明确列出相同路径；但文档 5（Cursor）和文档 8（DeepSeek Harness）等均使用 OpenAI 协议（`/compatible-mode/v1`）。二者并存无矛盾，属协议选择差异。关键约束在于：**API Key 必须与 Base URL 方案（Token Plan/Coding/按量）及地域（按量计费）严格一致**，否则返回 401 错误（见文档 10、15、16）。

## 使用方式

### 客户端工具（推荐快速上手）
- **安装**：多数工具提供一键脚本（如 `curl ... \| bash`）或包管理器安装（`npm install -g xxx` / `pip install xxx`），Windows 用户需注意 WSL2 或 Git Bash 依赖（见 [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md) 和 [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)）。
- **配置**：统一通过配置文件（如 `~/.hermes/config.yaml`、`~/.claude/settings.json`）或 GUI 设置界面（如 Cursor、Cherry Studio、Qoder）完成，核心是填入上述关键参数。
- **验证**：运行 `xxx --version` 检查安装，发起简单对话（如“你好”）确认响应即成功。

### 通用开发工具（适合调试与集成）
- **Postman/cURL**：适用于图像/视频等异步 AIGC API 测试，必须遵循两步流程：1) POST 创建任务获取 `task_id`；2) GET 轮询查询结果。北京地域默认使用 `dashscope.aliyuncs.com` 域名，国际地域需替换 `{WorkspaceId}`（见 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)）。
- **Dify**：需安装“通义千问”插件，配置时区分国内/国际端点，并启用思考模式（`enable_thinking: true`）以支持 Qwen3 系列模型（见 [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)）。
- **IDE 插件（Cline、Qwen Code 等）**：安装后在设置中选择 “OpenAI Compatible”，填入 Base URL 和 API Key；若使用 Qwen3 思考模式或 QwQ，需额外勾选 “Enable R1 messages format”（见文档 15）。

## 限制和注意事项

- **凭证隔离**：Token Plan 个人版、Token Plan 团队版、Coding Plan、按量计费的 API Key **完全不互通**。混用（如用 Token Plan Key 配置按量计费 URL）必然导致 401 错误（见文档 10、15、16）。
- **地域绑定（按量计费）**：API Key 与 Workspace ID 必须同地域（如北京 Key 配北京 Workspace ID），跨地域调用会产生费用或失败（见文档 11）。
- **模型能力限制**：
  - Token Plan/Coding Plan 仅支持文本生成，禁用多模态、AIGC、Embedding 等高级能力；
  - 千问 APP 工作助理仅支持 Token Plan，且手机端需 ≥ v7.1.2（见文档 7）；
  - Cursor 免费版仅支持 `auto` 模型，调用指定模型需升级至 Pro（见文档 5）。
- **安全与合规**：工作流平台（Dify、n8n、Coze）及 API 测试工具（Postman、Insomnia）**严禁使用 Token Plan/Coding Plan Key**，违规将导致订阅暂停或 Key 封禁（见文档 17 和文档 19）。
- **免费额度**：新人免费额度仅适用于华北2（北京）地域的按量计费模型，且各模型额度独立计算（见文档 11）。

## 来源文档

- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [千问](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)
- [DeepSeek Harness](../../raw/model-user-guide/use-chat-client-or-development-tool/deepseek-harness.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)


