# qwen api reference

Qwen API 提供多种兼容协议（OpenAI、Anthropic、DashScope 原生）的调用方式，支持文本、[多模态](../concepts/multi-modal.md)（图像/视频/音频）、工具调用与深度思考等能力。所有接口均基于业务空间专属域名（`{WorkspaceId}.<region>.maas.aliyuncs.com`）提供服务，推荐使用新域名以获得更高性能与稳定性。开发者需先[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，并根据所选协议安装对应 SDK。

## 支持的模型/功能

Qwen API 支持以下核心模型系列及能力：

- **文本大模型**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.6-flash`、`qwen-turbo`、`qwen-coder-next` 等全量千问商业版与开源版模型；同时支持 DeepSeek（v4 系列）、GLM（5.x）、Kimi（k3/k2.7-code）、MiniMax（M2.5/M2.1）等第三方直供模型。
- **[多模态](../concepts/multi-modal.md)模型**：`qwen3.8-omni-flash`（音视频端到端理解）、`qwen3-vl-plus`、`qwen-vl-max`、`QVQ`、`Qwen2.5-VL`，支持图像、视频（URL/Base64/本地文件）、音频（仅 `qwen3.8-omni-flash`）输入。
- **专用能力**：
  - 工具调用（Agent）：内置 `web_search`、`web_extractor`、`code_interpreter`、`web_search_image` 等工具，仅 [OpenAI兼容-Responses](raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md) 和 Anthropic Messages 接口完整支持。
  - 深度思考：通过 `reasoning.effort`（Responses）或 `output_config.effort`（Anthropic）控制推理强度，`qwen3.8-max`、`deepseek-v4-pro`、`glm-5.3` 等模型支持多档位力度调节。
  - 显式缓存：在 `system` 或 `messages.content` 中使用 `cache_control: {type: "ephemeral"}` 标记可缓存内容块，降低重复请求成本。
  - 结构化输出：Anthropic 接口支持严格 JSON Schema 输出（`output_config.format.type = "json_schema"`），需提示词含 "JSON" 关键词且满足 schema 约束。

> **注意**：Qwen-Audio 仅支持 DashScope 原生协议，不支持 OpenAI 兼容协议（见 [DashScope API 参考](raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)）；QwQ 模型不建议设置 `system` 消息，QVQ 模型中 `system` 消息无效（见 [OpenAI兼容-Chat](raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)）。

## 关键参数

| 参数 | 类型 | 说明 | 协议支持 |
|------|------|------|----------|
| `model` | `string` | 必填。模型 ID，如 `qwen3.8-max`、`qwen3-vl-plus`。不同协议支持列表有差异（详见各文档）。 | 全协议 |
| `messages` / `input` | `array` / `string|array` | 对话上下文。OpenAI Chat 要求标准 role/content 数组；Responses 支持纯字符串或增强型 EasyInputMessage；Anthropic 使用 role/content 数组且支持 `tool_use`/`tool_result`。 | Chat/Responses/Anthropic |
| `max_tokens` | `integer` | 回复最大 token 数。**注意**：在 Anthropic 协议中，对 `qwen3.8-max` 等模型，该值限制“回复+思考”总长度；对 `glm-5.2`，若传 `thinking.budget_tokens` 则仅限回复长度（见 [Anthropic兼容-Messages](raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)）。 | Chat/Responses/Anthropic |
| `stream` | `boolean` | 是否流式响应，默认 `false`。流式时返回 `text/event-stream`。 | 全协议 |
| `temperature` | `number` | 采样温度。**注意**：Anthropic 协议取值范围为 `[0, 2)`，与官方 `[0.0, 1.0]` 不同，迁移时需校验（见 [Anthropic兼容-Messages](raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)）。 | 全协议 |
| `tools` | `array` | 工具定义数组。Responses 和 Anthropic 支持内置工具与自定义 function；OpenAI Chat 仅支持基础 function call（无内置工具）。 | Responses/Anthropic |
| `previous_response_id` | `string` | Responses 特有。用于多轮对话，服务端自动拼接历史上下文，避免手动维护 `messages` 数组（见 [创建响应](raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）。 | Responses |

## 使用方式

### 1. 接入地址（Base URL）
所有协议均使用业务空间专属域名，格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com`。地域与路径映射如下：

| 协议 | 华北2（北京）路径 | 新加坡路径 | 其他地域 |
|------|------------------|------------|----------|
| **OpenAI Chat** | `/compatible-mode/v1/chat/completions` | `/compatible-mode/v1/chat/completions` | 同构，仅 region 变更 |
| **OpenAI Responses** | `/compatible-mode/v1/responses` | `/compatible-mode/v1/responses` | 同构 |
| **Anthropic Messages** | `/apps/anthropic/v1/messages` | `/apps/anthropic/v1/messages` | 同构 |
| **DashScope 原生** | `/api/v1/services/aigc/text-generation/generation`（文本）<br>`/api/v1/services/aigc/multimodal-generation/generation`（[多模态](../concepts/multi-modal.md)） | 同构 | 同构 |

> `{WorkspaceId}` 需替换为真实业务空间 ID（见 [获取业务空间ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)）。

### 2. 认证
- 通过 `Authorization: Bearer <API_KEY>` 请求头传入百炼 API Key。
- Anthropic 协议额外支持 `x-api-key` 请求头。

### 3. 多模态输入示例（以 OpenAI Chat 为例）
```json
{
  "model": "qwen3.8-omni-flash",
  "messages": [
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "分析这个视频"},
        {
          "type": "video_url",
          "video_url": {"url": "https://example.com/video.mp4"},
          "fps": 2,
          "min_pixels": 65536,
          "max_pixels": 655360
        }
      ]
    }
  ]
}
```

## 限制和注意事项

- **域名迁移强制要求**：旧域名 `dashscope.aliyuncs.com`（中国站）和 `dashscope-intl.aliyuncs.com`（国际站）已逐步淘汰。华北2（北京）、新加坡、中国香港地域必须迁移至业务空间专属域名（见 [OpenAI兼容-Chat](raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md) 和 [DashScope API 参考](raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)）。
- **三方模型地域限制**：DeepSeek（硅基流动直供）、Kimi（月之暗面直供）等三方模型**仅在中国站华北2（北京）地域可用**，且需在百炼控制台开通对应服务（见 [OpenAI兼容-Chat](raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)）。
- **API 路径废弃**：OpenAI Responses 的旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停止维护，必须迁移至 `/compatible-mode/v1/responses`（见 [创建响应](raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）。
- **参数兼容性**：OpenAI Responses API **不支持** `background`（异步执行）等部分 OpenAI 参数；Anthropic 协议**不提供** `/v1/models` 接口，客户端模型发现请求将返回 404（见 [Anthropic兼容-Messages](raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)）。
- **计费与 [Token](../concepts/token.md) 统计**：`usage` 字段中 `input_tokens_details.cached_tokens` 和 `output_tokens_details.reasoning_tokens` 分别统计缓存命中与思考 [Token](../concepts/token.md)，影响计费（见 [获取响应](raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)）。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


