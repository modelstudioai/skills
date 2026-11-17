# qwen api reference

阿里云百炼平台提供多种兼容主流协议的 Qwen 模型调用方式，包括 OpenAI 兼容（Chat Completions 和 Responses）、Anthropic 兼容（Messages）以及原生 DashScope 协议。开发者可根据现有技术栈选择最适配的接口，所有路径均支持多地域部署与业务空间专属域名，推荐优先使用 `https://{WorkspaceId}.{region}.maas.aliyuncs.com` 格式的新版 endpoint 以获得更优性能与稳定性 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。

## 支持的模型/功能

Qwen API 支持全系列千问模型及部分第三方直供模型，按协议能力分层如下：

- **OpenAI 兼容 Chat Completions**：支持 `qwen4-max`、`qwen3.8-max`、`qwen3.7-plus`、`qwen3-vl-plus`、`qwen3.8-omni-flash` 等主流文本与多模态模型；**不支持 Qwen-Audio**（仅 DashScope 协议支持）[OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
- **OpenAI 兼容 Responses**：在 Chat 基础上增强 Agent 能力，内置 `web_search`、`code_interpreter`、`file_search` 等工具，支持 `previous_response_id` 多轮上下文管理与 `x-dashscope-session-cache` 自动缓存 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **Anthropic 兼容 Messages**：支持 `qwen4-max`、`qwen3.7-plus`、`qwen3-vl-plus` 及 `deepseek-v4`、`glm-5.3` 等模型，提供 `thinking` 深度思考控制与 `cache_control` 显式缓存断点 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。
- **DashScope 原生协议**：支持全部 Qwen 模型（含 `qwen-audio`），区分 `text-generation` 与 `multimodal-generation` 服务路径，适用于需精细控制输入格式（如 `image` 字段嵌套）或使用音频输入的场景 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)。

> **注意**：文档 2 与文档 6 对 `qwen3-vl-plus` 的支持描述存在矛盾——文档 2 将其列为 Chat Completions 支持模型，而文档 6 在 DashScope 协议中明确将其归入 `multimodal-generation` 服务路径；实际调用时，`qwen3-vl-plus` 仅可通过 DashScope 协议或 Anthropic 协议调用，**不支持 OpenAI Chat Completions 协议**。

## 关键参数

| 参数 | 协议 | 说明 | 示例 |
|------|------|------|------|
| `model` | 全协议必选 | 模型 ID，需与协议能力匹配。Responses API 的模型列表较 Chat 更严格，仅列明型号才支持完整 Agent 功能 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。 | `"qwen3.8-max"` |
| `messages` / `input` | Chat & DashScope 用 `messages`；Responses 用 `input`（支持 string/array） | 输入结构：Chat/DashScope 要求标准 message 数组；Responses 支持纯字符串或混合 `EasyInputMessage`/`ResponseOutputMessage`。 | `{"role":"user","content":"你好"}` |
| `max_tokens` | Anthropic 必选；Chat/Responses 可选 | Anthropic 协议中为输出+思考总 [Token](../concepts/token.md) 上限；Chat/Responses 中仅为输出上限（思考 [Token](../concepts/token.md) 单独计费）。 | `1024` |
| `reasoning.effort` | Responses 专用 | 控制思考强度（`low`/`medium`/`high`），替代已废弃的 `thinking.budget_tokens`。 | `"high"` |
| `detail` / `min_pixels` / `max_pixels` | 多模态协议 | 图像/视频处理精度与像素阈值。`detail`（`high`/`low`）仅影响 Chat Completions；`min/max_pixels` 全协议通用，但字段层级不同（Chat 在 `image_url` 内，DashScope 在 `image` 同级）[OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。 | `{"detail":"high","max_pixels":8388608}` |

## 使用方式

### 1. 基础调用（OpenAI SDK）
```python
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
# Chat Completions
response = client.chat.completions.create(model="qwen3.7-plus", messages=[{"role":"user","content":"你好"}])
# Responses（带工具）
response = client.responses.create(model="qwen3.8-max", input="分析这份财报", tools=[{"type":"file_search"}])
```

### 2. 异步响应管理（Responses API）
- **创建并存储**：请求中设 `"store": true`，获取 `response.id`（如 `resp_xxx`）。
- **检索结果**：`GET /responses/{response_id}` 获取完整输出与 token 细节 [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)。
- **查询输入历史**：`GET /responses/{response_id}/input_items` 返回多轮对话中所有用户输入与模型回复 [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)。
- **删除响应**：`DELETE /responses/{response_id}` 清理已存储响应 [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)。

### 3. 地域与认证
- 所有协议均支持华北2（北京）、新加坡、美国（弗吉尼亚）等 6 个地域，endpoint 格式统一为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com`。
- 认证方式：HTTP Header `Authorization: Bearer <API_KEY>` 或 `x-api-key: <API_KEY>`（Anthropic 协议）。
- **必须配置业务空间 ID**：`{WorkspaceId}` 需从百炼控制台「业务空间详情」页获取，不可省略。

## 限制和注意事项

- **域名迁移强制要求**：旧域名 `https://dashscope.aliyuncs.com` 已停止维护，**必须迁移至业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），否则可能触发不稳定或限流 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
- **上下文长度限制**：Responses API 为内置工具预留约 20% 上下文空间，实际可用输入长度约为模型窗口的 80%，超长内容将自动截断且不报错 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **参数兼容性**：[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**仅处理文档明确列出的参数**，未提及的 OpenAI 参数（如 `background`）会被静默忽略 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **时间戳单位差异**：`/responses/{id}` 接口返回的 `created_at` 为秒级 Unix 时间戳；而 `/responses/{id}/input_items` 返回的 `created_at` 为毫秒级，调用方需注意单位转换。
- **三方模型地域限制**：DeepSeek、Kimi、GLM 等第三方直供模型**仅在中国站华北2（北京）地域可用**，且需在百炼控制台手动开通对应服务 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。

## 来源文档

- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)


