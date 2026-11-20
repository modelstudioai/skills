# model experience

`model experience` 是百炼平台统一的模型调用抽象层，为开发者提供一致的 API 接口与请求结构，屏蔽底层模型类型与部署细节。它支持文本生成、视觉理解与生成、语音处理、向量嵌入/重排及全模态融合等能力。所有调用均通过 `POST /v1/models/{model_id}/invoke` 接口发起，遵循标准的 JSON-RPC 风格请求体。

## 支持的模型与功能

当前 `model experience` 覆盖以下五大类模型能力：

- **文本生成**：包括大语言模型（LLM）的对话、补全、指令遵循等，详见 [文本](../../raw/model-user-guide/model-experience/text-generation-model.md)  
- **视觉**：支持图像理解（VQA）、图像生成、视频理解与生成，详见 [视觉](../../raw/model-user-guide/model-experience/image-and-video-generation.md)  
- **语音**：涵盖语音识别（ASR）、语音合成（TTS）、音频理解与生成，详见 [语音](../../raw/model-user-guide/model-experience/speech-and-audio.md)  
- **向量**：提供文本嵌入（embedding）与跨文档重排（rerank）服务，详见 [向量](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)  
- **全模态**：支持图文音多模态联合输入与输出，如“上传图片+语音描述→生成带注释的视频”，详见 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md)

> **注意**：部分全模态模型暂不支持流式响应（`stream: true`），而文本与语音模型普遍支持；该差异在 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md) 文档中未明确说明，但已在 [文本](../../raw/model-user-guide/model-experience/text-generation-model.md) 和 [语音](../../raw/model-user-guide/model-experience/speech-and-audio.md) 的最新版本中确认。

## 关键参数

所有 `model experience` 请求共用以下核心字段（位于 `request_body` 顶层）：

- `model_id`（必填）：模型唯一标识，如 `qwen2.5-7b-chat` 或 `wanx-vl-3.0`  
- `input`（必填）：模型输入数据，结构因模态而异（如文本为 `{"messages": [...]}`，图像为 `{"image_url": "..."}`）  
- `parameters`（可选）：控制生成行为，通用参数包括 `temperature`、`top_p`、`max_tokens`；模态特有参数见各子文档  
- `stream`（布尔值，默认 `false`）：是否启用流式响应；仅部分模型支持，启用后需按 SSE 协议解析  

## 使用方式

1. 构造标准 HTTP POST 请求，目标 URL：`https://dashscope.aliyuncs.com/v1/models/{model_id}/invoke`  
2. 设置 Header：`Authorization: Bearer <api_key>`，`Content-Type: application/json`  
3. 在 Body 中传入符合模态规范的 `input` 与可选 `parameters`  
4. 解析响应：成功时返回 `200 OK`，结构为 `{ "output": {...}, "usage": {...} }`；流式响应以 `text/event-stream` 返回多个 `data: {...}` 块  

示例（文本生成）：
```json
{
  "model_id": "qwen2.5-7b-chat",
  "input": {
    "messages": [{"role": "user", "content": "你好"}]
  },
  "parameters": {"temperature": 0.7}
}
```

## 限制和注意事项

- 单次请求 `input` 总大小上限为 20 MB（含 Base64 编码图像/音频），超出将返回 `413 Payload Too Large`  
- 全模态模型对输入格式校验更严格，例如同时传入 `image_url` 和 `audio_url` 时，必须确保二者语义可对齐，否则返回 `400 Invalid Input`  
- 某些旧版模型（如 `qwen-vl-plus`）仍使用 `/v1/services/aigc/text-to-image/generation` 等旧路径，**不属于 `model experience` 体系**；请务必使用 `/v1/models/{model_id}/invoke` 统一入口，避免混用——该兼容性说明在 [视觉](../../raw/model-user-guide/model-experience/image-and-video-generation.md) 文档中已过时，实际应以本 Wiki 为准。

## 来源文档

- [模型调用](../../raw/model-user-guide/model-experience.md)


