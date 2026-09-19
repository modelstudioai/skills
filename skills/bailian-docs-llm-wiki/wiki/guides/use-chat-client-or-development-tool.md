# use chat client or development tool

阿里云百炼支持多种主流 AI 编程客户端与开发工具（如 Hermes Agent、Cursor、Qwen Code 等）及通用开发平台（如 Dify、Postman），通过 OpenAI 或 Anthropic 兼容协议接入。开发者可根据使用场景选择工具：终端 CLI 工具适合轻量级编码辅助，IDE 插件（如 Cline、Qoder）深度集成开发流，而工作流平台（如 Dify）适用于构建生产级应用。所有工具均需按计费方案配置对应 API Key 与 Base URL。

## 支持的模型/功能

百炼支持的模型能力因计费方案和接入协议而异：

- **[Token](../concepts/token.md) Plan 个人版/团队版**：仅支持文本生成类模型（如 `qwen3.8-max`、`qwen3.7-plus`、`glm-5.3`、`deepseek-v4-pro`），不支持图像、音频、OCR、[多模态](../concepts/multimodal.md)推理等扩展能力；[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) 明确指出其“仅限在 AI 编程工具和 OpenClaw 类型 Agent 中使用”，且不支持工作流平台。
- **Coding Plan**：支持 `qwen3.7-plus`、`qwen3.6-plus` 等文本模型，但模型列表较 [Token](../concepts/token.md) Plan 更窄；[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md) 显示其默认模型为 `qwen3.7-plus`，未列出 `qwen3.8-*` 系列。
- **按量计费**：覆盖最全模型集，包括文生图（`wan2.6-t2i`）、文生视频、Qwen-VL、QVQ、Qwen-Omni、Qwen-Audio、Qwen-OCR 等；[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md) 以 `wan2.6-t2i` 为例完整演示了图像生成 API 调用流程。
- **功能特性**：思考模式（`enable_thinking`）在 Qwen3 系列中广泛支持（见 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)），但需注意部分工具（如 Cursor 免费版）强制启用 Auto 模式，不支持自定义模型调用。

> **注意**：文档 7（千问 APP）明确说明“仅支持 [Token](../concepts/token.md) Plan（个人版和团队版），不支持按量计费或 Coding Plan”，而文档 17（Dify）则强调“**不支持**使用 Token Plan 个人版、Token Plan 团队版和 Coding Plan 接入”，二者存在明确的适用边界冲突——前者限定于办公 APP 场景，后者限定于工作流平台，不可跨场景混用。

## 关键参数

所有工具均依赖以下核心参数完成认证与路由：

- **API Key**：必须与计费方案严格匹配。Token Plan 个人版、团队版、Coding Plan 的 API Key 互不通用；按量计费 Key 需与 Base URL 所属地域一致。错误示例见 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md) 中报错 `401 Incorrect API key provided` 的归因分析。
- **Base URL**：分 OpenAI 兼容与 Anthropic 兼容两类：
  - OpenAI 兼容路径统一为 `/compatible-mode/v1`（如 `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）；
  - Anthropic 兼容路径统一为 `/apps/anthropic`（如 `https://coding.dashscope.aliyuncs.com/apps/anthropic`）。
- **模型 ID**：需严格匹配套餐支持列表，且注意命名规范：Cursor 要求 `glm-5.3` 写为 `glm-5-3`（见 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)），而其他工具（如 OpenCode、Kilo CLI）直接使用点号格式。
- **地域标识**：按量计费 URL 含 `{WorkspaceId}` 占位符，必须替换为真实 Workspace ID（见 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)）；免费额度仅限华北2（北京）地域生效（见 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)）。

## 使用方式

### 安装与初始化
- CLI 工具（Hermes、Claude Code、Qwen Code、Kilo CLI）普遍依赖 Node.js ≥18 或 Python，Windows 用户需 WSL2 或 Git Bash；
- 桌面客户端（Cursor、Cherry Studio、Qoder CN）直接下载安装包；
- Web/本地服务（Dify、OpenClaw、QwenPaw）通过 npm 或脚本一键部署，启动后访问本地端口（如 `http://127.0.0.1:8088`）。

### 配置流程（通用范式）
1. **获取凭证**：从百炼控制台对应页面获取 API Key（如 [Token Plan 个人版](https://bailian.console.aliyun.com/cn-beijing/subscription/overview)）；
2. **设置 Base URL**：根据计费方案与协议选择 URL（OpenAI/Anthropic），按量计费需补全 `WorkspaceId`；
3. **声明模型**：在配置文件（如 `~/.hermes/config.yaml`）或 UI 设置中填入模型 ID；
4. **验证连接**：发送测试请求（如 `hermes --version` 或对话输入“你好”）。

> **注意**：文档 4（Cursor）与文档 13（Cline）均要求勾选 **Enable R1 messages format** 才能正确调用 Qwen3 思考模式，该参数在多数其他工具中为隐式启用，属特定工具兼容性要求。

## 限制和注意事项

- **计费方案隔离**：Token Plan/Coding Plan 的 API Key 严禁用于 Dify、Postman、自定义脚本等非授权场景（见 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)），违规将导致订阅暂停或 Key 封禁；
- **地域强绑定**：按量计费的 API Key、Base URL、Workspace ID 必须同地域；新加坡/美国地域的模型不享受华北2 的新人免费额度（见 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)）；
- **模型能力约束**：Token Plan 不支持万相、Qwen-VL、Qwen-Omni 等模型（见文档 17），而 Dify 调用此类模型需通过 HTTP 节点 + Curl 命令绕过插件限制；
- **协议差异**：Anthropic 兼容接口（`/apps/anthropic`）要求 `api_mode: anthropic_messages`（见文档 1），[OpenAI 兼容接口](../concepts/openai-compatible-api.md)（`/compatible-mode/v1`）则无需该字段，混配将导致 404；
- **客户端限制**：Cursor 免费版仅支持 Auto 模式，无法手动选择模型（见文档 4）；千问 APP 仅支持 7.1.2+ 版本，旧版无 Token Plan 入口（见文档 7）。

## 来源文档

- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [千问](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [DeepSeek Harness](../../raw/model-user-guide/use-chat-client-or-development-tool/deepseek-harness.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)


