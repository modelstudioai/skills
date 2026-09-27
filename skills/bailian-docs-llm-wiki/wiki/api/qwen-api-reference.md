# qwen api reference

阿里云百炼平台提供多种 API 接口调用 Qwen 系列大模型，包括 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)、Anthropic 兼容接口和原生 DashScope 接口。开发者可根据现有技术栈选择适配路径，所有接口均支持文本、多模态（图像/视频/音频）及工具调用能力，并统一通过业务空间专属域名接入，以保障性能与稳定性。

## 支持的模型/功能

Qwen API 支持全系列千问模型及主流第三方模型，按能力分为以下几类：

- **文本生成模型**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash`、`qwen-turbo`、`qwen-coder-next` 等；
- **多模态模型**：`qwen3.8-omni-flash`（音视频理解）、`qwen3-vl-plus`、`qwen-vl-max`、`qwen3.7-vl`、`QVQ`、`QwQ`；
- **专用模型**：`qwen3-math`（数学推理）、`qwen3-audio`（仅 DashScope 协议支持，[详见文档](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)）；
- **第三方直供模型**：DeepSeek（v4 系列）、Kimi（k3/k2.7-code）、GLM（5.x 系列）、MiniMax（M2.5/M3）等，其中三方模型**仅在中国站华北2（北京）地域可用**，且需在控制台开通对应服务 [原文标题](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。

功能层面，除基础文本生成外，各接口差异化支持：
- `OpenAI兼容-Chat`：标准 `chat/completions` 流式交互，支持 `messages` 数组输入；
- `OpenAI兼容-Responses`：增强型对话 API，内置联网搜索、网页抓取、代码解释器等工具，支持 `previous_response_id` 多轮上下文管理与 `x-dashscope-session-cache` 自动缓存 [原文标题](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)；
- `Anthropic兼容-Messages`：支持 `system` 字段、结构化输出（`output_config.format.json_schema`）及深度思考（`thinking.effort`），但**不提供 `/v1/models` 列表接口**；
- `DashScope原生API`：最底层协议，区分 `text-generation` 与 `multimodal-generation` 路径，支持 `max_frames` 等细粒度视频参数，是 `qwen3-audio` 唯一支持协议 [原文标题](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)。

> **注意**：Qwen-Audio 模型**不支持 OpenAI 兼容协议**，仅可通过 DashScope API 调用；同时，`OpenAI兼容-Responses` 的旧版路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停止维护，必须迁移至 `/compatible-mode/v1/responses`。

## 关键参数

| 参数 | 类型 | 说明 | 所属接口 |
|------|------|------|----------|
| `model` | `string` | 必填。模型 ID，如 `qwen3.8-max`、`qwen3-vl-plus`。不同接口支持列表略有差异，详见各文档模型章节 | 全部 |
| `messages` / `input` / `system` | `array` / `string` | 对话上下文。`Chat` 和 `DashScope` 使用 `messages`；`Responses` 支持 `string` 或 `array` 格式的 `input`；`Anthropic` 使用 `system` + `messages` 分离设计 | 各接口独立 |
| `stream` | `boolean` | 是否流式响应，默认 `false` | 全部 |
| `temperature` | `float` | 采样温度，取值范围 `[0, 2)`。**注意**：Anthropic 兼容接口此范围与官方 `[0.0, 1.0]` 不同 [原文标题](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md) | Chat / Responses / Anthropic |
| `max_tokens` | `integer` | 输出长度上限。**关键差异**：对 `qwen3.8-max`/`deepseek-v4` 等模型，该值限制「回复+思考」总 [Token](../concepts/token.md)；对其他模型仅限回复部分 | Chat / Anthropic / DashScope |
| `reasoning.effort` / `output_config.effort` | `string` | 控制思考强度。`Responses` 接口用 `reasoning.effort`（如 `high`）；`Anthropic` 接口用 `output_config.effort`（如 `xhigh`）；`thinking.budget_tokens` 已废弃 | Responses / Anthropic |
| `min_pixels` / `max_pixels` / `total_pixels` | `integer` | 图像/视频分辨率控制参数，用于缩放与抽帧。`DashScope` 支持 `max_frames`，而 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)不支持自定义该参数 | Chat / DashScope |

## 使用方式

### 1. 基础接入
所有接口均需：
- 替换 `{WorkspaceId}` 为真实业务空间 ID（控制台查看）；
- 配置 `DASHSCOPE_API_KEY`（环境变量或请求头 `Authorization: Bearer <key>`）；
- **强烈建议迁移至业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但新域名提供更高性能与稳定性 [原文标题](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。

### 2. 接口选择指南
| 场景 | 推荐接口 | 说明 |
|------|----------|------|
| 快速迁移 OpenAI 应用 | `OpenAI兼容-Chat` | 最小改动，标准 `chat/completions` 路径，适合纯文本/简单多模态 |
| 需要 Agent 能力（搜索/代码执行） | `OpenAI兼容-Responses` | 内置工具链，支持 `previous_response_id` 多轮管理，`store=true` 后可调用 `GET /responses/{id}` 查询历史 [原文标题](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md) |
| 迁移 Anthropic 应用 | `Anthropic兼容-Messages` | 支持 `system` 提示、结构化 JSON 输出（`output_config.format.json_schema`）及显式思考控制 |
| 需精细控制视频帧数或使用 Audio 模型 | `DashScope原生API` | 唯一支持 `qwen3-audio` 和 `max_frames` 参数的协议 |

### 3. 多模态输入示例（通用）
```json
{
  "messages": [
    {
      "role": "user",
      "content": [
        { "type": "text", "text": "描述这张图" },
        { 
          "type": "image_url", 
          "image_url": { "url": "https://xxx.jpg" } 
        }
      ]
    }
  ]
}
```
> 视频支持 `video_url`（文件）或 `video`（图像列表），`fps` 参数控制抽帧频率，`min_pixels`/`max_pixels` 控制分辨率。

## 限制和注意事项

- **地域限制**：三方模型（DeepSeek/Kimi/GLM/MiniMax）仅支持华北2（北京）地域，调用前须在控制台开通服务；
- **协议限制**：`Qwen-Audio` 仅支持 DashScope 协议，不兼容 OpenAI 接口；
- **路径废弃**：`OpenAI兼容-Responses` 旧路径 `/api/v2/.../responses` 已停用，必须使用 `/compatible-mode/v1/responses`；
- **参数兼容性**：[OpenAI 兼容接口](../concepts/openai-compatible-api.md)**忽略所有未明确文档列出的参数**（如 `background` 异步参数不支持）；
- **上下文截断**：`Responses` API 为预留工具调用空间，最大输入上下文约为模型窗口的 80%，超出部分自动截断（不报错）；
- **[Token](../concepts/token.md) 计费差异**：`Responses` 接口返回的 `usage.output_tokens_details.reasoning_tokens` 明确分离思考 [Token](../concepts/token.md)，按实际消耗计费；`Anthropic` 接口的 `thinking.budget_tokens` 参数已废弃，应改用 `output_config.effort`；
- **缓存行为**：`x-dashscope-session-cache: enable` 仅作用于 `Responses` 接口；`Anthropic` 接口需通过 `cache_control: {type: "ephemeral"}` 显式标记缓存断点。

## 来源文档

- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


