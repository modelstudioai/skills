# model experience

`model experience` 是百炼平台统一的模型调用抽象层，为开发者提供一致的 API 接口与参数语义，屏蔽底层模型类型（文本、视觉、语音等）和部署细节。它支持同步推理、流式响应、批量请求及[多模态](../concepts/multi-modal.md)协同调用，是构建 AI 应用的核心交互入口。详细设计目标见 [模型调用](../../raw/model-user-guide/model-experience.md)。

## 支持的模型与功能

当前 `model experience` 覆盖以下模型类别及其核心能力：

- **文本生成模型**：支持补全、对话、指令遵循、结构化输出（JSON Schema）、工具调用（function calling）  
- **视觉模型**：图像生成（文生图、图生图）、图像理解（OCR、描述、细粒度识别）、视频理解（关键帧分析、时序摘要）  
- **语音与音频模型**：语音转文字（ASR）、文字转语音（TTS）、语音增强、音频分类  
- **向量模型**：文本嵌入（embedding）、重排序（rerank），支持多语言与长上下文适配  
- **全模态模型**：原生支持图文音跨模态输入/输出，如“上传图片+语音提问→返回结构化 JSON 答案”  

各模型能力细节请参考对应子文档：[文本](../../raw/model-user-guide/model-experience/text-generation-model.md)、[视觉](../../raw/model-user-guide/model-experience/image-and-video-generation.md)、[语音](../../raw/model-user-guide/model-experience/speech-and-audio.md)。

## 关键参数

所有模型调用共用以下顶层参数（部分参数在特定模型类型中为必填或有特殊约束）：

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `model` | string | 模型唯一标识符（如 `qwen2.5-7b-chat`、`wanx-v1`），必须与实际部署模型匹配 |
| `input` | object | 模型输入内容，结构依模型类型而异（如文本模型为 `{"messages": [...]}`，视觉模型为 `{"image_url": "...", "prompt": "..."}`） |
| `parameters` | object | 推理控制参数，含 `temperature`、`top_p`、`max_tokens`、`stream`（布尔值）等；`stream=true` 时返回 SSE 流 |
| `extra` | object | 可选扩展字段，用于传递模型特有参数（如 TTS 的 `voice`、embedding 的 `return_type`） |

> **注意**：`parameters.max_tokens` 在视觉生成类模型中实际表示输出图像分辨率等级（如 `"max_tokens": 1024` 对应 1024×1024），而非 token 数量——该语义差异已在 [视觉](../../raw/model-user-guide/model-experience/image-and-video-generation.md) 文档中明确定义，但旧版 SDK 示例代码仍按文本逻辑注释，使用时请以该文档为准。

## 使用方式

1. **HTTP 调用**：向 `POST /v1/models/{model}/invoke` 发送 JSON 请求，需携带 `Authorization: Bearer <api_key>`  
2. **SDK 调用**（Python）：
   ```python
   from alibabacloud_bailian20231219 import models as bailian_models
   client = bailian_models.Client(...)
   response = client.invoke_model(
       model="qwen2.5-7b-chat",
       input={"messages": [{"role": "user", "content": "你好"}]},
       parameters={"temperature": 0.7, "stream": True}
   )
   ```
3. **流式处理**：当 `parameters.stream=true` 时，响应为 `text/event-stream`，每帧含 `data: {...}`，需按 SSE 协议解析；完整流式示例见 [文本](../../raw/model-user-guide/model-experience/text-generation-model.md)。

## 限制和注意事项

- 单次请求最大 `input` 大小：文本 ≤ 1MB，图像 ≤ 10MB（单图），视频 ≤ 100MB（单文件），音频 ≤ 50MB  
- 流式响应超时默认为 60 秒，不可配置；非流式请求超时为 30 秒（可通过 `X-Bailian-Timeout` Header 覆盖，上限 120 秒）  
- 全模态模型暂不支持 `parameters.return_full_response=true`（该参数在文本模型中用于返回原始 logits），尝试设置将被静默忽略  
- 所有模型均要求显式声明 `model` 字段，空值或无效 model ID 将返回 `400 Bad Request`，错误码 `InvalidModelId` —— 此行为与 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md) 文档中“支持自动路由”的旧描述矛盾，**请以当前接口契约为准，自动路由功能已下线**。

## 来源文档

- [模型调用](../../raw/model-user-guide/model-experience.md)


