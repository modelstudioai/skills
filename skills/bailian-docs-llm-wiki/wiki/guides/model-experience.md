# model experience

`model experience` 是百炼平台统一的模型调用入口，提供标准化的 API 接口与 SDK 封装，支持文本生成、多模态理解与生成、语音处理、向量嵌入等能力。所有模型均通过 `model_id` 识别，请求体结构一致，便于开发者快速集成与切换。该能力在 [模型调用](../../raw/model-user-guide/model-experience.md) 文档中定义为平台核心交互范式。

## 支持的模型与功能

- **文本生成**：支持 Qwen 系列大语言模型（如 `qwen-max`, `qwen-plus`, `qwen-turbo`），适用于对话、摘要、代码生成等场景；详见 [文本](../../raw/model-user-guide/model-experience/text-generation-model.md)  
- **视觉理解与生成**：包括图像理解（`qwen-vl-plus`）、文生图（`wanx-image`）、视频理解（`qwen2-vl-video`）等；参考 [视觉](../../raw/model-user-guide/model-experience/image-and-video-generation.md)  
- **语音与音频**：支持语音转文字（ASR）、文字转语音（TTS）、语音内容分析；见 [语音](../../raw/model-user-guide/model-experience/speech-and-audio.md)  
- **向量与重排序**：提供通用嵌入模型（`text-embedding-v3`）及语义重排序模型（`bge-reranker-v2-m3`）；参见 [向量](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)  
- **全模态**：支持图文音视频混合输入的端到端推理（如 `qwen2.5-omni`），需显式声明 `input_type`；详情见 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md)

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | 是 | 模型唯一标识，必须与文档中公布的 ID 完全一致（区分大小写） |
| `input` | object | 是 | 输入数据结构，格式依模型类型而异（如文本模型为 `{ "messages": [...] }`，视觉模型为 `{ "image_url": "...", "prompt": "..." }`） |
| `parameters` | object | 否 | 模型推理参数，常见字段：`temperature`（0.0–2.0）、`top_p`（0.1–1.0）、`max_tokens`（最大输出长度）；部分模型支持 `stream: true` 流式响应 |
| `enable_search` | boolean | 否 | 仅对支持 RAG 增强的文本模型有效（如 `qwen-max`），默认 `false` |

> **注意**：`max_tokens` 在视觉生成类模型中实际控制输出图像分辨率/帧数，而非 token 数量；该行为与 [文本](../../raw/model-user-guide/model-experience/text-generation-model.md) 中的语义不一致，使用时请以各子模型文档为准。

## 使用方式

1. **API 调用**：向 `https://dashscope.aliyuncs.com/api/v1/services/aigc/{service_type}/model` 发送 POST 请求（`service_type` 由模型类型推导，如文本为 `text-generation`，嵌入为 `embedding`）  
2. **SDK 调用**（Python 示例）：
   ```python
   from dashscope import Generation
   response = Generation.call(model='qwen-turbo',
                               messages=[{'role': 'user', 'content': '你好'}],
                               temperature=0.8)
   ```
3. 所有调用均需携带 `Authorization: Bearer <api_key>` 头；鉴权与配额策略统一由百炼平台管控。

## 限制和注意事项

- 单次请求 `input` 总大小上限为 20 MB（含 base64 图像、音频文件等二进制内容）  
- 视觉与语音类模型暂不支持批量请求（`batch_size > 1`），需逐条调用  
- 全模态模型（如 `qwen2.5-omni`）要求输入中至少包含一种非文本模态，纯文本输入将返回 400 错误  
- 某些旧版模型（如 `qwen1.5-7b-chat`）已进入维护期，其参数兼容性与错误码可能与 [模型调用](../../raw/model-user-guide/model-experience.md) 主文档描述存在偏差，建议优先选用 `qwen-*` 新系列 ID  
- 流式响应（`stream=True`）仅对文本生成与部分全模态模型生效；尝试在嵌入或重排序模型中启用将被静默忽略 —— 此行为未在 [向量](../../raw/model-user-guide/model-experience/embedding-rerank-model.md) 文档中明确说明，属隐式限制

## 来源文档

- [模型调用](../../raw/model-user-guide/model-experience.md)


