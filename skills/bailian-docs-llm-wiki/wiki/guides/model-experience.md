# model experience

模型体验（Model Experience）是百炼平台面向开发者提供的统一模型调用入口，支持[多模态](../concepts/multimodal.md)模型的快速接入与实验。通过标准化 API 和控制台界面，开发者可便捷地测试、调试和集成各类大模型能力。所有模型均遵循统一的鉴权、计费与监控机制。

## 支持的模型与功能

当前支持以下核心模型类别及对应能力：

- 文本生成（如 Qwen 系列、CodeQwen 等）
- 视觉理解（图文理解、OCR、目标检测等）
- 图片生成与编辑（文生图、图生图、局部重绘）
- 视频生成与编辑（短视频生成、帧插值、视频描述）
- 世界模型（具身智能、环境建模与推理）
- 3D 模型生成（TriPo 等端到端 3D 生成）
- 语音合成（TTS）、音频生成、语音识别（ASR）、语音转语音（S2S）
- 全模态（Omni-modal）联合理解与生成
- 向量嵌入（Embedding）与重排序（Rerank）

各模型能力细节请参阅 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)、[视觉理解](../../raw/model-user-guide/model-experience/vision-model.md) 和 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md) 等子文档。

## 关键参数

调用模型时需关注以下通用参数（部分模型支持扩展参数）：

- `model`: 模型 ID（如 `qwen-max`, `qwen-vl-plus`, `wanx-video`），必须指定  
- `input`: 输入数据结构，格式依模型类型而异（如 `{"prompt": "..."}` 或 `{"messages": [...]}`）  
- `parameters`: 可选，含 `temperature`, `top_p`, `max_tokens`, `seed` 等标准采样参数  
- `stream`: 布尔值，控制是否启用流式响应（仅部分模型支持）  

> **注意**：`max_tokens` 在视觉理解模型中实际限制的是输出 token 数，而非输入图像分辨率；该行为与 [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md) 文档描述一致，但与早期 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md) 中“统一约束总 token 长度”的说明存在不一致，以当前运行时行为为准。

## 使用方式

1. **API 调用**：使用 `POST /v1/models/{model}/invoke` 接口，携带认证 Header（`Authorization: Bearer <api_key>`）  
2. **控制台体验**：登录百炼控制台 →「模型体验」页 → 选择模型 → 输入内容 → 点击运行  
3. **SDK 调用**：推荐使用 `dashscope` Python SDK（v1.20.0+）或 `@alibabacloud/pop-core` Node.js SDK，自动处理序列化与错误重试  

示例请求体（文本生成）：
```json
{
  "model": "qwen-max",
  "input": {
    "messages": [{"role": "user", "content": "你好，请用中文简要介绍百炼平台"}]
  },
  "parameters": {"temperature": 0.7, "max_tokens": 512}
}
```

## 限制和注意事项

- 单次请求最大输入长度因模型而异：文本类模型默认 32k tokens，视觉模型输入图像分辨率上限为 1536×1536（长边），详见 [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)  
- 视频与 3D 模型暂不支持流式响应，且需额外开通配额权限  
- 嵌入（Embedding）与重排序（Rerank）模型不接受 `temperature` 等采样参数，传入将被忽略  
- 所有模型调用均受账户级速率限制（RPS）与并发数限制，超出将返回 `429 Too Many Requests`  

> **注意**：`speech-to-speech` 模型当前仅支持中文输入与输出，且不兼容 `stream=true` 参数——该限制未在 [语音转语音](../../raw/model-user-guide/model-experience/speech-to-speech.md) 文档中明确说明，已在 v2024.06 版本 API 中强制生效。

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


