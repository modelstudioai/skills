# model experience

模型体验（Model Experience）是百炼平台面向开发者提供的统一模型调用入口，支持多模态模型的快速接入与实验。通过标准化 API 和控制台界面，开发者可便捷地测试、调试和集成各类大模型能力。所有模型均遵循统一的鉴权、计费与监控机制。

## 支持的模型与功能

当前支持以下 12 类模型能力，覆盖文本、视觉、语音、音视频、3D 及全模态场景：

- 文本生成（如 Qwen 系列）  
- 视觉理解（如 Qwen-VL）  
- 图片生成与编辑（如 Wanx 图像生成）  
- 视频生成与编辑（如 Tongyi Tingwu 视频理解 + Wanx 视频生成）  
- 世界模型（基于环境感知与推理的交互式模型）  
- 3D 模型生成（通过 TriPo 实现文本到 3D 输出）  
- 语音合成（TTS）、音频生成、语音识别（ASR）、语音转语音（S2S）  
- 全模态（Omni-modal）联合理解与生成  
- [向量嵌入](../concepts/embedding.md)（Embedding）与重排序（Rerank）模型  

各子类能力细节请参阅 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)、[视觉理解](../../raw/model-user-guide/model-experience/vision-model.md) 和 [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。

## 关键参数

所有模型调用均支持以下通用参数（部分模型有扩展参数）：

- `model`: 必填，模型 ID（如 `qwen-max`, `wanx-v1`），需与 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md) 中列出的可用模型一致  
- `input`: 输入数据结构，格式依模型类型而异（如文本为 `{"prompt": "..."}`，图像为 `{"image_url": "..."}`）  
- `parameters`: 可选，控制生成行为（如 `temperature`, `top_p`, `max_tokens`）  
- `stream`: 布尔值，启用流式响应（仅部分模型支持，详见 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)）

> **注意**：`max_tokens` 在语音识别模型中实际表示音频时长上限（秒），而非 token 数量，该语义差异与 [原文标题](../../raw/model-user-guide/model-experience/speech-recognition.md) 的描述一致，但与其他文本模型文档存在术语不一致，建议以具体模型文档为准。

## 使用方式

1. **API 调用**：使用 `POST /v1/models/{model}/invoke`，携带认证 Header（`Authorization: Bearer <api_key>`）  
2. **控制台体验**：登录百炼控制台 →「模型体验」页 → 选择模型 → 输入示例 → 点击运行  
3. **SDK 集成**：推荐使用 `dashscope` Python SDK（v1.20.0+），自动处理参数序列化与错误重试  

所有调用均需提前在控制台开通对应模型权限；未授权模型将返回 `403 Forbidden`。

## 限制和注意事项

- 单次请求最大输入长度因模型而异：文本模型默认 32768 tokens，视觉模型图像分辨率上限为 1536×1536 像素（参见 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)）  
- 视频生成暂不支持自定义帧率与分辨率，仅提供预设档位（720p/1080p）  
- 3D 模型生成（TriPo）输出为 `.glb` 格式，暂不支持直接导出 `.obj` 或 `.fbx`  
- 全模态模型（Omni-modal）目前仅接受单图+单文本输入，多图或多轮交互暂未开放  
- 所有模型调用受配额与并发数限制，超出将触发 `429 Too Many Requests`，详情见配额管理页

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


