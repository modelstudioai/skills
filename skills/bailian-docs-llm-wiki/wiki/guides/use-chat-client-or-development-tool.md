# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端及开发平台接入模型服务，覆盖终端 CLI、IDE 插件、Web 应用和低代码平台等场景。开发者可根据使用习惯选择适配 OpenAI 或 Anthropic 兼容协议的客户端，并按计费方案（Token Plan 个人版/团队版、Coding Plan、按量计费）配置对应凭证。所有工具均需使用百炼提供的标准化 API 端点与模型 ID，但不同工具对协议、路径和参数格式有特定要求。

## 支持的模型/功能

百炼支持的模型能力取决于所选计费方案与客户端协议兼容性：

- **文本生成模型**：全方案通用，包括 `qwen3.8-max`、`qwen3.8-flash`、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.3` 等（详见 [Token Plan 个人版支持的模型](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)）；
- **多模态模型**（图像/音频/OCR）：仅限按量计费方案，Token Plan 和 Coding Plan **不支持** `Qwen-VL`、`Qwen-Audio`、`Qwen-OCR`、`Qwen-Omni` 等非文本模型；
- **思考模式（Reasoning）**：`qwen3.8-*` 系列默认启用，部分工具（如 Cline、Kilo CLI）需显式勾选 `Enable R1 messages format` 或配置 `enable_thinking: true`；
- **图像/视频生成**：需通过专用 AIGC API（如 `/services/aigc/text2image/image-synthesis`）调用，**不适用于 Chat Client 类工具**，应使用 Postman/cURL 或 SDK 直接调用 —— 参见 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)；
- **工作流与自动化能力**：Dify 等平台支持构建 Agent、Chatflow 和知识库，但**仅允许使用按量计费 API Key**，Token Plan 和 Coding Plan 套餐明确禁止用于此类平台（[更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) 中已强调）。

> **注意**：文档 5（千问 APP）明确指出“仅支持 Token Plan（个人版和团队版），不支持按量计费或 Coding Plan”，而文档 16（Dify）则强制要求“**必须使用按量付费的 API Key**”，二者在计费方案适用性上存在根本性冲突。实际接入时，请严格遵循各工具官方文档的约束：千问 APP 属于封闭客户端，仅接受 Token Plan；Dify 属于可编程平台，仅接受按量计费。

## 关键参数

所有客户端均需配置以下核心参数，但协议与路径存在关键差异：

| 参数 | OpenAI 兼容协议 | Anthropic 兼容协议 | 说明 |
|------|----------------|---------------------|------|
| **Base URL** | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（Token Plan）<br>`https://coding.dashscope.aliyuncs.com/v1`（Coding Plan）<br>`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（按量） | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`（Token Plan）<br>`https://coding.dashscope.aliyuncs.com/apps/anthropic`（Coding Plan）<br>`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic`（按量） | 协议决定路径后缀：`/compatible-mode/v1`（OpenAI） vs `/apps/anthropic`（Anthropic）；按量计费必须替换 `{WorkspaceId}` |
| **API Key** | 各方案专属 Key，**不可混用**（如 Token Plan 个人版 Key 不能用于 Coding Plan） | 同上，且需与 Base URL 协议一致 | 文档 8（QwenPaw）、文档 9（Cursor）、文档 17（Cline）均强调“401 错误主因是 Key 与 URL 方案/地域不匹配” |
| **Model ID** | `qwen3.8-flash`、`glm-5.3` 等（注意命名规范：Cursor 要求 `glm-5-3` 而非 `glm-5.3`） | 同上，但部分工具（如 Hermes Agent）要求 `api_mode: anthropic_messages` | 模型列表以各方案文档为准，如 [Coding Plan 支持的模型](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md) |
| **思考模式开关** | `extra_body.enable_thinking: true`（Qwen Code）<br>`"enable_thinking": true`（OpenClaw） | `thinking: { "type": "enabled" }`（Kilo CLI、OpenCode） | 非全局默认，需在客户端配置中显式开启 |

## 使用方式

### 1. 客户端安装与初始化
- **CLI 工具**（Hermes Agent、Claude Code、Qwen Code、Kilo CLI）：依赖 Node.js ≥18（文档 2、3、6、18），通过 `npm install -g` 或一键脚本安装；
- **IDE 插件**（Cline、Qoder JetBrains 插件）：直接从 VS Code 或 JetBrains Marketplace 安装；
- **桌面应用**（Cherry Studio、Chatbox、Cursor）：从官网下载安装包；
- **Web 平台**（Dify、QwenPaw）：访问对应网址或本地启动（`qwenpaw app`）。

### 2. 凭证配置流程
- **交互式配置**：Qwen Code（`/auth` 命令）、QwenPaw（Web Console 设置页）、Cursor（Settings > Models）提供可视化向导；
- **文件编辑**：OpenClaw（`~/.openclaw/openclaw.json`）、Hermes Agent（`~/.hermes/config.yaml`）、Codex（`~/.codex/config.toml`）需手动编辑 JSON/YAML/TOML；
- **环境变量**：Codex（`OPENAI_API_KEY`）、Claude Code（`ANTHROPIC_AUTH_TOKEN`）、DeepSeek Harness（`BAILIAN_API_KEY`）需通过 Shell 或系统级设置。

### 3. 协议与模型绑定验证
- 所有工具均需确保 **API Key、Base URL、协议类型三者严格匹配**。例如：
  - 使用 `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` 必须配 OpenAI 协议 + Token Plan 个人版 Key；
  - 使用 `https://coding.dashscope.aliyuncs.com/apps/anthropic` 必须配 Anthropic 协议 + Coding Plan Key；
- 模型调用前建议先执行 `curl -X GET {base_url}/models`（OpenAI）或 `curl -X GET {base_url}/v1/models`（Anthropic）验证连通性与模型列表。

## 限制和注意事项

- **计费方案隔离**：Token Plan 个人版、团队版、Coding Plan 的 API Key **完全不通用**，且与按量计费 Key 互斥。混用将导致 401 错误（文档 8、9、13、17 多次强调）；
- **地域强绑定**：按量计费的 API Key 与 Workspace ID 必须同地域（北京/新加坡/弗吉尼亚），跨地域使用会触发 401 或额度失效（文档 10 明确提示“免费额度仅适用于华北2（北京）地域”）；
- **平台能力限制**：
  - 千问 APP 仅支持 Token Plan，且手机端需 ≥7.1.2 版本（文档 5）；
  - Dify、n8n、Coze 等工作流平台 **禁止使用 Token Plan/Coding Plan Key**，违者可能导致订阅暂停（文档 16、19）；
  - Postman/cURL 仅用于测试，**生产环境必须使用 SDK**（文档 15）；
- **模型兼容性陷阱**：
  - Cursor 免费版仅支持 Auto 模式，无法调用自定义模型（文档 9）；
  - Qoder CN 企业版不支持百炼接入（文档 13）；
  - 部分工具（如 Cursor、Cherry Studio）要求模型 ID 使用短横线分隔（`glm-5-3`），而非点号（`glm-5.3`）；
- **安全配置**：OpenClaw 默认禁用网关鉴权（`auth.mode: none`），仅限单机使用；共享或远程访问必须运行 `openclaw doctor --fix` 启用 token 鉴权（文档 1）。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [千问](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [DeepSeek Harness](../../raw/model-user-guide/use-chat-client-or-development-tool/deepseek-harness.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)


