# model experience

`model experience` 是百炼平台面向开发者提供的统一模型调用体验层，封装了多模态模型的接入、参数配置与结果解析逻辑，支持通过标准化 API 或 SDK 快速集成各类生成与理解能力。其核心目标是降低模型使用门槛，同时保持底层模型能力的完整性与可控性。所有能力均基于 [原文标题](../../raw/model-user-guide/model-experience.md) 所列模块组织。

## 支持的模型与功能

当前 `model experience` 覆盖以下 12 类模型能力，每类对应独立文档说明具体输入输出格式、典型场景及最佳实践：

- 文本生成（含对话、补全、指令遵循）  
- 视觉理解（图像分类、OCR、图文推理等）  
- 图片生成与编辑（文生图、图生图、局部重绘）  
- 视频生成与编辑（文生视频、视频扩时、关键帧控制）  
- 世界模型（具身智能、环境建模与动作规划）  
- 3D 模型生成（TriPo 系列，支持 GLB/OBJ 输出）  
- 语音合成（TTS，支持多语种与音色克隆）  
- 音频生成（背景音、音效、音乐生成）  
- 语音识别（ASR，支持长音频流式转写）  
- 语音转语音（V2V，保留语义与韵律的跨语言/音色转换）  
- 全模态（Omni-modal，支持文本+图像+音频+视频混合输入）  
- 向量与重排序（Embedding 生成、语义相似度计算、Rerank 排序）

> **注意**：`world-model` 的接口定义与 `omni-modal` 在 [原文标题](../../raw/model-user-guide/model-experience/world-model.md) 和 [原文标题](../../raw/model-user-guide/model-experience/omni-modal.md) 中存在部分参数命名不一致（如 `context_mode` vs `input_mode`），建议以最新版 SDK 的 `ModelExperienceClient` 初始化逻辑为准，避免直接拼接请求体。

## 关键参数

所有模型调用共用以下顶层参数（部分能力可选）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-vl-plus`、`wanx-video-1.0`、`speech-tts-1.2`，详见各子文档 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md) 等所列支持列表 |
| `input` | object | 是 | 模型特定输入结构，如 `{"prompt": "..."}` 或 `{"image_url": "...", "text": "..."}` |
| `parameters` | object | 否 | 控制生成行为，常见字段：`temperature`（仅文本/音频类）、`top_p`、`max_output_tokens`、`seed`、`enable_streaming` |
| `extra` | object | 否 | 扩展字段，用于传递能力特有参数（如视觉理解中的 `detail_level`，图片生成中的 `style_preset`） |

## 使用方式

推荐通过百炼官方 SDK（Python/Java/Go）调用：

```python
from alibabacloud_bailian20231219 import models as bailian_models
from alibabacloud_bailian20231219.client import Client

client = Client(...)
req = bailian_models.CallModelExperienceRequest(
    model="qwen-vl-plus",
    input={"text": "描述这张图", "image_url": "https://..."},
    parameters={"temperature": 0.5}
)
resp = client.call_model_experience(req)
```

HTTP 直连方式需 POST 到 `/api/v1/model/experience`，Header 中携带 `X-DashScope-Access-Token`，Body 为 JSON 格式。详细协议规范见 [原文标题](../../raw/model-user-guide/model-experience.md)。

## 限制和注意事项

- 单次请求最大 `input` 总大小为 50 MB（含 Base64 编码图像/音频）；视频文件限 120 秒、200 MB  
- `streaming` 模式仅对文本生成、语音合成、部分视频生成生效，其余类型返回完整响应  
- 多模态输入（如图文混合）必须使用 `omni-modal` 模型标识，不可混用 `qwen-vl-plus` + `audio_generation` 参数  
- 所有模型均按 token/秒或请求次数计费，具体配额与计费规则请参考对应子文档，例如 [原文标题](../../raw/model-user-guide/model-experience/speech-synthesis.md) 明确标注了 TTS 的字符计费粒度  
- `embedding-rerank-model` 不支持 streaming，且 `rerank` 请求中 `query` 字段长度上限为 2048 Unicode 字符

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


