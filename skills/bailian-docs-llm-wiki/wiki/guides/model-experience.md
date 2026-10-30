# model experience

模型体验（Model Experience）是百炼平台面向开发者提供的统一模型调用入口，支持多模态模型的快速接入与实验。通过标准化 API 和控制台界面，开发者可便捷地测试、调试和集成各类大模型能力。所有模型均遵循统一的鉴权、计费与监控机制。

## 支持的模型与功能

当前支持以下核心模型类别及对应能力：

- 文本生成（如 Qwen 系列、CodeQwen 等）
- 视觉理解（图文理解、OCR、目标检测等）
- 图片生成与编辑（文生图、图生图、局部重绘）
- 视频生成与编辑（短视频生成、帧插值、视频描述）
- 世界模型（具身智能、环境建模与推理）
- 3D 模型生成（TriPo 等端到端 3D 生成）
- 语音合成（TTS）、音频生成（BGM、音效）、语音识别（ASR）、语音转语音（S2S）
- 全模态（Omni-modal）联合理解与生成
- [向量嵌入](../concepts/embedding.md)（Embedding）与重排序（Rerank）

各模型能力详情请参阅 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md)、[视觉理解](../../raw/model-user-guide/model-experience/vision-model.md) 和 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md) 等子文档。

## 关键参数

调用模型时需关注以下通用参数（部分模型支持扩展参数）：

- `model`: 模型 ID（如 `qwen-max`, `qwen-vl-plus`, `wanx-video`），必须指定  
- `input`: 输入数据结构，格式依模型类型而异（如 `{"prompt": "..."}` 或 `{"messages": [...]}`）  
- `parameters`: 可选配置，常见字段包括 `temperature`（0.0–2.0）、`top_p`、`max_tokens`、`seed`（确定性控制）  
- `stream`: 布尔值，启用流式响应（仅部分文本/语音模型支持）  

> **注意**：`max_tokens` 在视觉理解模型中实际表示输出 token 上限，而非输入长度限制；该行为与 [文本生成](../../raw/model-user-guide/model-experience/text-generation-model.md) 中的语义一致，但与早期 [视觉理解](../../raw/model-user-guide/model-experience/vision-model.md) 文档中“max_tokens 控制图像分辨率”的过时描述矛盾，请以当前 API 行为为准。

## 使用方式

1. **控制台体验**：登录百炼控制台 → 进入「模型体验」页 → 选择模型 → 填写输入 → 点击「运行」  
2. **API 调用**：使用 `POST /v1/models/{model}/invoke` 接口，携带 `Authorization: Bearer <api_key>` 头部  
3. **SDK 集成**：推荐使用 `dashscope` Python SDK（v1.20.0+）或 `@alibabacloud/dashscope-nodejs-sdk`（v2.4.0+），自动处理序列化与错误重试  

示例（Python）：
```python
from dashscope import Generation
resp = Generation.call(model='qwen-max', prompt='你好')
```

## 限制和注意事项

- 单次请求最大输入长度因模型而异：文本类模型默认 32768 tokens，视觉/视频模型受文件大小限制（上传文件 ≤ 100 MB）  
- 所有模型调用均计入账户配额，超出后返回 `429 Too Many Requests`  
- 流式响应不支持 `world-model` 和 `tripo-3d` 类模型，尝试启用将被静默忽略  
- 语音识别（ASR）模型对非中文音频支持有限，建议优先使用 [语音识别](../../raw/model-user-guide/model-experience/speech-recognition.md) 文档中标注为 `multilingual` 的模型版本  
- 视频生成任务最长等待时间 120 秒，超时后返回 `504 Gateway Timeout`，需客户端主动轮询结果（参考 [视频生成与编辑](../../raw/model-user-guide/model-experience/video-generate-edit-model.md)）

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


