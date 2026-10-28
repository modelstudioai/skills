# model experience

`model experience` 是百炼平台面向开发者提供的统一模型调用体验层，封装了多模态模型的接入、参数配置与结果解析逻辑，支持通过标准化 API 或 SDK 快速集成各类生成与理解能力。其核心目标是降低模型使用门槛，同时保持对底层模型特性的可控性。所有能力均基于 [原文标题](../../raw/model-user-guide/model-experience.md) 所列模块组织。

## 支持的模型与功能

当前 `model experience` 覆盖以下 12 类能力，每类对应独立模型服务与专用接口：

- 文本生成（如 Qwen 系列大语言模型）  
- 视觉理解（图文多模态理解）  
- 图片生成与编辑（含文生图、图生图、局部重绘）  
- 视频生成与编辑（支持短时长视频生成与帧级编辑）  
- 世界模型（具身智能与环境交互模拟）  
- 3D 模型生成（基于 TriPo 架构的单图/多图生成）  
- 语音合成（TTS，支持多语种与音色控制）  
- 音频生成（背景音、音效、音乐片段生成）  
- 语音识别（ASR，支持中英文混合及方言适配）  
- 语音转语音（V2V，保留语义与韵律的跨语言/跨音色转换）  
- 全模态（Omni-modal，统一输入接口处理文本、图像、音频、视频混合输入）  
- 向量与重排序（Embedding 生成与 Rerank 排序，用于检索增强场景）  

详细能力说明见 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)、[原文标题](../../raw/model-user-guide/model-experience/vision-model.md) 及其他子文档。

## 关键参数

通用参数（适用于绝大多数模型）包括：

- `model`: 必填，模型标识符（如 `qwen-max`, `qwen-vl-plus`, `wanx-video-1.0`），需从 [原文标题](../../raw/model-user-guide/model-experience.md) 中所列能力对应文档确认可用值；  
- `input`: 结构化输入，格式依模型类型而异（如文本生成为 `{"prompt": "..."}`，视觉理解为 `{"image_url": "...", "prompt": "..."}`）；  
- `parameters`: 可选，控制生成行为（如 `temperature`, `top_p`, `max_output_tokens`），各模型支持范围不同，以具体子文档为准；  
- `stream`: 布尔值，启用流式响应（仅部分模型支持，如文本生成、语音合成）。

> **注意**：`parameters.max_output_tokens` 在视频生成模型中实际表示最大输出帧数而非 token 数，该语义差异未在 [原文标题](../../raw/model-user-guide/model-experience/video-generate-edit-model.md) 中明确说明，开发者需按帧率换算预期时长。

## 使用方式

推荐通过百炼 SDK（Python/Java/Go）调用，示例（Python）：

```python
from alibabacloud_bailian20231219 import models as bailian_models
from alibabacloud_bailian20231219.client import Client

client = Client(...)
req = bailian_models.ChatCompletionsRequest(
    model="qwen-max",
    input={"messages": [{"role": "user", "content": "你好"}]},
    parameters={"temperature": 0.7}
)
resp = client.chat_completions(req)
```

HTTP 直连方式需构造 POST 请求至 `/v1/chat/completions`（文本类）或 `/v1/models/{model}/invoke`（非文本类），认证头 `Authorization: Bearer <api_key>` 为必需项。

## 限制和注意事项

- 单次请求最大输入长度因模型而异：文本生成默认 32k tokens，视觉理解图像分辨率上限为 1536×1536 像素，视频生成最长支持 4 秒（@30fps）；  
- 所有模型均不支持跨区域调用（如杭州 Region 的 AK 不能调用上海 Region 的模型 endpoint）；  
- 3D 模型生成（TriPo）暂不支持流式响应，且 `input` 中 `image_url` 必须为公网可直连的 HTTPS 地址；  
- 全模态（Omni-modal）模型目前仅接受单图 + 文本组合输入，多图或多模态混合输入尚未开放；  
- 语音识别（ASR）对信噪比低于 10dB 的音频识别准确率显著下降，建议前端预处理降噪。

> **注意**：[原文标题](../../raw/model-user-guide/model-experience/speech-recognition.md) 中标注的“支持实时流式 ASR”为历史版本描述，当前 `model experience` 层仅提供同步识别接口，流式能力计划于 Q3 上线，届时将更新文档。

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


