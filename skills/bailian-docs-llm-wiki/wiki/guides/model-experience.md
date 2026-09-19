# model experience

`model experience` 是百炼平台面向开发者提供的统一模型调用体验层，封装了[多模态](../concepts/multimodal.md)模型的接入、参数配置与结果解析逻辑，支持通过标准 API 或 SDK 快速集成文本、视觉、音视频、3D 等生成与理解能力。其核心目标是降低[多模态](../concepts/multimodal.md)模型使用门槛，同时保持底层模型能力的可扩展性与一致性。所有能力均基于 [原文标题](../../raw/model-user-guide/model-experience.md) 所列模块组织。

## 支持的模型与功能

当前 `model experience` 覆盖以下模型类型及对应功能：

- **文本生成**：支持大语言模型（LLM）的对话、补全、摘要等任务  
- **视觉理解**：图文[多模态](../concepts/multimodal.md)理解、OCR、图像分类与描述生成  
- **图片生成与编辑**：文生图、图生图、局部重绘、尺寸适配等  
- **视频生成与编辑**：文生视频、图生视频、视频剪辑与风格迁移  
- **3D模型生成**：支持 TriPo 3D 模型一键生成与导出（参见 [原文标题](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)）  
- **语音合成（TTS）与语音识别（ASR）**：对接阿里云 Model Studio 服务（详见 [原文标题](../../raw/model-user-guide/model-experience.md) 中的外部链接）  
- **音乐生成**：支持旋律、节奏、风格可控的音频生成（见 [原文标题](../../raw/model-user-guide/model-experience/fun-music.md)）  
- **全模态（Omni-modal）**：跨文本、图像、音频的联合理解与生成  
- **向量与重排序**：嵌入（embedding）生成与检索结果重排序（rerank）

> **注意**：原始文档中部分语音类能力（如语音合成、语音识别、语音转语音）指向外部 help.aliyun.com 链接，而其他能力均指向 `raw/` 下的本地文档。实际调用时需确认是否已统一接入 `model experience` 统一网关——若未接入，则需单独配置 Model Studio 凭据与 endpoint，不享受统一鉴权与限流策略。

## 关键参数

所有模型调用共用以下基础参数（部分模型支持扩展参数）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-max`, `wanx-v1`, `tripo-3d-2024`（完整列表见 [原文标题](../../raw/model-user-guide/model-experience.md)） |
| `input` | object | 是 | 模型输入数据结构，格式依模型类型而异（如文本模型为 `{"prompt": "..."}`，图像模型为 `{"image_url": "..."}`） |
| `parameters` | object | 否 | 模型推理参数，如 `temperature`, `top_p`, `seed`, `n`（生成数量）等；各模型支持项以对应子文档为准 |

## 使用方式

1. **API 调用**：向 `https://dashscope.aliyuncs.com/api/v1/services/aigc/<service_type>/completions` 发送 POST 请求（`<service_type>` 如 `text-generation`, `image-generation`, `omni-modal`）  
2. **SDK 调用**：使用 `dashscope` Python SDK（v1.20.0+）或 `@alibabacloud/dashscope-nodejs-sdk`（v2.5.0+），调用 `Generation.call()` / `MultiModalGeneration.call()` 等方法  
3. **输入构造**：严格遵循各子模型文档定义的 `input` schema，例如视觉理解需传 `image_url` 或 base64 编码图像，不可混用字段  

## 限制和注意事项

- 单次请求最大输入长度/大小依模型而异：文本模型上限 32768 tokens，图像模型单图不超过 20MB，视频模型单视频不超过 100MB  
- 免费额度仅覆盖部分模型（如 `qwen-turbo`, `wanx-v1`），高阶模型（如 `qwen-max`, `tripo-3d-2024`）需按量计费  
- 所有模型输出均带 `usage` 字段，含 `input_tokens`, `output_tokens`, `total_tokens`（对非 token 模型如图像/3D，`tokens` 字段为等效计算值）  
- 不同模型间 `parameters` 语义不完全兼容（如 `temperature` 对 TTS 无效），务必查阅对应子文档；例如 [原文标题](../../raw/model-user-guide/model-experience/image-model.md) 明确要求图像生成必须指定 `size` 参数，缺失将返回 400 错误

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


