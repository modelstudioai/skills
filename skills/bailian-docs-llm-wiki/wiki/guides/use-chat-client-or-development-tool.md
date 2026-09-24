# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端及开发平台接入模型服务，覆盖终端 CLI、IDE 插件、Web 应用和低代码工作流等场景。开发者可根据使用习惯选择适配的客户端，并按计费方案（[Token](../concepts/token.md) Plan 个人版/团队版、Coding Plan 或按量计费）配置对应 API Key 与 Base URL。所有工具均基于 OpenAI 或 Anthropic 兼容协议，无需修改业务逻辑即可快速集成。

## 支持的模型/功能

百炼支持的模型能力因接入方式而异：

- **文本生成类模型**（如 `qwen3.8-max`、`qwen3.7-plus`、`glm-5.3`、`deepseek-v4-pro`）在所有客户端中广泛可用，但需注意各套餐的模型覆盖范围不同：[Token](../concepts/token.md) Plan 个人版与团队版仅支持其订阅范围内模型，详见 [Token Plan 个人版支持的模型](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)；Coding Plan 仅支持其专属模型列表，详见 [Coding Plan 支持的模型](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)；按量计费支持最全模型集，包括文生图（`wan2.6-t2i`）、文生视频、多模态（`qwen-vl`、`qvq`）及 Omni 模态模型，详见 [支持的模型](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope#7f9c78ae99pwz)。
- **视觉与多模态能力**（图像理解、OCR、音频理解）需通过 Dify 的 HTTP 节点或 Postman/cURL 直接调用，不支持在 Chatbox、Cursor 等通用客户端中直接启用视觉开关（[使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)）。
- **思考模式（reasoning / enable_thinking）** 是 Qwen3 系列模型的核心特性，但并非所有客户端默认开启：Qwen Code、Cline、Kilo CLI 等明确要求设置 `enable_thinking: true` 或 `effort: xhigh` 才能触发深度推理；而 OpenClaw 在配置中通过 `"reasoning": true` 字段显式声明，详见 [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)。

> **注意**：Dify 明确不支持 [Token](../concepts/token.md) Plan 个人版、Token Plan 团队版和 Coding Plan，仅允许使用按量计费 API Key。将套餐 API Key 用于 Dify 将被视为违规，可能导致订阅暂停或 Key 封禁 —— 此限制在 [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md) 和 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) 两篇文档中一致强调，属强制策略，非过时信息。

## 关键参数

| 参数 | 说明 | 常见取值示例 |
|------|------|-------------|
| `Base URL` | 模型服务端点地址，必须与计费方案及地域严格匹配 | Token Plan 个人版：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；Coding Plan：`https://coding.dashscope.aliyuncs.com/v1`；按量计费（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `API Key` | 认证凭证，四类方案 Key **完全不通用** | Token Plan 个人版 Key 仅可用于 Token Plan 个人版 Base URL；按量计费 Key 必须与 `WorkspaceId` 所属地域一致 |
| `Model ID` | 模型标识符，部分客户端要求格式转换（如 `glm-5.3` → `glm-5-3`） | `auto`, `qwen3.8-flash`, `wan2.6-t2i`（仅按量计费） |
| `API Protocol` | 协议类型决定请求格式与字段语义 | `openai-completions`（`/v1/chat/completions`）、`anthropic-messages`（`/v1/messages`）、`openai-compat`（兼容 OpenAI v1） |

## 使用方式

### 1. 客户端安装与初始化
- CLI 工具（如 `hermes`、`claude`、`qwen`）依赖 Node.js ≥18（部分要求 ≥22），需先验证版本（`node --version`）；
- 桌面应用（如 Cursor、Cherry Studio、Qoder）需从官网下载安装包，首次启动后完成账号登录与初始向导；
- Web 平台（如 Dify、Chatbox）直接访问网页或登录已有账户，无需本地安装。

### 2. 凭证配置路径（典型）
- **OpenClaw**: `~/.openclaw/openclaw.json`（JSON 格式，含 `models.providers.bailian-token-plan` 块）  
- **Hermes Agent**: `~/.hermes/config.yaml`（YAML 格式，`model.base_url` + `model.api_key`）  
- **Qwen Code**: `~/.qwen/settings.json`（JSON，`env.BAILIAN_TOKEN_PLAN_API_KEY` + `modelProviders.openai[].baseUrl`）  
- **Dify**: Web 控制台 → 用户头像 → 设置 → 模型供应商 → 通义千问插件 → API-KEY 设置  

### 3. 协议与端点选择
- **OpenAI 兼容协议**（推荐）：Base URL 以 `/compatible-mode/v1` 结尾，使用标准 `chat/completions` 接口，适用于绝大多数客户端（Cursor、Chatbox、Qoder、Dify）；
- **Anthropic 兼容协议**：Base URL 以 `/apps/anthropic` 结尾，使用 `messages` 接口，主要适配 `claude-code`、`hermes-agent` 等原生 Anthropic 生态工具；
- **专用 API**（如图像生成）：必须使用 `dashscope.aliyuncs.com/api/v1/services/aigc/...` 端点，不兼容 OpenAI/Anthropic 协议，仅限 Postman/cURL 或自定义 SDK 调用。

## 限制和注意事项

- **计费方案适用范围严格隔离**：Token Plan 个人版/团队版、Coding Plan 仅限 AI 编程工具（如 Hermes、Claude Code、Qoder CN）及 OpenClaw 类 Agent 使用；**工作流平台（Dify、n8n）、API 测试工具（Postman）、自定义后端应用均被明确禁止接入**，详见 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。违规使用将触发风控处置。
- **地域绑定强制生效**：按量计费的 `WorkspaceId` 与 API Key 必须同地域（如北京 Workspace 的 Key 不可配新加坡 Base URL），否则返回 401；Token Plan 与 Coding Plan 的 Base URL 为固定域名，无地域切换选项。
- **模型名称格式差异**：Cursor、Cherry Studio 等客户端要求模型 ID 中的点号（`.`）替换为短横线（`-`），例如 `glm-5.3` → `glm-5-3`；而 OpenClaw、Hermes 等保留原格式，配置时需按客户端文档调整。
- **思考模式启用要求**：Qwen3 系列模型（`qwen3.8-*`, `qwen3.7-*`）在 Cline、Qwen Code、Kilo CLI 中需显式设置 `enable_thinking: true` 或 `effort: xhigh`，否则降级为普通响应；未启用时可能报错 `The value of the enable_thinking parameter is restricted to True`（Cherry Studio 常见问题）。
- **免费额度限制**：新人免费额度仅适用于华北2（北京）地域的按量计费模型，且按模型独立计算（`qwen3.8-max` 与 `wan2.6-t2i` 额度不共享），其他地域或套餐不享受此权益。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [千问](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [DeepSeek Harness](../../raw/model-user-guide/use-chat-client-or-development-tool/deepseek-harness.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)


