# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端及开发平台接入模型服务。开发者可根据使用场景（如终端编程、IDE 辅助、低代码工作流）选择适配的客户端，并按计费方案（Token Plan 个人版/团队版、Coding Plan、按量计费）配置对应凭证与端点。所有工具均基于 OpenAI 或 Anthropic 兼容协议，无需修改业务逻辑即可快速迁移。

## 支持的模型/功能

百炼模型可通过以下四类客户端接入：

- **终端编程工具**：OpenClaw、Hermes Agent、Claude Code、Codex、Qwen Code、Qoder CLI、Kilo CLI、OpenCode 等，支持命令行交互、代码生成、审查及多模态任务；
- **IDE 插件与桌面应用**：Cline（VS Code）、Qoder IDE / JetBrains 插件、Cursor、Cherry Studio、Chatbox、Dify（仅按量计费）等，提供图形化配置与上下文感知能力；
- **AI 助手与 Agent 框架**：QwenPaw、DeepSeek Harness、千问 APP 工作助理，支持本地部署、多渠道消息集成及技能扩展；
- **图像/视频生成调试工具**：Postman、cURL，适用于 AIGC API 的异步任务创建与结果轮询，详见 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

> **注意**：Token Plan 个人版、Token Plan 团队版和 Coding Plan **不支持**工作流/自动化平台（如 Dify、n8n、Coze）及 API 测试工具（如 Postman、Insomnia），详见 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) 中“不支持的工具类型”章节。违规使用可能导致订阅暂停或 API Key 封禁。

支持的核心模型包括 `qwen3.8-max`、`qwen3.8-flash`、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.3`、`deepseek-v4-pro` 等文本生成模型；视觉模型（如 `qwen-vl`、`qvq`）需在支持视觉输入的客户端（如 Dify Chatflow、Cursor）中启用对应开关；万相（`wan2.6-t2i`）等 AIGC 模型需通过 HTTP 节点或直接调用 `/api/v1/services/aigc/...` 接口使用。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `Base URL` | 必填，决定协议兼容性与计费归属 | OpenAI 协议：<br>`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>Anthropic 协议：<br>`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| `API Key` | 必填，严格绑定计费方案与地域 | Token Plan 个人版 Key 仅可用于 Token Plan Base URL；按量计费 Key 需与 `WorkspaceId` 所在地域一致 |
| `Model ID` | 必填，区分大小写，部分工具要求格式转换（如 `kimi-k2.6` → `kimi-k2-6`） | `qwen3.8-max`、`auto`、`glm-5-3` |
| `API Protocol` | 隐式决定请求头与 payload 结构 | `openai-completions`（`/v1/chat/completions`）、`anthropic-messages`（`/v1/messages`） |
| `enable_thinking` / `thinking` | 启用 Qwen3/R1 思考模式的必需参数 | 部分工具（如 Cline、Qoder CLI）需在设置界面勾选 **Enable R1 messages format** |

> **注意**：文档 1（OpenClaw）中 `qwen3.8-max` 的 `compat.thinkingFormat: "openai"` 与文档 12（Cline）要求勾选 **Enable R1 messages format** 存在隐含一致性——二者均指向同一思考协议实现，但表述层级不同（配置项 vs UI 开关）。实际调用时必须确保 `thinking` 参数开启且格式匹配，否则返回 `400 InternalError.Algo.InvalidParameter`。

## 使用方式

### 1. 安装与初始化
- 终端工具（如 Hermes Agent、Qwen Code）通常依赖 Node.js ≥18.0 或 Python ≥3.10，安装命令统一为 `npm install -g <pkg>` 或 `curl ... | bash`；
- 桌面应用（如 Cursor、Cherry Studio）需从官网下载安装包；
- Web 平台（如 Dify、QwenPaw Console）启动后访问 `http://127.0.0.1:<port>` 即可。

### 2. 凭证配置（通用流程）
1. **获取 API Key**：根据计费方案访问对应控制台页面（如 [Token Plan 个人版](https://bailian.console.aliyun.com/cn-beijing/subscription/overview)）；
2. **选择 Base URL**：严格匹配方案与协议（OpenAI vs Anthropic），地域需与 Key 一致；
3. **填写 Model ID**：参考各方案[支持的模型](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)列表，注意命名规范（如 `glm-5.3` → `glm-5-3`）；
4. **验证连接**：发送测试请求（如 `"你好"`），确认返回非空响应。

### 3. 高级能力启用
- **思考模式（R1）**：Qwen3 系列模型需显式开启，CLI 工具通过 `--thinking` 参数或配置文件 `thinking.type: enabled`；GUI 工具（如 Cline、Qoder）需在设置中启用开关；
- **多模态输入**：`qwen3.8-flash` 等支持 image 输入的模型，需在客户端配置 `input: ["text", "image"]` 并上传图片；
- **百炼 CLI 集成**：Cursor、Cline、Qoder 等支持通过自然语言触发 CLI 技能（如 `帮我生成 6 张亚马逊主图`），需提前全局安装 `bailian-cli` 并配置 API Key。

## 限制和注意事项

- **地域强绑定**：按量计费的 `WorkspaceId` 必须与 API Key 所属地域完全一致（如北京 Key 不可用于新加坡 URL），否则返回 `401 Unauthorized`；
- **免费额度限制**：新人免费额度仅限华北2（北京）地域的指定模型，其他地域或模型调用将立即计费，详见 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)；
- **模型兼容性约束**：
  - 千问 APP 工作助理**仅支持 Token Plan**（个人版/团队版），不支持按量计费或 Coding Plan；
  - Cursor 免费版**仅支持 `auto` 模型**，调用自定义模型需升级至 Pro 版本；
  - Dify **禁止使用 Token Plan/Coding Plan Key**，仅允许按量计费 Key，违者将触发风控封禁；
- **配置文件安全**：敏感信息（如 API Key）不应硬编码于 Git 仓库，推荐使用环境变量（如 `BAILIAN_API_KEY`）或加密配置管理；
- **错误排查优先级**：遇到 `401` 错误，首先检查 Key 与 URL 方案是否匹配；`400` 错误优先确认 `thinking` 参数与 R1 开关状态；`5xx` 错误建议查阅对应方案的 [常见问题文档](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
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
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)


