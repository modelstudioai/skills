# model experience

`model experience` 是百炼平台统一的模型调用抽象层，为开发者提供一致的 API 接口与参数语义，屏蔽底层模型类型（文本、视觉、语音等）和部署形态（托管/自定义）的差异。所有模型均通过 `/v1/models/{model_id}/invoke` 端点发起请求，支持同步响应与流式返回。该能力在 [模型调用](../../raw/model-user-guide/model-experience.md) 文档中定义了基础路由与模块划分。

## 支持的模型与功能

当前 `model experience` 覆盖以下模型类别，每类对应独立的功能子集与输入输出规范：

- **文本生成**：支持补全、对话、结构化输出（JSON Schema）、工具调用（Function Calling）  
- **视觉生成**：图像生成（文生图、图生图）、视频生成（短时长）、图像理解（VLM）  
- **语音处理**：语音转文字（ASR）、文字转语音（TTS）、语音识别与合成联合任务  
- **向量服务**：文本嵌入（embedding）、重排序（rerank），支持批量与单条请求  
- **全模态**：多模态输入（如图文混合 [prompt](prompt.md)）→ 多模态输出（如带图的文本响应），详见 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md)

> **注意**：[语音](../../raw/model-user-guide/model-experience/speech-and-audio.md) 文档中提及的“实时流式 TTS”功能尚未在 v1.2.0 的 `model experience` 统一接口中开放，需调用独立 `/v1/audio/speech` 专用端点，此为临时兼容设计，将在 v1.3.0 合并。

## 关键参数

所有模型调用共用以下核心参数（位于请求 body）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `input` | object | 是 | 模型输入数据，结构依模型类型而异（如 `text` 字段用于文本模型，`image_url` + `prompt` 用于 VLM） |
| `parameters` | object | 否 | 控制生成行为，如 `temperature`、`top_p`、`max_tokens`（文本），`size`（图像），`sample_rate`（语音）等 |
| `stream` | boolean | 否 | 是否启用流式响应，默认 `false`；仅部分模型支持（见各子文档） |

参数语义与取值范围严格遵循各模型类型的规范，例如 `embedding-rerank-model.md` 中定义的 `return_documents: true` 仅对 rerank 模型生效，文本模型忽略该字段。完整参数映射请参考 [文本生成模型](../../raw/model-user-guide/model-experience/text-generation-model.md) 等子文档。

## 使用方式

1. **获取模型 ID**：从控制台「模型中心」或 `GET /v1/models` 列表中选取已启用的模型 ID（如 `qwen-max`、`wanx-v1`、`bge-m3`）  
2. **构造请求**：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/v1/models/{model_id}/invoke" \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "input": {"prompt": "你好"},
           "parameters": {"temperature": 0.7}
         }'
   ```
3. **处理响应**：成功时返回 `200`，结构为 `{ "output": { ... }, "usage": { ... } }`；流式响应以 `text/event-stream` 返回 SSE 格式事件。

详细请求/响应示例与错误码说明见 [模型调用](../../raw/model-user-guide/model-experience.md)。

## 限制和注意事项

- 单次请求 `input` 总大小上限为 16 MB（含 base64 图片、音频等二进制内容）  
- 流式响应仅支持文本生成、部分 VLM 和 ASR 模型；TTS 与 rerank 模型暂不支持 `stream=true`  
- 模型 ID 具有租户隔离性，跨项目调用需显式授权或使用共享模型池  
- 所有模型调用受配额与 QPS 限制，具体阈值以控制台「用量管理」为准  

> **注意**：`model experience` 的 `parameters` 中 `stop` 字符串数组长度最大为 4，超出将被静默截断——该限制未在 [文本生成模型](../../raw/model-user-guide/model-experience/text-generation-model.md) 中明确说明，但已在实际 API 行为中验证，建议客户端主动校验。

## 来源文档

- [模型调用](../../raw/model-user-guide/model-experience.md)


