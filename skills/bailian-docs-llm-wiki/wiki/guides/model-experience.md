# model experience

`model experience` 是百炼平台统一的模型调用抽象层，为开发者提供一致的 API 接口与参数语义，屏蔽底层模型类型（文本、视觉、语音等）和部署细节。它支持同步推理、流式响应、批量请求及多模态协同调用，是构建 AI 应用的核心交互入口。详细设计目标见 [模型调用](../../raw/model-user-guide/model-experience.md)。

## 支持的模型与功能

当前 `model experience` 覆盖以下模型类别及其核心能力：

- **文本生成模型**：支持补全、对话、指令遵循、结构化输出（JSON Schema）、工具调用（function calling）  
- **视觉模型**：图像生成（文生图、图生图）、图像理解（OCR、描述、细粒度识别）、视频理解（关键帧分析、时序摘要）  
- **语音与音频模型**：语音转文字（ASR）、文字转语音（TTS）、语音增强、音频分类  
- **向量模型**：文本嵌入（embedding）、重排序（rerank），支持多语言与长上下文适配  
- **全模态模型**：跨模态联合理解与生成（如图文混合输入→文本输出），需显式声明 `input_modality` 参数  

各子类能力详见 [文本](../../raw/model-user-guide/model-experience/text-generation-model.md)、[视觉](../../raw/model-user-guide/model-experience/image-and-video-generation.md) 和 [向量](../../raw/model-user-guide/model-experience/embedding-rerank-model.md) 等专项文档。

## 关键参数

所有调用共用以下基础参数（部分为可选）：

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `model` | string | 模型 ID（如 `qwen2.5-7b-chat`、`wanx-v1`），必须与所选能力匹配；不支持跨模态混用（如用文本模型传 image URL） |
| `input` | object | 输入内容容器，结构依模态而异：文本用 `{"messages": [...]}`，视觉用 `{"image_url": "..."}`，语音用 `{"audio_url": "..."}` |
| `parameters` | object | 模型级超参，如 `temperature`、`top_p`、`max_tokens`；**注意**：`max_tokens` 在视觉生成中表示输出图像分辨率等级（非 token 数），该语义差异已在 [视觉](../../raw/model-user-guide/model-experience/image-and-video-generation.md) 文档中明确，但旧版 [模型调用](../../raw/model-user-guide/model-experience.md) 中未同步更新说明，以专项文档为准 |
| `stream` | boolean | 是否启用流式响应（仅文本/语音生成支持） |

## 使用方式

1. **HTTP 调用**：向 `POST /v1/models/{model}/invoke` 发送 JSON 请求，需携带 `Authorization: Bearer <api_key>`  
2. **SDK 调用**（Python）：
   ```python
   from alibabacloud_bailian20231229 import models as bailian_models
   client = bailian_models.Client(...)
   response = client.invoke_model(
       model="qwen2.5-7b-chat",
       input={"messages": [{"role": "user", "content": "你好"}]},
       parameters={"temperature": 0.7}
   )
   ```
3. **流式处理**：设置 `stream=True` 后，响应体为 SSE 格式，每帧含 `delta` 或 `finish_reason` 字段；完整示例见 [文本](../../raw/model-user-guide/model-experience/text-generation-model.md)

## 限制和注意事项

- 单次请求 `input` 总大小上限为 16 MB（含 base64 编码图像/音频）；URL 引用资源需公网可访问且响应头含 `Content-Type`  
- 视觉与语音模型暂不支持 `batch_size > 1`；文本模型批量调用需使用 `/v1/batch/invoke` 端点  
- 全模态模型要求 `input` 中各模态字段命名严格匹配（如 `image_urls`, `audio_urls`），否则返回 `400 Bad Request`  
- > **注意**：文档 [模型调用](../../raw/model-user-guide/model-experience.md) 中列出的“语音”链接指向 `speech-and-audio.md`，但该文件实际已重命名为 `speech-audio.md`（无连字符），当前链接已失效；请直接查阅最新版 [语音](../../raw/model-user-guide/model-experience/speech-audio.md) 文档（路径已修正）  
- 所有模型均强制启用安全过滤，敏感内容将被拦截并返回 `finish_reason: "content_filter"`，不可绕过

## 来源文档

- [模型调用](../../raw/model-user-guide/model-experience.md)


