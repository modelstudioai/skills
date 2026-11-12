# model experience

`model experience` 是百炼平台统一的模型调用抽象层，为开发者提供一致的 API 接口与参数语义，屏蔽底层模型类型（文本、视觉、语音等）和部署形态（托管/自定义）的差异。所有模型能力均通过 `/v1/models/{model_id}/invoke` 统一路由接入，支持同步响应与流式返回。该设计已在 [模型调用](../../raw/model-user-guide/model-experience.md) 文档中明确规范。

## 支持的模型与功能

当前 `model experience` 覆盖以下模态能力，每类对应独立的模型族与专用输入/输出 schema：

- **文本生成**：支持大语言模型（LLM）的补全、对话、工具调用等，详见 [文本](../../raw/model-user-guide/model-experience/text-generation-model.md)  
- **视觉生成**：包括图像生成、编辑、理解及视频生成，参见 [视觉](../../raw/model-user-guide/model-experience/image-and-video-generation.md)  
- **语音与音频**：涵盖 TTS、ASR、音色克隆与音频理解，详见 [语音](../../raw/model-user-guide/model-experience/speech-and-audio.md)  
- **向量服务**：提供嵌入（embedding）与重排序（rerank）两类低延迟向量模型，见 [向量](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)  
- **全模态模型**：支持跨文本、图像、音频的联合推理，如多模态对话与内容生成，参考 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md)

> **注意**：`omni-modal` 模型在 v2.3.0 后已要求显式声明 `input_media_type` 字段，而旧版 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md) 文档未更新该约束，实际调用需以 SDK v2.3.1+ 或 OpenAPI Spec 为准。

## 关键参数

所有调用共用以下核心参数（位于请求 body）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `input` | object | 是 | 模态特定输入结构，例如文本模型为 `{ "messages": [...] }`，图像模型为 `{ "image_url": "..." }`；具体格式见各子文档 |
| `parameters` | object | 否 | 模型级超参，如 `temperature`, `top_p`, `max_tokens`（文本）、`seed`, `steps`（视觉）等；[文本](../../raw/model-user-guide/model-experience/text-generation-model.md) 和 [视觉](../../raw/model-user-guide/model-experience/image-and-video-generation.md) 的参数命名存在部分不一致，建议优先使用 SDK 封装的参数映射表 |
| `stream` | boolean | 否 | 是否启用流式响应（仅部分模型支持），默认 `false` |

## 使用方式

1. **获取模型 ID**：从控制台「模型中心」或 `GET /v1/models` 列表中选取目标模型（如 `qwen2.5-7b-chat`、`wanx-v1`、`sensevoice-1.0`）  
2. **构造请求**：  
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/v1/models/{model_id}/invoke" \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "input": { ... },
           "parameters": { ... }
         }'
   ```
3. **处理响应**：检查 `output` 字段中的 `text`、`image_url`、`audio_url` 或 `embedding` 等模态专属字段；流式响应需按 SSE 协议解析 `data:` 行。

## 限制和注意事项

- 单次请求 `input` 总大小上限为 16 MB（含 base64 编码图像/音频），超出将返回 `413 Payload Too Large`  
- 视觉与语音类模型暂不支持 `stream: true`，启用后将被静默忽略并返回完整响应  
- 向量模型（embedding/rerank）**不接受** `parameters` 字段，传入将导致 `400 Bad Request`；该行为与 [向量](../../raw/model-user-guide/model-experience/embedding-rerank-model.md) 文档描述一致  
- 所有模型调用均受配额与速率限制管控，具体阈值请查阅控制台「用量管理」，而非依赖 [模型调用](../../raw/model-user-guide/model-experience.md) 中的示例值（该文档未同步最新配额策略）

## 来源文档

- [模型调用](../../raw/model-user-guide/model-experience.md)


