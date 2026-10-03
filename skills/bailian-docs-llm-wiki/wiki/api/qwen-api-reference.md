# qwen api reference

Qwen API Reference 文档汇总了阿里云百炼平台提供的千问系列模型调用方式，涵盖 OpenAI 兼容、Anthropic 兼容及原生 DashScope 三种协议。开发者可根据技术栈和功能需求选择合适接口，所有接口均支持多模态输入（文本、图像、音视频）与结构化输出，并统一通过业务空间专属域名接入。

## 支持的模型/功能

Qwen 系列模型覆盖全场景能力：  
- **文本生成**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash`、`qwen-turbo`、`qwen-coder-next` 等；  
- **多模态理解**：`qwen3.8-omni-flash`（支持音视频端到端理解）、`qwen3-vl-plus`、`qwen-vl-max`、`QVQ`；  
- **数学与代码**：`qwen3-math`、`qwen3-coder-plus`；  
- **第三方直供模型**：DeepSeek（v4 系列）、Kimi（k3/k2.7-code）、GLM（5.3/5.2）、MiniMax（M2.5/M2.1），但需注意[三方直供模型仅在中国站华北2（北京）地域可用](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)，且部分功能受限。  

> **注意**：Qwen-Audio 不支持 OpenAI 兼容协议，仅可通过 [DashScope API](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md) 调用；QwQ 模型不建议设置 `system` 消息，QVQ 模型中 `system` 消息无效 —— 这一限制在 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md) 和 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md) 中一致确认。

功能层面，OpenAI 兼容的 `/responses` 接口提供独特能力：内置联网搜索、网页抓取、代码解释器等工具调用，支持 `previous_response_id` 简化多轮上下文管理，并可通过 `x-dashscope-session-cache: enable` 启用服务端自动缓存；而 Anthropic 兼容接口则支持 `output_config.effort` 控制推理强度、`format.json_schema` 实现强约束结构化输出（[Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)）。

## 关键参数

| 参数 | 类型 | 说明 | 适用接口 |
|------|------|------|----------|
| `model` | `string` | 必填，模型 ID。注意不同协议支持列表存在差异：OpenAI `/chat/completions` 支持更广（含 Qwen-VL、Qwen-Omni、第三方模型），而 `/responses` 仅明确列出 `qwen3.8-*` 等主力型号（见 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）；Anthropic 接口明确区分 Max/Plus/Flash/Turbo/Coder/VL 子系列；DashScope 则按服务类型（`text-generation`/`multimodal-generation`）路由。 | 全部 |
| `messages` / `input` / `content` | `array` | 对话消息数组。OpenAI `/chat/completions` 和 DashScope 使用标准 `role`+`content` 结构；`/responses` 支持扁平 `string` 输入或 `EasyInputMessage` 数组；Anthropic 使用 `role`+`content`（支持 `image`/`video` 块）。多模态内容需按协议指定 `type`（如 `image_url`、`video`、`input_image`）。 | 全部 |
| `max_tokens` | `integer` | 含义因协议而异：OpenAI `/chat/completions` 中为输出 token 上限；`/responses` 中默认为输出上限（思考 token 单独计）；Anthropic 接口中对 `qwen3.8-max` 等模型表示「回复+思考」总上限，对 `glm-5.2` 等则仅限回复（思考由 `thinking.budget_tokens` 控制）—— 此处存在明显语义分歧，开发时须严格对照 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md) 的详细说明。 | OpenAI `/chat`、`/responses`、Anthropic |
| `temperature` | `number` | 采样温度。OpenAI 接口范围 `[0, 2)`；Anthropic 接口明确指出其取值范围 `[0, 2)` 与官方 `[0.0, 1.0]` 不同，迁移时需校准。 | OpenAI、Anthropic |
| `fps`, `min_pixels`, `max_pixels`, `total_pixels`, `max_frames` | `number` | 视频/图像预处理参数。`fps` 和 `min/max_pixels` 在 OpenAI `/chat/completions` 与 DashScope 中定义一致；`total_pixels` 为 `/chat/completions` 独有（控制总帧像素）；`max_frames` 为 DashScope 独有（控制抽帧数上限）。 | OpenAI `/chat/completions`、DashScope |

## 使用方式

### 接入地址（Base URL）
所有接口均使用业务空间专属域名，格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com`，其中 `{WorkspaceId}` 需替换为控制台获取的真实 ID。各协议路径如下：

- **OpenAI 兼容**：
  - Chat：`/compatible-mode/v1/chat/completions`（[OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)）
  - Responses：`/compatible-mode/v1/responses`（[创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)），**旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停用**。
- **Anthropic 兼容**：`/apps/anthropic/v1/messages`（[Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)）
- **DashScope 原生**：
  - 文本模型：`/api/v1/services/aigc/text-generation/generation`
  - 多模态模型：`/api/v1/services/aigc/multimodal-generation/generation`（[DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)）

SDK 配置示例（Python）：
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

### 认证
统一使用百炼 API Key，通过 `Authorization: Bearer <API_KEY>` 或 `x-api-key: <API_KEY>`（Anthropic 接口支持后者）传入。

## 限制和注意事项

- **地域与模型绑定**：第三方直供模型（如 SiliconFlow DeepSeek、月之暗面 Kimi）**仅在中国站华北2（北京）地域可用**，且需在控制台手动开通服务（[OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)）。
- **协议能力差异**：
  - `/chat/completions` 不支持 `Qwen-Audio` 和 `tool calls`；
  - `/responses` 支持工具调用但**不支持异步 `background` 参数**（固定同步）；
  - Anthropic 接口**不提供 `/v1/models` 列表接口**，客户端模型发现请求将返回 404。
- **参数兼容性**：`vl_high_resolution_images` 仅 DashScope 和 Anthropic 接口支持，[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)无此参数；`max_frames` 为 DashScope 独有，OpenAI 接口通过 `total_pixels` + `fps` 组合控制视频处理规模。
- **缓存与存储**：`/responses` 接口的 `store` 参数控制响应是否可被 `previous_response_id` 引用；`x-dashscope-session-cache: enable` 请求头启用服务端对话缓存，二者独立生效。
- **错误处理**：`GET /responses/{id}` 和 `GET /responses/{id}/input_items` 仅当 `store=true` 时返回的 `response_id` 才有效，否则返回 `Response with id 'resp_xxx' not found.` 错误（[获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)、[获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)）。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


