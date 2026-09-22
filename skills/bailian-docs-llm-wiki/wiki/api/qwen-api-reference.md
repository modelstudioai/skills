# qwen api reference

阿里云百炼平台提供多种 API 协议兼容的 Qwen 模型调用方式，包括 OpenAI 兼容、Anthropic 兼容和原生 DashScope 协议。开发者可根据现有技术栈选择最适配的接口，所有协议均支持主流千问系列模型（如 `qwen3.8-max`、`qwen3.7-plus`、`qwen3-vl-plus` 等）及部分第三方模型。核心能力覆盖文本生成、多模态理解（图像/视频/音频）、工具调用（搜索、代码执行、知识库检索）与结构化输出。

## 支持的模型/功能

Qwen API 支持以下模型类型与功能：

- **模型范围**：  
  - 千问系列：`qwen3.8-*`、`qwen3.7-*`、`qwen3.6-*`、`qwen3.5-*`、`qwen-plus`、`qwen-flash`、`qwen-turbo`、`qwen-coder-*`、`qwen-vl-*`、`qwen-omni-*`、`qwen-audio`（仅 DashScope 协议支持，[DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)）；  
  - 第三方模型：DeepSeek（v4 系列）、Kimi（k3/k2 系列）、GLM（5.x 系列）、MiniMax（M2/M3 系列）等，但**三方直供模型仅在中国站华北2（北京）地域可用**，且需在控制台开通对应服务 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。

- **核心功能**：  
  - 多模态输入：支持 `image_url`、`video_url`、`video`（图像列表）、`input_audio`、`input_video`（仅 `qwen3.8-omni-flash` 在 Responses API 中支持）；  
  - 工具调用：内置 `web_search`、`web_extractor`、`code_interpreter`、`file_search` 等，也支持自定义 `function` 工具；  
  - 结构化输出：通过 `output_config.format.type = "json_schema"` 实现强约束 JSON 输出（qwen3.8/3.7/DeepSeek/GLM 系列支持），其他模型需提示词含 “JSON” 关键词触发普通 JSON 模式 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)；  
  - 显式缓存与 Session 缓存：支持 `cache_control.type = "ephemeral"` 标记缓存断点，或通过请求头 `x-dashscope-session-cache: enable` 启用自动上下文缓存。

> **注意**：Qwen-Audio 不支持 OpenAI 兼容协议，仅支持 DashScope 协议；QwQ 模型不建议设置 `system` 消息，QVQ 模型设置 `system` 消息无效 —— 此矛盾信息在 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md) 和 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md) 中一致，属设计限制，非文档错误。

## 关键参数

| 参数 | 类型 | 必选 | 说明 | 协议支持 |
|------|------|------|------|-----------|
| `model` | `string` | ✅ | 模型 ID，如 `qwen3.8-max`、`qwen3-vl-plus`。具体列表见各协议文档。 | 全部 |
| `messages` / `input` | `array` / `string` | ✅ | 对话上下文（OpenAI/Anthropic/DashScope）或纯文本输入（Responses API）。`input` 支持 `string` 或结构化 `array`（含 `input_text`/`input_image` 等）[创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。 | OpenAI Chat、Anthropic、DashScope、Responses |
| `system` | `string` or `array` | ⚠️ | 系统指令。Anthropic 协议中可为数组以支持显式缓存；OpenAI 协议中仅 `role: "system"` 消息支持。 | Anthropic、OpenAI Chat、DashScope |
| `stream` | `boolean` | ❌（默认 `false`） | 是否流式返回。 | 全部 |
| `store` | `boolean` | ❌（默认 `true`） | Responses API 特有：是否持久化响应，以便后续通过 `previous_response_id` 引用。 | Responses |
| `previous_response_id` | `string` | ❌ | Responses API 特有：复用上一轮响应构建多轮对话，自动组合历史输入与输出。 | Responses |
| `output_config.effort` | `string` | ❌ | 控制思考强度（`low`/`high`/`max`/`xhigh`），替代已废弃的 `thinking.budget_tokens`。 | Anthropic、Responses（`reasoning.effort`） |
| `max_pixels` / `min_pixels` / `total_pixels` | `integer` | ❌ | 图像/视频分辨率控制参数，影响 [Token](../concepts/token.md) 消耗与识别精度。取值因模型而异，详见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。 | OpenAI Chat、DashScope |

## 使用方式

### 1. 接入端点（Endpoint）
所有协议均使用业务空间专属域名（推荐），格式为：  
`https://{WorkspaceId}.{region}.maas.aliyuncs.com/{path}`  
其中 `{WorkspaceId}` 为控制台获取的业务空间 ID，`{region}` 如 `cn-beijing`、`ap-southeast-1` 等。  
- **OpenAI 兼容**：`/compatible-mode/v1/chat/completions`（Chat）、`/compatible-mode/v1/responses`（Responses）；  
- **Anthropic 兼容**：`/apps/anthropic/v1/messages`；  
- **DashScope 原生**：`/api/v1/services/aigc/text-generation/generation`（文本）、`/api/v1/services/aigc/multimodal-generation/generation`（多模态）。

### 2. 认证
通过 `Authorization: Bearer <API_KEY>` 或 `x-api-key: <API_KEY>` 请求头传入百炼 API Key。需先[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。

### 3. SDK 配置示例（Python）
```python
# OpenAI 兼容
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

# Anthropic 兼容
import anthropic
client = anthropic.Anthropic(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic"
)

# DashScope 原生
import dashscope
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
```

## 限制和注意事项

- **地域与模型可用性**：第三方模型（如 DeepSeek、Kimi）仅在华北2（北京）中国站可用；业务空间专属域名（如 `*.cn-beijing.maas.aliyuncs.com`）在华北2、新加坡、中国香港三地已上线，**强烈建议迁移**以获得更高性能与稳定性 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。  
- **协议差异**：  
  - OpenAI Responses API 不支持 `background`（异步）参数，仅同步调用；  
  - Anthropic 协议中 `temperature` 范围为 `[0, 2)`，不同于官方 `[0.0, 1.0]`，迁移时需校验取值 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)；  
  - DashScope 协议中 `messages` 需嵌套于 `input` 对象内，而 OpenAI/Anthropic 协议为顶层字段。  
- **上下文管理**：  
  - Responses API 的最大输入上下文约为模型窗口的 80%（预留 20% 给工具调用与推理），超长内容将自动截断；  
  - `previous_response_id` 有效期为 7 天，`store=false` 的响应不可被引用。  
- **计费与 [Token](../concepts/token.md)**：  
  - `total_pixels` 参数直接影响图像 [Token](../concepts/token.md) 消耗（每 32×32 像素 ≈ 1 Token），长视频建议调低此值以控本；  
  - `usage` 返回中 `input_tokens_details.cached_tokens` 表示命中缓存的 Token 数，`output_tokens_details.reasoning_tokens` 为思考过程 Token，均单独计费。  
- **弃用提醒**：`thinking.budget_tokens` 参数已废弃，新接入请统一使用 `output_config.effort`（Anthropic）或 `reasoning.effort`（Responses）控制思考强度。

## 来源文档

- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


