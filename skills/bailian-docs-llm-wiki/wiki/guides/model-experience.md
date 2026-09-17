# model experience

模型体验（Model Experience）是百炼平台面向开发者提供的统一模型调用入口，支持[多模态](../concepts/multi-modal.md)模型的快速接入与实验。通过该能力，开发者可基于标准 API 或 Web 控制台直接调用各类预置模型，无需自行部署或管理底层推理服务。所有模型均经过平台统一封装，提供一致的请求格式、鉴权机制与可观测性支持。

## 支持的模型与功能

当前支持以下模型类型及对应能力：

- **文本生成**：支持通用对话、指令遵循、代码生成等任务，详见 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)  
- **视觉理解**：支持图像分类、OCR、图文理解等，详见 [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md)  
- **图片生成与编辑**：支持文生图、图生图、局部重绘等，详见 [图片生成与编辑](../../raw/model-user-guide/model-experience/image-model.md)  
- **视频生成与编辑**：支持文生视频、视频扩时、关键帧控制等，详见 [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)  
- **3D模型生成**：集成 TriPo 3D 生成能力，支持单图生成可导出的 3D 网格，详见 [3D模型生成](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)  
- **语音与音乐**：语音合成、语音识别、语音转语音、音乐生成等功能由 Model Studio 提供，其接口规范与认证方式与百炼主平台保持一致（注意：部分文档链接已跳转至 help.aliyun.com，实际调用需使用百炼统一 `model-experience` 域名和 AK/SK 鉴权）  
- **全模态**：支持跨文本、图像、音频的联合理解与生成，详见 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md)  
- **向量与重排序**：提供嵌入（embedding）与语义重排序（rerank）模型，适用于 RAG 场景，详见 [向量与重排序](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)

> **注意**：原始文档中语音类能力（语音合成、语音识别、语音转语音）的链接指向 help.aliyun.com，但实际在百炼平台中应通过 `/v1/model-experience` 接口调用，且必须使用百炼颁发的 AccessKey（而非 Model Studio 独立密钥）。请以 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md) 中定义的通用鉴权与 endpoint 规范为准。

## 关键参数

所有模型调用共用以下核心参数（部分模型支持扩展参数）：

- `model`: 模型标识符（如 `qwen2.5-7b-instruct`, `wanx-v1`, `qwen-vl-plus`），需从 [模型列表](../../raw/model-user-guide/model-experience/text-generation-model.md) 获取有效值  
- `input`: 输入数据结构，格式依模型类型而异（如 text 字段用于文本模型，`image_url` + `text` 用于[多模态](../concepts/multi-modal.md)模型）  
- `parameters`: 可选，控制生成行为（如 `temperature`, `top_p`, `max_tokens`, `seed`）  
- `stream`: 布尔值，启用流式响应（仅部分模型支持）

## 使用方式

1. **API 调用**：向 `https://dashscope.aliyuncs.com/api/v1/model-experience` 发送 POST 请求，携带 `Authorization: Bearer <api_key>` 或 `X-DashScope-Access-Key` 头  
2. **控制台调试**：登录百炼控制台 →「模型体验」页 → 选择模型 → 填写输入 → 点击运行  
3. **SDK 调用**：推荐使用 `dashscope` Python SDK（v1.20.0+），初始化时指定 `model` 和 `input` 即可，详见 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md) 中的代码示例  

## 限制和注意事项

- 单次请求最大 `input` 数据大小为 16 MB（图片/视频需 Base64 编码后计入）  
- 全模态与视频模型暂不支持流式响应；3D 生成任务默认超时时间为 300 秒  
- 同一 `model` 标识符在不同 region 可能对应不同底层实例，跨 region 调用前请确认可用性  
- 语音类模型（ASR/TTS）在百炼平台中仅支持 HTTP 同步调用，不支持 WebSocket 或长连接；其返回字段命名与文本模型存在差异（如 `output.text` vs `output.speech_text`），请以各子文档为准  
- > **注意**：[全模态](../../raw/model-user-guide/model-experience/omni-modal.md) 文档中描述的“支持实时音视频流输入”为早期规划功能，当前生产环境尚未开放，实际仅支持静态图像+文本组合输入

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


