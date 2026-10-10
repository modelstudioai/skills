# model experience

模型体验（Model Experience）是百炼平台面向开发者提供的统一模型调用入口，支持多模态模型的快速接入与实验。通过标准化 API 和控制台界面，开发者可便捷地测试、调试和集成各类大模型能力。所有模型均遵循统一的鉴权、计费与限流机制。

## 支持的模型与功能

当前支持以下核心模型类别及对应能力：  
- 文本生成（含对话、补全、摘要等）  
- 视觉理解（图像分类、OCR、多图推理）  
- 图片生成与编辑（文生图、图生图、局部重绘）  
- 视频生成与编辑（文生视频、视频扩时、关键帧编辑）  
- 世界模型（环境建模、具身推理、仿真交互）  
- 3D 模型生成（单图/多图生成 `.glb` 格式，支持 TriPo 系列）  
- 语音合成（TTS，支持多语种与音色定制）  
- 音频生成（环境音、SFX、非音乐类音频）  
- 音乐生成（旋律、编曲、风格化生成）  
- 语音识别（ASR，支持中英文混合与长音频）  
- 语音转语音（跨语种/音色实时转换）  
- 全模态（多模态联合理解与生成，如图文音视频协同）  
- 向量与重排序（文本嵌入、多粒度重排，用于 RAG 场景）  

各模型详情请参阅 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)、[原文标题](../../raw/model-user-guide/model-experience/vision-model.md) 和 [原文标题](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。

## 关键参数

所有模型调用均需指定 `model`（模型 ID）、`input`（输入数据结构）和 `parameters`（可选配置）。通用关键参数包括：  
- `temperature`: 控制输出随机性（0.0–2.0，默认值因模型而异）  
- `top_p`: 核采样阈值（0.0–1.0）  
- `max_tokens`: 输出长度上限（注意：部分视觉/视频模型不支持该参数）  
- `stream`: 是否启用流式响应（布尔值，仅文本、语音合成等支持）  
- `seed`: 随机种子（确保结果可复现，部分模型如世界模型、3D 生成暂不支持）  

> **注意**：`max_tokens` 在 [原文标题](../../raw/model-user-guide/model-experience/video-generate-edit-model.md) 中被定义为“最大帧数”，而非 token 数，与文本模型语义不同；使用时需严格参照对应模型文档。

## 使用方式

1. **API 调用**：通过 `POST /v1/models/{model}/invoke` 发起请求，`model` 值须从平台模型列表获取（如 `qwen-vl-plus`、`wanx-video-1.0`）；  
2. **控制台体验**：登录百炼控制台 →「模型体验」页 → 选择模型 → 输入 prompt 或上传文件 → 点击运行；  
3. **SDK 集成**：推荐使用 `dashscope` Python SDK（v1.20.0+），自动处理鉴权与参数校验；  
4. **批量测试**：支持 CSV 文件上传进行批量推理（仅限文本、语音识别、嵌入等结构化输入模型）。

## 限制和注意事项

- 所有模型调用受账户配额与 QPS 限制，超限返回 `429 Too Many Requests`；  
- 视频、3D、世界模型等计算密集型任务存在单次请求时长上限（默认 300 秒），超时将中断并返回错误；  
- 图片/视频/3D 模型暂不支持 `stream: true`；  
- 语音识别（ASR）对音频格式要求严格：仅支持 WAV/MP3/FLAC，采样率必须为 16kHz 或 44.1kHz，单文件 ≤ 100MB；  
- 全模态模型（`omni-1.0`）目前仅接受 JSON 格式 `input`，不兼容原始二进制 multipart 请求 —— 此限制与 [原文标题](../../raw/model-user-guide/model-experience/omni-modal.md) 描述一致，但与早期 SDK 示例存在偏差，请以该文档为准。

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


