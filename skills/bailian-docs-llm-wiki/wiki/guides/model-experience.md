# model experience

`model experience` 是百炼平台统一的模型调用抽象层，为开发者提供一致的 API 接口与参数语义，屏蔽底层模型类型（文本、视觉、语音等）和部署形态（托管/自定义/混合）的差异。它支持同步推理、流式响应、批量请求及上下文管理，适用于从原型验证到生产部署的全周期场景。所有能力均通过 `/v1/models/{model_id}/invoke` 统一端点接入。

## 支持的模型与功能

当前 `model experience` 覆盖以下模态能力，各模态对应独立的子文档说明：
- 文本生成：支持大语言模型（LLM）的 [prompt](prompt.md) completion、function calling、tool use 等 [文本](../../raw/model-user-guide/model-experience/text-generation-model.md)  
- 视觉生成：支持图像/视频生成、编辑、理解任务，含多轮视觉对话支持 [视觉](../../raw/model-user-guide/model-experience/image-and-video-generation.md)  
- 语音处理：涵盖 TTS、ASR、语音转写与音色克隆，需注意采样率与格式约束 [语音](../../raw/model-user-guide/model-experience/speech-and-audio.md)  
- 向量服务：提供 embedding 生成与重排序（rerank），适用于检索增强场景 [向量](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)  
- 全模态：支持图文音多模态联合输入与输出，需显式声明 `input_modality` 参数 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md)

> **注意**：`omni-modal` 文档中描述的 `input_modality: ["text", "image"]` 自动推断逻辑，与 `text-generation-model.md` 中明确要求 `input_modality` 必填存在不一致；实际调用时请始终显式指定该字段，以避免 400 错误。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | 是 | 平台注册的模型唯一标识，如 `qwen2.5-7b-chat` 或 `wanx-v1` |
| `input` | object | 是 | 模态感知输入结构，详见各模态子文档 [文本](../../raw/model-user-guide/model-experience/text-generation-model.md) |
| `parameters` | object | 否 | 模型级超参，如 `temperature`, `top_p`, `max_tokens`；部分模态支持 `stream: true` |
| `request_id` | string | 否 | 用于链路追踪的客户端透传 ID，建议在生产环境设置 |

## 使用方式

1. **认证**：使用 `Authorization: Bearer <api_key>` 请求头  
2. **请求体**：POST `/v1/models/{model_id}/invoke`，`Content-Type: application/json`  
3. **流式响应**：当 `parameters.stream = true` 时，返回 `text/event-stream`，按 SSE 协议解析 chunk（仅文本与全模态支持）  
4. **错误处理**：关注 HTTP 状态码（如 `429` 表示限流）、`error.code`（如 `"InvalidInput"`）及 `error.message` 字段  

## 限制和注意事项

- 单次请求 `input` 总大小上限为 16 MB（语音/视频文件经 base64 编码后计入）  
- 流式响应不支持 `rerank` 和 `embedding` 类模型，调用时若误设 `stream: true` 将返回 `400 Bad Request`  
- 多模态输入中，图像需为 JPEG/PNG 格式且单边分辨率 ≤ 2048px；视频仅支持 MP4（H.264）且时长 ≤ 10s —— 具体约束见 [视觉](../../raw/model-user-guide/model-experience/image-and-video-generation.md)  
- 所有模型调用默认启用缓存（基于 `input` + `parameters` 哈希），如需禁用，请在 `parameters` 中添加 `"cache_enabled": false`

## 来源文档

- [模型调用](../../raw/model-user-guide/model-experience.md)


