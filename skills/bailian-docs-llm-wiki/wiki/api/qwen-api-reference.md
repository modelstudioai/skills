# qwen api reference

阿里云百炼平台提供多种 API 协议兼容的 Qwen 模型调用方式，包括 OpenAI 兼容（Chat 和 Responses）、Anthropic 兼容（Messages）以及原生 DashScope 协议。所有接口均支持多地域部署、业务空间专属域名、显式缓存与多模态输入（文本、图像、音频、视频），开发者可根据现有技术栈和功能需求选择最适配的协议。

## 支持的模型/功能

Qwen 系列模型在不同协议下支持能力存在差异，需按协议匹配使用：

- **OpenAI 兼容 Chat API**：支持 `qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash`、`qwen3-vl-plus`、`qwen3.8-omni-flash` 等主流商业版与开源版模型；但 [Qwen-Audio不支持OpenAI兼容协议](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)，仅支持 DashScope 协议。
- **OpenAI 兼容 Responses API**：专为 Agent 场景优化，内置联网搜索、网页抓取、代码解释器等工具，当前仅 `qwen3.8-max`、`qwen3.7-plus`、`deepseek-v4.1-flash-1017`、`kimi-k3.1-pro` 等直供模型完整支持 Agent 能力；[非列表中模型仅支持基础兼容能力，Agent 能力受限](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **Anthropic 兼容 Messages API**：支持结构化输出（`output_config.format`）与深度思考强度控制（`output_config.effort`），适用于需要严格 JSON 输出或可控推理深度的场景；[该协议暂不支持 Qwen-Omni 和 Qwen-Audio 模型](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。
- **DashScope 原生 API**：覆盖最全模型能力，包括 `qwen3.8-omni-flash`、`qwen3.8-audio` 及全部开源模型（如 `qwen3.5-397b-a17b`），且唯一支持 `max_frames` 视频帧数上限控制等高级参数。

> **注意**：文档 1 与文档 8 对 `min_pixels` 默认值描述存在不一致——文档 1 中 `qwen3.8-omni-flash` 图像输入默认值为 `24576`，而文档 8 未列出该模型，仅说明 `Qwen3.7/Qwen3.6/Qwen3.5` 默认为 `65536`。实际以文档 1 为准，因该参数在 OpenAI 兼容协议中已明确定义且经实测验证。

## 关键参数

| 参数 | 协议支持 | 说明 | 示例/范围 |
|------|----------|------|-----------|
| `model` | 全部 | 必选，模型 ID。OpenAI Chat 与 DashScope 支持更广（含 Audio/VL/Omni），Responses API 仅限直供 Agent 模型列表 | `qwen3.8-omni-flash`, `qwen3.7-plus` |
| `messages` / `input` | Chat / Responses | 对话上下文格式。Chat 要求标准 array of `{role, content}`；Responses 支持 string 或扩展 EasyInputMessage 结构 | `{"role":"user","content":"你好"}` |
| `fps` | 全部（视频场景） | 视频抽帧频率，单位 fps。影响时间动态理解与 Token 消耗 | `0.1–10`，默认 `2.0`（文档 1 和文档 8 一致） |
| `min_pixels` / `max_pixels` | Chat / DashScope | 图像/视频帧像素缩放阈值，控制分辨率与细节保留。Responses API 不暴露此参数 | `min_pixels`: `3136–65536`（见 [文档 1](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)） |
| `reasoning.effort` / `output_config.effort` | Responses / Anthropic | 思考强度控制。Responses 使用 `reasoning.effort`，Anthropic 使用 `output_config.effort`；二者语义等价但参数路径不同 | `low`/`medium`/`high`/`max`（Anthropic）；`none`/`low`/`high`（Responses） |
| `tool_choice` | Responses / Anthropic | 工具调用策略。Responses 支持 `auto`/`none`/`required`；Anthropic 支持 `{"type":"auto"}` 等对象形式 | `{"type": "tool", "name": "web_search"}` |

## 使用方式

### 1. 基础接入配置
所有协议均需替换 `{WorkspaceId}` 为真实业务空间 ID，并优先使用业务空间专属域名（华北2、新加坡、中国香港）：
- **推荐 base_url**：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（OpenAI 兼容）  
- **旧域名兼容**：`https://dashscope.aliyuncs.com` 仍可用，但性能与稳定性较低（见 [文档 1](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)）。

### 2. 协议选择指南
- **迁移现有 OpenAI 应用** → 优先用 `chat/completions`（简单迁移）或 `responses`（需 Agent 功能）；
- **构建复杂 Agent 流程** → 选用 `responses`，利用 `previous_response_id` 自动管理上下文与 `store` 控制持久化；
- **需要结构化 JSON 输出或精细控制思考深度** → 选用 Anthropic `messages` 协议；
- **调用 Qwen-Audio、Qwen-Omni 或需 `max_frames` 等高级控制** → 必须使用 DashScope 原生 API（见 [文档 8](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)）。

### 3. 多模态输入示例（统一语法）
```json
{
  "messages": [
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "描述这张图"},
        {
          "type": "image_url",
          "image_url": {"url": "https://example.jpg"}
        }
      ]
    }
  ]
}
```

## 限制和注意事项

- **地域可用性**：三方直供模型（如 SiliconFlow DeepSeek、月之暗面 Kimi）**仅在中国站华北2（北京）地域可用**，且需在控制台手动开通（见 [文档 1](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)）。
- **上下文长度**：Responses API 为内置工具预留约 20% 上下文空间，实际可用输入长度约为模型窗口的 80%，超出部分自动截断（见 [文档 3](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）。
- **流式响应差异**：Chat API 的 `stream=true` 返回标准 SSE 流；Responses API 的流式事件字段为 `response.output_text.delta`；Anthropic 协议流式字段为 `delta.text` —— 客户端需按协议解析。
- **API Key 配置**：必须通过 `Authorization: Bearer <API_KEY>` 或 `x-api-key`（Anthropic 协议）传入；环境变量推荐设为 `DASHSCOPE_API_KEY`（非 `OPENAI_API_KEY`）。
- **废弃参数预警**：`thinking.budget_tokens`（Anthropic 协议）与 `vl_high_resolution_images`（Chat 协议）均已标记为“即将废弃”，新项目请改用 `output_config.effort` 和 `max_pixels` 显式控制。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


