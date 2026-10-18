# model experience

`model experience` 是百炼平台面向开发者提供的统一模型调用体验层，封装了[多模态](../concepts/multi-modal.md)模型的接入、参数配置与结果解析逻辑，支持通过标准化 API 或 SDK 快速集成各类生成与理解能力。其核心目标是降低模型使用门槛，同时保持底层模型能力的完整性与可控性。所有能力均基于 [原文标题](../../raw/model-user-guide/model-experience.md) 所列模块组织。

## 支持的模型与功能

当前 `model experience` 覆盖以下 12 类模型能力：
- 文本生成（含对话、补全、指令遵循等）
- 视觉理解（图像分类、OCR、图文推理等）
- 图片生成与编辑（文生图、图生图、局部重绘）
- 视频生成与编辑（文生视频、视频扩时、关键帧控制）
- 世界模型（具身智能、环境建模与推理）
- 3D 模型生成（TriPo 系列，支持单图/多图输入生成 GLB）
- 语音合成（TTS，支持多音色、语速/语调调节）
- 音频生成（背景音、音效、音乐生成）
- 语音识别（ASR，支持中英文及多方言）
- 语音转语音（V2V，保留语义与情感的跨语言/音色转换）
- 全模态（Omni-modal，支持文本+图像+音频+视频混合输入与输出）
- 向量与重排序（Embedding 生成、Cross-Encoder 重排序）

各子能力细节请参阅对应文档，例如 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md) 和 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)。

## 关键参数

通用参数（适用于绝大多数模型）包括：
- `model`: 模型标识符（如 `qwen-vl-plus`, `wanx-video-1.0`, `speech-tts-1.2`），必须与 [原文标题](../../raw/model-user-guide/model-experience.md) 中列出的名称严格一致；
- `input`: 输入结构体，格式因模态而异（如文本为 `{"text": "..."}`，图像为 `{"image_url": "..."}`，[多模态](../concepts/multi-modal.md)为 `{"messages": [...]}`）；
- `parameters`: 可选字典，常见字段有 `temperature`（仅文本/生成类）、`top_p`、`max_output_tokens`、`seed`、`quality`（图片/视频）、`voice`（TTS）等；
- `stream`: 布尔值，控制是否启用流式响应（部分模型如 ASR、TTS、视频生成暂不支持流式）。

> **注意**：`parameters.seed` 在视觉生成类模型中默认行为与文本模型不同——部分图像模型（如 `wanx-image-2.1`）需显式设置 `seed=-1` 才启用随机种子，该行为与 [原文标题](../../raw/model-user-guide/model-experience/image-model.md) 描述一致，但与早期文档中“默认启用 seed”的说明矛盾，以本条为准。

## 使用方式

推荐通过百炼 SDK（Python/Java/Go）或 REST API 调用：
```python
from alibabacloud_bailian20231229 import models as bailian_models
client = Bailian20231229Client(...)
req = bailian_models.CallModelRequest(
    model="qwen-vl-plus",
    input={"messages": [{"role": "user", "content": [{"text": "描述这张图"}, {"image_url": "https://..."}]}]},
    parameters={"temperature": 0.7}
)
resp = client.call_model(req)
```
REST 接口地址为 `POST /api/v1/models/{model}/call`，认证方式为 Bearer [Token](../concepts/token.md)（AccessKey）。所有请求需携带 `X-DashScope-SSE: enable` 头以启用服务端事件流（若支持）。

## 限制和注意事项

- 单次请求最大 `input` 总大小：文本 ≤ 1MB，图像 ≤ 20MB（单张），视频 ≤ 500MB（单个），音频 ≤ 100MB；
- 并发限制：免费版 5 QPS，企业版按配额配置，超出返回 `429 Too Many Requests`；
- 视频与 3D 模型生成任务为异步模式，需轮询 `task_id` 获取结果，同步接口仅返回任务元信息；
- 全模态（Omni-modal）模型暂不支持 `stream=True`，且 `input.messages` 中 content 数组长度上限为 8；
- 语音识别（ASR）对采样率要求严格：仅支持 8kHz / 16kHz 单声道 PCM/WAV，其他格式需预处理，详见 [原文标题](../../raw/model-user-guide/model-experience/speech-recognition.md)。

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


