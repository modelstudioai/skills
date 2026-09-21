# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端及开发平台接入模型服务，覆盖终端 CLI、IDE 插件、Web 应用和工作流系统等场景。开发者可根据使用习惯选择适配的客户端，并按计费方案（Token Plan 个人版/团队版、Coding Plan 或按量计费）配置对应 API Key 与 Base URL。所有工具均基于 OpenAI 或 Anthropic 兼容协议，无需修改业务逻辑即可快速切换后端模型。

## 支持的模型/功能

百炼支持的模型能力取决于所选计费方案与协议类型：

- **Token Plan（个人版/团队版）**：仅支持文本生成类模型（如 `qwen3.8-max`、`qwen3.7-plus`、`glm-5.3`），不支持图像、视频、语音或多模态推理类模型（如 Qwen-VL、Qwen-Omni、万相）。该限制在 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) 文档中明确说明。
- **Coding Plan**：支持文本生成模型（如 `qwen3.7-plus`），但不支持思考模式（reasoning）或 `auto` 模型；部分文档示例中配置了 `qwen3.7-plus`，而另一些则未明确禁用思考参数，需以实际控制台支持列表为准。
- **按量计费**：支持全部公开模型，包括文生图（`wan2.6-t2i`）、文生视频、Qwen-VL、QVQ、Qwen-Omni 等，且可通过 HTTP 直接调用（如 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md) 所述）。
- **Dify 等工作流平台**：**仅允许使用按量计费 API Key**；Token Plan 和 Coding Plan 套餐明确禁止用于 Dify、n8n、Coze 等自动化平台，违规将导致订阅暂停或 Key 封禁 —— 此规则详见 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。

> **注意**：文档 1（OpenClaw）中列出的 `qwen3.8-flash` 模型配置含 `"reasoning": true`，但文档 5（千问 APP）明确指出其仅支持 Token Plan，且未提及思考模式；而文档 17（更多工具）强调 Token Plan “仅支持文本生成类”模型，未包含 reasoning 能力。此处存在隐含矛盾：`reasoning: true` 字段可能为兼容性占位，实际调用时需显式启用 `enable_thinking`（如文档 6、11 所示），否则将报错。建议以运行时行为为准，首次调用前务必验证思考模式开关。

## 关键参数

所有客户端共用以下核心参数，但协议与路径存在差异：

| 参数 | OpenAI 兼容协议 | Anthropic 兼容协议 | 说明 |
|------|----------------|---------------------|------|
| **Base URL** | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（Token Plan）<br>`https://coding.dashscope.aliyuncs.com/v1`（Coding Plan）<br>`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（按量） | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`（Token Plan）<br>`https://coding.dashscope.aliyuncs.com/apps/anthropic`（Coding Plan）<br>`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic`（按量） | 必须与 API Key 方案及地域严格匹配；`{WorkspaceId}` 需替换为真实值（见 [获取Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)） |
| **API Key** | 各方案专属 Key（见各文档控制台链接） | 同左 | Token Plan 个人版 Key 仅可用于个人版 URL，不可混用团队版或 Coding Plan；按量 Key 必须与 Base URL 地域一致 |
| **Model ID** | `qwen3.8-max`、`qwen3.7-plus` 等（注意命名规范：`kimi-k2.6` → `kimi-k2-6`，见文档 3） | `qwen3.8-max`、`auto` 等（部分工具如 Claude Code 会映射 `ANTHROPIC_DEFAULT_OPUS_MODEL`） | 模型名大小写敏感；`auto` 仅在 Token Plan 和 Anthropic 协议下有效；Coding Plan 不支持 `auto` |

> **注意**：文档 4（Codex）中 `model_providers.Model_Studio_Token_Plan_Personal` 的 `wire_api: "responses"` 配置，与文档 2（Hermes Agent）和文档 17 中主流使用的 `openai-completions` 或 `anthropic-messages` 不一致，属历史兼容接口，新项目应避免使用。

## 使用方式

### 1. 客户端安装
- **CLI 工具**（如 Hermes Agent、Qwen Code、Kilo CLI）：依赖 Node.js ≥18（文档 2、6、14），部分需 WSL（Windows）（文档 2、8）。
- **IDE 插件**（如 Cline、Qoder JetBrains）：直接从 VS Code 或 JetBrains 商店安装（文档 11、12）。
- **桌面应用**（如 Cursor、Cherry Studio）：从官网下载安装包（文档 3、9）。
- **Web 平台**（如 Dify）：无需本地安装，通过 [cloud.dify.ai](https://cloud.dify.ai) 访问（文档 16）。

### 2. 凭证配置
- **环境变量方式**：如 Codex 要求 `OPENAI_API_KEY`（文档 4），Claude Code 使用 `ANTHROPIC_AUTH_TOKEN`（文档 8）。
- **配置文件方式**：OpenClaw 写入 `~/.openclaw/openclaw.json`（文档 1），Hermes Agent 使用 `~/.hermes/config.yaml`（文档 2）。
- **GUI 配置**：Cursor、Chatbox、Qoder IDE 等提供可视化设置界面（文档 3、10、12）。
- **交互式命令**：Qwen Code 支持 `/auth` 命令启动向导（文档 6），Qoder CLI 支持 `/model` TUI 配置（文档 12）。

### 3. 高级能力启用
- **思考模式（Reasoning）**：Qwen3 系列模型需显式开启（如文档 6、11 中 `enable_thinking: true` 或勾选 **Enable R1 messages format**）；未启用将返回 400 错误（文档 11）。
- **多模态输入**：`qwen3.8-max` 等支持 `image` 输入，但需客户端配置（如文档 1 中 `input: ["text", "image"]`），且仅按量计费支持完整视觉链路（文档 16）。
- **百炼 CLI 集成**：Cursor、Cline、Qoder 等支持通过自然语言调用 CLI 技能（如生成图片/视频），需提前全局安装 `bailian-cli`（文档 3、11、12）。

## 限制和注意事项

- **方案隔离性**：Token Plan 个人版、团队版、Coding Plan 的 API Key 与 Base URL **完全不通用**；混用将导致 401 错误（文档 11、13）。Dify 等平台**严禁使用套餐 Key**，仅接受按量 Key（文档 16）。
- **地域绑定**：按量计费的免费额度**仅限华北2（北京）地域**；使用新加坡或美国地域将立即计费（文档 9）。
- **模型可用性差异**：
  - 千问 APP 仅支持 Token Plan，不支持按量/Coding Plan（文档 5）；
  - Dify 不支持 Token Plan/Coding Plan，且 Qwen-Omni/Qwen-Audio 等需通过 HTTP 节点手动接入（文档 16）；
  - Postman/cURL 仅用于测试，**禁止生产环境使用**（文档 15）。
- **常见错误处理**：
  - `401 Incorrect API key provided`：检查 Key 与 URL 是否同方案同地域（文档 11、13、19）；
  - `The value of the enable_thinking parameter is restricted to True`：必须开启思考模式（文档 9）；
  - `Named models unavailable Free plans can only use Auto`：Cursor 免费版仅支持 `auto`（文档 3）。

> **注意**：文档 1（OpenClaw）末尾配置片段被截断（`"c`），且其 `qwen3.6-flash` 条目缺少完整 JSON 结构；实际配置时请以文档 6（Qwen Code）或文档 17（更多工具）中完整模型列表为准，避免语法错误导致启动失败。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [千问](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [DeepSeek Harness](../../raw/model-user-guide/use-chat-client-or-development-tool/deepseek-harness.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)


