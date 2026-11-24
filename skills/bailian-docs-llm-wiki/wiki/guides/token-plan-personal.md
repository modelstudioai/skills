# token plan personal

[Token](../concepts/token.md) Plan 个人版是面向独立开发者的按月订阅型模型调用权益套餐，提供固定 Credits 额度、并发 Agent 支持及可选的 Harness 工具权益。该计划当前仅支持华北2（北京）地域，所有模型调用与 Harness 工具使用均通过百炼平台统一鉴权与计量。详细权益结构与技术约束请参考官方文档。

## 支持的模型与功能

- **支持模型**：覆盖千问（`qwen4-max`, `qwen4-max-preview`, `qwen3.8-max`, `qwen3.8-flash`, `qwen3.7-plus`, `qwen-image-3.0-pro`, `qwen-audio-*` 等）、万相（`wan2.7-image`, `wan3.0-video`）、DeepSeek（`deepseek-v4.1-flash`, `deepseek-v4-pro-0813` 等）、智谱 AI（`glm-5.3`, `glm-5.2`）、HappyHorse（`happyhorse-1.1-t2v` 等）及领域模型 `decision-model-preview`（[原文标题](../../raw/token-plan-user-guide/token-plan-personal/token-plan-personal-overview.md)）。  
- **预览与限时权益**：`qwen4-max-preview` 为预览模型（2026-11-11 至 2026-11-25），期间 Credits 消耗低至 2 折；`decision-model-preview` 调用完全免费，接入方法见 [原文标题](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-decision-model.md)。  
- **内置工具**：模型原生支持 `web_search`, `web_search_image`, `image_search`, `web_extractor`, `code_interpreter` 等工具，调用时自动触发并按 Credits 抵扣，无需额外配置。

> **注意**：`auto` 模型不支持 `tool_choice`、`thinking.budget_tokens`（Anthropic 兼容）和 `thinking_budget`（OpenAI 兼容）参数，该限制在 [原文标题](../../raw/token-plan-user-guide/token-plan-personal/token-plan-personal-overview.md) 中明确说明。

## 关键参数

| 参数 | 说明 |
|------|------|
| `model` | 必填。合法 Model ID（如 `qwen4-max`, `deepseek-v4.1-flash`），`auto` 为智能路由模型。 |
| `api_key` | 必填。**[Token](../concepts/token.md) Plan 专属 API Key**（格式 `sk-sp-xxx`），仅用于模型调用与 Credits 抵扣；Harness 工具需使用百炼通用 API Key（`sk-xxx`），二者不可混用。 |
| `region` | 必填。当前仅支持 `cn-beijing`（华北2）。 |
| `tool_choice` | 仅对支持该参数的模型有效（`auto` 不支持）；若指定工具，将强制启用对应内置能力。 |

## 使用方式

- **模型调用**：使用 `sk-sp-xxx` Key，通过百炼标准 `/v1/chat/completions` 或 `/v1/models/{model}/chat` 接口发起请求，Credits 自动从套餐或用量包中抵扣。  
- **Harness 工具调用**：Standard/Pro 套餐用户使用 `sk-xxx` Key，通过 MCP 协议调用各工具的 HTTP Streamable 服务（如 `https://dashscope.aliyuncs.com/api/v1/mcps/EnhancedSearch/mcp`），消耗独立计量的免费额度或 88 折后付费额度（[原文标题](../../raw/token-plan-user-guide/token-plan-personal/token-plan-harness-benefits.md)）。  
- **接入流程**：在控制台「我的订阅 > Harness 权益」页签选择工具 → 点击「AI Native 接入」获取配置指令 → 将 MCP URL 与 `sk-xxx` Key 写入本地 Agent 配置（如 Qwen Code、Claude Code 等）。

## 限制和注意事项

- **地域限制**：[Token](../concepts/token.md) Plan 个人版**仅支持华北2（北京）地域**，跨地域调用将失败（[原文标题](../../raw/token-plan-user-guide/token-plan-personal/token-plan-personal-overview.md)）。  
- **退订与降配**：个人版不支持退订或降配；如需更换低档位，须等待当前订阅到期后重新购买。  
- **额度规则**：每月 Credits 按自然月重置；用量包有效期为 1 个月，到期未用额度自动作废，不结转、不退款。  
- **Harness 独立性**：Harness 权益与模型 Credits 完全隔离——不占用、不混算、不支持用量包抵扣；其免费额度按订阅周期发放，未用完不结转（[原文标题](../../raw/token-plan-user-guide/token-plan-personal/token-plan-harness-benefits.md)）。  
- **API Key 分离**：`sk-sp-xxx` 仅用于模型调用；`sk-xxx` 仅用于 Harness 工具（MCP）调用。混用将导致鉴权失败或计费错误。

## 来源文档

- [个人版订阅与权益](../../raw/token-plan-user-guide/token-plan-personal/token-plan-personal-overview.md)
- [Harness 权益](../../raw/token-plan-user-guide/token-plan-personal/token-plan-harness-benefits.md)


