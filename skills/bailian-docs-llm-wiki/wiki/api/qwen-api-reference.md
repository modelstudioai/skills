# qwen api reference

阿里云百炼平台提供多种 API 协议兼容的 Qwen 模型调用方式，包括 OpenAI 兼容、Anthropic 兼容和原生 DashScope 协议。开发者可根据现有技术栈选择最适配的接口，所有协议均支持主流 Qwen 系列模型（如 `qwen4-max`、`qwen3.8-max`、`qwen3.7-plus` 等）及多模态能力（图像、视频、音频、PDF），并统一通过业务空间专属域名接入，保障性能与稳定性。

## 支持的模型/功能

- **核心模型**：`qwen4-max`、`qwen3.8-max`、`qwen3.7-plus`、`qwen3.8-flash`、`qwen3-vl-plus`、`qwen3-coder-flash`、`qwen3.5-ocr` 等商业版与开源版模型；第三方直供模型（如 `deepseek-v4.1-flash`、`kimi-k3.1-pro`、`glm-5.3`）仅在华北2（北京）地域可用，且需在控制台开通服务 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
- **多模态输入**：支持文本、图像（URL/Base64）、视频（文件/帧列表）、音频（`qwen3.8-omni-flash`）、PDF（`qwen4-max`/`qwen3.8-flash`）等格式，各模型支持范围详见具体文档。
- **高级功能**：
  - 内置工具链：联网搜索、网页抽取、代码解释器、文搜图、图搜图、知识库检索（仅 [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md) 支持）；
  - 显式缓存：`qwen4-max` 支持 `prompt_cache_breakpoint` 和 `cache_control` 标记断点 [显式缓存（Qwen4）](../../raw/model-user-guide/model-experience/text-generation-model/explicit-cache-qwen4.md)；
  - 深度思考：通过 `reasoning.effort`（Responses）或 `thinking.type`（Anthropic）控制推理强度；
  - Session 缓存：通过请求头 `x-dashscope-session-cache: enable` 自动管理多轮对话上下文。

> **注意**：Qwen-Audio 不支持 OpenAI 兼容协议，仅支持 DashScope 协议；QwQ 模型不建议设置 System Message，QVQ 模型的 System Message 不生效 —— 此矛盾信息在 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md) 和 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md) 中重复出现，属平台统一行为，非文档错误。

## 关键参数

| 参数 | 作用 | 适用协议 | 说明 |
|------|------|----------|------|
| `model` | 指定模型 ID | 全部 | 必选；值必须为控制台已开通且支持该协议的模型，例如 `qwen3.7-plus`；三方模型需单独开通 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。 |
| `messages` / `input` | 输入内容 | Chat/Responses | `messages`（Chat/DashScope）为标准消息数组；`input`（Responses）支持 string 或 array，更灵活，且支持 `previous_response_id` 简化多轮管理。 |
| `max_tokens` | 输出长度上限 | Anthropic | 必选；对 `qwen4-max`/`deepseek-v4` 等模型，限制“回复+思考”总 token；对其他模型仅限回复长度 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。 |
| `temperature` | 生成随机性 | 全部 | 取值范围 `[0, 2)`，**注意** Anthropic 官方为 `[0.0, 1.0]`，迁移时需校准 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。 |
| `detail` / `min_pixels` / `max_pixels` | 图像/视频精度控制 | Chat/DashScope | 控制多模态输入分辨率与 Token 消耗；`detail`（`high`/`low`）为快捷配置，`min_pixels`/`max_pixels` 提供精确像素阈值 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。 |
| `store` | 响应持久化 | Responses | `true` 时返回可被 `retrieve`/`delete`/`list-input-items` 操作的 `response_id` [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。 |

## 使用方式

- **接入地址**：全部协议均推荐使用**业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），替换 `{WorkspaceId}` 为控制台获取的真实 ID；旧域名（如 `dashscope.aliyuncs.com`）仍可用但不推荐 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
- **认证**：通过 `Authorization: Bearer <API_KEY>` 或 `x-api-key`（Anthropic 协议）传入百炼 API Key，需提前[获取与配置](../../raw/model-api-reference/preparations/get-api-key.md)。
- **SDK 配置示例**：
  - OpenAI SDK：`base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"`；
  - DashScope SDK：`workspace="{WorkspaceId}", region="cn-beijing"`；
  - Anthropic SDK：`base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic"`。
- **协议选型建议**：
  - 已有 OpenAI 生态：优先用 `/compatible-mode/v1/chat/completions`（基础对话）或 `/compatible-mode/v1/responses`（需内置工具/多轮简化）；
  - 已有 Anthropic 生态：用 `/apps/anthropic/v1/messages`；
  - 需最大灵活性或使用 `qwen-audio`：用 DashScope 原生 `/api/v1/services/aigc/.../generation`。

## 限制和注意事项

- **地域限制**：第三方直供模型（DeepSeek/Kimi/GLM/MiniMax）仅在中国站华北2（北京）地域可用，且需在控制台手动开通对应服务 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
- **路径弃用**：OpenAI 兼容-Responses 的旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停止维护，必须迁移到 `/compatible-mode/v1/responses` [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **上下文截断**：Responses API 为预留工具调用空间，自动将输入上下文截断至模型窗口的约 80%，不报错 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **异步能力**：当前百炼所有 API 均为同步调用，`background` 参数被忽略 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **单位差异**：`created_at` 字段在 Responses API 的 `list-input-items` 接口返回毫秒级时间戳，而 `create`/`retrieve` 接口返回秒级，集成时需注意转换 [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)。

## 来源文档

- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


