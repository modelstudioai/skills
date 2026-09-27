# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程客户端、IDE 插件及开发工具接入模型服务，覆盖终端 CLI、桌面应用、Web IDE 和工作流平台等场景。开发者可根据使用习惯和项目需求，选择适配 OpenAI 或 Anthropic 兼容协议的工具，并按计费方案（[Token](../concepts/token.md) Plan 个人版/团队版、Coding Plan、按量计费）配置对应凭证与端点。所有工具均依赖标准 API 协议，无需修改业务逻辑即可切换模型。

## 支持的模型/功能

百炼支持的模型能力因接入方案而异：

- **[Token](../concepts/token.md) Plan 个人版与团队版**：仅限接入 AI 编程工具（如 OpenClaw、Claude Code、Qwen Code）和 Agent 类应用（如 QwenPaw、DeepSeek Harness），**不支持工作流平台（如 Dify）或通用 HTTP 工具（如 Postman）**。支持的模型以文本生成为主，包括 `qwen3.8-max`、`qwen3.8-flash`、`qwen3.7-plus`、`glm-5.3`、`deepseek-v4-pro` 等，部分模型支持图像输入（如 `qwen3.8-flash`）和思考模式（需显式启用 `enable_thinking`）。详见 [Token Plan 个人版支持的模型](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)。

- **Coding Plan**：面向开发者订阅，支持 `qwen3.7-plus` 等固定模型，仅限编程类工具调用，不支持视觉或多模态模型。

- **按量计费**：适用范围最广，支持所有兼容协议的工具（含 Dify、Postman、cURL），并开放全部模型能力，包括文生图（`wan2.6-t2i`）、文生视频、Qwen-VL、QVQ、Qwen-Omni 等。图像/视频类 API 采用异步机制（创建任务 + 轮询查询），详见 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

> **注意**：文档 16（Dify）明确指出，Dify **不支持** [Token](../concepts/token.md) Plan 个人版、Token Plan 团队版和 Coding Plan；若误用此类 API Key 将被视为违规，可能导致订阅暂停或 Key 封禁。该限制在 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) 中再次强调，属强制性策略，非配置错误。

## 关键参数

所有工具共用以下核心参数，但协议与路径存在差异：

| 参数 | OpenAI 兼容协议 | Anthropic 兼容协议 | 说明 |
|------|----------------|---------------------|------|
| **Base URL** | `https://{WorkspaceId}.<region>.maas.aliyuncs.com/compatible-mode/v1`（按量）<br>`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（Token Plan）<br>`https://coding.dashscope.aliyuncs.com/v1`（Coding Plan） | `https://{WorkspaceId}.<region>.maas.aliyuncs.com/apps/anthropic`（按量）<br>`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`（Token Plan）<br>`https://coding.dashscope.aliyuncs.com/apps/anthropic`（Coding Plan） | Token Plan/Coding Plan 的 Base URL 不含 `{WorkspaceId}`；按量计费必须替换为真实 Workspace ID。地域需与 API Key 一致。 |
| **API Key** | 各方案专属 Key，**不通用**。Token Plan 个人版 Key 仅可用于 Token Plan 个人版端点，Coding Plan Key 仅可用于 Coding Plan 端点。 | 同上，且 Anthropic 协议下环境变量名常为 `ANTHROPIC_AUTH_TOKEN`（如 [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md) 所示）。 | 复制时需确保无空格、换行；401 错误多因 Key 与 Base URL 方案/地域不匹配。 |
| **Model ID** | `qwen3.8-max`、`qwen3.7-plus` 等；部分工具（如 Cursor）要求模型名中 `.` 替换为 `-`（`glm-5.3` → `glm-5-3`）。 | 同上，但 Anthropic 协议下部分工具（如 Claude Code）通过 `ANTHROPIC_DEFAULT_SONNET_MODEL` 等环境变量映射模型别名。 | 模型必须在所选套餐的支持列表内，否则返回 400 错误。 |

## 使用方式

### 1. 安装与初始化
- **CLI 工具**（如 `qwen`、`claude`、`opencode`）：统一要求 Node.js ≥18.0（OpenClaw 需 ≥22.19.0），通过 `npm install -g <pkg>` 安装。
- **桌面应用**（如 Cursor、Cherry Studio、Qoder）：从官网下载安装包，启动后进入设置界面配置。
- **IDE 插件**（如 Cline、Qoder JetBrains 插件）：在 VS Code 或 JetBrains 扩展市场搜索安装，配置入口通常在侧边栏或右上角设置按钮。
- **Agent 平台**（如 QwenPaw、OpenClaw）：支持一键脚本（`curl ... \| bash`）或 pip 安装，首次运行自动触发向导。

### 2. 配置凭证（四类方案）
- **Token Plan 个人版/团队版**：使用专属 API Key + `compatible-mode/v1`（OpenAI）或 `/apps/anthropic`（Anthropic）端点；模型列表见对应套餐文档。
- **Coding Plan**：使用 Coding Plan API Key + `coding.dashscope.aliyuncs.com/v1`（OpenAI）或 `/apps/anthropic`（Anthropic）；仅支持 `qwen3.7-plus` 等指定模型。
- **按量计费**：使用百炼 API Key + `{WorkspaceId}.<region>.maas.aliyuncs.com/compatible-mode/v1`（OpenAI）或 `/apps/anthropic`（Anthropic）；支持全量模型，含 AIGC 能力。
- **Dify 等工作流平台**：**仅允许按量计费**，且必须使用 `compatible-mode/v1` 端点；需通过插件（如“通义千问”）或 OpenAI-API-compatible 插件配置，不可直接填入 Token Plan Key。

### 3. 高级功能启用
- **思考模式（Reasoning）**：Qwen3 系列模型需在请求体中显式设置 `"enable_thinking": true`（如 Qwen Code、Kilo CLI 配置）或通过环境变量（如 `CLAUDE_CODE_SUBAGENT_MODEL`）触发。
- **多模态输入**：`qwen3.8-flash`、`qwen3.8-max` 支持图像输入，需在工具配置中启用对应模态（如 OpenCode 的 `input: ["text", "image"]`）。
- **AIGC 异步调用**：图像/视频生成必须分两步：先 POST 创建任务获取 `task_id`，再 GET 轮询结果；该流程在 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md) 中有完整示例。

## 限制和注意事项

- **方案隔离性**：Token Plan 个人版、Token Plan 团队版、Coding Plan 的 API Key **完全不通用**，且仅限指定工具类型（编程 CLI/IDE/Agent）。跨方案使用（如用 Token Plan Key 配置 Dify）将导致 401 或服务封禁。
- **地域强绑定**：按量计费的 API Key 与 Base URL 必须同地域（如北京 Key 配北京端点），否则认证失败；Token Plan/Coding Plan 的端点固定为北京，无地域选项。
- **模型命名兼容性**：Cursor、Chatbox 等工具要求模型 ID 中的 `.` 替换为 `-`（如 `glm-5.3` → `glm-5-3`），否则报错 `model does not work`；Qoder CN 则严格校验提供商与类型匹配，选错即报 `Unknown Custom model Exception`。
- **免费额度限制**：按量计费的新手免费额度**仅适用于华北2（北京）地域的模型**，且各模型额度独立计算；使用新加坡/美国端点或跨模型调用均不享受免费额度。
- **视觉模型支持**：Qwen-VL、QVQ、Qwen-Omni 等模型**无法在 Dify 插件中直接配置**，必须通过 Chatflow 的 HTTP 节点以 cURL 方式调用，且建议启用流式响应降低超时风险（见 [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md) 文档）。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [千问](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [DeepSeek Harness](../../raw/model-user-guide/use-chat-client-or-development-tool/deepseek-harness.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)


