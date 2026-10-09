# model experience

模型体验（Model Experience）是百炼平台面向开发者提供的统一模型调用入口，支持多模态模型的快速接入与实验。通过标准化 API 和控制台界面，开发者可便捷地测试、调试和集成各类大模型能力。所有模型均遵循统一的鉴权、计费与监控机制。

## 支持的模型与功能

当前支持以下核心模型类别及对应能力：

- 文本生成（含对话、补全、摘要等）  
- 视觉理解（图像分类、OCR、图文理解）  
- 图片生成与编辑（文生图、图生图、局部重绘）  
- 视频生成与编辑（文生视频、视频扩时、关键帧编辑）  
- 世界模型（具身智能、环境建模与推理）  
- 3D 模型生成（单图生成 3D 网格，支持 GLB 导出）  
- 语音合成（TTS，多语种、多音色）  
- 音频生成（音效、环境声）  
- 音乐生成（旋律、编曲、风格迁移）  
- 语音识别（ASR，支持长音频流式识别）  
- 语音转语音（跨语言/音色转换）  
- 全模态（多输入模态联合理解与生成）  
- 向量与重排序（文本嵌入、稠密检索、结果重排）  

各模型能力详情请参阅 [模型体验](../../raw/model-user-guide/model-experience.md) 的子文档索引；例如，图片生成能力的具体参数与示例见 [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)，而 3D 生成流程则以 [3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md) 为准。

## 关键参数

通用请求参数包括：`model`（必需，如 `qwen-vl-plus`）、`input`（结构化输入，格式依模型类型而异）、`parameters`（可选，如 `temperature`, `top_p`, `seed`）。部分模型支持扩展字段，例如视觉模型需指定 `image_url` 或 `image_base64`，语音合成需传入 `voice` 和 `text`。所有参数定义与默认值均在对应子文档中明确说明，例如 [语音合成](../../raw/model-user-guide/model-experience/speech-synthesis.md) 中详细列出了 `speed`, `pitch`, `volume` 的取值范围与行为影响。

> **注意**：`max_tokens` 在文本生成模型中表示输出长度上限，但在视频生成模型中实际控制生成帧数（而非 token 数），该语义差异未在 [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md) 中显式强调，开发者需结合模型文档与实际响应验证。

## 使用方式

1. **API 调用**：使用 `POST /v1/models/{model}/invoke` 接口，携带 `Authorization: Bearer <api_key>` 头；  
2. **控制台调试**：登录百炼控制台 →「模型体验」页 → 选择目标模型 → 填写输入并提交；  
3. **SDK 集成**：Python SDK 提供 `BaiLianClient.invoke_model()` 方法，自动处理序列化与错误映射。  

所有调用均需遵守统一的输入 schema（详见 [模型体验](../../raw/model-user-guide/model-experience.md) 中的通用协议说明）。

## 限制和注意事项

- 单次请求最大输入长度因模型而异：文本类模型通常为 32k tokens，视觉模型单图分辨率上限为 1536×1536，视频模型单次生成最长 8 秒；  
- 免费额度仅限新用户首月，超出后按 [模型体验](../../raw/model-user-guide/model-experience.md) 所列计费项扣费；  
- 音频/视频类模型暂不支持异步回调，需轮询 `task_id` 获取结果；  
- `world-model` 类别尚处 Beta 阶段，接口稳定性与 SLA 不适用于生产环境；  
- 向量模型（如 `bge-m3`）返回的 embedding 维度固定，但重排序模型（如 `bge-reranker-v2-m3`）要求 query 与 candidates 分别传入，不可混用字段——该约束在 [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md) 中有明确定义。

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


