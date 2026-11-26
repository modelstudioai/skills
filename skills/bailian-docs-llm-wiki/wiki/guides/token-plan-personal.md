# token plan personal

[Token](../concepts/token.md) Plan 个人版是面向独立开发者的按月订阅服务，提供模型调用 Credits 额度、内置工具能力及 Harness 权益（Standard/Pro 套餐专属），所有权益均绑定百炼账号并限定于华北2（北京）地域。其核心设计兼顾成本可控性与开箱即用的 AI 工具链支持，适用于原型验证、轻量级 Agent 开发及个人项目迭代。详细规则请以控制台实时展示为准。

## 支持的模型/功能

- **支持模型**：覆盖千问（`qwen4-max`、`qwen3.8-flash` 等）、万相（`wan2.7-image`、`wan3.0-video`）、DeepSeek（`deepseek-v4.1-flash` 等）、智谱 AI（`glm-5.3`）、HappyHorse 及领域模型 `decision-model-preview`（[原文标题](../../raw/token-plan-user-guide/token-plan-personal/token-plan-personal-overview.md)）。  
- **`auto` 模型**：自动路由至最优底层模型，但**不支持** `tool_choice`、`thinking.budget_tokens`（Anthropic 兼容）和 `thinking_budget`（OpenAI 兼容）参数。  
- **内置工具**：通过 Responses API 调用模型时自动触发，按 Credits 抵扣，无需单独接入，包括 `web_search`（联网搜索）、`web_search_image`（文搜图）、`image_search`（图搜图）、`web_extractor`（网页抓取）、`code_interpreter`（代码解释器）等（[原文标题](../../raw/token-plan-user-guide/token-plan-personal/token-plan-personal-overview.md)）。  
- **Harness 权益**：Standard 与 Pro 套餐额外附赠，覆盖联网搜索增强版、图像生成、语音合成、代码解释器等 AgentStudio 工具，**不占用 Credits**，额度独立计量、用尽后享 88 折后付费（[原文标题](../../raw/token-plan-user-guide/token-plan-personal/token-plan-harness-benefits.md)）。

> **注意**：文档 1 中“决策模型 `decision-model-preview` 限时免费”与文档 2 中“Harness 权益不包含 RAG/Memory/Managed Agent 等工具”存在隐含冲突——前者属模型调用（免 Credits），后者属 Harness 工具（享折扣但非免费）。实际使用中，`decision-model-preview` 调用走模型 Credits 通道（当前免费），而百炼知识库（RAG）等需通过 Harness 通道调用（Standard/Pro 享额度+折扣），二者路径分离，不可混用。

## 关键参数

| 参数 | 说明 |
|------|------|
| **Credits 额度** | Lite（20,000）、Essential（45,000）、Standard（80,000）、Pro（200,000）/月；额度按订阅月重置，不结转（[原文标题](../../raw/token-plan-user-guide/token-plan-personal/token-plan-personal-overview.md)）。 |
| **Harness 免费额度** | Standard/Pro 独享，如联网搜索增强版（100/500 次/月）、图像生成（20/50 张/月）、代码解释器（100/500 次/月）等；未列额度的工具仅享 88 折（[原文标题](../../raw/token-plan-user-guide/token-plan-personal/token-plan-harness-benefits.md)）。 |
| **API Key 区分** | 模型调用必须使用 [Token](../concepts/token.md) Plan 专属 Key（`sk-sp-xxx`）；Harness 工具必须使用百炼通用 Key（`sk-xxx`），两者**不可混用**（[原文标题](../../raw/token-plan-user-guide/token-plan-personal/token-plan-harness-benefits.md)）。 |

## 使用方式

- **模型调用**：使用 `sk-sp-xxx` Key，通过百炼标准 API（如 `/v1/chat/completions`）发起请求，指定 `model`（如 `qwen4-max`）及可选 `tools`（如 `{"type": "web_search"}`），Credits 自动抵扣。  
- **Harness 工具调用**：使用 `sk-xxx` Key，通过 MCP 协议直连各工具 URL（如 `https://dashscope.aliyuncs.com/api/v1/mcps/EnhancedSearch/mcp`），配置 `Authorization: Bearer YOUR_API_KEY` 请求头。支持 CLI（`bl auth login`）、OpenCode、Codex、Claude Code、Qwen Code 等客户端一键接入（[原文标题](../../raw/token-plan-user-guide/token-plan-personal/token-plan-harness-benefits.md)）。  
- **用量包补充**：额度用尽后，可在控制台购买用量包（100 元/个，含 20,000 Credits），最多持有 5 个，有效期 1 个月，到期作废（[原文标题](../../raw/token-plan-user-guide/token-plan-personal/token-plan-personal-overview.md)）。

## 限制和注意事项

- **地域限制**：[Token](../concepts/token.md) Plan 个人版**仅支持华北2（北京）地域**，跨地域调用将失败（[原文标题](../../raw/token-plan-user-guide/token-plan-personal/token-plan-personal-overview.md)）。  
- **退订与降配**：个人版**不支持退订或降配**；如需更换低档位，须等待当前订阅到期后重新购买（[原文标题](../../raw/token-plan-user-guide/token-plan-personal/token-plan-personal-overview.md)）。  
- **额度与权益隔离**：模型 Credits、用量包、Harness 权益三者**完全独立核算**；用量包不能抵扣 Harness 费用，Harness 调用不消耗任何 Credits（[原文标题](../../raw/token-plan-user-guide/token-plan-personal/token-plan-harness-benefits.md)）。  
- **`qwen4-max-preview` 下线**：原 ID 请求已自动路由至 `qwen4-max`，按后者计费，预览期折扣失效，建议立即更新配置（[原文标题](../../raw/token-plan-user-guide/token-plan-personal/token-plan-personal-overview.md)）。  
- **夜间折扣**：`qwen3.8-max`/`qwen3.8-flash`（22:00–08:00 享 4 折）、`deepseek-v4-pro-0813` 等（同时间段享 5 折），折扣仅限指定模型与时段（[原文标题](../../raw/token-plan-user-guide/token-plan-personal/token-plan-personal-overview.md)）。

## 来源文档

- [个人版订阅与权益](../../raw/token-plan-user-guide/token-plan-personal/token-plan-personal-overview.md)
- [Harness 权益](../../raw/token-plan-user-guide/token-plan-personal/token-plan-harness-benefits.md)


