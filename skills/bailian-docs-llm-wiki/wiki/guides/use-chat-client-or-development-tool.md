# use chat client or development tool

阿里云百炼支持通过多种第三方 Chat 客户端与开发工具接入模型服务，覆盖终端 CLI、IDE 插件、桌面应用及低代码平台等场景。开发者可根据使用习惯选择合适工具，并按计费方案（[Token](../concepts/token.md) Plan 个人版/团队版、Coding Plan 或按量计费）配置对应 API Key 与 Base URL。所有工具均基于 OpenAI 或 Anthropic 兼容协议，无需修改业务逻辑即可快速集成。

## 支持的模型/功能

百炼支持的模型能力因接入方案而异：

- **[Token](../concepts/token.md) Plan 个人版与团队版**：仅支持文本生成类模型（如 `qwen3.8-max`、`qwen3.7-plus`、`glm-5.3`、`deepseek-v4-pro`），不支持多模态（图像/音频/OCR）或万相类生成模型。详见 [Token Plan 个人版支持的模型](raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md) 和 [Token Plan 团队版支持的模型](raw/model-user-guide/token-plan-guide/token-plan-overview.md)。
- **Coding Plan**：支持文本生成模型（如 `qwen3.7-plus`），但明确不支持思考模式（`enable_thinking`）、多模态输入或 R1 消息格式；部分工具（如 Cline）需额外启用 `Enable R1 messages format` 才能调用 Qwen3 系列模型 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)。
- **按量计费**：功能最全，支持全部文本模型、Qwen-VL/QVQ 视觉模型、Qwen-Omni/Qwen-Audio/Qwen-OCR 等多模态模型，以及万相（Wan2.6-t2i）文生图/视频 API。Dify 等工作流平台**仅允许使用按量计费 API Key**，严禁混用 [Token](../concepts/token.md) Plan 或 Coding Plan 凭证 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。

> **注意**：文档 7（千问 APP）明确指出“仅支持 Token Plan（个人版和团队版），不支持按量计费或 Coding Plan”，而文档 17（Dify）则强调“**不支持**使用 Token Plan 个人版、Token Plan 团队版和 Coding Plan 接入”。二者适用范围互斥，开发者须严格按工具类型匹配计费方案，否则将触发 401 或 403 错误。

## 关键参数

所有工具均依赖以下核心参数完成接入：

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `API Key` | 方案专属凭证，不可跨方案复用 | `sk-xxx`（按量）、`tp-xxx`（Token Plan）、`cp-xxx`（Coding Plan） |
| `Base URL` | 必须与 API Key 方案及地域严格匹配 | OpenAI 协议：<br>`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>Anthropic 协议：<br>`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| `Model ID` | 模型标识符，注意命名规范差异 | `qwen3.8-max`（标准）、`glm-5-3`（Cursor 要求连字符）、`auto`（自动选型） |
| `API Protocol` | 决定请求格式与兼容性 | `openai-completions`（DeepSeek Harness）、`anthropic-messages`（Hermes Agent） |

> **注意**：文档 5（Cursor）和文档 11（Chatbox）均要求将 `glm-5.3` 写为 `glm-5-3`，而文档 4（OpenCode）和文档 14（Kilo CLI）配置中直接使用 `glm-5.3`。该差异源于客户端解析逻辑不同，非模型本身变更，开发者需按所用工具文档调整模型名。

## 使用方式

### 1. 工具安装
- **CLI 类工具**（如 Hermes Agent、Qwen Code、Claude Code）：依赖 Node.js ≥18（部分要求 ≥22），通过 `npm install -g` 或一键脚本安装。
- **IDE 插件**（如 Cline、Qoder JetBrains 插件）：在 VS Code 或 JetBrains 市场搜索安装。
- **桌面应用**（如 Cursor、Cherry Studio、Qoder IDE）：从官网下载安装包。
- **Web/低代码平台**（如 Dify、QwenPaw）：通过浏览器访问或本地部署。

### 2. 凭证配置
通用流程为：
- 获取对应方案的 [API Key](raw/model-api-reference/preparations/get-api-key.md)；
- 根据方案与地域构造 `Base URL`（务必替换 `{WorkspaceId}`）；
- 在工具设置界面或配置文件中填入 `API Key`、`Base URL`、`Model ID`；
- 验证连接（如发送“你好”测试响应）。

典型配置路径示例：
- OpenClaw：`~/.openclaw/openclaw.json`
- Hermes Agent：`~/.hermes/config.yaml`
- Claude Code：`~/.claude/settings.json`
- QwenPaw：Web Console → 设置 → 模型 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)

### 3. 高级能力启用
- **思考模式（Reasoning）**：Qwen3 系列模型需显式开启 `enable_thinking`（CLI 工具常通过 `generationConfig.extra_body.enable_thinking: true` 或环境变量控制）。
- **多模态支持**：仅按量计费支持图像/视频 API，调用需遵循异步机制（创建任务 + 轮询查询）[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。
- **自定义技能（Skills）**：Qwen Code、Cline、Qoder 等支持通过百炼 CLI 注册技能，扩展图像生成、视频合成等能力。

## 限制和注意事项

- **方案隔离**：Token Plan 个人版、团队版、Coding Plan 的 API Key 与 Base URL **完全不互通**。混用将导致 401 错误（如文档 10、13、16 均强调此点）。
- **地域绑定**：按量计费的 API Key 与 `WorkspaceId` 必须同地域（如北京 Key 只能配北京 URL），否则产生费用或调用失败（文档 12 明确提示“免费额度仅适用于华北2（北京）地域”）。
- **工具类型限制**：Token Plan/Coding Plan **禁止用于工作流平台**（Dify、n8n、Coze）和 API 测试工具（Postman、cURL），仅限 AI 编程工具与 Agent 类应用 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。
- **模型兼容性**：部分工具（如 Cursor 免费版）仅支持 `auto` 模型，调用具体模型需升级至 Pro 版本；Qoder CN 企业版不支持百炼接入。
- **上下文与 Token 限制**：长对话易触发 `context window exceeded`，建议在提供商设置中显式配置 `max_tokens`（文档 10 提供 JSON 示例）。
- **错误排查**：统一参考各方案 FAQ 文档，如按量计费查 [错误码](raw/model-api-reference/preparations/error-code.md)，Coding Plan 查 [常见问题](raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)。

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
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)


