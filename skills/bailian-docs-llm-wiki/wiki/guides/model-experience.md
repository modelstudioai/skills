# model experience

`model experience` 是百炼平台面向开发者提供的统一模型调用体验层，封装了多模态模型的接入、参数配置与结果解析逻辑，支持通过标准化 API 或 SDK 快速集成各类生成与理解能力。其核心目标是降低模型使用门槛，同时保持底层模型能力的完整性与可控性。所有能力均基于 [原文标题](../../raw/model-user-guide/model-experience.md) 所列模块组织。

## 支持的模型与功能

当前 `model experience` 覆盖以下 12 类模型能力：
- 文本生成（含对话、补全、指令遵循等）
- 视觉理解（图像分类、OCR、图文推理等）
- 图片生成与编辑（文生图、图生图、局部重绘）
- 视频生成与编辑（文生视频、视频扩时、关键帧控制）
- 世界模型（具身智能、环境建模与交互模拟）
- 3D 模型生成（单图/多图生成 `.glb` 等格式，见 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)）
- 语音合成（TTS，支持多语种与音色定制）
- 音频生成（背景音、音效、BGM 生成）
- 语音识别（ASR，支持长音频流式识别）
- 语音转语音（V2V，保留语义与韵律的跨语言/音色转换）
- 全模态（多输入模态联合理解与生成，如“图片+语音+文本”协同推理）
- 向量与重排序（Embedding 生成、稠密检索、Cross-Encoder 重排序）

> **注意**：`world-model` 的实时仿真延迟要求（≤200ms）与 `video-generate-edit-model` 的最大输出时长（15s）在 [原文标题](../../raw/model-user-guide/model-experience/world-model.md) 和 [原文标题](../../raw/model-user-guide/model-experience/video-generate-edit-model.md) 中存在不一致表述；以最新版 `world-model.md`（v2.3.1）为准，视频生成模块已同步放宽至 30s。

## 关键参数

通用参数（适用于所有模型类型）：
- `model`: 必填，模型标识符（如 `qwen-vl-plus`、`wanx-video-1.0`），需与 [原文标题](../../raw/model-user-guide/model-experience.md) 中各子文档所列型号严格匹配；
- `input`: 结构化输入，格式依模型类型而异（如视觉模型需 `{"image": "base64..."}`，语音模型需 `{"audio": "base64..."}`）；
- `parameters`: 可选，包含 `temperature`、`top_p`、`max_tokens` 等通用采样参数，以及模型特有参数（如 `image_size`、`voice_id`）；
- `stream`: 布尔值，仅部分文本/语音模型支持流式响应。

## 使用方式

1. **API 调用**：向 `https://dashscope.aliyuncs.com/api/v1/services/aigc/<model_type>/<endpoint>` 发送 POST 请求（`<model_type>` 如 `text-generation`、`vision`）；  
2. **SDK 调用**：使用 `dashscope` Python SDK，示例：
   ```python
   from dashscope import MultiModalConversation
   response = MultiModalConversation.call(model='qwen-vl-plus', input={'messages': [{'role': 'user', 'content': [{'image': 'http://...'}, {'text': '描述这张图'}]}]})
   ```
3. 所有模型均支持[异步任务](../concepts/asynchronous-task.md)提交（`/async` 后缀端点）与轮询获取结果，适用于长耗时任务（如 3D 生成、视频生成）。

## 限制和注意事项

- 单次请求 `input` 总大小上限为 50MB（视频/3D 场景下建议 ≤20MB）；
- 免费试用额度按模型类型独立计费，超出后需绑定付费账号；
- `omni-modal` 模型暂不支持自定义 `parameters` 中的 `temperature`，该限制已在 [原文标题](../../raw/model-user-guide/model-experience/omni-modal.md) 中明确说明；
- 所有语音类模型（`speech-synthesis`、`speech-recognition` 等）输入音频必须为 PCM/WAV 格式，采样率 16kHz，单声道；MP3/AAC 需先转码。

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


