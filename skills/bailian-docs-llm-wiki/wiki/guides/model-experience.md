# model experience

`model experience` 是百炼平台统一的模型调用抽象层，为开发者提供一致的 API 接口与请求结构，屏蔽底层模型类型（文本、视觉、语音等）和部署形态（托管/自定义）的差异。所有模型调用均通过 `/v1/models/{model_id}/invoke` 端点发起，支持同步响应与流式返回。该能力在 [模型调用](../../raw/model-user-guide/model-experience.md) 文档中定义了基础路由与通用行为。

## 支持的模型与功能

当前 `model experience` 支持以下模态模型的标准化调用：

- **文本生成**：如 Qwen-Max、Qwen-Plus，支持 `text-generation` 任务  
- **视觉生成**：包括图像生成（如 Wanx）、视频生成（如 Tongyi-Vid），对应 `image-generation` 和 `video-generation` 任务类型  
- **语音与音频**：TTS（`text-to-speech`）、ASR（`speech-to-text`）及音频理解（`audio-classification`）  
- **向量与重排**：嵌入（`embedding`）、重排（`rerank`）模型，适用于检索增强场景  
- **全模态**：支持多模态输入（图文混合、音视频+文本）的联合推理（详见 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md)）

> **注意**：原始文档中 [语音](raw/model-user-guide/model-experience/speech-and-audio.md) 的 `speech-to-text` 任务目前仅支持单声道 16kHz PCM 输入；而最新 SDK v3.2+ 已扩展支持 8kHz 与 WAV 封装，实际兼容性请以 [模型调用](../../raw/model-user-guide/model-experience.md) 中的 `Accept` 与 `Content-Type` 规范为准。

## 关键参数

所有请求共用以下核心字段（JSON body）：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `input` | object | 是 | 模态特定输入结构，如 `{"prompt": "..."}`（文本）或 `{"image_url": "..."}`（视觉） |
| `parameters` | object | 否 | 模型级超参，如 `temperature`、`top_p`、`max_tokens`；部分模态不支持全部参数（如 `rerank` 模型忽略 `temperature`） |
| `task` | string | 是 | 明确指定任务类型，必须与模型能力匹配，例如 `"text-generation"`、`"embedding"` |

参数合法性校验由平台前置执行；非法 `task` 值将直接返回 `400 Bad Request`。完整参数映射见 [文本](../../raw/model-user-guide/model-experience/text-generation-model.md)、[向量](../../raw/model-user-guide/model-experience/embedding-rerank-model.md) 等模态子文档。

## 使用方式

1. **构造请求**：`POST https://dashscope.aliyuncs.com/v1/models/{model_id}/invoke`  
2. **设置 Header**：`Authorization: Bearer ${api_key}`，`Content-Type: application/json`  
3. **提交 Body**：按上述 `input`/`parameters`/`task` 结构组织 JSON  
4. **处理响应**：成功时返回 `200 OK`，`output` 字段包含结果；流式请求需设置 `stream: true` 并解析 SSE 响应  

示例（文本生成）：
```json
{
  "input": {"prompt": "写一首关于春天的五言绝句"},
  "parameters": {"temperature": 0.7, "max_tokens": 256},
  "task": "text-generation"
}
```

## 限制和注意事项

- 单次请求 `input` 总大小上限为 20 MB（视觉/语音类模型受此约束显著）  
- 流式响应仅对 `text-generation`、`text-to-speech` 和 `omni-modal` 任务生效；`embedding` 与 `rerank` 强制同步返回  
- 模型 ID 必须已开通权限且处于 `ACTIVE` 状态，未授权模型返回 `403 Forbidden`  
- > **注意**：[视觉](raw/model-user-guide/model-experience/image-and-video-generation.md) 文档中提及的 `negative_prompt` 参数，在当前 `model experience` v2.1 API 中尚未开放，调用将被静默忽略——该差异已在 [模型调用](../../raw/model-user-guide/model-experience.md) 的「已知限制」章节明确标注。

## 来源文档

- [模型调用](../../raw/model-user-guide/model-experience.md)


