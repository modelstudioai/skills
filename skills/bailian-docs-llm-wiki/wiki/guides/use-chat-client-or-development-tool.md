# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端及开发平台接入模型服务，覆盖终端 CLI、IDE 插件、Web 应用和低代码工作流等场景。开发者可根据技术栈偏好选择 OpenAI 兼容协议或 Anthropic 兼容协议，按需配置 Token Plan（个人版/团队版）、Coding Plan 或按量计费方案。所有工具均需使用对应计费方案专属的 API Key 和 Base URL，跨方案混用将导致 401 错误。

## 支持的模型/功能

百炼支持的模型能力取决于所选计费方案与协议类型：

- **Token Plan（个人版/团队版）**：仅支持文本生成类模型（如 `qwen3.8-max`、`qwen3.7-plus`、`glm-5.3`），不支持多模态（图像/音频/OCR）或万相等 AIGC 模型；[Token Plan 个人版支持的模型](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md) 和 [Token Plan 团队版支持的模型](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 已明确限定范围。
- **Coding Plan**：支持 `qwen3.7-plus` 等指定文本模型，详见 [Coding Plan 支持的模型](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)。
- **按量计费**：支持最全模型集，包括文本（Qwen3 系列）、视觉（Qwen-VL、QVQ）、语音（Qwen-Audio）、OCR（Qwen-OCR）、文生图/视频（万相系列）等；[Anthropic 兼容 API](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md) 和 [OpenAI 兼容支持的模型](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope#7f9c78ae99pwz) 均适用。
- **Dify 等工作流平台**：**仅允许使用按量计费 API Key**，Token Plan 和 Coding Plan 套餐明确禁止接入；该限制在 [Dify 文档](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md) 中被强调为强制策略，违规将导致订阅暂停或 Key 封禁。

> **注意**：文档 5（千问 APP）明确指出“仅支持 Token Plan（个人版和团队版），不支持按量计费或 Coding Plan”，而文档 17（Dify）则严格禁止 Token Plan/Coding Plan 接入。二者适用场景不同（前者为封闭式办公助理，后者为开放平台），但共同印证了百炼对套餐使用边界的强管控策略。

## 关键参数

所有工具配置均围绕以下核心参数展开，必须严格匹配：

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `API Key` | 方案专属凭证，**不可跨方案复用**。Token Plan 个人版 Key 不能用于 Coding Plan，按量计费 Key 必须与 Base URL 所在地域一致。 | `sk-xxx`（按量）、`tp-xxx`（Token Plan）、`cp-xxx`（Coding Plan） |
| `Base URL` | 协议与地域绑定：<br>- **OpenAI 兼容**：`/compatible-mode/v1` 路径<br>- **Anthropic 兼容**：`/apps/anthropic` 路径<br>- 地域需与 API Key 一致（如北京 Key 配北京 URL） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（OpenAI）<br>`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`（Anthropic） |
| `Model ID` | 模型标识符，部分工具要求格式转换（如 `kimi-k2.6` → `kimi-k2-6`）；Qwen3 思考模式模型需显式启用 `enable_thinking` 或 `effort` 参数。 | `qwen3.8-max`, `auto`, `glm-5-3` |
| `API Protocol` | 决定请求格式与鉴权方式：<br>- `openai-completions` / `openai-chat`：标准 OpenAI v1 接口<br>- `anthropic-messages`：Anthropic v1 格式（含 `system` 字段、`max_tokens` 等） | `anthropic-messages`, `openai-completions` |

## 使用方式

### 1. 安装与初始化
- CLI 工具（如 `qwen-code`, `hermes`, `kilo`）：依赖 Node.js ≥18（部分要求 ≥22），通过 `npm install -g` 或一键脚本安装。
- 桌面应用（如 `Cursor`, `Cherry Studio`, `Chatbox`）：从官网下载安装包，启动后进入设置配置。
- IDE 插件（如 `Cline`, `Qoder JetBrains 插件`）：在 VS Code 或 JetBrains 市场安装，重启后在插件设置中配置。
- Web 平台（如 `Dify`, `OpenClaw`）：部署后通过浏览器访问控制台，在模型管理界面添加供应商。

### 2. 配置凭证（通用流程）
1. **获取 API Key**：根据方案访问对应控制台页面（如 [Token Plan 个人版](https://bailian.console.aliyun.com/cn-beijing/subscription/overview)）。
2. **选择协议与 Base URL**：参考 [更多工具文档](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) 的协议对照表。
3. **填写模型 ID**：严格使用方案支持的模型名（如 Token Plan 不支持 `wan2.6-t2i`）。
4. **验证连接**：发送测试请求（如 `"你好"`），确认返回非空响应。

### 3. 高级能力启用
- **思考模式（R1）**：Qwen3 系列模型需在客户端显式开启（如 Cline 的 `Enable R1 messages format`、Qwen Code 的 `enable_thinking: true`）。
- **多模态输入**：仅按量计费支持图像/音频上传；Dify 中需在 LLM 节点开启“视觉”开关并配合 Qwen-VL/QVQ 模型。
- **异步任务**：图像/视频生成必须使用异步流程（创建任务 → 轮询 `task_id`），详见 [Postman/cURL 文档](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

## 限制和注意事项

- **套餐隔离性**：Token Plan 个人版、团队版、Coding Plan 的 API Key **完全不互通**；混用 Base URL 与 Key 将触发 `401 Incorrect API key provided`（见文档 9、13、14）。按量计费 Key 也必须与 Base URL 地域一致（如北京 Key 配北京 WorkspaceId）。
- **功能边界限制**：
  - Token Plan/Coding Plan **禁止用于 Dify、n8n、Coze 等工作流平台**（文档 17、19 明确声明）；
  - 千问 APP 工作助理 **仅限 Token Plan**（文档 5），不支持其他方案；
  - Postman/cURL 等 API 测试工具 **仅限按量计费**，且仅用于调试（文档 18 强调“不适用于生产环境”）。
- **模型兼容性陷阱**：
  - Cursor 免费版仅支持 `auto` 模型，调用具体模型需升级至 Pro（文档 4）；
  - Codex 需通过 `model-catalog.local.json` 显式声明模型元数据（文档 7），否则 `auto` 可能无法解析；
  - QwenPaw 等工具对长上下文需手动调整 `max_tokens`（文档 9）。
- **地域与额度**：按量计费免费额度**仅限华北2（北京）地域**，使用新加坡/美国端点将立即计费（文档 10）；各模型额度独立计算，不可共享（文档 10）。

> **注意**：文档 1（OpenClaw）中配置示例的 `baseUrl` 为 `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`，而文档 4（Cursor）和文档 6（Qwen Code）均使用 `/compatible-mode/v1` 路径。这并非矛盾——前者是 Anthropic 协议，后者是 OpenAI 协议，二者服务于不同工具链，实际使用时需按工具文档要求选择对应协议路径。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [千问](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [DeepSeek Harness](../../raw/model-user-guide/use-chat-client-or-development-tool/deepseek-harness.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)


