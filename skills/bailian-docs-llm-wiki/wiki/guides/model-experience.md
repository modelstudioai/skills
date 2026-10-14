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
- 全模态（多模态联合理解与生成，如图文音视频混合输入输出）  
- 向量与重排序（文本嵌入、多粒度向量编码、语义重排序）  

各模型能力详情请参阅 [模型体验](../../raw/model-user-guide/model-experience.md) 的子模块文档，例如 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md) 和 [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)。

## 关键参数

所有模型调用均需指定以下通用参数：  
- `model`: 必填，模型标识符（如 `qwen2.5-72b-instruct`, `wanx-v1.0`, `speech-tts-1.0`），须与 [模型体验](../../raw/model-user-guide/model-experience.md) 中列出的名称严格一致；  
- `input`: 结构化输入，格式依模型类型而异（如文本生成为 `{"prompt": "..."}`，视觉理解为 `{"image_url": "...", "prompt": "..."}`）；  
- `parameters`: 可选，控制生成行为（如 `temperature`, `top_p`, `max_tokens`），具体字段见各子模型文档，例如 [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md) 中定义的 `size`, `style`, `seed` 等。

> **注意**：部分旧版文档（如 `fun-music.md`）中列出的 `genre` 参数已废弃，实际生效参数以最新 OpenAPI Schema 为准，建议优先参考 [音频生成](../../raw/model-user-guide/model-experience/audio-generation.md) 和 [音乐生成](../../raw/model-user-guide/model-experience/fun-music.md) 的当前版本说明。

## 使用方式

1. **API 调用**：使用 `POST /v1/models/{model}/invoke` 接口，携带 `Authorization: Bearer <api_key>`；  
2. **控制台调试**：登录百炼控制台 →「模型体验」页 → 选择目标模型 → 填写输入并提交；  
3. **SDK 集成**：推荐使用 `dashscope` Python SDK（v1.20.0+）或 `@alibabacloud/pop-core` Node.js SDK，自动处理签名与重试逻辑。  

所有调用路径、错误码及示例均在对应子模型文档中提供，例如 [语音识别](../../raw/model-user-guide/model-experience/speech-recognition.md) 包含长音频分片上传与回调配置说明。

## 限制和注意事项

- 单次请求最大输入长度因模型而异：文本类模型默认 32k tokens，视觉类模型图像分辨率上限为 2048×2048（超限将自动缩放）；  
- 视频与 3D 模型生成任务为异步执行，需轮询 `GET /v1/tasks/{task_id}` 获取结果；  
- 全模态与世界模型暂不支持流式响应（`stream=false` 强制生效）；  
- 向量模型（如 `text-embedding-v3`）输出维度固定为 1024，不可配置；  
- 所有模型均按 token/千图/秒/分钟等维度计费，具体计费单元详见各模型文档，例如 [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md) 明确区分 embedding 与 rerank 的单价。

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


