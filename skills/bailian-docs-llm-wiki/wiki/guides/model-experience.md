# model experience

`model experience` 是百炼平台统一的模型调用抽象层，为开发者提供一致的 API 接口与参数语义，屏蔽底层模型类型（文本、视觉、语音等）和部署形态（托管/自定义）的差异。所有模型能力均通过 `/v1/models/{model_id}/invoke` 统一路由接入，支持同步响应与流式返回。该设计已在 [模型调用](../../raw/model-user-guide/model-experience.md) 文档中明确规范。

## 支持的模型与功能

当前 `model experience` 覆盖以下模态能力，对应独立子文档说明：

- **文本生成**：包括大语言模型（LLM）的 chat、completion 等模式，详见 [文本](../../raw/model-user-guide/model-experience/text-generation-model.md)  
- **视觉生成**：支持图像生成、编辑、理解及视频生成，详见 [视觉](../../raw/model-user-guide/model-experience/image-and-video-generation.md)  
- **语音处理**：涵盖 ASR、TTS、语音转写与音色克隆，详见 [语音](../../raw/model-user-guide/model-experience/speech-and-audio.md)  
- **向量服务**：提供 embedding 生成与重排序（rerank），详见 [向量](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)  
- **全模态交互**：支持多模态输入（如图文混合 prompt）与跨模态推理，详见 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md)

> **注意**：`omni-modal` 模型目前仅支持 `qwen2-vl` 系列，其他多模态模型（如 `qwen-audio`）仍需通过专用路由调用，该限制在 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md) 中未明确说明，以实际 SDK 版本 `v3.2.0+` 行为为准。

## 关键参数

所有调用共用以下核心参数（位于请求 body）：

- `model_id`（必填）：平台注册的模型唯一标识，非模型原始名称（如 `qwen2-72b-chat` 而非 `Qwen2-72B-Chat`）  
- `input`（必填）：结构化输入，格式依模态而异（如文本为 `{"messages": [...]}`，图像为 `{"image_url": "..."}`）  
- `parameters`（可选）：控制生成行为，通用字段包括 `temperature`、`top_p`、`max_tokens`；模态特有字段见各子文档  
- `stream`（可选，bool）：启用流式响应时设为 `true`，响应体为 SSE 格式  

参数校验优先级：平台级默认值 < 用户显式传入值 < 模型实例级配置（后者需通过控制台设置）。详细参数映射规则参见 [模型调用](../../raw/model-user-guide/model-experience.md)。

## 使用方式

1. **认证**：使用 `Authorization: Bearer <api_key>` 请求头  
2. **请求**：`POST https://dashscope.aliyuncs.com/api/v1/models/{model_id}/invoke`  
3. **响应**：成功时 HTTP 200，`output` 字段包含结果；错误时返回标准 `error.code` 与 `error.message`（如 `InvalidParameter`、`ModelNotReady`）  
4. **调试建议**：首次调用前，先用 `GET /v1/models/{model_id}` 查询模型元信息（含支持的模态、input schema），避免因 schema 不匹配导致 `BadRequest`  

完整示例与 SDK 封装（Python/Java/Go）见 [模型调用](../../raw/model-user-guide/model-experience.md)。

## 限制和注意事项

- 单次请求 `input` 总大小上限为 20 MB（含 base64 图像、音频等二进制内容）  
- 流式响应下，`max_tokens` 实际生效值可能受模型上下文窗口硬限制约束（如 `qwen2-72b-chat` 最大输出为 8192 tokens）  
- 向量模型（embedding/rerank）不支持 `stream: true`，强制忽略该参数  
- **重要**：`model_id` 必须与控制台「模型管理」中「服务 ID」完全一致；旧版文档中出现的 `model` 字段别名（如 `qwen-plus`）已废弃，新接口不再兼容 —— 此变更在 [文本](../../raw/model-user-guide/model-experience/text-generation-model.md) 中尚未更新，应以 OpenAPI Schema 为准。

## 来源文档

- [模型调用](../../raw/model-user-guide/model-experience.md)


