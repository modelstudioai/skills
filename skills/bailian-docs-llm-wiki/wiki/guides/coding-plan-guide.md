# coding plan guide

Coding Plan 是百炼平台面向开发者提供的编程专用模型订阅服务，通过固定月费模式提供千问、GLM、Kimi、MiniMax 等主流编码模型的稳定调用能力。它专为 AI 编程工具（如 Claude Code、OpenCode、OpenClaw 等）设计，不支持直接 API 调用，需配合兼容协议端点与套餐专属凭证使用。所有请求均按模型调用次数计费并受多级额度限制约束。

## 支持的模型与功能

- **当前主力推荐模型**：`qwen3.7-plus`（支持图片理解）、`qwen3.6-plus`（支持图片理解）、`kimi-k2.5`（支持图片理解）、`glm-5`、`MiniMax-M2.5`  
- **其他可用模型**：`qwen3.5-plus`（支持图片理解）  
- **模型能力统一支持**：  
  - 思考模式（Reasoning/Thinking Mode）：所有推荐模型默认支持，需通过客户端配置启用（如 OpenCode 的 `thinking.budgetTokens`、Qwen Code 的 `enable_thinking`、OpenClaw 的 `reasoning: true` + `compat.thinkingFormat: "qwen"`）；详见[OpenCode](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/opencode.md) 和 [OpenClaw](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/openclaw.md) 文档。  
  - 图片理解：仅标注“支持图片理解”的模型可用，输入需含 base64 编码图像数据。  
- **不支持的模型**：`qwen-portal/coder-model` 等非百炼平台模型，调用将返回 `model 'xxx' is not supported` 错误；该模型属于 Qwen Chat 网页版免费服务，与 Coding Plan 无关 [原文标题](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan-faq.md)。

> **注意**：文档 2 中称 Lite 套餐“支持所有套餐模型”，但文档 1 明确指出 Lite 套餐已于 2026 年 4 月 13 日起停止续费与升级，且当前仅 Pro 套餐在售；实际可用模型以 [Coding Plan概述](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan.md) 中“Pro 高级套餐”所列为准，Lite 已不可新购或续费。

## 关键参数

| 参数 | 说明 | 取值要求 | 来源依据 |
|------|------|----------|----------|
| **API Key** | 必须使用套餐专属 Key，格式为 `sk-sp-xxx` | 不可混用百炼通用 Key（`sk-xxx`），否则触发按量扣费或 `401 invalid access token` 错误 | [原文标题](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan-faq.md) |
| **Base URL** | 协议决定端点：<br>• OpenAI 兼容 → `https://coding.dashscope.aliyuncs.com/v1`<br>• Anthropic 兼容 → `https://coding.dashscope.aliyuncs.com/apps/anthropic` | 路径错误将导致 `404` 或 `403 invalid api-key`；例如 Claude Code 必须用 Anthropic 端点，不可误配为 `/v1` | [原文标题](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan-faq.md) |
| **thinking_budget / budgetTokens** | 控制思考链最大 Token 数 | 必须 ≤ 模型上限：`qwen3.7-plus`（262144）、`qwen3.6-plus`（81920）、`glm-5`（32768）等；超限报错 `The thinking_budget parameter must be a positive integer and not greater than 38912`（示例值已过时，以实际模型上限为准） | [原文标题](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan-faq.md) |
| **max_tokens / limit.output** | 控制响应最大输出长度 | 必须 ∈ `[1, xxxx]`，具体上限依模型而定；超限报错 `InternalError.Algo.InvalidParameter: Range of max_tokens should be [1, xxxx]` | [原文标题](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan-faq.md) |

## 使用方式

1. **订阅与凭证获取**  
   - 订阅 Pro 套餐：访问 [Coding Plan 购买页](https://common-buy.aliyun.com/coding-plan)；RAM 子账号需主账号授权管理员权限后方可订阅。  
   - 获取凭证：在 [Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan) 复制 `sk-sp-xxx` 格式 API Key，并确认 Base URL 协议类型。

2. **工具接入**  
   - 所有兼容工具均需配置上述 API Key 与对应 Base URL；  
   - 各工具思考模式启用方式不同，需严格参照其文档：  
     - Claude Code：`/config` → `Thinking mode` 切换为 `true`；  
     - OpenCode：在 `opencode.json` 中配置 `thinking.type: "enabled"` 与 `budgetTokens`；  
     - Qwen Code：在 `~/.qwen/settings.json` 的 `generationConfig.extra_body` 中设 `"enable_thinking": true`；  
     - OpenClaw：需同时设置 `reasoning: true` 与 `compat.thinkingFormat: "qwen"`，并重启 Gateway。  
   - 完整工具列表及配置指引见 [Coding Plan概述](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan.md)。

3. **上下文管理**  
   - 输入超长报错 `400 InvalidParameter: Range of input length should be [1, xxx]` 时，优先新建会话（`/new`）或压缩上下文（`/compact`）；  
   - OpenCode 用户可配置 `limit` 参数控制上下文长度，详见 [OpenCode](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/opencode.md)。

## 限制和注意事项

- **额度限制（Pro 套餐）**：  
  - 每 5 小时：6,000 次请求（滚动恢复，每分钟释放 5 小时前用量）；  
  - 每周：45,000 次请求（每周一 00:00:00 UTC+8 重置）；  
  - 每月：90,000 次请求（订阅日当日 00:00:00 UTC+8 重置）。  
  - 单次提问消耗 5–30+ 次额度，取决于任务复杂度、上下文长度及工具调用次数。

- **严格使用范围**：  
  - **禁止 API 直接调用**：不得用于自动化脚本、自定义后端服务或非交互式批量任务；违规将导致订阅暂停或 Key 封禁；  
  - **禁止账号共享**：套餐为订阅人专享，共享可能导致权益受限；  
  - **数据授权**：输入与输出内容将用于服务优化，终止使用后不再新增授权，但历史数据授权不可撤回（参见《阿里云百炼服务协议》第 5.2 条）。

- **网络与稳定性**：  
  - `Connection closed mid-response` 多因本地代理（VPN/HTTP Proxy）不稳定导致，建议关闭代理或确保其可稳定访问 `coding.dashscope.aliyuncs.com`；  
  - 海外用户可正常使用，若遇延迟，推荐使用 [Model Studio Coding Plan](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan.md)。

- **错误排查重点**：  
  - `401 invalid access token`：检查是否误用 `sk-xxx` 通用 Key；  
  - `403 invalid api-key`：确认 Base URL 域名拼写（必须为 `coding.dashscope.aliyuncs.com`，非 `dashscope.aliyuncs.com`）；  
  - `Unknown model` / `No API key found for provider "xxxxx"`：OpenClaw 用户需确保 `openclaw.json` 中 `models.providers` 包含 `bailian` 键，且 `agents.defaults.model.primary` 前缀为 `bailian/`。

## 来源文档

- [Coding Plan 常见问题](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan-faq.md)
- [Coding Plan概述](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan.md)


