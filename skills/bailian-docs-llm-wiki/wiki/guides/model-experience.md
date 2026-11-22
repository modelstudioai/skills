# model experience

`model experience` 是百炼平台统一的模型调用入口，提供标准化的 API 接口与 SDK 封装，支持文本生成、[多模态](../concepts/multi-modal.md)理解与生成、语音处理、向量嵌入等能力。所有模型均通过 `model_id` 识别，请求体结构一致，便于开发者快速集成与切换。该能力在 [模型调用](../../raw/model-user-guide/model-experience.md) 文档中定义为平台核心交互范式。

## 支持的模型与功能

- **文本生成**：支持 Qwen 系列大语言模型（如 `qwen-max`, `qwen-plus`, `qwen-turbo`），适用于对话、摘要、代码生成等场景；详见 [文本](../../raw/model-user-guide/model-experience/text-generation-model.md)  
- **视觉理解与生成**：包括图像理解（`qwen-vl-plus`）、文生图（`wanx-image`）、视频理解（`qwen2-vl-video`）等；参考 [视觉](../../raw/model-user-guide/model-experience/image-and-video-generation.md)  
- **语音与音频**：支持语音转文字（ASR）、文字转语音（TTS）、语音识别与合成一体化模型（如 `qwen-audio`）；见 [语音](../../raw/model-user-guide/model-experience/speech-and-audio.md)  
- **向量与重排序**：提供嵌入模型（`text-embedding-v3`）和语义重排序模型（`bge-reranker-v2-m3`）；参见 [向量](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)  
- **全模态**：支持图文音视频混合输入的端到端推理（如 `qwen2.5-omni`），需显式声明 `input_type`；详情见 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md)

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | ✓ | 模型唯一标识，必须与文档中公布的 ID 完全一致（区分大小写） |
| `input` | object | ✓ | 输入内容，结构因模型类型而异（如 `text` 字段用于文本模型，`image_url` 用于视觉模型） |
| `parameters` | object | ✗ | 可选，控制生成行为（如 `temperature`, `top_p`, `max_tokens`）；部分模型不支持全部参数，以 [模型调用](../../raw/model-user-guide/model-experience.md) 中的兼容性表格为准 |
| `stream` | boolean | ✗ | 是否启用流式响应，默认 `false`；仅对文本/语音生成类模型有效 |

> **注意**：`parameters.max_tokens` 在视觉生成模型中实际对应输出图像分辨率控制（如 `1024x1024`），而非 token 数量，该语义差异已在 [视觉](../../raw/model-user-guide/model-experience/image-and-video-generation.md) 文档中明确，但与 [文本](../../raw/model-user-guide/model-experience/text-generation-model.md) 中的同名参数含义冲突，调用时须按模型类型分别理解。

## 使用方式

1. **API 调用**：向 `POST https://dashscope.aliyuncs.com/api/v1/services/aigc/model-experience` 发送 JSON 请求，携带 `Authorization: Bearer <api_key>` 头  
2. **SDK 调用（Python）**：
   ```python
   from dashscope import Model
   response = Model.call(model='qwen-turbo',
                         input={'text': '你好'},
                         parameters={'temperature': 0.7})
   ```
3. 所有模型均遵循统一错误码体系（如 `InvalidParameter`, `ModelNotSupported`），错误详情见 [模型调用](../../raw/model-user-guide/model-experience.md)

## 限制和注意事项

- 单次请求 `input` 总大小上限为 20 MB（含 base64 图片、音频二进制等）  
- 全模态模型（`qwen2.5-omni`）暂不支持流式响应，设置 `stream=true` 将被静默忽略  
- 嵌入模型（`text-embedding-v3`）不接受 `parameters` 字段，传入将返回 `InvalidParameter` 错误  
- 视频理解模型要求输入为公开可访问的 HTTPS URL，本地文件或私有 OSS 地址需先上传并获取公网地址 —— 此限制在 [视觉](../../raw/model-user-guide/model-experience/image-and-video-generation.md) 中明确，但 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md) 文档未同步说明，建议以视觉文档为准

## 来源文档

- [模型调用](../../raw/model-user-guide/model-experience.md)


