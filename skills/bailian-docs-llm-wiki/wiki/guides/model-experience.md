# model experience

模型体验（Model Experience）是百炼平台面向开发者提供的统一模型调用入口，支持多模态模型的快速接入与实验。通过标准化 API 和控制台界面，开发者可便捷地测试、调试和集成各类大模型能力。所有模型均遵循统一的鉴权、计费与限流机制。

## 支持的模型与功能

当前支持以下 12 类模型能力，覆盖文本、视觉、语音、音视频、3D、世界建模及检索增强等场景：

- 文本生成（如 Qwen 系列、Baichuan 等 LLM）
- 视觉理解（图文理解、OCR、图表解析）
- 图片生成与编辑（文生图、图生图、局部重绘）
- 视频生成与编辑（短视频生成、帧插值、剪辑指令执行）
- 世界模型（具身推理、环境模拟与交互预测）
- 3D 模型生成（TriPo 等单图生成 3D 网格与纹理）  
- 语音合成（TTS，支持多语种与情感控制）
- 音频生成（背景音、音效、音乐生成）
- 语音识别（ASR，支持中英文混合与方言适配）
- 语音转语音（跨语言/音色迁移）
- 全模态（Omni-Modal）：支持文本、图像、音频、视频任意组合输入与输出
- 向量与重排序（Embedding 与 Rerank 模型，用于 RAG 流水线）

各子类能力详情请参阅 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)、[视觉理解](../../raw/model-user-guide/model-experience/vision-model.md) 和 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md) 等对应文档。

## 关键参数

所有模型调用共用以下核心参数（部分模型支持扩展参数）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型 ID，如 `qwen-max`、`wanx-v1`、`speech-tts-1`；需从 [模型列表](../../raw/model-user-guide/model-experience.md) 获取有效值 |
| `input` | object | 是 | 输入数据结构，格式依模型类型而异（如文本生成为 `{ "prompt": "..." }`，视觉理解为 `{ "image_url": "...", "prompt": "..." }`） |
| `parameters` | object | 否 | 模型级超参，如 `temperature`、`top_p`、`seed`（文本类），或 `style`、`resolution`（图像类） |
| `enable_streaming` | boolean | 否 | 是否启用流式响应（仅部分文本/语音模型支持） |

> **注意**：`parameters` 中的 `max_tokens` 在部分旧版文档中被误标为 `max_output_tokens`，实际以 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md) 中定义为准；其他模态模型不支持该参数。

## 使用方式

1. **API 调用**：使用 `POST /v1/models/{model}/invoke` 接口，携带 `Authorization: Bearer <api_key>` 头；
2. **控制台调试**：登录百炼控制台 →「模型体验」页 → 选择模型 → 填写输入 → 点击「运行」；
3. **SDK 调用**：Python SDK 示例：
   ```python
   from alibabacloud_bailian20231219 import models as bailian_models
   client = BailianClient(...)
   response = client.invoke_model(
       model_id="qwen-plus",
       input={"prompt": "你好"},
       parameters={"temperature": 0.7}
   )
   ```

完整请求/响应格式与错误码详见 [模型体验](../../raw/model-user-guide/model-experience.md) 主文档。

## 限制和注意事项

- 单次请求最大输入长度因模型而异：文本类默认 32K tokens，视觉类图像 URL 需可公开访问且尺寸 ≤ 4096×4096px，视频类时长 ≤ 60 秒；
- 所有模型默认启用并发限流（免费版 1 QPS，企业版按配额配置），超限返回 `429 Too Many Requests`；
- 世界模型与 TriPo 3D 生成暂不支持流式响应和 `enable_streaming` 参数；
- 音频/视频类模型输出为 base64 编码或 OSS 直链（由 `response_format` 控制），需在调用前明确指定；
- > **注意**：[语音转语音](../../raw/model-user-guide/model-experience/speech-to-speech.md) 文档中提及的“实时低延迟模式”尚未全量上线，当前所有语音转语音请求均为离线批处理模式，实际延迟约 2–5 秒。

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


