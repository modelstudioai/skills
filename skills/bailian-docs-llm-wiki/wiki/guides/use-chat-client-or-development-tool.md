# use chat client or development tool

Token Plan 提供标准化的 API 接入能力，支持主流 AI 编程助手与智能体开发工具（如 Qoder、Claude Code、Qwen Code 等）通过 OpenAI 或 Anthropic 兼容协议快速集成。开发者只需配置对应协议的 Base URL 和 `sk-sp-` 开头的 Token Plan 专属 API Key 即可调用。所有配置均需严格匹配计费计划，避免误走按量通道或鉴权失败。

## 支持的模型/功能

Token Plan 当前不直接暴露底层模型列表，而是通过工具链抽象提供能力。所支持的工具已在 [接入AI工具](../../raw/token-plan-user-guide/use-chat-client-or-development-tool.md) 中明确列出，包括 Qoder、Claude Code、Codex、Qwen Code、OpenClaw、Hermes Agent、OpenCode、Trae、DeepSeek Harness、WorkBuddy 等。各工具实际调用的模型由 Token Plan 后端动态路由，开发者无需指定模型名称，仅需遵循其协议类型（OpenAI 兼容或 Anthropic 兼容）发起请求。

> **注意**：部分工具文档（如 [Qwen Code](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/qwen-code.md)）中提及“支持 `qwen-max` 模型名显式指定”，但该行为未在主文档 [接入AI工具](../../raw/token-plan-user-guide/use-chat-client-or-development-tool.md) 中声明，且实测中 Token Plan 网关会忽略 `model` 字段——请以主文档为准，勿依赖客户端传入的 model 参数。

## 关键参数

| 参数 | 值/说明 | 来源 |
|------|---------|------|
| `base_url` | OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` | [接入AI工具](../../raw/token-plan-user-guide/use-chat-client-or-development-tool.md) |
| `api_key` | 必须为 `sk-sp-` 开头的 Token Plan 专属密钥，生成后仅显示一次 | [接入AI工具](../../raw/token-plan-user-guide/use-chat-client-or-development-tool.md) |
| `Content-Type` | `application/json`（OpenAI 兼容）或 `application/json` + `x-api-key` header（Anthropic 兼容，部分工具要求） | [接入AI工具](../../raw/token-plan-user-guide/use-chat-client-or-development-tool.md) |

## 使用方式

1. 在目标工具（如 Qoder 或 Trae）的设置页中，选择「自定义 API」或「Local/Proxy Endpoint」模式；  
2. 根据工具支持的协议类型，填入对应 Base URL；  
3. 输入 `sk-sp-` 开头的 API Key（注意：不可复用 Coding Plan 或百炼 `sk-` 密钥）；  
4. 保存并测试连接（建议先用 `curl` 或 Postman 验证 `/v1/models` 或 `/v1/messages` 端点）。

## 限制和注意事项

- Token Plan 的 API Key 与 Base URL 严格绑定：`sk-sp-` 密钥**仅能**配合 Token Plan 的两个 Base URL 使用，混用 Coding Plan 或百炼 Base URL 将导致 401/403 错误或意外按量扣费；  
- 所有工具均不支持流式响应（`stream: true`）以外的高级参数（如 `logprobs`, `top_logprobs`, `response_format`），网关会静默忽略；  
- Anthropic 兼容路径 `/apps/anthropic` 仅支持 `messages` 接口，不支持 `/v1/complete` 等旧版端点；  
- 若工具文档（如 [DeepSeek Harness](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/deepseek-harness.md)）建议使用 `https://dashscope.aliyuncs.com/...`，请忽略——该地址属于百炼按量付费体系，与 Token Plan 不兼容。

## 来源文档

- [接入AI工具](../../raw/token-plan-user-guide/use-chat-client-or-development-tool.md)


