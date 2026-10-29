# model experience

模型体验（Model Experience）是百炼平台面向开发者提供的统一模型调用入口，支持多模态模型的快速接入与实验。通过标准化 API 和控制台界面，开发者可便捷地测试、调试和集成各类大模型能力。所有模型均遵循统一的鉴权、计费与限流机制。

## 支持的模型与功能

当前支持以下 12 类模型能力，覆盖文本、视觉、语音、音视频、3D、世界建模及检索增强等场景：  
- 文本生成（含对话、补全、摘要等）  
- 视觉理解（图文理解、OCR、图表解析）  
- 图片生成与编辑（文生图、图生图、局部重绘）  
- 视频生成与编辑（文生视频、视频插帧、时序编辑）  
- 世界模型（具身智能、环境建模与推理）  
- 3D 模型生成（基于文本或图像生成可导出的 3D 网格）  
- 语音合成（TTS，支持多语种与音色定制）  
- 音频生成（背景音乐、音效、AI作曲）  
- 语音识别（ASR，支持长音频与实时流式识别）  
- 语音转语音（跨语言/音色转换）  
- 全模态（多输入模态联合理解与生成）  
- 向量与重排序（嵌入向量生成、语义相似度计算、结果重排）  

各能力详情请参阅对应子文档，例如 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)、[视觉理解](../../raw/model-user-guide/model-experience/vision-model.md) 和 [3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)。

## 关键参数

所有模型调用共用以下核心参数（部分模型支持扩展参数）：  
- `model`: 必填，模型标识符（如 `qwen-vl-plus`、`wanx-video-1.0`），需从 [模型列表](../../raw/model-user-guide/model-experience.md) 获取有效值；  
- `input`: 必填，结构化输入数据（格式依模型类型而异，如 `text` 字段用于文本模型，`image_url` + `prompt` 用于视觉模型）；  
- `parameters`: 可选，控制生成行为（如 `temperature`、`top_p`、`max_output_tokens`）；  
- `stream`: 布尔值，是否启用流式响应（仅部分模型支持，详见 [语音识别](../../raw/model-user-guide/model-experience/speech-recognition.md) 和 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md) 文档）。

> **注意**：`max_output_tokens` 在视频生成模型中实际生效上限为 512（而非文档中声明的 2048），该限制已在 [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md) 的最新版本中修正，旧版文档尚未同步更新。

## 使用方式

1. **控制台体验**：登录百炼控制台 → 进入「模型体验」页 → 选择目标模型 → 填写输入并提交，实时查看响应与 [Token](../concepts/token.md) 统计；  
2. **API 调用**：使用 `POST /v1/models/{model}/invoke` 接口，携带 `Authorization` 头（Bearer + API Key）；  
3. **SDK 集成**：推荐使用 `alibabacloud-bailian20231219` Python/Java SDK，自动处理序列化、重试与错误码映射（参考 [语音合成](../../raw/model-user-guide/model-experience/speech-synthesis.md) 中的 SDK 示例）。

## 限制和注意事项

- 单次请求最大输入长度因模型而异：文本模型默认 32768 tokens，视觉模型图像分辨率上限为 1536×1536 像素（超限将自动缩放）；  
- 视频与 3D 模型暂不支持批量并发调用，单账户每分钟限流 5 次；  
- 全模态与世界模型处于 Beta 阶段，接口稳定性与输出确定性低于 GA 模型，生产环境需谨慎评估；  
- 所有模型输出受内容安全策略过滤，敏感内容将被截断并返回 `400 Bad Request` 与 `content_blocked` 错误码；  
- 向量与重排序模型不支持 `stream: true`，且 `input` 中文本长度超过 8192 字符时将被静默截断——该行为与 [嵌入与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md) 文档描述一致，但未在控制台提示中体现，建议预处理输入。

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


