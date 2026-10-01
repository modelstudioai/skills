# model experience

`model experience` 是百炼平台面向开发者提供的统一模型调用体验层，封装了多模态模型的接入、参数配置与结果解析逻辑，支持通过标准 API 或 SDK 快速集成。其核心目标是降低模型使用门槛，同时保留对关键行为的细粒度控制。所有能力均基于 [原文标题](../../raw/model-user-guide/model-experience.md) 中定义的模型分类体系组织。

## 支持的模型与功能

当前 `model experience` 覆盖以下模型类型（按模态与任务划分）：
- **文本生成**：支持对话、摘要、代码生成等，详见 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model.md)；
- **视觉理解**：包括图文问答、OCR、图像描述等，参见 [原文标题](../../raw/model-user-guide/model-experience/vision-model.md)；
- **生成类模型**：涵盖图片生成与编辑、视频生成与编辑、3D 模型生成（TriPo）、音乐生成（FunMusic）、音频生成等；
- **语音处理**：语音合成（TTS）、语音识别（ASR）、语音转语音（S2S），其中 TTS 和 ASR 的最新接口规范以阿里云官方帮助文档为准；
- **基础能力**：向量嵌入（embedding）、重排序（rerank）、全模态联合推理（omni-modal）等。

> **注意**：原始文档中列出的语音合成、语音识别、语音转语音三类能力指向外部帮助中心链接（https://help.aliyun.com/zh/model-studio/...），而其他模型均指向内部 `raw/` 路径。这意味着语音类能力的参数结构、错误码及 SDK 封装可能与 `model experience` 统一调用协议不完全一致，建议优先查阅对应帮助文档并验证 `X-Model-Experience-Version` 头是否被正确识别。

## 关键参数

所有 `model experience` 接口共用以下核心参数（HTTP Header 或请求体字段）：
- `model`: 必填，模型标识符（如 `qwen-vl-plus`、`wanx-video-1.0`），需严格匹配 [原文标题](../../raw/model-user-guide/model-experience.md) 中列出的模型名；
- `input`: 输入数据结构，格式依模型类型而异（如文本为 `{"prompt": "..."}`，多模态为 `{"messages": [...]}`）；
- `parameters`: 可选，控制生成行为（如 `temperature`, `top_p`, `max_tokens`），具体支持项因模型而异，须参考各子文档；
- `stream`: 布尔值，启用流式响应（仅部分模型支持）。

## 使用方式

1. **API 调用**：向 `https://dashscope.aliyuncs.com/api/v1/services/aigc/<service>/call` 发送 POST 请求，`<service>` 由模型类型推导（如 `text-generation`、`vision`、`image-generation`）；
2. **SDK 调用**：使用 `dashscope` Python SDK 或 `@alibabacloud/dashscope-nodejs-sdk`，通过 `Generation.call()`、`MultiModalConversation.call()` 等方法传入 `model` 和 `input`；
3. **统一入口**：推荐使用 `/v1/model-experience/call`（Beta）作为泛化调用路径，自动路由至对应服务，该路径行为以 [原文标题](../../raw/model-user-guide/model-experience.md) 的最新版本为准。

## 限制和注意事项

- 单次请求最大输入长度依模型而定（如文本模型通常 ≤ 32768 tokens，视觉模型图像尺寸 ≤ 1536×1536 像素）；
- 视频/3D/世界模型等高资源消耗类型存在更严格的 QPS 与并发限制，需在控制台申请配额；
- `model experience` 不支持跨模型状态保持（如无法在一次会话中混合调用 `qwen-vl-plus` 和 `wanx-video-1.0`）；
- 所有模型输出中的 `usage` 字段（token 数、图像分辨率、时长等）为预估，实际计费以服务端日志为准。

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


