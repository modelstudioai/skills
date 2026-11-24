# model experience

`model experience` 是百炼平台统一的模型调用入口，提供标准化的 API 接口与 SDK 封装，支持文本生成、多模态理解与生成、语音处理、[向量嵌入](../concepts/vector-embedding.md)等能力。所有模型均通过 `model_id` 识别，请求体结构一致，便于开发者快速集成与切换。该能力在 [模型调用](../../raw/model-user-guide/model-experience.md) 文档中定义为平台核心交互范式。

## 支持的模型与功能

- **文本生成**：支持 Qwen 系列大语言模型（如 `qwen-max`, `qwen-plus`, `qwen-turbo`），适用于对话、摘要、代码生成等场景；详见 [文本](../../raw/model-user-guide/model-experience/text-generation-model.md)  
- **视觉理解与生成**：包括图像理解（`qwen-vl-plus`）、文生图（`wanx-image`）、视频理解（`qwen2-vl-video`）等；参考 [视觉](../../raw/model-user-guide/model-experience/image-and-video-generation.md)  
- **语音与音频**：支持语音转文字（ASR）、文字转语音（TTS）、语音内容分析；见 [语音](../../raw/model-user-guide/model-experience/speech-and-audio.md)  
- **向量与重排序**：提供通用嵌入模型（`text-embedding-v3`）及语义重排序模型（`bge-reranker-v2-m3`）；参见 [向量](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)  
- **全模态**：支持图文音视频混合输入的端到端推理（如 `qwen2.5-omni`），需显式声明 `input_type`；详情见 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md)

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | 是 | 模型唯一标识，必须与 [模型调用](../../raw/model-user-guide/model-experience.md) 中注册的 ID 一致 |
| `input` | object | 是 | 统一输入结构，格式依模型类型而异（如文本为 `{"messages": [...]}`，图像为 `{"image_url": "..."}`） |
| `parameters` | object | 否 | 模型特有参数，如 `temperature`, `top_p`, `max_tokens`（文本类）或 `seed`, `size`（图像类） |
| `stream` | boolean | 否 | 是否启用流式响应，默认 `false`；仅部分模型支持（如 `qwen-max` 支持，`text-embedding-v3` 不支持） |

> **注意**：`max_tokens` 在文本模型中表示输出长度上限，但在 `qwen2-vl-video` 中实际控制视频帧采样数，语义不一致，使用时需查阅对应子文档。

## 使用方式

1. **API 调用**：向 `https://dashscope.aliyuncs.com/api/v1/services/aigc/model-experience` 发送 POST 请求，携带 `Authorization: Bearer <api_key>`  
2. **SDK 调用**（Python 示例）：
   ```python
   from dashscope import Generation
   response = Generation.call(
       model='qwen-max',
       input={'messages': [{'role': 'user', 'content': '你好'}]},
       parameters={'temperature': 0.8}
   )
   ```
3. 所有模型共用同一 endpoint 和鉴权机制，无需为不同模态维护独立服务地址 —— 这是 [模型调用](../../raw/model-user-guide/model-experience.md) 的核心设计原则。

## 限制和注意事项

- 单次请求 `input` 总大小上限为 20 MB（含 base64 图像、音频文件等），超限将返回 `413 Payload Too Large`  
- 流式响应（`stream=True`）仅对文本生成类模型稳定支持；视觉/语音类模型即使设置 `stream=True`，也可能退化为非流式返回（参见 [视觉](../../raw/model-user-guide/model-experience/image-and-video-generation.md) 的兼容性说明）  
- 全模态模型（如 `qwen2.5-omni`）要求 `input` 中各模态字段命名严格匹配 schema（如 `image_urls`, `audio_urls`, `video_url`），字段缺失或错拼将导致 `400 Bad Request`  
- 嵌入模型（`text-embedding-v3`）不接受 `parameters` 字段，传入将被静默忽略 —— 此行为与 [向量](../../raw/model-user-guide/model-experience/embedding-rerank-model.md) 文档描述一致，但与早期 SDK 示例存在出入，建议以当前文档为准

## 来源文档

- [模型调用](../../raw/model-user-guide/model-experience.md)


