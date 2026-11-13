# model experience

`model experience` 是百炼平台统一的模型调用抽象层，为开发者提供一致的 API 接口与请求结构，屏蔽底层模型类型（文本、视觉、语音等）和部署形态（托管/自定义）的差异。所有模型调用均通过 `/v1/models/{model_id}/invoke` 端点发起，支持同步响应与流式返回。该能力在 [模型调用](../../raw/model-user-guide/model-experience.md) 文档中定义为平台核心交互范式。

## 支持的模型与功能

当前 `model experience` 支持以下模态模型的标准化调用：

- **文本生成模型**：如 Qwen-Max、Qwen-Plus，支持 prompt 补全、[函数调用](../concepts/function-calling.md)（tool calling）、多轮对话上下文管理  
- **视觉模型**：包括图像生成（如 Wanx）、图像理解（如 Qwen-VL）、视频理解（如 Qwen2-VL），详见 [视觉](../../raw/model-user-guide/model-experience/image-and-video-generation.md)  
- **语音模型**：涵盖语音转文字（ASR）、文字转语音（TTS）、语音识别与合成联合任务  
- **向量模型**：支持 embedding 生成与重排序（rerank），适用于检索增强场景  
- **全模态模型**：如 Qwen2.5-Omni，可统一处理文本、图像、音频输入并生成多模态输出，其能力边界见 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md)

> **注意**：部分旧版文档（如 `raw/model-user-guide/text-generation.md`）仍将 `text-generation` 视为独立调用路径，但自 v2.3 起已全部归入 `model experience` 统一入口，实际使用应以 [模型调用](../../raw/model-user-guide/model-experience.md) 为准。

## 关键参数

所有请求共用以下核心字段（JSON body）：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `input` | object | 是 | 模态相关输入结构，例如 `{"messages": [...]}`（文本）、`{"image_url": "..."}`（视觉）或 `{"audio_url": "..."}`（语音） |
| `parameters` | object | 否 | 模型推理参数，如 `temperature`、`top_p`、`max_tokens`；全模态模型额外支持 `modalities` 显式声明输入模态组合 |
| `stream` | boolean | 否 | `true` 时启用 SSE 流式响应；仅部分模型支持（如文本、部分全模态模型） |

参数语义与取值范围需结合具体模型文档确认，例如 embedding 模型不接受 `temperature`，而 rerank 模型要求 `input` 中必须包含 `query` 和 `documents` 字段 —— 参考 [向量](../../raw/model-user-guide/model-experience/embedding-rerank-model.md)。

## 使用方式

1. **获取模型 ID**：从控制台「模型服务」页或 `GET /v1/models` API 获取可用模型列表，注意区分 `type`（如 `text-generation`、`embedding`）与 `status`（`available` 才可调用）  
2. **构造请求**：  
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/v1/models/qwen-max/invoke \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "input": {"messages": [{"role": "user", "content": "你好"}]},
           "parameters": {"temperature": 0.8}
         }'
   ```
3. **处理响应**：成功时返回 `output` 对象（含 `text`、`choices` 或 `embeddings` 等字段），错误时返回标准 `code` 与 `message`（如 `InvalidParameter`、`ModelNotReady`）

## 限制和注意事项

- 单次请求最大 `input` 大小为 16 MB（语音/视频 URL 需可公网访问且响应头含 `Content-Length`）  
- 流式响应（`stream=true`）下，`output` 字段为事件流，每帧含 `delta` 或 `finish_reason`，**不保证与非流式响应字段完全对齐**  
- 全模态模型对输入模态组合有严格校验（如 `image_url` + `audio_url` 同时存在时可能被拒绝），务必按 [全模态](../../raw/model-user-guide/model-experience/omni-modal.md) 文档验证输入结构  
- 模型 ID 具有地域绑定性（如 `qwen-max-cn-beijing` 仅限北京 Region 调用），跨 Region 调用将返回 `ResourceNotFound` 错误

## 来源文档

- [模型调用](../../raw/model-user-guide/model-experience.md)


