# model experience

`model experience` 是百炼平台统一的模型调用抽象层，为开发者提供一致的 API 接口与请求结构，屏蔽底层模型类型（文本、视觉、语音等）和部署形态（托管/自定义）的差异。所有模型均通过 `/v1/models/{model_id}/invoke` 端点发起调用，支持同步响应与流式返回。该能力在 [模型调用](../../raw/model-user-guide/model-experience.md) 文档中定义了基础路由与通用行为。

## 支持的模型与功能

当前 `model experience` 覆盖以下模型类别，每类对应独立的功能文档：

- **文本生成**：支持大语言模型（LLM）的 prompt-to-text、[函数调用](../concepts/function-calling.md)（Function Calling）、工具集成等，详见 [文本](../../raw/model-user-guide/model-experience/text-generation-model.md)  
- **视觉生成**：支持文生图、图生图、图像编辑及视频生成，输入支持多图+文本混合，详见 [视觉](../../raw/model-user-guide/model-experience/image-and-video-generation.md)  
- **语音处理**：涵盖语音识别（ASR）、语音合成（TTS）、语音转写与音色克隆，详见 [语音](../../raw/model-user-guide/model-experience/speech-and-audio.md)  
- **向量服务**：提供嵌入（embedding）与重排序（rerank）两类向量模型，统一使用 `input` 字段传入文本或文档列表，详见 [向量](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)  
- **全模态模型**：支持跨模态理解与生成（如图文问答、视频摘要），需显式声明 `multimodal_input` 结构，详见 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md)

> **注意**：部分旧版 SDK 示例中仍将 `rerank` 模型归类于 `text` 类型下，但根据最新 [向量](../../raw/model-user-guide/model-experience/embedding-rerank-model.md) 文档，`rerank` 已明确为独立模型类型，且不接受 `messages` 字段——请以该文档为准。

## 关键参数

所有调用共用以下核心字段（位于 JSON 请求体）：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `input` | object \| string | ✅ | 模型输入。文本类为 `string` 或 `{"messages": [...]}`；视觉/语音类为 `{"image": "...", "text": "..."}` 等结构化对象；向量类为 `string` 或 `string[]` |
| `parameters` | object | ❌ | 模型特有参数，如 `temperature`（文本）、`seed`（视觉）、`sample_rate`（语音）等，具体见各子文档 |
| `stream` | boolean | ❌ | 是否启用流式响应，默认 `false`；仅对支持流式的模型生效（如文本、部分语音模型） |

`model_id` 必须在路径中指定（如 `qwen2.5-7b-instruct`），不可在 `input` 或 `parameters` 中重复传入。

## 使用方式

1. **构造请求**：`POST https://dashscope.aliyuncs.com/v1/models/{model_id}/invoke`  
2. **设置 Header**：`Authorization: Bearer <api_key>`，`Content-Type: application/json`  
3. **提交 JSON Body**：按目标模型类型组织 `input` 和 `parameters`，参考对应子文档结构  
4. **解析响应**：成功时返回 `200`，结构为 `{ "output": {...}, "usage": {...} }`；流式响应以 `text/event-stream` 返回 SSE 格式数据  

示例（文本生成）：
```json
{
  "input": {
    "messages": [
      {"role": "user", "content": "你好"}
    ]
  },
  "parameters": {
    "temperature": 0.8
  }
}
```

## 限制和注意事项

- 单次请求 `input` 总大小上限为 **16 MB**（含 base64 编码图像/音频），超出将返回 `413 Payload Too Large`  
- 流式响应仅支持 `text-generation` 和 `speech-to-text` 类模型；`embedding`、`rerank` 及 `image-generation` 不支持 `stream=true`，强制设置将被忽略  
- 向量模型（`embedding` / `rerank`）**不接受 `messages` 字段**，若误传将返回 `400 Bad Request` —— 此行为与早期 [文本](../../raw/model-user-guide/model-experience/text-generation-model.md) 文档中“兼容性说明”存在冲突，实际以 [向量](../../raw/model-user-guide/model-experience/embedding-rerank-model.md) 文档为准  
- 全模态模型要求 `input` 中所有媒体字段（如 `image`, `video`, `audio`）必须为有效的 base64 URL（`data:<mime>;base64,<payload>`），纯文件路径或 OSS URL 不被接受

## 来源文档

- [模型调用](../../raw/model-user-guide/model-experience.md)


