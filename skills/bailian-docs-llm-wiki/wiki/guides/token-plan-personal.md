# token plan personal

Token Plan 个人版是面向独立开发者的按月订阅模型服务套餐，提供固定额度的 Credits 用于调用百炼平台支持的各类大模型，并为 Standard 和 Pro 档位额外附赠 Harness 权益（覆盖联网搜索、图像生成等 AgentStudio 工具）。所有模型调用均通过 `sk-sp-xxx` 格式的 Token Plan 专属 API Key 进行，而 Harness 工具则需使用独立的百炼 API Key（`sk-xxx`）调用 MCP 接口。套餐权益、额度规则与接入方式需结合控制台实时状态使用。

## 支持的模型与功能

### 模型支持
Token Plan 个人版支持多厂商、多模态模型，包括：
- **千问系列**：`qwen4-max`、`qwen4-max-preview`（预览期至 2026-11-25，消耗低至 2 折）、`qwen3.8-max`/`qwen3.8-flash`（夜间 22:00–08:00 享 4 折）、`qwen-image-3.0-pro`、`qwen-audio-3.0-tts-plus` 等；
- **万相系列**：`wan2.7-image`、`wan2.7-image-pro`、`wan3.0-video`；
- **DeepSeek 系列**：`deepseek-v4.1-flash`、`deepseek-v4-pro-0813`（夜间享 5 折）等；
- **智谱 AI、HappyHorse 及领域模型**：如 `glm-5.3`、`happyhorse-1.1-t2v`、`decision-model-preview`（调用不消耗 Credits）。

> **注意**：`auto` 模型不支持 `tool_choice`、`thinking.budget_tokens`（Anthropic 兼容）和 `thinking_budget`（OpenAI 兼容）参数，详见 [个人版订阅与权益](../../raw/token-plan-user-guide/token-plan-personal/token-plan-personal-overview.md)。

### 内置工具（模型级）
以下工具通过 Responses API 调用模型时自动触发，按 Credits 抵扣，无需单独开通：
- `web_search`（联网搜索）、`web_search_image`（文搜图）、`image_search`（图搜图）、`web_extractor`（网页抓取）、`code_interpreter`（代码解释器）

### Harness 权益工具（独立计量）
仅 Standard 与 Pro 套餐附赠，**不占用 Credits**，使用百炼 API Key（`sk-xxx`）调用 MCP 接口，支持：
- 自研工具：联网搜索增强版、垂类搜索、网页解析、图像生成、语音合成、语音识别、代码解释器；
- 百炼知识库、记忆库、全托管智能体、沙箱等暂无免费额度，但享 88 折后付费。

详细额度见 [Harness 权益](../../raw/token-plan-user-guide/token-plan-personal/token-plan-harness-benefits.md)，例如 Standard 档位每月含联网搜索增强版 100 次、图像生成 20 张；Pro 档位对应为 500 次、50 张。

## 关键参数

| 参数类型 | 说明 |
|----------|------|
| **API Key 类型** | 模型调用必须使用 `sk-sp-xxx`（Token Plan 专属），Harness 工具必须使用 `sk-xxx`（百炼通用 API Key）；二者不可混用，详见 [Harness 权益](../../raw/token-plan-user-guide/token-plan-personal/token-plan-harness-benefits.md)。 |
| **模型调用参数** | 支持标准 OpenAI/Anthropic 兼容参数（如 `model`, `messages`, `max_tokens`）；`qwen4-max-preview` 等预览模型支持 `stream`, `response_format`，但 `auto` 模型不支持 `tool_choice` 等特定参数。 |
| **Harness MCP 配置** | 所有 Harness 工具均为 HTTP Streamable 类型，请求头统一为 `Authorization: Bearer ${DASHSCOPE_API_KEY}`；MCP URL 在控制台「我的订阅 > Harness 权益」页签中获取。 |

## 使用方式

### 模型调用（Credits 抵扣）
1. 获取 `sk-sp-xxx` API Key（[控制台 → API Key 管理](https://bailian.console.aliyun.com/cn-beijing/api-keys)）；
2. 使用标准 `/v1/chat/completions` 或 `/v1/embeddings` 等接口，指定支持的 `model` ID；
3. 请求成功即按模型单价扣除对应 Credits，剩余额度可在 [控制台 → 我的订阅](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan) 查看。

### Harness 工具接入（独立权益抵扣）
1. 在控制台「我的订阅 > Harness 权益」页签确认已开通对应工具；
2. 获取百炼 API Key（`sk-xxx`），**非** `sk-sp-xxx`；
3. 选择接入方式：
   - **AI Native（推荐）**：复制控制台「一键接入」指令，在 Qwen Code / Claude Code / Codex / OpenCode 中执行（如 `qwen mcp add EnhancedSearch ...`）；
   - **手动配置**：将 MCP URL 与 `Authorization` 头写入本地 Agent 配置文件（如 `~/.qwen/settings.json`），并设置环境变量 `DASHSCOPE_API_KEY`；
4. 调用时系统自动优先抵扣免费额度，用尽后按 88 折计费。

完整接入示例见 [Harness 权益](../../raw/token-plan-user-guide/token-plan-personal/token-plan-harness-benefits.md) 中「接入联网搜索增强版」章节。

## 限制和注意事项

- **地域限制**：Token Plan 个人版目前仅支持华北2（北京）地域。
- **额度规则**：
  - 模型 Credits 按月发放，不结转；用量包（100 元/20,000 Credits）有效期 1 个月，到期作废；
  - Harness 免费额度按订阅周期发放，未用完不结转，升配后剩余额度按公式折算（见 [Harness 权益](../../raw/token-plan-user-guide/token-plan-personal/token-plan-harness-benefits.md)）。
- **权限与退订**：
  - 个人版不支持自助退订或降配；订阅到期后 API Key 暂停，续费后自动恢复；
  - Lite 与 Essential 套餐**不包含 Harness 权益**；团队版不支持该权益。
- **关键隔离原则**：
  - Harness 权益与模型 Credits **完全独立核算**：Harness 调用不扣 Credits，用量包也不能抵扣 Harness 费用；
  - `sk-xxx`（百炼 Key）仅用于 Harness 工具；`sk-sp-xxx`（Token Plan Key）仅用于模型调用 —— 混用将导致鉴权失败或错误计费。

> **注意**：文档 2 中提及“Essential 套餐权益含‘联网搜索等内置工具’”，但文档 1 明确指出“Lite 与 Essential 套餐不包含 Harness 权益”，且内置工具（如 `web_search`）属于模型级能力、按 Credits 抵扣，而 Harness 的“联网搜索增强版”是独立 MCP 服务。二者属不同技术栈，此处无矛盾，但开发者须严格区分调用路径与计费归属。

## 来源文档

- [Harness 权益](../../raw/token-plan-user-guide/token-plan-personal/token-plan-harness-benefits.md)
- [个人版订阅与权益](../../raw/token-plan-user-guide/token-plan-personal/token-plan-personal-overview.md)


