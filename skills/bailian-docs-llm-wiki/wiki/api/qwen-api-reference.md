# qwen api reference

阿里云百炼平台提供多种兼容主流协议的 API 接口，用于调用 Qwen 系列大模型（含文本、[多模态](../concepts/multimodal.md)、代码、数学等）及第三方直供模型。核心接口包括 OpenAI 兼容的 Chat 和 Responses API、Anthropic 兼容的 Messages API，以及原生 DashScope API。所有接口均支持多地域部署，并推荐使用业务空间专属域名以获得更优性能与稳定性。

## 支持的模型/功能

Qwen API 支持全系列千问模型及主流第三方模型，按协议能力划分如下：

- **OpenAI 兼容 Chat API**（[OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)）：支持 `qwen3.8-max`、`qwen3.7-plus`、`qwen-vl-plus`、`qwen-coder-next`、`qwen-math`、`qwen-omni` 等商业版与开源版模型；同时支持 DeepSeek（硅基流动/快手万擎）、Kimi（月之暗面）、GLM、MiniMax 等三方直供模型（仅限华北2北京地域）。**注意**：Qwen-Audio 不支持该协议，仅支持 DashScope 协议。

- **OpenAI 兼容 Responses API**（[创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）：专为复杂 Agent 场景设计，内置联网搜索、网页抓取、代码解释器、文搜图、知识库搜索等工具。支持 `qwen3.8-max`、`qwen3.7-flash`、`qwen3.5-plus` 及 `deepseek-v4-pro`、`glm-5.3` 等模型，但非列表中模型仅支持基础文本生成，Agent 能力受限。

- **Anthropic 兼容 Messages API**（[Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)）：支持结构化输出（JSON Schema）、深度思考（`output_config.effort`）、显式缓存（`cache_control`）等高级能力。覆盖 `qwen3.8-max`、`qwen3-vl-flash`、`kimi-k3`、`glm-5.2` 等模型，但 `temperature` 取值范围为 `[0, 2)`，与 Anthropic 官方 `[0.0, 1.0]` 不同。

- **DashScope 原生 API**（[DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)）：最底层协议，区分纯文本（`text-generation`）与[多模态](../concepts/multimodal.md)（`multimodal-generation`）服务端点。支持 `qwen-audio`、`qwen3.7-plus`、`qwen3-vl-plus` 等全量模型，且提供 `max_frames` 等 DashScope 特有参数。

> **注意**：文档 1 与文档 8 对 `min_pixels`/`max_pixels` 的默认值描述存在细微差异（如 `qwen-vl-plus` 图像输入默认值，文档 1 写为 `4096`，文档 8 写为 `4096`，一致；但文档 1 中 `Qwen2.5-VL` 视频输入默认值为 `50176`，文档 8 同样为 `50176`，无矛盾。经核查，两文档在关键参数上实际一致，无需修正）。

## 关键参数

| 参数 | 适用协议 | 说明 | 示例值 |
|------|----------|------|--------|
| `model` | 全部 | 必填，模型 ID。需与所选协议支持列表严格匹配 | `"qwen3.8-max"`, `"qwen3-vl-plus"` |
| `messages` / `input` | Chat / Responses | 对话上下文数组或字符串输入。Responses 支持 `string` 或 `array`，Chat 仅支持 `array` | `[{"role":"user","content":"你好"}]` |
| `stream` | 全部 | 是否启用流式响应，默认 `false` | `true` |
| `temperature` | Chat / Anthropic / DashScope | 控制输出随机性，取值 `[0, 2)` | `0.7` |
| `max_tokens` | Anthropic / DashScope | 输出长度上限（具体含义因模型而异，详见各协议文档） | `2048` |
| `fps` | Chat / DashScope（视频输入） | 视频抽帧频率，范围 `[0.1, 10]`，默认 `2.0` | `3.0` |
| `min_pixels` / `max_pixels` | Chat / DashScope（图像/视频） | 输入分辨率控制参数，单位为总像素数 | `min_pixels: 65536`, `max_pixels: 8388608` |
| `tools` | Responses / Anthropic | 工具定义数组，用于 Function Call | `[{"type": "web_search"}]` |
| `output_config.effort` | Anthropic | 控制思考强度，取值如 `"xhigh"`（qwen3.8）、`"max"`（glm-5.3） | `"xhigh"` |

## 使用方式

### 1. 基础配置
- 替换 `{WorkspaceId}` 为真实业务空间 ID（见 [业务空间ID获取](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)）。
- 使用推荐的业务空间专属域名（如华北2：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），**不建议继续使用旧域名 `dashscope.aliyuncs.com`**。
- 配置 API Key（见 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)）。

### 2. 协议选择指南
- **快速迁移 OpenAI 应用** → 优先选用 **Chat API**（路径 `/compatible-mode/v1/chat/completions`），兼容性最高。
- **构建智能体（Agent）** → 选用 **Responses API**（路径 `/compatible-mode/v1/responses`），利用其内置工具链与 `previous_response_id` 上下文管理。
- **需要结构化 JSON 输出或深度思考** → 选用 **Anthropic Messages API**（路径 `/apps/anthropic/v1/messages`）。
- **需要最大灵活性或调用 `qwen-audio` 等特殊模型** → 选用 **DashScope 原生 API**（路径 `/api/v1/services/aigc/.../generation`）。

### 3. SDK 调用示例（Python）
```python
# OpenAI SDK（Chat API）
from openai import OpenAI
client = OpenAI(
    api_key="sk-xxx",
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
response = client.chat.completions.create(model="qwen3.8-max", messages=[{"role":"user","content":"你好"}])

# OpenAI SDK（Responses API）
response = client.responses.create(model="qwen3.8-max", input="你好")

# Anthropic SDK（Messages API）
import anthropic
client = anthropic.Anthropic(
    api_key="sk-xxx",
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic"
)
message = client.messages.create(model="qwen3.8-max", max_tokens=1024, messages=[{"role":"user","content":"你好"}])
```

## 限制和注意事项

- **地域可用性**：三方直供模型（如 DeepSeek、Kimi）**仅在中国站华北2（北京）地域可用**，调用前需在百炼控制台开通对应服务。
- **API 路径弃用**：Responses API 的旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停止维护，请立即迁移至 `/compatible-mode/v1/responses`（见 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）。
- **上下文截断**：Responses API 为预留工具调用空间，最大输入上下文约为模型窗口的 80%，超出部分将自动截断（不报错）。
- **缓存行为**：`vl_high_resolution_images=True` 时，`max_pixels` 参数失效，图像最大像素固定为 `16777216`（Qwen3 系列）或 `12845056`（Qwen2.5-VL/QVQ）。
- **音频/视频支持**：`qwen3.8-omni-flash` 是目前唯一支持 `input_audio` 和 `input_video` 类型的 Responses 模型；Qwen-Audio 仅支持 DashScope 协议。
- **计费说明**：`reasoning_tokens`（思考 [Token](../concepts/token.md)）计入 `output_tokens_details.reasoning_tokens`，按推理 [Token](../concepts/token.md) 单独计费；`cached_tokens`（缓存命中 [Token](../concepts/token.md)）在 `usage.input_tokens_details.cached_tokens` 中返回。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


