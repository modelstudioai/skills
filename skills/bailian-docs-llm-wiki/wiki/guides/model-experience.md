# model experience

`model experience` 是百炼平台统一的模型调用抽象层，为开发者提供一致的 API 接口与参数语义，屏蔽底层模型类型（文本、视觉、语音等）和部署形态（托管/自定义）的差异。所有模型能力均通过 `/v1/models/{model_id}/invoke` 统一入口接入，支持同步响应与[流式输出](../concepts/streaming-output.md)。该设计已在 [模型调用](../../raw/model-user-guide/model-experience.md) 文档中明确规范。

## 支持的模型与功能

当前 `model experience` 覆盖以下模态能力：
- **文本生成**：包括大语言模型（LLM）的对话、补全、结构化输出等，详见 [文本](../../raw/model-user-guide/model-experience/text-generation-model.md)  
- **视觉生成**：图像生成、编辑、理解及视频生成，详见 [视觉](../../raw/model-user-guide/model-experience/image-and-video-generation.md)  
- **语音与音频**：TTS、ASR、音色克隆与音频理解，详见 [语音](../../raw/model-user-guide/model-experience/speech-and-audio.md)  
- **向量服务**：嵌入（embedding）与重排序（rerank），详见 [向量](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)  
- **全模态模型**：支持跨文本、图像、语音输入的联合推理，详见 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md)  

> **注意**：部分旧版文档（如 `raw/legacy/llm-api.md`）仍将 `text-generation` 作为独立路径调用，该方式已废弃；请以 [模型调用](../../raw/model-user-guide/model-experience.md) 中定义的统一 `/v1/models/{model_id}/invoke` 为准。

## 关键参数

所有调用共用以下核心参数（JSON body）：
- `model_id`（必填）：平台注册的模型唯一标识，非模型原始名称（如 `qwen2.5-7b-chat` 而非 `Qwen2.5-7B-Chat`）  
- `input`（必填）：模态特定输入结构，例如文本为 `{"messages": [...]}`，图像为 `{"image_url": "..."}`  
- `parameters`（可选）：标准化参数集，含 `temperature`、`top_p`、`max_tokens`（文本/语音）、`n`（采样数）、`stream`（布尔值）等  
- `tools`（可选）：用于[函数调用](../concepts/function-calling.md)（Function Calling）场景，格式与 OpenAI 兼容  

参数语义严格遵循 [模型调用](../../raw/model-user-guide/model-experience.md) 定义，不因模型类型而异。

## 使用方式

1. **认证**：使用 `Authorization: Bearer <api_key>` 请求头  
2. **请求**：`POST https://dashscope.aliyuncs.com/v1/models/{model_id}/invoke`  
3. **响应**：成功时返回 `200 OK`，结构统一为 `{ "output": {...}, "usage": {...} }`；流式响应使用 `Content-Type: text/event-stream`，事件格式为 `data: {...}\n\n`  
4. **SDK 支持**：Python SDK v1.20+、Java SDK v1.15+ 原生适配 `model experience` 接口，无需额外封装  

## 限制和注意事项

- 单次请求 `input` 总大小上限为 16 MB（含 base64 图像、音频二进制等）  
- 流式响应仅支持文本、语音 TTS 及部分全模态模型；图像生成暂不支持流式（见 [视觉](../../raw/model-user-guide/model-experience/image-and-video-generation.md)）  
- `model_id` 必须通过 [模型调用](../../raw/model-user-guide/model-experience.md) 中的「模型列表 API」或控制台获取，硬编码模型名将导致 `404 Not Found`  
- 向量模型（embedding/rerank）不接受 `temperature` 或 `stream` 参数，传入将被静默忽略 —— 此行为与 [向量](../../raw/model-user-guide/model-experience/embedding-rerank-model.md) 文档一致，但与部分早期测试文档冲突，以本页为准

## 来源文档

- [模型调用](../../raw/model-user-guide/model-experience.md)


