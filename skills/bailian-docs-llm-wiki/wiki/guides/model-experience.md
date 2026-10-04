# model experience

模型体验（Model Experience）是百炼平台面向开发者提供的统一模型调用入口，支持多模态模型的快速接入与实验。通过该能力，开发者可基于标准 API 或 Web 控制台直接调用各类预置模型，无需自行部署或管理底层推理服务。所有模型均经过平台统一封装，提供一致的请求格式、鉴权机制与错误码体系。

## 支持的模型与功能

当前支持以下模型类别及对应能力：

- 文本生成（如 Qwen 系列大语言模型）  
- 视觉理解（图文理解、OCR、目标检测等）  
- 图片生成与编辑（文生图、图生图、局部重绘）  
- 视频生成与编辑（文生视频、视频扩时、关键帧编辑）  
- 世界模型（具身智能、环境建模与推理）  
- 3D 模型生成（TriPo 等结构化 3D 输出）  
- 语音合成（TTS）、音频生成、音乐生成  
- 语音识别（ASR）、语音转语音（S2S）  
- 全模态模型（跨文本/图像/音频/视频联合理解与生成）  
- [向量嵌入](../concepts/embedding.md)与重排序（embedding/rerank）  

详细能力说明请参阅 [模型体验](../../raw/model-user-guide/model-experience.md)。各子类模型的具体输入输出规范、示例和限制见其独立文档，例如 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md) 和 [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)。

## 关键参数

调用模型体验接口时，通用关键参数包括：

- `model`: 必填，模型 ID（如 `qwen-max`, `wanx-v1`, `speech-tts-16k`），需从 [模型体验](../../raw/model-user-guide/model-experience.md) 中列出的支持列表中选取  
- `input`: 必填，结构化输入数据，格式依模型类型而异（如文本生成为 `{"prompt": "..."}`，视觉理解为 `{"image_url": "...", "prompt": "..."}`）  
- `parameters`: 可选，控制生成行为（如 `temperature`, `top_p`, `max_tokens`），具体支持项以各模型文档为准  
- `stream`: 布尔值，是否启用流式响应（仅部分模型支持，详见 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)）

> **注意**：部分旧文档（如 [fun-music.md](../../raw/model-user-guide/model-experience/fun-music.md)）中仍引用已下线的 `music-gen-1.0` 模型 ID；实际可用模型请以控制台「模型体验」页实时列表或 [模型体验](../../raw/model-user-guide/model-experience.md) 中最新维护的链接为准。

## 使用方式

1. **Web 控制台**：进入「模型体验」页面，选择目标模型 → 配置参数 → 提交测试请求  
2. **API 调用**：使用 `POST /api/v1/services/aigc/{service}/models/{model}/invoke` 接口（`service` 对应模型类型，如 `text-generation`, `vision`, `audio-generation`）  
3. **SDK 支持**：Python SDK 中 `Bailian` 类提供 `call_model()` 方法，自动路由至对应 service  

所有调用均需携带有效 `Authorization` 头（Bearer [Token](../concepts/token.md)）。完整请求示例与错误处理逻辑见 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)。

## 限制和注意事项

- 单次请求最大输入长度因模型而异：文本类模型通常上限为 32K tokens，视觉类模型图像分辨率建议 ≤ 2048×2048 像素  
- 视频/3D/世界模型等计算密集型服务存在更严格的并发与配额限制，需在控制台申请提升  
- 音频类模型（如 [语音合成](https://help.aliyun.com/zh/model-studio/speech-synthesis)、[语音识别](https://help.aliyun.com/zh/model-studio/speech-recognition)）部分能力由独立语音服务提供，其 API 地址与鉴权方式与主模型体验接口不兼容  
- 所有模型输出内容须符合中国法律法规及平台内容安全策略，违规内容将被拦截并记录日志

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


