# model experience

模型体验（Model Experience）是百炼平台面向开发者提供的统一模型调用入口，支持多模态模型的快速接入与实验。通过该能力，开发者可基于标准 API 或 Web 控制台直接调用各类预置模型，无需自行部署或管理底层推理服务。所有模型均经过平台统一封装，提供一致的请求格式、鉴权机制与错误码体系。

## 支持的模型与功能

当前支持以下 12 类模型能力，覆盖文本、视觉、语音、音频、3D、视频及全模态场景：

- 文本生成（含对话、补全、摘要等）  
- 视觉理解（图像分类、OCR、图文理解等）  
- 图片生成与编辑（文生图、图生图、局部重绘）  
- 视频生成与编辑（文生视频、视频扩时、关键帧编辑）  
- 世界模型（具身智能、环境建模与交互模拟）  
- 3D 模型生成（单图生成可导出 GLB 的 3D 网格）  
- 语音合成（TTS）、音频生成（音效/环境声）、音乐生成（旋律+编曲）  
- 语音识别（ASR）、语音转语音（Voice Conversion）  
- 全模态（Multi-modal grounding，支持跨模态联合推理）  
- 向量与重排序（Embedding 生成、语义检索重排）  

详细能力说明见 [模型体验](../../raw/model-user-guide/model-experience.md)。各子类模型的具体输入输出规范、示例和典型用例，请参考对应子文档，例如 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md) 和 [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)。

## 关键参数

所有模型调用均需指定以下核心参数（部分模型支持扩展参数）：

- `model`: 模型标识符（如 `qwen-vl-plus`、`wanx-video`），必须与 [模型体验](../../raw/model-user-guide/model-experience.md) 中列出的名称严格一致；  
- `input`: JSON 对象，结构依模型类型而异（如文本模型为 `{"prompt": "..."}`，视觉模型为 `{"image_url": "...", "prompt": "..."}`）；  
- `parameters`: 可选，控制生成行为（如 `temperature`、`top_p`、`max_output_tokens`），具体字段以各子模型文档为准；  
- `stream`: 布尔值，启用流式响应（仅部分文本/语音模型支持）。  

> **注意**：部分旧文档（如 [fun-music.md](../../raw/model-user-guide/model-experience/fun-music.md)）中仍使用 `audio_generation` 作为模型名，但实际 API 要求使用 `fun-music` —— 请以 [模型体验](../../raw/model-user-guide/model-experience.md) 中的列表为准。

## 使用方式

1. **API 调用**：通过 `POST /v1/models/{model}/invoke` 接口发送请求，需携带 `Authorization: Bearer <api_key>`；  
2. **Web 控制台**：在「模型体验」页选择目标模型，填写输入后点击「运行」，支持实时调试与历史记录回溯；  
3. **SDK 调用**：推荐使用 `dashscope` Python SDK（v1.18.0+），调用 `Generation.call(model=..., input=...)` 即可；  
4. **批量任务**：对图片/视频/3D 等高耗时模型，建议使用异步模式（`/v1/models/{model}/async_invoke`），并通过 `get_result` 轮询状态。  

完整请求示例与错误处理逻辑详见 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md) 和 [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)。

## 限制和注意事项

- 所有模型调用受配额限制（QPS、并发数、单次最大 token 数），具体阈值因模型类型和用户等级而异；  
- 视频与 3D 模型暂不支持流式响应，且生成耗时较长（通常 30–120 秒），需合理设置客户端超时；  
- 语音识别（ASR）和语音合成（TTS）模型的采样率、编码格式有明确要求（如 WAV/PCM 16kHz），不兼容 MP3 直接上传；  
- 全模态与世界模型处于灰度阶段，仅对白名单用户开放，申请入口见 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md)；  
- 音频生成类模型（如 `audio-generation`）与音乐生成（`fun-music`）功能独立，不可混用参数或输入结构。

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


