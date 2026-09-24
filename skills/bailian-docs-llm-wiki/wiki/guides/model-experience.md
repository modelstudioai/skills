# model experience

`model experience` 是百炼平台面向开发者提供的统一模型调用体验层，封装了多模态模型的接入、参数配置与结果解析逻辑，支持通过标准 API 或 SDK 快速集成。其核心目标是降低模型使用门槛，同时保持对底层模型能力的可控性与可观察性。所有功能均基于 [原文标题](../../raw/model-user-guide/model-experience.md) 所列能力矩阵构建。

## 支持的模型与功能

当前 `model experience` 覆盖以下模型类型及对应能力：

- **文本生成**：支持对话、补全、摘要、代码生成等任务  
- **视觉理解**：图文理解、OCR、图像分类与细粒度推理  
- **图片生成与编辑**：文生图、图生图、局部重绘、尺寸适配  
- **视频生成与编辑**：短时长视频生成、关键帧控制、跨帧一致性优化  
- **世界模型**：具备环境建模与因果推理能力的具身智能接口  
- **3D模型生成**：支持 TriPo 等 3D 生成模型的端到端调用  
- **语音与音频**：语音合成（TTS）、语音识别（ASR）、语音转语音（TTS-TTS）、音频生成、音乐生成（详见 [原文标题](../../raw/model-user-guide/model-experience/audio-generation.md) 和 [原文标题](../../raw/model-user-guide/model-experience/fun-music.md)）  
- **全模态**：支持文本、图像、音频、视频等多模态输入联合推理  
- **向量与重排序**：嵌入（embedding）生成与检索结果重排序（rerank）

> **注意**：语音合成与语音识别的官方文档已迁移至 help.aliyun.com，但其 API 接口规范、鉴权方式及错误码仍与百炼平台保持一致；实际调用时请以 [原文标题](../../raw/model-user-guide/model-experience.md) 中的模块映射关系为准，避免直接依赖外部链接中的参数名。

## 关键参数

所有模型调用共用以下基础参数（部分模型支持扩展参数）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-vl-plus`、`wanx-video-1.0`、`tri-po-3d-1.2`，需从 [原文标题](../../raw/model-user-guide/model-experience.md) 列表中选取有效值 |
| `input` | object | 是 | 输入数据结构，格式依模型类型而异（如文本模型为 `{ "prompt": "..." }`，视觉模型为 `{ "image_url": "...", "text": "..." }`） |
| `parameters` | object | 否 | 模型特有参数，例如 `temperature`（文本）、`seed`（生成类）、`top_k`（rerank）等 |

不支持在单次请求中混合多个模型类型（如同时传入 `image_url` 和 `audio_url` 且未启用全模态模型）。

## 使用方式

1. **API 调用**：向 `https://dashscope.aliyuncs.com/api/v1/services/aigc/<service_type>/<model_name>` 发送 POST 请求（`service_type` 根据模型类别自动推导，如 `text-generation`、`vision`、`omni-modal`）  
2. **SDK 调用**：使用 `dashscope` Python SDK 时，统一调用 `ModelExperience.invoke()` 方法，传入 `model` 和 `input` 即可，无需手动拼接 service_type  
3. **响应结构**：返回统一格式的 `output` 字段（含 `text`、`image_url`、`audio_url` 等子字段）和 `usage`（token/credit 消耗统计）

## 限制和注意事项

- 单次请求最大输入长度：文本 ≤ 32768 tokens，图像 ≤ 4096×4096 像素，视频 ≤ 5 秒（H.264 编码），音频 ≤ 60 秒（WAV/MP3）  
- 全模态模型暂不支持自定义 [prompt](prompt.md) 模板，输入结构必须严格遵循 schema 定义  
- 3D 模型生成（TriPo）仅支持 `.glb` 输出格式，且需显式指定 `parameters.output_format = "glb"`  
- 视频生成与编辑模型的 `frame_rate` 参数默认为 `24`，不可设为 `0` 或负数，否则返回 `InvalidParameter` 错误  

> **注意**：`world-model` 当前仅开放白名单调用，其 `input` 结构与常规模型差异较大（需包含 `state`、`action_space` 等字段），详细定义请参考 [原文标题](../../raw/model-user-guide/model-experience/world-model.md)，而非通用模型文档。

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


