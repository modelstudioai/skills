# token plan personal

Token Plan 个人版是面向独立开发者的按月订阅服务，提供模型调用 Credits 额度、Harness 权益及配套工具能力。它通过 `sk-sp-xxx` 格式的专属 API Key 调用百炼模型（按 Credits 抵扣），同时 Standard/Pro 套餐用户可额外使用 Harness 工具（如联网搜索增强版、图像生成等），该部分消耗独立计量、不占用 Credits。所有权益均绑定订阅周期，额度按月发放、不结转，且当前不支持退订或降配。

## 支持的模型与功能

- **主流模型覆盖**：支持千问（qwen4-max、qwen3.8-flash、qwen4-max-preview 等）、万相（wan2.7-image、wan3.0-video）、DeepSeek（deepseek-v4.1-flash、deepseek-v4-pro-0813）、智谱 GLM（glm-5.3）、HappyHorse（happyhorse-1.1-t2v）及领域模型（如 `decision-model-preview`）。其中 `auto` 模型不支持 `tool_choice`、`thinking.budget_tokens` 和 `thinking_budget` 参数 [原文标题](../../raw/token-plan-user-guide/token-plan-personal/token-plan-personal-overview.md)。
- **限时模型权益**：`qwen4-max-preview` 为预览模型（2026-11-11 至 2026-11-25），期间 Credits 消耗低至 2 折；夜间（22:00–08:00）调用部分 qwen/deepseek 模型享 4–5 折 [原文标题](../../raw/token-plan-user-guide/token-plan-personal/token-plan-personal-overview.md)。
- **内置工具**：模型原生支持 `web_search`、`web_search_image`、`image_search`、`web_extractor`、`code_interpreter` 等工具，调用时自动触发并按 Credits 抵扣，无需单独接入。
- **Harness 权益工具**：Standard 与 Pro 套餐附赠独立于 Credits 的 Harness 权益，覆盖联网搜索增强版、垂类搜索、网页解析、图像生成、语音合成、代码解释器等工具，享有每月免费额度及超量后 88 折计费 [原文标题](../../raw/token-plan-user-guide/token-plan-personal/token-plan-harness-benefits.md)。

## 关键参数

| 参数 | 说明 |
|------|------|
| `model` | 必填。模型 ID（如 `qwen3.8-max`、`deepseek-v4.1-flash`），`auto` 可启用自动选模。 |
| `tool_choice` | 仅对支持工具的模型生效；`auto` 模型不支持该参数 [原文标题](../../raw/token-plan-user-guide/token-plan-personal/token-plan-personal-overview.md)。 |
| `thinking_budget` / `thinking.budget_tokens` | Anthropic/OpenAI 兼容参数；`auto` 模型不支持 [原文标题](../../raw/token-plan-user-guide/token-plan-personal/token-plan-personal-overview.md)。 |
| `stream` | 布尔值，控制是否流式响应，默认 `false`。 |
| `max_tokens` | 输出长度上限，受模型能力限制。 |

> **注意**：Harness 工具（如 EnhancedSearch）不使用 `sk-sp-xxx` Key，而需 `sk-xxx` 百炼 API Key，并通过 MCP 协议调用，其参数与模型 API 完全不同，详见 [原文标题](../../raw/token-plan-user-guide/token-plan-personal/token-plan-harness-benefits.md)。

## 使用方式

- **模型调用**：使用 `sk-sp-xxx` Token Plan 专属 API Key，向百炼模型 API（如 `/v1/chat/completions`）发起请求，Credits 自动按模型单价与输入/输出 token 数抵扣。
- **Harness 工具调用**：
  - Standard/Pro 用户在控制台 [我的订阅 > Harness 权益](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal) 查看可用工具及 MCP 地址；
  - 使用 `sk-xxx` 百炼 API Key（非 `sk-sp-xxx`），按 MCP 协议配置本地 Agent（如 Qwen Code、Claude Code）或直接 HTTP 调用；
  - 示例 MCP URL：`https://dashscope.aliyuncs.com/api/v1/mcps/EnhancedSearch/mcp`，Header 为 `Authorization: Bearer YOUR_API_KEY` [原文标题](../../raw/token-plan-user-guide/token-plan-personal/token-plan-harness-benefits.md)。
- **用量包补充**：额度用尽后，可在控制台购买用量包（100 元/个/月，含 20,000 Credits），最多持有 5 个，有效期 1 个月，到期未用自动作废。

## 限制和注意事项

- **地域限制**：Token Plan 个人版目前仅支持华北2（北京）地域。
- **API Key 隔离**：`sk-sp-xxx` 仅用于模型调用（抵扣 Credits）；`sk-xxx` 仅用于 Harness 工具（抵扣权益次数/折扣账单），两者不可混用。
- **额度规则**：
  - 每月 Credits 额度按订阅月重置，不结转；
  - Harness 免费额度按月发放，未用完不结转；
  - 用量包不参与 Harness 计费，仅补充模型 Credits。
- **升级与续费**：
  - 升级档位按剩余天数补差价，新增 Credits 按比例折算发放；
  - 续费不增加当前周期额度，新周期起按新档位计量；
  - 不支持退订与降配；到期后 API Key 暂停，重新订阅即恢复。
- **模型兼容性**：`qwen4-max-preview` 别名 `qwen4.0-max-preview`，账单中统一显示为后者；预览期结束后将下线，开发者应避免长期依赖。

## 来源文档

- [个人版订阅与权益](../../raw/token-plan-user-guide/token-plan-personal/token-plan-personal-overview.md)
- [Harness 权益](../../raw/token-plan-user-guide/token-plan-personal/token-plan-harness-benefits.md)


