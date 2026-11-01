# model experience

`model experience` 是百炼平台面向开发者提供的统一模型调用体验层，封装了多模态模型的接入、参数配置与结果解析逻辑，支持通过标准化 API 或 SDK 快速集成各类生成与理解能力。其核心目标是降低模型使用门槛，同时保持对底层模型特性的可控性。所有能力均基于 [原文标题](../../raw/model-user-guide/model-experience.md) 所列模块组织。

## 支持的模型与功能

当前 `model experience` 覆盖以下 12 类模型能力，每类对应独立文档说明具体输入输出格式、适用场景及典型示例：

- 文本生成（含对话、补全、摘要等）  
- 视觉理解（图文理解、OCR、图像分类）  
- 图片生成与编辑（文生图、图生图、局部重绘）  
- 视频生成与编辑（文生视频、视频扩时、关键帧控制）  
- 世界模型（具身推理、环境交互模拟）  
- 3D 模型生成（单图生成网格、支持 GLB 输出）  
- 语音合成（TTS，支持多音色、语速/语调调节）  
- 音频生成（背景音、音效、音乐片段生成）  
- 语音识别（ASR，支持多语种、带标点和时间戳）  
- 语音转语音（V2V，保留语义与情感的跨语言/音色转换）  
- 全模态（多模态联合理解与生成，如“看图说话+生成配图”）  
- 向量与重排序（文本嵌入、多向量检索、交叉重排）

详细能力清单与入口说明见 [原文标题](../../raw/model-user-guide/model-experience.md)。

## 关键参数

通用参数（适用于绝大多数模型）包括：

- `model`: 必填，模型标识符（如 `qwen-vl-plus`、`wanx-video-1.0`），需与 [原文标题](../../raw/model-user-guide/model-experience.md) 中各子模块文档所列型号严格一致；  
- `input`: 结构化输入对象，格式因模型类型而异（如视觉理解需 `{"image": "base64...", "text": "描述"}`，语音识别需 `{"audio_url": "https://..."}`）；  
- `parameters`: 可选，控制生成质量与行为（如 `temperature`, `top_p`, `max_output_tokens`, `seed`），具体支持项以各子模块文档为准；  
- `stream`: 布尔值，仅部分文本/语音类模型支持流式响应。

> **注意**：`parameters` 中 `max_output_tokens` 在文本生成模型中表示最大 token 数，但在视频生成模型中实际约束为最大帧数（非 token），该不一致性已在 [原文标题](../../raw/model-user-guide/model-experience/video-generate-edit-model.md) 中明确，但未在顶层文档同步更新，请以子模块文档为准。

## 使用方式

1. **API 调用**：向 `/v1/models/{model}/invoke` 发送 POST 请求，`Content-Type: application/json`，请求体包含 `input` 和 `parameters`；  
2. **SDK 调用**（Python/Java/Go）：使用 `ModelClient.invoke()` 方法，传入 `model`, `input`, `parameters` 字典；  
3. **批量调用**：仅支持文本生成、嵌入、ASR 等低延迟模型，需通过 `/v1/batch/invoke` 接口，详见各子模块文档。

所有调用均需携带有效的 `Authorization: Bearer <api_key>` 头。完整请求示例与错误码说明请参考 [原文标题](../../raw/model-user-guide/model-experience.md)。

## 限制和注意事项

- 单次请求 `input` 总大小上限为 50 MB（视频/音频类模型单独限制为 200 MB）；  
- 流式响应仅返回 `delta` 字段，不包含完整历史上下文，客户端需自行拼接；  
- 视觉理解与图片生成模型对图像分辨率有隐式要求（如不低于 256×256，不超过 2048×2048），超出将被自动缩放，可能影响精度；  
- 世界模型与全模态模型暂不支持[异步任务](../concepts/asynchronous-task.md)模式，超时时间为 120 秒，超时后连接关闭且不保证结果完整性；  
- 所有模型调用均受项目级 QPS 与总 [Token](../concepts/token.md)/Frame 配额限制，配额策略以控制台实时显示为准。

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


