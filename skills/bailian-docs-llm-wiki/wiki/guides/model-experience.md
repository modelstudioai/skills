# model experience

`model experience` 是百炼平台面向开发者提供的统一模型调用体验层，封装了多模态模型的接入、参数配置与结果解析逻辑，支持通过标准 API 或 SDK 快速集成。其核心目标是降低模型使用门槛，同时保持对底层模型能力的可控性与可观察性。所有功能均基于 [原文标题](../../raw/model-user-guide/model-experience.md) 所列能力体系构建。

## 支持的模型与功能

当前 `model experience` 覆盖以下模型类别（按模态与任务划分）：

- **文本生成**：支持对话、补全、摘要、代码生成等，详见 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)  
- **视觉理解**：图文问答、OCR、图像分类与描述，参见 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)  
- **生成类模型**：包括图片生成与编辑、视频生成与编辑、3D 模型生成（TriPo）、音乐生成（FunMusic）、音频生成等  
- **语音处理**：语音合成（TTS）、语音识别（ASR）、语音转语音（S2S），其中 TTS 和 ASR 的最新接口规范以阿里云 Model Studio 官方帮助文档为准（[原文标题](../../raw/model-user-guide/model-experience.md) 中仅作入口索引）  
- **检索增强**：向量嵌入（embedding）与重排序（rerank）模型，适用于 RAG 场景  

> **注意**：原始文档中列出的 `世界模型` 条目目前尚未在百炼控制台或 OpenAPI 中开放公测，实际调用将返回 `ModelNotAvailable` 错误；该能力状态与 [原文标题](../../raw/model-user-guide/model-experience.md) 的列表存在滞后，建议以控制台「模型广场」实时状态为准。

## 关键参数

所有模型调用共用以下基础参数（部分模型支持扩展参数）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型 ID（如 `qwen-max`, `qwen-vl-plus`, `wanx-video`），需与 [原文标题](../../raw/model-user-guide/model-experience.md) 中所列一致 |
| `input` | object | 是 | 输入内容结构体，格式依模型类型而异（如文本模型为 `{"prompt": "..."}`，视觉模型为 `{"image": "base64...", "prompt": "..."}`） |
| `parameters` | object | 否 | 模型推理参数，如 `temperature`, `top_p`, `max_tokens` 等；具体支持项见各子文档（如 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)） |

## 使用方式

1. **API 调用**：通过 `/v1/services/aigc/{model}/invoke` 接口发起 POST 请求，需携带 `Authorization: Bearer <access_token>`  
2. **SDK 调用**：推荐使用 `dashscope` Python SDK（≥1.20.0）或 `@alibabacloud/tea-openapi` Node.js SDK，初始化时指定 `model` 即可自动路由至对应服务  
3. **控制台调试**：在「模型体验」页选择模型 → 配置输入与参数 → 点击「运行」，响应结构与 API 一致  

## 限制和注意事项

- 单次请求最大输入长度因模型而异：文本模型上限为 32768 tokens（`qwen-max`），视觉模型图像尺寸不超过 2048×2048 像素，视频生成最长 5 秒  
- 免费额度仅限新用户首月，超出后按模型调用量计费（详见各子文档定价说明）  
- 所有生成类模型（图片/视频/3D/音乐）输出内容受《生成式 AI 服务管理暂行办法》约束，禁止生成违法、侵权或违背公序良俗内容  
- `语音识别` 和 `语音合成` 的实际可用模型列表与参数范围，请以 [原文标题](../../raw/model-user-guide/model-experience.md) 中链接的 Model Studio 官方文档为准，百炼平台不额外封装其专属参数（如 `voice`、`sample_rate`）

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


