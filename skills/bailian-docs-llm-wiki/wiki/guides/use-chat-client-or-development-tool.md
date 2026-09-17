# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端及开发平台接入模型服务，覆盖终端 CLI、IDE 插件、Web UI 和工作流系统等场景。开发者可根据使用习惯选择 OpenClaw、Qwen Code 等 Agent 工具，或 Cursor、Cline 等 IDE 集成环境；也可在 Dify 等低代码平台中构建应用。所有工具均通过标准 API 协议（OpenAI 兼容或 Anthropic 兼容）对接，配置统一、迁移成本低。

## 支持的模型/功能

百炼模型可通过四类计费方案接入：**按量计费**、**Coding Plan**、**[Token](../concepts/token.md) Plan 个人版**和**[Token](../concepts/token.md) Plan 团队版**。各方案支持的模型范围不同，且存在明确的使用边界：

- **[Token](../concepts/token.md) Plan 个人版与团队版**：仅支持文本生成类模型（如 `qwen3.8-max`、`qwen3.7-plus`、`glm-5.3`），不支持图像、视频、语音或多模态模型（如 Qwen-VL、Qwen-Omni、万相）。该限制在 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) 文档中有明确定义。
- **Coding Plan**：支持 `qwen3.7-plus`、`qwen3.6-flash` 等主力编码模型，但不支持 `qwen3.8-*` 系列及 DeepSeek V4 全系模型。
- **按量计费**：支持最全模型集，包括文生图（`wan2.6-t2i`）、文生视频（`wan2.1-v2v`）、多模态（`qwen-vl`、`qwen-omni`）、思考增强（`qwen3.8-flash` 启用 `enable_thinking`）等，详见 [OpenAI 兼容 - 支持的模型](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md) 和 [Anthropic 兼容 API](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。

> **注意**：文档 6（千问）明确指出“千问工作助理仅支持 Token Plan（个人版和团队版），不支持按量计费或 Coding Plan”，而文档 17（Dify）则强调“Dify **不支持**使用 Token Plan 个人版、Token Plan 团队版和 Coding Plan 接入”，二者政策完全对立。实际接入时必须严格遵循工具类型约束：AI 编程工具（如 Qwen Code、Claude Code）和 OpenClaw 类 Agent 可用 Token Plan/Coding Plan；工作流/自动化平台（如 Dify、n8n）**仅允许按量计费**，否则可能触发封禁。

## 关键参数

所有工具均依赖以下核心参数完成认证与路由：

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `API Key` | 方案专属密钥，**不可跨方案复用**。Token Plan 个人版 Key 不能用于按量计费 Base URL，反之亦然 | `sk-xxxxxxxxxxxxx`（按量）、`tp-xxxxxx`（Token Plan） |
| `Base URL` | 决定协议兼容性与模型可用性：<br>- OpenAI 兼容：路径以 `/compatible-mode/v1` 结尾<br>- Anthropic 兼容：路径以 `/apps/anthropic` 结尾 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（OpenAI）<br>`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`（Anthropic） |
| `Model ID` | 必须与所选方案支持的模型列表一致。部分工具（如 Cursor、Chatbox）要求模型名中 `.` 替换为 `-`（`glm-5.3` → `glm-5-3`） | `qwen3.8-flash`, `qwen3.7-plus` |
| `WorkspaceId` | 仅按量计费必需，需从[控制台获取](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)，并替换 Base URL 中的 `{WorkspaceId}` 占位符 | `ws-abc123xyz` |

## 使用方式

### 安装与初始化
- **CLI 工具**（如 Qwen Code、Kilo CLI、Claude Code）：依赖 Node.js ≥18，通过 `npm install -g` 安装，验证用 `xxx --version`。
- **桌面客户端**（如 Cursor、Cherry Studio、Chatbox）：直接下载安装包，无需额外运行时。
- **IDE 插件**（如 Cline、Qoder）：在 VS Code 或 JetBrains 扩展市场安装。
- **Web 平台**（如 Dify、QwenPaw）：本地启动服务（`qwenpaw app`）或访问托管地址（`cloud.dify.ai`）。

### 配置流程（通用）
1. 获取对应方案的 API Key（见各文档链接）；
2. 根据工具要求选择协议（OpenAI 或 Anthropic）并填入 Base URL；
3. 在模型配置项中输入合法 Model ID（参考各方案[支持的模型](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)）；
4. 保存后，在对话界面或模型下拉菜单中选择该模型并测试（如发送“你好”）。

> **注意**：文档 13（Cline）和文档 15（Kilo CLI）均指出，若使用 `qwen3.*` 思考模式模型，必须启用 `Enable R1 messages format` 或等效配置（如 `enable_thinking: true`），否则返回 400 错误。该参数非可选，而是强制要求。

### 特殊能力启用
- **思考模式（R1 / Thinking）**：适用于 `qwen3.8-*`、`qwen3.7-*` 等模型，需在请求体中显式设置 `"enable_thinking": true`（OpenAI 兼容）或通过 `effort: xhigh`（Anthropic 兼容）。详见 [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md) 配置示例。
- **多模态输入**：`qwen3.8-flash`、`qwen3.7-plus` 等支持 `image` 输入，但需 Base URL 为 `/compatible-mode/v1` 且客户端支持上传（如 Cursor、Qoder CN）。
- **异步任务**（图像/视频生成）：必须使用专用 AIGC API（非 `/compatible-mode/v1`），并实现两步调用：先 `POST /image-synthesis` 创建任务，再 `GET /tasks/{task_id}` 轮询结果。详细流程见 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

## 限制和注意事项

- **地域绑定**：按量计费的 API Key 与 WorkspaceId 必须同地域（如北京 Key 配北京 WorkspaceId），跨地域调用将失败或产生费用。Token Plan/Coding Plan 的 Base URL 已固定地域，无需指定 WorkspaceId。
- **免费额度限制**：新人免费额度仅限华北2（北京）地域的按量计费模型，且各模型额度独立计算、每小时更新。其他地域或 Token Plan 套餐无免费额度。
- **凭证安全**：避免硬编码 API Key。CLI 工具推荐用环境变量（如 `BAILIAN_API_KEY`），桌面端应使用内置加密存储。
- **错误排查优先级**：
  1. 检查 `API Key` 与 `Base URL` 是否来自同一方案（如 Token Plan Key + Token Plan URL）；
  2. 验证 `Model ID` 是否在该方案支持列表中（如 `qwen3.8-max` 不可用于 Coding Plan）；
  3. 查看对应方案的 FAQ 文档（如 [Token Plan 常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)）。
- **违规风险**：将 Token Plan/Coding Plan Key 用于 Dify、Postman 等禁止场景，或在未授权子账号下调用，将导致订阅暂停或 Key 封禁。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [千问](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [DeepSeek Harness](../../raw/model-user-guide/use-chat-client-or-development-tool/deepseek-harness.md)


