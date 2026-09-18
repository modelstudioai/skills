# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端及开发平台接入模型服务，覆盖终端 CLI、IDE 插件、Web 应用和低代码工作流等场景。开发者可根据使用习惯选择适配的客户端，并按计费方案（Token Plan 个人版/团队版、Coding Plan 或按量计费）配置对应凭证与端点。所有工具均基于 OpenAI 或 Anthropic 兼容协议，无需修改业务逻辑即可快速切换。

## 支持的模型/功能

百炼支持的模型能力因接入方案而异：

- **Token Plan（个人版/团队版）**：仅支持文本生成类模型（如 `qwen3.8-max`、`qwen3.7-plus`、`glm-5.3`），不支持图像、视频、语音或多模态推理模型；千问 APP 工作助理 [仅支持 Token Plan](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)，不支持按量计费或 Coding Plan。
- **Coding Plan**：支持 `qwen3.7-plus` 等文本模型，但明确不支持 `qwen3.8-*` 系列（见 [Coding Plan 文档](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)）。
- **按量计费**：功能最全，支持全部文本模型（含思考模式）、视觉模型（Qwen-VL、QVQ）、音频模型（Qwen-Audio）、OCR 模型（Qwen-OCR）及万相文生图/视频模型；Dify 等工作流平台**仅允许使用按量计费 API Key**，[Token Plan 和 Coding Plan 均不支持](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。
- **通用限制**：所有方案均不支持在 Postman/cURL 等 API 测试工具中直接调用 Token Plan/Coding Plan 凭证——这些工具属于[不支持的工具类型](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)，仅可用于按量计费的调试验证。

> **注意**：文档 1 中 OpenClaw 配置示例列出 `qwen3.8-max` 和 `qwen3.8-flash` 的 `contextWindow: 983616`，但文档 4（OpenCode）和文档 16（Kilo CLI）对同模型标注 `limit.context: 983616`，而文档 6（Codex）在 `model-catalog.local.json` 中写为 `"context_window": 983616` —— 数值一致，命名差异属各工具配置规范不同，非矛盾。但文档 1 中 `glm-5.3` 条目被截断（末尾为 `"contextWindo`），应以完整文档 [token-plan-personal-overview.md](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md) 为准。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| **API Key** | 方案专属密钥，不可跨方案复用 | Token Plan 个人版：控制台 [subscription/overview](https://bailian.console.aliyun.com/cn-beijing/subscription/overview) 获取 |
| **Base URL** | 必须与 API Key 方案及地域严格匹配 | Token Plan 个人版 OpenAI 协议：<br>`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>按量计费（北京）Anthropic 协议：<br>`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| **Model ID** | 模型标识符，注意命名规范差异 | `qwen3.8-flash`（标准） vs `glm-5-3`（Cursor 要求连字符） vs `kimi-k2-6`（Cursor） |
| **Protocol** | OpenAI 兼容（`/compatible-mode/v1`）或 Anthropic 兼容（`/apps/anthropic`） | 多数工具默认推荐 OpenAI 协议；Hermes Agent 明确支持双协议切换 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md) |

## 使用方式

### 1. 客户端安装
- **CLI 工具**（如 Qwen Code、Hermes Agent、Claude Code）：依赖 Node.js ≥18（部分要求 ≥22.19.0），通过 `npm install -g` 或一键脚本安装。
- **桌面应用**（如 Cursor、Cherry Studio、Qoder）：从官网下载安装包，无需本地环境配置。
- **IDE 插件**（如 Cline、Qoder JetBrains 插件）：在 VS Code 或 JetBrains 扩展市场搜索安装。
- **Web 平台**（如 Dify、QwenPaw）：部署后通过浏览器访问，QwenPaw 可本地运行 `qwenpaw app` 启动。

### 2. 凭证配置
所有工具均需配置三项核心参数：
- **API Key**：从对应方案控制台获取（如 Token Plan 个人版 → [subscription/overview](https://bailian.console.aliyun.com/cn-beijing/subscription/overview)）；
- **Base URL**：严格按方案+地域选择（见上表），`{WorkspaceId}` 需替换为真实 ID（[获取方法](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)）；
- **Model ID**：填入该方案支持的模型名，注意大小写与连字符（如 Cursor 要求 `glm-5-3` 而非 `glm-5.3`）。

> **注意**：文档 13（Cline）和文档 14（Qoder）均强调，若使用 Qwen3 思考模式或 QwQ 模型，必须在设置中启用 **Enable R1 messages format**，否则报错 `400 InternalError.Algo.InvalidParameter`；此为关键兼容性开关，非可选配置。

### 3. 验证与调试
- 发送简单请求（如 `"你好"`）确认基础连通性；
- 对于长上下文或工具调用失败，检查 `max_tokens` 等生成参数（见 [QwenPaw FAQ](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)）；
- 图像/视频生成等异步任务需分两步：先 `POST /image-synthesis` 创建任务获 `task_id`，再 `GET /tasks/{task_id}` 轮询结果（[Postman/cURL 文档](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md) 提供完整流程）。

## 限制和注意事项

- **方案隔离**：Token Plan 个人版、团队版、Coding Plan 的 API Key **完全不通用**；混用将导致 `401 Incorrect API key provided`（见文档 10、13、15）。按量计费 Key 亦不可用于 Token Plan 端点。
- **地域绑定**：按量计费的 API Key 与 Workspace ID 必须同地域（如北京 Key 配北京 Workspace ID），否则认证失败或产生意外费用（[Cherry Studio FAQ](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md) 明确指出免费额度仅限华北2）。
- **模型可用性**：同一模型在不同方案中支持状态不同。例如 `qwen3.8-flash` 在 Token Plan 个人版中可用，但在 Coding Plan 中未列出（见 [Coding Plan 支持模型列表](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)）。
- **工具类型限制**：Token Plan/Coding Plan **禁止用于工作流平台（Dify、n8n）、API 测试工具（Postman）、自定义后端服务**；违规使用可能导致订阅暂停（[more-tools.md](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) 明确声明）。
- **客户端特异性**：
  - Cursor 免费版仅支持 Auto 模式，调用自定义模型需升级至 Pro 版（[Cursor FAQ](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)）；
  - 千问 APP 工作助理仅支持 Token Plan，且手机端需 ≥7.1.2 版本（[qwen-office-assistant.md](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)）；
  - Dify 必须使用按量计费 Key，且推荐通过 OpenAI 兼容插件而非 Anthropic 协议接入（[dify.md](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)）。

---

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
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)


